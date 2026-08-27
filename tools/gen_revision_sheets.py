#!/usr/bin/env python3
"""Generate printable one-page-per-area revision sheets.

For each topic area, extract every chapter's "Key takeaways" and "Last-minute
revision" blocks into docs/revision/sheets/<area>.md — an ultra-condensed sheet
for the final days. Regenerate: python tools/gen_revision_sheets.py
"""
from __future__ import annotations
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(DOCS, "revision", "sheets")
os.makedirs(OUT, exist_ok=True)

AREAS = {
 "php-web-security":"PHP & Web Security","http":"HTTP","architecture":"Symfony Architecture",
 "controllers":"Controllers","routing":"Routing","twig":"Templating (Twig)","forms":"Forms",
 "validation":"Data Validation","dependency-injection":"Dependency Injection","security":"Security",
 "http-caching":"HTTP Caching","console":"Console","testing":"Automated Tests","miscellaneous":"Miscellaneous","messenger":"Messenger",
}

def strip_links(text):
    """Convert [label](target) -> label so relative links don't break when the
    content is relocated into revision/sheets/."""
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

def section(text, header):
    """Return the body of a '## header' section up to the next '## '."""
    m = re.search(rf"(?ms)^##\s+{re.escape(header)}\s*$(.*?)(?=^##\s|\Z)", text)
    return strip_links(m.group(1).strip()) if m else ""

def title(text):
    m = re.search(r"(?m)^#\s+(.+)$", text)
    return m.group(1).strip() if m else "?"

for area, label in AREAS.items():
    files = sorted(
        f for f in glob.glob(os.path.join(DOCS, area, "*.md"))
        # Exclude the index hub (both languages: 'index.md' AND its
        # 'index.fr.md' sidecar — the old check only matched the former,
        # letting the French index's H1 leak in as a spurious empty
        # section) and every '*.fr.md' sidecar (this sheet is English-only;
        # including the French files duplicated every chapter's content).
        if os.path.basename(f) not in ("index.md", "index.fr.md")
        and not f.endswith(".fr.md")
    )
    L = [f"# Revision Sheet — {label}", "",
         "Ultra-condensed, print-friendly recap of every subchapter (key takeaways +"
         " last-minute cheat). For the final days. Full detail: "
         f"[{label}](../../{area}/index.md).", ""]
    for f in files:
        t = open(f, encoding="utf-8").read()
        name = title(t)
        kt = section(t, "Key takeaways")
        # Last-minute revision usually wraps a tip admonition; strip admonition markers.
        lm = section(t, "Last-minute revision")
        lm = re.sub(r'(?m)^\s*!!!.*tip.*$', '', lm)
        lm = re.sub(r'(?m)^\s{0,4}', '', lm).strip()
        L.append(f"## {name}")
        if kt:
            L.append(kt)
        if lm:
            L.append("")
            L.append("**Cheat:** " + " ".join(l.strip("- ").strip() for l in lm.splitlines() if l.strip() and not l.strip().startswith('"')))
        L.append("")
    open(os.path.join(OUT, f"{area}.md"), "w", encoding="utf-8").write("\n".join(L).rstrip()+"\n")
    print("sheet:", area)

# index
idx = ["# Revision Sheets", "",
       "Print-friendly, one-per-area condensed recaps for the final days — every "
       "subchapter's key takeaways + cheat, on a single page.", "",
       "!!! tip \"Print or save as PDF\"",
       "    Open a sheet and use your browser's Print → Save as PDF for offline "
       "revision on paper or phone.", "", "## Sheets", ""]
for area, label in AREAS.items():
    idx.append(f"- [{label}]({area}.md)")
idx += ["", "---", "", "<small>Back to [Revision Hub](../index.md)</small>"]
open(os.path.join(OUT, "index.md"), "w", encoding="utf-8").write("\n".join(idx)+"\n")
print("done: sheets index +", len(AREAS), "sheets")

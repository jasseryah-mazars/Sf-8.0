#!/usr/bin/env python3
"""Generate printable one-page-per-area revision sheets.

For each topic area, extract every chapter's "Key takeaways" and "Last-minute
revision" blocks into docs/revision/sheets/<area>.md — an ultra-condensed sheet
for the final days. Regenerate: python tools/gen_revision_sheets.py
"""
from __future__ import annotations
import os, re, glob
from generated_blocks import carry_over

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

def section(text, *headers):
    """Body of the first '## <header>' section found, up to the next '## '.

    Several spellings are accepted because the four-file learning journey renamed
    some of them (`## Key takeaways` also appears as `## Expert takeaways`).
    Returns None when none matches, so the caller can fail instead of silently
    emitting an empty sheet.
    """
    for header in headers:
        m = re.search(rf"(?ms)^##\s+{re.escape(header)}\s*$(.*?)(?=^##\s|\Z)", text)
        if m:
            return strip_links(m.group(1).strip())
    return None

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
        # A topic's learning-journey files are not chapters. They carry no
        # 'Key takeaways', so each would land in the sheet as a bare heading
        # ("## Topic Exam — Abstract Classes") with nothing under it.
        and not f.endswith(("-exercises.md", "-exam.md", "-flashcards.md"))
    )
    L = [f"# Revision Sheet — {label}", "",
         "Ultra-condensed, print-friendly recap of every subchapter (key takeaways +"
         " last-minute cheat). For the final days. Full detail: "
         f"[{label}](../../{area}/index.md).", ""]
    for f in files:
        t = open(f, encoding="utf-8").read()
        name = title(t)
        kt = section(t, "Key takeaways", "Expert takeaways")
        if kt is None:
            # Silence here is what made this generator dangerous: renaming a heading
            # emptied every sheet with no error at all. Name the file, the headings
            # looked for, and stop.
            raise SystemExit(
                f"gen_revision_sheets: FAIL — {os.path.relpath(f, ROOT)} has neither "
                f"'## Key takeaways' nor '## Expert takeaways'.\n"
                f"  The revision sheet for '{area}' would be emitted with that chapter "
                f"blank. Add one of those headings, or exclude the file deliberately."
            )
        # Last-minute revision usually wraps a tip admonition; strip admonition markers.
        lm = section(t, "Last-minute revision") or ""
        lm = re.sub(r'(?m)^\s*!!!.*tip.*$', '', lm)
        lm = re.sub(r'(?m)^\s{0,4}', '', lm).strip()
        L.append(f"## {name}")
        if kt:
            L.append(kt)
        if lm:
            L.append("")
            L.append("**Cheat:** " + " ".join(l.strip("- ").strip() for l in lm.splitlines() if l.strip() and not l.strip().startswith('"')))
        L.append("")
    out = os.path.join(OUT, f"{area}.md")
    text = carry_over(out, "\n".join(L).rstrip()+"\n")
    open(out, "w", encoding="utf-8").write(text)
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
out = os.path.join(OUT, "index.md")
text = carry_over(out, "\n".join(idx)+"\n")
open(out, "w", encoding="utf-8").write(text)
print("done: sheets index +", len(AREAS), "sheets")

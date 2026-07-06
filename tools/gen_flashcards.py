#!/usr/bin/env python3
"""Generate spaced-repetition flashcards from the curated quiz bank.

Writes one mobile-friendly, tap-to-reveal deck per area under
docs/revision/flashcards/, a deck index, and an Anki-importable CSV
(quiz/flashcards.csv). Front = question; back = correct answer(s) + why.
Justification: active recall + spaced repetition is the most efficient way to
memorise under exam time pressure. Run: python tools/gen_flashcards.py
"""
from __future__ import annotations
import os, glob, csv, html, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "revision", "flashcards")
os.makedirs(OUT, exist_ok=True)

TITLES = {
 "php-web-security":"PHP & Web Security","http":"HTTP","architecture":"Symfony Architecture",
 "controllers":"Controllers","routing":"Routing","twig":"Templating (Twig)","forms":"Forms",
 "validation":"Data Validation","dependency-injection":"Dependency Injection","security":"Security",
 "http-caching":"HTTP Caching","console":"Console","testing":"Automated Tests","miscellaneous":"Miscellaneous",
}

csv_rows = []
counts = {}
for f in sorted(glob.glob(os.path.join(ROOT, "quiz", "*.yml"))):
    stem = os.path.splitext(os.path.basename(f))[0]
    if stem not in TITLES:
        continue
    data = yaml.safe_load(open(f, encoding="utf-8")) or {}
    cards = []
    for cat in data.get("categories", []):
        for q in cat.get("questions", []):
            corr = [a["value"] for a in q.get("answers", []) if a.get("correct")]
            if not corr:
                continue
            cards.append((q["question"], corr, q.get("explanation", "").strip(), q.get("documentation", "")))
    counts[stem] = len(cards)
    title = TITLES[stem]
    lines = [f"# Flashcards — {title}", "",
             f"{len(cards)} cards. **Read the question, answer in your head, then tap to reveal.** "
             f"Mark the ones you miss and cycle them again.", "",
             "!!! tip \"How to drill\"", "    First pass: reveal every card. "
             "Later passes: only the ones you missed. Spread passes over days.", ""]
    for i, (qq, corr, expl, doc) in enumerate(cards, 1):
        ans = " ; ".join(corr)
        lines.append(f"??? question \"{i}. {qq}\"")
        lines.append(f"    **✅ {ans}**")
        if expl:
            lines.append("")
            lines.append(f"    {expl}")
        if doc:
            lines.append("")
            lines.append(f"    :material-book-open-variant: [Docs]({doc})")
        lines.append("")
        # Anki CSV: front, back, tag
        back = f"{ans}" + (f"<br><br>{html.escape(expl)}" if expl else "")
        csv_rows.append([qq, back, stem])
    lines += ["---", "", f"<small>Back to [Flashcards](index.md) · "
              f"[{title}](../../{stem}/index.md)</small>"]
    open(os.path.join(OUT, f"{stem}.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

# index page
idx = ["# Flashcards", "",
       "Active-recall decks generated from the practice-question bank — one per "
       "topic area. Tap a card to reveal the answer. Best used in short, repeated "
       "sessions (spaced repetition) on your phone.", "",
       "!!! abstract \"Why flashcards\"",
       "    Testing yourself (active recall) beats re-reading. Spacing the reviews "
       "beats cramming. These decks turn the 534-question bank into that workflow.", "",
       f"**Total cards:** {sum(counts.values())}", "", "## Decks", ""]
for stem, title in TITLES.items():
    idx.append(f"- [{title}]({stem}.md) — {counts.get(stem,0)} cards")
idx += ["", "## Anki import", "",
        "Prefer a real SRS app? Import [`quiz/flashcards.csv`](https://github.com/"
        "jasseryah-mazars/Sf-8.0/blob/main/quiz/flashcards.csv) into "
        "[Anki](https://apps.ankiweb.net/) (Basic note type; fields: Front, Back, "
        "Tags; the area tag lets you study one deck at a time).", "",
        "---", "", "<small>Back to [Revision Hub](../index.md)</small>"]
open(os.path.join(OUT, "index.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")

with open(os.path.join(ROOT, "quiz", "flashcards.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Front", "Back", "Tags"])
    w.writerows(csv_rows)

print(f"decks: {len(counts)} | total cards: {sum(counts.values())}")
print("per area:", ", ".join(f"{k}={v}" for k, v in counts.items()))

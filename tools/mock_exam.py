#!/usr/bin/env python3
"""Assemble a timed mock exam from the quiz bank (75 questions / 90 minutes).

Question count per area is weighted to mirror the real Symfony 8 exam emphasis
(Architecture / DI / Security / Messenger heavier; HTTP Caching lighter). Writes a
reproducible sample to docs/revision/mock-exam.md. Run: python tools/mock_exam.py
Options are shown UNMARKED so you actually answer; the key is collapsed per Q.
Justification: practising 75 Qs under a 90-min clock builds timing + stamina.
"""
from __future__ import annotations
import os, glob, random, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "revision", "mock-exam.md")

# Weights sum to 75 and mirror exam emphasis (see specs/GapAnalysis + Roadmap).
WEIGHTS = {
 "architecture":8,"dependency-injection":8,"security":8,"miscellaneous":10,"controllers":6,
 "forms":5,"routing":5,"twig":5,"http":5,"validation":4,"testing":4,"console":3,
 "php-web-security":3,"http-caching":1,
}
TITLES = {
 "php-web-security":"PHP & Web Security","http":"HTTP","architecture":"Architecture",
 "controllers":"Controllers","routing":"Routing","twig":"Twig","forms":"Forms",
 "validation":"Validation","dependency-injection":"Dependency Injection","security":"Security",
 "http-caching":"HTTP Caching","console":"Console","testing":"Testing","miscellaneous":"Miscellaneous",
}

def load():
    pool = {}
    for f in glob.glob(os.path.join(ROOT, "quiz", "*.yml")):
        stem = os.path.splitext(os.path.basename(f))[0]
        if stem not in WEIGHTS:
            continue
        qs = []
        for cat in (yaml.safe_load(open(f, encoding="utf-8")) or {}).get("categories", []):
            qs += cat.get("questions", [])
        pool[stem] = qs
    return pool

def build(seed=8):
    rng = random.Random(seed)
    pool = load()
    picked = []
    for stem, n in WEIGHTS.items():
        qs = pool.get(stem, [])[:]
        rng.shuffle(qs)
        for q in qs[:n]:
            picked.append((stem, q))
    rng.shuffle(picked)
    return picked

def render(picked):
    L = ["# Mock Exam (Exam Mode)", "",
         "!!! danger \"Exam-mode rules\"",
         "    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer "
         "every question (there is no negative marking). Multiple answers may be "
         "correct — the stem says how many. Reveal a key only after you have "
         "committed to an answer.", "",
         "!!! tip \"Timing\"",
         "    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep "
         "moving, and come back. Aim to finish with 10 minutes to review flags.", "",
         "??? info \"How this exam was built\"",
         "    75 questions sampled from the practice bank, weighted to mirror exam "
         "emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching "
         "lighter). Regenerate a fresh set with `python tools/mock_exam.py`.", "",
         "---", ""]
    for i, (stem, q) in enumerate(picked, 1):
        opts = [a["value"] for a in q.get("answers", [])]
        letters = "ABCDEFGH"
        L.append(f"**Q{i}.** {q['question']}  <small>_({TITLES[stem]})_</small>")
        L.append("")
        for j, o in enumerate(opts):
            L.append(f"- {letters[j]}. {o}")
        L.append("")
        corr = [letters[j] for j, a in enumerate(q.get("answers", [])) if a.get("correct")]
        expl = q.get("explanation", "").strip()
        doc = q.get("documentation", "")
        L.append(f"??? success \"Answer Q{i}\"")
        L.append(f"    **{', '.join(corr)}**")
        if expl:
            L.append("")
            L.append(f"    {expl}")
        if doc:
            L.append("")
            L.append(f"    :material-book-open-variant: [Docs]({doc})")
        L.append("")
    L += ["---", "", "<small>Back to [Revision Hub](index.md) · "
          "[Practice Quiz Bank](quiz.md)</small>"]
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    picked = build()
    open(OUT, "w", encoding="utf-8").write(render(picked))
    from collections import Counter
    c = Counter(s for s, _ in picked)
    print(f"mock exam: {len(picked)} questions ->", os.path.relpath(OUT, ROOT))
    print("distribution:", ", ".join(f"{TITLES[k]}={v}" for k, v in c.items()))

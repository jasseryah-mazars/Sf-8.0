#!/usr/bin/env python3
"""Generate a Chapter Exam per topic area from the Global Question Bank.

Each exam mixes all subchapters of the area and orders questions
progressively (easy → medium → hard). Answers are collapsed with full
explanations. Regenerate: python tools/gen_chapter_exams.py
"""
from __future__ import annotations
import os, glob, yaml
from generated_blocks import carry_over

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "exams")
os.makedirs(OUT, exist_ok=True)

AREAS = {
 "php-web-security":"PHP & Web Security","http":"HTTP","architecture":"Symfony Architecture",
 "controllers":"Controllers","routing":"Routing","twig":"Templating (Twig)","forms":"Forms",
 "validation":"Data Validation","dependency-injection":"Dependency Injection","security":"Security",
 "http-caching":"HTTP Caching","console":"Console","testing":"Automated Tests","miscellaneous":"Miscellaneous","messenger":"Messenger",
}
RANK = {"easy": 0, "medium": 1, "hard": 2}
LETTERS = "ABCDEFGH"

def questions(stem):
    f = os.path.join(ROOT, "quiz", f"{stem}.yml")
    if not os.path.exists(f):
        return []
    qs = []
    for cat in (yaml.safe_load(open(f, encoding="utf-8")) or {}).get("categories", []):
        qs += cat.get("questions", [])
    return qs

def render(area, label, qs):
    qs = sorted(qs, key=lambda q: RANK.get(q.get("difficulty"), 1))
    L = [f"# Chapter Exam — {label}", "",
         "!!! abstract \"How to use\"",
         f"    {len(qs)} questions spanning every subchapter of **{label}**, ordered "
         "easy → hard. Answer before revealing each key. For a timed, cross-topic "
         "paper use the [Mock Exams](../revision/mock-exam.md).", "",
         "!!! danger \"Not an official exam\"",
         "    Practice question, not an official exam question. This bank is "
         "community-authored and aligned with the syllabus — it is not sourced "
         "from, or reviewed by, the official Symfony 8 certification.", "",
         f"Full theory: [{label}](../{area}/index.md).", "", "---", ""]
    for i, q in enumerate(qs, 1):
        d = q.get("difficulty", "")
        t = q.get("type", "")
        tag = " · ".join(x for x in (d, t) if x)
        L.append(f"**Q{i}.** {q['question']}" + (f"  <small>_({tag})_</small>" if tag else ""))
        L.append("")
        ans = q.get("answers", [])
        for j, a in enumerate(ans):
            L.append(f"- {LETTERS[j]}. {a.get('value','')}")
        L.append("")
        corr = [LETTERS[j] for j, a in enumerate(ans) if a.get("correct")]
        L.append(f"??? success \"Answer Q{i}\"")
        L.append(f"    **{', '.join(corr)}**")
        expl = (q.get("explanation") or "").strip()
        if expl:
            L.append(""); L.append("    " + expl.replace("\n", "\n    "))
        doc = q.get("documentation") or ""
        if doc:
            L.append(""); L.append(f"    :material-book-open-variant: [Docs]({doc})")
        L.append("")
    L += ["---", "", f"<small>Back to [Chapter Exams](index.md) · [{label}](../{area}/index.md)</small>"]
    return "\n".join(L) + "\n"

counts = {}
for area, label in AREAS.items():
    qs = questions(area)
    counts[area] = len(qs)
    out = os.path.join(OUT, f"{area}.md")
    text = carry_over(out, render(area, label, qs))
    open(out, "w", encoding="utf-8").write(text)

idx = ["# Chapter Exams", "",
       "One exam per topic area — every subchapter mixed together, ordered "
       "progressively from easy to hard, with fully-explained answers. Sit one after "
       "finishing an area; use the [Mock Exams](../revision/mock-exam.md) for timed, "
       "whole-syllabus practice.", "", "## Exams", ""]
for area, label in AREAS.items():
    idx.append(f"- [{label}]({area}.md) — {counts[area]} questions")
idx += ["", "---", "", "<small>Related: [Revision Hub](../revision/index.md) · "
        "[Mock Exams](../revision/mock-exam.md)</small>"]
out = os.path.join(OUT, "index.md")
text = carry_over(out, "\n".join(idx)+"\n")
open(out, "w", encoding="utf-8").write(text)
print("chapter exams:", sum(counts.values()), "questions across", len(AREAS), "areas")

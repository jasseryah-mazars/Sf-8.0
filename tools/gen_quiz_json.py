#!/usr/bin/env python3
"""Generate the interactive quiz dataset consumed by the on-site exam player.

Reads every quiz/*.yml file and emits docs/assets/quiz-data.json — a compact,
self-contained dataset the client-side player (docs/assets/quiz.js) loads to run
Practice and Exam sessions that mirror the real Symfony certification format:
only three answer interactions, all select-only (no free text / code writing):

  * True / False      — the `true-false` questions.
  * Single answer     — exactly one correct option (radio).
  * Multiple choice    — two or more correct options (checkbox).

The player derives the interaction purely from how many options are `correct`,
so the pedagogical `type` labels (trap/internals/scenario/…) stay informational.
"""
from __future__ import annotations

import glob
import json
import os
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required: pip install pyyaml\n")
    raise

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUIZ_DIR = os.path.join(ROOT, "quiz")
OUT = os.path.join(ROOT, "docs", "assets", "quiz-data.json")

# quiz filename stem -> human area label (kept in sync with the site nav).
AREA_LABELS = {
    "architecture": "Symfony Architecture",
    "console": "Console",
    "controllers": "Controllers",
    "dependency-injection": "Dependency Injection",
    "forms": "Forms",
    "http": "HTTP",
    "http-caching": "HTTP Caching",
    "miscellaneous": "Miscellaneous",
    "php-web-security": "PHP & Web Security",
    "routing": "Routing",
    "security": "Security",
    "testing": "Automated Tests",
    "twig": "Templating (Twig)",
    "validation": "Data Validation",
}

# Official exam shape: 75 questions, 90 minutes, ~65% pass mark.
EXAM_CONFIG = {"questions": 75, "minutes": 90, "passPercent": 65}


def exam_type(qtype: str, n_correct: int) -> str:
    if qtype == "true-false":
        return "True / False"
    return "Multiple choice" if n_correct > 1 else "Single answer"


def build() -> dict:
    questions: list[dict] = []
    seen_ids: set[str] = set()
    for path in sorted(glob.glob(os.path.join(QUIZ_DIR, "*.yml"))):
        stem = os.path.splitext(os.path.basename(path))[0]
        area = AREA_LABELS.get(stem, stem)
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        for cat in data.get("categories", []):
            cat_name = cat.get("name", "")
            for q in cat.get("questions", []):
                answers = q.get("answers", [])
                if not answers:
                    continue
                qid = q.get("id", "")
                if qid in seen_ids:
                    raise SystemExit(f"duplicate question id: {qid}")
                seen_ids.add(qid)
                opts = [{"t": str(a.get("value", "")), "c": bool(a.get("correct"))}
                        for a in answers]
                n_correct = sum(1 for o in opts if o["c"])
                if n_correct == 0:
                    raise SystemExit(f"question {qid} has no correct answer")
                qtype = q.get("type", "single")
                questions.append({
                    "id": qid,
                    "area": area,
                    "cat": cat_name,
                    "type": qtype,
                    "diff": q.get("difficulty", "medium"),
                    "sub": q.get("subchapter", ""),
                    "syl": q.get("syllabus", ""),
                    "q": str(q.get("question", "")),
                    "a": opts,
                    "input": "checkbox" if n_correct > 1 else "radio",
                    "examType": exam_type(qtype, n_correct),
                    "exp": str(q.get("explanation", "")).strip(),
                    "doc": q.get("documentation", ""),
                })
    areas = sorted({q["area"] for q in questions})
    return {
        "generated_by": "tools/gen_quiz_json.py",
        "exam": EXAM_CONFIG,
        "areas": areas,
        "difficulties": ["easy", "medium", "hard"],
        "count": len(questions),
        "questions": questions,
    }


def main() -> int:
    payload = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    by_exam: dict[str, int] = {}
    for q in payload["questions"]:
        by_exam[q["examType"]] = by_exam.get(q["examType"], 0) + 1
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {payload['count']} questions "
          f"across {len(payload['areas'])} areas")
    print(f"  by exam interaction: {by_exam}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

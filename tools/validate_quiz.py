#!/usr/bin/env python3
"""Validate every quiz/*.yml against the certificationy-compatible schema.

Rules: parseable YAML; each question has >=2 answers, >=1 correct, a non-empty
`explanation`, and a `documentation` URL. Exit non-zero on any violation.
Run: python tools/validate_quiz.py
"""
from __future__ import annotations
import glob, os, sys, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main() -> int:
    files = 0; total = 0; issues = []
    for f in sorted(glob.glob(os.path.join(ROOT, "quiz", "*.yml"))):
        files += 1
        rel = os.path.relpath(f, ROOT)
        try:
            data = yaml.safe_load(open(f, encoding="utf-8")) or {}
        except Exception as e:
            issues.append(f"{rel}: YAML parse error: {e}"); continue
        for c in data.get("categories", []):
            for q in c.get("questions", []):
                total += 1
                stem = (q.get("question", "?") or "?")[:50]
                ans = q.get("answers", [])
                if len(ans) < 2: issues.append(f"{rel}: <2 answers -> {stem}")
                if not [a for a in ans if a.get("correct")]: issues.append(f"{rel}: no correct answer -> {stem}")
                if not (q.get("explanation") or "").strip(): issues.append(f"{rel}: missing explanation -> {stem}")
                doc = q.get("documentation") or ""
                if not doc.startswith("http"): issues.append(f"{rel}: missing/invalid documentation -> {stem}")
    print(f"validated {files} quiz files, {total} questions; {len(issues)} issue(s)")
    for i in issues[:50]: print("  ", i)
    return 1 if issues else 0

if __name__ == "__main__":
    sys.exit(main())

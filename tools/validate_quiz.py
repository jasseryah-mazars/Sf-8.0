#!/usr/bin/env python3
"""Validate the Global Question Bank (quiz/*.yml).

Base schema (required): every question has >=2 answers, >=1 correct, a non-empty
`explanation`, and a `documentation` URL.

v2 metadata (optional but validated when present): `id` (unique across the bank),
`type` (enum), `difficulty` (enum), `subchapter`, `concepts` (list), `syllabus`.

Also reports type/difficulty distribution and **subchapter coverage** against the
Traceability Matrix (warning, not failure, so it never blocks CI mid-expansion).

Exit non-zero only on hard errors (base-schema violations, bad enum, duplicate id).
Run: python tools/validate_quiz.py
"""
from __future__ import annotations
import glob, os, re, sys, collections, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIX = os.path.join(ROOT, "specs", "TraceabilityMatrix.md")
TYPES = {"single", "multiple", "true-false", "code", "config", "debug",
         "internals", "scenario", "trap"}
DIFF = {"easy", "medium", "hard"}


def expected_subchapters() -> set[str]:
    subs = set()
    for line in open(MATRIX, encoding="utf-8"):
        m = re.search(r"`([a-z0-9-]+/[a-z0-9-]+)\.md`", line)
        if m:
            subs.add(m.group(1))
    return subs


def main() -> int:
    files = total = out_of_scope = 0
    errors: list[str] = []
    ids: dict[str, str] = {}
    by_type = collections.Counter()
    by_diff = collections.Counter()
    covered = set()
    meta_count = 0

    for f in sorted(glob.glob(os.path.join(ROOT, "quiz", "*.yml"))):
        files += 1
        rel = os.path.relpath(f, ROOT)
        try:
            data = yaml.safe_load(open(f, encoding="utf-8")) or {}
        except Exception as e:
            errors.append(f"{rel}: YAML parse error: {e}")
            continue
        for c in data.get("categories", []):
            for q in c.get("questions", []):
                total += 1
                stem = (q.get("question", "?") or "?")[:50]
                ans = q.get("answers", [])
                if len(ans) < 2:
                    errors.append(f"{rel}: <2 answers -> {stem}")
                if not [a for a in ans if a.get("correct")]:
                    errors.append(f"{rel}: no correct answer -> {stem}")
                if not (q.get("explanation") or "").strip():
                    errors.append(f"{rel}: missing explanation -> {stem}")
                if not (q.get("documentation") or "").startswith("http"):
                    errors.append(f"{rel}: missing/invalid documentation -> {stem}")
                # v2 metadata
                qid = q.get("id")
                if qid is not None:
                    if qid in ids:
                        errors.append(f"{rel}: duplicate id '{qid}' (also {ids[qid]})")
                    ids[qid] = rel
                t = q.get("type")
                if t is not None and t not in TYPES:
                    errors.append(f"{rel}: bad type '{t}' -> {stem}")
                n_correct = sum(1 for a in ans if a.get("correct"))
                if t in ("single", "true-false") and n_correct != 1:
                    errors.append(
                        f"{rel}: type '{t}' must have exactly 1 correct answer, "
                        f"found {n_correct} -> {stem}"
                    )
                elif t == "multiple" and n_correct < 2:
                    errors.append(
                        f"{rel}: type 'multiple' must have >=2 correct answers, "
                        f"found {n_correct} -> {stem}"
                    )
                d = q.get("difficulty")
                if d is not None and d not in DIFF:
                    errors.append(f"{rel}: bad difficulty '{d}' -> {stem}")
                if any(k in q for k in ("id", "type", "difficulty", "subchapter")):
                    meta_count += 1
                if t:
                    by_type[t] += 1
                if d:
                    by_diff[d] += 1
                if q.get("out_of_scope"):
                    out_of_scope += 1
                    continue  # excluded from official syllabus coverage stats
                sc = q.get("subchapter")
                if sc:
                    covered.add(sc.removesuffix(".md"))

    print(f"validated {files} quiz files, {total} questions; {len(errors)} error(s)")
    print(f"  official (in-scope): {total - out_of_scope} · "
          f"out-of-scope/additional (excluded from certification): {out_of_scope}")
    print(f"  with v2 metadata: {meta_count}/{total}")
    if by_type:
        print("  by type:", dict(by_type))
    if by_diff:
        print("  by difficulty:", dict(by_diff))
    exp = expected_subchapters()
    if exp:
        missing = sorted(exp - covered)
        print(f"  subchapter coverage: {len(exp) - len(missing)}/{len(exp)} "
              f"({100*(len(exp)-len(missing))//max(len(exp),1)}%)")
        if missing:
            print(f"  [warn] {len(missing)} subchapters with no tagged question "
                  f"(first 10): {missing[:10]}")
    for e in errors[:60]:
        print("  ERROR:", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

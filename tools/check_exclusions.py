#!/usr/bin/env python3
"""Exclusions consistency check (P1-05).

Verifies the three chapters the mission brief excludes from the official
Symfony 8 certification syllabus (ESI, PHPUnit Bridge, Lock component) are
*consistently* marked excluded everywhere that matters, so "moved instead
of deleted, clearly marked" doesn't silently drift out of sync over time:

1. Each excluded chapter's .md and .fr.md files live under
   docs/appendices/out-of-syllabus/ (not in the main syllabus tree).
2. Each carries the explicit exclusion admonition
   ('Hors syllabus officiel Symfony 8.0') in both languages.
3. mkdocs.yml's nav lists them only under the top-level entry whose label
   contains "Appendices" (the exact label has changed before — see the
   in-code comment where it's matched), not anywhere in the main
   syllabus-topic nav sections.
4. Every quiz question whose `subchapter` matches one of these three
   chapters is tagged `out_of_scope: true` (a question about an excluded
   chapter must not silently count toward official coverage stats).
5. specs/TraceabilityMatrix.md's own "Out-of-scope / Additional Learning"
   section still lists all three (keeps the human-readable matrix and the
   machine check from drifting apart).

This does not decide *which* chapters should be excluded (that's a mission
brief / human decision, recorded in specs/RemediationLog.md's P0-03 entry)
— it only checks the three that are already on record stay consistently
marked, everywhere, going forward.
"""
from __future__ import annotations
import glob, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
QUIZ = os.path.join(ROOT, "quiz")

# (chapter slug under appendices/out-of-syllabus/, expected quiz subchapter prefix(es))
EXCLUDED = [
    ("esi", ["http-caching/esi"]),
    ("phpunit-bridge", ["testing/phpunit-bridge"]),
    ("lock", ["miscellaneous/lock"]),
]

MARKER = "Hors syllabus officiel Symfony 8.0"


def fail(msgs: list[str], msg: str) -> None:
    msgs.append(msg)


def main() -> int:
    errors: list[str] = []

    # 1 & 2: files present under appendices/out-of-syllabus/, admonition present
    for slug, _ in EXCLUDED:
        for suffix in ("md", "fr.md"):
            path = os.path.join(DOCS, "appendices", "out-of-syllabus", f"{slug}.{suffix}")
            if not os.path.exists(path):
                fail(errors, f"missing expected excluded-chapter file: {os.path.relpath(path, ROOT)}")
                continue
            text = open(path, encoding="utf-8").read()
            if MARKER not in text:
                fail(errors, f"{os.path.relpath(path, ROOT)} is missing the "
                              f"'{MARKER}' exclusion admonition")

    # 3: mkdocs.yml nav — the slug must appear only inside the Appendices
    # block. The nav label itself has changed before (e.g. the learner-
    # navigation redesign renamed it to "Out-of-Syllabus Appendices") —
    # match on the stable "Appendices" substring in the top-level nav key
    # rather than the exact historical label, so a legitimate future rename
    # doesn't false-positive here again.
    nav_path = os.path.join(ROOT, "mkdocs.yml")
    nav_text = open(nav_path, encoding="utf-8").read()
    appendices_match = re.search(r"^\s*-\s*[^:\n]*Appendices[^:\n]*:\s*$", nav_text, re.MULTILINE)
    appendices_start = appendices_match.start() if appendices_match else -1
    if appendices_start == -1:
        fail(errors, "mkdocs.yml has no top-level nav entry with 'Appendices' in its label")
    else:
        before = nav_text[:appendices_start]
        for slug, _ in EXCLUDED:
            needle = f"appendices/out-of-syllabus/{slug}.md"
            if needle not in nav_text:
                fail(errors, f"mkdocs.yml nav does not reference {needle}")
            if needle in before:
                fail(errors, f"{needle} appears in mkdocs.yml nav BEFORE the "
                              f"Appendices section — may be listed in the main syllabus nav")

    # 4: quiz questions for these subchapters must be tagged out_of_scope: true
    for f in sorted(glob.glob(os.path.join(QUIZ, "*.yml"))):
        rel = os.path.relpath(f, ROOT)
        try:
            data = yaml.safe_load(open(f, encoding="utf-8")) or {}
        except Exception as e:
            # P3: name the offending file rather than a bare traceback.
            raise RuntimeError(f"check_exclusions: failed to parse {rel}: {e}") from e
        for cat in data.get("categories", []):
            for q in cat.get("questions", []):
                sub = (q.get("subchapter") or "")
                for slug, prefixes in EXCLUDED:
                    if any(sub.startswith(p) for p in prefixes):
                        if not q.get("out_of_scope"):
                            fail(errors, f"{rel}: question {q.get('id')} has "
                                          f"subchapter '{sub}' (excluded chapter "
                                          f"'{slug}') but is not tagged out_of_scope: true")

    # 5: TraceabilityMatrix.md still names all three in its exclusions section
    matrix_path = os.path.join(ROOT, "specs", "TraceabilityMatrix.md")
    if os.path.exists(matrix_path):
        matrix_text = open(matrix_path, encoding="utf-8").read()
        section_start = matrix_text.find("Out-of-scope / Additional Learning")
        section = matrix_text[section_start:] if section_start != -1 else ""
        if section_start == -1:
            fail(errors, "specs/TraceabilityMatrix.md has no 'Out-of-scope / "
                          "Additional Learning' section")
        else:
            for slug, _ in EXCLUDED:
                # cheap presence check: the chapter's doc path should be named
                needle = f"out-of-syllabus/{slug}.md"
                if needle not in section:
                    fail(errors, f"specs/TraceabilityMatrix.md's exclusions "
                                  f"section does not mention {needle}")
    else:
        fail(errors, "specs/TraceabilityMatrix.md not found — run "
                      "tools/gen_traceability_matrix.py first")

    if errors:
        print(f"check_exclusions: {len(errors)} inconsistency(ies) found:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"check_exclusions: {len(EXCLUDED)} excluded chapters consistently "
          f"marked (files, nav, quiz tagging, matrix section) — 0 inconsistencies")
    return 0


if __name__ == "__main__":
    sys.exit(main())

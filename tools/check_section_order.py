#!/usr/bin/env python3
"""
Section-order audit for Symfony 8 cert-prep chapters.

Empirically derived (see docstring below) canonical order of the recurring
sections used by every content chapter under ``docs/``. This tool is an AUDIT:
by default it always exits 0 and writes a Markdown report. Pass ``--strict`` to
exit 1 when any violation is found (for optional future CI gating).

How the canonical order was derived
------------------------------------
All 153 content chapters (every ``docs/**/*.md`` excluding index/hub/labs/
exam/glossary/resources/tags/_meta/revision files) were scanned for:
  * the three leading Material admonitions ``!!! tip "In a nutshell"``,
    ``!!! example "Real-world analogy"``, ``!!! abstract "Learning objectives"``
  * every level-2 heading (``## X``)
Headings were normalised to their family name (the part before an em/en dash),
their mean normalised position computed across all chapters, and sorted. The
result below is the modal template followed by essentially every chapter.

Stdlib only, Python 3.12.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Canonical order (family display name -> matching prefix)                     #
# --------------------------------------------------------------------------- #
# Order below is the empirically derived modal template. Each entry is a
# (family, prefix) pair; a raw heading belongs to a family when it starts with
# that family's prefix (case-sensitive). This absorbs per-chapter qualifiers
# such as "Deep Dive — how it works internally" or
# "When (not) to use a custom resolver / alternatives".
_SECTIONS: list[tuple[str, str]] = [
    ("In a nutshell",                 "In a nutshell"),
    ("Real-world analogy",            "Real-world analogy"),
    ("Learning objectives",           "Learning objectives"),
    ("Theory",                        "Theory"),
    ("Deep Dive",                     "Deep Dive"),
    ("Configuration & code",          "Configuration & code"),
    ("Best practices & anti-patterns","Best practices"),
    ("When (not) to use it / alternatives", "When (not) to use"),
    ("Exercises",                     "Exercises"),
    ("Certification questions",       "Certification questions"),
    ("Key takeaways",                 "Key takeaways"),
    ("Last-minute revision",          "Last-minute revision"),
    ("Connections",                   "Connections"),
    ("Official References",           "Official References"),
    ("Video references",              "Video references"),
    ("Confidence check",              "Confidence check"),
]

# The plain list of recurring section titles, in their correct order.
CANONICAL_ORDER: list[str] = [family for family, _ in _SECTIONS]

# Rank lookup for validation.
_RANK: dict[str, int] = {family: i for i, (family, _) in enumerate(_SECTIONS)}

# The three leading admonitions we track (title -> "In a nutshell" etc.).
_ADMONITIONS = {"In a nutshell", "Real-world analogy", "Learning objectives"}

_ADM_RE = re.compile(r'^!!!\s+\w+\s+"([^"]+)"')
_H2_RE = re.compile(r'^##\s+(.+?)\s*$')

# Directories / filenames that are NOT content chapters.
_EXCLUDE_DIRS = {"_meta", "labs", "revision", "exams", "exam-guide"}
_EXCLUDE_NAMES = {"index.md", "glossary.md", "resources.md", "tags.md", "roadmap.md"}


def classify(raw_title: str) -> str | None:
    """Return the canonical family for a raw heading/admonition title, else None."""
    raw = raw_title.strip()
    for family, prefix in _SECTIONS:
        if raw == prefix or raw.startswith(prefix):
            return family
    return None


def find_content_chapters(docs_dir: Path) -> list[Path]:
    files: list[Path] = []
    for root, dirs, fnames in os.walk(docs_dir):
        dirs[:] = [d for d in dirs if d not in _EXCLUDE_DIRS]
        top = Path(root).relative_to(docs_dir).parts
        if top and top[0] in _EXCLUDE_DIRS:
            continue
        for f in fnames:
            if not f.endswith(".md") or f.endswith(".fr.md"):
                continue
            if f in _EXCLUDE_NAMES or "hub" in f:
                continue
            files.append(Path(root) / f)
    files.sort()
    return files


def extract_sections(path: Path) -> list[str]:
    """Ordered list of canonical families present in the file (in file order)."""
    seq: list[str] = []
    in_code = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = _ADM_RE.match(line)
        if m:
            title = m.group(1).strip()
            if title in _ADMONITIONS:
                seq.append(title)
            continue
        m = _H2_RE.match(line)
        if m:
            fam = classify(m.group(1))
            if fam is not None:
                seq.append(fam)
    return seq


def check_order(seq: list[str]) -> list[str]:
    """Return human-readable violation messages for out-of-order sections."""
    violations: list[str] = []
    max_rank = -1
    max_name = None
    for name in seq:
        rank = _RANK[name]
        if rank < max_rank:
            # max_name is physically earlier in the file but canonically later.
            violations.append(f'"{max_name}" appears before "{name}"')
        else:
            max_rank = rank
            max_name = name
    return violations


def build_report(docs_dir: Path, chapters: list[Path]) -> tuple[str, int, int]:
    compliant = 0
    non_compliant = 0
    per_file: list[tuple[Path, list[str], list[str]]] = []

    for path in chapters:
        seq = extract_sections(path)
        violations = check_order(seq)
        if violations:
            non_compliant += 1
        else:
            compliant += 1
        per_file.append((path, seq, violations))

    lines: list[str] = []
    lines.append("# Section Order Report")
    lines.append("")
    lines.append("Audit of the relative order of recurring chapter sections against the")
    lines.append("empirically derived canonical template. Report-only; sections not in the")
    lines.append("canonical list are ignored, and missing sections are not flagged.")
    lines.append("")
    lines.append("## Canonical order")
    lines.append("")
    for i, name in enumerate(CANONICAL_ORDER, 1):
        lines.append(f"{i}. {name}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Content chapters scanned: **{len(chapters)}**")
    lines.append(f"- Compliant: **{compliant}**")
    lines.append(f"- Non-compliant: **{non_compliant}**")
    lines.append("")
    lines.append("## Violations")
    lines.append("")
    if non_compliant == 0:
        lines.append("None. All scanned chapters follow the canonical section order.")
    else:
        for path, _seq, violations in per_file:
            if not violations:
                continue
            rel = path.relative_to(docs_dir.parent)
            lines.append(f"### {rel}")
            lines.append("")
            for v in violations:
                lines.append(f"- {v}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n", compliant, non_compliant


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit chapter section ordering.")
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit 1 if any violations are found (default: always exit 0).",
    )
    parser.add_argument(
        "--docs", default=None,
        help="Path to docs/ directory (default: <repo>/docs).",
    )
    parser.add_argument(
        "--report", default=None,
        help="Report output path (default: <repo>/specs/SectionOrderReport.md).",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent.parent
    docs_dir = Path(args.docs).resolve() if args.docs else repo_root / "docs"
    report_path = (
        Path(args.report).resolve() if args.report
        else repo_root / "specs" / "SectionOrderReport.md"
    )

    if not docs_dir.is_dir():
        print(f"docs directory not found: {docs_dir}", file=sys.stderr)
        return 0 if not args.strict else 1

    chapters = find_content_chapters(docs_dir)
    report, compliant, non_compliant = build_report(docs_dir, chapters)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    print(f"Scanned {len(chapters)} content chapters.")
    print(f"Compliant: {compliant}  Non-compliant: {non_compliant}")
    print(f"Report written to {report_path}")

    if args.strict and non_compliant > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

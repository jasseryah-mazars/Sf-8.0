#!/usr/bin/env python3
"""Blocking check (P0-01): no unversioned or wrong-version Symfony doc links.

The certification requires verification against Symfony 8.0 exclusively, so
every `symfony.com/doc/...` reference in this repository must be pinned to
`/doc/8.0/` — never `/doc/current/` (which silently drifts to whatever Symfony
considers newest) and never another version (`/doc/7.x/`, `/doc/9.x/`, ...).
GitHub source links are checked separately: they must pin `blob/8.0` or
`tree/8.0` on `github.com/symfony/symfony`.

This script is the automated guard specs/RemediationLog.md's P0-01 entry
requires: it fails (non-zero exit) the moment a non-compliant reference is
reintroduced, in any tracked file. Run from the repo root:

    python tools/check_doc_version_refs.py

Wired into `tools/audit.py`'s call chain and into CI (see .github/workflows).
"""
from __future__ import annotations
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THIS_FILE = os.path.abspath(__file__)

# Directories that are never source-of-truth content: build output, VCS
# internals, dependency caches, and this run's own scratch reports.
EXCLUDE_DIRS = {".git", "site", "__pycache__", "reports", "node_modules", "vendor"}

# File types worth scanning for prose/config references.
INCLUDE_EXT = {".md", ".py", ".yml", ".yaml", ".json", ".html"}

# A version segment is "acceptable" when it is the pinned Symfony framework
# branch (8.0) *or* the pinned Twig docs branch (3.x — Twig's docs version by
# major.x, distinct from Symfony's own versioning; the project version-locks
# Twig to "up to 3.22", i.e. the 3.x line). Anything else — current, 7.0,
# 7.4, 9.0, latest, ... — is a violation. A terminator (path separator, quote,
# backtick, paren, bracket, whitespace, end-of-string, or trailing
# punctuation) must immediately follow so "8.0.1" or "3.x-dev" don't
# false-positive as clean.
_TERM = r'(?:/|$|["\'`\)\]\.,;\s])'
# Require a URL scheme immediately before the host, so a bare backtick-quoted
# mention like `symfony.com/doc/current` in prose *describing* the old
# convention (e.g. in a remediation log) doesn't false-positive — only an
# actual, followable link (which this project's own conventions always write
# as a full https:// URL) is a real reference to enforce.
BAD_DOC_RE = re.compile(rf"https?://symfony\.com/doc/(?!(?:8\.0|3\.x){_TERM})(\S+)")

# A github.com/symfony/symfony source link that is NOT pinned to 8.0.
BAD_SRC_RE = re.compile(
    rf"https?://github\.com/symfony/symfony/(blob|tree)/(?!8\.0{_TERM})(\S+)"
)

# Documented, justified exceptions: (relative path, substring that makes a
# line a false positive). Each entry needs a reason — see specs/RemediationLog.md
# P0-01 for the full justification. Keep this list short; prefer fixing the
# reference over adding an exception.
ALLOWED = [
    # Historical/descriptive: quotes the URL pattern used by the *ancestor*
    # community list this project was rewritten from (a Symfony 7 resource),
    # not a live reference of this project's own content.
    ("specs/GapAnalysis.md", "symfony.com/doc/7.0/"),
]


def iter_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if os.path.splitext(fn)[1] in INCLUDE_EXT:
                yield os.path.join(dirpath, fn)


def check() -> list[tuple[str, int, str]]:
    """Return a list of (relative_path, line_number, offending_text) violations."""
    violations: list[tuple[str, int, str]] = []
    for path in iter_files():
        if os.path.abspath(path) == THIS_FILE:
            continue  # this file's own docstring/regex source is not a reference
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path, encoding="utf-8") as fh:
                lines = fh.readlines()
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, start=1):
            if any(rel == allow_rel and substr in line for allow_rel, substr in ALLOWED):
                continue
            for m in BAD_DOC_RE.finditer(line):
                violations.append((rel, i, f"symfony.com/doc/{m.group(1)[:40]}"))
            for m in BAD_SRC_RE.finditer(line):
                violations.append((rel, i, f"github.com/symfony/symfony/{m.group(1)}/{m.group(2)[:40]}"))
    return violations


def main() -> int:
    violations = check()
    if not violations:
        print("check_doc_version_refs: OK — every symfony.com/doc and "
              "github.com/symfony/symfony reference is pinned to 8.0.")
        return 0
    print(f"check_doc_version_refs: FAIL — {len(violations)} non-8.0-pinned "
          "reference(s) found:")
    for rel, line_no, text in violations:
        print(f"  {rel}:{line_no}: {text}")
    print(
        "\nEvery Symfony doc/source reference must pin the 8.0 branch "
        "(symfony.com/doc/8.0/... or github.com/symfony/symfony/blob|tree/8.0/...). "
        "See specs/FutureMaintenance.md §2 (Versioning policy) for the rationale "
        "and the deliberate baseline-change process."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())

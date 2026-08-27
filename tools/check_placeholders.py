#!/usr/bin/env python3
"""Structured checks (P1-01) not covered by the existing audit tooling:

  1. Every chapter's "## Official References" section is non-empty (at
     least one Markdown link inside it) — final_audit.py only checks the
     heading exists, not that it has real content under it.
  2. No literal TODO/FIXME/XXX/TBD/[placeholder] marker anywhere under
     docs/, outside of fenced code blocks (a snippet demonstrating a real
     `// TODO` comment as teaching content — e.g. in a chapter about code
     style or deprecations — is not a repo placeholder and is allow-listed
     by excluding fenced-code-block content from the scan).
  3. Every internal Markdown link (no URL scheme) resolves to a file that
     actually exists relative to the linking file — a fast, standalone,
     Python-only pre-check of what `mkdocs build --strict` verifies at
     build time (kept separate so it can run without a full site build).

Exit non-zero if any real violation is found. Run: python tools/check_placeholders.py
"""
from __future__ import annotations
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|XXX|TBD)\b|\[placeholder\]", re.IGNORECASE)
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
OFFICIAL_REFS_RE = re.compile(r"(?m)^##\s+Official References\s*$")
MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")


def strip_code_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def md_files():
    for dirpath, dirnames, filenames in os.walk(DOCS):
        dirnames[:] = [d for d in dirnames if not d.startswith("_meta")]
        for fn in filenames:
            if fn.endswith(".md"):
                yield os.path.join(dirpath, fn)


def check_official_references(path: str, text: str) -> list[str]:
    m = OFFICIAL_REFS_RE.search(text)
    if not m:
        return []  # not every page is a full chapter (index/meta pages) — final_audit.py already tracks chapter coverage for this heading
    after = text[m.end():]
    # section ends at the next "## " heading or EOF
    next_h2 = re.search(r"(?m)^##\s+", after)
    section = after[: next_h2.start()] if next_h2 else after
    if not MD_LINK_RE.search(section):
        return [f"{os.path.relpath(path, ROOT)}: '## Official References' section has no Markdown link inside it"]
    return []


def check_placeholders(path: str, text: str) -> list[str]:
    clean = strip_code_fences(text)
    out = []
    for i, line in enumerate(clean.split("\n"), start=1):
        m = PLACEHOLDER_RE.search(line)
        if m:
            out.append(f"{os.path.relpath(path, ROOT)}:{i}: placeholder marker '{m.group(0)}' outside a code fence")
    return out


def check_internal_links(path: str, text: str) -> list[str]:
    out = []
    base_dir = os.path.dirname(path)
    clean = strip_code_fences(text)
    for m in MD_LINK_RE.finditer(clean):
        target = m.group(1).strip()
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target_path = target.split("#", 1)[0]
        if not target_path:
            continue
        resolved = os.path.normpath(os.path.join(base_dir, target_path))
        if not os.path.exists(resolved):
            out.append(f"{os.path.relpath(path, ROOT)}: broken internal link -> {target}")
    return out


def main() -> int:
    violations: list[str] = []
    files_scanned = 0
    for path in md_files():
        files_scanned += 1
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        violations += check_official_references(path, text)
        violations += check_placeholders(path, text)
        violations += check_internal_links(path, text)

    print(f"check_placeholders: scanned {files_scanned} files under docs/")
    if not violations:
        print("  OK — every 'Official References' section has a link, no TODO/placeholder "
              "markers outside code fences, no broken internal links.")
        return 0
    print(f"  FAIL — {len(violations)} violation(s):")
    for v in violations[:100]:
        print("   ", v)
    if len(violations) > 100:
        print(f"    ... and {len(violations) - 100} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())

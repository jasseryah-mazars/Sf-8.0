#!/usr/bin/env python3
"""Report code-block lines wider than MAX_WIDTH across docs/**/*.md.

Report-only (always exits 0 unless --strict): lists, per file, every fenced
code-block line longer than the limit so they can be reflowed to avoid
horizontal scrolling. Mermaid blocks are ignored (diagrams, not code).

Run: python tools/check_code_width.py [--max 80] [--strict] [--summary]
"""
from __future__ import annotations

import argparse
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = re.compile(r"^(\s*)```(\w*)")


def iter_long_lines(path: str, max_width: int):
    in_block = False
    lang = ""
    indent = 0
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        m = FENCE.match(line)
        if m:
            if not in_block:
                in_block, lang, indent = True, m.group(2), len(m.group(1))
            else:
                in_block = False
            continue
        if in_block and lang != "mermaid":
            # measure the code itself, not the admonition indentation
            if len(line) - indent > max_width:
                yield n, lang or "text", len(line) - indent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=80)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--summary", action="store_true")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(ROOT, "docs", "**", "*.md"),
                             recursive=True))
    total = 0
    offenders: dict[str, int] = {}
    for f in files:
        rel = os.path.relpath(f, ROOT)
        hits = list(iter_long_lines(f, args.max))
        if hits:
            offenders[rel] = len(hits)
            total += len(hits)
            if not args.summary:
                for n, lang, width in hits:
                    print(f"{rel}:{n}: {width} chars ({lang})")
    print(f"\n{total} line(s) over {args.max} chars "
          f"in {len(offenders)} file(s) / {len(files)} scanned")
    if args.summary:
        for rel, n in sorted(offenders.items(), key=lambda kv: -kv[1])[:40]:
            print(f"  {n:4d}  {rel}")
    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    raise SystemExit(main())

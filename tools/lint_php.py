#!/usr/bin/env python3
"""Lint every complete PHP snippet in docs/ with `php -l`.

Enforces the "every snippet must compile" rule. Handles Material content-tab
indentation (dedents each block). Skips, on purpose:
  - method/property excerpts (a top-level `public|protected|private function|...`
    is a documentation fragment, not a file);
  - any block containing a `// lint-skip` marker (intentional error demos).
Exit non-zero on any real parse/compile failure. Run: python tools/lint_php.py
"""
from __future__ import annotations
import glob, re, subprocess, tempfile, os, sys, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r"```php\n(.*?)```", re.DOTALL)
EXCERPT = re.compile(r"(?m)^\s*(public|protected|private)\s+(static\s+)?(function|readonly|int|string|bool|float|array|\?)")

def is_file_snippet(code: str) -> bool:
    s = code.lstrip()
    if not s.startswith("<?php"):
        return False            # inline fragment, not a file
    if "// lint-skip" in code:
        return False            # intentional (e.g. demonstrates an error)
    # strip <?php, declare, use, comments/blank; first real line
    body = re.sub(r"(?m)^\s*(<\?php|declare\(.*?\);|use\s+[^;]+;|//.*|#.*|/\*.*?\*/)\s*$", "", s)
    body = "\n".join(l for l in body.splitlines() if l.strip())
    return not EXCERPT.match(body)   # skip bare method/property excerpts

def main() -> int:
    linted = 0
    fails = []
    for f in glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True):
        if "/_meta/" in f:
            continue
        for m in BLOCK.finditer(open(f, encoding="utf-8").read()):
            code = textwrap.dedent(m.group(1))
            if not is_file_snippet(code):
                continue
            linted += 1
            with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False) as tf:
                tf.write(code); path = tf.name
            r = subprocess.run(["php", "-l", path], capture_output=True, text=True)
            os.unlink(path)
            if r.returncode != 0:
                msg = (r.stderr.strip().splitlines() or ["error"])[0]
                fails.append((os.path.relpath(f, ROOT), msg))
    print(f"linted {linted} complete PHP snippets; {len(fails)} failure(s)")
    for f, msg in fails:
        print(f"  FAIL {f}: {msg}")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())

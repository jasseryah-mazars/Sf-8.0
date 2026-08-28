#!/usr/bin/env python3
"""Blocking Mermaid validator — compiles every ```mermaid block with the real engine.

Why this exists
---------------
`mkdocs build --strict` cannot catch a broken diagram: MkDocs only copies the
fenced text into the page, and Mermaid renders it **in the visitor's browser**.
A diagram with a syntax error therefore builds green and then shows
"Syntax error in text" to the reader. This script closes that gap by parsing and
rendering every block with the exact Mermaid build the site ships
(`tools/node_modules/mermaid`, pinned in `tools/package.json`), inside real
Chromium — never by regex.

Usage
-----
    python3 tools/validate_mermaid.py                     # whole docs/ tree
    python3 tools/validate_mermaid.py docs/php-web-security
    python3 tools/validate_mermaid.py --json report.json

Exit status: 0 when every diagram parses and renders, 1 otherwise (and on any
setup failure — a validator that cannot run must not report success).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVER = os.path.join(ROOT, "tools", "_mermaid_validate.js")
MERMAID_DIST = os.path.join(
    ROOT, "tools", "node_modules", "mermaid", "dist", "mermaid.min.js"
)
PKG_JSON = os.path.join(ROOT, "tools", "package.json")

FENCE_OPEN = "```mermaid"


def pinned_version() -> str | None:
    """The mermaid version this repo pins, read from tools/package.json."""
    try:
        with open(PKG_JSON, encoding="utf-8") as fh:
            pkg = json.load(fh)
    except (OSError, ValueError):
        return None
    for field in ("devDependencies", "dependencies"):
        v = (pkg.get(field) or {}).get("mermaid")
        if v:
            return v.lstrip("^~")
    return None


def installed_version() -> str | None:
    p = os.path.join(ROOT, "tools", "node_modules", "mermaid", "package.json")
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh).get("version")
    except (OSError, ValueError):
        return None


def iter_markdown(target: str):
    if os.path.isfile(target):
        yield target
        return
    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".git", "site"}]
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                yield os.path.join(dirpath, fn)


def extract_blocks(path: str):
    """Yield (line_number_of_fence, diagram_text) for each ```mermaid block.

    Line numbers are 1-based and point at the opening fence, so a failure can be
    opened directly at file:line.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == FENCE_OPEN:
            start = i + 1  # 1-based line of the fence
            body: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                body.append(lines[i])
                i += 1
            yield start, "\n".join(body)
        i += 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", default=None,
                    help="files or directories to scan (default: docs/)")
    ap.add_argument("--json", dest="json_out", default=None,
                    help="also write a machine-readable report here")
    args = ap.parse_args()

    targets = args.paths or [os.path.join(ROOT, "docs")]

    pinned, got = pinned_version(), installed_version()
    if got is None:
        print("validate_mermaid: FAIL — mermaid is not installed under tools/.", file=sys.stderr)
        print("  fix: (cd tools && npm install)", file=sys.stderr)
        return 1
    if pinned and got != pinned:
        print(f"validate_mermaid: FAIL — pinned mermaid {pinned} but {got} is installed.",
              file=sys.stderr)
        print("  fix: (cd tools && npm install)", file=sys.stderr)
        return 1

    blocks, empties = [], []
    for target in targets:
        target = target if os.path.isabs(target) else os.path.join(ROOT, target)
        for path in iter_markdown(target):
            rel = os.path.relpath(path, ROOT)
            for line, text in extract_blocks(path):
                if not text.strip():
                    empties.append((rel, line))
                    continue
                blocks.append({
                    "id": f"{len(blocks)}",
                    "file": rel,
                    "line": line,
                    "text": text,
                })

    if not blocks and not empties:
        print("validate_mermaid: no mermaid blocks found in " + ", ".join(targets))
        return 0

    payload = json.dumps({"mermaidPath": MERMAID_DIST, "blocks": blocks})

    # Resolve `playwright` from the global install, matching the browsers already
    # provisioned in this image. Installing it locally pulls a newer release that
    # expects a Chromium build the image does not ship. Same approach as
    # tools/check_site_quality.py.
    env = os.environ.copy()
    local_modules = os.path.join(ROOT, "tools", "node_modules")
    global_modules = subprocess.run(
        ["npm", "root", "-g"], capture_output=True, text=True
    ).stdout.strip() or "/usr/lib/node_modules"
    env["NODE_PATH"] = f"{local_modules}:{global_modules}"

    try:
        proc = subprocess.run(
            ["node", DRIVER], input=payload, capture_output=True, text=True,
            cwd=os.path.join(ROOT, "tools"), timeout=900, env=env,
        )
    except FileNotFoundError:
        print("validate_mermaid: FAIL — node not found on PATH.", file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired:
        print("validate_mermaid: FAIL — driver timed out.", file=sys.stderr)
        return 1

    if proc.returncode != 0 or not proc.stdout.strip():
        print("validate_mermaid: FAIL — driver did not return a result.", file=sys.stderr)
        print((proc.stderr or "").strip()[:2000], file=sys.stderr)
        return 1

    try:
        out = json.loads(proc.stdout)
    except ValueError:
        print("validate_mermaid: FAIL — driver output was not JSON.", file=sys.stderr)
        print(proc.stdout[:2000], file=sys.stderr)
        return 1

    if out.get("fatal"):
        print(f"validate_mermaid: FAIL — {out['fatal']}", file=sys.stderr)
        return 1

    by_id = {b["id"]: b for b in blocks}
    failures = []
    for r in out.get("results", []):
        if not r.get("ok"):
            b = by_id[r["id"]]
            failures.append((b["file"], b["line"], r.get("stage"), r.get("error") or ""))

    engine = out.get("version", "unknown")
    total = len(blocks)

    for rel, line in empties:
        failures.append((rel, line, "extract", "empty mermaid block"))

    if failures:
        print(f"validate_mermaid: FAIL — {len(failures)} of {total + len(empties)} "
              f"diagram(s) rejected by mermaid {got} (engine reported {engine})\n",
              file=sys.stderr)
        for rel, line, stage, err in sorted(failures):
            first = err.strip().splitlines()[0] if err.strip() else "(no message)"
            print(f"  {rel}:{line}  [{stage}] {first}", file=sys.stderr)
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8") as fh:
                json.dump({"engine": engine, "pinned": got, "total": total,
                           "failures": failures}, fh, indent=2)
        return 1

    print(f"validate_mermaid: OK — {total} diagram(s) parsed and rendered "
          f"with mermaid {got} (engine reported {engine}); 0 error(s).")
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump({"engine": engine, "pinned": got, "total": total, "failures": []},
                      fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())

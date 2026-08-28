#!/usr/bin/env python3
"""Vendor the pinned Mermaid build into docs/assets/, and keep it honest.

Why this exists
---------------
mkdocs-material hardcodes a lazy CDN fetch for diagrams:

    typeof mermaid == "undefined" ? load("https://unpkg.com/mermaid@11/...") : ...

Two problems with that. It is an **unpinned major range**, so the version a reader
renders with drifts underneath us and can stop matching the version
`tools/validate_mermaid.py` validated against. And it is a single point of failure:
one CDN outage or a corporate proxy and every diagram on the site disappears —
`specs/SiteQualityReport.md` already flagged this, and `unpkg.com` is in fact
blocked from this environment.

Because Material only fetches when `mermaid` is undefined, loading our own copy
first wins: it never reaches the CDN.

This script copies the exact build from `tools/node_modules/mermaid`, refusing to
run if that version differs from the pin in `tools/package.json`. That single
assertion is what makes "the site and the validator use the same engine" a
guarantee instead of a hope.

Usage:
    python3 tools/vendor_mermaid.py          # copy if needed
    python3 tools/vendor_mermaid.py --check  # verify only, exit 1 on drift
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG_JSON = os.path.join(ROOT, "tools", "package.json")
SRC = os.path.join(ROOT, "tools", "node_modules", "mermaid", "dist", "mermaid.min.js")
SRC_PKG = os.path.join(ROOT, "tools", "node_modules", "mermaid", "package.json")
DEST = os.path.join(ROOT, "docs", "assets", "mermaid.min.js")
STAMP = os.path.join(ROOT, "docs", "assets", "mermaid.version.json")


def pinned() -> str | None:
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


def installed() -> str | None:
    try:
        with open(SRC_PKG, encoding="utf-8") as fh:
            return json.load(fh).get("version")
    except (OSError, ValueError):
        return None


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="verify the vendored copy matches the pin; do not write")
    args = ap.parse_args()

    want, got = pinned(), installed()
    if want is None:
        print("vendor_mermaid: FAIL — no mermaid pin in tools/package.json", file=sys.stderr)
        return 1
    if got is None:
        print("vendor_mermaid: FAIL — mermaid not installed. Run: (cd tools && npm install)",
              file=sys.stderr)
        return 1
    if got != want:
        print(f"vendor_mermaid: FAIL — pinned {want}, installed {got}. "
              f"Run: (cd tools && npm install)", file=sys.stderr)
        return 1

    if args.check:
        if not os.path.exists(DEST):
            print(f"vendor_mermaid: FAIL — {os.path.relpath(DEST, ROOT)} is missing. "
                  f"Run: python3 tools/vendor_mermaid.py", file=sys.stderr)
            return 1
        if sha256(DEST) != sha256(SRC):
            print(f"vendor_mermaid: FAIL — vendored copy differs from mermaid {want}. "
                  f"Run: python3 tools/vendor_mermaid.py", file=sys.stderr)
            return 1
        print(f"vendor_mermaid: OK — docs/assets/mermaid.min.js matches pinned mermaid {want}.")
        return 0

    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    shutil.copyfile(SRC, DEST)
    with open(STAMP, "w", encoding="utf-8") as fh:
        json.dump({
            "version": want,
            "sha256": sha256(DEST),
            "source": "tools/node_modules/mermaid/dist/mermaid.min.js",
            "why": ("Vendored so the site renders with the same engine "
                    "tools/validate_mermaid.py validates against, and so diagrams do "
                    "not depend on an unpinned CDN range."),
        }, fh, indent=2)
        fh.write("\n")
    size = os.path.getsize(DEST)
    print(f"vendor_mermaid: wrote docs/assets/mermaid.min.js "
          f"(mermaid {want}, {size / 1024 / 1024:.1f} MiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

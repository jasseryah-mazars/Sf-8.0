#!/usr/bin/env python3
"""Lint every complete XML document in docs/ (P1-02) with Python's built-in
xml.dom.minidom parser (well-formedness only, no DTD/XSD schema validation
— no network access to fetch a schema in this environment).

Mirrors tools/lint_php.py's "complete file vs excerpt" distinction: a block
starting with `<?xml` is a full document and must be well-formed; a bare
multi-root fragment (e.g. showing two sibling config sections without their
enclosing root, as documentation shorthand) is not a real XML document and
is skipped rather than false-flagged.

Exit non-zero on any real well-formedness failure. Run: python tools/lint_xml.py
"""
from __future__ import annotations
import glob, re, os, sys, textwrap
import xml.dom.minidom
import xml.parsers.expat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r"```xml\n(.*?)```", re.DOTALL)


def main() -> int:
    linted = 0
    skipped = 0
    fails = []
    for f in glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True):
        if "/_meta/" in f:
            continue
        text = open(f, encoding="utf-8").read()
        for m in BLOCK.finditer(text):
            code = textwrap.dedent(m.group(1))  # Material tabbed content indents fences
            if not code.strip():
                continue
            if not code.lstrip().startswith("<?xml"):
                skipped += 1  # fragment, not a full document — see docstring
                continue
            linted += 1
            try:
                xml.dom.minidom.parseString(code)
            except xml.parsers.expat.ExpatError as e:
                fails.append((os.path.relpath(f, ROOT), str(e)))
    print(f"linted {linted} complete XML documents, skipped {skipped} fragments "
          f"(no single root — documentation shorthand, not a real XML file); "
          f"{len(fails)} failure(s)")
    for rel, msg in fails:
        print(f"  FAIL {rel}: {msg}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Editorial-structure normalization checks (P2-01).

Three checks not already covered by tools/check_placeholders.py (Official
References links, TODO markers, internal link resolution) or
tools/check_section_order.py (relative order of recurring sections):

1. **Nav <-> docs consistency.** Every `docs/**/*.md` file should be
   reachable from `mkdocs.yml`'s `nav:` tree (an unreferenced page is
   effectively invisible — no menu path to it, only a bare URL), and every
   nav entry should point at a file that actually exists on disk. i18n
   sidecar files (`*.fr.md`) are handled by the `mkdocs-static-i18n` plugin
   automatically and are correctly never listed in `nav:` directly, so
   they're excluded from the orphan check.
2. **Balanced code fences.** Every ` ``` ` opener in a file must have a
   matching closer — this is a structural Markdown check across every code
   block (any language, not just PHP/YAML/Twig/XML, which the language-
   specific linters already validate more deeply). An unbalanced fence
   breaks rendering for everything after it in the page.
3. **No heading with literally empty body.** A `##`/`###`/`####` heading
   immediately followed by another heading (or end of file) with nothing
   but blank lines in between is very likely a leftover stub, not
   intentional content.

Each check is independent and reports every violation found (not just the
first), so a single run surfaces the full list to fix.

Run: python tools/check_editorial_structure.py
"""
from __future__ import annotations
import glob, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
MKDOCS_YML = os.path.join(ROOT, "mkdocs.yml")

HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^```")


def load_nav_paths() -> set[str]:
    """Every .md path referenced anywhere in mkdocs.yml's nav tree,
    normalized relative to docs/. YAML with mkdocs-material's custom tags
    (!ENV etc.) isn't used in this repo's nav, but scan the raw text
    instead of parsing YAML, to sidestep the same custom-tag risk
    lint_yaml.py had to solve for in DI config snippets."""
    text = open(MKDOCS_YML, encoding="utf-8").read()
    # crude but effective: nav entries are ": path/to/file.md" or a bare
    # "- path/to/file.md" list item; both end in .md at end of line/value.
    paths = set(re.findall(r"[:\-]\s*([\w/\-]+\.md)\s*$", text, re.MULTILINE))
    return paths


def find_all_docs() -> list[str]:
    out = []
    for root, dirs, files in os.walk(DOCS):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if f.endswith(".md") and not f.endswith(".fr.md"):
                rel = os.path.relpath(os.path.join(root, f), DOCS)
                out.append(rel.replace(os.sep, "/"))
    return out


def load_exclude_docs_prefixes() -> list[str]:
    """Directories/patterns mkdocs.yml's own `exclude_docs:` removes from the
    build entirely (e.g. `_meta/` — internal authoring docs, never
    published) — files under these are correctly absent from nav, not
    orphans."""
    text = open(MKDOCS_YML, encoding="utf-8").read()
    m = re.search(r"(?m)^exclude_docs:\s*\|\s*\n((?:^\s+\S.*\n?)+)", text)
    if not m:
        return []
    return [line.strip() for line in m.group(1).splitlines() if line.strip()]


def check_nav_consistency() -> list[str]:
    errors = []
    nav_paths = load_nav_paths()
    disk_paths = set(find_all_docs())
    excluded_prefixes = load_exclude_docs_prefixes()
    disk_paths = {p for p in disk_paths
                  if not any(p.startswith(pfx) for pfx in excluded_prefixes)}

    # Dead nav entries: referenced but missing on disk.
    for p in sorted(nav_paths):
        if p not in disk_paths:
            errors.append(f"mkdocs.yml nav references '{p}' which does not exist under docs/")

    # Orphan pages: excluded categories are legitimately not nav-listed
    # (generated per-chapter exam/flashcard/revision pages that are only
    # reached via their own index hub, not individually in the main nav —
    # verified by spot-checking exams/index.md and revision/index.md link
    # to every sibling file in their own directory, not via mkdocs nav).
    _generated_dirs = {"exams", "revision"}
    for p in sorted(disk_paths):
        top = p.split("/")[0]
        if top in _generated_dirs:
            continue
        if p not in nav_paths:
            errors.append(f"docs/{p} exists but is not referenced anywhere in mkdocs.yml nav (orphan page)")
    return errors


def check_code_fences() -> list[str]:
    errors = []
    for path in find_all_docs():
        full = os.path.join(DOCS, path)
        lines = open(full, encoding="utf-8").read().splitlines()
        count = sum(1 for l in lines if FENCE_RE.match(l))
        if count % 2 != 0:
            errors.append(f"docs/{path}: odd number of ``` fence markers ({count}) — an unclosed code block")
    return errors


def check_empty_sections() -> list[str]:
    """A heading is empty only if there is no content at all before the next
    heading at the SAME OR SHALLOWER level — a '## Deep Dive' immediately
    followed by '### The wrapping model' and its content is not empty, that
    subsection IS its content. Only a heading whose entire subtree (up to
    the next sibling-or-higher heading) is blank is flagged."""
    errors = []
    for path in find_all_docs():
        full = os.path.join(DOCS, path)
        lines = open(full, encoding="utf-8").read().splitlines()
        for i, line in enumerate(lines):
            m = HEADING_RE.match(line)
            if not m:
                continue
            level = len(m.group(1))
            title = m.group(2)
            body = []
            for nxt in lines[i + 1:]:
                nm = HEADING_RE.match(nxt)
                if nm and len(nm.group(1)) <= level:
                    break
                if nxt.strip():
                    body.append(nxt)
            if not body:
                errors.append(f"docs/{path}: heading '{title}' (line {i + 1}) has no content in its subtree before the next same-or-shallower heading/EOF")
    return errors


def main() -> int:
    all_errors: list[str] = []

    nav_errors = check_nav_consistency()
    fence_errors = check_code_fences()
    empty_errors = check_empty_sections()

    for label, errs in [("nav<->docs consistency", nav_errors),
                         ("code-fence balance", fence_errors),
                         ("empty sections", empty_errors)]:
        print(f"{label}: {len(errs)} violation(s)")
        for e in errs:
            print(f"  - {e}")
        all_errors += errs

    if all_errors:
        print(f"\ncheck_editorial_structure: {len(all_errors)} total violation(s)")
        return 1
    print("\ncheck_editorial_structure: OK — nav/docs consistent, all code "
          "fences balanced, no empty-body headings found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

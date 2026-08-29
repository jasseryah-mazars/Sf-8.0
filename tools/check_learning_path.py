#!/usr/bin/env python3
"""Hold every copy of the reading order to one source: specs/learning_path.yml.

The pedagogical order was written down in five independent places — the nav in
`mkdocs.yml`, each domain index's `## Micro-chapters` list, the
"Continue to the next topic" link ending every `-flashcards.md`, `roadmap.md`, and
the French navigation. Nothing compared them, so they could disagree silently, and
the reader would meet a chapter before the one it depends on.

This check makes `specs/learning_path.yml` the only place the order is edited.
Anything that repeats it must agree, or the build fails naming the divergence.

What is verified:

  nav          every topic appears in mkdocs.yml, under its own domain, in order;
               nothing in the nav is missing from the path.
  index        each `<domain>/index.md` lists its topics in the same order.
  next topic   each `-flashcards.md` ends by pointing at the topic that actually
               follows — including across a domain boundary, where it points at the
               next domain's index.
  prereqs      no topic is ordered before something it `requires`.

Usage:
    python3 tools/check_learning_path.py
    python3 tools/check_learning_path.py --domain php-web-security

Exit status: 0 when every consumer agrees with the path, 1 otherwise.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
PATH_FILE = os.path.join(ROOT, "specs", "learning_path.yml")
MKDOCS = os.path.join(ROOT, "mkdocs.yml")


def load_path() -> list[dict]:
    with open(PATH_FILE, encoding="utf-8") as fh:
        return yaml.safe_load(fh)["domains"]


def nav_order() -> dict[str, list[str]]:
    """Topic slugs per domain directory, in the order mkdocs.yml lists them."""
    text = open(MKDOCS, encoding="utf-8").read()
    try:
        start = text.index("\n  - Certification Domains")
    except ValueError:
        return {}
    rest = text[start + 1:]
    end = re.search(r"(?m)^  - (?!Certification Domains)\S", rest)
    block = rest[: end.start()] if end else rest

    order: dict[str, list[str]] = {}
    current: str | None = None
    for line in block.split("\n"):
        m = re.match(r"^          - (?:.*?: )?([a-z0-9-]+)/([a-z0-9._-]+)\.md\s*$", line)
        if not m:
            continue
        directory, slug = m.group(1), m.group(2)
        if slug == "index":
            current = directory
            order.setdefault(directory, [])
            continue
        if current == directory:
            order[directory].append(slug)
    return order


def index_order(directory: str) -> list[str]:
    """Topic slugs linked from a domain index, in the order they are listed.

    Only the first link on each bullet counts — the journey links that follow
    ("exercises · exam · flashcards") point at the same topic, not the next one.
    """
    path = os.path.join(DOCS, directory, "index.md")
    if not os.path.exists(path):
        return []
    slugs: list[str] = []
    for line in open(path, encoding="utf-8"):
        if not line.startswith("- ["):
            continue
        m = re.search(r"\]\(([a-z0-9-]+)\.md\)", line)
        if m and m.group(1) not in slugs:
            slugs.append(m.group(1))
    return slugs


def flashcards_next(directory: str, slug: str) -> str | None:
    """The target of the 'Continue to the next…' link, or None when absent."""
    path = os.path.join(DOCS, directory, f"{slug}-flashcards.md")
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()
    m = re.search(r"Continue to the next[^\n]*?\]\(([^)\s]+)\)", text)
    return m.group(1) if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--domain", help="check a single domain directory")
    args = ap.parse_args()

    domains = load_path()
    if args.domain:
        domains = [d for d in domains if d["dir"] == args.domain]
        if not domains:
            print(f"check_learning_path: no such domain '{args.domain}'", file=sys.stderr)
            return 1

    all_domains = load_path()
    nav = nav_order()
    errors: list[str] = []
    checked = 0

    for i, dom in enumerate(all_domains):
        if args.domain and dom["dir"] != args.domain:
            continue
        directory = dom["dir"]
        slugs = [t["slug"] for t in dom["topics"]]
        checked += len(slugs)

        # 1. Prerequisites must come earlier in the order.
        seen: set[str] = set()
        for t in dom["topics"]:
            for req in t.get("requires", []):
                if req not in seen:
                    errors.append(
                        f"{directory}: '{t['slug']}' requires '{req}', which is not "
                        f"ordered before it")
            seen.add(t["slug"])

        # 2. mkdocs.yml nav.
        got = nav.get(directory)
        if got is None:
            errors.append(f"{directory}: no nav section in mkdocs.yml")
        elif got != slugs:
            missing = [s for s in slugs if s not in got]
            extra = [s for s in got if s not in slugs]
            if missing:
                errors.append(f"{directory}: absent from mkdocs.yml nav: "
                              f"{', '.join(missing)}")
            if extra:
                errors.append(f"{directory}: in mkdocs.yml nav but not in the path: "
                              f"{', '.join(extra)}")
            if not missing and not extra:
                errors.append(f"{directory}: mkdocs.yml nav order differs\n"
                              f"      path: {' → '.join(slugs)}\n"
                              f"      nav:  {' → '.join(got)}")

        # 3. The domain index lists them in the same order.
        idx = [s for s in index_order(directory) if s in slugs]
        if idx and idx != slugs:
            errors.append(f"{directory}/index.md: '## Micro-chapters' order differs\n"
                          f"      path:  {' → '.join(slugs)}\n"
                          f"      index: {' → '.join(idx)}")

        # 4. Each flashcards deck points at the topic that actually follows.
        for j, slug in enumerate(slugs):
            target = flashcards_next(directory, slug)
            if target is None:
                continue
            if j + 1 < len(slugs):
                expected = f"{slugs[j + 1]}.md"
            elif i + 1 < len(all_domains):
                expected = f"../{all_domains[i + 1]['dir']}/index.md"
            else:
                continue
            if target.split("#")[0] != expected:
                errors.append(
                    f"{directory}/{slug}-flashcards.md: next-topic link is "
                    f"'{target}', the path says '{expected}'")

    if errors:
        print(f"check_learning_path: FAIL — {len(errors)} divergence(s) from "
              f"specs/learning_path.yml\n", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        print("\n  The path file is the source. Edit it there, then make the "
              "consumers match.", file=sys.stderr)
        return 1

    official = sum(1 for d in all_domains for t in d["topics"]
                   if t["status"] == "OFFICIAL")
    additional = sum(1 for d in all_domains for t in d["topics"]
                     if t["status"] == "ADDITIONAL")
    print(f"check_learning_path: OK — {checked} topic(s) agree with the path "
          f"({official} OFFICIAL, {additional} ADDITIONAL across "
          f"{len(all_domains)} domains).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

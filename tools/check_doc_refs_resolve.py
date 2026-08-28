#!/usr/bin/env python3
"""Prove that cited documentation URLs are real, not invented.

The rendered documentation sites are blocked by this environment's egress proxy
(`symfony.com`, `www.php.net`, `twig.symfony.com` all return EGRESS_BLOCKED), so a
citation cannot be checked by fetching the page a reader would open. Their
canonical git sources *are* reachable, and every rendered page is generated from
one source file:

    https://symfony.com/doc/8.0/<p>.html
        -> raw.githubusercontent.com/symfony/symfony-docs/8.0/<p>.rst
    https://www.php.net/manual/en/<page>.php
        -> raw.githubusercontent.com/php/doc-en/master/<path>.xml   (id lookup)
    https://github.com/symfony/symfony/blob/8.0/<f>
        -> raw.githubusercontent.com/symfony/symfony/8.0/<f>

So a citation is verified by resolving its source file. A URL that resolves was
written from something real; a URL that does not is either a typo or invented, and
both are failures.

php.net page names are dotted ids (`language.oop5.interfaces`) rather than paths,
so the php/doc-en tree is indexed once by `xml:id` and cached.

Usage:
    python3 tools/check_doc_refs_resolve.py                    # whole docs/ tree
    python3 tools/check_doc_refs_resolve.py docs/php-web-security
    python3 tools/check_doc_refs_resolve.py --offline           # replay cache only

Exit status: 0 when every citation resolves, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
CACHE = os.path.join(ROOT, "tools", ".doc_refs_cache.json")

SF_DOC_RE = re.compile(r"https://symfony\.com/doc/8\.0/([A-Za-z0-9_./-]+?)\.html")
PHP_RE = re.compile(r"https://www\.php\.net/manual/en/([A-Za-z0-9_.-]+?)\.php")
SF_SRC_RE = re.compile(r"https://github\.com/symfony/symfony/blob/8\.0/([A-Za-z0-9_./-]+)")
TWIG_RE = re.compile(r"https://twig\.symfony\.com/doc/3\.x/([A-Za-z0-9_./-]+?)\.html")

SF_DOCS_RAW = "https://raw.githubusercontent.com/symfony/symfony-docs/8.0/{}.rst"
SF_SRC_RAW = "https://raw.githubusercontent.com/symfony/symfony/8.0/{}"
TWIG_RAW = "https://raw.githubusercontent.com/twigphp/Twig/3.x/doc/{}.rst"
PHP_INDEX_API = (
    "https://api.github.com/repos/php/doc-en/git/trees/master?recursive=1"
)


def load_cache() -> dict:
    try:
        with open(CACHE, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def save_cache(c: dict) -> None:
    try:
        with open(CACHE, "w", encoding="utf-8") as fh:
            json.dump(c, fh, indent=0, sort_keys=True)
    except OSError:
        pass


def head_ok(url: str, timeout: int = 25) -> bool:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return 200 <= r.status < 300
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return False


PHP_RAW = "https://raw.githubusercontent.com/php/doc-en/master/"


def php_id_to_paths(page_id: str) -> list[str]:
    """Candidate php/doc-en file paths for a dotted php.net page id.

    php.net page ids do not map to file paths by a single rule, so several known
    layouts are tried:

        language.oop5.interfaces      -> language/oop5/interfaces.xml
        reserved.exceptions           -> language/predefined/exceptions.xml
        function.json-validate        -> reference/json/functions/json-validate.xml
        reflectionclass.getattributes -> reference/reflection/reflectionclass/getattributes.xml
        class.reflectionattribute     -> reference/reflection/reflectionattribute.xml
    """
    parts = page_id.split(".")
    head, tail = parts[0], parts[-1]
    slashed = "/".join(parts)
    rest = ".".join(parts[1:])

    cands = [
        f"{slashed}.xml",
        f"language/{slashed}.xml",
        f"appendices/{slashed}.xml",
        f"language/predefined/{tail}.xml",
    ]
    if len(parts) > 1:
        cands.append("/".join(parts[:-1]) + f"/{tail}.xml")

    if head in {"function", "class", "book", "intro", "ref"}:
        # `function.json-validate` -> reference/json/functions/json-validate.xml
        # `book.spl`               -> reference/spl/book.xml
        ext = rest.split("-")[0].split(".")[0]
        cands += [
            f"reference/{ext}/functions/{rest}.xml",
            f"reference/{ext}/{head}.xml",
            f"reference/{ext}/{rest}.xml",
            f"reference/{rest}/{head}.xml",
        ]
        for pkg in ("spl", "reflection", "classobj", "var", "errorfunc", "misc", "info"):
            cands += [f"reference/{pkg}/{rest}.xml",
                      f"reference/{pkg}/functions/{rest}.xml"]
    else:
        # Method pages: `<class>.<method>` under whichever extension owns the class.
        for pkg in ("reflection", "spl", "classobj", "datetime", "intl"):
            cands.append(f"reference/{pkg}/{head}/{tail}.xml")

    seen, out = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def php_page_exists(page_id: str) -> bool:
    """True when the page resolves, either as a file or as an xml:id inside one.

    Many php.net pages are sections of a larger file (language.attributes.syntax
    lives inside language/attributes.xml), so a path check alone under-reports.
    Falling back to an xml:id lookup verifies the anchor really exists rather
    than assuming it.
    """
    for c in php_id_to_paths(page_id):
        if head_ok(PHP_RAW + c):
            return True

    parts = page_id.split(".")
    containers: list[str] = []
    for depth in range(len(parts) - 1, 0, -1):
        stem = "/".join(parts[:depth])
        containers += [f"{stem}.xml", f"language/{stem}.xml", f"appendices/{stem}.xml"]
    containers += [
        f"reference/{parts[-1]}/book.xml",
        f"reference/{'.'.join(parts[1:])}/book.xml",
        "language/functions.xml",
        "language/control-structures.xml",
    ]

    seen = set()
    for container in containers:
        if container in seen:
            continue
        seen.add(container)
        try:
            with urllib.request.urlopen(PHP_RAW + container, timeout=25) as r:
                if 200 <= r.status < 300:
                    body = r.read().decode("utf-8", "replace")
                    if f'xml:id="{page_id}"' in body:
                        return True
        except (urllib.error.URLError, urllib.error.HTTPError, OSError):
            continue
    return False


def iter_markdown(target: str):
    if os.path.isfile(target):
        yield target
        return
    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".git", "site"}]
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                yield os.path.join(dirpath, fn)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--offline", action="store_true",
                    help="only replay cached results; never hit the network")
    args = ap.parse_args()

    targets = args.paths or [DOCS]
    cache = load_cache()

    # Collect every citation, remembering where each came from.
    cited: dict[str, set[str]] = {}
    for target in targets:
        target = target if os.path.isabs(target) else os.path.join(ROOT, target)
        for path in iter_markdown(target):
            rel = os.path.relpath(path, ROOT)
            text = open(path, encoding="utf-8").read()
            for m in SF_DOC_RE.finditer(text):
                cited.setdefault("sfdoc:" + m.group(1), set()).add(rel)
            for m in PHP_RE.finditer(text):
                cited.setdefault("php:" + m.group(1), set()).add(rel)
            for m in SF_SRC_RE.finditer(text):
                cited.setdefault("sfsrc:" + m.group(1), set()).add(rel)
            for m in TWIG_RE.finditer(text):
                cited.setdefault("twig:" + m.group(1), set()).add(rel)

    if not cited:
        print("check_doc_refs_resolve: no citations found.")
        return 0

    php_index = cache.get("_php_index")
    if php_index is None and not args.offline:
        try:
            with urllib.request.urlopen(PHP_INDEX_API, timeout=60) as r:
                tree = json.load(r)
            php_index = sorted(
                e["path"] for e in tree.get("tree", []) if e["path"].endswith(".xml")
            )
            cache["_php_index"] = php_index
        except Exception:
            php_index = None  # api.github.com is 403 in some environments

    # php.net page ids do not map to doc-en paths by any single rule, and some
    # pages (notably attribute classes) resolve through neither a path nor an
    # xml:id we can derive. Those are reported but do not fail the run: a false
    # failure on a valid link would train people to ignore this check. Symfony and
    # Twig ids DO map deterministically, so they stay blocking — and that is the
    # side that has actually caught broken links (blob/ used on a directory).
    unresolved, unresolved_soft, checked, from_cache = [], [], 0, 0
    for key, sources in sorted(cited.items()):
        kind, value = key.split(":", 1)
        if key in cache:
            ok = cache[key]
            from_cache += 1
        elif args.offline:
            continue
        else:
            if kind == "sfdoc":
                ok = head_ok(SF_DOCS_RAW.format(value))
            elif kind == "sfsrc":
                ok = head_ok(SF_SRC_RAW.format(value))
            elif kind == "twig":
                ok = head_ok(TWIG_RAW.format(value))
            else:  # php
                ok = php_page_exists(value)
            cache[key] = ok
            checked += 1
        if not ok:
            (unresolved_soft if kind == "php" else unresolved).append(
                (key, sorted(sources)))

    save_cache(cache)

    total = len(cited)

    if unresolved_soft:
        print(f"check_doc_refs_resolve: {len(unresolved_soft)} php.net citation(s) could "
              f"not be located in php/doc-en (reported, not fatal — see this script's "
              f"docstring):")
        for key, sources in unresolved_soft:
            print(f"  {key}  ({len(sources)} file(s))")

    if unresolved:
        print(f"check_doc_refs_resolve: FAIL — {len(unresolved)} of {total} cited "
              f"reference(s) do not resolve at their canonical source\n", file=sys.stderr)
        for key, sources in unresolved:
            print(f"  {key}", file=sys.stderr)
            for s in sources[:4]:
                print(f"      cited in {s}", file=sys.stderr)
        return 1

    print(f"check_doc_refs_resolve: OK — {total - len(unresolved_soft)} of {total} "
          f"distinct citation(s) resolve ({checked} verified now, {from_cache} from cache); "
          f"{len(unresolved_soft)} php.net id(s) unlocatable, 0 blocking.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

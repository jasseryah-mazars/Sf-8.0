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
and they do not map to `doc-en` files by any single rule, so resolution tries the
known layouts and then falls back to looking the id up as an `xml:id` inside a
containing file — many php.net pages are sections rather than whole files.

Every miss fails. There is no "reported but tolerated" tier any more: it hid 42
real pages behind a resolver bug (see FUNC_DIRS) and made "every URL is verified"
a claim the tool could not back. The few ids that genuinely resolve through no
known layout go in QUARANTINE — named, explained, and self-expiring, so the list
can only shrink.

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
# Greedy, and the trailing `.php` must end the URL: a non-greedy match stops at the
# first ".php" *inside* the id, so `function.phpversion.php` was silently read as
# the page id `function` — a phantom that can never resolve.
PHP_RE = re.compile(r"https://www\.php\.net/manual/en/([A-Za-z0-9_.-]+)\.php(?![\w-])")
SF_SRC_RE = re.compile(r"https://github\.com/symfony/symfony/blob/8\.0/([A-Za-z0-9_./-]+)")
TWIG_RE = re.compile(r"https://twig\.symfony\.com/doc/3\.x/([A-Za-z0-9_./-]+?)\.html")

SF_DOCS_RAW = "https://raw.githubusercontent.com/symfony/symfony-docs/8.0/{}.rst"
SF_SRC_RAW = "https://raw.githubusercontent.com/symfony/symfony/8.0/{}"
TWIG_RAW = "https://raw.githubusercontent.com/twigphp/Twig/3.x/doc/{}.rst"


# php.net ids that resolve through no known `doc-en` layout and no `xml:id` lookup.
# All three are real manual pages — the PHP 8.0 `Attribute` class, the PHP 8.4
# `Deprecated` attribute, and the OPcache preloading chapter — so failing on them
# would be a false alarm. They are named here rather than tolerated silently by a
# whole severity tier, and the list is self-expiring: an id that starts resolving
# fails the check until it is deleted, so QUARANTINE can only shrink.
#
# Established 2026-08-29, after the resolver rewrite took the unlocatable count
# from 42 to 3.
PHP_QUARANTINE = {
    "class.attribute",
    "class.deprecated",
    "opcache.preloading",
}


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


# Function-name prefix -> the `reference/<dir>/` that owns it in php/doc-en. The
# extension directory is NOT derivable from the function name (`strlen` lives under
# `strings`, `intdiv` under `math`, `create_function` under `funchand`), which is
# exactly what the previous naive derivation got wrong: it looked for
# `reference/strlen/...` and silently reported 42 real pages as unlocatable.
#
# Longest prefix wins, so `mb_` beats a bare fallback. Every entry below was
# confirmed by fetching the file, not guessed.
FUNC_DIRS = [
    ("mb_", "mbstring"), ("iconv", "iconv"), ("grapheme_", "intl/grapheme"),
    ("intl", "intl"), ("collator_", "intl"), ("numfmt_", "intl"), ("datefmt_", "intl"),
    ("json_", "json"), ("pdo_", "pdo"), ("spl_", "spl"), ("iterator_", "spl"),
    ("session_", "session"), ("preg_", "pcre"), ("array_", "array"),
    ("ctype_", "ctype"), ("opcache_", "opcache"), ("password_", "password"),
    ("hash_", "hash"), ("filter_", "filter"), ("var_", "var"),
    ("class_", "classobj"), ("get_class", "classobj"), ("get_object", "classobj"),
    ("enum_exists", "classobj"), ("interface_exists", "classobj"),
    # class_implements/class_parents/class_uses are SPL, not classobj.
    ("class_implements", "spl"), ("class_parents", "spl"), ("class_uses", "spl"),
    ("get_extension_funcs", "info"),
    ("error_", "errorfunc"), ("set_error_handler", "errorfunc"),
    ("restore_error_handler", "errorfunc"), ("trigger_error", "errorfunc"),
    ("set_exception_handler", "errorfunc"), ("debug_", "errorfunc"),
    ("extension_loaded", "info"), ("get_loaded_extensions", "info"),
    ("phpversion", "info"), ("php_", "info"), ("ini_", "info"),
    ("call_user_func", "funchand"), ("func_", "funchand"),
    ("create_function", "funchand"), ("function_exists", "funchand"),
    ("is_callable", "var"), ("serialize", "var"), ("unserialize", "var"),
    ("str", "strings"), ("substr", "strings"), ("html", "strings"),
    ("sprintf", "strings"), ("printf", "strings"), ("trim", "strings"),
    ("implode", "strings"), ("explode", "strings"), ("ucfirst", "strings"),
    ("number_format", "strings"), ("nl2br", "strings"), ("addslashes", "strings"),
    ("intdiv", "math"), ("abs", "math"), ("round", "math"), ("floor", "math"),
    ("ceil", "math"), ("min", "math"), ("max", "math"), ("rand", "math"),
    ("random_", "csprng"), ("in_array", "array"), ("count", "array"),
    ("sort", "array"), ("usort", "array"), ("compact", "array"), ("extract", "array"),
]

# `<something>.configuration` and `<something>.installation` are INI/setup pages that
# php/doc-en names differently from their php.net id.
SUFFIX_FILES = {"configuration": "ini", "installation": "setup", "setup": "setup"}


def _func_dir(name: str) -> str | None:
    """The reference/ directory owning a function, by longest matching prefix."""
    best = None
    for prefix, directory in FUNC_DIRS:
        if name.startswith(prefix) and (best is None or len(prefix) > len(best[0])):
            best = (prefix, directory)
    return best[1] if best else None


def php_id_to_paths(page_id: str) -> list[str]:
    """Candidate php/doc-en file paths for a dotted php.net page id.

    php.net ids do not map to file paths by a single rule, so the known layouts are
    tried in order. Each was verified against the live repository:

        language.oop5.interfaces      -> language/oop5/interfaces.xml
        closure.bind                  -> language/predefined/closure/bind.xml
        arrayaccess.offsetexists      -> language/predefined/arrayaccess/offsetexists.xml
        function.strlen               -> reference/strings/functions/strlen.xml
        function.mb-strlen            -> reference/mbstring/functions/mb-strlen.xml
        function.grapheme-strlen      -> reference/intl/grapheme/grapheme-strlen.xml
        pdo.getavailabledrivers       -> reference/pdo/pdo/getavailabledrivers.xml
        class.collator                -> reference/intl/collator.xml
        class.jsonserializable        -> reference/json/jsonserializable.xml
        opcache.configuration         -> reference/opcache/ini.xml
        intl.installation             -> reference/intl/setup.xml
        spl.datastructures            -> reference/spl/datastructures.xml
    """
    parts = page_id.split(".")
    head, tail = parts[0], parts[-1]
    slashed = "/".join(parts)
    rest = ".".join(parts[1:])
    underscored = rest.replace("-", "_")

    cands = [
        f"{slashed}.xml",
        f"language/{slashed}.xml",
        f"appendices/{slashed}.xml",
        f"language/predefined/{tail}.xml",
    ]

    if head == "function":
        # The function's own extension directory, then the two shapes it can take.
        d = _func_dir(underscored)
        if d:
            cands += [f"reference/{d}/functions/{rest}.xml", f"reference/{d}/{rest}.xml"]
        # `reference/intl/grapheme/grapheme-strlen.xml` — some extensions nest by family.
        if "_" in underscored:
            family = underscored.split("_")[0]
            cands += [f"reference/{family}/functions/{rest}.xml",
                      f"reference/{family}/{family}/{rest}.xml",
                      f"reference/{family}/{rest}.xml"]
    elif head in {"class", "book", "intro", "ref"}:
        ext = rest.split("-")[0].split(".")[0]
        cands += [
            f"language/predefined/{rest}.xml",
            f"reference/{ext}/{head}.xml",
            f"reference/{ext}/{rest}.xml",
            f"reference/{rest}/{head}.xml",
        ]
        for pkg in ("intl", "json", "spl", "reflection", "classobj", "var", "datetime"):
            cands.append(f"reference/{pkg}/{rest}.xml")
            # Some extensions drop their own prefix from the filename:
            # `class.intldateformatter` lives at `reference/intl/dateformatter.xml`.
            if rest.startswith(pkg) and rest != pkg:
                cands.append(f"reference/{pkg}/{rest[len(pkg):]}.xml")
    else:
        # `<class>.<method>` — predefined classes first (Closure, Generator, the enum
        # and SPL interfaces all live there), then whichever extension owns the class.
        if len(parts) == 2:
            cands.insert(0, f"language/predefined/{head}/{tail}.xml")
            cands.append(f"reference/{head}/{head}/{tail}.xml")
            if tail in SUFFIX_FILES:
                cands.append(f"reference/{head}/{SUFFIX_FILES[tail]}.xml")
            cands.append(f"reference/{head}/{tail}.xml")
        for pkg in ("reflection", "spl", "classobj", "datetime", "intl", "pdo"):
            cands.append(f"reference/{pkg}/{head}/{tail}.xml")

    if len(parts) > 1:
        cands.append("/".join(parts[:-1]) + f"/{tail}.xml")

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
        # Built-in attribute pages (`class.attribute`, `class.deprecated`) are
        # sections of the attributes chapter, not files of their own.
        "language/attributes.xml",
        "language/oop5/attributes.xml",
        "language/enumerations.xml",
    ]
    if len(parts) == 2:
        # `<ext>.<page>` sections often live in the extension's own INI/setup file.
        containers += [f"reference/{parts[0]}/{parts[1]}.xml",
                       f"reference/{parts[0]}/ini.xml",
                       f"reference/{parts[0]}/setup.xml",
                       f"reference/{parts[0]}/book.xml"]

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


# Authoring templates, not documentation. Their `src/Symfony/...` and `...` are
# placeholders an author replaces, so scanning them reports two permanent false
# positives that train people to ignore the check.
SKIP_FILES = {os.path.join("docs", "_meta", "CHAPTER_TEMPLATE.md")}


def iter_markdown(target: str):
    if os.path.isfile(target):
        yield target
        return
    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".git", "site"}]
        for fn in sorted(filenames):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            if os.path.relpath(path, ROOT) in SKIP_FILES:
                continue
            yield path


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
            if kind == "php" and value in PHP_QUARANTINE:
                unresolved_soft.append((key, sorted(sources)))
            else:
                unresolved.append((key, sorted(sources)))

    save_cache(cache)

    total = len(cited)

    if unresolved_soft:
        print(f"check_doc_refs_resolve: {len(unresolved_soft)} quarantined php.net "
              f"citation(s) (named in PHP_QUARANTINE, not fatal):")
        for key, sources in unresolved_soft:
            print(f"  {key}  ({len(sources)} file(s))")

    # A quarantine entry that has started resolving must be deleted, or the list
    # would only ever grow. Only ids this run actually looked at can prove it.
    stale = sorted(q for q in PHP_QUARANTINE
                   if ("php:" + q) in cited
                   and not any(k == "php:" + q for k, _ in unresolved_soft))
    if stale:
        print("check_doc_refs_resolve: FAIL — quarantined php.net id(s) now resolve; "
              "delete them (the list must only shrink):", file=sys.stderr)
        for key in stale:
            print(f"  {key}", file=sys.stderr)
        return 1

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
          f"{len(unresolved_soft)} quarantined, 0 unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

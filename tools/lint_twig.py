#!/usr/bin/env python3
"""Partial Twig syntax check for every ```twig snippet in docs/ (P1-02).

**Scope, stated honestly:** no real Twig lexer/parser is available in this
environment (no `Twig\\Environment` PHP class installed, no network access
to `packagist.org` to install one via Composer — confirmed, not assumed;
Composer plugins are also disabled in this sandbox). This script therefore
does **not** perform full Twig grammar validation. It checks one structural
property that is still a real, useful signal of a broken snippet: paired
block tags (`if`/`endif`, `for`/`endfor`, `block`/`endblock`,
`macro`/`endmacro`, `autoescape`/`endautoescape`, `embed`/`endembed`,
`apply`/`endapply`, `verbatim`/`endverbatim`, `set ... %}...{% endset`,
`sandbox`/`endsandbox`, `filter`/`endfilter`) are correctly nested and
closed — a lightweight stack-based check, not a full grammar. `{# ... #}`
comment spans are stripped before this scan, so a tag *name mentioned in
prose inside a comment* (e.g. `{# a theme is a set of {% block %}s #}`) is
correctly not mistaken for a real opening tag.

A deliberately naive first version of this script also tried counting raw
`{{`/`}}` substring occurrences for balance — dropped after it produced
false positives on entirely valid Twig containing nested hash/array
literals (e.g. `{{ form_start(form, {'attr': {'novalidate': 'novalidate'}})
}}` — the adjacent `}}` from two nested `{'...': ...}` literals is not a
print-delimiter close, and naive substring counting cannot tell the
difference). Removed rather than left in with a wrong result — see
specs/RemediationLog.md P1-02 for this exact false-positive history.

A snippet can pass this check and still contain a real Twig error (e.g. a
misspelled filter name, a wrong argument) — this is explicitly NOT claimed
to be caught here. See specs/RemediationLog.md P1-02 for the full, honest
scope of what is and is not automated for Twig.

Exit non-zero on any real structural imbalance found. Run:
python tools/lint_twig.py
"""
from __future__ import annotations
import glob, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r"```(?:twig|html\+twig)\n(.*?)```", re.DOTALL)

COMMENT_RE = re.compile(r"\{#.*?#\}", re.DOTALL)

PAIRED_TAGS = {
    "if": "endif", "for": "endfor", "block": "endblock", "macro": "endmacro",
    "autoescape": "endautoescape", "embed": "endembed", "apply": "endapply",
    "verbatim": "endverbatim", "sandbox": "endsandbox", "filter": "endfilter",
    "set": "endset",  # only the block form (`{% set x %}...{% endset %}`) pairs
    "with": "endwith", "spaceless": "endspaceless", "trans": "endtrans",
    "deprecated": None,  # single-tag, never paired
}
OPENERS = {k for k, v in PAIRED_TAGS.items() if v}
CLOSERS = {v: k for k, v in PAIRED_TAGS.items() if v}
# `else`/`elseif` belong to an already-open `if`; `endif` closes it — no
# separate stack entry needed for them.

TAG_RE = re.compile(r"\{%-?\s*(\w+)")


def check_block_tags(code: str) -> str | None:
    code = COMMENT_RE.sub("", code)  # tag names mentioned in prose inside a comment aren't real tags
    stack: list[str] = []
    for m in TAG_RE.finditer(code):
        tag = m.group(1)
        if tag == "set":
            # `{% set x = y %}` (single-tag, has '=') vs `{% set x %}...{% endset %}`
            # (block form). Only the block form participates in pairing.
            line_end = code.find("%}", m.end())
            segment = code[m.end():line_end] if line_end != -1 else ""
            if "=" in segment:
                continue
        if tag in OPENERS:
            stack.append(tag)
        elif tag in CLOSERS:
            expected = CLOSERS[tag]
            if not stack:
                return f"'{tag}' with no matching open tag"
            if stack[-1] != expected:
                return f"'{tag}' does not match innermost open tag '{stack[-1]}'"
            stack.pop()
    if stack:
        return f"unclosed tag(s): {', '.join(stack)}"
    return None


def main() -> int:
    linted = 0
    fails = []
    for f in glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True):
        if "/_meta/" in f:
            continue
        text = open(f, encoding="utf-8").read()
        for m in BLOCK.finditer(text):
            code = m.group(1)
            if not code.strip():
                continue
            linted += 1
            err = check_block_tags(code)
            if err:
                fails.append((os.path.relpath(f, ROOT), err))
    print(f"linted {linted} Twig snippets (block-tag pairing only, "
          f"NOT full Twig grammar — see this script's own docstring); {len(fails)} failure(s)")
    for rel, msg in fails:
        print(f"  FAIL {rel}: {msg}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Carry hand-written blocks across a regeneration.

`docs/exams/`, `docs/revision/flashcards/` and `docs/revision/sheets/` are written
from scratch by their generators, but 48 of those files carry a hand-written
`## 🧠 Pour les nuls` section that no generator emits. Before this module existed,
running any generator silently deleted every one of them — a landmine, because the
loss is invisible until a reader notices the section is gone.

The block is genuinely hand-written and per-file (it explains *that* page in
French), so it cannot be templated: there is no rule that derives it. It can only
be preserved. `carry_over()` lifts it out of the file being replaced and splices it
back into the new text at the same place it has in every one of those files —
immediately before the first `## ` heading, after the H1 and its intro.

Regeneration therefore becomes idempotent for the block: generate, carry over,
write. A file that has no such block is passed through unchanged.

Usage — build the text FIRST, then open, or the block is lost:

    from generated_blocks import carry_over
    text = carry_over(path, "\\n".join(lines))
    open(path, "w").write(text)

Writing it as `open(path, "w").write(carry_over(path, ...))` silently defeats the
whole module: Python evaluates `open(path, "w")` first, which truncates the file,
so `carry_over` then reads nothing back.
"""
from __future__ import annotations

import os
import re

HEADING = "## 🧠 Pour les nuls"

# The block ends at whichever comes first: the next heading of any level, a `---`
# rule, or the first collapsed `???` block. Several of these pages have no second
# heading at all — the chapter exams start their questions after a rule, the
# flashcard decks go straight into `??? question` — so a heading-only terminator
# would swallow the entire rest of the file.
_SECTION_RE = re.compile(
    r"(?ms)^" + re.escape(HEADING) + r"\s*$.*?"
    r"(?=^#{1,6}\s|^-{3,}\s*$|^\?\?\?|\Z)"
)
# Insert at the same boundary: the first `## ` heading, `---` rule, or `???`
# block — the three places these pages actually start their body.
_ANCHOR_RE = re.compile(r"(?m)^(?:##\s|-{3,}\s*$|\?\?\?)")


def extract(text: str) -> str:
    """The full `## 🧠 Pour les nuls` section of `text`, or '' when absent."""
    m = _SECTION_RE.search(text)
    return m.group(0).rstrip() if m else ""


def carry_over(path: str, new_text: str) -> str:
    """`new_text` with the block from the file at `path` spliced back in.

    Returns `new_text` unchanged when the old file has no block, or when the new
    text already carries one (so a generator that learns to emit it later wins).
    """
    if not os.path.exists(path):
        return new_text
    with open(path, encoding="utf-8") as fh:
        block = extract(fh.read())
    if not block or HEADING in new_text:
        return new_text

    m = _ANCHOR_RE.search(new_text)
    at = m.start() if m else len(new_text.rstrip()) + 1
    head, tail = new_text[:at].rstrip("\n"), new_text[at:]
    return f"{head}\n\n{block}\n\n{tail}" if tail else f"{head}\n\n{block}\n"

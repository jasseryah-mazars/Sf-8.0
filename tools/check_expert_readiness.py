#!/usr/bin/env python3
"""Decide, per topic, whether it is genuinely ready for Expert-level revision.

A status, not a score. Every mandatory criterion must pass; one failure is enough
for NOT EXPERT READY. Averaging would let a topic with a wrong answer in it look
"96% ready", which is exactly the kind of reassuring number this project must not
produce.

Criteria, per topic:

  files        lesson, exercises, exam and flashcards all present and non-empty
  volume       >= 28 exam questions, >= 30 flashcards
  types        all nine question types present (single answer, multiple answers,
               true/false, code analysis, execution order, configuration
               consequence, debugging, edge case, Expert trap)
  diversity    >= 2 questions of each of the six reasoning types, and no
               near-duplicate questions
  concepts     every concept in specs/concepts/<domain>.yml that the lesson
               teaches also appears in the exam AND on a flashcard; and no
               question or card matches no concept at all
  path         the topic is in specs/learning_path.yml with its status

Volume is a floor, never a pass mark: 28 repetitive questions are worth three, so
diversity and concept coverage are what actually decide the verdict.

A topic with no concept file is NOT EXPERT READY. Absence of a measurement is not
evidence of coverage — it is the reason the count cannot be trusted.

Usage:
    python3 tools/check_expert_readiness.py
    python3 tools/check_expert_readiness.py --domain php-web-security
    python3 tools/check_expert_readiness.py --topic php-web-security/attributes
    python3 tools/check_expert_readiness.py --summary

Exit status: 0 when every topic that has been migrated is EXPERT READY.
Topics not yet migrated to the four-file journey are skipped, not failed —
they are simply not in scope for this check yet.
"""
from __future__ import annotations

import argparse
import difflib
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
CONCEPTS_DIR = os.path.join(ROOT, "specs", "concepts")
PATH_FILE = os.path.join(ROOT, "specs", "learning_path.yml")

MIN_QUESTIONS = 28
MIN_CARDS = 30
MIN_PER_REASONING_TYPE = 2

# The nine question types. Each maps to the markers that identify it in a question
# heading or body — questions label themselves ("Q7 · Code analysis"), and the
# fallback patterns catch the ones that describe rather than label.
TYPES = {
    "single answer":            [r"\bsingle answer\b", r"(?m)^\s*- A\."],
    "multiple answers":         [r"multiple answers?", r"select (all|two|three)",
                                 r"which (two|three)\b"],
    "true/false":               [r"true\s*/\s*false", r"\btrue or false\b"],
    "code analysis":            [r"code analysis", r"what does .{0,40}(output|print|return)",
                                 r"what is printed"],
    "execution order":          [r"execution order", r"\bin what order\b",
                                 r"\border of (execution|calls)\b"],
    "configuration consequence": [r"configuration consequence", r"\bwhat happens if\b.{0,60}config",
                                  r"\bwith this configuration\b"],
    "debugging":                [r"\bdebugging\b", r"why does .{0,40}(fail|throw|not work)",
                                 r"\bdiagnose\b"],
    "edge case":                [r"edge case"],
    "Expert trap":              [r"expert trap", r"\btrap\b"],
}

# The six that test reasoning rather than recall. These carry the >= 2 floor: a
# topic can hit 28 questions on recall alone and teach nobody anything.
REASONING_TYPES = ["code analysis", "execution order", "configuration consequence",
                   "debugging", "edge case", "Expert trap"]

SUFFIXES = {"exercises": "-exercises.md", "exam": "-exam.md",
            "flashcards": "-flashcards.md"}


def read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def load_path() -> dict[str, dict]:
    """Topic key 'domain/slug' -> its learning-path entry."""
    out = {}
    for dom in yaml.safe_load(read(PATH_FILE))["domains"]:
        for t in dom["topics"]:
            out[f'{dom["dir"]}/{t["slug"]}'] = dict(t, domain=dom["dir"])
    return out


def load_concepts() -> dict[str, list[dict]]:
    """Topic key 'domain/slug' -> its concept list, for domains that have a file."""
    out: dict[str, list[dict]] = {}
    if not os.path.isdir(CONCEPTS_DIR):
        return out
    for fn in sorted(os.listdir(CONCEPTS_DIR)):
        if not fn.endswith(".yml"):
            continue
        data = yaml.safe_load(read(os.path.join(CONCEPTS_DIR, fn))) or {}
        domain = data.get("domain", fn[:-4])
        for slug, spec in (data.get("topics") or {}).items():
            out[f"{domain}/{slug}"] = spec.get("concepts") or []
    return out


def split_questions(text: str) -> list[str]:
    """Each `??? question` block, body included."""
    parts = re.split(r"(?m)^\?\?\?\s+question\s+", text)
    return [p for p in parts[1:] if p.strip()]


def question_types(block: str) -> set[str]:
    low = block.lower()
    found = set()
    for name, patterns in TYPES.items():
        if any(re.search(p, low if p.islower() or "\\" in p else block, re.I | re.M)
               for p in patterns):
            found.add(name)
    return found


def prompt_of(block: str) -> str:
    """The question's actual prompt, not its heading label.

    Comparing headings is useless and actively misleading: every question begins
    "Question 9 · Configuration consequence", so two unrelated questions that share
    a type label look identical. The prompt is the indented text under the heading,
    up to the first answer option or the collapsed answer.
    """
    # A flashcard's heading IS its prompt ("What does f(...) produce?"); an exam
    # question's heading is only a label. Tell them apart by shape, not by file.
    heading = block.split("\n", 1)[0].strip().strip('"')
    if not re.match(r"^(Q\d+|Question\s+\d+)\b", heading):
        return heading

    lines = block.split("\n")[1:]
    out = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if out:
                break
            continue
        if stripped.startswith(("- ", "??? ", "!!! ", "```")):
            break
        out.append(stripped)
    return " ".join(out) or block.split("\n", 1)[0].strip().strip('"')


def near_duplicates(blocks: list[str]) -> list[tuple[str, str]]:
    """Pairs of questions that differ only cosmetically.

    A question is not new because a class or method name changed, so the
    comparison strips identifiers and compares what is left: the sentence shape.
    """
    def shape(b: str) -> str:
        """The prompt, normalised — identifiers KEPT.

        Stripping inline code was wrong: it deletes the subject. "Which statement
        about `PDO` is correct?" and "Which statement about
        `composer check-platform-reqs` is correct?" both collapse to the same stock
        phrasing, and two unrelated questions look identical. Keeping the
        identifiers still catches the case this is for — the same question with one
        class name swapped stays far above the threshold, because only one token of
        many has changed.
        """
        s = prompt_of(b).lower().replace("`", " ")
        s = re.sub(r"\bq\d+\b|\bquestion \d+\b", " ", s)
        s = re.sub(r"[^a-z0-9_ ]+", " ", s)
        return " ".join(s.split())

    shapes = [(shape(b), prompt_of(b)) for b in blocks]
    dups = []
    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            a, b = shapes[i][0], shapes[j][0]
            if not a or not b or min(len(a), len(b)) < 25:
                continue
            if difflib.SequenceMatcher(None, a, b).ratio() >= 0.92:
                dups.append((shapes[i][1], shapes[j][1]))
    return dups


def mentions(text: str, keywords: list[str]) -> bool:
    low = text.lower()
    return any(k.lower() in low for k in keywords)


def check_topic(key: str, entry: dict, concepts: list[dict] | None) -> list[str]:
    """Mandatory-criterion failures for one topic. Empty means EXPERT READY."""
    domain, slug = key.split("/", 1)
    base = os.path.join(DOCS, domain, slug)
    lesson = read(base + ".md")
    files = {name: read(base + suf) for name, suf in SUFFIXES.items()}

    fail: list[str] = []
    for name, text in files.items():
        if len(text.strip()) < 200:
            fail.append(f"{name} file missing or empty")
    if fail:
        return fail

    questions = split_questions(files["exam"])
    cards = split_questions(files["flashcards"])

    if len(questions) < MIN_QUESTIONS:
        fail.append(f"{len(questions)} exam questions, floor is {MIN_QUESTIONS}")
    if len(cards) < MIN_CARDS:
        fail.append(f"{len(cards)} flashcards, floor is {MIN_CARDS}")

    per_type: dict[str, int] = {t: 0 for t in TYPES}
    for q in questions:
        for t in question_types(q):
            per_type[t] += 1
    absent = [t for t, n in per_type.items() if n == 0]
    if absent:
        fail.append(f"question type(s) absent: {', '.join(sorted(absent))}")
    thin = [f"{t} ({per_type[t]})" for t in REASONING_TYPES
            if 0 < per_type[t] < MIN_PER_REASONING_TYPE]
    if thin:
        fail.append(f"fewer than {MIN_PER_REASONING_TYPE} question(s) of: "
                    f"{', '.join(thin)}")

    dups = near_duplicates(questions)
    if dups:
        fail.append(f"{len(dups)} near-duplicate question pair(s), first: "
                    f"'{dups[0][0][:60]}' ~ '{dups[0][1][:60]}'")

    if concepts is None:
        fail.append(f"no concept matrix — add {domain}.yml to specs/concepts/ "
                    f"(a missing measurement is not coverage)")
        return fail

    taught = [c for c in concepts if mentions(lesson, c["keywords"])]
    if not taught:
        fail.append("no concept from the matrix appears in the lesson — "
                    "the keyword set is probably stale")
    unexamined = [c["id"] for c in taught if not mentions(files["exam"], c["keywords"])]
    uncarded = [c["id"] for c in taught
                if not mentions(files["flashcards"], c["keywords"])]
    if unexamined:
        fail.append(f"taught but never examined: {', '.join(unexamined)}")
    if uncarded:
        fail.append(f"taught but on no flashcard: {', '.join(uncarded)}")

    orphan_q = [prompt_of(q) for q in questions
                if not any(mentions(q, c["keywords"]) for c in concepts)]
    orphan_c = [prompt_of(c) for c in cards
                if not any(mentions(c, x["keywords"]) for x in concepts)]
    if orphan_q:
        fail.append(f"{len(orphan_q)} question(s) match no known concept, first: "
                    f"'{orphan_q[0][:70]}'")
    if orphan_c:
        fail.append(f"{len(orphan_c)} flashcard(s) match no known concept, first: "
                    f"'{orphan_c[0][:70]}'")
    return fail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--domain")
    ap.add_argument("--topic", help="'domain/slug'")
    ap.add_argument("--summary", action="store_true",
                    help="one line per topic, no detail")
    args = ap.parse_args()

    path = load_path()
    concepts = load_concepts()

    keys = sorted(path)
    if args.domain:
        keys = [k for k in keys if k.startswith(args.domain + "/")]
    if args.topic:
        keys = [k for k in keys if k == args.topic]
    if not keys:
        print("check_expert_readiness: no matching topic", file=sys.stderr)
        return 1

    ready, not_ready, skipped = [], [], []
    for key in keys:
        domain, slug = key.split("/", 1)
        if not os.path.exists(os.path.join(DOCS, domain, slug + "-exam.md")):
            skipped.append(key)
            continue
        fails = check_topic(key, path[key], concepts.get(key))
        (ready if not fails else not_ready).append((key, fails))

    for key, fails in not_ready:
        print(f"NOT EXPERT READY  {key}")
        if not args.summary:
            for f in fails:
                print(f"      · {f}")
    for key, _ in ready:
        print(f"EXPERT READY      {key}")

    total = len(ready) + len(not_ready)
    print(f"\ncheck_expert_readiness: {len(ready)}/{total} topic(s) EXPERT READY"
          + (f"; {len(skipped)} not yet migrated to the four-file journey"
             if skipped else ""))
    if not_ready:
        print("  A single failed criterion withholds the status. There is no "
              "partial credit here by design.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

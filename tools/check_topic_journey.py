#!/usr/bin/env python3
"""Blocking check for the per-topic Expert learning journey.

A topic that has been restructured owns four files:

    docs/<domain>/<topic>.md              the lesson
    docs/<domain>/<topic>-exercises.md    guided practice
    docs/<domain>/<topic>-exam.md         certification questions
    docs/<domain>/<topic>-flashcards.md   active recall

This script only inspects topics that have **started** the migration (at least one
activity file exists). Untouched topics are reported as such and never fail the
build, so the domains can be migrated one at a time.

What it enforces, and why each rule exists:

* all four files present and non-empty — a half-migrated topic is a dead end;
* the lesson no longer carries a `## Certification questions` section — that
  content belongs in the exam file, and leaving both duplicates the questions;
* every exam answer, exercise hint and exercise solution sits inside a collapsed
  `???` block — an answer visible before the click destroys the retrieval practice
  the page exists for;
* every revealed answer/solution carries an explanation *and* a reference;
* the journey links exist in both directions and resolve on disk;
* no `symfony.com/doc/current` anywhere — references must pin 8.0;
* every lesson keeps its French `## 🧠 Pour les nuls` section, and no other
  section drifts into French;
* no TODO/placeholder markers.

Exit status: 0 when every migrated topic is complete and correct, 1 otherwise.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

SUFFIXES = ("-exercises.md", "-exam.md", "-flashcards.md")

# Domain directories that hold Certification Domains topics.
DOMAINS = (
    "php-web-security", "http", "architecture", "dependency-injection", "controllers",
    "routing", "twig", "validation", "forms", "security", "http-caching", "console",
    "messenger", "testing", "miscellaneous",
)

CERT_Q_RE = re.compile(r"(?m)^##\s+Certification questions\s*$")
POUR_LES_NULS_RE = re.compile(r"(?m)^##\s+.*Pour les nuls\s*$")
DOC_CURRENT_RE = re.compile(r"symfony\.com/doc/current")
PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|XXX|TBD)\b")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+?)(?:#[^)]*)?\)")
DETAILS_RE = re.compile(r"(?m)^(\s*)\?\?\?\+?\s+(\w+)\s+\"([^\"]*)\"")

# Non-code lines that are strong evidence of French prose leaking outside the
# "Pour les nuls" section. Deliberately narrow: these words do not occur in
# English technical prose, so a hit is a real language mix, not a false alarm.
FRENCH_MARKERS = re.compile(
    r"\b(c'est|qu'il|nous|vous|votre|cette|toujours|jamais|lorsque|"
    r"pourquoi|parce que|ensuite|donc|ainsi|à la|de la|du coup)\b",
    re.IGNORECASE,
)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def strip_code_fences(text: str) -> str:
    return re.sub(r"(?ms)^```.*?^```", "", text)


def pour_les_nuls_span(text: str) -> tuple[int, int] | None:
    m = POUR_LES_NULS_RE.search(text)
    if not m:
        return None
    nxt = re.compile(r"(?m)^##\s+").search(text, m.end())
    return (m.start(), nxt.start() if nxt else len(text))


def find_topics() -> dict[str, list[str]]:
    """Map domain -> list of topic stems that have started the migration."""
    started: dict[str, list[str]] = {}
    for domain in DOMAINS:
        d = os.path.join(DOCS, domain)
        if not os.path.isdir(d):
            continue
        stems = set()
        for fn in os.listdir(d):
            if fn.endswith(".fr.md") or not fn.endswith(".md"):
                continue
            for suf in SUFFIXES:
                if fn.endswith(suf):
                    stems.add(fn[: -len(suf)])
        if stems:
            started[domain] = sorted(stems)
    return started


def check_collapsed_answers(rel: str, text: str, kind: str) -> list[str]:
    """Every answer/solution must live inside a collapsed ??? block."""
    errors: list[str] = []
    body = strip_code_fences(text)

    if kind == "exam":
        # Each question block must contain a nested collapsed answer.
        questions = re.findall(r'(?m)^\?\?\?\s+question\s+"', body)
        answers = re.findall(r'(?m)^\s+\?\?\?\s+success\s+"Show answer"', body)
        if not questions:
            errors.append(f"{rel}: no '??? question' blocks found in an exam file")
        if len(answers) < len(questions):
            errors.append(
                f"{rel}: {len(questions)} question(s) but only {len(answers)} collapsed "
                f"'Show answer' block(s) — every answer must be hidden until clicked"
            )
        for label in ("**Correct answer", "**Explanation:**", "**Official reference:**"):
            if body.count(label) < len(questions):
                errors.append(
                    f"{rel}: {len(questions)} question(s) but only {body.count(label)} "
                    f"occurrence(s) of '{label}' — each answer needs it"
                )
        # An expanded '???+' would render open; that defeats the purpose.
        if re.search(r'(?m)^\s*\?\?\?\+\s+success', body):
            errors.append(f"{rel}: uses '???+' for an answer — it would render expanded")

    if kind == "exercises":
        exercises = re.findall(r"(?m)^##\s+Exercise\s+\d+", body)
        hints = re.findall(r'(?m)^\?\?\?\s+tip\s+"Show a hint"', body)
        sols = re.findall(r'(?m)^\?\?\?\s+success\s+"Show the solution"', body)
        if not exercises:
            errors.append(f"{rel}: no '## Exercise N' sections found")
        if len(hints) < len(exercises):
            errors.append(
                f"{rel}: {len(exercises)} exercise(s) but {len(hints)} hidden hint(s)"
            )
        if len(sols) < len(exercises):
            errors.append(
                f"{rel}: {len(exercises)} exercise(s) but {len(sols)} hidden solution(s)"
            )
        for label in ("**Certification takeaway:**", "**Official reference:**"):
            if body.count(label) < len(exercises):
                errors.append(
                    f"{rel}: {len(exercises)} exercise(s) but only {body.count(label)} "
                    f"occurrence(s) of '{label}'"
                )
        if re.search(r'(?m)^\s*\?\?\?\+\s+success', body):
            errors.append(f"{rel}: uses '???+' for a solution — it would render expanded")

    if kind == "flashcards":
        prompts = re.findall(r'(?m)^\?\?\?\s+question\s+"', body)
        answers = re.findall(r'(?m)^\s+\?\?\?\s+success\s+"Show answer"', body)
        if not prompts:
            errors.append(f"{rel}: no '??? question' cards found")
        if len(answers) < len(prompts):
            errors.append(
                f"{rel}: {len(prompts)} card(s) but {len(answers)} hidden answer(s)"
            )
        for label in ("**Why it matters:**", "**Official reference:**"):
            if body.count(label) < len(prompts):
                errors.append(
                    f"{rel}: {len(prompts)} card(s) but only {body.count(label)} "
                    f"occurrence(s) of '{label}'"
                )

    return errors


def check_links_resolve(rel: str, text: str, domain_dir: str) -> list[str]:
    errors = []
    for target in MD_LINK_RE.findall(strip_code_fences(text)):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = os.path.normpath(os.path.join(domain_dir, target.split("?")[0]))
        if not os.path.exists(resolved):
            errors.append(f"{rel}: link '{target}' does not resolve on disk")
    return errors


def check_language(rel: str, text: str) -> list[str]:
    """English everywhere except the French 'Pour les nuls' section."""
    errors: list[str] = []
    span = pour_les_nuls_span(text)
    if span is None:
        errors.append(f"{rel}: lesson has no '## 🧠 Pour les nuls' section")
        outside = text
    else:
        outside = text[: span[0]] + text[span[1]:]

    outside = strip_code_fences(outside)
    # Ignore the standard French disclaimer some banks still carry.
    outside = outside.replace(
        "Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.", ""
    )
    outside = outside.replace("Examen Symfony 8", "")
    hits = sorted(set(m.group(0).lower() for m in FRENCH_MARKERS.finditer(outside)))
    if hits:
        errors.append(
            f"{rel}: French prose outside '🧠 Pour les nuls' (markers: {', '.join(hits[:6])})"
        )
    return errors


def check_topic(domain: str, stem: str) -> tuple[list[str], dict]:
    errors: list[str] = []
    d = os.path.join(DOCS, domain)
    files = {
        "lesson": os.path.join(d, f"{stem}.md"),
        "exercises": os.path.join(d, f"{stem}-exercises.md"),
        "exam": os.path.join(d, f"{stem}-exam.md"),
        "flashcards": os.path.join(d, f"{stem}-flashcards.md"),
    }

    for kind, path in files.items():
        rel = os.path.relpath(path, ROOT)
        if not os.path.isfile(path):
            errors.append(f"{rel}: missing — a migrated topic needs all four files")
            continue
        if os.path.getsize(path) == 0:
            errors.append(f"{rel}: empty file")

    if errors:
        return errors, {}

    texts = {k: read(p) for k, p in files.items()}
    lesson_rel = os.path.relpath(files["lesson"], ROOT)

    # 1. Questions must have left the lesson.
    if CERT_Q_RE.search(texts["lesson"]):
        errors.append(
            f"{lesson_rel}: still has a '## Certification questions' section — "
            f"migrate it to {stem}-exam.md"
        )

    # 2. Hidden answers / explanations / references.
    for kind in ("exam", "exercises", "flashcards"):
        errors += check_collapsed_answers(
            os.path.relpath(files[kind], ROOT), texts[kind], kind
        )

    # 3. Journey links, both directions.
    wants = {
        "lesson": [f"{stem}-exercises.md", f"{stem}-exam.md", f"{stem}-flashcards.md"],
        "exercises": [f"{stem}.md", f"{stem}-exam.md"],
        "exam": [f"{stem}.md", f"{stem}-exercises.md", f"{stem}-flashcards.md"],
        "flashcards": [f"{stem}.md", f"{stem}-exam.md"],
    }
    for kind, targets in wants.items():
        rel = os.path.relpath(files[kind], ROOT)
        for t in targets:
            if f"({t})" not in texts[kind]:
                errors.append(f"{rel}: missing journey link to '{t}'")

    # 4. Cross-cutting content rules.
    for kind, path in files.items():
        rel = os.path.relpath(path, ROOT)
        t = texts[kind]
        if DOC_CURRENT_RE.search(t):
            errors.append(f"{rel}: contains a 'symfony.com/doc/current' reference")
        stripped = strip_code_fences(t)
        if PLACEHOLDER_RE.search(stripped):
            errors.append(f"{rel}: contains a TODO/FIXME/XXX/TBD marker")
        errors += check_links_resolve(rel, t, d)

    errors += check_language(lesson_rel, texts["lesson"])

    stats = {
        "questions": len(re.findall(r'(?m)^\?\?\?\s+question\s+"', texts["exam"])),
        "exercises": len(re.findall(r"(?m)^##\s+Exercise\s+\d+", texts["exercises"])),
        "cards": len(re.findall(r'(?m)^\?\?\?\s+question\s+"', texts["flashcards"])),
    }
    return errors, stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--domain", help="only check this domain directory")
    args = ap.parse_args()

    started = find_topics()
    if args.domain:
        started = {k: v for k, v in started.items() if k == args.domain}

    if not started:
        print("check_topic_journey: no migrated topics found — nothing to check.")
        return 0

    all_errors: list[str] = []
    total = 0
    for domain, stems in started.items():
        for stem in stems:
            errs, stats = check_topic(domain, stem)
            total += 1
            if errs:
                all_errors += errs
            else:
                print(f"  OK  {domain}/{stem}  "
                      f"({stats['questions']} questions, {stats['exercises']} exercises, "
                      f"{stats['cards']} cards)")

    if all_errors:
        print(f"\ncheck_topic_journey: FAIL — {len(all_errors)} violation(s) "
              f"across {total} migrated topic(s)\n", file=sys.stderr)
        for e in all_errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"\ncheck_topic_journey: OK — {total} migrated topic(s), 0 violation(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

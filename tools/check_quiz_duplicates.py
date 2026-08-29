#!/usr/bin/env python3
"""Near-duplicate question detector (P1-03) across the entire quiz bank.

This is the automatable part of the "no duplicate questions" audit item the
mission names — a full read of all 1,292 questions for meaning-level
duplication is a human task (see specs/QuizAuditReport.md); this script
finds *candidate* pairs via token-overlap similarity so a human reviewer
doesn't have to start from a blank page.

Method: normalize each question's stem (lowercase, strip punctuation,
tokenize on whitespace), compute the Jaccard similarity of the token sets
for every pair of questions, and report pairs above a threshold. This is a
lexical-overlap signal, not semantic understanding — it will miss two
differently-worded questions testing the same fact, and it may flag two
questions that share a lot of common technical vocabulary (e.g. "Which
kernel event fires first?" vs "Which kernel event fires last?") as
candidates even though they are legitimately different questions. Every
reported pair needs a human read before being called a real duplicate.

Run: python tools/check_quiz_duplicates.py [--threshold 0.75]
"""
from __future__ import annotations
import argparse, glob, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORD_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "the", "a", "an", "is", "are", "of", "to", "in", "on", "for", "and", "or",
    "which", "what", "how", "does", "do", "you", "your", "when", "this",
    "that", "with", "true", "false", "not", "it", "be", "can", "will",
}


def tokenize(text: str) -> frozenset[str]:
    words = WORD_RE.findall(text.lower())
    return frozenset(w for w in words if w not in STOPWORDS and len(w) > 2)


def load_all_questions() -> list[tuple[str, str, str]]:
    """Return [(file, id_or_index, question_text), ...]."""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "quiz", "*.yml"))):
        rel = os.path.relpath(f, ROOT)
        try:
            data = yaml.safe_load(open(f, encoding="utf-8")) or {}
        except Exception as e:
            # P3: name the offending file rather than a bare traceback.
            raise RuntimeError(f"check_quiz_duplicates: failed to parse {rel}: {e}") from e
        for cat in data.get("categories", []):
            for i, q in enumerate(cat.get("questions", [])):
                qid = q.get("id", f"#{i}")
                text = (q.get("question") or "").strip()
                if text:
                    out.append((rel, qid, text))
    return out


def jaccard(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.75)
    args = ap.parse_args()

    questions = load_all_questions()
    tokens = [tokenize(t) for _, _, t in questions]
    n = len(questions)
    pairs = []
    for i in range(n):
        if not tokens[i]:
            continue
        for j in range(i + 1, n):
            if not tokens[j]:
                continue
            # cheap pre-filter: skip pairs whose token-set sizes differ too
            # much to possibly reach the threshold
            si, sj = len(tokens[i]), len(tokens[j])
            if si == 0 or sj == 0:
                continue
            if min(si, sj) / max(si, sj) < args.threshold:
                continue
            sim = jaccard(tokens[i], tokens[j])
            if sim >= args.threshold:
                pairs.append((sim, questions[i], questions[j]))

    pairs.sort(key=lambda p: -p[0])
    print(f"checked {n} questions, {n * (n - 1) // 2} pairs, "
          f"threshold={args.threshold}: {len(pairs)} candidate near-duplicate pair(s)")
    for sim, (f1, id1, t1), (f2, id2, t2) in pairs[:200]:
        print(f"  {sim:.2f}  {f1}:{id1} <-> {f2}:{id2}")
        print(f"        A: {t1[:90]}")
        print(f"        B: {t2[:90]}")
    if len(pairs) > 200:
        print(f"  ... and {len(pairs) - 200} more (see full output if regenerating a report)")
    print("\nEvery pair above is a CANDIDATE only (lexical overlap, not semantic "
          "understanding) - a human must read each pair before treating it as a "
          "real duplicate. This script does not fail CI (informational only).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

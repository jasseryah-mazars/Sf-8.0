# Certification Domains — Lot 1 Final Audit

_End-of-lot verification for `PHP & Web Security`. Branch `master`. Every number below was
counted from the files by a script, not asserted from memory; the commands are given so the
count can be reproduced rather than trusted._

## 1. Verdict

**Lot 1 is complete: 13 topics × 4 files = 52 files.** The full check suite is green and
`mkdocs build --strict` exits 0.

Two things are deliberately **not** claimed:

- Nothing here says the site is 100% anything. This lot covers **13 of 169** topics. The
  other 156 are untouched and named as such in the plan.
- No syllabus-*wording* claim is upgraded to "verified". `certification.symfony.com` has no
  public git mirror and is blocked by this environment's egress proxy, so the existing
  "tracks, but is not itself, the official syllabus" banner in
  `specs/OfficialSyllabusBaseline.md` stands unchanged.

## 2. Counts

| Measure | Value |
|---|---|
| Topics restructured | **13 / 13** |
| Files (lesson + exercises + exam + flashcards) | **52** |
| Exam questions | **292** |
| — migrated out of lessons | 55 (none lost) |
| — newly written | 237 |
| Guided exercises | **91** (7 per topic) |
| Flashcards | **421** |
| Lessons at Expert depth | **13 / 13** |
| Diagrams parsing and rendering repo-wide | **443** |

Reproduce:

```bash
python3 tools/check_topic_journey.py          # per-topic counts + the four-file contract
python3 tools/validate_mermaid.py             # every diagram, real engine, real browser
mkdocs build --strict
```

## 3. Question conservation

The mission's hard rule was that no existing question may be lost. 55 questions lived under
`## Certification questions` in the 13 lessons; all 13 lessons now have no such section.

Conservation was checked **concept by concept**, not by count alone: before each topic was
touched, its original questions were extracted from `git show HEAD:<file>` into a scratch
snapshot, and each concept was then located in the finished exam file. This mattered — in
batch 1 two agents removed the lesson section before writing the exam file, and 9 questions
existed only in git history for a while. `tools/check_topic_journey.py` is what made that
state visible instead of silent, and the agent brief now says: **write the exam file first.**

## 4. The four-file contract, enforced mechanically

`tools/check_topic_journey.py` is blocking in CI and asserts, for all 13 topics:

- all four files present and non-empty;
- no lesson retains `## Certification questions`;
- every exam answer, exercise hint and exercise solution inside a collapsed `???` block —
  nothing visible before a click;
- an explanation **and** an `**Official reference:**` after every answer;
- journey links resolving in both directions, on disk;
- no `doc/current` anywhere;
- French confined to `## 🧠 Pour les nuls`;
- no TODO or placeholder.

## 5. Verification of sources

The rendered documentation sites are egress-blocked here. Four of the five mandated
authorities publish their source as git, and that is where every claim was verified:

| Authority | Rendered site | Verified at |
|---|---|---|
| Symfony 8.0 documentation | `symfony.com/doc/8.0/` ❌ | `symfony-docs@8.0` `.rst` ✅ |
| Symfony 8.0 source | blocked | `symfony/symfony@8.0` ✅ |
| PHP manual | `www.php.net` ❌ | `php/doc-en@master` DocBook ✅ |
| Twig 3.x | `twig.symfony.com` ❌ | `twigphp/Twig@3.x/doc` ✅ |
| Official syllabus | `certification.symfony.com` ❌ | **no git source — unverifiable** |

`symfony-docs@8.0` was confirmed genuinely version-pinned (its `controller.rst` differs from
`7.4`), so it is the text that renders at `symfony.com/doc/8.0/`.

## 6. Known gaps, stated plainly

**Three French pages still show "Syntax error in text" to a reader.**
`web-security.fr.md:146`, `error-handling.fr.md:142`, `interpolation.fr.md:168`. All three
are pre-existing, all three have English twins that are now fixed, and each is a one-line
change. They are in a self-expiring quarantine in `tools/validate_mermaid.py`: printed on
every run with the exact fix, non-blocking, and an entry that stops matching a broken diagram
**fails** the check, so the list can only shrink. The reason they are not simply fixed is the
mission's own instruction not to modify `.fr.md`.

**21 cited documentation URLs do not resolve, across 14 domains outside this lot.** Sixteen
are `symfony.com/doc/8.0/` pages that moved (`components/cache` → `cache`, and similar).
Every affected English page has a French sidecar carrying the identical dead link, so fixing
only the English half would leave French readers on a 404 and the repo internally
inconsistent. The full list with four confirmed relocations is in
`specs/CertificationDomainsEnhancementLog.md`.

**The French sidecars of all 13 topics are now stale.** The English lessons were rewritten
and the French ones were not, by instruction. `fallback_to_default: true` means French
readers keep the old French page for lessons, and fall back to English for the 39 new
activity files — the same behaviour `docs/exams/` has had all along.

## 7. Defects found and fixed along the way

Each was pre-existing and surfaced by tooling written for this lot:

| Defect | Where | Status |
|---|---|---|
| `;` read as a statement separator, breaking a `sequenceDiagram` | `web-security.md:143` | fixed |
| `[\ErrorException]` — `[\ … \]` is a shape delimiter | `miscellaneous/error-handling.md:135` | fixed |
| `\"` is not a mermaid escape; `#` opens an entity code | `twig/interpolation.md:127` | fixed |
| `blob/8.0/<directory>` — GitHub 404s it; needs `tree/` | `extensions.md` ×2, `web-security.md` ×2 | fixed |
| Interfaces table said properties were impossible; 8.4 allows them | `interfaces.md` | fixed |
| Regeneration silently deleted 70 hand-written sections | 4 generators | fixed |
| Revision sheets treated activity files as chapters | `gen_revision_sheets.py` | fixed |
| Link checks read inline PHP as markdown links | 2 checkers | fixed |
| `final_audit` would report a false regression after the split | `final_audit.py` | fixed |

Two of these are worth remembering as method rather than as bugs. `check_mermaid_render.py`
initially failed **every** page, and the checker was wrong, not the site: Material renders
into a closed shadow root that `querySelectorAll` cannot see. And the obvious spelling of the
block-preservation fix, `open(p, "w").write(carry_over(p, …))`, defeats itself — Python
truncates the file before the read. A check that fails everything, and a fix that changes
nothing, are both usually about the tool.

## 8. What remains

- **156 topics in 14 domains** still have the old single-file shape. The plan lists them.
- The three quarantined French diagrams and the 21 dead citations, both blocked only by the
  `.fr.md` instruction.
- `tools/check_doc_refs_resolve.py` is not yet gated in CI, for the same reason.

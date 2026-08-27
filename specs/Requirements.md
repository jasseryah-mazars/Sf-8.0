# Requirements

Formal requirements for the Symfony 8 Certification Prep platform. Each has a
stable ID. **Functional** requirements (`FR-*`) describe *what the platform does*;
**non-functional** requirements (`NFR-*`) are traced to
[QualityRequirements.md](QualityRequirements.md) so quality lives in one place and
is only *referenced* here.

Verification legend: **Build** = enforced by `mkdocs build --strict` / CI ·
**Matrix** = [TraceabilityMatrix.md](TraceabilityMatrix.md) · **Review** =
[ReviewChecklist.md](ReviewChecklist.md) / [DefinitionOfDone.md](DefinitionOfDone.md).

## Functional requirements

### Content — coverage

| ID | Requirement | Verify |
|---|---|---|
| FR-1 | Cover 100% of the official Symfony 8 syllabus across the 14 topic areas. | Matrix |
| FR-2 | Provide exactly one micro-chapter per syllabus sub-topic listed in the Matrix. | Matrix |
| FR-3 | Each topic area has an `index.md` landing page restating prerequisites, level, difficulty, dependencies, revision priority, and a linked chapter checklist. | Review |
| FR-4 | Content targets Symfony 8.0 / PHP 8.4+ / Twig 3.x only; no deprecated or removed APIs appear as taught content. | Review |
| FR-5 | Excluded topics (UX, AI, Doctrine, Monolog, AssetMapper, Encore, third-party bundles/bridges) are never taught; mentioned only to mark them out of scope. | Review |

### Content — per-chapter anatomy

| ID | Requirement | Verify |
|---|---|---|
| FR-6 | Every chapter follows [`CHAPTER_TEMPLATE.md`](../docs/_meta/CHAPTER_TEMPLATE.md) section order. See [ContentStructure.md](ContentStructure.md). | Review |
| FR-7 | Every chapter states measurable learning objectives with syllabus mapping, level, time estimate, and prerequisites. | Review |
| FR-8 | Every chapter includes a **Deep Dive** naming real FQCNs, execution flow/lifecycle, extension points, and trade-offs. | Review |
| FR-9 | Every chapter with a flow/lifecycle/hierarchy includes at least one Mermaid diagram. | Review |
| FR-10 | Every code snippet compiles (valid `<?php`, `declare(strict_types=1)`, real imports/types) and is Symfony 8 / PHP 8.4. | Review |
| FR-11 | Every chapter includes: best-practices/anti-patterns table, when-(not)-to-use, certification traps, common mistakes, exercises + hidden solutions, inline certification questions, key takeaways, last-minute revision, and references. | Review |
| FR-12 | Official-doc references use `symfony.com/doc/8.0`; source references pin `github.com/symfony/symfony/blob/8.0`. | Build, Review |

### Navigation & information architecture

| ID | Requirement | Verify |
|---|---|---|
| FR-13 | Every content page is reachable from `mkdocs.yml` `nav:`; no orphan pages. | Build |
| FR-14 | Any chapter is reachable in ≤2 taps via tabbed navigation plus client-side search. | Review |
| FR-15 | Cross-references between chapters use **relative** links that resolve in both the built site and on GitHub. | Build |
| FR-16 | The site provides an Exam Guide section, a learner-facing Roadmap, and a Revision Hub, all wired into the nav. | Build |

### Exam Guide & Revision Hub

| ID | Requirement | Verify |
|---|---|---|
| FR-17 | The Exam Guide documents the exam format (75 questions / 90 min; single, multiple, true/false), tooling, and Advanced vs Expert positioning. | Review |
| FR-18 | The Roadmap presents the optimized study order (not syllabus order) with a dependency graph and per-stage metadata. | Review |
| FR-19 | The Revision Hub provides a master cheat sheet, a cross-area trap index, memory aids, and quiz guidance. | Review |

### Quiz bank

| ID | Requirement | Verify |
|---|---|---|
| FR-20 | Provide a machine-readable quiz bank under `quiz/`, one YAML file per topic area, [certificationy-cli](https://github.com/certificationy/certificationy-cli)-compatible. | Review |
| FR-21 | Each chapter contributes 3–6 questions; every question has ≥2 options, marked correct answer(s), an `explanation`, and a `documentation` URL. | Review |
| FR-22 | Quiz stems and options contain no deprecated APIs and are Symfony 8 / PHP 8.4 accurate. | Review |
| FR-23 | Questions are educational, not leaked/brain-dumped exam items. | Review |

### Build, CI & deployment

| ID | Requirement | Verify |
|---|---|---|
| FR-24 | `mkdocs build --strict` succeeds with zero warnings (no broken links, no missing nav targets, no orphans). | Build |
| FR-25 | CI (GitHub Actions) builds strictly on every push/PR and deploys the site to GitHub Pages from the default branch only. | Build |
| FR-26 | The build toolchain is pinned in `requirements.txt` for reproducibility. | Build |
| FR-27 | Rendering is correct on a narrow (mobile) viewport; Material features (tabs, search, mermaid, admonitions) work. | Review |

### Licensing & attribution

| ID | Requirement | Verify |
|---|---|---|
| FR-28 | The project is MIT-licensed (`LICENSE` present). | Review |
| FR-29 | Upstream attribution to the ThomasBerends 7.0 list is preserved (README + [MigrationPlan.md](MigrationPlan.md)). | Review |
| FR-30 | A Symfony trademark disclaimer is present (site copyright + README). | Review |

## Non-functional requirements

Each maps to a Quality Requirement; the normative statement lives there.

| ID | Requirement | Traces to |
|---|---|---|
| NFR-1 | Technical correctness for Symfony 8.0 / PHP 8.4; claims backed by docs/source. | [Q1](QualityRequirements.md) |
| NFR-2 | Expert-level depth: internals, lifecycle, extension points, trade-offs. | [Q2](QualityRequirements.md) |
| NFR-3 | One template, one voice, uniform terminology and conventions. | [Q3](QualityRequirements.md) |
| NFR-4 | 100% syllabus completeness with full per-chapter anatomy. | [Q4](QualityRequirements.md) |
| NFR-5 | Mobile-first readability: micro-chapters (150–450 lines), narrow tables, small diagrams. | [Q5](QualityRequirements.md) |
| NFR-6 | Maintainability: small decoupled files, `doc/8.0` + `8.0` source pins, clear contribution path. | [Q6](QualityRequirements.md), [FutureMaintenance.md](FutureMaintenance.md) |
| NFR-7 | Buildability: strict green build, no broken links or orphans. | [Q7](QualityRequirements.md) |
| NFR-8 | Learnability: content ordered by the optimized Roadmap. | [Q8](QualityRequirements.md) |
| NFR-9 | Clear, concise, progressive, precise English; no filler or duplication. | [Q9](QualityRequirements.md) |
| NFR-10 | Legal/scope: MIT, attribution, trademark disclaimer, excluded topics absent. | [Q10](QualityRequirements.md) |

## Traceability

Every `FR-*` is satisfied by shipped chapters/tooling tracked in the
[Traceability Matrix](TraceabilityMatrix.md); every `NFR-*` is verified per chapter
via the [Review Checklist](ReviewChecklist.md) and globally by CI. The platform is
**Done** only when all requirements verify green — see
[DefinitionOfDone.md](DefinitionOfDone.md).

## Related specs

[Specification](Specification.md) · [Architecture](Architecture.md) ·
[QualityRequirements](QualityRequirements.md) · [Roadmap](Roadmap.md) ·
[TraceabilityMatrix](TraceabilityMatrix.md) · [DefinitionOfDone](DefinitionOfDone.md).

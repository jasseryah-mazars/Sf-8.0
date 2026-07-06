# Authoring Conventions

Shared rules so every chapter reads as one voice. Read this before writing.

## Versions & scope (non-negotiable)

- **Symfony 8.0**, **PHP 8.4+**, **Twig 3.x**. Never show deprecated APIs.
- Doc links use `https://symfony.com/doc/current/...` (tracks the latest stable,
  which is 8.x). Source links pin the branch: `.../blob/8.0/...`.
- **Excluded** — never author content for: Symfony UX, Symfony AI, Doctrine,
  Monolog, AssetMapper, Webpack Encore, third-party bundles/bridges, or any
  component not in the official syllabus. Mention them only to say "out of scope"
  when a learner would otherwise expect them.

## PHP code style

- Start standalone files with `<?php` then `declare(strict_types=1);`.
- Constructor property promotion, `readonly` where appropriate, typed properties,
  first-class callable syntax, enums, named arguments where they aid clarity.
- Attributes over annotations/XML. Prefer `#[Route]`, `#[AsCommand]`,
  `#[AsEventListener]`, `#[Autowire]`, `#[When]`, etc.
- Realistic FQCNs and `use` statements. Code must compile — no `// ...` inside an
  expression that would break parsing.

## Symfony config style

- YAML lives under `config/`. Show the real file path in a comment on line 1.
- Prefer attributes for routing/DI; show YAML as the alternative. XML only when
  the topic specifically involves it (e.g. some bundle extension examples).

## Markdown & Material features

- One `# H1` per file (the title). Sections use `##`; sub-sections `###`.
- Use admonitions: `!!! abstract` (objectives), `!!! note` (source refs),
  `!!! tip` (cheat sheet), `!!! warning` (common mistakes), `!!! danger`
  (certification traps), `!!! info` (asides). Collapsible: `???` / `???+`.
- Code tabs: `=== "PHP Attributes"` / `=== "YAML"` / `=== "Console"`.
- Console blocks use the ```console fence with a leading `$`.
- Keep tables narrow (2–4 columns) — they must render on a phone.

## Diagrams (Mermaid)

- Use fenced ```mermaid blocks (rendered by Material via superfences).
- Prefer `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`.
- Keep them small and legible on mobile (≤ ~12 nodes). Label edges.
- At least one diagram per chapter when there is a flow, lifecycle, or hierarchy.

## Links & cross-references

- Relative links between chapters (`../security/voters.md`) so they work in the
  built site and on GitHub.
- Every major concept links to official docs. Add a Symfony **source** link in a
  `!!! note "Source reference"` when explaining internals.
- End each chapter with a `Related:` line of 2–4 cross-links.

## Tone

- Progressive: assume a competent PHP dev, teach up to Expert. Explain *why* and
  *how internally*, never only *how*. No filler, no duplication — cross-link
  instead of repeating.

## Quiz contributions

- For each chapter, add 3–6 questions to the matching `quiz/<area>.yml`.
- certificationy format (see `quiz/README.md`). Every question has an
  `explanation` and a `documentation` link.

## Definition of Done

A chapter passes only if it satisfies `specs/DefinitionOfDone.md` and the
`specs/ReviewChecklist.md`. `mkdocs build --strict` must succeed.

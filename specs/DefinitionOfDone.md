# Definition of Done

A unit of work (chapter, quiz file, or spec) is **Done** only when every
applicable item below is true. This is the gate referenced by every task.

## Every chapter

- [ ] Follows [`docs/_meta/CHAPTER_TEMPLATE.md`](../docs/_meta/CHAPTER_TEMPLATE.md)
      section order and [`CONVENTIONS.md`](../docs/_meta/CONVENTIONS.md).
- [ ] **Learning objectives** stated (measurable) with syllabus mapping, level,
      time estimate, prerequisites.
- [ ] **Theory** section — correct, progressive, no filler.
- [ ] **Deep dive** — explains *why* + *how internally*: named classes/interfaces
      (FQCN), execution flow/lifecycle, extension points, trade-offs,
      performance/memory, security where relevant.
- [ ] At least **one Mermaid diagram** when a flow/lifecycle/hierarchy exists.
- [ ] **Code** in the relevant formats (PHP attributes + YAML at minimum; Console;
      XML only if relevant). All snippets **compile** and are **Symfony 8 / PHP 8.4**.
- [ ] **No deprecated APIs**, no legacy syntax.
- [ ] **Best practices & anti-patterns** table.
- [ ] **When (not) to use / alternatives** with decision guidance.
- [ ] **Certification traps** and **common mistakes** sections.
- [ ] **Exercises** with hidden **solutions**.
- [ ] **Certification questions** (inline, collapsible) with explanations + refs.
- [ ] **Key takeaways** + **Last-minute revision** cheat sheet.
- [ ] **`## Official References`** section (mandatory): official Symfony docs
      (`doc/8.0`) for Symfony concepts, **php.net** for PHP concepts, plus
      **source**/RFC links where internals are discussed. A chapter is invalid
      without it.
- [ ] **Related** cross-links (2–4), all resolving.
- [ ] Added to `mkdocs.yml` `nav:`.
- [ ] 3–6 matching questions added to `quiz/<area>.yml`.

## Every quiz file

- [ ] Valid YAML, certificationy-compatible schema (see `quiz/README.md`).
- [ ] Each question has ≥2 options, correct answer(s) marked, an `explanation`,
      and a `documentation` URL.
- [ ] No deprecated APIs in stems or options.

## Every spec

- [ ] Complete, internally consistent, cross-linked, English, no TODOs left.

## Global gates (whole platform)

- [ ] `mkdocs build --strict` passes with **zero** warnings (no broken links,
      no orphan pages, all nav targets exist).
- [ ] [TraceabilityMatrix.md](TraceabilityMatrix.md) shows **100%** syllabus coverage.
- [ ] Excluded topics (UX, AI, Doctrine, Monolog, AssetMapper, Encore, third-party)
      are absent as taught content.
- [ ] Markdown renders correctly on a narrow (mobile) viewport.

# Tasks — Foundation

Bootstrapping tasks that everything else depends on. All complete.

## T-FND-01 — Repository scaffold
- **Description:** MkDocs Material config with full `nav`, `requirements.txt`,
  `.gitignore`, GitHub Actions Pages workflow.
- **Deliverables:** `mkdocs.yml`, `requirements.txt`, `.gitignore`,
  `.github/workflows/deploy.yml`.
- **Acceptance:** `mkdocs build --strict` runs (fails only on missing content pages,
  which the content tasks create). **Complexity:** M.

## T-FND-02 — Repository meta
- **Deliverables:** `README.md`, `CONTRIBUTING.md`, `LICENSE` (upstream
  attribution + trademark disclaimer). **Complexity:** S.

## T-FND-03 — SpecKit documents
- **Deliverables:** the 13 files in `specs/`. **Complexity:** L.

## T-FND-04 — Chapter template & conventions
- **Deliverables:** `docs/_meta/CHAPTER_TEMPLATE.md`,
  `docs/_meta/CONVENTIONS.md`, `docs/_meta/AGENT_BRIEF.md`. **Complexity:** M.

## T-FND-05 — Quiz bank schema
- **Deliverables:** `quiz/README.md` defining the certificationy-compatible
  schema and rules. **Complexity:** S.

## T-FND-06 — Task breakdown
- **Deliverables:** this `tasks/` folder. **Complexity:** M.

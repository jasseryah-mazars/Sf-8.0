# Symfony 8 Expert Certification Prep

> Community preparation resource aligned with the Symfony 8.0 certification syllabus. Coverage is validated through the traceability matrix and automated checks.

[![Build & Deploy Docs](https://github.com/jasseryah-mazars/Sf-8.0/actions/workflows/deploy.yml/badge.svg)](https://github.com/jasseryah-mazars/Sf-8.0/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Live site](https://img.shields.io/badge/docs-live-brightgreen.svg)](https://jasseryah-mazars.github.io/Sf-8.0/)

## 🌐 Live site

**👉 [jasseryah-mazars.github.io/Sf-8.0](https://jasseryah-mazars.github.io/Sf-8.0/)** — the full, searchable platform (works great on mobile).

This repository is an exam-focused learning platform built around the
**[official Symfony Certification syllabus](https://certification.symfony.com/exams/symfony.html)**.
Community preparation resource aligned with the Symfony 8.0 certification
syllabus. Coverage is validated through the traceability matrix and
automated checks — see [`specs/TraceabilityMatrix.md`](specs/TraceabilityMatrix.md)
for the current, honestly-scored status per syllabus item. Chapters include
theory, internal deep dives, Mermaid diagrams, runnable Symfony 8 / PHP 8.4
code, exercises with solutions, certification traps, and last-minute
revision material.

It began as a rewrite of Thomas Berends'
[Symfony Certification Preparation List](https://github.com/ThomasBerends/symfony-certification-preparation-list)
— which was a curated list of links — and was rebuilt into a full, self-contained
study resource.

## 🎯 What makes this different

- **Coverage tracked and validated** — in a [Traceability Matrix](specs/TraceabilityMatrix.md) using a six-level status per syllabus item (absent → structure → partial → technically validated → editorially validated → conforme); no item reaches the top status without a checked official-docs reference and a matching quiz question. Read the matrix's own "What the [N]-subtopic count is, and is not" notes before quoting a coverage percentage — it distinguishes this project's own tracked completeness from an independently-verified match to the live official syllabus page (which this environment cannot always re-fetch — see [`specs/OfficialSyllabusBaseline.md`](specs/OfficialSyllabusBaseline.md)).
- **Deep dives, not summaries** — every concept explains *why* and *how internally*
  (classes, interfaces, lifecycle, extension points, performance).
- **Certification traps & common mistakes** in every chapter.
- **Micro-chapters** — small files, optimized for reading on a phone.
- **Exercises + solutions** and a **practice quiz bank** (YAML,
  [certificationy](https://github.com/certificationy/certificationy-cli)-compatible).
- **Modern code targeted** — PHP 8.4+, Symfony 8, attributes; deprecated APIs are avoided and flagged for removal when found.

## 📖 Read the docs

The content is published as a searchable [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) site,
live at **<https://jasseryah-mazars.github.io/Sf-8.0/>**.

```bash
# Local preview
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve      # http://127.0.0.1:8000
```

Browse the raw Markdown under [`docs/`](docs/) if you prefer.

## 🗺️ Start here

1. **[Exam Guide](docs/exam-guide/index.md)** — format, scoring, Advanced vs Expert.
2. **[Learning Roadmap](docs/roadmap.md)** — the optimized study order (not the syllabus order).
3. Work through the topic areas, then use the **[Revision Hub](docs/revision/index.md)**.

## 🧭 Exam facts (Symfony 8)

| Fact | Value |
|---|---|
| Questions | 75, randomly selected |
| Duration | 90 minutes |
| Question types | Single choice, multiple choice, true/false |
| Levels | **Advanced** and **Expert** (by score) |
| PHP baseline | **PHP 8.4+** (Symfony 8 requirement) |

## 📂 Repository layout

```
docs/            # Learning content (MkDocs docs root), one folder per syllabus topic
quiz/            # Machine-readable YAML question bank (certificationy-compatible)
specs/           # SpecKit planning artifacts (specification, architecture, roadmap, ...)
tasks/           # Granular, independently-executable task definitions
CONTRIBUTING.md  # How to contribute a chapter or question
mkdocs.yml       # Site configuration and navigation
```

## 🚫 Out of scope

Per the syllabus, the following are **not** taught here: Symfony UX, Symfony AI,
Doctrine, Monolog, AssetMapper, Webpack Encore, and third-party bundles/bridges.

Three chapters this repository used to present as in-scope were re-checked
against the mission brief and moved to
[`docs/appendices/`](docs/appendices/out-of-syllabus/index.md) as clearly-marked
supplementary content (Edge Side Includes, the PHPUnit Bridge, the Lock
component) — kept for enrichment, excluded from official coverage stats,
generated exams, and the quiz bank's official question count. The full,
current list of exclusions — including a few additional out-of-scope APIs
inside otherwise in-scope chapters (e.g. third-party Messenger transports,
the Intl component's ICU utility classes) — is in
[`specs/TraceabilityMatrix.md`](specs/TraceabilityMatrix.md)'s "Out-of-scope
/ Additional Learning" section, kept in sync by
[`tools/check_exclusions.py`](tools/check_exclusions.py) in CI.

## 🤝 Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and the
[chapter template](docs/_meta/CHAPTER_TEMPLATE.md).

## 📜 License

[MIT](LICENSE). Symfony is a trademark of Symfony SAS. This is an independent
community project, not affiliated with or endorsed by Symfony SAS.

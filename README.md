# Symfony 8 Expert Certification Prep

> The definitive open-source platform to prepare for the **Symfony 8 Certification** (Advanced & Expert levels).

[![Build & Deploy Docs](https://github.com/jasseryah-mazars/Sf-8.0/actions/workflows/deploy.yml/badge.svg)](https://github.com/jasseryah-mazars/Sf-8.0/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Live site](https://img.shields.io/badge/docs-live-brightgreen.svg)](https://jasseryah-mazars.github.io/Sf-8.0/)

## 🌐 Live site

**👉 [jasseryah-mazars.github.io/Sf-8.0](https://jasseryah-mazars.github.io/Sf-8.0/)** — the full, searchable platform (works great on mobile).

This repository is a complete, exam-focused learning platform built around the
**[official Symfony Certification syllabus](https://certification.symfony.com/exams/symfony.html)**.
Every official topic is covered in depth with theory, internal deep dives,
Mermaid diagrams, runnable Symfony 8 / PHP 8.4 code, exercises with solutions,
certification traps, and last-minute revision material.

It began as a rewrite of Thomas Berends'
[Symfony Certification Preparation List](https://github.com/ThomasBerends/symfony-certification-preparation-list)
— which was a curated list of links — and was rebuilt into a full, self-contained
study resource.

## 🎯 What makes this different

- **100% syllabus coverage** — tracked in a [Traceability Matrix](specs/TraceabilityMatrix.md).
- **Deep dives, not summaries** — every concept explains *why* and *how internally*
  (classes, interfaces, lifecycle, extension points, performance).
- **Certification traps & common mistakes** in every chapter.
- **Micro-chapters** — small files, optimized for reading on a phone.
- **Exercises + solutions** and a **practice quiz bank** (YAML,
  [certificationy](https://github.com/certificationy/certificationy-cli)-compatible).
- **Modern code only** — PHP 8.4+, Symfony 8, attributes, no deprecated APIs.

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

## 🤝 Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and the
[chapter template](docs/_meta/CHAPTER_TEMPLATE.md).

## 📜 License

[MIT](LICENSE). Symfony is a trademark of Symfony SAS. This is an independent
community project, not affiliated with or endorsed by Symfony SAS.

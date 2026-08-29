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
- **Beginner-friendly *and* Expert-deep, in the same chapter** — every pedagogical chapter opens with a **"Pour les nuls"** section (plain-language idea, a real-world analogy, a minimal Symfony example, a memory trick) *before* going into the same Deep Dive/internals content it always had — simplifying the entry point never simplifies the rest of the chapter.
- **Deep dives, not summaries** — every concept explains *why* and *how internally*
  (classes, interfaces, lifecycle, extension points, performance).
- **Certification traps & common mistakes** in every chapter, plus an explicit
  **🎯 Examen Symfony 8** tag on every chapter stating whether it is in scope.
- **Micro-chapters** — small files, optimized for reading on a phone.
- **Exercises + solutions** and a **practice quiz bank** (YAML,
  [certificationy](https://github.com/certificationy/certificationy-cli)-compatible) — every practice question is explicitly labeled
  *"Question d'entraînement inspirée du syllabus"*, never presented as an official exam question.
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

## 🗺️ Start here (recommended path)

1. **[Dashboard](https://jasseryah-mazars.github.io/Sf-8.0/)** — the guided home page: pick a path, or resume where you left off.
2. **[Exam Guide](docs/exam-guide/index.md)** — format, scoring, Advanced vs Expert.
3. **[Learning Roadmap](docs/roadmap.md)** — the optimized study order (not the syllabus order below).
4. Work through the 15 domains in that order — each chapter opens with **Pour les nuls** for a fast first pass, then goes as deep as the certification's Expert tier requires.
5. Practice with the **[Exam Simulator](docs/exam-simulator.md)** (1,292 questions) after each domain.
6. Finish with the **[Revision Hub](docs/revision/index.md)** — cheat sheets, confusions, edge cases, and traps, organized for **quick / normal / Expert / last-week** revision modes (see [`docs/revision/modes.md`](docs/revision/modes.md)).

## 📚 The 15 official domains

Every domain below has its own index chapter, its own quiz file, and — for every pedagogical sub-chapter — a "Pour les nuls" opener plus certification-trap and Expert-depth sections.

| # | Domain | Start here |
|---|---|---|
| 1 | PHP & Web Security | [`docs/php-web-security/`](docs/php-web-security/index.md) |
| 2 | HTTP | [`docs/http/`](docs/http/index.md) |
| 3 | Symfony Architecture | [`docs/architecture/`](docs/architecture/index.md) |
| 4 | Controllers | [`docs/controllers/`](docs/controllers/index.md) |
| 5 | Routing | [`docs/routing/`](docs/routing/index.md) |
| 6 | Templating (Twig) | [`docs/twig/`](docs/twig/index.md) |
| 7 | Forms | [`docs/forms/`](docs/forms/index.md) |
| 8 | Data Validation | [`docs/validation/`](docs/validation/index.md) |
| 9 | Dependency Injection | [`docs/dependency-injection/`](docs/dependency-injection/index.md) |
| 10 | Security | [`docs/security/`](docs/security/index.md) |
| 11 | HTTP Caching | [`docs/http-caching/`](docs/http-caching/index.md) |
| 12 | Console | [`docs/console/`](docs/console/index.md) |
| 13 | Automated Tests | [`docs/testing/`](docs/testing/index.md) |
| 14 | Miscellaneous (Cache, Serializer, Mailer, Process, Clock, PropertyAccess, Runtime…) | [`docs/miscellaneous/`](docs/miscellaneous/index.md) |
| 15 | Messenger | [`docs/messenger/`](docs/messenger/index.md) |

Internationalization & localization is tracked as a sub-topic inside Miscellaneous (see [`docs/miscellaneous/intl.md`](docs/miscellaneous/intl.md)) rather than a 16th top-level nav entry — it is fully covered either way; see the [Traceability Matrix](specs/TraceabilityMatrix.md) for the exact mapping.

## 🧭 Exam facts (Symfony 8)

| Fact | Value |
|---|---|
| Certification targeted | **Symfony 8 Certification** ([official syllabus](https://certification.symfony.com/exams/symfony.html)), Advanced & Expert tiers |
| Questions | 75, randomly selected |
| Duration | 90 minutes |
| Question types | Single choice, multiple choice, true/false |
| Levels | **Advanced** and **Expert** (by score) |
| Symfony baseline | **Symfony 8.0 exclusively** (never 8.1+, which this repo explicitly avoids) |
| PHP baseline | **PHP 8.4+** (Symfony 8 requirement) |

## 🧠 Study method

Each chapter is built to serve three different reading speeds without ever dumbing down the content:

- **First pass (beginner)** — read only the `!!! tip "In a nutshell"` box and the **🧠 Pour les nuls** section: one-sentence idea, a real-world analogy, a minimal Symfony example, a memory trick.
- **Normal pass** — read the full chapter: Theory → Deep Dive (internals, classes, lifecycle) → Configuration & code → Certification traps → Exercises.
- **Expert / last-week pass** — jump straight to the `👑`/`⚠️`/`🧠` callouts (Expert nuances, certification traps, memorization aids) and the **Last-minute revision** cheat sheet at the end of each chapter, or use the dedicated [Revision Hub](docs/revision/index.md) modes.

Every important chapter also states explicitly, in its header, whether the topic is **on the official exam** (`🎯 Examen Symfony 8 : OUI/NON/PARTIEL`) — so you never spend exam-prep time on something the certification doesn't test, and never miss something it does.

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

# Symfony 8 Expert Certification Prep

A free, self-contained study platform for the **Symfony 8 Certification**
(Advanced & Expert). Follow the guided path below and you'll always know
what to open next — no need to understand the site's structure first.

<a class="sf-cta-primary" href="php-web-security/">▶ Start my preparation</a>

<div id="sf-resume"></div>

## 🧠 Pour les nuls

**C'est quoi ce site ?** Un support de préparation complet et gratuit à la certification Symfony 8 — chaque page t'apprend un concept précis, avec des exemples et des questions d'entraînement.

**Pourquoi ça existe ?** Le syllabus officiel liste 15 domaines à connaître, mais ne fournit aucun contenu pédagogique lui-même — ce site comble ce vide avec des cours structurés, testés et vérifiés.

**🏠 Analogie de la vraie vie :** Une auto-école complète plutôt qu'une simple liste de règles du code de la route : ici, chaque règle est expliquée, illustrée, et suivie d'exercices — pas juste énumérée.

**Symfony dans la vraie vie :** Choisis une des trois cartes ci-dessous selon ton niveau (débutant, préparation Advanced, préparation Expert) — le site s'adapte à ton point de départ plutôt que de t'imposer un seul chemin.

**⚠️ Erreur fréquente :** essayer de tout lire dans l'ordre de la barre de navigation (alphabétique) au lieu de suivre le [Roadmap](roadmap.md) — l'ordre alphabétique ignore les prérequis entre domaines.

**🧠 Comment le mémoriser :** "Pas sûr par où commencer ? PHP & Web Security d'abord, puis le Roadmap dans l'ordre."

## Not sure where to start?

!!! tip "One recommendation, not another list"
    **Start with the [PHP & Web Security](php-web-security/index.md) area,
    then follow the [Roadmap](roadmap.md) in order.** If you already know
    Symfony well and just want to check your level first, take a
    **[quick practice round](exam-simulator.md)** — 20 questions, instant
    feedback, no setup.

## Choose your path

<div class="sf-paths">

<a class="sf-path-card" href="php-web-security/">
<strong>🌱 I'm new to Symfony</strong>
<span>Start from the beginning: PHP fundamentals, then the full
recommended order.</span>
</a>

<a class="sf-path-card" href="roadmap/">
<strong>📘 I'm preparing for Advanced</strong>
<span>Follow the complete study roadmap — broad, solid coverage of all
15 areas.</span>
</a>

<a class="sf-path-card" href="tours/">
<strong>🎓 I'm preparing for Expert</strong>
<span>Go straight to internals: Source Tours, Deep Dives, and
certification traps.</span>
</a>

<a class="sf-path-card" href="revision/">
<strong>⏱ I'm revising before the exam</strong>
<span>Cheat sheet, flashcards, traps, and timed mock exams — the
Revision Hub.</span>
</a>

<a class="sf-path-card" href="exam-simulator/">
<strong>🎯 I want to test my level</strong>
<span>Jump into the interactive simulator — Practice or full Exam mode.</span>
</a>

</div>

## Your step-by-step path

<ol class="sf-steps">
<li><strong>Evaluate your level.</strong> Read <a href="exam-guide/levels/">Advanced vs Expert</a> to know what you're aiming for.</li>
<li><strong>Follow the recommended path.</strong> Open the <a href="roadmap/">Roadmap</a> — the study order that avoids using a concept before it's taught.</li>
<li><strong>Study one area.</strong> Start with <a href="php-web-security/">PHP & Web Security</a> — every area follows the same anatomy (theory, deep dive, exercises).</li>
<li><strong>Do the exercises.</strong> Each area has a hands-on lab: <a href="labs/">Labs</a>.</li>
<li><strong>Test your knowledge.</strong> Run a practice round in the <a href="exam-simulator/">Exam Simulator</a>.</li>
<li><strong>Review your weak spots.</strong> The <a href="revision/">Revision Hub</a> picks the right tool for the time you have.</li>
<li><strong>Sit a mock exam.</strong> Full-length, timed: <a href="revision/mock-exam/">Mock Exam</a>.</li>
</ol>

## Certification domains

Every official topic area, in the platform's recommended study order. **Study**
opens the chapter index; **Test** jumps straight into practice questions for
that area only.

!!! tip "What the columns mean"
    **Status** is this project's own automated coverage tracking (see the
    [Traceability Matrix](https://github.com/jasseryah-mazars/Sf-8.0/blob/master/specs/TraceabilityMatrix.md))
    — it is not a claim that every possible exam question is covered.
    **Flashcards / Exam / Sheet** are quick links to that area's revision
    material.

### 🧱 Foundations

No Symfony yet — the language and the protocol everything else builds on.

| # | Area | Status | Study | Test | Flashcards | Exam | Sheet |
|---|---|---|---|---|---|---|---|
| 1 | [PHP & Web Security](php-web-security/index.md) | 9/9 PASS | [Study](php-web-security/index.md) | [Test](exam-simulator.md?area=PHP%20%26%20Web%20Security) | [Cards](revision/flashcards/php-web-security.md) | [Exam](exams/php-web-security.md) | [Sheet](revision/sheets/php-web-security.md) |
| 2 | [HTTP](http/index.md) | 11/11 PASS | [Study](http/index.md) | [Test](exam-simulator.md?area=HTTP) | [Cards](revision/flashcards/http.md) | [Exam](exams/http.md) | [Sheet](revision/sheets/http.md) |

### 🧠 Core Symfony (the mental model)

The kernel and the container — the two machines every other component plugs
into. Highest exam yield; never skip or skim these two.

| # | Area | Status | Study | Test | Flashcards | Exam | Sheet |
|---|---|---|---|---|---|---|---|
| 3 | [Symfony Architecture](architecture/index.md) | 12/17 PASS · 5 TO VERIFY | [Study](architecture/index.md) | [Test](exam-simulator.md?area=Symfony%20Architecture) | [Cards](revision/flashcards/architecture.md) | [Exam](exams/architecture.md) | [Sheet](revision/sheets/architecture.md) |
| 4 | [Dependency Injection](dependency-injection/index.md) | 12/12 PASS | [Study](dependency-injection/index.md) | [Test](exam-simulator.md?area=Dependency%20Injection) | [Cards](revision/flashcards/dependency-injection.md) | [Exam](exams/dependency-injection.md) | [Sheet](revision/sheets/dependency-injection.md) |

### 🧩 Application components (the feature layer & breadth)

Everyday request handling, then the high-weight security block, then breadth.
Each area lists only its **real** prerequisites — several (Security, HTTP
Caching, Console) are technically unlocked earlier than they appear below;
they are sequenced later for exam-weight reasons explained in the
[Roadmap](roadmap.md).

| # | Area | Status | Study | Test | Flashcards | Exam | Sheet |
|---|---|---|---|---|---|---|---|
| 5 | [Controllers](controllers/index.md) | 15/15 PASS | [Study](controllers/index.md) | [Test](exam-simulator.md?area=Controllers) | [Cards](revision/flashcards/controllers.md) | [Exam](exams/controllers.md) | [Sheet](revision/sheets/controllers.md) |
| 6 | [Routing](routing/index.md) | 13/13 PASS | [Study](routing/index.md) | [Test](exam-simulator.md?area=Routing) | [Cards](revision/flashcards/routing.md) | [Exam](exams/routing.md) | [Sheet](revision/sheets/routing.md) |
| 7 | [Templating (Twig)](twig/index.md) | 14/14 PASS | [Study](twig/index.md) | [Test](exam-simulator.md?area=Templating%20%28Twig%29) | [Cards](revision/flashcards/twig.md) | [Exam](exams/twig.md) | [Sheet](revision/sheets/twig.md) |
| 8 | [Data Validation](validation/index.md) | 9/9 PASS | [Study](validation/index.md) | [Test](exam-simulator.md?area=Data%20Validation) | [Cards](revision/flashcards/validation.md) | [Exam](exams/validation.md) | [Sheet](revision/sheets/validation.md) |
| 9 | [Forms](forms/index.md) | 13/13 PASS | [Study](forms/index.md) | [Test](exam-simulator.md?area=Forms) | [Cards](revision/flashcards/forms.md) | [Exam](exams/forms.md) | [Sheet](revision/sheets/forms.md) |
| 10 | [Security](security/index.md) | 13/13 PASS | [Study](security/index.md) | [Test](exam-simulator.md?area=Security) | [Cards](revision/flashcards/security.md) | [Exam](exams/security.md) | [Sheet](revision/sheets/security.md) |
| 11 | [HTTP Caching](http-caching/index.md) | 5/5 PASS | [Study](http-caching/index.md) | [Test](exam-simulator.md?area=HTTP%20Caching) | [Cards](revision/flashcards/http-caching.md) | [Exam](exams/http-caching.md) | [Sheet](revision/sheets/http-caching.md) |
| 12 | [Console](console/index.md) | 9/9 PASS | [Study](console/index.md) | [Test](exam-simulator.md?area=Console) | [Cards](revision/flashcards/console.md) | [Exam](exams/console.md) | [Sheet](revision/sheets/console.md) |
| 13 | [Messenger](messenger/index.md) | 7/7 PASS | [Study](messenger/index.md) | [Test](exam-simulator.md?area=Messenger) | [Cards](revision/flashcards/messenger.md) | [Exam](exams/messenger.md) | [Sheet](revision/sheets/messenger.md) |
| 14 | [Automated Tests](testing/index.md) | 12/12 PASS | [Study](testing/index.md) | [Test](exam-simulator.md?area=Automated%20Tests) | [Cards](revision/flashcards/testing.md) | [Exam](exams/testing.md) | [Sheet](revision/sheets/testing.md) |
| 15 | [Miscellaneous](miscellaneous/index.md) | 15/15 PASS | [Study](miscellaneous/index.md) | [Test](exam-simulator.md?area=Miscellaneous) | [Cards](revision/flashcards/miscellaneous.md) | [Exam](exams/miscellaneous.md) | [Sheet](revision/sheets/miscellaneous.md) |
| — | [Internationalization and localization](miscellaneous/intl.md) | 1/1 PASS | [Study](miscellaneous/intl.md) | [Test](exam-simulator.md?area=Miscellaneous) | — | — | — |

<small>Internationalization is a single sub-topic inside the Miscellaneous
chapter set (no dedicated flashcard/exam file exists for it yet) — its
"Study" link goes straight to that section; the empty cells are honest gaps,
not broken links.</small>

### 🚫 Out of scope (excluded, not taught)

Named here **only** to mark the boundary — none of this is taught or
evaluated as substantive content. Three components exist in the nav as full
chapters *because* the syllabus explicitly names them as excluded and a
candidate should be able to recognize that on sight; each carries its own
"Excluded from Symfony 8 certification" notice.

| Topic | Where it's mentioned |
|---|---|
| Edge Side Includes (ESI) | [Excluded chapter](appendices/out-of-syllabus/esi.md) |
| PHPUnit Bridge | [Excluded chapter](appendices/out-of-syllabus/phpunit-bridge.md) |
| Lock Component | [Excluded chapter](appendices/out-of-syllabus/lock.md) |
| Symfony UX, Symfony AI, Doctrine, Monolog, AssetMapper, Webpack Encore, PHP Polyfills, String/Uid/TypeInfo components, Amazon SQS, third-party Messenger transports | Boundary mentions only (distractors, scope notes) |

## Quick actions

- [Roadmap](roadmap.md) — the full dependency graph and study order.
- [Exam Simulator](exam-simulator.md) — interactive Practice/Exam modes.
- [Chapter Exams](exams/index.md) — fixed per-area question sets.
- [Mock Exams](revision/mock-exam.md) — full-length, timed papers.
- [Revision Hub](revision/index.md) — every last-minute revision tool.
- [Master Cheat Sheet](revision/cheat-sheet.md) — highest-yield facts per area.
- [Top Certification Traps](revision/traps.md) — the subtle distinctions the exam loves.
- [Study Planner](revision/study-planner.md) — pick an 8/4/1-week schedule.
- [Glossary](glossary.md) — one-line definitions linking to the chapter that teaches each term.
- [Official Symfony Certification](https://certification.symfony.com/) — the exam's own site.

## Who it's for

- **The Practitioner** — 2–5 years of Symfony, targeting **Advanced**. You want
  structured coverage and confidence on edge cases.
- **The Expert candidate** — senior, targeting **Expert**. You want internals,
  trade-offs, and trap-spotting.

Both levels are the *same exam*, scored differently — see
[Advanced vs Expert](exam-guide/levels.md).

## Exam facts (Symfony 8)

| Fact | Value |
|---|---|
| Questions | 75, randomly selected |
| Duration | 90 minutes (~72 s/question) |
| Question types | Single choice, multiple choice, true/false |
| Levels | **Advanced** and **Expert** (determined by score) |
| PHP baseline | **PHP 8.4+** (Symfony 8 requirement) |
| Emphasis shift | Messenger **up-weighted**; HTTP Caching **down-weighted** |

## Where to go next

- [Exam Guide](exam-guide/index.md) — format, scoring, Advanced vs Expert, strategy.
- [Roadmap](roadmap.md) — the ordered study path and dependency graph.
- [Revision Hub](revision/index.md) — modes, cheat sheets, flashcards, confusions,
  mock exam, traps, memory aids, quiz.

---

<small>MIT-licensed. Symfony is a trademark of Symfony SAS. This is an independent
community project, not affiliated with or endorsed by Symfony SAS. It began as a
rewrite of the community
[ThomasBerends preparation list](https://github.com/ThomasBerends/symfony-certification-preparation-list)
(a list of links, targeting Symfony 7) and was rebuilt into full teaching content
for Symfony 8. A study resource meant to be used **alongside the official Symfony
documentation** it links to, not as a replacement for it.</small>

## Official References

- [Official Symfony Certification](https://certification.symfony.com/)
- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)

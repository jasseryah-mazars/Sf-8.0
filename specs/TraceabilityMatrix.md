# Traceability Matrix

_Regenerate: `python tools/gen_traceability_matrix.py`. Six-status schema
(P0-04, this run). "Dernière validation" below is the date this file was
last **automatically regenerated** (2026-08-27) — it is a re-check-timestamp for
the automated evidence, not a human editorial review date; nothing in this
column implies a person re-read the chapter on that date._

## What the 175-subtopic count is, and is not

**The `SYLLABUS` list below (175 subtopics, 16 topic areas) is this
repository's own working taxonomy** — originally assembled from the
mission brief text and this repo's pre-existing topic list across prior
sessions, cross-referenced against `certification.symfony.com` and
`symfony.com/doc/8.0/` **when those were reachable in past sessions**, not
independently re-fetched and re-verified against the live syllabus page
in the current run (`certification.symfony.com` and `symfony.com` are
blocked by this environment's network egress proxy — confirmed live via a
fetch attempt, not assumed). **The number 175 is a fact about this file's
own row count, not a proof that the official syllabus itself lists exactly
175 subtopics.** Treat any wording or count mismatch against the live
syllabus page as an open item, not something this matrix has confirmed
either way, until someone with network access re-diffs it — see
`specs/OfficialSyllabusBaseline.md` §1 for the exact source-reachability
table this decision is based on.

## Status legend (six statuses, ordinal — weakest wins)

| Statut | Means |
|---|---|
| `absent` | No Main Chapter mapped, or the file does not exist on disk. |
| `structure` | File exists, non-empty, but missing a worked example, an
  Exercises section, or a Solutions block. |
| `partiel` | Structure complete, but missing a situational/trap/debug quiz
  question, a Certification-traps block, or a Symfony 8.0
  (`blob/8.0`/`tree/8.0`) source reference. |
| `validé techniquement` | Structure + technical evidence complete, but no
  official doc/php.net/RFC reference is present. |
| `validé éditorialement` | The above plus an official reference, but no
  French translation exists yet (this repo is bilingual by design — see
  the schema note in `tools/gen_traceability_matrix.py` for why a missing
  FR file caps the status here rather than at `conforme`). |
| `conforme` | All of the above, **including** a French translation. |

**None of these six statuses — including `conforme` — is a claim that
Symfony's certification board, or any human reviewer, has approved the
chapter.** They are automated-evidence proxies only, each one strictly
narrower than the one before it. A `validate_quiz.py`/`lint_php.py`
green run means the *structure* the tools can see is valid — it does not
mean the 1,292 quiz questions or the PHP snippets are individually
confirmed accurate against Symfony 8.0; see `specs/QuizAuditReport.md`
and `specs/RemediationLog.md` (P1-02/P1-03) for exactly what was and was
not checked.

**Network limitation (standing, this environment):**
`certification.symfony.com`, `symfony.com`, `www.php.net`, and
`www.rfc-editor.org` are blocked by this environment's network egress
proxy (`EGRESS_BLOCKED`, confirmed via live fetch attempts, not
fabricated) — only `github.com` (source code) is reachable. No row below
was re-verified against a live fetch of these sources this run; where a
row's evidence depends on one of them, that is stated in its Anomaly
column instead of silently assumed correct.

## PHP

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| PHP-01 | PHP | PHP API (up to 8.4) | `php-web-security/php-api.md` | 12 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| PHP-02 | PHP | OOP | `php-web-security/oop.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| PHP-03 | PHP | Attributes | `php-web-security/attributes.md` | 2 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | New chapter this lot; French translation exists (attributes.fr.md). |
| PHP-04 | PHP | Interfaces | `php-web-security/interfaces.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| PHP-05 | PHP | Closures | `php-web-security/closures.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| PHP-06 | PHP | Abstract Classes | `php-web-security/abstract-classes.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| PHP-07 | PHP | Exception & Error Handling | `php-web-security/exceptions.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| PHP-08 | PHP | Traits | `php-web-security/traits.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| PHP-09 | PHP | Enums | `php-web-security/enums.md` | 2 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | New chapter this lot, replacing a duplicated subsection in php-api.md (now a cross-reference). |

## HTTP

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| HTTP-01 | HTTP | HTTP Specification (RFC 9110) | `http/rfc-9110.md` | 1 Q | ✓ | ✓ | ✓ | validé éditorialement | 2026-08-27 | New chapter this lot; authored from trained knowledge of RFC 9110 (rfc-editor.org unreachable from this environment this session — text not re-fetched live). No French translation yet. Manque : traduction française absente. |
| HTTP-02 | HTTP | Client/Server interaction | `http/client-server.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | Introductory chapter; does not replace RFC 9110, which is now the anchor reference (see Additional Chapters). |
| HTTP-03 | HTTP | Status codes | `http/status-codes.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| HTTP-04 | HTTP | HTTP request | `http/request.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| HTTP-05 | HTTP | HTTP response | `http/response.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| HTTP-06 | HTTP | HTTP methods | `http/methods.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| HTTP-07 | HTTP | Cookies | `http/cookies.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| HTTP-08 | HTTP | Caching | `http/caching.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| HTTP-09 | HTTP | Content negotiation | `http/content-negotiation.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| HTTP-10 | HTTP | Language detection | `http/language-detection.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| HTTP-11 | HTTP | HttpClient component | `http/httpclient.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Symfony Architecture

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| ARCH-01 | Symfony Architecture | Symfony Flex | `architecture/flex.md` | 8 Q | ✓ | — | — | partiel | 2026-08-27 | Manque : aucune référence source Symfony 8.0 (blob/8.0 ou tree/8.0). |
| ARCH-02 | Symfony Architecture | License | `architecture/license.md` | 5 Q | — | — | — | structure | 2026-08-27 | Manque : aucun exemple travaillé. |
| ARCH-03 | Symfony Architecture | Components | `architecture/components.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-04 | Symfony Architecture | HttpFoundation component | `architecture/components.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone HttpFoundation chapter; mapped to the Components overview plus the Request/Response chapters that are built on it. |
| ARCH-05 | Symfony Architecture | Bridges | `architecture/bridges.md` | 5 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-06 | Symfony Architecture | Code organization | `architecture/code-organization.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-07 | Symfony Architecture | Request handling | `architecture/request-handling.md` | 13 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-08 | Symfony Architecture | Exception handling | `architecture/exception-handling.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-09 | Symfony Architecture | Event dispatcher & kernel events | `architecture/events.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-10 | Symfony Architecture | Official best practices | `architecture/best-practices.md` | 6 Q | ✓ | — | — | partiel | 2026-08-27 | Manque : aucune référence source Symfony 8.0 (blob/8.0 ou tree/8.0). |
| ARCH-11 | Symfony Architecture | Release management | `architecture/release-management.md` | 8 Q | ✓ | — | — | partiel | 2026-08-27 | Manque : aucune référence source Symfony 8.0 (blob/8.0 ou tree/8.0). |
| ARCH-12 | Symfony Architecture | Backward compatibility promise | `architecture/bc-promise.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-13 | Symfony Architecture | Deprecations best practices | `architecture/deprecations.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-14 | Symfony Architecture | Framework overloading | `architecture/overloading.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-15 | Symfony Architecture | Release management & roadmap schedule | `architecture/roadmap-schedule.md` | 6 Q | ✓ | — | — | partiel | 2026-08-27 | Manque : aucune référence source Symfony 8.0 (blob/8.0 ou tree/8.0). |
| ARCH-16 | Symfony Architecture | Interoperability & PSRs | `architecture/psr.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ARCH-17 | Symfony Architecture | Naming conventions | `architecture/naming-conventions.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Controllers

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| CTRL-01 | Controllers | Naming conventions | `controllers/naming-conventions.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-02 | Controllers | AbstractController | `controllers/abstract-controller.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-03 | Controllers | HttpKernel component | `architecture/request-handling.md` | 13 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone HttpKernel chapter; mapped to Request Handling (the kernel's own lifecycle chapter). |
| CTRL-04 | Controllers | FrameworkBundle | `architecture/components.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone FrameworkBundle chapter; mapped to Components → "How the framework composes them" (extension/config-tree/compiler-pass pipeline, real cert question) — re-checked and judged sufficient rather than a true gap. See also Routing → FrameworkBundle (same mapping). |
| CTRL-05 | Controllers | The request | `controllers/request.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-06 | Controllers | The response | `controllers/response.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-07 | Controllers | The cookies | `controllers/cookies.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-08 | Controllers | The session | `controllers/session.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-09 | Controllers | Flash messages | `controllers/flash-messages.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-10 | Controllers | HTTP redirects | `controllers/http-redirects.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-11 | Controllers | Internal redirects | `controllers/internal-redirects.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-12 | Controllers | Generate 404 pages | `controllers/error-pages.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-13 | Controllers | File upload | `controllers/file-upload.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-14 | Controllers | Built-in internal controllers | `controllers/built-in-controllers.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CTRL-15 | Controllers | Argument value resolvers | `controllers/value-resolvers.md` | 14 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Routing

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| ROUT-01 | Routing | Routing component | `routing/configuration.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone "what is the Routing component" chapter; mapped to Configuration, the entry-point chapter. |
| ROUT-02 | Routing | FrameworkBundle | `architecture/components.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | See Controllers → FrameworkBundle; same mapping to Components → "How the framework composes them". |
| ROUT-03 | Routing | Configuration (YAML & attributes) | `routing/configuration.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-04 | Routing | Restrict URL parameters | `routing/requirements.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-05 | Routing | Default values | `routing/defaults.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-06 | Routing | Generate URL parameters | `routing/url-generation.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-07 | Routing | Trigger redirects | `routing/redirects.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-08 | Routing | Special internal routing attributes | `routing/special-attributes.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-09 | Routing | Domain name matching | `routing/host-matching.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-10 | Routing | Conditional request matching | `routing/conditions.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-11 | Routing | HTTP methods matching | `routing/methods.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-12 | Routing | User's locale guessing | `routing/locale.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| ROUT-13 | Routing | Router debugging | `routing/debugging.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Templating (Twig)

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| TWIG-01 | Templating (Twig) | TwigBundle | `twig/controller-rendering.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone TwigBundle chapter; mapped to Controller Rendering, the chapter that actually covers the Twig↔Symfony integration TwigBundle wires up. |
| TWIG-02 | Templating (Twig) | Twig syntax up to 3.22 | `twig/syntax.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | Version ceiling made explicit per mission brief; verify chapter contains no 3.23+-only syntax. |
| TWIG-03 | Templating (Twig) | Auto escaping | `twig/auto-escaping.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-04 | Templating (Twig) | Template inheritance | `twig/inheritance.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-05 | Templating (Twig) | Global variables | `twig/globals.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-06 | Templating (Twig) | Filters and functions | `twig/filters-functions.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-07 | Templating (Twig) | Template includes | `twig/includes.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-08 | Templating (Twig) | Loops and conditions | `twig/loops-conditions.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-09 | Templating (Twig) | URLs generation | `twig/urls.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-10 | Templating (Twig) | Controller rendering | `twig/controller-rendering.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-11 | Templating (Twig) | Translations and pluralization | `twig/translations.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-12 | Templating (Twig) | String interpolation | `twig/interpolation.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-13 | Templating (Twig) | Assets management | `twig/assets.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TWIG-14 | Templating (Twig) | Debugging variables | `twig/debugging.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Forms

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| FORM-01 | Forms | Form component | `forms/creation.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone "what is the Form component" chapter; mapped to Forms Creation, the chapter that introduces the component end-to-end. |
| FORM-02 | Forms | Form options (OptionsResolver) | `forms/types.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | OptionsResolver is taught distributed across 3 chapters (dedicated "OptionsResolver features" tab + certification question in types.md), not a standalone options-resolver.md — judged sufficiently covered; not created per the "only if necessary" rule. |
| FORM-03 | Forms | Forms creation | `forms/creation.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-04 | Forms | Forms handling | `forms/handling.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-05 | Forms | Form types (built-in & custom) | `forms/types.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-06 | Forms | Forms rendering with Twig | `forms/rendering.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-07 | Forms | Forms theming | `forms/theming.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-08 | Forms | CSRF protection | `forms/csrf.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-09 | Forms | Handling file upload | `forms/file-upload.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-10 | Forms | Built-in form types | `forms/built-in-types.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-11 | Forms | Data transformers | `forms/data-transformers.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-12 | Forms | Form events | `forms/events.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| FORM-13 | Forms | Form type extensions | `forms/type-extensions.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Data Validation

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| VAL-01 | Data Validation | Validator component | `validation/object-validation.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone "what is the Validator component" chapter; mapped to Object validation, the entry-point chapter. |
| VAL-02 | Data Validation | PHP object validation | `validation/object-validation.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| VAL-03 | Data Validation | Built-in validation constraints | `validation/built-in-constraints.md` | 14 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| VAL-04 | Data Validation | Validation scopes | `validation/scopes.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| VAL-05 | Data Validation | Validation groups | `validation/groups.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| VAL-06 | Data Validation | Group sequence | `validation/group-sequence.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| VAL-07 | Data Validation | Custom callback validators | `validation/callbacks.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| VAL-08 | Data Validation | Custom constraints | `validation/custom-constraints.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| VAL-09 | Data Validation | Violations builder | `validation/violations-builder.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Dependency Injection

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| DI-01 | Dependency Injection | Dependency Injection component | `dependency-injection/container.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone "what is the DI component" chapter; mapped to the Service Container chapter. |
| DI-02 | Dependency Injection | Service container | `dependency-injection/container.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-03 | Dependency Injection | Built-in services | `dependency-injection/built-in-services.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-04 | Dependency Injection | Configuration parameters | `dependency-injection/parameters.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-05 | Dependency Injection | Services registration (YAML & attributes) | `dependency-injection/registration.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-06 | Dependency Injection | Service decoration | `dependency-injection/decoration.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-07 | Dependency Injection | Tags | `dependency-injection/tags.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-08 | Dependency Injection | Semantic configuration | `dependency-injection/semantic-config.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-09 | Dependency Injection | Factories | `dependency-injection/factories.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-10 | Dependency Injection | Compiler passes | `dependency-injection/compiler-passes.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-11 | Dependency Injection | Services autowiring | `dependency-injection/autowiring.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| DI-12 | Dependency Injection | Service locators | `dependency-injection/service-locators.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Security

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| SEC-01 | Security | Security Core | `security/authentication.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone "Security Core" overview chapter; mapped to Authentication + Authorization, its two pillars. |
| SEC-02 | Security | CSRF | `forms/csrf.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | Taught under Forms (CSRF is implemented via the Security component's CsrfTokenManager but exposed through form protection) — cross-area mapping, not duplicated here. |
| SEC-03 | Security | Authentication | `security/authentication.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-04 | Security | Authorization | `security/authorization.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-05 | Security | Configuration | `security/configuration.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-06 | Security | Providers | `security/providers.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-07 | Security | Firewalls | `security/firewalls.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-08 | Security | Users | `security/users.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-09 | Security | PasswordHasher (password hashers) | `security/password-hashers.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-10 | Security | Roles | `security/roles.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-11 | Security | Access control rules | `security/access-control.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-12 | Security | Authenticators, passports & badges | `security/authenticators.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| SEC-13 | Security | Voters & voting strategies | `security/voters.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## HTTP Caching

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| CACHE-01 | HTTP Caching | Cache types | `http-caching/cache-types.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CACHE-02 | HTTP Caching | Expiration (Expires, Cache-Control) | `http-caching/expiration.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CACHE-03 | HTTP Caching | Validation (ETag, Last-Modified) | `http-caching/validation.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CACHE-04 | HTTP Caching | Client-side caching | `http-caching/client-side.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CACHE-05 | HTTP Caching | Server-side caching | `http-caching/server-side.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Console

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| CONS-01 | Console | Console component | `console/built-in-commands.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone "what is the Console component" chapter; mapped to Built-in Commands, the chapter that introduces the component end-to-end. |
| CONS-02 | Console | Built-in commands | `console/built-in-commands.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CONS-03 | Console | Custom commands | `console/custom-commands.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CONS-04 | Console | Configuration | `console/configuration.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CONS-05 | Console | Options & arguments (incl. PHP attributes) | `console/options-arguments.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | Covers both classic addArgument()/addOption() and the #[Argument]/#[Option] attribute style — merged into one row rather than duplicated, since both live in the same chapter. |
| CONS-06 | Console | Input & Output objects | `console/input-output.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CONS-07 | Console | Built-in helpers | `console/helpers.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CONS-08 | Console | Console events | `console/events.md` | 10 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| CONS-09 | Console | Verbosity levels | `console/verbosity.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Automated Tests

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| TEST-01 | Automated Tests | CssSelector component | `testing/crawler.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | No standalone CssSelector chapter; the Crawler chapter's selector examples cover it — cross-referenced, not duplicated. |
| TEST-02 | Automated Tests | DomCrawler component | `testing/crawler.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TEST-03 | Automated Tests | WebProfilerBundle | `miscellaneous/profiler.md` | 4 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | Web Profiler content lives under Miscellaneous; cross-referenced here for Automated Tests' WebProfilerBundle subtopic rather than duplicated. |
| TEST-04 | Automated Tests | Unit tests with PHPUnit | `testing/unit-tests.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TEST-05 | Automated Tests | Functional tests with PHPUnit | `testing/functional-tests.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TEST-06 | Automated Tests | Client object | `testing/client.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TEST-07 | Automated Tests | Crawler object | `testing/crawler.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TEST-08 | Automated Tests | Profiler object | `testing/profiler.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TEST-09 | Automated Tests | Framework objects access | `testing/framework-objects.md` | 7 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TEST-10 | Automated Tests | Client configuration | `testing/client-configuration.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TEST-11 | Automated Tests | Request/response introspection | `testing/introspection.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| TEST-12 | Automated Tests | Handling legacy deprecated code | `testing/deprecations.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Miscellaneous

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| MISC-01 | Miscellaneous | Event / EventDispatcher component | `architecture/events.md` | 11 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | Covered under Symfony Architecture → Event dispatcher & kernel events; cross-referenced here, not duplicated. |
| MISC-02 | Miscellaneous | PropertyAccess component | `miscellaneous/property-access.md` | 2 Q | ✓ | ✓ | ✓ | validé éditorialement | 2026-08-27 | New chapter (this lot), verified against PropertyAccessor/PropertyAccessorBuilder/ReflectionExtractor source on the 8.0 branch. No French translation yet. Manque : traduction française absente. |
| MISC-03 | Miscellaneous | Web Profiler & Web Debug Toolbar & Data Collectors | `miscellaneous/profiler.md` | 4 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-04 | Miscellaneous | HTTP Caching / Reverse Proxies / Expiration / Validation | `http-caching/cache-types.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | Fully covered under the dedicated HTTP Caching area; mapped to Cache Types (its entry-point chapter) since Miscellaneous also names these concepts, not duplicated. |
| MISC-05 | Miscellaneous | Configuration (Config/DotEnv/ExpressionLanguage) | `miscellaneous/configuration.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-06 | Miscellaneous | Error handling | `miscellaneous/error-handling.md` | 4 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-07 | Miscellaneous | Code debugging | `miscellaneous/debugging.md` | 4 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-08 | Miscellaneous | Deployment best practices | `miscellaneous/deployment.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-09 | Miscellaneous | Cache component | `miscellaneous/cache.md` | 9 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-10 | Miscellaneous | Process component | `miscellaneous/process.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-11 | Miscellaneous | Serializer component | `miscellaneous/serializer.md` | 8 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-12 | Miscellaneous | Mime & Mailer components | `miscellaneous/mailer.md` | 6 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-13 | Miscellaneous | Filesystem & Finder components | `miscellaneous/filesystem-finder.md` | 4 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-14 | Miscellaneous | Runtime component | `miscellaneous/runtime.md` | 5 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |
| MISC-15 | Miscellaneous | Clock component | `miscellaneous/clock.md` | 5 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | — |

## Messenger

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| MSG-01 | Messenger | Messenger component | `messenger/component.md` | 3 Q | ✓ | ✓ | ✓ | validé éditorialement | 2026-08-27 | Split (this lot) from a prior monolithic miscellaneous/messenger.md into docs/messenger/ — one chapter per official subtopic, each with its own full anatomy. Manque : traduction française absente. |
| MSG-02 | Messenger | Messages and handlers | `messenger/messages-handlers.md` | 6 Q | ✓ | ✓ | ✓ | validé éditorialement | 2026-08-27 | Manque : traduction française absente. |
| MSG-03 | Messenger | Middleware | `messenger/middleware.md` | 5 Q | ✓ | ✓ | ✓ | validé éditorialement | 2026-08-27 | Manque : traduction française absente. |
| MSG-04 | Messenger | Transports | `messenger/transports.md` | 5 Q | ✓ | ✓ | ✓ | validé éditorialement | 2026-08-27 | Third-party transports (Doctrine, Redis, Amazon SQS) are out of scope — see Out-of-scope section; the chapter says so explicitly. Manque : traduction française absente. |
| MSG-05 | Messenger | Workers | `messenger/workers.md` | 2 Q | ✓ | ✓ | ✓ | validé éditorialement | 2026-08-27 | Manque : traduction française absente. |
| MSG-06 | Messenger | Retries and failures | `messenger/retries-failures.md` | 5 Q | ✓ | ✓ | ✓ | validé éditorialement | 2026-08-27 | Manque : traduction française absente. |
| MSG-07 | Messenger | Events | `messenger/events.md` | 2 Q | ✓ | ✓ | ✓ | validé éditorialement | 2026-08-27 | Covers 6 worker events (WorkerStarted/MessageReceived/MessageHandled/MessageFailed/Running/Stopped/RateLimited) plus the dispatch-side SendMessageToTransportsEvent, verified against source. Manque : traduction française absente. |

## Internationalization and localization

| ID | Domaine | Sous-sujet | Chapitre | Quiz | Structurel | Technique | Éditorial | Statut | Dernière validation | Anomalie |
|---|---|---|---|---|---|---|---|---|---|---|
| I18N-01 | Internationalization and localization | Internationalization and localization | `miscellaneous/intl.md` | 4 Q | ✓ | ✓ | ✓ | conforme | 2026-08-27 | Chapter also teaches Intl-component ICU utilities (Countries/Languages/Locales/Currencies/Timezones), now explicitly marked excluded from the exam inside the chapter (this lot) — see Out-of-scope section. |

## Out-of-scope / Additional Learning

Content kept in the repository as enrichment but explicitly **not**
part of the official Symfony 8 certification syllabus, and excluded
from official coverage statistics, generated exams, and the quiz bank's
official question count (tagged `out_of_scope: true` where applicable):

| Area | Item | Note |
|---|---|---|
| PHP — additional/depth | Namespaces & Autoloading | php-web-security/namespaces.md — kept as enrichment, not on the official 9-item PHP list. |
| PHP — additional/depth | PHP Extensions | php-web-security/extensions.md — kept as enrichment. |
| PHP — additional/depth | SPL | php-web-security/spl.md — kept as enrichment. |
| PHP — additional/depth | Web Security Fundamentals | php-web-security/web-security.md — kept as enrichment. |
| HTTP Caching | Edge Side Includes (ESI) | http-caching/esi.md — excluded from the syllabus per mission brief; chapter now carries an explicit exclusion notice, its 10 quiz questions are tagged out_of_scope: true. |
| Automated Tests | PHPUnit Bridge | testing/phpunit-bridge.md — excluded per mission brief; chapter now carries an explicit exclusion notice, its 8 quiz questions are tagged out_of_scope: true. |
| Miscellaneous | Lock component | miscellaneous/lock.md — excluded per mission brief; chapter now carries an explicit exclusion notice, its 6 quiz questions are tagged out_of_scope: true. |
| Messenger | Doctrine / Redis / Amazon SQS transports | Third-party Messenger transports — excluded per mission brief; messenger/transports.md says so explicitly. No quiz questions found testing them specifically. |
| Internationalization | Intl component ICU utilities | Countries/Languages/Locales/Currencies/Timezones static lookup classes in miscellaneous/intl.md — excluded from the exam per mission brief; chapter now carries an explicit exclusion notice. No quiz question found testing this API. |
| Ecosystem (never taught) | Symfony UX, Symfony AI, Doctrine, Monolog, AssetMapper, Webpack Encore, third-party bundles/bridges | Out of scope by design since the project's original GapAnalysis.md; mentions found are contextual/comparative, not taught content — not re-audited line-by-line this lot. |

## Coverage summary

_Automated evidence only (see the six-status legend above) — not a
claim of pedagogical completeness, official-syllabus confirmation, or
100% alignment. **175 is this file's own row count, not an
official figure** — see the note above the tables._

| Official Topic | Subtopics | conforme | validé éditorialement | validé techniquement | partiel | structure | absent |
|---|---|---|---|---|---|---|---|
| PHP | 9 | 9 | 0 | 0 | 0 | 0 | 0 |
| HTTP | 11 | 10 | 1 | 0 | 0 | 0 | 0 |
| Symfony Architecture | 17 | 12 | 0 | 0 | 4 | 1 | 0 |
| Controllers | 15 | 15 | 0 | 0 | 0 | 0 | 0 |
| Routing | 13 | 13 | 0 | 0 | 0 | 0 | 0 |
| Templating (Twig) | 14 | 14 | 0 | 0 | 0 | 0 | 0 |
| Forms | 13 | 13 | 0 | 0 | 0 | 0 | 0 |
| Data Validation | 9 | 9 | 0 | 0 | 0 | 0 | 0 |
| Dependency Injection | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| Security | 13 | 13 | 0 | 0 | 0 | 0 | 0 |
| HTTP Caching | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| Console | 9 | 9 | 0 | 0 | 0 | 0 | 0 |
| Automated Tests | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| Miscellaneous | 15 | 14 | 1 | 0 | 0 | 0 | 0 |
| Messenger | 7 | 0 | 7 | 0 | 0 | 0 | 0 |
| Internationalization and localization | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| **Total** | **175** | **161** | **9** | **0** | **4** | **1** | **0** |

**161/175 subtopics reach `conforme`** — the strict bar
(structure + technical evidence + official reference + French
translation). This is expected to be a small number; it is a much
stricter bar than the previous single `PASS` status, by design (P0-04).
`validé techniquement` or better: 170/175.
**Never state 100% or full conformity from this file alone.**

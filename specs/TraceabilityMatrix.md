# Traceability Matrix

_Reconstructed against the mission brief (2026-08-26): official syllabus
realignment, PHP Attributes/Enums, HTTP RFC 9110, missing component rows,
a dedicated Messenger topic, and an explicit Out-of-scope / Additional
Learning section. Regenerate: `python tools/gen_traceability_matrix.py`._

**Status legend:** `PASS` = automated evidence found for every one of:
existing path, non-empty content, a worked example, an Exercises section,
a Solutions block, at least one situational/scenario/trap/debug quiz
question tagged to it, a Certification-traps pitfall block, a Symfony 8.0
(`blob/8.0` or `tree/8.0`) source reference, and an official doc/php.net/RFC reference —
**and** no out-of-scope dependency. `TO VERIFY` = anything short of that;
the Anomaly column names exactly what is missing. **No row is marked PASS
without this checked evidence — a PASS here is not a claim that the
content is pedagogically excellent, only that the required building
blocks are present.**

**Network limitation (this run):** `certification.symfony.com`,
`symfony.com`, `www.php.net`, and `www.rfc-editor.org` were unreachable
from this environment (egress blocked) — only `github.com` (source code)
was reachable. Official Topic/Subtopic wording below is taken from the
mission brief and this repo's pre-existing topic list, not independently
re-fetched from the live syllabus page this session. Treat wording
mismatches against the live page as a TO VERIFY item, not a confirmed
anomaly, until someone with access re-checks it.

**Never state 100% coverage from this file alone** — it reports what
automated checks can confirm, not human pedagogical review, and several
rows are explicit, named gaps (see Status = TO VERIFY rows and their
Anomaly column).

## PHP

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PHP | PHP API (up to 8.4) | `php-web-security/php-api.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| PHP | OOP | `php-web-security/oop.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| PHP | Attributes | `php-web-security/attributes.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | New chapter this lot; French translation exists (attributes.fr.md). |
| PHP | Interfaces | `php-web-security/interfaces.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| PHP | Closures | `php-web-security/closures.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| PHP | Abstract Classes | `php-web-security/abstract-classes.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| PHP | Exception & Error Handling | `php-web-security/exceptions.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| PHP | Traits | `php-web-security/traits.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| PHP | Enums | `php-web-security/enums.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | New chapter this lot, replacing a duplicated subsection in php-api.md (now a cross-reference). |

## HTTP

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HTTP | HTTP Specification (RFC 9110) | `http/rfc-9110.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | New chapter this lot; authored from trained knowledge of RFC 9110 (rfc-editor.org unreachable from this environment this session — text not re-fetched live). No French translation yet. |
| HTTP | Client/Server interaction | `http/client-server.md` | `http/rfc-9110.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Introductory chapter; does not replace RFC 9110, which is now the anchor reference (see Additional Chapters). |
| HTTP | Status codes | `http/status-codes.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP | HTTP request | `http/request.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP | HTTP response | `http/response.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP | HTTP methods | `http/methods.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP | Cookies | `http/cookies.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP | Caching | `http/caching.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP | Content negotiation | `http/content-negotiation.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP | Language detection | `http/language-detection.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP | HttpClient component | `http/httpclient.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Symfony Architecture

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Symfony Architecture | Symfony Flex | `architecture/flex.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | TO VERIFY | Missing: no Symfony 8.0 (blob/8.0 or tree/8.0) source reference. |
| Symfony Architecture | License | `architecture/license.md` | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | TO VERIFY | Missing: no worked example block. |
| Symfony Architecture | Components | `architecture/components.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | HttpFoundation component | `architecture/components.md` | `controllers/request.md`; `controllers/response.md`; `http/request.md`; `http/response.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone HttpFoundation chapter; mapped to the Components overview plus the Request/Response chapters that are built on it. |
| Symfony Architecture | Bridges | `architecture/bridges.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | Code organization | `architecture/code-organization.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | Request handling | `architecture/request-handling.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | Exception handling | `architecture/exception-handling.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | Event dispatcher & kernel events | `architecture/events.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | Official best practices | `architecture/best-practices.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | TO VERIFY | Missing: no Symfony 8.0 (blob/8.0 or tree/8.0) source reference. |
| Symfony Architecture | Release management | `architecture/release-management.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | TO VERIFY | Missing: no Symfony 8.0 (blob/8.0 or tree/8.0) source reference. |
| Symfony Architecture | Backward compatibility promise | `architecture/bc-promise.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | Deprecations best practices | `architecture/deprecations.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | Framework overloading | `architecture/overloading.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | Release management & roadmap schedule | `architecture/roadmap-schedule.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | TO VERIFY | Missing: no Symfony 8.0 (blob/8.0 or tree/8.0) source reference. |
| Symfony Architecture | Interoperability & PSRs | `architecture/psr.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Symfony Architecture | Naming conventions | `architecture/naming-conventions.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Controllers

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Controllers | Naming conventions | `controllers/naming-conventions.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | AbstractController | `controllers/abstract-controller.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | HttpKernel component | `architecture/request-handling.md` | `controllers/built-in-controllers.md`; `controllers/value-resolvers.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone HttpKernel chapter; mapped to Request Handling (the kernel's own lifecycle chapter). |
| Controllers | FrameworkBundle | `architecture/components.md` | `dependency-injection/container.md`; `architecture/code-organization.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone FrameworkBundle chapter; mapped to Components → "How the framework composes them" (extension/config-tree/compiler-pass pipeline, real cert question) — re-checked and judged sufficient rather than a true gap. See also Routing → FrameworkBundle (same mapping). |
| Controllers | The request | `controllers/request.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | The response | `controllers/response.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | The cookies | `controllers/cookies.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | The session | `controllers/session.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | Flash messages | `controllers/flash-messages.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | HTTP redirects | `controllers/http-redirects.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | Internal redirects | `controllers/internal-redirects.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | Generate 404 pages | `controllers/error-pages.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | File upload | `controllers/file-upload.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | Built-in internal controllers | `controllers/built-in-controllers.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Controllers | Argument value resolvers | `controllers/value-resolvers.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Routing

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Routing | Routing component | `routing/configuration.md` | `routing/index.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone "what is the Routing component" chapter; mapped to Configuration, the entry-point chapter. |
| Routing | FrameworkBundle | `architecture/components.md` | `routing/configuration.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | See Controllers → FrameworkBundle; same mapping to Components → "How the framework composes them". |
| Routing | Configuration (YAML & attributes) | `routing/configuration.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | Restrict URL parameters | `routing/requirements.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | Default values | `routing/defaults.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | Generate URL parameters | `routing/url-generation.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | Trigger redirects | `routing/redirects.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | Special internal routing attributes | `routing/special-attributes.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | Domain name matching | `routing/host-matching.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | Conditional request matching | `routing/conditions.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | HTTP methods matching | `routing/methods.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | User's locale guessing | `routing/locale.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Routing | Router debugging | `routing/debugging.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Templating (Twig)

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Templating (Twig) | TwigBundle | `twig/controller-rendering.md` | `twig/index.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone TwigBundle chapter; mapped to Controller Rendering, the chapter that actually covers the Twig↔Symfony integration TwigBundle wires up. |
| Templating (Twig) | Twig syntax up to 3.22 | `twig/syntax.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Version ceiling made explicit per mission brief; verify chapter contains no 3.23+-only syntax. |
| Templating (Twig) | Auto escaping | `twig/auto-escaping.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | Template inheritance | `twig/inheritance.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | Global variables | `twig/globals.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | Filters and functions | `twig/filters-functions.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | Template includes | `twig/includes.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | Loops and conditions | `twig/loops-conditions.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | URLs generation | `twig/urls.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | Controller rendering | `twig/controller-rendering.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | Translations and pluralization | `twig/translations.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | String interpolation | `twig/interpolation.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | Assets management | `twig/assets.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Templating (Twig) | Debugging variables | `twig/debugging.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Forms

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Forms | Form component | `forms/creation.md` | `forms/index.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone "what is the Form component" chapter; mapped to Forms Creation, the chapter that introduces the component end-to-end. |
| Forms | Form options (OptionsResolver) | `forms/types.md` | `forms/creation.md`; `forms/type-extensions.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | OptionsResolver is taught distributed across 3 chapters (dedicated "OptionsResolver features" tab + certification question in types.md), not a standalone options-resolver.md — judged sufficiently covered; not created per the "only if necessary" rule. |
| Forms | Forms creation | `forms/creation.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | Forms handling | `forms/handling.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | Form types (built-in & custom) | `forms/types.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | Forms rendering with Twig | `forms/rendering.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | Forms theming | `forms/theming.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | CSRF protection | `forms/csrf.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | Handling file upload | `forms/file-upload.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | Built-in form types | `forms/built-in-types.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | Data transformers | `forms/data-transformers.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | Form events | `forms/events.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Forms | Form type extensions | `forms/type-extensions.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Data Validation

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Data Validation | Validator component | `validation/object-validation.md` | `validation/index.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone "what is the Validator component" chapter; mapped to Object validation, the entry-point chapter. |
| Data Validation | PHP object validation | `validation/object-validation.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Data Validation | Built-in validation constraints | `validation/built-in-constraints.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Data Validation | Validation scopes | `validation/scopes.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Data Validation | Validation groups | `validation/groups.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Data Validation | Group sequence | `validation/group-sequence.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Data Validation | Custom callback validators | `validation/callbacks.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Data Validation | Custom constraints | `validation/custom-constraints.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Data Validation | Violations builder | `validation/violations-builder.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Dependency Injection

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Dependency Injection | Dependency Injection component | `dependency-injection/container.md` | `dependency-injection/index.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone "what is the DI component" chapter; mapped to the Service Container chapter. |
| Dependency Injection | Service container | `dependency-injection/container.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Built-in services | `dependency-injection/built-in-services.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Configuration parameters | `dependency-injection/parameters.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Services registration (YAML & attributes) | `dependency-injection/registration.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Service decoration | `dependency-injection/decoration.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Tags | `dependency-injection/tags.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Semantic configuration | `dependency-injection/semantic-config.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Factories | `dependency-injection/factories.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Compiler passes | `dependency-injection/compiler-passes.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Services autowiring | `dependency-injection/autowiring.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Dependency Injection | Service locators | `dependency-injection/service-locators.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Security

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Security | Security Core | `security/authentication.md` | `security/authorization.md`; `security/index.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone "Security Core" overview chapter; mapped to Authentication + Authorization, its two pillars. |
| Security | CSRF | `forms/csrf.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Taught under Forms (CSRF is implemented via the Security component's CsrfTokenManager but exposed through form protection) — cross-area mapping, not duplicated here. |
| Security | Authentication | `security/authentication.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | Authorization | `security/authorization.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | Configuration | `security/configuration.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | Providers | `security/providers.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | Firewalls | `security/firewalls.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | Users | `security/users.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | PasswordHasher (password hashers) | `security/password-hashers.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | Roles | `security/roles.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | Access control rules | `security/access-control.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | Authenticators, passports & badges | `security/authenticators.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Security | Voters & voting strategies | `security/voters.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## HTTP Caching

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HTTP Caching | Cache types | `http-caching/cache-types.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP Caching | Expiration (Expires, Cache-Control) | `http-caching/expiration.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP Caching | Validation (ETag, Last-Modified) | `http-caching/validation.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP Caching | Client-side caching | `http-caching/client-side.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| HTTP Caching | Server-side caching | `http-caching/server-side.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Console

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Console | Console component | `console/built-in-commands.md` | `console/index.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone "what is the Console component" chapter; mapped to Built-in Commands, the chapter that introduces the component end-to-end. |
| Console | Built-in commands | `console/built-in-commands.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Console | Custom commands | `console/custom-commands.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Console | Configuration | `console/configuration.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Console | Options & arguments (incl. PHP attributes) | `console/options-arguments.md` | `console/custom-commands.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Covers both classic addArgument()/addOption() and the #[Argument]/#[Option] attribute style — merged into one row rather than duplicated, since both live in the same chapter. |
| Console | Input & Output objects | `console/input-output.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Console | Built-in helpers | `console/helpers.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Console | Console events | `console/events.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Console | Verbosity levels | `console/verbosity.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Automated Tests

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Automated Tests | CssSelector component | `testing/crawler.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | No standalone CssSelector chapter; the Crawler chapter's selector examples cover it — cross-referenced, not duplicated. |
| Automated Tests | DomCrawler component | `testing/crawler.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Automated Tests | WebProfilerBundle | `miscellaneous/profiler.md` | `testing/profiler.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Web Profiler content lives under Miscellaneous; cross-referenced here for Automated Tests' WebProfilerBundle subtopic rather than duplicated. |
| Automated Tests | Unit tests with PHPUnit | `testing/unit-tests.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Automated Tests | Functional tests with PHPUnit | `testing/functional-tests.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Automated Tests | Client object | `testing/client.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Automated Tests | Crawler object | `testing/crawler.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Automated Tests | Profiler object | `testing/profiler.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Automated Tests | Framework objects access | `testing/framework-objects.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Automated Tests | Client configuration | `testing/client-configuration.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Automated Tests | Request/response introspection | `testing/introspection.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Automated Tests | Handling legacy deprecated code | `testing/deprecations.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Miscellaneous

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Miscellaneous | Event / EventDispatcher component | `architecture/events.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Covered under Symfony Architecture → Event dispatcher & kernel events; cross-referenced here, not duplicated. |
| Miscellaneous | PropertyAccess component | `miscellaneous/property-access.md` | `miscellaneous/serializer.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | New chapter (this lot), verified against PropertyAccessor/PropertyAccessorBuilder/ReflectionExtractor source on the 8.0 branch. No French translation yet. |
| Miscellaneous | Web Profiler & Web Debug Toolbar & Data Collectors | `miscellaneous/profiler.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | HTTP Caching / Reverse Proxies / Expiration / Validation | `http-caching/cache-types.md` | `http-caching/index.md` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Fully covered under the dedicated HTTP Caching area; mapped to Cache Types (its entry-point chapter) since Miscellaneous also names these concepts, not duplicated. |
| Miscellaneous | Configuration (Config/DotEnv/ExpressionLanguage) | `miscellaneous/configuration.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Error handling | `miscellaneous/error-handling.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Code debugging | `miscellaneous/debugging.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Deployment best practices | `miscellaneous/deployment.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Cache component | `miscellaneous/cache.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Process component | `miscellaneous/process.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Serializer component | `miscellaneous/serializer.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Mime & Mailer components | `miscellaneous/mailer.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Filesystem & Finder components | `miscellaneous/filesystem-finder.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Runtime component | `miscellaneous/runtime.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |
| Miscellaneous | Clock component | `miscellaneous/clock.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | — |

## Messenger

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Messenger | Messenger component | `miscellaneous/messenger.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Single monolithic chapter covers all 7 Messenger subtopics; mission asks for a docs/messenger/ split with one chapter per subtopic — not done this lot (time budget), flagged for the next one. |
| Messenger | Transports | `miscellaneous/messenger.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | See Messenger component row — same monolithic-chapter caveat. Third-party transports (Doctrine, Redis, Amazon SQS) are out of scope — see Out-of-scope section. |
| Messenger | Messages and handlers | `miscellaneous/messenger.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | See Messenger component row — same monolithic-chapter caveat. |
| Messenger | Workers | `miscellaneous/messenger.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | See Messenger component row — same monolithic-chapter caveat. |
| Messenger | Retries and failures | `miscellaneous/messenger.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | See Messenger component row — same monolithic-chapter caveat. |
| Messenger | Middleware | `miscellaneous/messenger.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | See Messenger component row — same monolithic-chapter caveat. |
| Messenger | Events | `miscellaneous/messenger.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | CORRECTION (this lot): a prior pass wrongly reported this as a gap — the Worker lifecycle section already covers WorkerStartedEvent/WorkerMessageReceivedEvent/WorkerMessageHandledEvent/WorkerMessageFailedEvent/WorkerRunningEvent/WorkerStoppedEvent/WorkerRateLimitedEvent with a real diagram, example listener, and source reference. The one genuinely missing event, SendMessageToTransportsEvent (the dispatch-side event fired by SendMessageMiddleware), was added this lot, verified against source. See also Messenger component row — same monolithic-chapter caveat. |

## Internationalization and localization

| Official Topic | Official Subtopic | Main Chapter | Additional Chapters | Example | Exercise | Solution | Situational Q | Pitfall | Sf 8.0 Ref | Official Ref | Status | Anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Internationalization and localization | Internationalization and localization | `miscellaneous/intl.md` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Chapter also teaches Intl-component ICU utilities (Countries/Languages/Locales/Currencies/Timezones), now explicitly marked excluded from the exam inside the chapter (this lot) — see Out-of-scope section. |

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
| Messenger | Doctrine / Redis / Amazon SQS transports | Third-party Messenger transports — excluded per mission brief. Not currently taught as their own content in miscellaneous/messenger.md (spot-checked); no quiz questions found testing them specifically. |
| Internationalization | Intl component ICU utilities | Countries/Languages/Locales/Currencies/Timezones static lookup classes in miscellaneous/intl.md — excluded from the exam per mission brief; chapter now carries an explicit exclusion notice. No quiz question found testing this API. |
| Ecosystem (never taught) | Symfony UX, Symfony AI, Doctrine, Monolog, AssetMapper, Webpack Encore, third-party bundles/bridges | Out of scope by design since the project's original GapAnalysis.md; mentions found are contextual/comparative, not taught content — not re-audited line-by-line this lot. |

## Coverage summary

_Automated evidence only (see Status legend above) — not a claim of
pedagogical completeness or of 100% syllabus alignment._

| Official Topic | Subtopics | PASS (automated evidence) |
|---|---|---|
| PHP | 9 | 9 |
| HTTP | 11 | 11 |
| Symfony Architecture | 17 | 12 |
| Controllers | 15 | 15 |
| Routing | 13 | 13 |
| Templating (Twig) | 14 | 14 |
| Forms | 13 | 13 |
| Data Validation | 9 | 9 |
| Dependency Injection | 12 | 12 |
| Security | 13 | 13 |
| HTTP Caching | 5 | 5 |
| Console | 9 | 9 |
| Automated Tests | 12 | 12 |
| Miscellaneous | 15 | 15 |
| Messenger | 7 | 7 |
| Internationalization and localization | 1 | 1 |
| **Total** | **175** | **170 (97.1%)** |

**5 of 175 official subtopics are `TO VERIFY`** —
either a genuine content gap (no Main Chapter, or a named missing
building block) or a chapter this run's automated checks could not
fully confirm. See each row's Anomaly column. This count is never to
be reported as "100% done" — several TO VERIFY rows are real,
named gaps, not merely unchecked boxes.

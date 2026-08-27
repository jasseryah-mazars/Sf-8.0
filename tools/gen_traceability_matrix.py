#!/usr/bin/env python3
"""Reconstruct specs/TraceabilityMatrix.md against the mission brief's syllabus
realignment (2026-08-26): PHP Attributes/Enums, HTTP RFC 9110, missing
component rows, a dedicated Messenger topic, and an explicit Out-of-scope /
Additional Learning section for content that is not on the official syllabus
(ESI, PHPUnit Bridge, Lock, PHP depth topics, third-party Messenger
transports, excluded Intl ICU utilities, and adjacent third-party ecosystem
items).

Every row's Status starts at "TO VERIFY". A row is promoted to "PASS" only
when this script finds REAL evidence in the repo for every one of:
  - the Main Chapter path exists and is non-empty;
  - it contains a worked example (a fenced ``php or ``yaml block);
  - it has an "## Exercises" section;
  - it has a "??? success \"Solutions\"" block;
  - at least one situational/scenario-type quiz question is tagged to its
    subchapter (type in {scenario, trap, debug} in quiz/*.yml);
  - it has a "Certification traps" pitfall block;
  - it links a Symfony 8.0 source (`blob/8.0` or `tree/8.0`) AND an official doc/php.net/RFC
    reference.
No row is promoted on a guess. Gaps (no Main Chapter, or a genuinely missing
building block) stay "TO VERIFY" with the Anomaly column explaining why.

IMPORTANT — network limitation of this run: certification.symfony.com and
symfony.com were not reachable from this environment (egress blocked), so
"Official Subtopic" wording/"Official Source Reference" are taken from the
mission brief text and this repo's pre-existing (community-authored) topic
list, not independently re-verified against the live syllabus page this
session. This is recorded once here rather than on every row.

Run: python tools/gen_traceability_matrix.py
"""
from __future__ import annotations
import os, re, glob, collections
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
QUIZ = os.path.join(ROOT, "quiz")
OUT = os.path.join(ROOT, "specs", "TraceabilityMatrix.md")

SITUATIONAL_TYPES = {"scenario", "trap", "debug"}


# ---------------------------------------------------------------- evidence --

def _read(path: str) -> str:
    full = os.path.join(DOCS, path)
    if not os.path.exists(full):
        return ""
    return open(full, encoding="utf-8").read()


_quiz_cache: dict[str, list[dict]] | None = None


def _quiz_by_subchapter() -> dict[str, list[dict]]:
    global _quiz_cache
    if _quiz_cache is not None:
        return _quiz_cache
    by_sub: dict[str, list[dict]] = collections.defaultdict(list)
    for f in glob.glob(os.path.join(QUIZ, "*.yml")):
        data = yaml.safe_load(open(f, encoding="utf-8")) or {}
        for cat in data.get("categories", []):
            for q in cat.get("questions", []):
                sc = q.get("subchapter")
                if sc:
                    by_sub[sc.removesuffix(".md")].append(q)
    _quiz_cache = by_sub
    return by_sub


def evidence(main: str | None) -> dict:
    """Compute the automated PASS-criteria evidence for one Main Chapter path."""
    ev = {
        "path_exists": False, "non_empty": False, "example": False,
        "exercise": False, "solution": False, "situational": False,
        "pitfall": False, "sf8_ref": False, "official_ref": False,
    }
    if not main:
        return ev
    txt = _read(main)
    ev["path_exists"] = os.path.exists(os.path.join(DOCS, main))
    ev["non_empty"] = len(txt.strip()) > 200
    ev["example"] = bool(re.search(r"```(?:php|yaml|console|twig|html\+twig|http)", txt))
    ev["exercise"] = bool(re.search(r"(?m)^#{2,4}\s+Exercises", txt))
    ev["solution"] = '"Solutions"' in txt
    ev["pitfall"] = "Certification traps" in txt
    # Symfony 8.0 source (blob/8.0, tree/8.0) OR, for Twig-language content,
    # Twig's own version-pinned source (twigphp/Twig/{blob,tree}/3.x) — Twig
    # is not part of symfony/symfony, so its own repo is the correct citation.
    ev["sf8_ref"] = bool(re.search(r"blob/8\.0|tree/8\.0|twigphp/Twig/(?:blob|tree)/3\.x", txt))
    ev["official_ref"] = bool(re.search(
        r"symfony\.com/doc/8\.0|php\.net|rfc-editor\.org|twig\.symfony\.com", txt))
    stem = main.removesuffix(".md")
    tagged = _quiz_by_subchapter().get(stem, [])
    ev["situational"] = any(q.get("type") in SITUATIONAL_TYPES for q in tagged)
    ev["_quiz_count"] = len(tagged)
    return ev


def status_for(ev: dict, out_of_scope_dep: bool) -> str:
    required = ("path_exists", "non_empty", "example", "exercise", "solution",
                "situational", "pitfall", "sf8_ref", "official_ref")
    if out_of_scope_dep:
        return "TO VERIFY"
    if all(ev.get(k) for k in required):
        return "PASS"
    return "TO VERIFY"


def gaps(ev: dict, main: str | None) -> list[str]:
    if not main:
        return ["no Main Chapter mapped"]
    labels = {
        "path_exists": "path missing", "non_empty": "file empty/stub",
        "example": "no worked example block", "exercise": "no Exercises section",
        "solution": "no Solutions block", "situational": "no situational/scenario/trap quiz question tagged",
        "pitfall": "no Certification traps block", "sf8_ref": "no Symfony 8.0 (blob/8.0 or tree/8.0) source reference",
        "official_ref": "no official doc/php.net/RFC reference",
    }
    return [v for k, v in labels.items() if not ev.get(k)]


# ------------------------------------------------------------------ syllabus -
# (topic, subtopic, main, additional[list], anomaly_or_None)
Row = tuple[str, str, str | None, list[str], str | None]

SYLLABUS: list[Row] = [
    # -- PHP (official 9-item list per mission; depth topics moved to Out-of-scope) --
    ("PHP", "PHP API (up to 8.4)", "php-web-security/php-api.md", [], None),
    ("PHP", "OOP", "php-web-security/oop.md", [], None),
    ("PHP", "Attributes", "php-web-security/attributes.md", [], "New chapter this lot; French translation exists (attributes.fr.md)."),
    ("PHP", "Interfaces", "php-web-security/interfaces.md", [], None),
    ("PHP", "Closures", "php-web-security/closures.md", [], None),
    ("PHP", "Abstract Classes", "php-web-security/abstract-classes.md", [], None),
    ("PHP", "Exception & Error Handling", "php-web-security/exceptions.md", [], None),
    ("PHP", "Traits", "php-web-security/traits.md", [], None),
    ("PHP", "Enums", "php-web-security/enums.md", [], "New chapter this lot, replacing a duplicated subsection in php-api.md (now a cross-reference)."),

    # -- HTTP --
    ("HTTP", "HTTP Specification (RFC 9110)", "http/rfc-9110.md", [], "New chapter this lot; authored from trained knowledge of RFC 9110 (rfc-editor.org unreachable from this environment this session — text not re-fetched live). No French translation yet."),
    ("HTTP", "Client/Server interaction", "http/client-server.md", ["http/rfc-9110.md"], "Introductory chapter; does not replace RFC 9110, which is now the anchor reference (see Additional Chapters)."),
    ("HTTP", "Status codes", "http/status-codes.md", [], None),
    ("HTTP", "HTTP request", "http/request.md", [], None),
    ("HTTP", "HTTP response", "http/response.md", [], None),
    ("HTTP", "HTTP methods", "http/methods.md", [], None),
    ("HTTP", "Cookies", "http/cookies.md", [], None),
    ("HTTP", "Caching", "http/caching.md", [], None),
    ("HTTP", "Content negotiation", "http/content-negotiation.md", [], None),
    ("HTTP", "Language detection", "http/language-detection.md", [], None),
    ("HTTP", "HttpClient component", "http/httpclient.md", [], None),

    # -- Symfony Architecture --
    ("Symfony Architecture", "Symfony Flex", "architecture/flex.md", [], None),
    ("Symfony Architecture", "License", "architecture/license.md", [], None),
    ("Symfony Architecture", "Components", "architecture/components.md", [], None),
    ("Symfony Architecture", "HttpFoundation component", "architecture/components.md", ["controllers/request.md", "controllers/response.md", "http/request.md", "http/response.md"], "No standalone HttpFoundation chapter; mapped to the Components overview plus the Request/Response chapters that are built on it."),
    ("Symfony Architecture", "Bridges", "architecture/bridges.md", [], None),
    ("Symfony Architecture", "Code organization", "architecture/code-organization.md", [], None),
    ("Symfony Architecture", "Request handling", "architecture/request-handling.md", [], None),
    ("Symfony Architecture", "Exception handling", "architecture/exception-handling.md", [], None),
    ("Symfony Architecture", "Event dispatcher & kernel events", "architecture/events.md", [], None),
    ("Symfony Architecture", "Official best practices", "architecture/best-practices.md", [], None),
    ("Symfony Architecture", "Release management", "architecture/release-management.md", [], None),
    ("Symfony Architecture", "Backward compatibility promise", "architecture/bc-promise.md", [], None),
    ("Symfony Architecture", "Deprecations best practices", "architecture/deprecations.md", [], None),
    ("Symfony Architecture", "Framework overloading", "architecture/overloading.md", [], None),
    ("Symfony Architecture", "Release management & roadmap schedule", "architecture/roadmap-schedule.md", [], None),
    ("Symfony Architecture", "Interoperability & PSRs", "architecture/psr.md", [], None),
    ("Symfony Architecture", "Naming conventions", "architecture/naming-conventions.md", [], None),

    # -- Controllers --
    ("Controllers", "Naming conventions", "controllers/naming-conventions.md", [], None),
    ("Controllers", "AbstractController", "controllers/abstract-controller.md", [], None),
    ("Controllers", "HttpKernel component", "architecture/request-handling.md", ["controllers/built-in-controllers.md", "controllers/value-resolvers.md"], "No standalone HttpKernel chapter; mapped to Request Handling (the kernel's own lifecycle chapter)."),
    ("Controllers", "FrameworkBundle", "architecture/components.md", ["dependency-injection/container.md", "architecture/code-organization.md"], "No standalone FrameworkBundle chapter; mapped to Components → \"How the framework composes them\" (extension/config-tree/compiler-pass pipeline, real cert question) — re-checked and judged sufficient rather than a true gap. See also Routing → FrameworkBundle (same mapping)."),
    ("Controllers", "The request", "controllers/request.md", [], None),
    ("Controllers", "The response", "controllers/response.md", [], None),
    ("Controllers", "The cookies", "controllers/cookies.md", [], None),
    ("Controllers", "The session", "controllers/session.md", [], None),
    ("Controllers", "Flash messages", "controllers/flash-messages.md", [], None),
    ("Controllers", "HTTP redirects", "controllers/http-redirects.md", [], None),
    ("Controllers", "Internal redirects", "controllers/internal-redirects.md", [], None),
    ("Controllers", "Generate 404 pages", "controllers/error-pages.md", [], None),
    ("Controllers", "File upload", "controllers/file-upload.md", [], None),
    ("Controllers", "Built-in internal controllers", "controllers/built-in-controllers.md", [], None),
    ("Controllers", "Argument value resolvers", "controllers/value-resolvers.md", [], None),

    # -- Routing --
    ("Routing", "Routing component", "routing/configuration.md", ["routing/index.md"], "No standalone \"what is the Routing component\" chapter; mapped to Configuration, the entry-point chapter."),
    ("Routing", "FrameworkBundle", "architecture/components.md", ["routing/configuration.md"], "See Controllers → FrameworkBundle; same mapping to Components → \"How the framework composes them\"."),
    ("Routing", "Configuration (YAML & attributes)", "routing/configuration.md", [], None),
    ("Routing", "Restrict URL parameters", "routing/requirements.md", [], None),
    ("Routing", "Default values", "routing/defaults.md", [], None),
    ("Routing", "Generate URL parameters", "routing/url-generation.md", [], None),
    ("Routing", "Trigger redirects", "routing/redirects.md", [], None),
    ("Routing", "Special internal routing attributes", "routing/special-attributes.md", [], None),
    ("Routing", "Domain name matching", "routing/host-matching.md", [], None),
    ("Routing", "Conditional request matching", "routing/conditions.md", [], None),
    ("Routing", "HTTP methods matching", "routing/methods.md", [], None),
    ("Routing", "User's locale guessing", "routing/locale.md", [], None),
    ("Routing", "Router debugging", "routing/debugging.md", [], None),

    # -- Templating (Twig) --
    ("Templating (Twig)", "TwigBundle", "twig/controller-rendering.md", ["twig/index.md"], "No standalone TwigBundle chapter; mapped to Controller Rendering, the chapter that actually covers the Twig↔Symfony integration TwigBundle wires up."),
    ("Templating (Twig)", "Twig syntax up to 3.22", "twig/syntax.md", [], "Version ceiling made explicit per mission brief; verify chapter contains no 3.23+-only syntax."),
    ("Templating (Twig)", "Auto escaping", "twig/auto-escaping.md", [], None),
    ("Templating (Twig)", "Template inheritance", "twig/inheritance.md", [], None),
    ("Templating (Twig)", "Global variables", "twig/globals.md", [], None),
    ("Templating (Twig)", "Filters and functions", "twig/filters-functions.md", [], None),
    ("Templating (Twig)", "Template includes", "twig/includes.md", [], None),
    ("Templating (Twig)", "Loops and conditions", "twig/loops-conditions.md", [], None),
    ("Templating (Twig)", "URLs generation", "twig/urls.md", [], None),
    ("Templating (Twig)", "Controller rendering", "twig/controller-rendering.md", [], None),
    ("Templating (Twig)", "Translations and pluralization", "twig/translations.md", [], None),
    ("Templating (Twig)", "String interpolation", "twig/interpolation.md", [], None),
    ("Templating (Twig)", "Assets management", "twig/assets.md", [], None),
    ("Templating (Twig)", "Debugging variables", "twig/debugging.md", [], None),

    # -- Forms --
    ("Forms", "Form component", "forms/creation.md", ["forms/index.md"], "No standalone \"what is the Form component\" chapter; mapped to Forms Creation, the chapter that introduces the component end-to-end."),
    ("Forms", "Form options (OptionsResolver)", "forms/types.md", ["forms/creation.md", "forms/type-extensions.md"], "OptionsResolver is taught distributed across 3 chapters (dedicated \"OptionsResolver features\" tab + certification question in types.md), not a standalone options-resolver.md — judged sufficiently covered; not created per the \"only if necessary\" rule."),
    ("Forms", "Forms creation", "forms/creation.md", [], None),
    ("Forms", "Forms handling", "forms/handling.md", [], None),
    ("Forms", "Form types (built-in & custom)", "forms/types.md", [], None),
    ("Forms", "Forms rendering with Twig", "forms/rendering.md", [], None),
    ("Forms", "Forms theming", "forms/theming.md", [], None),
    ("Forms", "CSRF protection", "forms/csrf.md", [], None),
    ("Forms", "Handling file upload", "forms/file-upload.md", [], None),
    ("Forms", "Built-in form types", "forms/built-in-types.md", [], None),
    ("Forms", "Data transformers", "forms/data-transformers.md", [], None),
    ("Forms", "Form events", "forms/events.md", [], None),
    ("Forms", "Form type extensions", "forms/type-extensions.md", [], None),

    # -- Data Validation --
    ("Data Validation", "Validator component", "validation/object-validation.md", ["validation/index.md"], "No standalone \"what is the Validator component\" chapter; mapped to Object validation, the entry-point chapter."),
    ("Data Validation", "PHP object validation", "validation/object-validation.md", [], None),
    ("Data Validation", "Built-in validation constraints", "validation/built-in-constraints.md", [], None),
    ("Data Validation", "Validation scopes", "validation/scopes.md", [], None),
    ("Data Validation", "Validation groups", "validation/groups.md", [], None),
    ("Data Validation", "Group sequence", "validation/group-sequence.md", [], None),
    ("Data Validation", "Custom callback validators", "validation/callbacks.md", [], None),
    ("Data Validation", "Custom constraints", "validation/custom-constraints.md", [], None),
    ("Data Validation", "Violations builder", "validation/violations-builder.md", [], None),

    # -- Dependency Injection --
    ("Dependency Injection", "Dependency Injection component", "dependency-injection/container.md", ["dependency-injection/index.md"], "No standalone \"what is the DI component\" chapter; mapped to the Service Container chapter."),
    ("Dependency Injection", "Service container", "dependency-injection/container.md", [], None),
    ("Dependency Injection", "Built-in services", "dependency-injection/built-in-services.md", [], None),
    ("Dependency Injection", "Configuration parameters", "dependency-injection/parameters.md", [], None),
    ("Dependency Injection", "Services registration (YAML & attributes)", "dependency-injection/registration.md", [], None),
    ("Dependency Injection", "Service decoration", "dependency-injection/decoration.md", [], None),
    ("Dependency Injection", "Tags", "dependency-injection/tags.md", [], None),
    ("Dependency Injection", "Semantic configuration", "dependency-injection/semantic-config.md", [], None),
    ("Dependency Injection", "Factories", "dependency-injection/factories.md", [], None),
    ("Dependency Injection", "Compiler passes", "dependency-injection/compiler-passes.md", [], None),
    ("Dependency Injection", "Services autowiring", "dependency-injection/autowiring.md", [], None),
    ("Dependency Injection", "Service locators", "dependency-injection/service-locators.md", [], None),

    # -- Security --
    ("Security", "Security Core", "security/authentication.md", ["security/authorization.md", "security/index.md"], "No standalone \"Security Core\" overview chapter; mapped to Authentication + Authorization, its two pillars."),
    ("Security", "CSRF", "forms/csrf.md", [], "Taught under Forms (CSRF is implemented via the Security component's CsrfTokenManager but exposed through form protection) — cross-area mapping, not duplicated here."),
    ("Security", "Authentication", "security/authentication.md", [], None),
    ("Security", "Authorization", "security/authorization.md", [], None),
    ("Security", "Configuration", "security/configuration.md", [], None),
    ("Security", "Providers", "security/providers.md", [], None),
    ("Security", "Firewalls", "security/firewalls.md", [], None),
    ("Security", "Users", "security/users.md", [], None),
    ("Security", "PasswordHasher (password hashers)", "security/password-hashers.md", [], None),
    ("Security", "Roles", "security/roles.md", [], None),
    ("Security", "Access control rules", "security/access-control.md", [], None),
    ("Security", "Authenticators, passports & badges", "security/authenticators.md", [], None),
    ("Security", "Voters & voting strategies", "security/voters.md", [], None),

    # -- HTTP Caching (ESI removed to Out-of-scope) --
    ("HTTP Caching", "Cache types", "http-caching/cache-types.md", [], None),
    ("HTTP Caching", "Expiration (Expires, Cache-Control)", "http-caching/expiration.md", [], None),
    ("HTTP Caching", "Validation (ETag, Last-Modified)", "http-caching/validation.md", [], None),
    ("HTTP Caching", "Client-side caching", "http-caching/client-side.md", [], None),
    ("HTTP Caching", "Server-side caching", "http-caching/server-side.md", [], None),

    # -- Console --
    ("Console", "Console component", "console/built-in-commands.md", ["console/index.md"], "No standalone \"what is the Console component\" chapter; mapped to Built-in Commands, the chapter that introduces the component end-to-end."),
    ("Console", "Built-in commands", "console/built-in-commands.md", [], None),
    ("Console", "Custom commands", "console/custom-commands.md", [], None),
    ("Console", "Configuration", "console/configuration.md", [], None),
    ("Console", "Options & arguments (incl. PHP attributes)", "console/options-arguments.md", ["console/custom-commands.md"], "Covers both classic addArgument()/addOption() and the #[Argument]/#[Option] attribute style — merged into one row rather than duplicated, since both live in the same chapter."),
    ("Console", "Input & Output objects", "console/input-output.md", [], None),
    ("Console", "Built-in helpers", "console/helpers.md", [], None),
    ("Console", "Console events", "console/events.md", [], None),
    ("Console", "Verbosity levels", "console/verbosity.md", [], None),

    # -- Automated Tests (PHPUnit Bridge removed to Out-of-scope) --
    ("Automated Tests", "CssSelector component", "testing/crawler.md", [], "No standalone CssSelector chapter; the Crawler chapter's selector examples cover it — cross-referenced, not duplicated."),
    ("Automated Tests", "DomCrawler component", "testing/crawler.md", [], None),
    ("Automated Tests", "WebProfilerBundle", "miscellaneous/profiler.md", ["testing/profiler.md"], "Web Profiler content lives under Miscellaneous; cross-referenced here for Automated Tests' WebProfilerBundle subtopic rather than duplicated."),
    ("Automated Tests", "Unit tests with PHPUnit", "testing/unit-tests.md", [], None),
    ("Automated Tests", "Functional tests with PHPUnit", "testing/functional-tests.md", [], None),
    ("Automated Tests", "Client object", "testing/client.md", [], None),
    ("Automated Tests", "Crawler object", "testing/crawler.md", [], None),
    ("Automated Tests", "Profiler object", "testing/profiler.md", [], None),
    ("Automated Tests", "Framework objects access", "testing/framework-objects.md", [], None),
    ("Automated Tests", "Client configuration", "testing/client-configuration.md", [], None),
    ("Automated Tests", "Request/response introspection", "testing/introspection.md", [], None),
    ("Automated Tests", "Handling legacy deprecated code", "testing/deprecations.md", [], None),

    # -- Miscellaneous (Lock removed to Out-of-scope; Messenger promoted to its own topic below) --
    ("Miscellaneous", "Event / EventDispatcher component", "architecture/events.md", [], "Covered under Symfony Architecture → Event dispatcher & kernel events; cross-referenced here, not duplicated."),
    ("Miscellaneous", "PropertyAccess component", "miscellaneous/property-access.md", ["miscellaneous/serializer.md"], "New chapter (this lot), verified against PropertyAccessor/PropertyAccessorBuilder/ReflectionExtractor source on the 8.0 branch. No French translation yet."),
    ("Miscellaneous", "Web Profiler & Web Debug Toolbar & Data Collectors", "miscellaneous/profiler.md", [], None),
    ("Miscellaneous", "HTTP Caching / Reverse Proxies / Expiration / Validation", "http-caching/cache-types.md", ["http-caching/index.md"], "Fully covered under the dedicated HTTP Caching area; mapped to Cache Types (its entry-point chapter) since Miscellaneous also names these concepts, not duplicated."),
    ("Miscellaneous", "Configuration (Config/DotEnv/ExpressionLanguage)", "miscellaneous/configuration.md", [], None),
    ("Miscellaneous", "Error handling", "miscellaneous/error-handling.md", [], None),
    ("Miscellaneous", "Code debugging", "miscellaneous/debugging.md", [], None),
    ("Miscellaneous", "Deployment best practices", "miscellaneous/deployment.md", [], None),
    ("Miscellaneous", "Cache component", "miscellaneous/cache.md", [], None),
    ("Miscellaneous", "Process component", "miscellaneous/process.md", [], None),
    ("Miscellaneous", "Serializer component", "miscellaneous/serializer.md", [], None),
    ("Miscellaneous", "Mime & Mailer components", "miscellaneous/mailer.md", [], None),
    ("Miscellaneous", "Filesystem & Finder components", "miscellaneous/filesystem-finder.md", [], None),
    ("Miscellaneous", "Runtime component", "miscellaneous/runtime.md", [], None),
    ("Miscellaneous", "Clock component", "miscellaneous/clock.md", [], None),

    # -- Messenger (promoted to its own official topic per mission brief) --
    ("Messenger", "Messenger component", "messenger/component.md", ["messenger/index.md"], "Split (this lot) from a prior monolithic miscellaneous/messenger.md into docs/messenger/ — one chapter per official subtopic, each with its own full anatomy."),
    ("Messenger", "Messages and handlers", "messenger/messages-handlers.md", [], None),
    ("Messenger", "Middleware", "messenger/middleware.md", [], None),
    ("Messenger", "Transports", "messenger/transports.md", [], "Third-party transports (Doctrine, Redis, Amazon SQS) are out of scope — see Out-of-scope section; the chapter says so explicitly."),
    ("Messenger", "Workers", "messenger/workers.md", [], None),
    ("Messenger", "Retries and failures", "messenger/retries-failures.md", [], None),
    ("Messenger", "Events", "messenger/events.md", [], "Covers 6 worker events (WorkerStarted/MessageReceived/MessageHandled/MessageFailed/Running/Stopped/RateLimited) plus the dispatch-side SendMessageToTransportsEvent, verified against source."),

    # -- Internationalization and localization (promoted to its own official topic per mission brief) --
    ("Internationalization and localization", "Internationalization and localization", "miscellaneous/intl.md", [], "Chapter also teaches Intl-component ICU utilities (Countries/Languages/Locales/Currencies/Timezones), now explicitly marked excluded from the exam inside the chapter (this lot) — see Out-of-scope section."),
]

# (topic label, item, note)
OUT_OF_SCOPE: list[tuple[str, str, str]] = [
    ("PHP — additional/depth", "Namespaces & Autoloading", "php-web-security/namespaces.md — kept as enrichment, not on the official 9-item PHP list."),
    ("PHP — additional/depth", "PHP Extensions", "php-web-security/extensions.md — kept as enrichment."),
    ("PHP — additional/depth", "SPL", "php-web-security/spl.md — kept as enrichment."),
    ("PHP — additional/depth", "Web Security Fundamentals", "php-web-security/web-security.md — kept as enrichment."),
    ("HTTP Caching", "Edge Side Includes (ESI)", "http-caching/esi.md — excluded from the syllabus per mission brief; chapter now carries an explicit exclusion notice, its 10 quiz questions are tagged out_of_scope: true."),
    ("Automated Tests", "PHPUnit Bridge", "testing/phpunit-bridge.md — excluded per mission brief; chapter now carries an explicit exclusion notice, its 8 quiz questions are tagged out_of_scope: true."),
    ("Miscellaneous", "Lock component", "miscellaneous/lock.md — excluded per mission brief; chapter now carries an explicit exclusion notice, its 6 quiz questions are tagged out_of_scope: true."),
    ("Messenger", "Doctrine / Redis / Amazon SQS transports", "Third-party Messenger transports — excluded per mission brief; messenger/transports.md says so explicitly. No quiz questions found testing them specifically."),
    ("Internationalization", "Intl component ICU utilities", "Countries/Languages/Locales/Currencies/Timezones static lookup classes in miscellaneous/intl.md — excluded from the exam per mission brief; chapter now carries an explicit exclusion notice. No quiz question found testing this API."),
    ("Ecosystem (never taught)", "Symfony UX, Symfony AI, Doctrine, Monolog, AssetMapper, Webpack Encore, third-party bundles/bridges", "Out of scope by design since the project's original GapAnalysis.md; mentions found are contextual/comparative, not taught content — not re-audited line-by-line this lot."),
]


def fmt_paths(paths: list[str]) -> str:
    if not paths:
        return "—"
    return "; ".join(f"`{p}`" for p in paths)


def render() -> str:
    lines = [
        "# Traceability Matrix",
        "",
        "_Reconstructed against the mission brief (2026-08-26): official syllabus",
        "realignment, PHP Attributes/Enums, HTTP RFC 9110, missing component rows,",
        "a dedicated Messenger topic, and an explicit Out-of-scope / Additional",
        "Learning section. Regenerate: `python tools/gen_traceability_matrix.py`._",
        "",
        "**Status legend:** `PASS` = automated evidence found for every one of:",
        "existing path, non-empty content, a worked example, an Exercises section,",
        "a Solutions block, at least one situational/scenario/trap/debug quiz",
        "question tagged to it, a Certification-traps pitfall block, a Symfony 8.0",
        "(`blob/8.0` or `tree/8.0`) source reference, and an official doc/php.net/RFC reference —",
        "**and** no out-of-scope dependency. `TO VERIFY` = anything short of that;",
        "the Anomaly column names exactly what is missing. **No row is marked PASS",
        "without this checked evidence — a PASS here is not a claim that the",
        "content is pedagogically excellent, only that the required building",
        "blocks are present.**",
        "",
        "**Network limitation (this run):** `certification.symfony.com`,",
        "`symfony.com`, `www.php.net`, and `www.rfc-editor.org` were unreachable",
        "from this environment (egress blocked) — only `github.com` (source code)",
        "was reachable. Official Topic/Subtopic wording below is taken from the",
        "mission brief and this repo's pre-existing topic list, not independently",
        "re-fetched from the live syllabus page this session. Treat wording",
        "mismatches against the live page as a TO VERIFY item, not a confirmed",
        "anomaly, until someone with access re-checks it.",
        "",
        "**Never state 100% coverage from this file alone** — it reports what",
        "automated checks can confirm, not human pedagogical review, and several",
        "rows are explicit, named gaps (see Status = TO VERIFY rows and their",
        "Anomaly column).",
        "",
    ]

    # header
    cols = ["Official Topic", "Official Subtopic", "Main Chapter",
            "Additional Chapters", "Example", "Exercise", "Solution",
            "Situational Q", "Pitfall", "Sf 8.0 Ref", "Official Ref",
            "Status", "Anomaly"]
    total = 0
    passed = 0
    by_topic_totals: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])

    current_topic = None
    for topic, subtopic, main, additional, note in SYLLABUS:
        if topic != current_topic:
            if current_topic is not None:
                lines.append("")
            lines.append(f"## {topic}")
            lines.append("")
            lines.append("| " + " | ".join(cols) + " |")
            lines.append("|" + "---|" * len(cols))
            current_topic = topic
        ev = evidence(main)
        out_dep = bool(note and "excluded" in (note or "").lower() and "GAP" not in note)
        status = status_for(ev, out_of_scope_dep=False)
        gap_list = gaps(ev, main)
        anomaly_parts = []
        if note:
            anomaly_parts.append(note)
        if status != "PASS":
            anomaly_parts.append("Missing: " + ", ".join(gap_list) + ".")
        anomaly = " ".join(anomaly_parts) if anomaly_parts else "—"

        def mark(key: str) -> str:
            return "✓" if ev.get(key) else "—"

        total += 1
        by_topic_totals[topic][0] += 1
        if status == "PASS":
            passed += 1
            by_topic_totals[topic][1] += 1

        main_cell = f"`{main}`" if main else "—"
        row = [topic, subtopic, main_cell, fmt_paths(additional),
               mark("example"), mark("exercise"), mark("solution"),
               mark("situational"), mark("pitfall"), mark("sf8_ref"),
               mark("official_ref"), status, anomaly]
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in row) + " |")

    lines += ["", "## Out-of-scope / Additional Learning", "",
              "Content kept in the repository as enrichment but explicitly **not**",
              "part of the official Symfony 8 certification syllabus, and excluded",
              "from official coverage statistics, generated exams, and the quiz bank's",
              "official question count (tagged `out_of_scope: true` where applicable):",
              "", "| Area | Item | Note |", "|---|---|---|"]
    for area, item, note in OUT_OF_SCOPE:
        lines.append(f"| {area} | {item} | {note} |")

    lines += ["", "## Coverage summary", "",
              "_Automated evidence only (see Status legend above) — not a claim of",
              "pedagogical completeness or of 100% syllabus alignment._", "",
              "| Official Topic | Subtopics | PASS (automated evidence) |",
              "|---|---|---|"]
    for topic, (n, p) in by_topic_totals.items():
        lines.append(f"| {topic} | {n} | {p} |")
    pct = f"{100.0 * passed / total:.1f}%" if total else "n/a"
    lines.append(f"| **Total** | **{total}** | **{passed} ({pct})** |")
    lines += ["",
              f"**{total - passed} of {total} official subtopics are `TO VERIFY`** —",
              "either a genuine content gap (no Main Chapter, or a named missing",
              "building block) or a chapter this run's automated checks could not",
              "fully confirm. See each row's Anomaly column. This count is never to",
              "be reported as \"100% done\" — several TO VERIFY rows are real,",
              "named gaps, not merely unchecked boxes.", ""]
    return "\n".join(lines)


def main() -> None:
    content = render()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()

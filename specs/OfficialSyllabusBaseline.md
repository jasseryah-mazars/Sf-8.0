# Official Syllabus Baseline

_Established 2026-08-27. Regenerate/re-verify whenever network access to the primary
sources below becomes available, or when Symfony announces a syllabus revision._

> **This file's title says "Official" because it *tracks* the official syllabus —**
> **it is not itself an official document, and §2/§3 below are not proof of what**
> **the official syllabus says.** The taxonomy in §3 was derived from
> `specs/TraceabilityMatrix.md`, which is this repository's own working document,
> not `certification.symfony.com` re-read live. Nowhere in this repository should
> "175 subtopics" or the taxonomy below be cited as confirmation of the official
> syllabus's actual contents — only as this project's current best-effort tracking
> of it, explicitly pending live re-verification (§1).

## 1. Sources consulted this run (network reachability, checked live)

| # | Source | URL | Reachable this run? | Result |
|---|---|---|---|---|
| 1 | Official certification syllabus | https://certification.symfony.com/exams/symfony.html | ❌ No — `EGRESS_BLOCKED` (network egress proxy blocks `certification.symfony.com`) | Not re-fetched live this run |
| 2 | Symfony 8.0 documentation | https://symfony.com/doc/8.0/ | ❌ No — `EGRESS_BLOCKED` (network egress proxy blocks `symfony.com`) | Not re-fetched live this run |
| 3 | Symfony 8.0 source (GitHub) | https://github.com/symfony/symfony/tree/8.0 | ✅ Yes (web page render); ❌ `api.github.com` returns 403 in this environment | Branch/tag `8.0` confirmed to exist; per-file source verification done throughout the repo via `github.com/.../blob/8.0/...` links (raw source, reachable) |
| 4 | PHP 8.4 official documentation | https://www.php.net/ | ❌ No — blocked in this environment (established in prior sessions; not re-tested this exact run, same proxy policy) | Verified via `php -v` (8.4.19 installed) + `php -l`/PHPUnit-free static parse in `tools/lint_php.py`, not by fetching php.net pages |
| 5 | Twig documentation matching the syllabus | https://twig.symfony.com/doc/3.x/ (and `symfony.com/doc/3.x/` mirror) | ❌ No — same proxy policy blocks `symfony.com`/`twig.symfony.com` | Not re-fetched live this run |
| 6 | This repository's own content, after verification | (local) | ✅ Yes | Used as the basis for the taxonomy below, cross-referenced against `specs/TraceabilityMatrix.md`, itself built over several prior sessions against sources 2–3 when they *were* reachable |

**Consequence of the network limitation (documented per the mission's own
conflict/ambiguity rule — "documente la décision"):** sources 1, 2 and 5 — the
live syllabus page, the live Symfony 8.0 doc tree, and the live Twig doc tree —
could not be re-fetched from this environment. The taxonomy in §2 is the
**operational baseline** carried over from `specs/TraceabilityMatrix.md`, which
prior sessions built and repeatedly cross-checked against these same sources
while they were reachable (see `specs/GapAnalysis.md`, `specs/Requirements.md`,
and the matrix's own revision history). It is not a fresh, independent re-read
of the syllabus page performed today. Anyone with network access to
`certification.symfony.com` should diff this file's §2 against the live page
and record any divergence in `specs/RemediationLog.md` before trusting a
`conforme` status on a syllabus-taxonomy question.

## 2. Version baseline

| Component | Pinned version | Source |
|---|---|---|
| Symfony | **8.0 exclusively** | Mission brief; `github.com/symfony/symfony/tree/8.0` confirmed to exist |
| PHP | **8.4** (`8.4+` baseline, no 8.5-only syntax) | Mission brief; `php -v` in this environment reports 8.4.19 |
| Twig | **3.x, up to 3.22** | Carried over from prior sessions' version-lock (`docs/_meta/CONVENTIONS.md`); not re-verified against a live Twig changelog this run (network blocked) |

## 3. Official taxonomy (operational baseline)

**16 official topic areas, 175 subtopics total.** This count is
whatever `specs/TraceabilityMatrix.md` currently enumerates — deliberately
**not** hardcoded here or anywhere else in the tooling (see
`tools/final_audit.py`, fixed this run to stop hardcoding the historical `154`
figure). Re-running the extraction that produced this section is one command:
`python3` snippet in `specs/RemediationLog.md`'s P0-02 entry.

### PHP (9)

- PHP API (up to 8.4)
- OOP
- Attributes
- Interfaces
- Closures
- Abstract Classes
- Exception & Error Handling
- Traits
- Enums

### HTTP (11)

- HTTP Specification (RFC 9110)
- Client/Server interaction
- Status codes
- HTTP request
- HTTP response
- HTTP methods
- Cookies
- Caching
- Content negotiation
- Language detection
- HttpClient component

### Symfony Architecture (17)

- Symfony Flex
- License
- Components
- HttpFoundation component
- Bridges
- Code organization
- Request handling
- Exception handling
- Event dispatcher & kernel events
- Official best practices
- Release management
- Backward compatibility promise
- Deprecations best practices
- Framework overloading
- Release management & roadmap schedule
- Interoperability & PSRs
- Naming conventions

### Controllers (15)

- Naming conventions
- AbstractController
- HttpKernel component
- FrameworkBundle
- The request
- The response
- The cookies
- The session
- Flash messages
- HTTP redirects
- Internal redirects
- Generate 404 pages
- File upload
- Built-in internal controllers
- Argument value resolvers

### Routing (13)

- Routing component
- FrameworkBundle
- Configuration (YAML & attributes)
- Restrict URL parameters
- Default values
- Generate URL parameters
- Trigger redirects
- Special internal routing attributes
- Domain name matching
- Conditional request matching
- HTTP methods matching
- User's locale guessing
- Router debugging

### Templating (Twig) (14)

- TwigBundle
- Twig syntax up to 3.22
- Auto escaping
- Template inheritance
- Global variables
- Filters and functions
- Template includes
- Loops and conditions
- URLs generation
- Controller rendering
- Translations and pluralization
- String interpolation
- Assets management
- Debugging variables

### Forms (13)

- Form component
- Form options (OptionsResolver)
- Forms creation
- Forms handling
- Form types (built-in & custom)
- Forms rendering with Twig
- Forms theming
- CSRF protection
- Handling file upload
- Built-in form types
- Data transformers
- Form events
- Form type extensions

### Data Validation (9)

- Validator component
- PHP object validation
- Built-in validation constraints
- Validation scopes
- Validation groups
- Group sequence
- Custom callback validators
- Custom constraints
- Violations builder

### Dependency Injection (12)

- Dependency Injection component
- Service container
- Built-in services
- Configuration parameters
- Services registration (YAML & attributes)
- Service decoration
- Tags
- Semantic configuration
- Factories
- Compiler passes
- Services autowiring
- Service locators

### Security (13)

- Security Core
- CSRF
- Authentication
- Authorization
- Configuration
- Providers
- Firewalls
- Users
- PasswordHasher (password hashers)
- Roles
- Access control rules
- Authenticators, passports & badges
- Voters & voting strategies

### HTTP Caching (5)

- Cache types
- Expiration (Expires, Cache-Control)
- Validation (ETag, Last-Modified)
- Client-side caching
- Server-side caching

### Console (9)

- Console component
- Built-in commands
- Custom commands
- Configuration
- Options & arguments (incl. PHP attributes)
- Input & Output objects
- Built-in helpers
- Console events
- Verbosity levels

### Automated Tests (12)

- CssSelector component
- DomCrawler component
- WebProfilerBundle
- Unit tests with PHPUnit
- Functional tests with PHPUnit
- Client object
- Crawler object
- Profiler object
- Framework objects access
- Client configuration
- Request/response introspection
- Handling legacy deprecated code

### Miscellaneous (15)

- Event / EventDispatcher component
- PropertyAccess component
- Web Profiler & Web Debug Toolbar & Data Collectors
- HTTP Caching / Reverse Proxies / Expiration / Validation
- Configuration (Config/DotEnv/ExpressionLanguage)
- Error handling
- Code debugging
- Deployment best practices
- Cache component
- Process component
- Serializer component
- Mime & Mailer components
- Filesystem & Finder components
- Runtime component
- Clock component

### Messenger (7)

- Messenger component
- Messages and handlers
- Middleware
- Transports
- Workers
- Retries and failures
- Events

### Internationalization and localization (1)

- Internationalization and localization

## 4. Explicitly out of scope (per the mission brief and prior sessions' work)

Named only to mark the boundary — none of this is taught or evaluated as
substantive, scored content in this repository:

- Symfony UX, Symfony AI, Doctrine, Monolog, AssetMapper, Webpack Encore,
  PHP Polyfills, String/Uid/TypeInfo components, third-party Messenger
  transports (Doctrine, Redis, Amazon SQS), and any component absent from
  the taxonomy in §3.
- Edge Side Includes (ESI), PHPUnit Bridge, and the Lock component are
  explicitly named by the mission as excluded despite having a full chapter
  each in this repository (`docs/appendices/out-of-syllabus/esi.md`,
  `docs/appendices/out-of-syllabus/phpunit-bridge.md`, `docs/appendices/out-of-syllabus/lock.md`) — each
  chapter already carries its own "Excluded from Symfony 8 certification"
  notice from a prior session's audit; see P0-03 in `specs/RemediationPlan.md`
  for the re-verification and `docs/appendices/out-of-syllabus/` relocation
  this run performs.

_See `specs/TraceabilityMatrix.md`'s own "Out-of-scope / Additional Learning"
section for the row-by-row detail this summary is drawn from._


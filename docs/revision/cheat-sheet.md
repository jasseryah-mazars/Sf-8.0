# Master Cheat Sheet

The highest-yield, glanceable facts across all 15 topic areas. This is a
**skeleton for the night before** — each section links to the full area for detail.
Everything here is Symfony 8 / PHP 8.4 / Twig 3.x.

!!! tip "How to use it"
    Cover the right-hand column and recite it. If a section feels thin, open its
    topic index (linked in each heading) for the full chapters and cheat sheets.

## 1. PHP & Web Security → [area](../php-web-security/index.md)

- **PHP 8.4:** property hooks, asymmetric visibility (`public private(set)`),
  `new` without parentheses in chaining, lazy objects, `#[\Deprecated]` attribute,
  `array_find` / `array_any` / `array_all` / `array_find_key`.
- **PHP 8.3:** typed class constants, `#[\Override]`, `json_validate()`, dynamic
  class-constant fetch.
- **Web threats:** XSS → output encoding/escaping; CSRF → per-form tokens; SQLi →
  parameterized/prepared statements; session fixation → regenerate id on login;
  transport → HTTPS + HSTS.
- **SPL:** `Iterator`, `IteratorAggregate`, `ArrayAccess`, `Countable`,
  `SplStack`, `SplQueue`, `SplObjectStorage`, `ArrayObject`.

## 2. HTTP → [area](../http/index.md)

| Class | Meaning | Common |
|---|---|---|
| 1xx | Informational | 100, 101 |
| 2xx | Success | 200, 201, 204 |
| 3xx | Redirection | 301, 302, 304, 307, 308 |
| 4xx | Client error | 400, 401, 403, 404, 405, 409, 422, 429 |
| 5xx | Server error | 500, 502, 503, 504 |

- **Safe methods:** GET, HEAD, OPTIONS, TRACE. **Idempotent:** safe + PUT, DELETE.
  **Neither:** POST, PATCH.
- **Negotiation headers:** `Accept`, `Accept-Language`, `Accept-Encoding`,
  `Accept-Charset`.

## 3. Symfony Architecture → [area](../architecture/index.md)

- **Kernel event order:** `kernel.request` → `kernel.controller` →
  `kernel.controller_arguments` → *(`kernel.view` only if controller returns a
  non-`Response`)* → `kernel.response` → `kernel.finish_request` →
  `kernel.terminate`. `kernel.exception` fires on any thrown exception.
- **Event classes:** `RequestEvent`, `ControllerEvent`, `ControllerArgumentsEvent`,
  `ViewEvent`, `ResponseEvent`, `FinishRequestEvent`, `TerminateEvent`,
  `ExceptionEvent`.
- **Request types:** `HttpKernelInterface::MAIN_REQUEST` / `SUB_REQUEST`.
- **Releases:** minor every ~6 months (May & Nov); major every ~2 years; the **last
  minor of a major is the LTS**. Standard = 8 months bug-fix + 6 months security;
  LTS = 3 years bug-fix + 4 years security. Follows **semver + BC promise**
  (`@internal`, `@final`, `@experimental`).

## 4. Dependency Injection → [area](../dependency-injection/index.md)

- **Services are private by default**; **autowiring + autoconfiguration on** by
  default in the standard config.
- **Container is compiled once** and cached; compiler passes run at compile time.
- **Compiler pass registration:** `ContainerBuilder::addCompilerPass()` in
  `Kernel::build()` or a bundle `build()` — **no attribute** for this.
- **Attributes:** `#[Autowire]`, `#[AutowireLocator]`, `#[AutowireIterator]`,
  `#[AsTaggedItem]`, `#[AsDecorator]`, `#[When(env: 'prod')]`, `#[Exclude]`.
- **Params:** `%kernel.project_dir%`, `%env(...)%`; inject via `#[Autowire('%...%')]`.

## 5. Controllers → [area](../controllers/index.md)

- **`AbstractController` helpers:** `render()`, `redirectToRoute()`, `forward()`
  (internal sub-request), `json()`, `file()`, `addFlash()`, `isGranted()`,
  `createNotFoundException()`, `createAccessDeniedException()`, `generateUrl()`,
  `getUser()`, `createForm()`.
- **Value resolvers:** `#[MapRequestPayload]`, `#[MapQueryString]`,
  `#[MapQueryParameter]`, backed-enum, UID, `DateTime` resolvers.
- A controller must return a `Response`; otherwise `kernel.view` must build one.

## 6. Routing → [area](../routing/index.md)

- **`#[Route]` options:** `path`, `name`, `methods`, `requirements`, `defaults`,
  `host`, `schemes`, `condition`, `priority`, `locale`.
- **URL generation reference types:** `ABSOLUTE_URL`, `ABSOLUTE_PATH` (default),
  `RELATIVE_PATH`, `NETWORK_PATH`.
- **Special params:** `_controller`, `_format`, `_locale`, `_fragment`.
- **Debug:** `debug:router`, `router:match <path>`.

## 7. Templating (Twig) → [area](../twig/index.md)

- **Delimiters:** `{{ ... }}` print, `{% ... %}` logic, `{# ... #}` comment.
- **Auto-escaping is ON** (html strategy); disable per-value with `|raw`.
- **Inheritance:** `{% extends %}`, `{% block %}`, `{{ parent() }}`; reuse with
  `{% include %}`, `{% embed %}`, `{% use %}`.
- **URLs/assets:** `path()`, `url()` (absolute), `asset()`, `absolute_url()`.
- **i18n:** `|trans`, `{% trans %}`.

## 8. Data Validation → [area](../validation/index.md)

- Constraints on **properties, getters, or the class**; attributes like
  `#[Assert\NotBlank]`, `#[Assert\Length]`, `#[Assert\Valid]` (cascade).
- **Groups** + **`GroupSequence`** control which/when; **`Sequentially`** stops at
  first failure.
- Custom pair = **`Constraint`** (`getTargets()`) + **`ConstraintValidator`**
  (`validate($value, Constraint $c)`), report via
  `$this->context->buildViolation()`.

## 9. Forms → [area](../forms/index.md)

- **Flow:** `createForm()` → `handleRequest($request)` → `isSubmitted() && isValid()`.
- **Form event order:** `PRE_SET_DATA` → `POST_SET_DATA` → `PRE_SUBMIT` →
  `SUBMIT` → `POST_SUBMIT`.
- **Data transformers:** model ↔ norm ↔ view; `addModelTransformer()`,
  `addViewTransformer()`.
- **CSRF on by default** for forms (`csrf_protection`, `csrf_token_id`).
- **Type extension:** implement `getExtendedTypes()`.

## 10. Security → [area](../security/index.md)

- **`security.yaml` keys:** `firewalls`, `providers`, `password_hashers`,
  `access_control`, `role_hierarchy`.
- **Auth flow:** authenticator `supports()` → `authenticate()` returns a
  **`Passport`** (with **badges**) → token created → success/failure handler.
- **Passport badges:** `UserBadge`, `PasswordCredentials`, `CsrfTokenBadge`,
  `RememberMeBadge`, `PasswordUpgradeBadge`, `PreAuthenticatedUserBadge`.
- **Voters:** `voteOnAttribute()` returns granted/denied/abstain. **Strategies:**
  **affirmative (default)**, consensus, unanimous, priority.
- **Attributes:** `IS_AUTHENTICATED_FULLY`, `_REMEMBERED`, `_LAZILY`,
  `PUBLIC_ACCESS`, `IS_IMPERSONATOR`.
- **Hashers:** `auto` (bcrypt / Argon2id).

## 11. HTTP Caching → [area](../http-caching/index.md)

- **Expiration model:** `Expires`, `Cache-Control: max-age` (browser),
  `s-maxage` (shared/proxy).
- **Validation model:** `ETag` ↔ `If-None-Match`; `Last-Modified` ↔
  `If-Modified-Since` → **`304 Not Modified`**.
- **Cache-Control directives:** `public`, `private`, `no-cache` (revalidate before
  use), `no-store` (never store), `must-revalidate`, `max-age`, `s-maxage`.
- **`Vary`** varies the cache key; Symfony ships a **`HttpCache`** reverse proxy.
  *(Down-weighted in the Symfony 8 exam.)* ESI is out of scope — **excluded
  from Symfony 8 certification**.

## 12. Console → [area](../console/index.md)

- **Command:** `#[AsCommand(name: '...', description: '...')]`; `execute()` returns
  `Command::SUCCESS` (0), `FAILURE` (1), or `INVALID` (2).
- **Arguments:** `REQUIRED`, `OPTIONAL`, `IS_ARRAY`. **Options:** `VALUE_NONE`,
  `VALUE_REQUIRED`, `VALUE_OPTIONAL`, `VALUE_IS_ARRAY`, `VALUE_NEGATABLE`.
- **Verbosity:** `-q` quiet (16) · normal (32) · `-v` verbose (64) · `-vv`
  very-verbose (128) · `-vvv` debug (256).
- **Events:** `console.command`, `console.signal`, `console.error`,
  `console.terminate`.

## 13. Messenger → [area](../messenger/index.md)

- **Up-weighted** on the Symfony 8 exam. `MessageBusInterface::dispatch()`
  returns an **`Envelope`** wrapping the message + **stamps** (metadata).
- Handlers via **`#[AsMessageHandler]`**; the middleware pipeline is
  **russian-doll** (`$stack->next()->handle($envelope, $stack)`).
- **Transports** (Doctrine, AMQP, Redis, `sync`, `in-memory`) are DSN-configured;
  worker via `messenger:consume`.
- **Retry strategy** (exponential backoff + **jitter**, default 0.1) +
  **failure transport** for exhausted retries.

## 14. Automated Tests → [area](../testing/index.md)

- **Base classes:** `KernelTestCase` (services), `WebTestCase` (HTTP via `Client`).
- **Client:** `request()`, `submitForm()`, `followRedirect()`; **Crawler:**
  `filter()`, `selectButton()`, `selectLink()`.
- **Assertions:** `assertResponseIsSuccessful()`,
  `assertResponseStatusCodeSame()`, `assertSelectorTextContains()`.
- **Container in tests:** `static::getContainer()`.
- **Deprecations:** PHPUnit bridge + `SYMFONY_DEPRECATIONS_HELPER`.

## 15. Miscellaneous → [area](../miscellaneous/index.md)

- **Serializer:** normalizers + encoders; `serialize()` / `deserialize()`; formats
  json/xml/csv/yaml.
- **Cache:** PSR-6 `CacheItemPoolInterface`, PSR-16, Symfony Contracts
  `CacheInterface::get($key, $callback)`.
- **Lock:** `LockFactory::createLock()`. **Clock:** `ClockInterface::now()`,
  `MockClock` for tests. **Runtime:** app entry point. **Intl / Config / DotEnv /
  ExpressionLanguage** round out the group.

---

<small>Related: [Top Certification Traps](traps.md) · [Memory Aids](memory-aids.md) · [Revision Hub](index.md)</small>

## Official References

- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)

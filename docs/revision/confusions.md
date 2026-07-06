# Easily Confused

The exam is built on **near-misses**: two things that look alike, one right answer.
This page is the antidote — the pairs candidates mix up, side by side. Skim it the
morning of the exam.

!!! abstract "How to use"
    Cover the right column, read the left, and say the difference out loud. If you
    hesitate, open the linked chapter.

## HTTP & responses

| These look alike | The distinction |
|---|---|
| **301 vs 302** | 301 = permanent (cached/reused); 302 = temporary. Default of `RedirectResponse` is **302**. |
| **307/308 vs 301/302** | 307/308 **keep the HTTP method & body**; 301/302 may switch to GET. |
| **401 vs 403** | 401 = *not authenticated* (who are you?); 403 = *authenticated but forbidden*. |
| **404 vs 410** | 404 = not found (maybe later); 410 = gone permanently. |
| **`max-age` vs `s-maxage`** | `max-age` = any cache; `s-maxage` = **shared** caches only (overrides `max-age` there) and implies `public`. |
| **ETag vs Last-Modified** | ETag = content fingerprint (exact); Last-Modified = timestamp (1s resolution). ETag **wins** if both present. |
| **`no-cache` vs `no-store`** | `no-cache` = may store but must revalidate; `no-store` = never store at all. |

## Architecture & kernel

| These look alike | The distinction |
|---|---|
| **`kernel.request` vs `kernel.controller`** | request runs **before** the controller is resolved; controller runs **after**, can change the callable. |
| **`kernel.view` vs `kernel.response`** | `view` fires **only** when the controller returns a **non-Response**; `response` fires for **every** response. |
| **`kernel.terminate` vs `kernel.response`** | response = before sending; terminate = **after** the response is sent (async-safe work). |
| **Listener vs Subscriber** | Listener wired in config/attribute; Subscriber declares its own events via `getSubscribedEvents()`. |

## Dependency Injection

| These look alike | The distinction |
|---|---|
| **Compile time vs runtime** | Container is **compiled once** (passes, autowiring) then dumped; `get()` happens at runtime from the compiled container. |
| **Autowiring vs Autoconfiguration** | Autowiring = inject **arguments** by type; autoconfigure = apply **tags/attributes** by interface. |
| **`#[Autowire]` vs binding** | `#[Autowire]` targets one argument; `bind` (in `_defaults`) targets many by name/type. |
| **Compiler pass registration** | There is **no `#[CompilerPass]` attribute** — register in `Kernel::build()` / bundle `build()`. |
| **`decoration_priority` direction** | Higher priority = applied **first** = **outermost** wrapper. `.inner` = the decorated service. |
| **Service locator vs injecting all** | Locator = **lazy**, fetch on demand; injecting all instantiates everything eagerly. |

## Security

| These look alike | The distinction |
|---|---|
| **Authentication vs Authorization** | AuthN = *who are you* (firewall/authenticator); AuthZ = *are you allowed* (access_control/voters). |
| **Badge vs Credentials** | `PasswordCredentials`/`CustomCredentials` verify secrets; other badges (`UserBadge`, `CsrfTokenBadge`…) add context. |
| **Voter strategies** | affirmative = one GRANT wins; unanimous = any DENY loses; consensus = majority. Default = **affirmative**. |
| **`ROLE_*` vs `IS_AUTHENTICATED_*`** | roles are assigned; `IS_AUTHENTICATED_*`/`PUBLIC_ACCESS` are runtime attributes, not roles. |
| **`access_control` order** | **first match wins** (top-to-bottom) — put specific paths above general ones. |
| **Abstain ≠ Deny** | A voter returning ABSTAIN does not block; only DENY does (per strategy). |

## Forms & validation

| These look alike | The distinction |
|---|---|
| **`PRE_SUBMIT` vs `PRE_SET_DATA`** | SET_DATA = model → form (pre-fill); SUBMIT = request → model (incoming data). |
| **Model vs view data** | Model = your object; view = the string in the input. Transformers convert between them. |
| **`addModelTransformer` vs `addViewTransformer`** | model↔norm vs norm↔view. Order matters; view transformer runs closest to the widget. |
| **`Default` vs `{ClassName}` group** | validating `Default` ≠ the class group when a `GroupSequence` exists on the class. |
| **`NotNull` vs `NotBlank`** | `NotNull` fails only on `null`; `NotBlank` also fails on `''`, `[]`, `false`. |

## Routing & Twig

| These look alike | The distinction |
|---|---|
| **`path()` vs `url()`** | `path()` = relative; `url()` = absolute (scheme+host). |
| **Reference types** | `ABSOLUTE_PATH` (default), `ABSOLUTE_URL`, `NETWORK_PATH`, `RELATIVE_PATH`. |
| **`render()` vs `render_esi()`** | `render` embeds inline (sub-request now); `render_esi` defers to a cache/ESI gateway. |
| **`{{ }}` vs `{% %}`** | `{{ }}` prints an expression; `{% %}` executes a tag (logic). |
| **`|raw` risk** | disables autoescaping → XSS if the value is user data. |

## Console & testing

| These look alike | The distinction |
|---|---|
| **`SUCCESS/FAILURE/INVALID`** | 0 / 1 / 2. Return them from `execute()`/`__invoke()`. |
| **Verbosity integers** | QUIET 16, NORMAL 32, VERBOSE 64, VERY_VERBOSE 128, DEBUG 256. |
| **`KernelTestCase` vs `WebTestCase`** | Kernel = boot container/services; Web = also make HTTP requests via the client. |
| **Test container privacy** | `self::getContainer()` exposes **private** services (real container doesn't). |

---

<small>Related: [Top Certification Traps](traps.md) · [Memory Aids](memory-aids.md) · [Cheat Sheet](cheat-sheet.md)</small>

## Official References

- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/current/)

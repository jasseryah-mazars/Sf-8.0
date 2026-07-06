# Top Certification Traps

The exam rewards **precise distinctions**, not definitions. This is a cross-area
index of the subtleties, misconceptions, and version-specific gotchas that most
often cost points. Each chapter has its own `!!! danger "Certification traps"`
block; this page seeds the well-known ones and links to the full area.

!!! danger "Read every option literally"
    Most traps are triggered by one word — **"always", "by default", "only",
    "never", "must"** — or by an old-but-familiar (deprecated) option offered next
    to the current one. Slow down on those.

## Architecture → [area](../architecture/index.md)

- **`kernel.view` only fires when the controller returns a *non-`Response`*.** If it
  already returns a `Response`, `view` is skipped.
- **`kernel.terminate` runs *after* the response is sent** — not before. Heavy
  work goes here, not in a response listener.
- Event **name** vs event **class** (`kernel.request` ↔ `RequestEvent`) — questions
  mix them.
- The **LTS is the last minor of a major**, not a separate track.

## Dependency Injection → [area](../dependency-injection/index.md)

- **Services are private by default** — you cannot `$container->get()` them unless
  made public or fetched via a service locator / test container.
- **Compiler passes have no attribute** — register them in `build()`.
- **Autowiring resolves by type, not by variable name** (except with `#[Autowire]`
  / named bindings). Renaming an argument does not change wiring.
- Parameters are **compile-time**; env vars (`%env(...)%`) are resolved at
  **runtime**.

## Security → [area](../security/index.md)

- **Default access-decision strategy is `affirmative`** (one granting voter is
  enough) — not unanimous.
- **`IS_AUTHENTICATED_REMEMBERED` ≠ `IS_AUTHENTICATED_FULLY`.** Remember-me users
  are authenticated but not "fully"; sensitive actions require FULLY.
- A **`Passport` carries badges**; `authenticate()` returns the passport, it does
  not return a token directly.
- **`access_control` matches top-to-bottom; first match wins** — order matters.
- `PUBLIC_ACCESS` is the way to allow anonymous access under the current system.

## HTTP & HTTP Caching → [HTTP](../http/index.md) · [Caching](../http-caching/index.md)

- **`no-cache` does not mean "don't cache"** — it means "revalidate before use".
  **`no-store`** means never store.
- **`max-age` is for browsers; `s-maxage` is for shared/proxy caches** and takes
  precedence in shared caches.
- **Expiration vs validation are different models** — `Expires`/`max-age` vs
  `ETag`/`Last-Modified`; validation yields **304 Not Modified**.
- **PUT is idempotent, POST is not.** GET/HEAD are safe *and* idempotent.
- `302` vs `301` vs `307`/`308` — permanent vs temporary, and method-preserving.

## Console → [area](../console/index.md)

- **Verbosity flags:** `-v`, `-vv`, `-vvv` map to verbose / very-verbose / debug —
  don't swap them.
- **`execute()` should return an int** (`Command::SUCCESS`/`FAILURE`/`INVALID`);
  returning nothing/`null` is wrong under current typing.
- **`VALUE_NONE`** options are boolean flags (presence = true); they take no value.
- Console event names (`console.command`, `console.error`, `console.terminate`,
  `console.signal`) vs kernel events — different dispatchers.

## Forms & Validation → [Forms](../forms/index.md) · [Validation](../validation/index.md)

- **Form event order:** `PRE_SET_DATA` → `POST_SET_DATA` → `PRE_SUBMIT` → `SUBMIT`
  → `POST_SUBMIT`. `PRE_SUBMIT` sees raw request data; `SUBMIT` sees normalized.
- **CSRF is enabled by default** for forms — disabling it is a deliberate choice.
- **`isValid()` implies `isSubmitted()`** internally, but call `handleRequest()`
  first; validating an unsubmitted form is meaningless.
- **Validation groups:** default group is `Default`; a `GroupSequence` changes both
  *which* constraints run and *in what order* (stops on first failing group).
- **Data transformers** run view→norm→model on submit and the reverse on display —
  direction confusion is a classic trap.

## Controllers & Routing → [Controllers](../controllers/index.md) · [Routing](../routing/index.md)

- **`forward()` is an internal sub-request** (server-side), **`redirect*()` sends a
  3xx to the browser** — not the same thing.
- **Route `priority`** breaks ties; more specific routes need higher priority or to
  be declared first.
- **`generateUrl()` default reference type is `ABSOLUTE_PATH`**, not absolute URL.
- Attribute routing is the current default; annotation syntax is legacy.

## Twig → [area](../twig/index.md)

- **Auto-escaping is on by default** (html) — `|raw` opts out and is a security
  risk if misused.
- **`{% include %}` vs `{% embed %}` vs `{% use %}`** — embed allows block
  overrides; use imports blocks horizontally.
- `path()` returns a **relative** URL, `url()` an **absolute** one.

## Miscellaneous / Messenger → [area](../miscellaneous/index.md)

- **Messenger is up-weighted** — know buses vs transports vs middleware vs stamps,
  the **retry + failure transport** flow, and the **worker** lifecycle
  (`messenger:consume`).
- **`sync` transport handles messages immediately** in-process; async needs a
  running worker.
- **Symfony Contracts `CacheInterface::get()`** uses a callback (stampede
  protection) — different from raw PSR-6 `getItem()`/`save()`.
- Serializer: **normalizer** (object ↔ array) vs **encoder** (array ↔ string) are
  distinct stages.

## PHP & Web Security → [area](../php-web-security/index.md)

- **`readonly` properties** can be initialized once (typically in the constructor);
  reassigning throws.
- **`#[\Override]` (8.3)** fails at compile time if the method overrides nothing.
- **Prepared statements stop SQLi; escaping stops XSS** — don't mix the mitigations.

---

<small>Related: [Master Cheat Sheet](cheat-sheet.md) · [Memory Aids](memory-aids.md) · [Exam-Day Strategy](../exam-guide/strategy.md)</small>

## Official References

- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/current/)

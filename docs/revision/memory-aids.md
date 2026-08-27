# Memory Aids

Mnemonics and memory devices for the **orderings and enumerations** the exam
expects you to recall cold. Facts in isolation decay; a hook makes them stick.

!!! abstract "How to use these"
    Learn the underlying mechanism first (in the topic chapters), then use these
    hooks to lock the *order* and *set membership* in memory. Verify against the
    [Master Cheat Sheet](cheat-sheet.md).

## Kernel event order

`kernel.request` → `kernel.controller` → `kernel.controller_arguments` →
*(`kernel.view`)* → `kernel.response` → `kernel.finish_request` → `kernel.terminate`.

!!! tip "Mnemonic: **R-C-A-V-R-F-T**"
    "**R**eally **C**ool **A**pps **V**alidate **R**esponses, **F**inish,
    **T**erminate."

    - **V**iew is in brackets — it **only fires if the controller returns a
      non-`Response`**.
    - **Terminate** runs **after** the response is sent (`kernel.terminate`).
    - **Exception** is out-of-band: it fires whenever something throws.

## HTTP status classes

`1xx info · 2xx success · 3xx redirect · 4xx client error · 5xx server error`.

!!! tip "Hook"
    "**1** Information, **2** it worked, **3** go elsewhere, **4** you messed up,
    **5** we messed up."

    - **304** Not Modified = the cache validation win.
    - **401** = *unauthenticated* (who are you?); **403** = *unauthorized*
      (you're known, but not allowed). "401 before 403."

## Safe vs idempotent methods

- **Safe** (no state change): **GET, HEAD, OPTIONS, TRACE**.
- **Idempotent** (repeatable, same effect): safe methods **+ PUT, DELETE**.
- **Neither:** **POST, PATCH**.

!!! tip "Hook"
    "**POST creates, PUT replaces** — replacing twice is the same, posting twice is
    two." (PUT idempotent, POST not.)

## Cache-Control directives

!!! tip "The two that flip people"
    - **`no-cache`** = *store but revalidate before every use* (NOT "don't cache").
    - **`no-store`** = *never write it down*.
    - **`max-age`** = browser lifetime; **`s-maxage`** = **s**hared/proxy lifetime
      (the "s" is for shared).

    "**no-cache** asks first; **no-store** forgets."

## Cache: expiration vs validation

- **Expiration** = time-based: `Expires`, `Cache-Control: max-age`/`s-maxage`.
- **Validation** = content-based: `ETag` ↔ `If-None-Match`, `Last-Modified` ↔
  `If-Modified-Since`, answered with **304**.

!!! tip "Hook"
    "**E**xpiration = **E**gg timer; **V**alidation = **V**erify with a fingerprint
    (ETag)."

## Security passport badges

`UserBadge · PasswordCredentials · CsrfTokenBadge · RememberMeBadge ·
PasswordUpgradeBadge · PreAuthenticatedUserBadge`.

!!! tip "Mnemonic: **U-P-C-R-P-P**"
    "**U**sers **P**resent **C**redentials, **R**emember, then **P**assword-upgrade
    or **P**re-auth."

    - **`UserBadge`** is the only always-required one (identifies the user).
    - `CsrfTokenBadge` + `RememberMeBadge` are opt-in behaviours.

## Access-decision strategies

`affirmative (default) · consensus · unanimous · priority`.

!!! tip "Hook"
    "**A**ny grants (affirmative), **most** wins (consensus), **all** must agree
    (unanimous), **first** to speak (priority)." **Default = affirmative.**

## Console verbosity ladder

`-q quiet (16) · normal (32) · -v verbose (64) · -vv very-verbose (128) ·
-vvv debug (256)`.

!!! tip "Hook"
    Count the **v**'s: **1 v = verbose, 2 = very, 3 = debug**. Values **double** each
    step (16→32→64→128→256).

## Console event order

`console.command` → *(run)* → `console.error` (on throw) → `console.terminate`
(always). `console.signal` on OS signals.

!!! tip "Hook"
    "**Command** starts, **Error** if it breaks, **Terminate** always ends." (Mirror
    of the kernel's terminate-always rule.)

## Form event order

`PRE_SET_DATA` → `POST_SET_DATA` → `PRE_SUBMIT` → `SUBMIT` → `POST_SUBMIT`.

!!! tip "Hook"
    Two phases: **SET** (populate the form from model) then **SUBMIT** (map request
    into model). "**Set before Submit; Pre before Post.**" `PRE_SUBMIT` = raw
    request data; `SUBMIT` = normalized.

## Data transformer direction

- **Display:** model → normalized → **view** (string in the input).
- **Submit:** view → normalized → **model**.

!!! tip "Hook"
    "**Out to the eye, back to the model.**" (View going out, model coming in.)

## URL reference types

`ABSOLUTE_URL · ABSOLUTE_PATH (default) · RELATIVE_PATH · NETWORK_PATH`.

!!! tip "Hook"
    Default is **ABSOLUTE_PATH** (`/blog/1`). "URL = full `https://…`; PATH = from
    root `/…`."

## IS_AUTHENTICATED ladder

`PUBLIC_ACCESS < IS_AUTHENTICATED_LAZILY < _REMEMBERED < _FULLY`.

!!! tip "Hook"
    "**Public → Lazy → Remembered → Fully.**" Sensitive actions demand **FULLY**;
    remember-me only reaches **REMEMBERED**.

---

<small>Related: [Master Cheat Sheet](cheat-sheet.md) · [Top Certification Traps](traps.md) · [Revision Hub](index.md)</small>

## Official References

- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)

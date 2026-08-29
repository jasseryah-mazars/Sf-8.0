# Handling Deprecated Code in Tests

!!! tip "In a nutshell"
    The PHPUnit bridge collects triggered deprecations and can fail the build,
    sorting each into a self / direct / indirect / legacy bucket. Exam hook:
    `#[IgnoreDeprecations]` (not the removed `@group legacy`) silences a test, and
    `max[self]=0` fails only on *your own* code.

!!! example "Real-world analogy"
    Picture a building inspector walking your property and writing up code violations, each
    tagged by who is responsible. Some are things *you* built wrong (**self**); some come
    from a contractor *you hired directly* (**direct**); some are buried deep in a
    sub-contractor's work your contractor subbed out (**indirect**). You set the policy for
    when the sale falls through: fail on *anything* (`max[total]=0`) or only on your own
    workmanship (`max[self]=0`), tolerating what others must fix. A baseline is the
    grandfather clause — a signed list of already-known issues that won't block the sale, so
    only *new* violations do.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Explain the `self` / `direct` / `indirect` / `legacy` deprecation buckets
    - [ ] Configure the helper modes: `max[...]`, `disabled`, `weak`
    - [ ] Silence expected deprecations with `#[IgnoreDeprecations]`
    - [ ] Assert an expected deprecation and use a baseline for legacy debt

    **Syllabus:** `Automated Tests → Handling deprecated code` ·
    **Level:** Expert ·

    **Est. time:** 25 min ·
    **Prerequisites:** [PHPUnit Bridge](../appendices/out-of-syllabus/phpunit-bridge.md)
    **Examen Symfony 8 :** OUI
---

## Pour les nuls

### L'idée en une phrase
Le PHPUnit bridge classe chaque dépréciation déclenchée selon qui en est responsable — ton propre code, une dépendance directe, ou une dépendance de dépendance.

### Imagine dans la vraie vie
Un inspecteur du bâtiment relève des infractions au code, chacune étiquetée selon le responsable. Certaines, c'est *toi* qui les as mal construites (**self**) ; certaines viennent d'un entrepreneur *que tu as engagé directement* (**direct**) ; certaines sont enterrées profondément dans le travail d'un sous-traitant (**indirect**).

### Dans Symfony
Configurer `max[self]=0` fait échouer le build seulement si **ton propre code** déclenche une dépréciation — les dépréciations venant de bibliothèques tierces (que tu ne contrôles pas) sont tolérées jusqu'à ce que tu puisses les mettre à jour.

### Exemple simple
```php
#[IgnoreDeprecations]
public function testAncienneApi(): void { /* teste volontairement du code déprécié */ }
```

### Comment le mémoriser 🧠
`#[IgnoreDeprecations]` remplace l'ancien `@group legacy` **supprimé** — ne cherche jamais cette annotation dans du code Symfony 8, elle n'existe plus.

---

## Theory

Symfony signals API removals ahead of time by triggering `E_USER_DEPRECATED` via
`trigger_deprecation()`. In tests, the [PHPUnit bridge](../appendices/out-of-syllabus/phpunit-bridge.md)
**collects** these and can **fail the build** so upgrades never surprise you. The
skill is telling *your* deprecations (which you must fix) from *third-party* ones
(which you tolerate until they release a fix), and quieting the ones you
deliberately keep testing.

```php
// Library code signals a future removal:
trigger_deprecation(
    'acme/blog',                        // package
    '2.4',                              // version that deprecated it
    'Method "%s()" is deprecated.',     // message (sprintf-style)
    'old',
);

// ...which internally triggers a silenced E_USER_DEPRECATED error:
@trigger_error(
    'Since acme/blog 2.4: Method "old()" is deprecated.',
    \E_USER_DEPRECATED,
);
```

!!! question "Predict first"
    Your CI runs with `max[self]=0`. A vendor library triggers a deprecation deep
    inside its own internals. Does the build go red?

??? note "Reveal"
    No — that is an **indirect** deprecation, and `max[self]=0` counts only your
    own code (`self`). It is reported but does not fail. Only a `self` deprecation
    (or a broader `max[total]=0`) would break the build.

## Deep Dive — how it works internally

The `DeprecationErrorHandler` classifies each deprecation by inspecting the call
stack:

| Bucket | Meaning |
|---|---|
| **self** | Triggered by *your own* code (your namespace) |
| **direct** | Triggered by a dependency you called **directly** |
| **indirect** | Triggered deep inside a dependency's own internals |
| **legacy** | From tests marked legacy (see below) — never counted against thresholds |

At the end of the run the handler prints per-bucket counts and compares them with
the thresholds in `SYMFONY_DEPRECATIONS_HELPER` (`max[self]`, `max[direct]`, etc.).
Exceeding any non-`legacy` threshold fails the suite with a non-zero exit code.

```console
$ # One threshold per bucket in SYMFONY_DEPRECATIONS_HELPER;
$ # exceeding any non-legacy one fails the run
$ SYMFONY_DEPRECATIONS_HELPER='max[self]=0&max[direct]=3&max[indirect]=999' \
    php bin/phpunit

$ # e.g. 1 self deprecation > max[self]=0 -> non-zero exit code
$ echo $?
1
```

### Marking and asserting deprecations

- `#[IgnoreDeprecations]` (`Symfony\Bridge\PhpUnit\Attribute\IgnoreDeprecations`)
  on a test method/class tells the handler to **ignore** deprecations from that
  test — the modern replacement for the old `@group legacy` docblock.
- `ExpectUserDeprecationMessageTrait` and its `expectUserDeprecationMessage()`
  helper let a test **assert** that a specific deprecation message is emitted
  (useful when *you* add a `trigger_deprecation()` and want to prove it fires). The
  old `ExpectDeprecationTrait::expectDeprecation()` was removed in Symfony 7.0.

```php
use Symfony\Bridge\PhpUnit\Attribute\IgnoreDeprecations;
use Symfony\Bridge\PhpUnit\ExpectUserDeprecationMessageTrait;

final class LegacyPathTest extends TestCase
{
    use ExpectUserDeprecationMessageTrait;

    #[IgnoreDeprecations]   // handler skips this test's deprecations
    public function testDeprecatedPathStillWorks(): void
    {
        // exercising deprecated code here cannot fail the build
    }

    public function testEmitsDeprecation(): void
    {
        // asserts the message emitted by trigger_deprecation()
        // (the old ExpectDeprecationTrait::expectDeprecation() is gone)
        $this->expectUserDeprecationMessage('Since app 2.0: "foo()" is deprecated.');

        trigger_deprecation('app', '2.0', '"foo()" is deprecated.');
    }
}
```

```mermaid
flowchart TD
    A["trigger_deprecation()"] --> B[DeprecationErrorHandler]
    B --> C{classify by stack}
    C -->|self| D[count vs max_self]
    C -->|direct| E[count vs max_direct]
    C -->|indirect| F[count vs max_indirect]
    C -->|legacy / ignored| G[excluded]
    D & E & F --> H{over threshold?}
    H -->|yes| I[fail build]
```

!!! note "Source reference"
    Classification and thresholds live in
    `Symfony\Bridge\PhpUnit\DeprecationErrorHandler` and its `Configuration`
    ([symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/PhpUnit/DeprecationErrorHandler/Configuration.php)).

### Baselines

For a legacy codebase drowning in deprecations, record a **baseline**: a JSON file
of currently-known deprecations that are then ignored, so the build only fails on
*new* ones. Generate it once, commit it, and reduce it over time.

For the framework's own deprecation *authoring* rules (how and when to call
`trigger_deprecation()`, the BC promise), see
[Architecture → Deprecations Best Practices](../architecture/deprecations.md).

## Configuration & code

=== "Helper modes"

    ```console
    $ # Fail on ANY deprecation (strictest)
    $ SYMFONY_DEPRECATIONS_HELPER='max[total]=0' php bin/phpunit

    $ # Fail only on YOUR code's deprecations; tolerate dependencies
    $ SYMFONY_DEPRECATIONS_HELPER='max[self]=0' php bin/phpunit

    $ # Report but never fail
    $ SYMFONY_DEPRECATIONS_HELPER=weak php bin/phpunit

    $ # Turn collection off entirely
    $ SYMFONY_DEPRECATIONS_HELPER=disabled=1 php bin/phpunit
    ```

=== "Ignore + assert"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Tests\Legacy;

    use App\Legacy\OldService;
    use PHPUnit\Framework\TestCase;
    use Symfony\Bridge\PhpUnit\Attribute\IgnoreDeprecations;
    use Symfony\Bridge\PhpUnit\ExpectUserDeprecationMessageTrait;

    final class OldServiceTest extends TestCase
    {
        use ExpectUserDeprecationMessageTrait;

        #[IgnoreDeprecations]                 // this test may exercise deprecated paths
        public function testStillWorks(): void
        {
            self::assertSame('ok', (new OldService())->run());
        }

        public function testEmitsDeprecation(): void
        {
            $this->expectUserDeprecationMessage(
                'Since app 2.0: Using OldService::legacy() is deprecated.',
            );

            (new OldService())->legacy();     // must trigger that exact deprecation
        }
    }
    ```

=== "Baseline"

    ```console
    $ # 1) Generate the baseline of current deprecations
    $ SYMFONY_DEPRECATIONS_HELPER='baselineFile=./tests/baseline.json&generateBaseline=true' \
        php bin/phpunit

    $ # 2) Subsequent runs ignore baselined deprecations, fail on new ones
    $ SYMFONY_DEPRECATIONS_HELPER='baselineFile=./tests/baseline.json' php bin/phpunit
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Keep `max[self]=0` — your code stays clean | `disabled=1` masking your own debt |
| Use a baseline for large legacy suites | Blanket `#[IgnoreDeprecations]` everywhere |
| `expectUserDeprecationMessage()` for your own triggers | Asserting on message text with `assertStringContains` |
| Shrink the baseline over time | Regenerating the baseline on every failure |

## When (not) to use it / alternatives

Run **strict** (`max[self]=0` at minimum) on your own code — it is free upgrade
insurance. Tolerate `indirect` deprecations you can't fix (pin `max[indirect]`
higher or use a baseline). Use `weak` only in transitional CI where you want
visibility without a red build; never ship `disabled=1` as the permanent state.

!!! danger "Certification traps"
    - `self` = **your** code, `direct` = a dependency **you call**, `indirect` =
      deep inside a dependency. Getting these swapped is a classic exam trip.
    - `#[IgnoreDeprecations]` replaces the old `@group legacy` for silencing a
      test's deprecations.
    - `weak` still **reports**; only `disabled=1` stops collection.
    - `max[total]=0` fails on *any* bucket; `max[self]=0` is narrower.

!!! warning "Common mistakes"
    - Adding `#[IgnoreDeprecations]` to hide a deprecation you *should* fix.
    - Forgetting the bridge/extension must be active for any of this to work.

## Exercises

1. **(Basic)** Configure CI to fail only when *your* code triggers a deprecation,
   tolerating dependency deprecations.
2. **(Intermediate)** Write a test that asserts calling a deprecated method emits
   the expected `trigger_deprecation()` message.

??? success "Solutions"

    **1.**

    ```console
    $ SYMFONY_DEPRECATIONS_HELPER='max[self]=0' php bin/phpunit
    ```

    `self` counts only your namespace; `direct`/`indirect` deprecations are
    reported but do not fail the build.

    **2.**

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Tests\Legacy;

    use App\Legacy\Registry;
    use PHPUnit\Framework\TestCase;
    use Symfony\Bridge\PhpUnit\ExpectUserDeprecationMessageTrait;

    final class RegistryTest extends TestCase
    {
        use ExpectUserDeprecationMessageTrait;

        public function testDeprecatedAlias(): void
        {
            $this->expectUserDeprecationMessage(
                'Since app 3.0: "Registry::add()" is deprecated, use "set()".',
            );

            (new Registry())->add('k', 'v');
        }
    }
    ```

## Certification questions

*Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.*

??? question "Q1. A deprecation triggered inside a vendor library's own internals is bucketed as…"
    - [ ] A. self
    - [ ] B. direct
    - [x] C. indirect ✅
    - [ ] D. legacy

    **Why:** `indirect` = triggered deep inside a dependency, not by your direct
    call. **Ref:** [PHPUnit bridge](https://symfony.com/doc/8.0/components/phpunit_bridge.html#making-tests-fail).

??? question "Q2. Which value reports deprecations but never fails the build?"
    - [x] A. `weak` ✅
    - [ ] B. `disabled=1`
    - [ ] C. `max[total]=0`
    - [ ] D. `strict`

    **Why:** `weak` collects and prints without enforcing thresholds; `disabled`
    stops collection. **Ref:** [PHPUnit bridge](https://symfony.com/doc/8.0/components/phpunit_bridge.html#configuration).

??? question "Q3. The modern way to silence a single test's expected deprecations is…"
    - [x] A. `#[IgnoreDeprecations]` ✅
    - [ ] B. `@group legacy` (removed)
    - [ ] C. `error_reporting(0)`
    - [ ] D. `SYMFONY_DEPRECATIONS_HELPER=disabled`

    **Why:** the `IgnoreDeprecations` attribute is the current replacement for the
    legacy group. **Ref:** [PHPUnit bridge](https://symfony.com/doc/8.0/components/phpunit_bridge.html).

??? question "Q4. `max[self]=0` fails the build when…"
    - [x] A. Your own code triggers any deprecation ✅
    - [ ] B. Any dependency triggers a deprecation
    - [ ] C. Any deprecation from anywhere occurs
    - [ ] D. A test is marked legacy

    **Why:** `self` counts only deprecations originating in your code.
    **Ref:** [PHPUnit bridge](https://symfony.com/doc/8.0/components/phpunit_bridge.html#making-tests-fail).

## Key takeaways

- Buckets: **self** (you) · **direct** (dep you call) · **indirect** (dep
  internals) · **legacy** (excluded).
- Modes: `max[self|direct|indirect|total]=n`, `weak` (report only),
  `disabled=1` (off), baseline (ignore known).
- `#[IgnoreDeprecations]` silences a test; `expectUserDeprecationMessage()`
  asserts one.
- Keep `max[self]=0`; use a baseline to burn down legacy debt.

## Last-minute revision

!!! tip "Cheat sheet"
    - Env var: `SYMFONY_DEPRECATIONS_HELPER`.
    - `max[total]=0` (any) · `max[self]=0` (yours) · `weak` · `disabled=1`.
    - Baseline: `baselineFile=…&generateBaseline=true`, then `baselineFile=…`.
    - Attributes/traits: `#[IgnoreDeprecations]`, `ExpectUserDeprecationMessageTrait`.

## Connections

- **Depends on:** [PHPUnit Bridge](../appendices/out-of-syllabus/phpunit-bridge.md) — the bridge's `DeprecationErrorHandler` does the bucketing and gating.
- **Reused in:** [Architecture — Deprecations](../architecture/deprecations.md) — the framework's own rules for *authoring* deprecations.
- **Confused with:** [Unit Tests](unit-tests.md) — asserting a deprecation message differs from asserting a return value.

## Official References
- [Official Symfony docs — PHPUnit bridge deprecations](https://symfony.com/doc/8.0/components/phpunit_bridge.html#making-tests-fail)
- [Symfony source — DeprecationErrorHandler Configuration](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/PhpUnit/DeprecationErrorHandler/Configuration.php)
- [Architecture — Deprecations Best Practices](../architecture/deprecations.md)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony testing" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/components/phpunit_bridge.html#making-tests-fail) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** failing on deprecations is free upgrade insurance
- [ ] configure `max[self|direct|indirect|total]`, `weak`, `disabled`, and a baseline
- [ ] debug why a deprecation is bucketed `indirect` instead of `self`
- [ ] spot the trap that `#[IgnoreDeprecations]` replaced `@group legacy`
- [ ] explain how the handler classifies a deprecation by its call stack

---

<small>Related: [PHPUnit Bridge](../appendices/out-of-syllabus/phpunit-bridge.md) · [Architecture — Deprecations](../architecture/deprecations.md) · [Unit Tests](unit-tests.md)</small>

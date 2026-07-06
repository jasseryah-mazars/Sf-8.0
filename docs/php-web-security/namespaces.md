# Namespaces & Autoloading

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Explain PHP's name-resolution rules (qualified, unqualified, fully qualified).
    - [ ] Configure and reason about **PSR-4** autoloading via Composer.
    - [ ] Use `use`, aliasing, and grouped imports correctly.

    **Syllabus:** `PHP → Namespaces` ·
    **Level:** Advanced ·
    **Est. time:** 25 min ·
    **Prerequisites:** [OOP](oop.md)

---

## Theory

A **namespace** is a hierarchical label (`App\Service\Mailer`) that prevents
name collisions. PHP resolves names using rules that depend on whether a name is
**unqualified** (`Mailer`), **qualified** (`Service\Mailer`) or **fully
qualified** (`\App\Service\Mailer`). **Autoloading** turns a class name into a
file path so you never write `require`.

| Form | Example | Resolution |
|---|---|---|
| Fully qualified | `\App\Foo` | Absolute, from global root |
| Qualified | `Service\Foo` | Relative to current namespace (or a `use`) |
| Unqualified | `Foo` | Current namespace, then a matching `use` |

## Deep Dive — how it works internally

### Name resolution rules

1. `declare(strict_types=1)` and `namespace` must be the **first** statements.
2. **Fully qualified** names (leading `\`) are used verbatim.
3. For **classes/interfaces/traits**, unqualified and qualified names resolve
   against `use` imports first, then the current namespace.
4. For **functions and constants**, an unqualified call first tries the current
   namespace, then **falls back to the global namespace** — this fallback exists
   only for functions/constants, not classes. That is why `\strlen()` inside a
   namespace still works, and why a leading `\` micro-optimises the lookup.

```php
<?php
declare(strict_types=1);

namespace App\Service;

use App\Contract\MailerInterface;
use App\Contract\Transport as Tx;   // alias
use function App\Support\slugify;   // function import
use const App\Support\VERSION;      // const import

final class Mailer implements MailerInterface
{
    public function send(Tx $t): void
    {
        $count = \count($t->messages);  // leading \ = global function
        echo slugify(VERSION);
    }
}
```

### PSR-4 autoloading

PSR-4 maps a **namespace prefix** to a **base directory**. The autoloader
strips the prefix, replaces `\` with `/`, and appends `.php`.

```json
{
    "autoload": {
        "psr-4": { "App\\": "src/" }
    }
}
```

`App\Service\Mailer` → `src/Service/Mailer.php`. Composer generates
`vendor/autoload.php`, which registers the loader via `spl_autoload_register()`.

```mermaid
flowchart LR
    A["new App\\Service\\Mailer()"] --> B[Class not loaded]
    B --> C[spl_autoload_register callback]
    C --> D[PSR-4 prefix map: App\\ → src/]
    D --> E[require src/Service/Mailer.php]
```

For production, `composer dump-autoload --optimize` (or `--classmap-authoritative`)
builds a static classmap so no filesystem stat per class is needed.

!!! note "Source reference"
    Composer's loader implements PSR-4; Symfony's `MicroKernelTrait` and
    autoconfiguration rely on it —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Kernel/MicroKernelTrait.php).

## Configuration & code

=== "Grouped use"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use App\Service\{Mailer, Reporter, Clock};   // grouped import
    use function array_map;
    ```

=== "Console"

    ```console
    $ composer dump-autoload --optimize
    Generating optimized autoload files
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| One class per file, path = namespace | Multiple classes per file |
| `use` at top, alias on collision | Long inline FQCNs everywhere |
| `\` prefix on hot global functions | Redefining SPL/global names |
| `--optimize` autoload in prod | Shipping dev autoloader |

## When (not) to use it / alternatives

- Always namespace application code; only a tiny script or a global polyfill
  belongs in the global namespace.
- Use aliasing when two imports share a short name; do not alias for style alone.

!!! danger "Certification traps"
    - Function/constant calls **fall back to global**; class names do **not**.
      `new DateTime()` inside a namespace fails unless imported or `\`-prefixed.
    - `use` imports **do not** load a file — they are compile-time aliases only.
    - `namespace` and `declare` must precede any other statement (no output before).
    - PSR-4 is **case-sensitive** on the class-to-path mapping on Linux.

!!! warning "Common mistakes"
    - Writing `\App\...` with a leading slash inside a `use` (invalid — `use`
      is always absolute already).
    - Assuming `use App\Foo;` also imports `App\Foo\Bar` (it imports only `Foo`).

## Exercises

1. **(Advanced)** Given `namespace App;` and a call to `strlen()`, explain why it
   works without a `use`.
2. **(Advanced)** Map `App\Repository\UserRepository` to a file path under a
   `"App\\": "src/"` PSR-4 rule.

??? success "Solutions"

    **1.** `strlen` is a function; unqualified function calls fall back to the
    global namespace when no `App\strlen` exists. Adding `\strlen()` skips the
    lookup and is marginally faster.

    **2.** `src/Repository/UserRepository.php` — strip the `App\` prefix, replace
    `\` with `/`, append `.php`.

## Certification questions

??? question "Q1. Inside `namespace App;`, an unqualified call `count($x)` resolves to…"
    - [x] A. `App\count` if defined, else global `\count` ✅
    - [ ] B. Always `App\count`
    - [ ] C. A fatal error
    - [ ] D. `\count` only

    **Why:** Functions fall back to the global namespace. **Ref:** [Namespace resolution](https://www.php.net/manual/en/language.namespaces.rules.php).

??? question "Q2. What does `use App\Service\Mailer;` do?"
    - [ ] A. Loads the file immediately
    - [x] B. Creates a compile-time alias so `Mailer` means the FQCN ✅
    - [ ] C. Instantiates the class
    - [ ] D. Registers an autoloader

    **Why:** `use` is a pure alias; loading happens later via the autoloader.
    **Ref:** [Using namespaces](https://www.php.net/manual/en/language.namespaces.importing.php).

??? question "Q3. Under PSR-4 `\"App\\\\\": \"src/\"`, where does `App\\Foo\\Bar` live?"
    - [ ] A. `src/App/Foo/Bar.php`
    - [x] B. `src/Foo/Bar.php` ✅
    - [ ] C. `src/foo/bar.php`
    - [ ] D. `App/Foo/Bar.php`

    **Why:** The prefix `App\` maps to `src/`, so only the remainder becomes the path.
    **Ref:** [PSR-4](https://www.php-fig.org/psr/psr-4/).

??? question "Q4. Inside `namespace App;`, which correctly references the global `DateTime`?"
    - [ ] A. `new DateTime()`
    - [x] B. `new \DateTime()` ✅
    - [ ] C. `new App\DateTime()`
    - [ ] D. `new DateTime\Global()`

    **Why:** Class names do not fall back to global, so a leading `\` (or a `use`)
    is required. **Ref:** [Namespace resolution](https://www.php.net/manual/en/language.namespaces.rules.php).

## Key takeaways

- Functions/constants fall back to global; **classes do not**.
- `use` is a compile-time alias, not a file load.
- PSR-4 maps prefix → base dir; strip prefix, `\`→`/`, add `.php`.
- `composer dump-autoload --optimize` for production.

## Last-minute revision

!!! tip "Cheat sheet"
    - `namespace` + `declare` first; nothing before them.
    - `\Foo` = fully qualified; `Foo` = current ns (class) or global (function).
    - Grouped: `use App\{A, B, C};` · function: `use function`; const: `use const`.
    - PSR-4: `App\ → src/`, case-sensitive on Linux.

## Official References
- [PHP: Namespaces](https://www.php.net/manual/en/language.namespaces.php)
- [PHP: Name resolution rules](https://www.php.net/manual/en/language.namespaces.rules.php)
- [PSR-4 Autoloader](https://www.php-fig.org/psr/psr-4/)
- [Symfony source — MicroKernelTrait](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Kernel/MicroKernelTrait.php)

---

<small>Related: [OOP](oop.md) · [Interfaces](interfaces.md) · [PHP API](php-api.md)</small>

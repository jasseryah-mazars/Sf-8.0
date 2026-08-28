# Namespaces & Autoloading

!!! tip "In a nutshell"
    Namespaces prevent name clashes; PSR-4 maps a prefix to a directory so
    Composer autoloads classes. The trap: unqualified **function/constant** calls
    fall back to the global namespace, but **class names do not**.

!!! example "Real-world analogy"
    A namespace is like a full postal address: two people both named "John Smith" are
    told apart by street and city, just as `App\Service\Mailer` never clashes with
    another `Mailer` elsewhere. PSR-4 is the filing rule that maps a department name to
    a physical drawer, so the clerk (the autoloader) finds the right folder without you
    ever quoting the exact path. The fallback quirk: everyday words — like calling a
    shared helpline (`strlen`) — resort to the town's central directory if there is no
    local entry, but a *proper name* like `DateTime` never does; you must give its full
    address.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Explain PHP's name-resolution rules (qualified, unqualified, fully qualified).
    - [ ] Configure and reason about **PSR-4** autoloading via Composer.
    - [ ] Use `use`, aliasing, and grouped imports correctly.

    **Syllabus:** `PHP → Namespaces` ·
    **Level:** Advanced ·
    **Est. time:** 25 min ·
    **Prerequisites:** [OOP](oop.md)

!!! quote "🎯 Examen Symfony 8 : NON"
    Ce chapitre n'est **pas** sur la liste officielle des 9 sous-sujets PHP du
    syllabus (voir [PHP & Web Security](index.md)) — il est conservé comme
    contenu d'enrichissement/prérequis. Il ne sera pas noté comme tel à
    l'examen, mais comprendre l'autoloading aide à lire tout code Symfony.

---

## Pour les nuls

### L'idée en une phrase
Un namespace, c'est une adresse postale complète pour une classe — elle évite que deux classes portant le même nom se marchent dessus.

### Imagine dans la vraie vie
Deux personnes s'appellent "Jean Dupont" dans la même ville : on les distingue par leur rue et leur numéro. `App\Service\Mailer` et `Vendor\Lib\Mailer` sont deux "Jean Dupont" différents — leur adresse complète (le namespace) lève toute ambiguïté, et le facteur (l'autoloader) sait dans quel casier chercher.

### Dans Symfony
Composer utilise PSR-4 pour faire correspondre `App\` au dossier `src/` : quand Symfony a besoin de `App\Controller\HomeController`, l'autoloader sait immédiatement dans quel fichier chercher, sans qu'aucun `require` manuel ne soit écrit.

### Exemple simple
```php
namespace App\Service;

class Mailer {} // adresse complète : App\Service\Mailer
```

### Comment le mémoriser 🧠
Une fonction non qualifiée sans équivalent local **retombe** dans l'espace global (comme un appel à une hotline nationale faute de service local) — mais un **nom de classe**, lui, ne retombe jamais : il doit toujours porter son adresse complète.

## Theory

A **namespace** is a hierarchical label (`App\Service\Mailer`) that prevents
name collisions. PHP resolves names using rules that depend on whether a name is
**unqualified** (`Mailer`), **qualified** (`Service\Mailer`) or **fully
qualified** (`\App\Service\Mailer`). **Autoloading** turns a class name into a
file path so you never write `require`.

```php
namespace App\Controller;

use App\Service\Mailer;      // import once at the top

new \App\Service\Mailer();   // fully qualified — absolute from the root
new Service\Mailer();        // qualified — App\Controller\Service\Mailer !
new Mailer();                // unqualified — resolved via the use import
```

| Form | Example | Resolution |
|---|---|---|
| Fully qualified | `\App\Foo` | Absolute, from global root |
| Qualified | `Service\Foo` | Relative to current namespace (or a `use`) |
| Unqualified | `Foo` | Current namespace, then a matching `use` |

!!! question "Predict first"
    Inside `namespace App;`, `strlen($s)` works without a `use`, but
    `new DateTime()` fails. Why the difference?

??? note "Reveal"
    Unqualified **function/constant** calls fall back to the global namespace;
    **class names do not**. So `strlen` resolves to `\strlen`, but `DateTime`
    means `App\DateTime` unless you write `\DateTime` or import it.

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

## Connections

- **Depends on:** [OOP](oop.md) — namespaces organise the classes/interfaces you define.
- **Reused in:** [Extensions](extensions.md) — the same `composer.json` declares `ext-*` beside PSR-4; [Interfaces](interfaces.md) type-hints imported FQCNs.
- **Confused with:** [Traits](traits.md) — file-level `use Some\Class;` (import) vs class-body `use TraitName;` (trait inclusion).

## Continue your learning

1. **[Guided exercises](namespaces-exercises.md)** — resolve every name kind by hand, then watch the global fallback fire and not fire.
2. **[Topic exam](namespaces-exam.md)** — every certification question for this topic, answers hidden.
3. **[Flashcards](namespaces-flashcards.md)** — active recall on resolution rules, `use` semantics, PSR-4 and the autoloading boundary.

## Official References
- [PHP: Namespaces](https://www.php.net/manual/en/language.namespaces.php)
- [PHP: Name resolution rules](https://www.php.net/manual/en/language.namespaces.rules.php)
- [PSR-4 Autoloader](https://www.php-fig.org/psr/psr-4/)
- [Symfony source — MicroKernelTrait](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Kernel/MicroKernelTrait.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "PHP & web security" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/index.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** functions fall back to global but classes do not
- [ ] configure PSR-4 and `dump-autoload --optimize` for a Symfony 8 app
- [ ] debug a "class not found" from a missing `\` or `use` inside a namespace
- [ ] spot the trick: `use` claimed to load a file (it only aliases) or a leading `\` in a `use`
- [ ] explain how PSR-4 maps a prefix to a path (strip prefix, `\`→`/`, add `.php`)

---

<small>Related: [OOP](oop.md) · [Interfaces](interfaces.md) · [PHP API](php-api.md)</small>

# Attributes

!!! tip "In a nutshell"
    An attribute (`#[...]`) is structured, compile-time metadata attached to a
    class, method, property, parameter, function or class constant. It does
    **nothing by itself** — reading it is opt-in via Reflection
    (`getAttributes()`), and instantiating it (`newInstance()`) is what
    actually runs its constructor. Symfony's `#[Route]`, `#[AsCommand]` and
    friends are ordinary attribute classes consumed this way.

!!! example "Real-world analogy"
    An attribute is a sticky note pinned to a form field — "must be reviewed
    by Legal". The note changes nothing about how the form is filled in; it
    only matters if *someone reads the notes* (`getAttributes()`) and then
    *acts on one* (`newInstance()`). A form with no one checking its notes
    behaves exactly like one with no notes at all.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Declare a custom attribute class and restrict its allowed targets.
    - [ ] Read attributes back with `ReflectionClass::getAttributes()` and
          understand *when* the attribute class is actually instantiated.
    - [ ] Explain how Symfony attributes such as `#[Route]` are just
          Reflection-read metadata, not magic.

    **Syllabus:** `PHP → Attributes` ·
    **Level:** Advanced / Expert ·
    **Est. time:** 25 min ·
    **Prerequisites:** [OOP](oop.md), [Interfaces](interfaces.md)

    **Examen Symfony 8 :** OUI

---

## Pour les nuls

### L'idée en une phrase
Un attribut `#[...]` est une étiquette collée sur du code — elle ne fait rien toute seule, il faut que quelqu'un la lise pour qu'elle serve à quelque chose.

### Imagine dans la vraie vie
Un post-it collé sur un dossier disant "à relire par le service juridique" ne déclenche rien par magie : il faut que le service juridique passe, lise le post-it, et agisse en fonction. Sans personne pour le lire, le dossier avec post-it se comporte exactement comme un dossier sans post-it.

### Dans Symfony
`#[Route('/produits')]` au-dessus d'une méthode de contrôleur ne "route" rien par lui-même : au démarrage, Symfony lit tous ces attributs via Reflection et construit sa table de routage à partir de ce qu'il a trouvé. L'attribut est passif ; c'est Symfony qui agit dessus.

### Exemple simple
```php
#[Route('/bonjour')]
public function bonjour(): Response { return new Response('Salut !'); }
// Symfony lit cet attribut au démarrage — la méthode elle-même ignore qu'il existe
```

### Comment le mémoriser 🧠
Un attribut, c'est une **étiquette muette** : elle ne parle que si quelqu'un (Symfony, via Reflection) la lit à voix haute.

## Theory

An **attribute** is metadata written as `#[AttributeName(args)]` directly
above a class, method, property, function, parameter, or (since PHP 8.3)
class constant. Unlike a docblock comment, it is **parsed into the compiled
opcode structure** — a real, typed, inspectable value — but by itself an
attribute changes **nothing** about how the code runs. It only has an effect
once something reads it back through the Reflection API.

```php
#[Route('/orders/{id}', name: 'order_show', methods: ['GET'])]
public function show(int $id): Response { /* ... */ }
```

Here `Route` is not special syntax: it is a plain PHP class. Symfony's router
reads it via Reflection when building the route collection; if nothing ever
called `getAttributes()` on this method, the `#[Route(...)]` line would be
inert text as far as PHP itself is concerned.

!!! question "Predict first"
    You put `#[LogCall]` on a method but never call `getAttributes()` anywhere
    in your code. Does `LogCall`'s constructor ever run?

??? note "Reveal"
    **No.** An attribute is only instantiated when something calls
    `newInstance()` on the `ReflectionAttribute` obtained from
    `getAttributes()`. Nothing runs automatically — attributes are inert
    metadata until a consumer opts in to reading them.

## Deep Dive — how it works internally

### Declaring an attribute class

Mark a class with the built-in `#[\Attribute]` attribute so PHP accepts it as
an attribute target. Its constructor takes an `int $flags` bitmask (default
`Attribute::TARGET_ALL`) built from these class constants:

| Constant | Meaning |
|---|---|
| `TARGET_CLASS` | Classes, interfaces, enums, traits |
| `TARGET_FUNCTION` | Named (non-method) functions |
| `TARGET_METHOD` | Class methods |
| `TARGET_PROPERTY` | Class properties |
| `TARGET_CLASS_CONSTANT` | Class constants (PHP 8.3+) |
| `TARGET_PARAMETER` | Function/method parameters |
| `TARGET_ALL` | All of the above (the default) |
| `IS_REPEATABLE` | Combine with a target flag to allow repeating it |

```php
<?php
declare(strict_types=1);

namespace App\Attribute;

#[\Attribute(\Attribute::TARGET_METHOD | \Attribute::IS_REPEATABLE)]
final class LogCall
{
    public function __construct(
        public readonly string $channel = 'app',
    ) {}
}
```

Using `LogCall` on a class or property is a compile-time `Error` (wrong
target); using it twice on the same method **without** `IS_REPEATABLE` is
also a fatal error — PHP rejects a duplicate non-repeatable attribute before
your code ever runs.

### Reading attributes back

Every reflector exposes the same shape:
`getAttributes(?string $name = null, int $flags = 0): array<ReflectionAttribute>`.
Filtering by `$name` with the `ReflectionAttribute::IS_INSTANCEOF` flag
matches subclasses too, not just an exact class match.

```php
$method = new \ReflectionMethod(OrderController::class, 'show');

foreach ($method->getAttributes(LogCall::class) as $attribute) {
    $attribute->getName();        // "App\Attribute\LogCall"
    $attribute->getArguments();   // ['channel' => 'orders'] or positional/named mix
    $attribute->getTarget();      // int bitmask, e.g. Attribute::TARGET_METHOD
    $attribute->isRepeated();     // true if the same attribute appears >1 time
    $instance = $attribute->newInstance(); // constructs it NOW — autoloads the class
}
```

`getAttributes()` never instantiates anything — it only exposes name,
arguments, and target as plain data. `newInstance()` is the one call that
triggers autoloading and runs the constructor. This laziness is why a class
can carry dozens of attributes from libraries it doesn't even use at
runtime: reading the list is free; only consumed attributes pay to
construct.

```mermaid
flowchart LR
    A["#[LogCall('orders')]<br/>on a method"] --> B["compiled as inert metadata"]
    B --> C["getAttributes(LogCall::class)"]
    C -->|"data only: name, args, target"| D["ReflectionAttribute"]
    D -->|"newInstance()"| E["LogCall object — class autoloaded now"]
```

### How Symfony consumes attributes

Symfony's own attributes are ordinary classes built the same way. `Route`
declares `#[\Attribute(\Attribute::IS_REPEATABLE | \Attribute::TARGET_CLASS
| \Attribute::TARGET_METHOD)]` — repeatable (a method can carry two
`#[Route]`s for two paths) and valid on both classes (a prefix) and methods.
The router's attribute loader walks controllers with `getAttributes(Route::class)`
and calls `newInstance()` to build each `Route` object; nothing is magic
beyond Reflection.

!!! note "Source reference"
    `Symfony\Component\Routing\Attribute\Route` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Attribute/Route.php).

### Built-in PHP attributes

PHP itself ships a handful of attribute classes you consume, not declare:

| Attribute | Since | Target | Purpose |
|---|---|---|---|
| `#[\Override]` | 8.3 | Method | Assert the method overrides a parent/interface one |
| `#[\SensitiveParameter]` | 8.2 | Parameter | Redact the argument from stack traces |
| `#[\AllowDynamicProperties]` | 8.2 | Class | Opt back into dynamic properties (deprecated by default) |
| `#[\ReturnTypeWillChange]` | 8.1 | Method | Silence a return-type-widening deprecation |
| `#[\Deprecated]` | 8.4 | Method/function/class constant | Declare a user-land deprecation (optional `message`, `since`) |

`#[\Override]` and PHP 8.4's typed-constant/property-hook features are
covered in [PHP API](php-api.md); this chapter is about the attribute
*mechanism* itself, which those features sit on top of.

### Null behavior

`getAttributes()` on a target with none returns an **empty array**, never
`null` — a plain `foreach` is always safe. Calling `newInstance()` on an
attribute whose class doesn't exist (or isn't autoloadable) throws an
`Error` at that call, not when the attribute was merely declared — the
failure is deferred all the way to the point of instantiation.

```php
foreach ($method->getAttributes(LogCall::class) as $attr) { /* runs 0+ times */ }
// no LogCall attributes -> getAttributes() returns [] -> loop body never runs

$attr->newInstance(); // Error thrown HERE if App\Attribute\LogCall can't autoload
                       // — not when the file containing #[LogCall] was parsed
```

!!! note "Null in real life"
    A sticky note nobody wrote is not a missing note — it is simply an empty
    list of notes to read. The only way to "fail" is to try to act on a note
    that turns out to reference something that doesn't exist.

## Configuration & code

=== "Declaring & reading"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Attribute;

    #[\Attribute(\Attribute::TARGET_METHOD | \Attribute::IS_REPEATABLE)]
    final class LogCall
    {
        public function __construct(
            public readonly string $channel = 'app',
        ) {}
    }
    ```

=== "Consumer"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Logging;

    use App\Attribute\LogCall;

    final class LogCallCompilerPass
    {
        /** @return LogCall[] */
        public function attributesOn(string $class, string $method): array
        {
            $reflection = new \ReflectionMethod($class, $method);

            return array_map(
                static fn (\ReflectionAttribute $a) => $a->newInstance(),
                $reflection->getAttributes(LogCall::class),
            );
        }
    }
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Restrict `TARGET_*` to what makes sense | Leaving the default `TARGET_ALL` on a method-only concept |
| Use `IS_REPEATABLE` when >1 instance is meaningful | Repeating a non-repeatable attribute (fatal error) |
| Read attributes once at compile/boot time | Calling `getAttributes()`/`newInstance()` on every request |
| Keep attribute constructors side-effect-free | Doing I/O in an attribute's `__construct()` |

## When (not) to use it / alternatives

Use an attribute for **declarative, structural metadata** read once (by a
compiler pass, a loader, or a framework) — routes, commands, service tags,
validation constraints. Prefer a plain interface or method when the
behavior must run on every call: an attribute only carries data, it is not
itself invoked.

!!! danger "Certification traps"
    - An attribute does **nothing** until something calls `getAttributes()`
      **and** `newInstance()` — declaring it alone has zero runtime effect.
    - `getAttributes()` returns *data* (name, arguments, target); only
      `newInstance()` constructs the object and autoloads its class.
    - Default target is `Attribute::TARGET_ALL`; omitting flags does **not**
      mean "no targets allowed."
    - Two non-repeatable attributes of the same class on one target is a
      fatal error, not a silent overwrite.
    - `ReflectionAttribute::IS_INSTANCEOF` matches subclasses of `$name`, not
      just an exact class match.

!!! warning "Common mistakes"
    - Expecting an attribute's constructor to run automatically at parse
      time — it runs only on explicit `newInstance()`.
    - Forgetting `IS_REPEATABLE` and being surprised by a fatal error the
      second time the attribute is used on the same target.

## Exercises

1. **(Advanced)** Declare a `#[Cacheable(ttl: 60)]` attribute valid only on
   methods, and read it back with Reflection without instantiating it.
2. **(Expert)** Make `#[Cacheable]` repeatable and write code that lists every
   occurrence on a method along with its arguments.

??? success "Solutions"

    **1.**
    ```php
    #[\Attribute(\Attribute::TARGET_METHOD)]
    final class Cacheable
    {
        public function __construct(public readonly int $ttl = 0) {}
    }

    $attrs = (new \ReflectionMethod(Service::class, 'find'))
        ->getAttributes(Cacheable::class); // data only — nothing instantiated yet
    ```

    **2.** Add `\Attribute::IS_REPEATABLE` to the flags, then
    `foreach ($attrs as $a) { $a->getArguments(); }` reads every occurrence's
    arguments without calling `newInstance()`.

## Certification questions

*Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.*

??? question "Q1. When does declaring `#[LogCall]` on a method run `LogCall`'s constructor?"
    - [ ] A. Immediately when the file is parsed
    - [ ] B. The first time the method is called
    - [x] C. Only when something calls `newInstance()` on the read attribute ✅
    - [ ] D. Never — attributes cannot be instantiated

    **Why:** attributes are inert metadata; `getAttributes()` returns data,
    `newInstance()` is the one call that constructs the object.
    **Ref:** [PHP: Attributes](https://www.php.net/manual/en/language.attributes.php).

??? question "Q2. What does `getAttributes()` return when no matching attribute is present?"
    - [x] A. An empty array ✅
    - [ ] B. `null`
    - [ ] C. `false`
    - [ ] D. Throws `ReflectionException`

    **Why:** an absent attribute is represented as an empty list, never
    `null` — a plain `foreach` is always safe.
    **Ref:** [PHP: ReflectionClass::getAttributes](https://www.php.net/manual/en/reflectionclass.getattributes.php).

??? question "Q3. What happens if a non-repeatable attribute is applied twice to the same method?"
    - [ ] A. The second application silently overwrites the first
    - [x] B. PHP raises a fatal error before the code runs ✅
    - [ ] C. `getAttributes()` returns only the first one
    - [ ] D. Both apply, merged into one instance

    **Why:** `IS_REPEATABLE` must be set for a target to carry the same
    attribute more than once; otherwise it is rejected outright.
    **Ref:** [PHP: Attributes — Repeated attributes](https://www.php.net/manual/en/language.attributes.reflection.php).

??? question "Q4. `Symfony\Component\Routing\Attribute\Route` declares which flags?"
    - [ ] A. `TARGET_ALL` only
    - [x] B. `IS_REPEATABLE \| TARGET_CLASS \| TARGET_METHOD` ✅
    - [ ] C. `TARGET_METHOD` only, not repeatable
    - [ ] D. `TARGET_PROPERTY \| TARGET_PARAMETER`

    **Why:** `Route` is valid on classes (a path prefix) and methods, and
    repeatable so one action can expose two paths.
    **Ref:** [Symfony source — Route](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Attribute/Route.php).

## Key takeaways

- An attribute is inert metadata: it does nothing until read via Reflection.
- `getAttributes()` returns data (name/arguments/target); `newInstance()`
  is the only call that constructs the object and autoloads its class.
- `Attribute::TARGET_*` restricts where an attribute may be used;
  `IS_REPEATABLE` allows more than one occurrence on the same target.
- Symfony's `#[Route]`, `#[AsCommand]`, etc. are plain attribute classes —
  the framework's loaders are the "something" that reads and instantiates them.

## Last-minute revision

!!! tip "Cheat sheet"
    - Declare: `#[\Attribute(TARGET_* | IS_REPEATABLE)]` above the class.
    - Read: `getAttributes(?string $name = null, int $flags = 0): array`.
    - `ReflectionAttribute`: `getName()`, `getArguments()`, `getTarget()`,
      `isRepeated()`, `newInstance()`.
    - `ReflectionAttribute::IS_INSTANCEOF` — match subclasses too.
    - Class constants can carry attributes since PHP **8.3**.

## Connections

- **Depends on:** [OOP](oop.md) — attribute classes are plain classes with a
  constructor.
- **Reused in:** [Routing](../routing/configuration.md), [Console](../console/custom-commands.md),
  [Dependency Injection](../dependency-injection/registration.md) — `#[Route]`,
  `#[AsCommand]`, `#[Autowire]` are all consumed exactly this way.
- **Confused with:** [PHP API](php-api.md) — that chapter covers `#[\Override]`
  and other language features; this one covers the attribute mechanism itself.

## Official References
- [PHP manual — Attributes](https://www.php.net/manual/en/language.attributes.php)
- [PHP manual — Reflection API and attributes](https://www.php.net/manual/en/language.attributes.reflection.php)
- [Symfony source — Route attribute](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Attribute/Route.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "PHP attributes" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://www.php.net/manual/en/language.attributes.php) — the PHP manual page for attributes.

## Confidence check

I'm ready when I can:

- [ ] explain **why** an attribute alone has no runtime effect
- [ ] declare a targeted, repeatable attribute and read it back in Symfony 8
- [ ] debug code that expected `getAttributes()` to instantiate something
- [ ] spot the trap: default target is `TARGET_ALL`, not "none"
- [ ] explain how Symfony's `#[Route]`/`#[AsCommand]` are read via Reflection, not magic

---

<small>Related: [OOP](oop.md) · [PHP API](php-api.md) · [Interfaces](interfaces.md)</small>

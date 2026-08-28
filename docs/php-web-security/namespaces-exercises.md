# Guided Exercises — Namespaces & Autoloading

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    an answer before revealing a hint, and to a full attempt before revealing the solution —
    a resolution rule you predicted wrongly and then corrected sticks far better than one you
    read.

    Theory: **[Namespaces & Autoloading](namespaces.md)** · Then:
    **[Topic exam](namespaces-exam.md)**

    All code targets **PHP 8.4**. Most of these run with a bare `php file.php`; the last two
    assume a Symfony 8.0 skeleton with the default `config/services.yaml`.

## Exercise 1 · Discover the three kinds of name

**Objective:** Feel the difference between unqualified, qualified and fully qualified names
before learning the rules that govern them.

**Context:** One file, one namespace, three ways of writing what looks like "the same" name.

**Starting point:**

```php
<?php
namespace App\Reporting;

class Formatter
{
    public static function who(): string
    {
        return self::class;
    }
}

echo Formatter::who(), "\n";        // (1) unqualified
echo \App\Reporting\Formatter::who(), "\n";  // (3) fully qualified
```

**Task:** Predict what each of the two `echo` lines prints. Then add a third line using the
**qualified** form `Reporting\Formatter::who()` and predict *that* before running it.

**Expected observation:** Lines 1 and 3 print the same FQCN. The qualified line fails — and
the error message tells you exactly which name PHP built.

??? tip "Show a hint"
    A qualified name is not "a name with the namespace in it". It is a name PHP treats as
    **relative** to where you are standing. Ask yourself: relative to what? You are already
    inside `App\Reporting`.

??? success "Show the solution"
    Lines 1 and 3 both print `App\Reporting\Formatter`.

    The qualified form fails:

    ```
    Error: Class "App\Reporting\Reporting\Formatter" not found
    ```

    **Why it works:** the manual's filesystem analogy is exact. An **unqualified** name
    (`Formatter`) is like `foo.txt` — resolved inside the current directory, so the current
    namespace is prepended. A **qualified** name (`Reporting\Formatter`) is like
    `subdirectory/foo.txt` — also relative, so the current namespace is prepended to the
    *whole* thing, giving `App\Reporting\Reporting\Formatter`. A **fully qualified** name
    (`\App\Reporting\Formatter`) is like `/main/foo.txt` — absolute, taken literally.

    **Certification takeaway:** "qualified" does **not** mean "absolute". Only a leading
    backslash makes a name absolute. Exam distractors routinely offer a qualified name where
    a fully qualified one is required.

    **Official reference:** https://www.php.net/manual/en/language.namespaces.basics.php

## Exercise 2 · Build the smallest possible PSR-4 autoloader

**Objective:** Turn a class name into a file path by hand, so the "magic" of
`vendor/autoload.php` becomes a five-line function.

**Context:** No Composer. Two files. One PSR-4 rule: `App\` maps to `src/`.

**Starting point:**

```text
project/
├── run.php
└── src/
    └── Service/
        └── Mailer.php
```

`src/Service/Mailer.php`:

```php
<?php
declare(strict_types=1);

namespace App\Service;

final class Mailer
{
    public function send(string $to): string
    {
        return 'sent to ' . $to;
    }
}
```

**Task:** In `run.php`, register an autoloader with `spl_autoload_register()` that implements
the PSR-4 rule `App\` → `src/`, then instantiate `App\Service\Mailer` and call `send()`.
Write no `require` for the class itself.

**Expected observation:** `sent to a@b.test`, with the class file loaded on demand.

??? tip "Show a hint"
    Three string operations, in this order: check that the class name starts with the prefix,
    remove the prefix, and translate the remaining `\` separators into directory separators.
    Then append `.php` and `require` the file if it exists.

??? success "Show the solution"
    `run.php`:

    ```php
    <?php
    declare(strict_types=1);

    spl_autoload_register(static function (string $class): void {
        $prefix = 'App\\';
        $baseDir = __DIR__ . '/src/';

        if (!str_starts_with($class, $prefix)) {
            return; // not ours — let the next registered loader try
        }

        $relative = substr($class, strlen($prefix));
        $file = $baseDir . str_replace('\\', '/', $relative) . '.php';

        if (is_file($file)) {
            require $file;
        }
    });

    $mailer = new \App\Service\Mailer();
    echo $mailer->send('a@b.test'), "\n";
    ```

    **Why it works:** PSR-4 is a pure string transformation — strip the mapped prefix,
    replace `\` with the directory separator, append `.php`. Composer's generated loader does
    exactly this, only faster and with several prefixes at once. `spl_autoload_register()`
    builds a **queue**: the manual notes it "effectively creates a queue of autoload
    functions, and runs through each of them in the order they are defined", which is why
    returning early (instead of throwing) when the prefix does not match is the correct
    behaviour for a well-behaved loader.

    **Certification takeaway:** the prefix maps to the base directory and then **disappears**
    from the path. `App\Service\Mailer` becomes `src/Service/Mailer.php`, never
    `src/App/Service/Mailer.php` — that second form is PSR-0 thinking.

    **Official reference:** https://www.php.net/manual/en/function.spl-autoload-register.php

## Exercise 3 · Inspect *when* the file is actually read

**Objective:** Prove to yourself that `use` performs no I/O, and see the exact moment the
autoloader fires.

**Context:** Same project. This time you instrument the loader instead of writing one.

**Starting point:**

```php
<?php
declare(strict_types=1);

namespace App;

spl_autoload_register(static function (string $class): void {
    echo "AUTOLOAD ASKED FOR: {$class}\n";
});

use App\Service\Mailer;

echo "after the use statement\n";

class_exists(Mailer::class);

echo "done\n";
```

**Task:** Predict the exact order of the three lines of output before running. In particular,
decide whether `AUTOLOAD ASKED FOR:` appears before or after
`after the use statement` — and what class name it reports.

**Expected observation:**

```text
after the use statement
AUTOLOAD ASKED FOR: App\Service\Mailer
done
```

??? tip "Show a hint"
    Ask what a `use` statement leaves behind after compilation. If it produced no opcode at
    all, when could it possibly trigger anything?

??? success "Show the solution"
    The output is exactly as predicted above: the `use` line produces **no** output, and the
    autoloader fires only when `class_exists()` forces a real lookup.

    **Why it works:** "Importing is performed at compile-time." A `use` statement adds one
    row to the file's class import table and emits no runtime instruction. The class name
    reported is the **fully qualified** `App\Service\Mailer`, because `Mailer::class` was
    translated through the import table by the compiler before the string ever existed.

    Two consequences worth internalising: a `use` for a class that does not exist is
    harmless as long as you never reference the class; and the autoloader is always handed an
    FQCN with **no** leading backslash.

    **Certification takeaway:** `use` is an alias, not a `require`. Every distractor that
    claims `use` "loads the file", "includes the class", or "registers an autoloader" is
    wrong for the same single reason.

    **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

## Exercise 4 · Change one variable: alias a class, then call it as a function

**Objective:** Discover that PHP keeps three independent import tables, by changing nothing
but the *kind* of symbol you reference.

**Context:** One import, two references.

**Starting point:**

```php
<?php
declare(strict_types=1);

namespace A;

use ArrayObject as AO;

function AO(): string
{
    return 'A\AO() was called';
}

$o = new AO([1, 2, 3]);
echo get_class($o), "\n";   // (1) class context
echo AO(), "\n";            // (2) function context
```

**Task:** Predict both lines. Then remove the local `function AO()` and predict line 2 again
before running.

**Expected observation:** Line 1 prints `ArrayObject`. Line 2 prints `A\AO() was called`.
After deleting the local function, line 2 fails with
`Error: Call to undefined function A\AO()` — note *which* name PHP reports.

??? tip "Show a hint"
    The import you wrote is `use ArrayObject as AO;` — with no `function` keyword. Which of
    PHP's three import tables did it fill?

??? success "Show the solution"
    Line 1 prints `ArrayObject`: the class import table contains `AO => ArrayObject`, so the
    unqualified class name is translated.

    Line 2 prints `A\AO() was called`: the **function** import table is empty, so the
    unqualified function name falls through the ordinary rules — current namespace first,
    which finds `A\AO()`.

    Delete that function and line 2 becomes:

    ```
    Error: Call to undefined function A\AO()
    ```

    PHP tried `A\AO()`, then the global `AO()`, and reported the failure.

    **Why it works:** resolution rule 5 says unqualified names are "translated according to
    the current import table **for the respective symbol type**". `use X as Y;` fills the
    class table, `use function X as Y;` the function table, `use const X as Y;` the constant
    table. They never leak into each other, which is why a class alias and a function of the
    same short name coexist without conflict.

    **Certification takeaway:** an alias applies to **one symbol kind**. A question that
    shows `use C\E as F;` and then calls `F()` is testing exactly this: the answer is
    "current namespace, then global", never "the aliased class".

    **Official reference:** https://www.php.net/manual/en/language.namespaces.rules.php

## Exercise 5 · Diagnose a failure: the class that refuses to be global

**Objective:** Read the two most common namespace fatals and map each to the rule that
produced it.

**Context:** A perfectly ordinary-looking file that fails twice for two different reasons.

**Starting point:**

```php
<?php
// lint-skip — this file is meant to fail at runtime, twice
declare(strict_types=1);

namespace App\Support;

$when = new DateTimeImmutable('2026-01-01');   // failure #1

$class = 'DateTimeImmutable';
$also = new $class('2026-01-01');              // failure #2 — or is it?
```

**Task:** Run it. Fix failure #1 in **two different ways** (without touching the namespace
line). Then decide, before running again, whether failure #2 exists at all — and explain why.

**Expected observation:** Failure #1 is `Error: Class "App\Support\DateTimeImmutable" not
found`. Failure #2 does **not** occur.

??? tip "Show a hint"
    Compare the two lines carefully: one name is seen by the *compiler*, the other only by
    the *runtime*, as a string. Do the same resolution rules apply to both?

??? success "Show the solution"
    Failure #1:

    ```
    Error: Class "App\Support\DateTimeImmutable" not found
    ```

    Two independent fixes:

    ```php
    $when = new \DateTimeImmutable('2026-01-01');   // fix A: fully qualified
    ```

    ```php
    use DateTimeImmutable;                          // fix B: import it
    // ...
    $when = new DateTimeImmutable('2026-01-01');
    ```

    Failure #2 never happens: `new $class` succeeds and builds a real `DateTimeImmutable`.

    **Why it works:** unqualified **class** names have no global fallback — the manual's own
    example shows `new ArrayObject` fataling inside `namespace A\B\C;`. But a **dynamic**
    class name is a plain string evaluated at runtime, and "there is no difference between a
    qualified and a fully qualified Name inside a dynamic class name": the string is treated
    as absolute, so `'DateTimeImmutable'` means the global class and resolves fine.

    That asymmetry is genuinely counter-intuitive and is exactly why it is examinable: the
    literal form fails, the string form succeeds, and neither is affected by a `use` you
    might add.

    **Certification takeaway:** two rules, two directions. Compile-time class names get the
    current namespace prepended (no global fallback). Runtime string class names get nothing
    prepended and no alias applied (always fully qualified).

    **Official reference:** https://www.php.net/manual/en/language.namespaces.dynamic.php

## Exercise 6 · Handle the edge cases of file structure

**Objective:** Provoke the four structural fatals that namespaces can raise, and learn to
recognise each message.

**Context:** Four tiny files, each broken in a different way.

**Starting point:**

```php
<?php
// lint-skip — file (a): declare after namespace
namespace App;
declare(strict_types=1);
```

```php
<?php
// lint-skip — file (b): mixing the two namespace syntaxes
namespace App;
class One {}
namespace Other {
    class Two {}
}
```

```php
<?php
// lint-skip — file (c): a use inside a function body
namespace App;
function boot(): void {
    use App\Service\Mailer;
}
```

```php
<?php
// lint-skip — file (d): import name collides with a local declaration
namespace App;
use Other\Thing as Mailer;
class Mailer {}
```

**Task:** For each file, predict *whether* it fails, and whether the failure is a **parse**
error (detected by `php -l`) or a **fatal** raised while the file is compiled. Then run
`php -l` on each and compare.

**Expected observation:** All four fail. Their messages are all different, and only file (c)
is a plain syntax error.

??? tip "Show a hint"
    Two of these are about *ordering* — what may appear before what. One is about *scope* —
    where a construct is even grammatical. One is about *binding* — two things claiming the
    same short name in the same file.

??? success "Show the solution"

    ```text
    (a) Fatal error: strict_types declaration must be the very first statement in the script
    (b) Fatal error: Cannot mix bracketed namespace declarations with unbracketed
        namespace declarations
    (c) Parse error: syntax error, unexpected token "use"
    (d) Fatal error: Cannot redeclare class App\Mailer (previously declared as local import)
    ```

    **Why it works:**

    - **(a)** `declare` is the *only* construct allowed before `namespace`, and
      `strict_types` in particular must be the very first statement of the script. Reversing
      the two lines fixes it.
    - **(b)** A file must use one namespace syntax throughout. If you truly need several
      namespaces in one file, use the bracketed form everywhere — and remember that
      unnamespaced code then has to live inside an unnamed `namespace { … }` block.
    - **(c)** "The `use` keyword must be declared in the outermost scope of a file (the
      global scope) or inside namespace declarations… so it cannot be block scoped." Because
      importing happens at compile time, a *runtime* scope makes no sense for it.
    - **(d)** "Import names must not conflict with classes defined in the same file." The
      import already bound the short name `Mailer` in this file's class table.

    **Certification takeaway:** `declare` before `namespace`, `namespace` before everything
    else, `use` after `namespace` and never inside a function, one namespace syntax per file.
    Four rules, four distinct error messages — recognising the message is often the fastest
    route to the right answer.

    **Official reference:** https://www.php.net/manual/en/language.namespaces.definition.php

## Exercise 7 · Expert challenge: break Symfony's PSR-4 service discovery

**Objective:** Connect PHP name resolution to the Symfony container, by making the framework
tell you exactly what it expected to find and where.

**Context:** A Symfony 8.0 skeleton with the default `config/services.yaml`:

```yaml
services:
    _defaults:
        autowire: true
        autoconfigure: true

    App\:
        resource: '../src/'
```

and `composer.json` mapping `"App\\": "src/"`.

**Starting point:** A working service at `src/Service/Mailer.php` in namespace
`App\Service`, injected somewhere by its type-hint.

**Task:**

1. `git mv src/Service/Mailer.php src/Mailer/Mailer.php` **without** editing the file's
   `namespace App\Service;` line, then clear the cache and rebuild the container.
2. Read the exception carefully and name the class Symfony expected.
3. Fix it the correct way; then explain why fixing only the `composer.json` PSR-4 rule (for
   example by adding `"App\\Service\\": "src/Mailer/"`) would satisfy the autoloader but
   still not satisfy the container.

**Expected observation:** An `InvalidArgumentException` naming `App\Mailer\Mailer` — a class
that appears nowhere in your code.

??? tip "Show a hint"
    Service discovery does not read your `namespace` lines. It walks the directory tree and
    *computes* the class name it expects from the path, then asks reflection whether that
    class exists. Which of those two names is derived from what?

??? success "Show the solution"
    The container build fails with:

    ```text
    Expected to find class "App\Mailer\Mailer" in file ".../src/Mailer/Mailer.php" while
    importing services from resource "../src/*", but it was not found!
    Check the namespace prefix used with the resource.
    ```

    The correct fix is to make the namespace follow the path — change the file to
    `namespace App\Mailer;` and update every `use App\Service\Mailer;` accordingly.

    **Why it works:** `FileLoader::registerClasses()` takes the configured prefix (`App\`),
    strips the resource base from each discovered path, converts `/` to `\`, drops the
    `.php`, and uses the result as the class name. It then calls
    `$this->container->getReflectionClass($class)`; when that returns nothing it throws the
    message above. Your file still *declares* `App\Service\Mailer`, so nothing named
    `App\Mailer\Mailer` exists.

    Patching only `composer.json` would let the autoloader find `App\Service\Mailer` again,
    but the container would keep deriving `App\Mailer\Mailer` from the path and keep
    failing — the two systems answer different questions. Composer resolves **name →
    file**; Symfony's discovery resolves **file → name**. Only a layout where namespace and
    path agree satisfies both, which is why "PSR-4 is a convention, not a rule" is false in
    practice for a Symfony application.

    There is a second-order consequence worth stating: because the default import gives each
    class a service id equal to its **fully-qualified class name**, and autowiring "looks for
    a service whose id exactly matches the type-hint", renaming a namespace renames a
    container key. Every injection point that type-hinted the old FQCN stops resolving at the
    same moment.

    **Certification takeaway:** in Symfony, the namespace is not documentation — it is
    simultaneously the autoloader's file path, the container's service id, and the
    autowiring key. A path/namespace mismatch surfaces as a container-build exception that
    names a class you never wrote.

    **Official reference:** https://symfony.com/doc/8.0/service_container.html

---

<small>Back to the lesson: [Namespaces & Autoloading](namespaces.md) · Next: [Topic exam](namespaces-exam.md)</small>

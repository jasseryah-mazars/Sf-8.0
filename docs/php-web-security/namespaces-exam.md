# Topic Exam — Namespaces & Autoloading

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because name-resolution
    questions are built on near-misses: one missing backslash changes the answer.

    Theory: **[Namespaces & Autoloading](namespaces.md)** ·
    Practice: **[Guided exercises](namespaces-exercises.md)** ·
    Recall: **[Flashcards](namespaces-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4** and **Symfony 8.0**.

## Name resolution

??? question "Question 1"
    Inside `namespace App;`, an unqualified call `count($x)` resolves to…

    - A. `App\count` if it is defined, otherwise the global `\count`
    - B. Always `App\count`, whether or not it exists
    - C. A fatal error, because functions must be imported before use
    - D. The global `\count` only — the current namespace is never consulted

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** for an unqualified **function** name with no matching import, PHP
        resolves at runtime in two steps: first it looks for the function in the current
        namespace (`App\count`), then it tries the **global** function `count()`. That
        two-step lookup is the global fallback, and it exists only for functions and
        constants.

        **B** describes the rule that applies to *class* names, not functions — classes stop
        at the current namespace and never fall back. **C** invents a requirement: no import
        is needed precisely because of the fallback. **D** drops the first step; a
        user-defined `App\count()` would shadow the global one, which is exactly how the
        manual's `A\B\C\strlen()` example works.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.rules.php

??? question "Question 2"
    Inside `namespace App;`, which expression references the **global** `DateTimeImmutable`
    class, given no `use` statement in the file?

    - A. `new DateTimeImmutable()`
    - B. `new \DateTimeImmutable()`
    - C. `new App\DateTimeImmutable()`
    - D. `new global\DateTimeImmutable()`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** class names **never** fall back to the global namespace. A leading
        backslash makes the name fully qualified, so `\DateTimeImmutable` resolves literally
        to `DateTimeImmutable` in the global namespace. Adding `use DateTimeImmutable;` at
        the top of the file would work equally well.

        **A** is an unqualified class name: with no import, the current namespace is
        prepended and PHP looks for `App\DateTimeImmutable`, which does not exist. **C** is a
        *qualified* name, so the current namespace is prepended too — it resolves to
        `App\App\DateTimeImmutable`, which is even further from the target. **D** is not PHP:
        there is no `global` namespace keyword; the global space is addressed with a bare
        leading `\`.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.fallback.php

??? question "Question 3 · Multiple answers"
    In which situations does PHP fall back to the **global** namespace when a name is not
    found in the current namespace? (Choose all that apply.)

    - A. An unqualified function name, e.g. `strlen($s)`
    - B. An unqualified constant name, e.g. `INI_ALL`
    - C. An unqualified class name, e.g. `new ArrayObject()`
    - D. A qualified name, e.g. `Sub\helper()`

    ??? success "Show answer"
        **Correct answers:** A and B

        **Explanation:** the manual states the fallback for exactly two symbol kinds:
        "For functions and constants, PHP will fall back to global functions or constants
        if a namespaced function or constant does not exist." So `strlen()` and `INI_ALL`
        both resolve globally when the namespaced version is missing.

        **C** is the classic trap: inside `namespace A\B\C;`, `new ArrayObject` is a fatal
        error because PHP looks only for `A\B\C\ArrayObject` — the manual spells this exact
        case out. **D** is wrong because a qualified name is not eligible for the fallback at
        all: its first segment is either translated by the import table or the current
        namespace is prepended, and resolution stops there.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.fallback.php

??? question "Question 4 · Code analysis"
    What does `new F()` create?

    ```php
    <?php
    namespace A;

    use B\D, C\E as F;

    $x = new F();
    ```

    - A. An object of class `A\F`
    - B. An object of class `C\E`
    - C. An object of class `F` in the global namespace
    - D. An object of class `B\D\F`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `F` is an unqualified **class-like** name, so PHP consults the
        class/namespace import table first. `use C\E as F;` puts `F => C\E` in that table,
        so `new F()` resolves to `C\E` and, if the class is not yet loaded, the autoloader is
        asked for `C\E`. The manual's own "Name resolutions illustrated" example uses this
        exact pair of imports.

        **A** would be the answer only if no import matched — then the current namespace is
        prepended. **C** requires a leading backslash: `new \F()` is fully qualified and
        deliberately ignores the import table. **D** confuses the two imports on the same
        line; `use B\D, C\E as F;` is just two independent imports, and `B\D` is aliased to
        `D`, not combined with `F`.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.rules.php

??? question "Question 5 · Trap"
    Using the *same* file header as the previous question, what does the call `F();` do?

    ```php
    <?php
    namespace A;

    use B\D, C\E as F;

    F();
    ```

    - A. Calls the static method `E::F()` of class `C\E`
    - B. Calls a function `C\E()`
    - C. Tries `A\F()`, then falls back to the global function `F()`
    - D. Is a fatal error, because `F` is already taken by a class import

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** PHP keeps **three separate import tables** — one for class-like
        names, one for functions, one for constants. `use C\E as F;` fills only the
        class table. A function call therefore finds no import rule, so the unqualified
        function rules apply: look for `A\F()` in the current namespace, then for the global
        `F()`. Importing the function would require `use function C\E as F;`.

        **A** invents a syntax: a static call needs `F::method()`, and a bare `F()` is never
        a static call. **B** assumes the class import leaks into the function table, which is
        precisely the misconception this question tests. **D** is wrong because the two
        tables cannot collide: a class alias and a function name may share the same short
        name without any error.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.rules.php

??? question "Question 6 · Execution order"
    Code lives in `namespace A\B;` and calls `foo()`. There is no `use function` import. In
    what order does PHP attempt resolution?

    - A. Global `foo()`, then `A\B\foo()`
    - B. `A\B\foo()`, then global `foo()`
    - C. `A\B\foo()` only; a missing function is a fatal error
    - D. `A\foo()`, then `A\B\foo()`, then global `foo()`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual's resolution rules say that for an unqualified
        function name with no applicable import rule, outside the global namespace, the name
        is resolved **at runtime**: "It looks for a function from the current namespace:
        `A\B\foo()`", then "It tries to find and call the *global* function `foo()`."
        Current namespace first, global second.

        **A** reverses the order, which would make it impossible to shadow a global function
        with a namespaced one — the whole point of the manual's `A\B\C\strlen()` example.
        **C** removes the fallback entirely and describes class-name behaviour. **D** invents
        an intermediate step: PHP never walks *up* the namespace hierarchy segment by
        segment; there are exactly two candidates.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.rules.php

??? question "Question 7 · True or false"
    A fully qualified name such as `\Another\thing` is never rewritten by a `use` statement
    in the same file.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** A — true

        **Explanation:** resolution rule 1 says "Fully qualified names always resolve to the
        name without leading namespace separator". The manual demonstrates the pair
        explicitly: after `use My\Full\Classname as Another;`, `new Another\thing` builds
        `My\Full\Classname\thing`, while `new \Another\thing` stays `Another\thing`. Imports
        affect only unqualified and qualified names.

        **B** would mean a leading `\` is cosmetic. It is not: it is the one syntax that
        guarantees a name means what it literally says, which is why library code writes
        `\strlen()` and `\Exception` when it wants to be immune to both imports and the
        current namespace.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

## Importing with `use`

??? question "Question 8"
    What does the statement `use App\Service\Mailer;` do?

    - A. Loads `src/Service/Mailer.php` immediately
    - B. Creates a compile-time alias so that `Mailer` means `App\Service\Mailer`
    - C. Instantiates the class once and caches it
    - D. Registers an autoloader for the `App\Service` namespace

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "Importing is performed at compile-time." A `use` statement adds one
        entry to the file's class import table and produces no runtime work whatsoever. The
        file is read from disk only later, when the class is actually *used* — `new`, a
        static call, `class_exists()`, a type-hint being checked — and the registered
        autoloader is invoked then.

        **A** is the single most common misconception: `use` performs no I/O at all. You can
        `use` a class that does not exist and the file still parses and runs, as long as you
        never reference it. **C** confuses importing with instantiation; `use` never
        evaluates anything. **D** confuses importing with `spl_autoload_register()`, which is
        what `vendor/autoload.php` calls.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "Question 9 · True or false"
    `use App\Foo;` also imports the class `App\Foo\Bar`, so `Bar` can be used unqualified.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — false

        **Explanation:** a `use` statement aliases exactly **one** name. After `use App\Foo;`
        the import table contains `Foo => App\Foo` and nothing else. `Bar` alone remains an
        unqualified name that resolves against the current namespace. What *does* work is the
        qualified form `Foo\Bar`, because rule 3 translates the first segment of a qualified
        name through the import table, giving `App\Foo\Bar`.

        **A** describes a recursive, package-style import that PHP does not have. If you want
        both names available unqualified, write two imports, or one group use declaration:
        `use App\Foo\{Bar, Baz};`.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "Question 10"
    What does `use function App\Support\slugify;` do at the top of a file?

    - A. Imports a class named `slugify`
    - B. Defines a new global function `slugify()`
    - C. Aliases the namespaced function so `slugify()` can be called unqualified
    - D. Is invalid syntax — only classes, interfaces and traits can be imported

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** `use function` adds an entry to the **function** import table, so an
        unqualified `slugify()` in that file resolves directly to `App\Support\slugify`
        without consulting the current namespace or the global fallback. `use const` does the
        same for constants.

        **A** is what a plain `use App\Support\slugify;` would do — it would fill the *class*
        table and leave function calls untouched. **B** is impossible: `use` never declares
        anything. **D** is factually wrong; the manual lists the importable symbol kinds as
        "constants, functions, classes, interfaces, traits, enums and namespaces".

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "Question 11 · Multiple answers"
    Which statements about `use` declarations are correct? (Choose all that apply.)

    - A. They are resolved at compile time and cost nothing at runtime
    - B. They must appear in the outermost scope of the file or inside a namespace block
    - C. Import rules are per file — an `include`d file does not inherit them
    - D. A `use` statement triggers the autoloader for the imported symbol

    ??? success "Show answer"
        **Correct answers:** A, B and C

        **Explanation:** all three come straight from the "Aliasing/Importing" section.
        **A**: "Importing is performed at compile-time." **B**: "The `use` keyword must be
        declared in the outermost scope of a file (the global scope) or inside namespace
        declarations… so it cannot be block scoped" — writing `use` inside a function body is
        a parse error. **C**: "Importing rules are per file basis, meaning included files
        will **NOT** inherit the parent file's importing rules."

        **D** is the odd one out: importing is purely a compile-time alias. Autoloading only
        happens when the symbol is actually referenced at runtime.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "Question 12"
    Which single statement is equivalent to these three imports?

    ```php
    use some\ns\ClassA;
    use some\ns\ClassB;
    use some\ns\ClassC as C;
    ```

    - A. `use some\ns\*;`
    - B. `use some\ns\{ClassA, ClassB, ClassC as C};`
    - C. `use some\ns[ClassA, ClassB, ClassC as C];`
    - D. `use some\ns\ClassA + ClassB + ClassC as C;`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** group `use` declarations, added in PHP 7.0, factor a common prefix
        and list the imported names in braces, with `as` still available per entry. The same
        shape works for the other two tables: `use function some\ns\{fn_a, fn_b};` and
        `use const some\ns\{ConstA, ConstB};`.

        **A** is a wildcard import, which PHP has never supported — every imported name must
        be written out. **C** and **D** are invented syntaxes; braces are the only grouping
        construct, and there is no operator form. Note that PHP also accepts a *comma* form
        on one line (`use My\A as X, My\B;`), but that repeats no prefix and is not what the
        question shows.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "Question 13 · Debugging"
    A file contains exactly this. What happens?

    ```php
    <?php // lint-skip — this snippet is a deliberate fatal error; it is the question
    namespace my\stuff;

    use another\thing as MyClass;

    class MyClass {}
    ```

    - A. Nothing special — the local class silently wins
    - B. A fatal error: the class declaration conflicts with the import
    - C. A deprecation notice, and the import wins
    - D. It is valid; `MyClass` refers to `another\thing` everywhere in the file

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual's FAQ is explicit — "Import names must not conflict with
        classes defined in the same file." PHP 8.4 reports
        `Fatal error: Cannot redeclare class my\stuff\MyClass (previously declared as local
        import)`. The import already bound the short name `MyClass` in this file's class
        table, so the declaration has nowhere to go.

        **A** and **C** invent a precedence rule and a deprecation path that do not exist;
        the conflict is unconditional and fatal. **D** would be true only if the class
        declaration were removed, or if it lived in a *different* file — the same FAQ shows
        that importing `another\thing as MyClass` while `my\stuff\MyClass` is declared in
        another file is perfectly legal.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.faq.php#language.namespaces.faq.conflict

## Declaring namespaces in a file

??? question "Question 14"
    Which construct may legally appear **before** a `namespace` declaration in a PHP file?

    - A. A `use` statement
    - B. A `declare` statement
    - C. An `include` of a bootstrap file
    - D. A single blank line of HTML output

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "A file containing a namespace must declare the namespace at the top
        of the file before any other code — with one exception: the `declare` keyword." So
        `declare(strict_types=1);` on the line above `namespace App;` is the one legal
        ordering, and it is the convention Symfony's own source uses.

        **A** is backwards: imports come *after* the namespace, since they belong to it.
        **C** executes code, which is exactly what the rule forbids. **D** is the classic
        production failure — the manual notes that "no non-PHP code may precede a namespace
        declaration, including extra whitespace", and PHP 8.4 answers with
        `Fatal error: Namespace declaration statement has to be the very first statement or
        after any declare call in the script`.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.definition.php

??? question "Question 15 · Debugging"
    A file declares `namespace A;` without braces at the top, then later opens
    `namespace B { … }` with braces. What does PHP do?

    - A. Accepts it; the brace syntax is just an alternative spelling
    - B. Fatal error: bracketed and unbracketed namespace declarations cannot be mixed
    - C. Silently ignores the bracketed block
    - D. Treats `B` as a sub-namespace of `A`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** a file must pick one style for all of its namespace declarations.
        PHP 8.4 reports `Fatal error: Cannot mix bracketed namespace declarations with
        unbracketed namespace declarations`. The manual documents the two syntaxes as
        alternatives — the simple combination syntax and the bracketed syntax — and
        recommends the bracketed one when a file really must hold several namespaces.

        **A** ignores the "one style per file" constraint. **C** invents silent behaviour PHP
        never has for a syntax error of this kind. **D** describes nesting, which the FAQ
        rules out separately: "Nested namespaces are not allowed"; `namespace A\B;` is how
        you express a sub-namespace.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.definitionmultiple.php

??? question "Question 16 · True or false"
    To combine namespaced code and non-namespaced (global) code in a single file, you wrap
    the global code in `namespace { … }` with no name — and only the bracketed syntax
    supports this.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** A — true

        **Explanation:** the manual states it directly: "To combine global non-namespaced code
        with namespaced code, only bracketed syntax is supported. Global code should be
        encased in a namespace statement with no namespace name." It also adds that no PHP
        code may exist outside the braces, except an opening `declare` statement.

        **B** would imply the unbracketed form can express "back to global", which it cannot:
        once a file uses `namespace A;` without braces, everything after it belongs to `A`
        until the next unbracketed declaration, and there is no unnamed unbracketed form.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.definitionmultiple.php

## Dynamic names and edge cases

??? question "Question 17 · Code analysis"
    What does this script print or raise?

    ```php
    <?php
    namespace A;

    use ArrayObject as AO;

    $class = 'AO';
    $o = new $class([1, 2]);
    ```

    - A. It creates an `ArrayObject`, because the alias applies
    - B. It creates an `A\AO`, because the current namespace is prepended
    - C. `Error: Class "AO" not found`
    - D. A parse error — a variable class name may not be aliased

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** two documented rules combine. First, "Importing is performed at
        compile-time, and so does not affect dynamic class, function or constant names" — the
        string `'AO'` was never seen by the compiler as a name. Second, a dynamic class name
        is always interpreted as **fully qualified**: "there is no difference between a
        qualified and a fully qualified Name inside a dynamic class name", so the leading
        backslash is unnecessary and the current namespace is *not* prepended. PHP therefore
        looks for a global class literally called `AO` and throws
        `Error: Class "AO" not found`.

        **A** is the trap the manual demonstrates with `$a = 'Another'; new $a;`. **B**
        applies the class-name rule for *compile-time* names, which does not extend to
        strings. **D** is wrong: `new $class` parses fine; the failure is at runtime. The fix
        is to write the full name, e.g. `$class = ArrayObject::class;`, which the compiler
        *does* translate through the import table.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.dynamic.php

??? question "Question 18 · Edge case"
    Why is `$a = "dangerous\name"; $obj = new $a;` a bug?

    - A. Double quotes are forbidden for class names
    - B. `\n` is interpreted as a newline, so the string is not the class name you wrote
    - C. PHP prepends the current namespace to double-quoted class names
    - D. `new` cannot accept a string variable

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the backslash is the escape character inside double-quoted strings,
        so `"dangerous\name"` contains `dangerous` + a **line feed** + `ame` — not the name
        `dangerous\name`. The manual titles this exact example "Dangers of using namespaced
        names inside a double-quoted string" and recommends doubling backslashes in every
        string, or using single quotes as in `'not\at\all\dangerous'`.

        **A** invents a rule about quote style; the problem is escaping, not quoting. **C**
        contradicts the dynamic-name rule: string class names are treated as fully qualified,
        never prefixed. **D** is wrong — `new $a` with a string variable is exactly how
        dynamic instantiation works, and it is the reason this trap exists at all.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.faq.php#language.namespaces.faq.quote

??? question "Question 19"
    Inside `namespace MyProject;`, what do `__NAMESPACE__` and `namespace\func()` refer to,
    and what does `__NAMESPACE__` hold in un-namespaced code?

    - A. `"MyProject"`; `MyProject\func()`; and `"\\"` in global code
    - B. `"MyProject"`; `MyProject\func()`; and `""` in global code
    - C. `"\MyProject"`; the global `func()`; and `"global"` in global code
    - D. `"MyProject"`; the global `func()`; and `null` in global code

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `__NAMESPACE__` is "a string that contains the current namespace
        name" with **no** leading separator, and "in global, un-namespaced code, it contains
        an empty string". The `namespace` keyword used as an operator is "the namespace
        equivalent of the `self` operator for classes": `namespace\func()` explicitly means
        `MyProject\func()`, bypassing the import table and the global fallback.

        **A** invents a backslash sentinel for global code. **C** adds a leading backslash to
        `__NAMESPACE__` and misreads the operator as a way to reach the global space — that
        is what a bare `\` prefix does. **D** makes `__NAMESPACE__` nullable, which it never
        is, and repeats **C**'s error about the operator.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.nsconstants.php

??? question "Question 20 · Edge case"
    In PHP 8.4, inside `namespace bar;`, `echo FOO;` runs where neither `bar\FOO` nor a
    global `FOO` is defined. What happens?

    - A. It prints the string `"FOO"` with a warning
    - B. It prints nothing and emits a notice
    - C. It throws `Error: Undefined constant "bar\FOO"`
    - D. It is a compile-time fatal error

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** since PHP 8.0, "if an undefined constant is used an `Error` is
        thrown". The constant fallback still runs first — `bar\FOO`, then global `FOO` — but
        when both are missing the engine raises an `Error`, and PHP 8.4 reports the name it
        tried in the current namespace: `Undefined constant "bar\FOO"`.

        **A** and **B** describe pre-8.0 behaviour: bare-word fallback to a string was
        deprecated in 7.2 (`E_WARNING`) and removed in 8.0. **D** is wrong about *when*: the
        file compiles fine, because unqualified function and constant names outside the
        global namespace are resolved at **runtime**.

        **Official reference:** https://www.php.net/manual/en/language.constants.php

## Autoloading, Composer and Symfony

??? question "Question 21"
    A `composer.json` maps the PSR-4 prefix `App\` to `src/`. Which file does the autoloader
    look for when `App\Foo\Bar` is first referenced?

    - A. `src/App/Foo/Bar.php`
    - B. `src/Foo/Bar.php`
    - C. `src/foo/bar.php`
    - D. `App/Foo/Bar.php`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the mapped prefix is replaced by the base directory and then
        disappears. Composer's own documentation says it plainly: "a namespace prefix `Foo\`
        pointing to a directory `src/` means that the autoloader will look for a file named
        `src/Bar/Baz.php`… Note that as opposed to the older PSR-0 style, the prefix (`Foo\`)
        is **not** present in the file path."

        **A** keeps the prefix inside the base directory — that is PSR-0 thinking. **C**
        lowercases the segments; PSR-4 preserves case, and on a case-sensitive filesystem the
        class simply will not be found. **D** drops the base directory entirely, which would
        only be correct if the mapping were `"App\\": "App/"`.

        **Official reference:** https://getcomposer.org/doc/04-schema.md#psr-4

??? question "Question 22 · Multiple answers"
    Which statements about Composer autoloader optimisation are correct? (Choose all that
    apply.)

    - A. `--optimize` converts PSR-4/PSR-0 rules into an explicit class map
    - B. `--classmap-authoritative` stops the loader from probing the filesystem for classes
      absent from the map
    - C. `--classmap-authoritative` also enables class-map generation
    - D. `--optimize` removes the `autoload-dev` rules from the generated autoloader

    ??? success "Show answer"
        **Correct answers:** A, B and C

        **Explanation:** **A** is Composer's "Optimization Level 1": "Class map generation
        essentially converts PSR-4/PSR-0 rules into classmap rules." **B** is Level 2/A:
        "if something is not found in the classmap, then it does not exist and the autoloader
        should not attempt to look on the filesystem according to PSR-4 rules." **C** is
        stated in the same section: "Enabling this automatically enables Level 1 class map
        optimizations." Symfony's performance page recommends
        `composer dump-autoload --no-dev --classmap-authoritative` for production.

        **D** attributes the wrong flag: excluding development rules is what `--no-dev` does —
        Symfony's own wording is that it "excludes the classes that are only needed in the
        development environment (i.e. `require-dev` dependencies and `autoload-dev` rules)".

        **Official reference:** https://symfony.com/doc/8.0/performance.html

??? question "Question 23 · Scenario"
    A Symfony 8 project uses the default `services.yaml` with `App\: resource: '../src/'`.
    A developer moves `src/Service/Mailer.php` to `src/Mailer/Mailer.php` but leaves the
    file's `namespace App\Service;` untouched. What happens when the container is built?

    - A. Nothing — Composer's PSR-4 rule still finds the class
    - B. An `InvalidArgumentException`: the class expected in that file was not found, with a
      hint to check the namespace prefix
    - C. The service is registered under the id `App\Service\Mailer` as before
    - D. A silent no-op: the file is skipped because its namespace does not match

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `FileLoader::registerClasses()` reconstructs the expected class name
        from the *path* — prefix plus the relative path with `/` turned into `\` and `.php`
        stripped — so it expects `App\Mailer\Mailer` in that file. When reflection finds no
        such class it throws: `Expected to find class "%s" in file "%s" while importing
        services from resource "%s", but it was not found! Check the namespace prefix used
        with the resource.`

        **A** confuses two different mechanisms: Composer's autoloader is only asked for a
        class *by name*, whereas service discovery scans *files* and derives names from
        paths — and Composer would fail here too, since PSR-4 maps `App\Service\Mailer` to
        `src/Service/Mailer.php`, which no longer exists. **C** cannot happen: the id would
        be derived from the path, not from the file's own `namespace` line. **D** is what
        happens for a file whose derived name is not a valid identifier, not for a valid name
        whose class is missing — that case is a hard exception.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/Loader/FileLoader.php

??? question "Question 24 · Scenario"
    With the default `services.yaml` autodiscovery, what is the service id of the class
    `App\Service\Mailer`, and why does that matter for autowiring?

    - A. `app.mailer` — autowiring maps snake_case ids to type-hints
    - B. `mailer` — the short class name, lowercased
    - C. `App\Service\Mailer` — autowiring looks for a service whose id exactly matches the
      type-hint
    - D. `App\Service\Mailer::class` is only an alias; the real id is generated randomly

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** the default import comment in `services.yaml` states that it
        "creates a service per class whose id is the fully-qualified class name", and the
        autowiring page adds: "The autowiring system **looks for a service whose id exactly
        matches the type-hint**… Autowiring isn't magic." This is why a namespace is not a
        cosmetic detail in Symfony: the FQCN *is* the container key.

        **A** and **B** describe the pre-3.3 manual-id convention, which autowiring cannot
        use — Symfony would report that it cannot autowire the argument. **D** is wrong on
        both counts: `Mailer::class` evaluates to the string `App\Service\Mailer`, and
        container ids are deterministic, never random.

        **Official reference:** https://symfony.com/doc/8.0/service_container/autowiring.html

??? question "Question 25 · Configuration consequence"
    In the Symfony skeleton, `autoload.psr-4` maps `App\` to `src/` and `autoload-dev.psr-4`
    maps `App\Tests\` to `tests/`. What breaks if you deploy with
    `composer install --no-dev --optimize-autoloader` and a production class references
    `App\Tests\Fixtures\SampleData`?

    - A. Nothing — `autoload-dev` rules are always dumped
    - B. A "class not found" error, because `--no-dev` omits the `autoload-dev` rules
    - C. A Composer validation error at install time
    - D. The class is found, but under `src/Tests/Fixtures/SampleData.php`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `autoload-dev` exists so that "classes needed to run the test suite
        should not be included in the main autoload rules to avoid polluting the autoloader
        in production". `--no-dev` therefore leaves those PSR-4 rules out of the generated
        autoloader, and a production reference to `App\Tests\…` fails at runtime with a
        class-not-found error. The lesson: never reference test-only namespaces from `src/`.

        **A** contradicts the purpose of the split. **C** is wrong because Composer has no
        way to know at install time which classes your code will reference. **D** is the
        subtle one: Composer's `ClassLoader` tries the **longest** matching PSR-4 prefix
        first and shortens it segment by segment, so with `App\Tests\` gone it really does
        fall back to `App\` and probe `src/Tests/Fixtures/SampleData.php` — but that file
        does not exist, so the lookup fails and the outcome is still a class-not-found error,
        not a working relocation.

        **Official reference:** https://getcomposer.org/doc/04-schema.md#autoload-dev

---

<small>Back to the lesson: [Namespaces & Autoloading](namespaces.md) · [Guided exercises](namespaces-exercises.md) · [Review flashcards](namespaces-flashcards.md)</small>

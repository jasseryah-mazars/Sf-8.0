# Flashcards — Namespaces & Autoloading

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Namespaces & Autoloading](namespaces.md)** ·
    Practice: **[Guided exercises](namespaces-exercises.md)** ·
    Test: **[Topic exam](namespaces-exam.md)**

## Definitions and roles

??? question "What problem do namespaces solve, in the manual's own words?"
    Think before revealing the answer.

    ??? success "Show answer"
        Two problems for library and application authors: **name collisions** between your
        code and internal PHP or third-party classes/functions/constants, and the ability to
        **alias or shorten** the long names people used to invent to avoid those collisions.

        **Why it matters:** it explains why aliasing (`as`) is part of the feature rather than
        a nicety — the second problem is half the reason namespaces exist.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.rationale.php

??? question "Which kinds of code are actually affected by a namespace declaration?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only **classes** (including abstract classes, traits and enums), **interfaces**,
        **functions** and **constants**. Variables, for instance, are unaffected.

        **Why it matters:** a namespaced file does not "namespace everything in it". `$foo`
        is still just `$foo`, and `define()`d constants do not automatically join the
        namespace either.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.definition.php

## The three kinds of name

??? question "Define unqualified, qualified and fully qualified names — with an example of each."
    Think before revealing the answer.

    ??? success "Show answer"
        - **Unqualified:** no separator at all — `Foo`.
        - **Qualified:** contains a separator but does not start with one — `Foo\Bar`.
        - **Fully qualified:** starts with a separator — `\Foo\Bar`.

        A fourth form exists: a **relative name**, starting with the keyword — `namespace\Foo`.

        **Why it matters:** the resolution rules are written per name kind. Misclassifying a
        name is the fastest way to get a resolution question wrong.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.rules.php

??? question "Inside `namespace App\Reporting;`, what does the qualified name `Reporting\Formatter` resolve to?"
    Think before revealing the answer.

    ??? success "Show answer"
        `App\Reporting\Reporting\Formatter` — the current namespace is prepended to the
        *whole* qualified name (assuming no import matches its first segment).

        **Why it matters:** "qualified" feels absolute and is not. Only a leading `\` makes a
        name absolute; everything else is relative to where you are standing.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.basics.php

??? question "Fully qualified names and `use`: which one wins?"
    Think before revealing the answer.

    ??? success "Show answer"
        Neither — they never meet. "Fully qualified names always resolve to the name without
        leading namespace separator", and imports affect **only** unqualified and qualified
        names. After `use My\Full\Classname as Another;`, `new Another\thing` is
        `My\Full\Classname\thing` but `new \Another\thing` is `Another\thing`.

        **Why it matters:** it is the reason library code writes `\strlen()` and
        `\Exception` — a leading backslash is immunity from both the current namespace and
        any import in the file.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

## The global fallback

??? question "Which symbol kinds fall back to the global namespace, and which do not?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Functions and constants fall back. Classes never do.** For an unqualified function
        or constant, PHP tries the current namespace and then the global one; for a class
        name it prepends the current namespace and stops there.

        **Why it matters:** this single asymmetry generates more exam questions than any
        other namespace rule. `strlen()` works unqualified inside a namespace; `new
        DateTime()` does not.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.fallback.php

??? question "In `namespace A\B;`, in what order is an unqualified `foo()` resolved?"
    Think before revealing the answer.

    ??? success "Show answer"
        Function import table first (if `use function` matched, resolution ends there).
        Otherwise it is resolved **at runtime**: `A\B\foo()`, then the global `foo()`.

        **Why it matters:** "current namespace first" is what makes shadowing possible — the
        manual's example defines `A\B\C\strlen()` that internally calls `\strlen()`. Reverse
        the order and that pattern could not exist.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.rules.php

??? question "Why does `\strlen()` sometimes appear instead of `strlen()` in framework code?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because the leading backslash makes the name fully qualified, so the engine skips the
        current-namespace lookup and binds the global function directly — and it removes any
        possibility of a same-named function in the current namespace shadowing it.

        **Why it matters:** it is a correctness guarantee first and a micro-optimisation
        second. Symfony and Composer both use this style in hot paths.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.global.php

??? question "In PHP 8.4, what happens when an unqualified constant is found neither in the current namespace nor globally?"
    Think before revealing the answer.

    ??? success "Show answer"
        An `Error` is thrown — e.g. `Undefined constant "bar\FOO"`. Before PHP 8.0 an
        undefined bare-word constant degraded into a string (deprecated in 7.2).

        **Why it matters:** older material — including some namespace examples still phrased
        for PHP 5 — describes a notice and a bare-word fallback. On a PHP 8.4 exam that
        answer is wrong.

        **Official reference:** https://www.php.net/manual/en/language.constants.php

## Importing and aliasing

??? question "What exactly does a `use` statement do, and when?"
    Think before revealing the answer.

    ??? success "Show answer"
        It adds one alias to the file's import table, **at compile time**. It performs no
        I/O, loads nothing, instantiates nothing and registers nothing.

        **Why it matters:** every distractor claiming `use` "loads the class file" is wrong
        for this one reason. The file is read later, by the autoloader, when the symbol is
        first referenced at runtime.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "How many import tables does PHP keep, and what fills each?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Three:** class-like names (`use X;`), functions (`use function X;`) and constants
        (`use const X;`). Unqualified names are translated "according to the current import
        table **for the respective symbol type**".

        **Why it matters:** `use C\E as F;` followed by `F()` does *not* call anything in
        `C\E` — the function table was never filled, so the call falls through to `A\F()`
        then global `F()`.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.rules.php

??? question "Which symbol kinds can `use` import?"
    Think before revealing the answer.

    ??? success "Show answer"
        Constants, functions, classes, interfaces, traits, enums and namespaces — the
        manual lists exactly these.

        **Why it matters:** "only classes can be imported" is a plausible-sounding distractor,
        and importing a *namespace* (`use My\Full\NSname;` then `NSname\subns\func()`) is a
        real, underused form.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "Does `use App\Foo;` make `App\Foo\Bar` available as `Bar`?"
    Think before revealing the answer.

    ??? success "Show answer"
        No. It aliases exactly one name. `Bar` alone still resolves against the current
        namespace; what *does* work is the qualified `Foo\Bar`, because the first segment of
        a qualified name goes through the import table.

        **Why it matters:** imports are not recursive over a namespace tree, and PHP has no
        wildcard import at all.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "Write the group-use equivalent of three imports from `some\ns` (one aliased)."
    Think before revealing the answer.

    ??? success "Show answer"
        `use some\ns\{ClassA, ClassB, ClassC as C};`

        The same shape exists per table: `use function some\ns\{fn_a, fn_b};` and
        `use const some\ns\{ConstA, ConstB};`.

        **Why it matters:** group `use` declarations arrived in PHP 7.0 and are the only
        grouping syntax — there is no `use some\ns\*;`.

        **Official reference:** https://www.php.net/manual/en/migration70.new-features.php#migration70.new-features.group-use-declarations

??? question "Where may a `use` statement appear, and does an `include`d file inherit imports?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only in the outermost scope of the file or inside a namespace declaration — never in
        a function or other block, because importing is compile-time and cannot be block
        scoped. And no: "Importing rules are per file basis, meaning included files will
        **NOT** inherit the parent file's importing rules."

        **Why it matters:** the per-file rule is why every Symfony class file repeats its own
        `use` block, and why a `use` in a bootstrap file helps nothing downstream.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "Is a leading backslash allowed inside a `use` statement — `use \My\Full\Classname;`?"
    Think before revealing the answer.

    ??? success "Show answer"
        It is **allowed** but "unnecessary and not recommended", because import names must
        already be fully qualified and are never processed relative to the current namespace.

        **Why it matters:** a common half-truth is that the leading backslash there is a
        syntax error. It is not — it is a style violation, which makes it a poor exam answer
        if the option says "fatal error".

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

??? question "What fails when an import and a class declaration share a short name in the same file?"
    Think before revealing the answer.

    ??? success "Show answer"
        A fatal error: `Cannot redeclare class App\Mailer (previously declared as local
        import)`. "Import names must not conflict with classes defined in the same file" —
        but the same import is perfectly legal if the colliding class lives in a *different*
        file.

        **Why it matters:** the "same file" qualifier is the whole point. The rule is about
        the file's import table, not about global uniqueness.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.faq.php#language.namespaces.faq.conflict

## Dynamic names

??? question "Do imports apply to a class name held in a string?"
    Think before revealing the answer.

    ??? success "Show answer"
        No. "Importing is performed at compile-time, and so does not affect dynamic class,
        function or constant names." After `use My\Full\Classname as Another;`,
        `$a = 'Another'; new $a;` instantiates a class literally called `Another`.

        **Why it matters:** it is the cleanest illustration of "compile time versus runtime"
        in the whole chapter — and the reason `Foo::class` exists.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.dynamic.php

??? question "Is a dynamic class name relative to the current namespace?"
    Think before revealing the answer.

    ??? success "Show answer"
        No — it is always treated as **fully qualified**. "There is no difference between a
        qualified and a fully qualified Name inside a dynamic class name", so the leading
        backslash is unnecessary and nothing is prepended.

        **Why it matters:** inside `namespace App;`, the literal `new DateTimeImmutable()`
        fails while `$c = 'DateTimeImmutable'; new $c();` succeeds. Same words, opposite
        outcomes.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.dynamic.php

??? question "Why is a double-quoted class name such as `dangerous\name` a hazard?"
    Think before revealing the answer.

    ??? success "Show answer"
        Inside a double-quoted string the backslash is an escape character, so `\n` becomes a
        newline. Always double the backslashes (`"dangerous\\name"`) or use single quotes.

        **Why it matters:** the resulting "class not found" names a string containing a line
        break, which is baffling until you know this rule.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.faq.php#language.namespaces.faq.quote

## The `namespace` operator and `__NAMESPACE__`

??? question "What does `__NAMESPACE__` contain, in a namespace and in global code?"
    Think before revealing the answer.

    ??? success "Show answer"
        The current namespace name as a string, **without** a leading separator — e.g.
        `"MyProject"`. In global, un-namespaced code it is the **empty string**.

        **Why it matters:** it is the building block for dynamic name construction
        (`__NAMESPACE__ . '\\' . $classname`), and the empty-string case is a favourite
        distractor against `"\\"` or `"global"`.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.nsconstants.php

??? question "What is the `namespace` keyword used as an operator, and what is it analogous to?"
    Think before revealing the answer.

    ??? success "Show answer"
        It explicitly requests an element from the current namespace or a sub-namespace:
        `namespace\func()`, `namespace\sub\cname::method()`. The manual calls it "the
        namespace equivalent of the `self` operator for classes".

        **Why it matters:** it bypasses the import table, so it is the way to say "the one in
        *my* namespace" even when an alias of the same short name exists.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.nsconstants.php

## File structure rules

??? question "What may appear before a `namespace` declaration in a file?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only a `declare` statement. No other code, and no non-PHP output — "including extra
        whitespace". Anything else gives
        `Namespace declaration statement has to be the very first statement or after any
        declare call in the script`.

        **Why it matters:** it is the concrete reason a single blank line before `<?php`
        takes a page down, and why the canonical file header is `declare(strict_types=1);`
        then `namespace`.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.definition.php

??? question "How do you combine namespaced and global code in one file?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only with the **bracketed** syntax: wrap the global code in an unnamed
        `namespace { … }` block. No PHP code may sit outside the braces except an opening
        `declare`, and bracketed and unbracketed declarations may never be mixed in the same
        file.

        **Why it matters:** mixing the two syntaxes is a distinct fatal — `Cannot mix
        bracketed namespace declarations with unbracketed namespace declarations` — and it is
        an easy configuration-consequence question.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.definitionmultiple.php

??? question "Are nested namespaces allowed, and can one namespace span several files?"
    Think before revealing the answer.

    ??? success "Show answer"
        Nesting is **not** allowed — write `namespace my\stuff\nested;` instead of nesting two
        blocks. But "unlike any other PHP construct, the same namespace may be defined in
        multiple files", which is what lets a namespace map onto a whole directory.

        **Why it matters:** the two facts look contradictory until you separate *syntax*
        (one declaration, hierarchical name) from *content* (spread across many files) — and
        the second is what makes PSR-4 possible at all.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.definition.php

## Autoloading, Composer and Symfony

??? question "State the PSR-4 transformation from class name to file path."
    Think before revealing the answer.

    ??? success "Show answer"
        Strip the mapped **namespace prefix**, replace the remaining `\` with the directory
        separator, append `.php`, and resolve against the mapped **base directory**. The
        prefix is *not* repeated inside the path — with `App\` → `src/`,
        `App\Service\Mailer` is `src/Service/Mailer.php`.

        **Why it matters:** "the prefix (`Foo\`) is not present in the file path" is the one
        sentence that separates PSR-4 from PSR-0, and the distractor is always
        `src/App/Service/Mailer.php`.

        **Official reference:** https://getcomposer.org/doc/04-schema.md#psr-4

??? question "Why must a PSR-4 namespace prefix end with a backslash?"
    Think before revealing the answer.

    ??? success "Show answer"
        To avoid collisions between similar prefixes: without the trailing `\`, `Foo` would
        also match classes in the `FooBar` namespace. `Foo\` and `FooBar\` are distinct.
        Symfony enforces the same rule for service discovery — `FileLoader::registerClasses()`
        throws `Namespace prefix must end with a "\"`.

        **Why it matters:** it is a small rule with a visible failure mode in both Composer
        and the Symfony container.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/Loader/FileLoader.php

??? question "What is the difference between `autoload` and `autoload-dev`?"
    Think before revealing the answer.

    ??? success "Show answer"
        `autoload-dev` holds rules needed only to run the test suite, kept out of the main
        rules "to avoid polluting the autoloader in production". In the Symfony skeleton,
        `autoload` maps `App\` → `src/` and `autoload-dev` maps `App\Tests\` → `tests/`.
        `--no-dev` omits the dev rules from the dumped autoloader.

        **Why it matters:** referencing an `App\Tests\…` class from `src/` works locally and
        fails in production — a class-not-found error with no code change to blame.

        **Official reference:** https://getcomposer.org/doc/04-schema.md#autoload-dev

??? question "`--optimize` versus `--classmap-authoritative`: what does each do?"
    Think before revealing the answer.

    ??? success "Show answer"
        `--optimize` (Level 1) converts PSR-4/PSR-0 rules into an explicit class map, so
        known classes resolve without a filesystem check. `--classmap-authoritative`
        (Level 2/A) enables Level 1 **and** declares the map final: a class absent from it is
        considered not to exist, with no PSR-4 filesystem fallback.

        **Why it matters:** Symfony recommends
        `composer dump-autoload --no-dev --classmap-authoritative` in production — but
        anything generating classes at runtime will break under it.

        **Official reference:** https://symfony.com/doc/8.0/performance.html

??? question "In a default Symfony 8 app, what is a service's id, and why does the namespace decide it?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **fully-qualified class name**. The default `App\: resource: '../src/'` import
        "creates a service per class whose id is the fully-qualified class name", and
        autowiring "looks for a service whose id exactly matches the type-hint".

        **Why it matters:** renaming a namespace renames a container key. The namespace is
        not documentation in Symfony — it is the autoloader's path, the service id and the
        autowiring key at the same time.

        **Official reference:** https://symfony.com/doc/8.0/service_container/autowiring.html

??? question "Symfony says it expected to find a class in a file and tells you to check the namespace prefix used with the resource. What went wrong?"
    Think before revealing the answer.

    ??? success "Show answer"
        The file's declared namespace does not match its path. Service discovery derives the
        expected class name from the **path** (prefix + relative path with `/` → `\`, minus
        `.php`) and then asks reflection for it; the file declares a different name, so
        nothing is found.

        **Why it matters:** the exception names a class you never wrote, which is confusing
        until you know the name was computed, not read. Fix the `namespace` line, not the
        loader.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/Loader/FileLoader.php

??? question "What does `spl_autoload_register()` build, and in what order do loaders run?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **queue** of autoload callbacks, run "in the order they are defined". A loader that
        does not recognise a class should simply return so the next one gets a turn; the
        optional `prepend` argument puts a loader at the front instead.

        **Why it matters:** it is why Composer's loader coexists with any custom loader, and
        why a well-behaved loader never throws for a class that is not its responsibility.

        **Official reference:** https://www.php.net/manual/en/function.spl-autoload-register.php

## Memory hooks

??? question "One sentence to remember the fallback rule."
    Think before revealing the answer.

    ??? success "Show answer"
        **Verbs fall back, nouns do not.** Functions and constants (the things you *call* and
        *read*) drop to the global space; class names (the things you *name*) never do.

        **Why it matters:** it compresses the single most examined rule of the chapter into
        four words, and it also predicts the fix: give the noun its full address (`\DateTime`
        or a `use`).

        **Official reference:** https://www.php.net/manual/en/language.namespaces.fallback.php

??? question "One sentence to remember what `use` costs."
    Think before revealing the answer.

    ??? success "Show answer"
        **`use` is a nickname, not a delivery.** It teaches the compiler a shorter name; the
        file arrives later, and only if you actually ask for the class.

        **Why it matters:** it settles, in one image, every question about whether `use`
        loads, includes, instantiates or registers anything.

        **Official reference:** https://www.php.net/manual/en/language.namespaces.importing.php

---

<small>Back to the lesson: [Namespaces & Autoloading](namespaces.md) · [Retake the topic exam](namespaces-exam.md) · Continue to the next topic: [PHP Extensions](extensions.md)</small>

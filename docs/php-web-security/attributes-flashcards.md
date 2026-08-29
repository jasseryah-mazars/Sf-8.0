# Flashcards — Attributes

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Attributes](attributes.md)** ·
    Practice: **[Guided exercises](attributes-exercises.md)** ·
    Test: **[Topic exam](attributes-exam.md)**

## What an attribute is

??? question "What is an attribute, in one sentence?"
    Think before revealing the answer.

    ??? success "Show answer"
        Compiled **metadata**: a class name plus constant-expression arguments, attached to a
        declaration. It never runs by itself.

        **Why it matters:** every other rule follows from "inert until read". Declaring an
        attribute executes nothing.

        **Official reference:** https://www.php.net/manual/en/language.attributes.php

??? question "What single call actually constructs the attribute object?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`newInstance()`**. `getAttributes()` returns descriptors only.

        **Why it matters:** the constructor never runs at parse time or on method invocation —
        both are standard distractors.

        **Official reference:** https://www.php.net/manual/en/reflectionattribute.newinstance.php

??? question "Does `newInstance()` cache?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No** — two calls, two distinct objects.

        **Why it matters:** reading attributes in a hot loop constructs objects repeatedly, which
        is exactly why frameworks read them once at compile time and cache the result themselves.

        **Official reference:** https://www.php.net/manual/en/reflectionattribute.newinstance.php

## Where validation happens — the core theme

??? question "When is a user-land attribute on a forbidden target detected?"
    Think before revealing the answer.

    ??? success "Show answer"
        At **`newInstance()`**, as an `Error: Attribute "X" cannot target ...` — **not** at parse
        time.

        **Why it matters:** the compiler validates nothing for user-land attributes. Expecting a
        compile error is the single most common wrong answer in this topic.

        **Official reference:** https://www.php.net/manual/en/language.attributes.classes.php

??? question "Which attribute failures ARE caught by the compiler?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only those on **built-in** attributes — for example `#[\Override]` on a method that
        overrides nothing.

        **Why it matters:** it is the one exception to "validated on read", and it defines the
        boundary: **user-land validated on read, built-in validated by the compiler.**

        **Official reference:** https://www.php.net/manual/en/language.attributes.php

??? question "A non-repeatable attribute is applied twice — what does `getAttributes()` return?"
    Think before revealing the answer.

    ??? success "Show answer"
        **All** occurrences. The repetition error surfaces only at `newInstance()`.

        **Why it matters:** `getAttributes()` reports what is written, it does not police it —
        so the count you get is not evidence that the usage is legal.

        **Official reference:** https://www.php.net/manual/en/language.attributes.reflection.php

## Flags

??? question "What is the value of `TARGET_ALL`, and does it include `IS_REPEATABLE`?"
    Think before revealing the answer.

    ??? success "Show answer"
        `TARGET_ALL` is **63**. `IS_REPEATABLE` is a **separate** bit, **64**, and is **not**
        included.

        **Why it matters:** "may appear anywhere" and "may appear more than once" are orthogonal,
        so repeatability must always be added explicitly.

        **Official reference:** https://www.php.net/manual/en/class.attribute.php

??? question "What does `TARGET_CLASS` cover beyond plain classes?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Interfaces, traits and enums** — every class-like declaration.

        **Why it matters:** it is broader than the name suggests, so restricting an attribute to
        `TARGET_CLASS` does not restrict it to classes alone.

        **Official reference:** https://www.php.net/manual/en/class.attribute.php

??? question "What does `TARGET_CLASS_CONSTANT` cover, and since when are class constants targetable?"
    Think before revealing the answer.

    ??? success "Show answer"
        It covers class constants **and enum cases** (which are class constants at the language
        level). Targetable since **PHP 8.0**, not 8.3.

        **Why it matters:** 8.3 gave class constants *types*; that is a different fact about the
        same feature, and the two merge easily under pressure.

        **Official reference:** https://www.php.net/manual/en/class.attribute.php

## Reflection API

??? question "`getArguments()` versus `newInstance()`"
    Think before revealing the answer.

    ??? success "Show answer"
        `getArguments()` evaluates the constant expressions and returns plain values — the
        attribute class need not exist. `newInstance()` autoloads it, validates target and
        repetition, then constructs.

        **Why it matters:** `getArguments()` is cheap and total; `newInstance()` is where every
        failure mode lives.

        **Official reference:** https://www.php.net/manual/en/class.reflectionattribute.php

??? question "What does `getAttributes()` return when nothing matches?"
    Think before revealing the answer.

    ??? success "Show answer"
        An **empty array** — never `null`, never `false`. A plain `foreach` is always safe.

        **Why it matters:** older PHP APIs return `null`/`false` on "nothing found", which makes
        those the natural wrong guesses.

        **Official reference:** https://www.php.net/manual/en/reflectionclass.getattributes.php

??? question "When is the `$flags` argument of `getAttributes()` honoured?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only when a **`$name`** is also passed. With `$name = null` the flag is **silently
        ignored**. `IS_INSTANCEOF` is its only accepted value.

        **Why it matters:** it fails silently — you get more attributes than you filtered for,
        and the bug appears far from its cause.

        **Official reference:** https://www.php.net/manual/en/reflectionclass.getattributes.php

??? question "What does `getTarget()` report?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **site of use** — the kind of declaration this occurrence sits on. Never the flags
        the attribute class permits.

        **Why it matters:** permitted targets live in the attribute class's own
        `#[\Attribute(...)]` declaration; reading `getTarget()` to discover them is the trap.

        **Official reference:** https://www.php.net/manual/en/reflectionattribute.gettarget.php

## Inheritance

??? question "Are class-level attributes inherited by subclasses?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** Neither by subclasses nor by implementers. Reflection on the child reports only
        what is written on the child.

        **Why it matters:** it looks like a reflection bug the first time you hit it. Walking
        `getParentClass()` yourself is how frameworks implement inheritance-aware lookup.

        **Official reference:** https://www.php.net/manual/en/language.attributes.reflection.php

## Arguments

??? question "What kind of expression may an attribute argument be?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **constant expression** — plus `new`, which was explicitly permitted from **PHP 8.1**.
        Arbitrary function calls are not allowed.

        **Why it matters:** `new` is a deliberate addition to the permitted set, not a general
        relaxation of the constant-expression rule.

        **Official reference:** https://www.php.net/manual/en/language.attributes.syntax.php

??? question "When are attribute arguments evaluated?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Lazily** — when `getArguments()` or `newInstance()` runs. Nothing is evaluated at
        declaration.

        **Why it matters:** it is the same "inert until read" principle applied to the arguments
        rather than the class.

        **Official reference:** https://www.php.net/manual/en/language.attributes.syntax.php

## Symfony usage

??? question "Which flags does Symfony's `#[Route]` declare?"
    Think before revealing the answer.

    ??? success "Show answer"
        `IS_REPEATABLE | TARGET_CLASS | TARGET_METHOD` — valid on a class (path prefix) and on a
        method (the action), and repeatable so one action can expose several paths.

        **Why it matters:** the distractors drop either the class-level prefix or the
        repeatability that makes multi-path actions possible.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Attribute/Route.php

??? question "When does Symfony read attributes like `#[AsCommand]`?"
    Think before revealing the answer.

    ??? success "Show answer"
        Once at **container compile time**, with the result baked into the compiled container —
        not on every request.

        **Why it matters:** it follows directly from `newInstance()` being uncached, and it
        explains why a new attribute sometimes does nothing until the cache is cleared.

        **Official reference:** https://symfony.com/doc/8.0/console.html

## Memory hooks

??? question "One sentence covering when attribute errors surface"
    Think before revealing the answer.

    ??? success "Show answer"
        **"User-land attributes are validated on read; built-in attributes are validated by the
        compiler."**

        **Why it matters:** it settles the target, repetition and `#[\Override]` questions with a
        single rule instead of three memorised outcomes.

        **Official reference:** https://www.php.net/manual/en/language.attributes.php

??? question "Mnemonic for the three reflection methods"
    Think before revealing the answer.

    ??? success "Show answer"
        **"Read, evaluate, construct."** `getAttributes()` reads descriptors, `getArguments()`
        evaluates values, `newInstance()` constructs — and only the last one can throw.

        **Why it matters:** it orders the API by increasing cost and increasing risk, which is
        exactly the axis questions probe.

        **Official reference:** https://www.php.net/manual/en/class.reflectionattribute.php

---

<small>Back to the lesson: [Attributes](attributes.md) · [Retake the topic exam](attributes-exam.md) · Next topic: [Anonymous Functions & Closures](closures.md)</small>

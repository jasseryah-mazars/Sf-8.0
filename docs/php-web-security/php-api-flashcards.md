# Flashcards — PHP API (up to 8.4)

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[PHP API (up to 8.4)](php-api.md)** ·
    Practice: **[Guided exercises](php-api-exercises.md)** ·
    Test: **[Topic exam](php-api-exam.md)**

## Version dating — the highest-yield cards

??? question "Which PHP version does Symfony 8 require?"
    Think before revealing the answer.

    ??? success "Show answer"
        **PHP 8.4+.**

        **Why it matters:** it sets the baseline for every other answer. On 8.4 you may use
        hooks, asymmetric visibility and lazy objects unconditionally — and the 8.4
        deprecations apply to you.

        **Official reference:** https://symfony.com/doc/8.0/setup.html

??? question "Date these: `match`, attributes, enums, `readonly` property, `readonly class`"
    Think before revealing the answer.

    ??? success "Show answer"
        `match` **8.0** · attributes **8.0** · enums **8.1** · `readonly` **property** 8.1 ·
        `readonly class` **8.2**.

        **Why it matters:** `readonly` property versus `readonly` class is one version apart and
        is a routine swap in answer options.

        **Official reference:** https://www.php.net/manual/en/migration82.new-features.php

??? question "Date these: typed class constants, `#[\\Override]`, `json_validate()`"
    Think before revealing the answer.

    ??? success "Show answer"
        All three are **PHP 8.3**.

        **Why it matters:** 8.3 is a small release, so grouping its three headline features
        together is cheaper than memorising them separately.

        **Official reference:** https://www.php.net/manual/en/migration83.new-features.php

??? question "Date these: property hooks, asymmetric visibility, lazy objects, `#[\\Deprecated]`"
    Think before revealing the answer.

    ??? success "Show answer"
        All four are **PHP 8.4** — the current baseline.

        **Why it matters:** these are the newest features, so they are the most likely to appear
        as "does this even exist?" distractors.

        **Official reference:** https://www.php.net/manual/en/migration84.new-features.php

??? question "Union, intersection, DNF — which version each?"
    Think before revealing the answer.

    ??? success "Show answer"
        Union **8.0**, intersection **8.1**, DNF **8.2**. DNF exists because 8.1 could not mix
        an intersection with a union.

        **Why it matters:** union and intersection are one release apart and feel like a single
        feature — the standard distractor pair.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

## Enums

??? question "`from()` versus `tryFrom()` on an unknown value"
    Think before revealing the answer.

    ??? success "Show answer"
        `from()` throws **`\ValueError`**; `tryFrom()` returns **`null`**.

        **Why it matters:** it decides which one is safe for user input, and the pairing is
        asked constantly.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Under `strict_types=1`, what does `tryFrom()` do with an argument of the wrong TYPE?"
    Think before revealing the answer.

    ??? success "Show answer"
        It raises a **`TypeError`** — it does **not** return `null`. `tryFrom()` absorbs unknown
        *values*, never wrong *types*.

        **Why it matters:** "tryFrom never throws" is the tempting oversimplification, and this
        is the case that breaks it.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Is backed-enum lookup case-sensitive?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Yes** — an exact match on the backing value. `'ACTIVE'` does not find case `'active'`.

        **Why it matters:** normalise input *before* calling `from()`/`tryFrom()`, or valid
        user input fails for a reason that is invisible in the enum declaration.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

## match

??? question "How does `match` compare, and what happens when nothing matches?"
    Think before revealing the answer.

    ??? success "Show answer"
        It compares with **`===`** and throws **`\UnhandledMatchError`** when no arm matches and
        there is no `default`.

        **Why it matters:** both halves differ from `switch`, which compares loosely and falls
        through silently — that contrast is the reason `match` exists.

        **Official reference:** https://www.php.net/manual/en/control-structures.match.php

??? question "What happens with two `default` arms in one `match`?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **compile-time fatal error** — not a runtime one.

        **Why it matters:** the *timing* of the failure is the exam point: it never reaches
        execution, so no `try/catch` helps.

        **Official reference:** https://www.php.net/manual/en/control-structures.match.php

## readonly and asymmetric visibility

??? question "Since 8.4, what set-visibility does `readonly` imply?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`protected(set)`** — so a subclass may perform the one-time initialisation.

        **Why it matters:** any option saying "only the declaring class" describes ≤ 8.3 and is
        the intended trap on the 8.4 baseline.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "`readonly` versus `private(set)` — how many writes does each allow?"
    Think before revealing the answer.

    ??? success "Show answer"
        `readonly` allows exactly **one** write, ever. `private(set)` allows **many**, provided
        they come from inside the class.

        **Why it matters:** they look interchangeable and are not — one is an immutability
        guarantee, the other an encapsulation boundary.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "What does `private(set)` imply beyond the write scope?"
    Think before revealing the answer.

    ??? success "Show answer"
        It is implicitly **`final`** — a subclass cannot redeclare the property.

        **Why it matters:** nothing in the syntax says `final`, yet the subclass fails to
        compile. It is an invisible consequence.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "What two constraints does asymmetric visibility place on the property itself?"
    Think before revealing the answer.

    ??? success "Show answer"
        It must be **typed** and **non-static**. And the set scope may never be **wider** than
        the read scope.

        **Why it matters:** those are exactly the constraints distractors omit — and static
        support is not part of 8.4.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "Where may a `readonly` property be written a SECOND time?"
    Think before revealing the answer.

    ??? success "Show answer"
        Inside **`__clone()`**, since PHP 8.3 — so a clone can be given a fresh identity.

        **Why it matters:** a narrow, dateable exception to an otherwise absolute rule, which is
        precisely what makes it good question material.

        **Official reference:** https://www.php.net/manual/en/language.oop5.cloning.php

## Property hooks

??? question "Backed versus virtual hooked property — what decides which?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Backed** if a hook references the property itself (`$this->x`); **virtual** otherwise.
        A virtual property has no storage.

        **Why it matters:** it determines whether storage exists, which drives what
        serialisation and reflection can do with it.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

??? question "Can a property be both hooked and `readonly`?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No** — mutually exclusive, a compile-time fatal. Use asymmetric visibility instead.

        **Why it matters:** both are 8.4 features and look composable, so combining them is the
        natural wrong guess.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

## Type declarations and initialisers

??? question "Write a valid DNF type, and say why the parentheses are mandatory"
    Think before revealing the answer.

    ??? success "Show answer"
        `(A&B)|null`. Each intersection must be parenthesised before being unioned; a bare
        `A|B&C` is a **parse error** because PHP will not guess precedence between `|` and `&`.

        **Why it matters:** the wrong options are all shapes that *look* reasonable, so the rule
        has to be known rather than inferred.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

??? question "Where is `new` NOT allowed in an initialiser?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Property defaults and class constants.** It *is* allowed in parameter defaults, static
        variable initialisers and attribute arguments.

        **Why it matters:** the boundary is principled — a property default or class constant
        may be evaluated before any object exists, so it cannot construct one.

        **Official reference:** https://www.php.net/manual/en/language.oop5.decon.php

??? question "What is the status of `f(string $a = null)` in 8.4?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Deprecated.** Implicit nullability is gone — write `?string $a = null`.

        **Why it matters:** it was idiomatic for years, so the old form still appears in real
        codebases and in answer options.

        **Official reference:** https://www.php.net/manual/en/migration84.deprecated.php

## Standard library

??? question "What does `json_validate()` return, and why prefer it?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **`bool`**. It reports validity without building the decoded structure, so it uses far
        less memory than `json_decode()` on large payloads.

        **Why it matters:** the distractors are "returns the decoded value" and "returns `null`
        on success" — the latter borrowing `json_decode()`'s failure convention.

        **Official reference:** https://www.php.net/manual/en/function.json-validate.php

??? question "What does `#[\\Deprecated]` target, and what does it emit?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Functions, methods and class constants** — not properties. It emits
        **`E_USER_DEPRECATED`**.

        **Why it matters:** both halves are asked. The severity is `E_USER_DEPRECATED` because
        the deprecation comes from user-land code, not the engine.

        **Official reference:** https://www.php.net/manual/en/class.deprecated.php

??? question "Which version introduced first-class callable syntax `f(...)`?"
    Think before revealing the answer.

    ??? success "Show answer"
        **PHP 8.1.** It works for plain functions, methods, static methods and invokables.
        `Closure::fromCallable()` remains the pre-8.1 equivalent.

        **Why it matters:** the distractors restrict it to methods only, or misdate it to 8.0
        alongside `match`.

        **Official reference:** https://www.php.net/manual/en/functions.first_class_callable_syntax.php

## Memory hooks

??? question "One-line rule for dating a PHP feature under exam pressure"
    Think before revealing the answer.

    ??? success "Show answer"
        **"8.0 syntax, 8.1 types and enums, 8.2 readonly classes and DNF, 8.3 constants and
        Override, 8.4 properties."** One theme per release.

        **Why it matters:** version questions are pure recall with no derivable answer, so a
        thematic anchor beats a flat list.

        **Official reference:** https://www.php.net/manual/en/migration84.new-features.php

??? question "Mnemonic for `TypeError` versus `\\ValueError` on enum lookup"
    Think before revealing the answer.

    ??? success "Show answer"
        **"Wrong type → `TypeError`. Right type, unknown value → `\ValueError`"** — or `null`
        if you used `tryFrom()`.

        **Why it matters:** it settles the whole family of enum-lookup questions with one rule
        instead of four memorised outcomes.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

---

<small>Back to the lesson: [PHP API (up to 8.4)](php-api.md) · [Retake the topic exam](php-api-exam.md) · Next topic: [Object-Oriented Programming](oop.md)</small>

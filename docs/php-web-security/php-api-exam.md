# Topic Exam — PHP API (up to 8.4)

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because the exam is built on
    near-misses rather than definitions.

    Theory: **[PHP API (up to 8.4)](php-api.md)** ·
    Practice: **[Guided exercises](php-api-exercises.md)** ·
    Recall: **[Flashcards](php-api-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

Symfony 8 requires **PHP 8.4+**. Several questions turn on *which version* introduced a
feature, because adjacent versions are the standard distractor pair.

## Enums

??? question "Question 1"
    What does `Suit::tryFrom('X')` return when `X` is not a case?

    - A. It throws `\ValueError`
    - B. `null`
    - C. `false`
    - D. The first case

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `tryFrom()` is the non-throwing lookup: an unknown value yields
        `null`, which is what makes it safe for user input.

        **A** describes `from()`, the throwing sibling — that pairing is the whole point of the
        question. **C** confuses PHP's older `false`-on-failure convention with a method that
        returns `?static`. **D** invents a fallback that would silently corrupt data.

        One genuine subtlety: under `declare(strict_types=1)` passing an argument of the
        **wrong type** (say an `int` to a string-backed enum) raises a `TypeError` rather than
        returning `null` — `tryFrom()` only absorbs *unknown values*, not *wrong types*.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Question 2 · Trap"
    Which statement about `match` is correct?

    - A. It compares with `===` and throws `\UnhandledMatchError` when nothing matches
    - B. It falls through like `switch`
    - C. It uses loose `==` comparison
    - D. It cannot return a value

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `match` is an **expression**: it compares strictly with `===`, returns
        a value, and raises `\UnhandledMatchError` when no arm matches and no `default` exists.

        **B** and **C** both describe `switch`, which falls through and compares loosely — the
        exact contrast the construct was introduced to fix. **D** inverts its defining property.

        Worth adding: two `default` arms in one `match` is a **compile-time** fatal, not a
        runtime error.

        **Official reference:** https://www.php.net/manual/en/control-structures.match.php

## Visibility and properties

??? question "Question 3"
    What does `public private(set) int $n;` mean?

    - A. `$n` is readonly
    - B. `$n` can be read publicly but written only inside the declaring class
    - C. `$n` is invisible outside the class
    - D. `$n` is static

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** asymmetric visibility (PHP 8.4) sets a **stricter write scope than
        read scope** — public to read, private to write.

        **A** is close but wrong in an important way: `readonly` permits exactly **one** write
        ever, while `private(set)` permits **many** writes, as long as they come from inside
        the class. **C** describes plain `private`. **D** is unrelated — and asymmetric
        visibility is not even allowed on static properties in 8.4.

        Two constraints that distractors like to drop: the property must be **typed** and
        **non-static**, and the set scope may never be **wider** than the read scope.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "Question 4 · Trap"
    On PHP 8.4, which scope may perform the one-time initialisation of a `readonly` property?

    - A. Only the declaring class
    - B. The declaring class and its subclasses
    - C. Any scope, once
    - D. Only the constructor of the declaring class

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** as of **8.4**, `readonly` is implicitly **`protected(set)`**, so a
        child class may perform the initialisation.

        **A** and **D** describe PHP **≤ 8.3**, when the write was restricted to the declaring
        class — a correct answer for an older runtime and the intended trap on an 8.4 baseline.
        **C** would defeat the guarantee entirely.

        The narrow exception worth pairing with this: since 8.3, `__clone()` is the one place a
        `readonly` property may be written a *second* time.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "Question 5 · Edge case"
    Can a property declare both a hook and `readonly`?

    - A. Yes, the hook simply runs once
    - B. No — it is a compile-time fatal error
    - C. Yes, but only for a virtual property
    - D. Only when the property is also `final`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** hooks and `readonly` are **mutually exclusive**, and combining them
        fails at compile time. The manual explicitly redirects you to asymmetric visibility
        for the "read widely, write narrowly" case.

        **A**, **C** and **D** all assume composability. Both features shipped in 8.4 and look
        designed to combine, which is exactly why this is asked — the restriction has to be
        known, it cannot be derived.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

## Type declarations

??? question "Question 6 · Code analysis"
    Which type declaration is a valid DNF type?

    - A. `A|B&C`
    - B. `(A&B)|null`
    - C. `?A&B`
    - D. `A&?B`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** DNF (disjunctive normal form) requires each intersection to be
        **parenthesised** and then unioned. `(A&B)|null` is exactly that shape.

        **A** is a **parse error**: PHP refuses to guess precedence between `|` and `&`, which
        is precisely why the parentheses are mandatory. **C** and **D** try to apply nullable
        shorthand inside an intersection, which is not permitted — express it as a union with
        `null` instead.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

??? question "Question 7 · Multiple choice"
    Select every statement that is true on PHP 8.4.

    - A. Union types arrived in 8.0
    - B. Intersection types arrived in 8.1
    - C. DNF types arrived in 8.2
    - D. Intersection types arrived in 8.0, alongside unions

    ??? success "Show answer"
        **Correct answers:** A, B and C

        **Explanation:** the timeline is union **8.0** → intersection **8.1** → DNF **8.2**.
        DNF exists *because* 8.1 could not mix an intersection with a union.

        **D** is the false one and the intended trap: unions and intersections feel like one
        feature and are one version apart. Anchor them by their motivation — unions came with
        the 8.0 type-system push, intersections a year later, and DNF to reconcile the two.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

??? question "Question 8 · Trap"
    What is the status of `function f(string $a = null)` on PHP 8.4?

    - A. Valid and idiomatic
    - B. Deprecated — write `?string $a = null`
    - C. A fatal error
    - D. Valid only under `declare(strict_types=1)`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** **implicitly nullable parameters are deprecated in 8.4**. A `null`
        default used to silently widen the type to `?string`; that implicit widening now emits
        a deprecation and you must write the `?` yourself.

        **A** was true for years, which is what makes it convincing. **C** overshoots —
        deprecated code still runs. **D** invents a dependency: `strict_types` governs scalar
        coercion at call sites, not nullability of the declaration.

        **Official reference:** https://www.php.net/manual/en/migration84.deprecated.php

## Functions and initialisers

??? question "Question 9 · Edge case"
    Where may `new` **not** be used in an initialiser?

    - A. Parameter defaults
    - B. Property defaults and class constants
    - C. Static variable initialisers
    - D. Attribute arguments

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "new in initializers" (8.1) covers parameter defaults, static variable
        initialisers and attribute arguments — but **not property defaults or class constants**,
        which must remain constant expressions evaluated without running code.

        **A**, **C** and **D** are the three positions the feature *does* permit. The boundary
        is principled: a property default or class constant may be evaluated before any object
        exists, so it cannot construct one.

        **Official reference:** https://www.php.net/manual/en/language.oop5.decon.php

??? question "Question 10"
    What does `json_validate($s)` return?

    - A. The decoded array
    - B. A `stdClass`
    - C. A `bool` indicating whether the string is valid JSON
    - D. `null` on success

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** `json_validate()` (PHP 8.3) answers only "is this valid JSON?" without
        building the decoded structure, so it validates large payloads at far lower memory cost
        than `json_decode()`.

        **A** and **B** describe `json_decode()` with and without associative mode. **D**
        inverts the convention — `null` is what `json_decode()` returns on *failure*, and
        conflating the two is the trap.

        **Official reference:** https://www.php.net/manual/en/function.json-validate.php

??? question "Question 11 · Multiple choice"
    Which are valid targets for `#[\\Deprecated]`, and what does it emit?

    - A. Functions
    - B. Methods
    - C. Class constants
    - D. Properties

    ??? success "Show answer"
        **Correct answers:** A, B and C

        **Explanation:** `#[\Deprecated]` (PHP 8.4) targets **functions, methods and class
        constants**, and emits `E_USER_DEPRECATED` when the target is used.

        **D** is the false one: properties are not a supported target. The severity matters too
        — `E_USER_DEPRECATED`, not `E_DEPRECATED`, because the deprecation originates in
        user-land code rather than the engine.

        **Official reference:** https://www.php.net/manual/en/class.deprecated.php

## Version dating

??? question "Question 12 · Execution order"
    Place these on the right version: `match`, `enum`, `readonly class`, typed class constants,
    property hooks.

    - A. 8.0, 8.1, 8.2, 8.3, 8.4 respectively
    - B. 8.1, 8.1, 8.2, 8.3, 8.4 respectively
    - C. 8.0, 8.0, 8.1, 8.2, 8.3 respectively
    - D. 8.0, 8.1, 8.1, 8.3, 8.4 respectively

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `match` **8.0** · `enum` **8.1** · `readonly class` **8.2** · typed
        class constants **8.3** · property hooks **8.4**. One feature per release, in order.

        **B** misdates `match` to 8.1, drawn to `enum`'s year. **C** shifts everything a
        release early. **D** misdates `readonly class` to 8.1 — 8.1 gave `readonly`
        *properties*; the class-level shorthand came in 8.2.

        Anchor worth memorising: `readonly` **property** 8.1, `readonly` **class** 8.2.

        **Official reference:** https://www.php.net/manual/en/migration84.new-features.php

??? question "Question 13 · Debugging"
    A first-class callable `$fn = strlen(...);` is written on PHP 8.0 and fails. Why?

    - A. The syntax requires PHP 8.1
    - B. `strlen` cannot be referenced this way
    - C. It needs `Closure::fromCallable()` on every version
    - D. Only methods support the syntax, never plain functions

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** first-class callable syntax `f(...)` arrived in **PHP 8.1**. On 8.0 the
        literal `...` in that position is a parse error.

        **B** and **D** invent restrictions: the syntax works for plain functions, methods,
        static methods and invokables alike. **C** describes the pre-8.1 workaround — which
        still works, but is not *required* from 8.1 onward.

        **Official reference:** https://www.php.net/manual/en/functions.first_class_callable_syntax.php

??? question "Question 14 · Scenario"
    A Symfony 8 application must run on the minimum supported PHP. Which version, and what
    does that let you assume?

    - A. 8.1 — enums and readonly, but no hooks
    - B. 8.2 — DNF types, but no typed class constants
    - C. 8.4 — hooks, asymmetric visibility and lazy objects are all available
    - D. 8.3 — typed constants, but no asymmetric visibility

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** Symfony 8 requires **PHP 8.4+**, so every feature up to and including
        property hooks, asymmetric visibility and lazy objects is available unconditionally —
        no polyfill, no version guard.

        **A**, **B** and **D** each name a real PHP version with a correct feature description,
        which is what makes them plausible. They are wrong only about Symfony 8's floor. This
        matters practically: on 8.4 you may *use* these features, and on 8.4 the deprecations
        listed in this chapter *apply to you*.

        **Official reference:** https://symfony.com/doc/8.0/setup.html

??? question "Question 15 · Expert trap"
    `enum Status: string` has case `Active = 'active'`. What is `Status::from('ACTIVE')`?

    - A. `Status::Active` — backed enum lookup is case-insensitive
    - B. `null`
    - C. A `\ValueError`
    - D. A `TypeError`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** backed-enum lookup is an exact, case-**sensitive** match on the backing
        value. `'ACTIVE'` is not `'active'`, so `from()` throws `\ValueError`.

        **A** invents case-insensitivity that does not exist. **B** is what `tryFrom()` would
        return — the method pairing again. **D** is the right exception class for the wrong
        reason: a `TypeError` would come from passing an argument of the wrong *type* under
        `strict_types=1`, not from a valid string that happens to be unknown.

        The distinction to carry: **wrong type → `TypeError`; right type, unknown value →
        `\ValueError` (or `null` from `tryFrom()`).**

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

---

<small>Back to the lesson: [PHP API (up to 8.4)](php-api.md) · [Guided exercises](php-api-exercises.md) · [Review flashcards](php-api-flashcards.md)</small>

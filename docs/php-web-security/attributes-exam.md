# Topic Exam — Attributes

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because the exam is built on
    near-misses rather than definitions.

    Theory: **[Attributes](attributes.md)** ·
    Practice: **[Guided exercises](attributes-exercises.md)** ·
    Recall: **[Flashcards](attributes-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

The recurring theme: attributes are **inert metadata**, and almost every validation happens
at `newInstance()` rather than at parse time.

## When attributes run

??? question "Question 1"
    When does declaring `#[LogCall]` on a method run `LogCall`'s constructor?

    - A. Immediately when the file is parsed
    - B. The first time the method is called
    - C. Only when something calls `newInstance()` on the read attribute
    - D. Never — attributes cannot be instantiated

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** attributes are **inert metadata**. Declaring one stores a class name
        and its constant-expression arguments; nothing is constructed. `getAttributes()` returns
        descriptors, and `newInstance()` is the single call that actually builds the object.

        **A** assumes declaration equals execution — the central misconception. **B** invents a
        connection to method invocation that does not exist; the method can be called a million
        times without the attribute ever being instantiated. **D** overcorrects: they are
        ordinary classes and *are* instantiable, just only on demand.

        **Official reference:** https://www.php.net/manual/en/language.attributes.php

??? question "Question 2 · Edge case"
    What does `getAttributes()` return when no matching attribute is present?

    - A. An empty array
    - B. `null`
    - C. `false`
    - D. It throws `ReflectionException`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** absence is represented as an **empty list**, so a plain `foreach` over
        the result is always safe and needs no null guard.

        **B** and **C** import conventions from older PHP APIs that return `null` or `false` on
        "nothing found". **D** treats an ordinary, expected outcome as exceptional — reflection
        throws when you ask about something that does not *exist*, not when a lookup legitimately
        matches nothing.

        **Official reference:** https://www.php.net/manual/en/reflectionclass.getattributes.php

??? question "Question 3 · Trap"
    A **user-land** non-repeatable attribute is applied twice to the same method. When is this
    detected?

    - A. At parse time, as a compile error
    - B. At `newInstance()`, as an `Error`
    - C. Never — the second silently overwrites the first
    - D. At `getAttributes()`, which returns only the first occurrence

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** for **user-land** attributes the compiler validates nothing. Repetition
        is caught when you call `newInstance()`, which throws an `Error`. Crucially,
        `getAttributes()` still returns **all** occurrences — it reports what is written, it does
        not police it.

        **A** is true only for **built-in** attributes such as `#[\Override]`, which the compiler
        does check. That split is the entire point of the question. **C** and **D** both assume a
        silent resolution that never happens.

        **Official reference:** https://www.php.net/manual/en/language.attributes.reflection.php

??? question "Question 4 · Trap"
    A user-land attribute declared `TARGET_METHOD` is placed on a property. What happens?

    - A. A compile error when the file is parsed
    - B. Nothing until `newInstance()`, which throws `Error: Attribute ... cannot target ...`
    - C. `getAttributes()` skips it silently
    - D. It is allowed — `TARGET_*` flags are advisory only

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** same principle as Question 3. Target validation for user-land
        attributes happens inside `newInstance()`, not at parse time, and surfaces as an `Error`.

        **A** again describes built-in attributes only. **C** is wrong for the same reason
        `getAttributes()` returns duplicates — it reports, it does not filter. **D** is the
        overcorrection: the flags are genuinely enforced, just later than people expect.

        **Official reference:** https://www.php.net/manual/en/language.attributes.classes.php

## Flags and targets

??? question "Question 5"
    What is the numeric value of `TARGET_ALL`, and does it include `IS_REPEATABLE`?

    - A. 63, and it does **not** include `IS_REPEATABLE`
    - B. 64, and it includes `IS_REPEATABLE`
    - C. 127, which is every flag including `IS_REPEATABLE`
    - D. 32, and repeatability is implied

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `TARGET_ALL` is **63** — every target bit set. `IS_REPEATABLE` is a
        **separate** bit, **64**, and is deliberately excluded: "may appear anywhere" and "may
        appear more than once" are orthogonal.

        **B** swaps the two constants. **C** describes `TARGET_ALL | IS_REPEATABLE`, which is
        what you would write explicitly to get both — the fact that you must write it is the
        point. **D** invents a value and an implication.

        **Official reference:** https://www.php.net/manual/en/class.attribute.php

??? question "Question 6 · Multiple choice"
    Which are true about `TARGET_CLASS` and `TARGET_CLASS_CONSTANT`?

    - A. `TARGET_CLASS` also covers interfaces, traits and enums
    - B. `TARGET_CLASS_CONSTANT` also covers enum cases
    - C. Class constants became a legal attribute target in PHP 8.3
    - D. Class constants have been a legal target since PHP 8.0

    ??? success "Show answer"
        **Correct answers:** A, B and D

        **Explanation:**
        **A** — `TARGET_CLASS` is about class-*like* declarations, so interfaces, traits and
        enums are included.
        **B** — enum cases are class constants at the language level, so they fall under
        `TARGET_CLASS_CONSTANT`.
        **D** — class constants have been targetable since **8.0**, when attributes shipped.

        **C** is the false one: 8.3 gave class constants **types**, not attribute targetability.
        Two unrelated 8.3-adjacent facts about class constants, easy to merge under pressure.

        **Official reference:** https://www.php.net/manual/en/class.attribute.php

??? question "Question 7"
    `Symfony\Component\Routing\Attribute\Route` declares which flags?

    - A. `TARGET_ALL` only
    - B. `IS_REPEATABLE | TARGET_CLASS | TARGET_METHOD`
    - C. `TARGET_METHOD` only, not repeatable
    - D. `TARGET_PROPERTY | TARGET_PARAMETER`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `#[Route]` is valid on a **class** (where it contributes a path prefix)
        and on a **method** (the action itself), and it is **repeatable** so one action can expose
        several paths.

        **C** forgets both the class-level prefix and the repeatability that makes multi-path
        actions possible. **A** is broader than the real declaration — Symfony constrains it
        deliberately, so a misplaced `#[Route]` fails. **D** names targets routing has no use for.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Attribute/Route.php

## Reflection API

??? question "Question 8 · Code analysis"
    What is the difference between `getArguments()` and `newInstance()` on a `ReflectionAttribute`?

    - A. They are aliases
    - B. `getArguments()` evaluates the arguments; `newInstance()` also autoloads, validates and constructs
    - C. `getArguments()` constructs the object; `newInstance()` returns raw values
    - D. `getArguments()` works only on built-in attributes

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `getArguments()` evaluates the constant expressions and hands back plain
        values — the attribute class need not even exist. `newInstance()` does strictly more: it
        autoloads the class, validates target and repetition, then constructs it.

        **C** inverts the two. **A** ignores that only one of them can throw. **D** invents a
        restriction.

        The practical consequence: `getArguments()` is the cheap, total operation;
        `newInstance()` is where every failure mode lives.

        **Official reference:** https://www.php.net/manual/en/class.reflectionattribute.php

??? question "Question 9 · Edge case"
    Two consecutive `newInstance()` calls on the same `ReflectionAttribute` — same object or two?

    - A. The same instance; results are cached
    - B. Two distinct objects; nothing is cached
    - C. Same object only if the attribute is not repeatable
    - D. It throws on the second call

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `newInstance()` constructs a **new object every call**. There is no
        caching layer.

        **A** assumes memoisation that would be surprising for a method named `newInstance`.
        **C** ties caching to repeatability, which are unrelated. **D** invents a one-shot rule.

        Why it matters in practice: reading attributes inside a hot loop constructs objects
        repeatedly, which is exactly why frameworks read them **once at compile time** and cache
        the result themselves.

        **Official reference:** https://www.php.net/manual/en/reflectionattribute.newinstance.php

??? question "Question 10 · Configuration consequence"
    `getAttributes(null, \ReflectionAttribute::IS_INSTANCEOF)` is called. What happens?

    - A. It filters by `instanceof` as intended
    - B. The `$flags` argument is ignored because `$name` is `null`
    - C. It throws `ReflectionException`
    - D. It returns an empty array

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `$flags` is only honoured when a `$name` is supplied. With `null` there
        is no type to test `instanceof` against, so the flag is silently ignored and you get every
        attribute back.

        **A** is the intent people expect. **C** and **D** assume a loud failure or an empty
        result — the genuinely dangerous part is that it fails **silently**: you get more
        attributes than you filtered for, and the bug surfaces far from its cause.

        `IS_INSTANCEOF` is also the **only** accepted value for `$flags`.

        **Official reference:** https://www.php.net/manual/en/reflectionclass.getattributes.php

??? question "Question 11 · Trap"
    What does `ReflectionAttribute::getTarget()` report?

    - A. The `TARGET_*` flags the attribute class permits
    - B. The kind of declaration the attribute was actually written on
    - C. The fully-qualified name of the attribute class
    - D. Whether the attribute is repeatable

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `getTarget()` reports the **site of use** — the sort of declaration this
        particular occurrence sits on.

        **A** is the trap, and a natural misreading: the *permitted* targets live in the
        attribute class's own `#[\Attribute(...)]` declaration, reachable through reflection on
        that class, not through this occurrence. **C** is `getName()`. **D** is again part of the
        declaration, not the usage.

        **Official reference:** https://www.php.net/manual/en/reflectionattribute.gettarget.php

## Inheritance

??? question "Question 12 · Debugging"
    `#[Audited]` is on a parent class. `getAttributes(Audited::class)` on the **child** returns
    an empty array. Why?

    - A. The child must redeclare `#[Audited]` — class attributes are not inherited
    - B. `IS_INSTANCEOF` is required to see inherited attributes
    - C. The attribute must be `IS_REPEATABLE` to be inherited
    - D. It is a reflection bug; use `getParentClass()->getAttributes()` as a workaround

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** class-level attributes are **not inherited** by subclasses or
        implementers. Reflection on the child reports only what is written on the child.

        **B** confuses filtering with traversal — `IS_INSTANCEOF` narrows results by type, it
        does not walk the hierarchy. **C** invents a link to repeatability. **D** mislabels
        designed behaviour as a bug, though it accidentally names the correct *technique*:
        walking `getParentClass()` yourself is exactly how frameworks implement inheritance-aware
        attribute lookup, because the language does not do it for you.

        **Official reference:** https://www.php.net/manual/en/language.attributes.reflection.php

## Symfony usage

??? question "Question 13 · Scenario"
    When does Symfony read the `#[AsCommand]` attribute on a command class?

    - A. On every console invocation, at runtime
    - B. Once at container compile time, with the result cached
    - C. Only when the command is executed
    - D. Never — `#[AsCommand]` is documentation only

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** Symfony reads attributes during **container compilation** and bakes the
        result into the compiled container, so `bin/console list` does not reflect over every
        class on every run.

        **A** would make the console slow in exactly the way Question 9 explains —
        `newInstance()` is uncached, so per-request reflection is expensive. **C** is
        self-defeating: the name must be known *before* execution to route the command. **D** is
        wrong — it drives real registration.

        This is the practical reason a new attribute sometimes "does nothing" until the cache is
        cleared.

        **Official reference:** https://symfony.com/doc/8.0/console.html

??? question "Question 14 · Multiple choice"
    Which statements about attribute arguments are true?

    - A. They must be constant expressions
    - B. `new` may be used in them since PHP 8.1
    - C. They may call arbitrary functions at declaration time
    - D. They are evaluated lazily, when `newInstance()` or `getArguments()` runs

    ??? success "Show answer"
        **Correct answers:** A, B and D

        **Explanation:**
        **A** — arguments are constant expressions, which is why arbitrary runtime values are
        rejected.
        **B** — "new in initializers" (8.1) explicitly includes attribute arguments, one of the
        three permitted positions.
        **D** — nothing is evaluated at declaration; evaluation happens on read.

        **C** is the false one and contradicts **A**: a general function call is not a constant
        expression. The apparent tension with **B** is the interesting part — `new` was
        *specifically* added to the permitted set; it is not a general relaxation of the
        constant-expression rule.

        **Official reference:** https://www.php.net/manual/en/language.attributes.syntax.php

??? question "Question 15 · Expert trap"
    Which attribute failure IS caught by the compiler rather than at `newInstance()`?

    - A. A user-land attribute on a forbidden target
    - B. A user-land non-repeatable attribute applied twice
    - C. `#[\Override]` on a method that overrides nothing
    - D. None — the compiler never validates attributes

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** **built-in** attributes are compiler-checked. `#[\Override]` (PHP 8.3)
        fails compilation when the method does not actually override a parent method — that is
        its entire purpose.

        **A** and **B** are the two user-land cases from Questions 3 and 4, both deferred to
        `newInstance()`. **D** overgeneralises the user-land rule into an absolute one.

        The line to remember: **user-land attributes are validated on read; built-in attributes
        are validated by the compiler.**

        **Official reference:** https://www.php.net/manual/en/language.attributes.php

---

<small>Back to the lesson: [Attributes](attributes.md) · [Guided exercises](attributes-exercises.md) · [Review flashcards](attributes-flashcards.md)</small>

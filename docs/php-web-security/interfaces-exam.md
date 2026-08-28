# Topic Exam — Interfaces & Type Declarations

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because the exam is built on
    near-misses rather than definitions.

    Theory: **[Interfaces & Type Declarations](interfaces.md)** ·
    Practice: **[Guided exercises](interfaces-exercises.md)** ·
    Recall: **[Flashcards](interfaces-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4**.

## Variance

??? question "Question 1"
    A parent method is declared `public function adopt(): Animal`. Which return type may a
    child legally declare when overriding it?

    - A. `object`
    - B. `Cat`, a subclass of `Animal`
    - C. `mixed`
    - D. `Animal|Plant`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** return types are **covariant** — a child may only *narrow*. `Cat`
        is a subtype of `Animal`, so every caller expecting an `Animal` is still satisfied.

        **A** widens to `object`, **C** widens to `mixed` (the top type), and **D** widens by
        adding `Plant` to a union. All three would let the child return something that is not
        an `Animal`, breaking every caller — so all three are compile-time fatals.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "Question 2"
    An interface declares `public function feed(Dog $d): void`. Which parameter type may an
    implementation legally declare?

    - A. `Poodle`, a subclass of `Dog`
    - B. `Animal`, a superclass of `Dog`
    - C. `Dog&Trainable`
    - D. `never`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** parameters are **contravariant** — an implementation may accept a
        *wider* type. Every caller passing a `Dog` still type-checks, because a `Dog` is an
        `Animal`.

        **A** narrows: a caller holding a plain `Dog` would be refused, which the contract
        forbade. **C** also narrows — an intersection demands *more* than `Dog` alone. **D**
        is invalid outright: `never` is a **return-only** type and cannot be used on a
        parameter.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "Question 3 · True or false"
    Class properties are covariant, so a child class may redeclare an inherited `Animal`
    property as `Cat`.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — false

        **Explanation:** properties are **invariant** by default. A property supports both a
        read and a write: reads would require covariance, writes would require contravariance,
        and only invariance satisfies both simultaneously. Redeclaring the type is a fatal
        error.

        The narrow 8.4 exception is worth knowing precisely: an **abstract or virtual**
        property that requires only `get` may be covariant, and one requiring only `set` may
        be contravariant. As soon as both operations exist, invariance returns.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "Question 4 · Code analysis"
    Does this class link successfully?

    ```php
    class Foo {}
    class Bar extends Foo {}

    interface A { public function myfunc(Foo $arg): Foo; }
    interface B { public function myfunc(Bar $arg): Bar; }

    class MyClass implements A, B
    {
        public function myfunc(Foo $arg): Bar { return new Bar(); }
    }
    ```

    - A. No — two interfaces cannot declare the same method
    - B. No — the parameter conflicts with interface B
    - C. Yes — the parameter is wide enough for both and the return narrow enough for both
    - D. Yes, but only because `Bar` extends `Foo` and the return types are ignored

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** solve each axis separately. The parameter must be equal-or-wider
        than **both** requirements: `Foo` is wider than `Bar`, so `Foo` satisfies A and B.
        The return must be equal-or-narrower than **both**: `Bar` is narrower than `Foo`, so
        it satisfies both. Widest parameter, narrowest return — the only legal pairing.

        **A** is false: implementing two interfaces declaring the same method is allowed
        whenever one signature can satisfy both. **B** is the classic reversal — `Foo` is a
        *widening* of B's `Bar` parameter, which contravariance permits. **D** is wrong
        because return types are absolutely not ignored; returning `Foo` here would fatal
        against B.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

## Type declarations

??? question "Question 5"
    Which types may be combined in an intersection type such as `A&B`?

    - A. Any scalar and class types
    - B. Only class and interface types
    - C. Only scalar types
    - D. Only enum types

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** intersection types express "satisfies **all** of these contracts",
        which only makes sense for object types. The manual is explicit that using a
        non-class type in an intersection **results in an error**, and that `mixed` and
        `never` are rejected as members too.

        **A** fails on the scalar half — `int&Countable` is an error. **C** is impossible for
        the same reason. **D** is arbitrarily narrow: enums are class types and are allowed,
        but so is any interface or class.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

??? question "Question 6 · Multiple choice"
    Select all statements that are true in PHP 8.4.

    - A. DNF types such as `(A&B)|null` are supported
    - B. `never` may be used as a return type only
    - C. `false` and `null` may be used as standalone types
    - D. Intersection types were introduced in PHP 8.0

    ??? success "Show answer"
        **Correct answers:** A, B and C

        **Explanation:**
        **A** — DNF (disjunctive normal form) types arrived in **8.2**, which is what finally
        allowed an intersection to be combined with a union.
        **B** — `never` arrived in **8.1** as a *return-only* type; it is invalid on a
        parameter or property.
        **C** — `false` and `null` became usable standalone in **8.2**; before that a union of
        only those types was not permitted.
        **D** is the false one: intersection types arrived in **8.1**, not 8.0. 8.0 introduced
        *union* types — a very easy pair to swap under time pressure.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

??? question "Question 7"
    What does `'text' instanceof SomeClass` evaluate to?

    - A. A `TypeError`
    - B. `false`
    - C. `true`
    - D. `null`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `instanceof` short-circuits on a non-object left operand and simply
        returns `false`. It never raises for this, which makes it safe to use as a guard on a
        value of unknown type.

        **A** is the trap: people expect strict typing to throw here, but `instanceof` is an
        operator, not a type declaration. **C** is wrong regardless of the class. **D** is
        wrong because the operator always yields a boolean.

        Worth separating from a related case: `$obj instanceof $className` **does** work with
        a *variable* holding a class-name string — it is only a non-object on the **left**
        that returns `false`.

        **Official reference:** https://www.php.net/manual/en/language.operators.type.php

## Interface rules

??? question "Question 8"
    In PHP 8.4, may a class implementing an interface override one of that interface's
    constants?

    - A. Yes — allowed since PHP 8.1.0
    - B. No — interface constants are always final
    - C. Only if the constant is untyped
    - D. Only if the class also declares the constant `final`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** overriding an interface constant in an implementing class was
        **forbidden before PHP 8.1.0** and is permitted from 8.1.0 onward. The manual's own
        example prints `Interface constant` from the interface and `Class constant` from the
        implementer.

        **B** describes pre-8.1 behaviour and is the intended distractor — a question written
        against an older PHP is testing the version, not the concept. **C** invents a
        restriction: typed constants (8.3) may be overridden too, provided the value still
        satisfies the declared type. **D** inverts the meaning of `final`, which *prevents*
        further overriding rather than enabling it.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "Question 9 · Code analysis"
    Is this interface declaration valid in PHP 8.4, and what does it require?

    ```php
    interface HasSlug
    {
        public string $slug { get; }
    }
    ```

    - A. Invalid — interfaces cannot declare properties
    - B. Valid — it requires a publicly readable `string $slug`
    - C. Valid — it requires a public property that is both readable and writeable
    - D. Valid, but only for abstract classes, not interfaces

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** **as of PHP 8.4.0 interfaces may declare properties**, and the
        declaration must state which operations are required. `{ get; }` demands a publicly
        *readable* `string $slug` and says nothing about writing.

        An implementer may satisfy it with a plain public property, with a **virtual**
        property implementing only the `get` hook, or with a `readonly` property.

        **A** was true up to 8.3 and is now the headline distractor. **C** would require
        `{ get; set; }`. **D** invents a restriction — the feature is specifically about
        interfaces.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "Question 10 · Edge case"
    An interface declares `public string $slug { set; }`. Can a `readonly` property satisfy it?

    - A. Yes — `readonly` properties are still settable once
    - B. No — `readonly` cannot satisfy a settable requirement
    - C. Yes, but only from inside the constructor
    - D. Only if the property is also declared `static`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** an interface property that is **settable may not be satisfied by a
        `readonly` property**. The contract advertises to *callers* that they may write to
        this property; `readonly` forbids exactly that after initialisation, so the guarantee
        cannot be honoured.

        **A** and **C** both confuse *initialisation* with the *public writeability* the
        contract promises: a one-time write inside the constructor is not what `{ set; }`
        offers callers. **D** is unrelated — and `readonly` static properties are not a thing.

        Note the asymmetry, which is the actual exam point: `readonly` **can** satisfy
        `{ get; }`, never `{ set; }`.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "Question 11"
    Can one class implement two interfaces that declare a method with identical signatures?

    - A. Yes, if it provides one compatible implementation
    - B. No, it is always a conflict
    - C. Only by resolving it with `insteadof`
    - D. Only when the method is static

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** identical signatures are trivially compatible, so a single
        implementation satisfies both contracts at once. Nothing special is needed.

        **B** overstates the rule — a genuine conflict arises only when no single signature
        can satisfy both, or when two interfaces declare the *same constant* with different
        values. **C** confuses interfaces with **traits**: `insteadof` resolves trait method
        collisions and has no meaning here, because interfaces carry no bodies to collide.
        **D** is unrelated to visibility or staticness.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

## Execution and internals

??? question "Question 12 · Execution order"
    When is a variance violation between a class and its interface detected?

    - A. When the offending method is first called
    - B. When the class is linked — at compile or autoload time
    - C. When the object is first instantiated
    - D. Only under `declare(strict_types=1)`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the engine verifies every required signature while **linking** the
        class — when the declaration is compiled, or when the autoloader loads the file in a
        Symfony app. Simply autoloading the class is enough to trigger the fatal.

        **A** and **C** both assume laziness the engine does not have: it cannot let
        `instanceof` answer `true` for a class that does not actually satisfy the contract.
        **D** confuses two independent mechanisms — `strict_types` governs *scalar coercion
        at call sites*, not signature compatibility, which is always enforced.

        This is why a variance mistake takes down the whole application rather than one
        endpoint.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "Question 13 · Debugging"
    CI reports:

    ```
    Declaration of CsvExporter::export(Report $r): iterable must be
    compatible with Exporter::export(Report $r): \Generator
    ```

    What was violated, and what is the minimal fix?

    - A. Contravariance on the parameter — narrow `Report`
    - B. Covariance on the return — return `\Generator` or a subtype
    - C. Nothing; `iterable` and `\Generator` are interchangeable
    - D. The class must be declared `abstract`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** read the message positionally — the **left** side is your
        declaration, the **right** side is the contract. The parameters match, so the
        violation is on the return: `iterable` is **wider** than `\Generator` (an array
        satisfies `iterable` but is not a `Generator`), and widening a return breaks
        covariance.

        **A** misreads the message: the parameter is identical on both sides. **C** is the
        substantive trap — every `Generator` is `iterable`, but not the reverse, so they are
        not interchangeable and callers relying on `send()` or `getReturn()` would break.
        **D** would only postpone the problem to the first concrete subclass.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "Question 14 · Trap"
    A method declared `public function serialize(): never` overrides a contract declaring
    `: string`. Legal?

    - A. No — `never` is not a subtype of `string`
    - B. Yes — `never` is the bottom type and satisfies any return contract
    - C. Only if the method is also declared `final`
    - D. Only in an abstract class

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `never` marks a function that **cannot return at all** — it always
        throws or exits. Since it never produces a value, there is no value that could violate
        `: string`. It is the *bottom* type, making it the narrowest possible covariant
        override, valid against every return contract.

        **A** applies subtype intuition to the one type where it inverts: `never` sits below
        everything, not outside the hierarchy. **C** and **D** invent conditions — `final` and
        `abstract` are orthogonal to variance.

        Contrast with `void`, which *does* return, just without a value, and is **not** a
        legal override of `: string`.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

??? question "Question 15 · Scenario"
    A published library interface gains one new method in a minor release. What happens to
    applications that implement it?

    - A. Nothing until they call the new method
    - B. Every implementer fails to link, with a fatal error
    - C. PHP inserts a default no-op implementation
    - D. Only implementers using `declare(strict_types=1)` break

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** an interface is an all-or-nothing contract. Adding a method means
        every existing implementer is now missing one, and each fails at **link time** — the
        moment its file is autoloaded, before any call happens.

        **A** repeats the laziness misconception from Question 12. **C** describes behaviour
        PHP deliberately does not provide; the closest real mechanisms are a default method
        in an abstract class or a trait, neither of which an interface offers. **D** is
        unrelated — `strict_types` governs scalar coercion, not contract completeness.

        This is exactly why Symfony's [backward-compatibility promise](../architecture/bc-promise.md)
        treats published interfaces as frozen, and introduces new behaviour via a *new*
        interface instead.

        **Official reference:** https://symfony.com/doc/8.0/contributing/code/bc.html

---

<small>Back to the lesson: [Interfaces & Type Declarations](interfaces.md) · [Guided exercises](interfaces-exercises.md) · [Review flashcards](interfaces-flashcards.md)</small>

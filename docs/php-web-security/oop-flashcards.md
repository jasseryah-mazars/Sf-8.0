# Flashcards — Object-Oriented Programming

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Object-Oriented Programming](oop.md)** ·
    Practice: **[Guided exercises](oop-exercises.md)** ·
    Test: **[Topic exam](oop-exam.md)**

## Binding and resolution

??? question "`self::` versus `static::` — when is each resolved, and to what?"
    Think before revealing the answer.

    ??? success "Show answer"
        `self::` is resolved at **compile time** to the **defining** class. `static::` is
        resolved at **runtime** to the **called** class — late static binding.

        **Why it matters:** it decides which class a factory actually instantiates. `new self()`
        in a parent always builds the parent; `new static()` builds whichever subclass was called.

        **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

??? question "Which call forms *forward* the called class, and which reset it?"
    Think before revealing the answer.

    ??? success "Show answer"
        `self::`, `parent::`, `static::` and `forward_static_call()` **forward** the called
        class. Naming a class explicitly (`OtherClass::method()`) **resets** it to that class.

        **Why it matters:** a `self::` forwarding call still preserves late static binding —
        the common wrong assumption is that `self::` destroys it.

        **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

## Cloning

??? question "Is `clone` deep or shallow, and when does `__clone()` run?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Shallow.** Nested objects stay shared between original and copy. `__clone()` runs
        on the **copy**, *after* the shallow copy is made, and is where you deep-copy.

        **Why it matters:** two "independent" objects silently mutating the same nested object
        is a classic production bug and a favourite exam scenario.

        **Official reference:** https://www.php.net/manual/en/language.oop5.cloning.php

??? question "Where may a `readonly` property be written a second time?"
    Think before revealing the answer.

    ??? success "Show answer"
        Inside **`__clone()`** — since PHP 8.3 that is the one place a `readonly` property may
        be reassigned, so a clone can be given a fresh identity.

        **Why it matters:** without it, `readonly` and cloning were mutually exclusive. It is a
        narrow, dateable exception, which makes it good question material.

        **Official reference:** https://www.php.net/manual/en/language.oop5.cloning.php

## Magic methods

??? question "When does `__get()` actually fire?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only for **inaccessible or undeclared** properties. Never for a declared, visible
        property, and never for a property that has a `get` hook.

        **Why it matters:** "why isn't my `__get()` being called?" is almost always a property
        that is perfectly visible from the calling scope.

        **Official reference:** https://www.php.net/manual/en/language.oop5.overloading.php

??? question "What visibility must magic methods have?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`public`**, except `__construct`, `__destruct` and `__clone`, which may be
        restricted. Breaking the rule is an `E_WARNING`; a wrong **type declaration** on a
        magic method is a **fatal error**.

        **Why it matters:** the two failure severities are different, and questions exploit
        that — one degrades, the other stops the application.

        **Official reference:** https://www.php.net/manual/en/language.oop5.magic.php

## Constructor promotion

??? question "What does constructor property promotion do, and what can it not promote?"
    Think before revealing the answer.

    ??? success "Show answer"
        It declares the property **and** assigns it in one step, accepting any single
        modifier. It **cannot** promote a `callable`, because `callable` is not a valid
        property type.

        **Why it matters:** the `callable` exclusion follows from a property-type rule rather
        than a promotion rule, which is why it surprises people.

        **Official reference:** https://www.php.net/manual/en/language.oop5.decon.php

??? question "With a promoted parameter that has a default, what receives the default?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **parameter**, not the property. The property is only ever assigned from whatever
        the parameter ends up holding at call time.

        **Why it matters:** it is not equivalent to writing a property default, and reasoning
        about it as one leads to wrong answers on subclass and reflection questions.

        **Official reference:** https://www.php.net/manual/en/language.oop5.decon.php

## PHP 8.4 changes — prime distractor material

??? question "Since 8.4, `readonly` is implicitly which set-visibility?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`protected(set)`** — not `private(set)`. A child class may now perform the one-time
        initialisation.

        **Why it matters:** any option asserting "only the declaring class may initialise it"
        describes PHP ≤ 8.3 and is the intended trap on the 8.4 baseline.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "What does `private(set)` imply beyond the write scope?"
    Think before revealing the answer.

    ??? success "Show answer"
        It is **implicitly `final`** — a subclass cannot redeclare the property.

        **Why it matters:** it is an invisible consequence: nothing in the syntax says `final`,
        yet the subclass fails to compile.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "Can a property have both a hook and `readonly`?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No** — mutually exclusive, and a compile-time fatal. The manual redirects you to
        asymmetric visibility instead.

        **Why it matters:** both features arrived in 8.4 and look composable, so "combine
        them" is a natural and wrong guess.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

??? question "Backed versus virtual property — what decides which one you have?"
    Think before revealing the answer.

    ??? success "Show answer"
        A hooked property is **backed** if any hook references the property itself
        (`$this->x`), and **virtual** otherwise. A virtual property stores nothing.

        **Why it matters:** it decides whether storage exists at all, which drives what
        `readonly`, serialisation and reflection can do with it.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

??? question "May a static property use asymmetric visibility in PHP 8.4?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** Asymmetric visibility requires a **typed, non-static** property. Static support
        is a later addition and out of scope on the 8.4 baseline.

        **Why it matters:** the two constraints — typed and non-static — are exactly what
        distractors drop.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "May the set scope of an asymmetric property be wider than the read scope?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Never.** The write scope must be equal to or narrower than the read scope.

        **Why it matters:** the whole point is "read widely, write narrowly". A wider write
        scope would let outsiders mutate what they should only observe.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

## Inheritance rules

??? question "Which methods are exempt from signature compatibility checks?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`__construct()`** and **`private`** methods.

        **Why it matters:** a child constructor may take a completely different signature —
        which surprises people who expect variance rules to apply everywhere.

        **Official reference:** https://www.php.net/manual/en/language.oop5.basic.php

??? question "What does `#[\\Override]` actually check, and since when?"
    Think before revealing the answer.

    ??? success "Show answer"
        Since **PHP 8.3**, it asserts at compile time that the method really does override a
        parent method. If it does not, compilation fails.

        **Why it matters:** it catches a renamed or mistyped parent method — a silent bug where
        your "override" quietly becomes a brand-new method that nothing calls.

        **Official reference:** https://www.php.net/manual/en/language.oop5.basic.php

## Memory hooks

??? question "Mnemonic for `self::` versus `static::`"
    Think before revealing the answer.

    ??? success "Show answer"
        **"`self` is where it's written, `static` is who called it."** Compile-time text versus
        runtime caller.

        **Why it matters:** it resolves the factory question instantly: `new static()` when a
        subclass should get itself back.

        **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

??? question "Mnemonic for what magic methods respond to"
    Think before revealing the answer.

    ??? success "Show answer"
        **"Magic only fills gaps."** If the member is declared *and* reachable from the calling
        scope, no magic method fires.

        **Why it matters:** it converts every "will `__get()` run here?" question into one
        visibility check.

        **Official reference:** https://www.php.net/manual/en/language.oop5.overloading.php

---

<small>Back to the lesson: [Object-Oriented Programming](oop.md) · [Retake the topic exam](oop-exam.md) · Next topic: [Interfaces & Type Declarations](interfaces.md)</small>

# Flashcards — Interfaces & Type Declarations

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Interfaces & Type Declarations](interfaces.md)** ·
    Practice: **[Guided exercises](interfaces-exercises.md)** ·
    Test: **[Topic exam](interfaces-exam.md)**

## Definitions and roles

??? question "What is an interface, in one sentence?"
    Think before revealing the answer.

    ??? success "Show answer"
        A pure contract: method signatures, constants, and — since PHP 8.4 — property
        requirements, with **no implementation**.

        **Why it matters:** it is the distinction from an abstract class. The moment you need
        shared code or state, an interface is the wrong tool.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "How many interfaces may a class implement, and how many may an interface extend?"
    Think before revealing the answer.

    ??? success "Show answer"
        A class may implement **many** interfaces. An interface may `extends` **several**
        parent interfaces.

        **Why it matters:** this is PHP's multiple inheritance of *type* without multiple
        inheritance of *state* — a class still `extends` exactly one class.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

## Variance

??? question "Return types: covariant or contravariant — and in which direction?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Covariant.** A child may return a *more specific* (narrower) type, never a wider one.

        **Why it matters:** the caller was promised "at least a `T`". Narrowing over-delivers
        and is safe; widening breaks every caller.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "Parameter types: covariant or contravariant — and in which direction?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Contravariant.** An implementation may accept a *wider* (more general) type, never
        a narrower one.

        **Why it matters:** narrowing would refuse callers the contract explicitly allowed.
        Reversing this rule with the return rule is the single most common exam mistake.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "One phrase that encodes both variance rules"
    Think before revealing the answer.

    ??? success "Show answer"
        **"Give more, ask for less."** Give a more specific return; ask for a more general
        parameter.

        **Why it matters:** under time pressure the direction is what people lose, not the
        vocabulary. This phrase survives where "co-" and "contra-" blur together.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "Why are ordinary properties invariant?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because a property supports **both** operations: a read would require covariance, a
        write would require contravariance, and only invariance satisfies both at once.

        **Why it matters:** it explains the rule instead of memorising it — and sets up the
        8.4 exception, which applies exactly where one of the two operations is missing.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "When may a property be covariant or contravariant? (PHP 8.4)"
    Think before revealing the answer.

    ??? success "Show answer"
        An **abstract or virtual** property requiring only `get` may be **covariant**; one
        requiring only `set` may be **contravariant**. Once it has both, it is invariant again.

        **Why it matters:** it is new in 8.4 and follows directly from the read/write
        reasoning — no separate rule to memorise.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

## Version changes — prime distractor material

??? question "Since which PHP version may an implementing class override an interface constant?"
    Think before revealing the answer.

    ??? success "Show answer"
        **PHP 8.1.0.** Before that, overriding an interface constant was forbidden.

        **Why it matters:** "interface constants are always final" was true once, which makes
        it a convincing distractor. On the 8.4 baseline it is false.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "Since which PHP version may an interface declare properties?"
    Think before revealing the answer.

    ??? success "Show answer"
        **PHP 8.4.0.** The declaration must state the required operations: `{ get; }`,
        `{ set; }`, or `{ get; set; }`.

        **Why it matters:** "interfaces cannot have properties" is the newest false-but-familiar
        statement in this topic, and most cheat sheets still print it.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "Which PHP version introduced union, intersection, and DNF types?"
    Think before revealing the answer.

    ??? success "Show answer"
        Union **8.0**, intersection **8.1**, DNF **8.2**. `never` also arrived in **8.1**;
        standalone `false`/`null` in **8.2**.

        **Why it matters:** union and intersection are one version apart and are routinely
        swapped in answer options.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

## Type system

??? question "What may appear inside an intersection type `A&B`?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Only class and interface types.** A non-class type is an error, and `mixed` and
        `never` are rejected as members.

        **Why it matters:** `int&Countable` looks plausible and is a hard error — intersection
        means "satisfies all these contracts", which is meaningless for a scalar.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

??? question "`never` versus `void` — what is the difference?"
    Think before revealing the answer.

    ??? success "Show answer"
        `void` **returns**, just without a value. `never` **never returns at all** — it always
        throws or exits.

        **Why it matters:** `never` is the bottom type, so it legally overrides *any* return
        type. `void` does not: it is not a valid override of `: string`.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

??? question "Is `: never` a legal override of `: string`?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Yes.** `never` is the bottom type; a method that never returns produces no value
        that could violate the contract, so it satisfies every return type vacuously.

        **Why it matters:** it feels wrong until you see that it is the *narrowest* possible
        covariant override rather than an exception to variance.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

## Edge cases and traps

??? question "What does `instanceof` return when the left operand is not an object?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`false`** — it never throws.

        **Why it matters:** it makes `instanceof` safe as a guard on an unknown value, and
        "it raises a TypeError" is the standard distractor.

        **Official reference:** https://www.php.net/manual/en/language.operators.type.php

??? question "Which interfaces does `instanceof` match?"
    Think before revealing the answer.

    ??? success "Show answer"
        The class, **all** its parents, and **every** interface in the closure — including
        interfaces inherited through an interface's own `extends`.

        **Why it matters:** implementing one interface can make `instanceof` true for several
        you never named directly. `class_implements()` shows the real set.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "Can a `readonly` property satisfy an interface property requirement?"
    Think before revealing the answer.

    ??? success "Show answer"
        It satisfies `{ get; }` but **never** `{ set; }` — a settable interface property may
        not be satisfied by `readonly`.

        **Why it matters:** the asymmetry is the exam point. `readonly` permanently forbids
        the public write that `{ set; }` advertises to callers.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "When is a variance violation detected?"
    Think before revealing the answer.

    ??? success "Show answer"
        At **link time** — when the class is compiled or autoloaded. Not on instantiation, and
        not on the first call.

        **Why it matters:** it explains the blast radius. A bad signature kills the whole
        application at load rather than failing one endpoint, and it cannot be caught.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "With two interfaces declaring the same method with different types, how do you find the legal signature?"
    Think before revealing the answer.

    ??? success "Show answer"
        Take the **widest** parameter required by any contract and the **narrowest** return
        allowed by any contract. If those demands cross, no legal signature exists.

        **Why it matters:** it turns the hardest case in the topic into two independent
        one-line decisions instead of guesswork.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "Why does adding a method to a published interface break implementers?"
    Think before revealing the answer.

    ??? success "Show answer"
        An interface is all-or-nothing: every existing implementer is suddenly missing a
        required method and fails to **link** the moment its file is autoloaded.

        **Why it matters:** it is the concrete reason Symfony's BC promise freezes published
        interfaces and adds a *new* interface instead of extending an old one.

        **Official reference:** https://symfony.com/doc/8.0/contributing/code/bc.html

## Memory hooks

??? question "Mnemonic for which side of a variance error message is yours"
    Think before revealing the answer.

    ??? success "Show answer"
        **Left is yours, right is the contract.** Then ask which side is wider: a wider
        *return* breaks covariance, a narrower *parameter* breaks contravariance.

        **Why it matters:** it makes the fatal message mechanical to read under exam pressure,
        with no need to open the source file.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "Mnemonic for interface versus abstract class"
    Think before revealing the answer.

    ??? success "Show answer"
        **Interface = the socket, abstract class = a half-built appliance.** A socket only
        imposes a shape and you can fit many; a half-built appliance already contains parts,
        and you can only inherit one.

        **Why it matters:** it encodes both differences at once — no state versus state, and
        many versus one.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

---

<small>Back to the lesson: [Interfaces & Type Declarations](interfaces.md) · [Retake the topic exam](interfaces-exam.md) · Next topic: [Anonymous Functions & Closures](closures.md)</small>

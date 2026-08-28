# Flashcards — Abstract Classes

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Abstract Classes](abstract-classes.md)** ·
    Practice: **[Guided exercises](abstract-classes-exercises.md)** ·
    Test: **[Topic exam](abstract-classes-exam.md)**

## Definitions and roles

??? question "What is an abstract class, in one sentence?"
    Think before revealing the answer.

    ??? success "Show answer"
        A class that **cannot be instantiated**, which may mix finished members — state, a
        constructor, concrete methods — with members deliberately left undefined for subclasses
        to supply.

        **Why it matters:** it is the tool for *partial implementation plus shared state*.
        The moment you need neither, an interface is the right choice; the moment you need
        both, an interface cannot do the job.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "What does declaring a method `abstract` actually do?"
    Think before revealing the answer.

    ??? success "Show answer"
        It declares the **signature and visibility only, with no body**, and records a debt:
        every non-abstract descendant must supply a signature-compatible implementation.

        **Why it matters:** it converts a forgotten step from a silent runtime bug into a
        load-time error, which is the entire reason the keyword exists.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "What is the template method pattern, in terms of PHP keywords?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **`final` concrete method** in the parent that fixes the algorithm, calling one or
        more **`abstract` hooks** the subclass must fill in.

        **Why it matters:** `final` is not decoration — it is what stops a subclass replacing
        the algorithm instead of customising a step, which is the whole invariant the pattern
        protects.

        **Official reference:** https://www.php.net/manual/en/language.oop5.final.php

## The two failure stages

??? question "When is 'class contains 1 abstract method' detected, and can you catch it?"
    Think before revealing the answer.

    ??? success "Show answer"
        At **link time** — when the declaration is compiled or the autoloader loads the file.
        It is a fatal error with **no exception object**, so it cannot be caught.

        **Why it matters:** it explains the blast radius. In a Symfony app the whole
        application dies on autoload, not one endpoint, and no `try/catch` helps.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "When is 'Cannot instantiate abstract class' raised, and can you catch it?"
    Think before revealing the answer.

    ??? success "Show answer"
        At **runtime**, by the `new` opcode, as an ordinary `\Error` — so **yes, it is
        catchable**.

        **Why it matters:** merging these two failures into one is the single most common
        mistake in this topic. Different stage, different catchability, different blast radius.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Can an abstract class with zero abstract methods be instantiated?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** The `abstract` keyword on the class is sufficient on its own; `new` consults
        that flag and nothing else.

        **Why it matters:** `AbstractController` and `AbstractType` both declare zero abstract
        methods, so "an abstract class must have at least one abstract method" is a statement
        real framework code disproves.

        **Official reference:** https://www.php.net/manual/en/reflectionclass.isabstract.php

## Modifier conflicts

??? question "Why can a member never be both `abstract` and `final`?"
    Think before revealing the answer.

    ??? success "Show answer"
        They state opposite requirements: `abstract` means "a subclass **must** override this",
        `final` means "a subclass **may not**". PHP rejects it by name —
        *"Cannot use the final modifier on an abstract class / method"*.

        **Why it matters:** it is a one-line contradiction that reads plausibly in an answer
        option, especially next to the perfectly valid `final` template method inside an
        abstract class.

        **Official reference:** https://www.php.net/manual/en/language.oop5.final.php

??? question "Why can an abstract method not be `private`?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because a private member is invisible to the subclass that would have to implement it.
        An abstract method declares its signature *"and whether it is public or protected"* —
        `private` is excluded, with the message
        *"Abstract function A::f() cannot be declared private"*.

        **Why it matters:** the same reasoning excludes `private` abstract properties in 8.4,
        so one explanation covers both.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Is `abstract public function f(): void {}` valid — and what kind of error is it?"
    Think before revealing the answer.

    ??? success "Show answer"
        Invalid. Any body, even an empty one, gives
        *"Fatal error: Abstract function A::f() cannot contain body"* — a **compile-time fatal
        error**, not a parse error.

        **Why it matters:** the file parses cleanly, so "parse error" is a precise-sounding but
        wrong answer. If you want a default body, drop `abstract` and write a concrete method.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

## Implementing an abstract member

??? question "Which override rules apply when you implement an abstract method?"
    Think before revealing the answer.

    ??? success "Show answer"
        All of them: **return covariant** (may narrow), **parameters contravariant** (may
        widen), **visibility equal or wider**, and extra parameters allowed only if
        **optional**.

        **Why it matters:** the manual states implementations must *"follow the usual
        inheritance and signature compatibility rules"*. "Abstract methods are exempt from
        variance" is a distractor with no basis.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "May an implementation add a parameter the abstract method never declared?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Only if it is optional.** A child *"may define optional parameters which are not
        present in the parent's signature"*. A required one gives
        *"Declaration of … must be compatible with …"*.

        **Why it matters:** the rule follows from one question — would a call written against
        the parent's signature still work? Optional: yes. Required: no.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "May an implementation change the visibility of an abstract method?"
    Think before revealing the answer.

    ??? success "Show answer"
        It may **relax** it (`protected` → `public`) but never **restrict** it. Narrowing gives
        *"Access level to C::f() must be protected (as in class A) or weaker"*.

        **Why it matters:** the message names the required level and the word "weaker", so it
        tells you the fix. Recognising it distinguishes a visibility bug from a variance bug at
        a glance.

        **Official reference:** https://www.php.net/manual/en/language.oop5.inheritance.php

??? question "Is a concrete method allowed to call an abstract one?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Yes** — that is the template method pattern. It is safe because an abstract class is
        never instantiated, so `$this` is always a concrete subclass that supplied the body.

        **Why it matters:** "invalid because it calls an abstract method" is a standard
        distractor on template-method code-analysis questions.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

## PHP 8.4 additions

??? question "Since which PHP version may a class declare an abstract property?"
    Think before revealing the answer.

    ??? success "Show answer"
        **PHP 8.4**, and only as `public` or `protected`:
        `abstract public string $label { get; }`.

        **Why it matters:** "only methods can be abstract" was true through 8.3 and is the
        newest false-but-familiar statement in this topic.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "How may a subclass satisfy an abstract property requirement?"
    Think before revealing the answer.

    ??? success "Show answer"
        With a **plain property** or a **hooked property** providing the demanded operation.
        Visibility may be widened (a `protected` requirement accepts a `public` property) but
        never narrowed. Providing more than asked — a read-write property for a `{ get; }`
        requirement — is fine.

        **Why it matters:** it is the same "over-delivering is safe" principle as covariant
        returns, so there is no separate rule to memorise.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "How is an unimplemented abstract property reported?"
    Think before revealing the answer.

    ??? success "Show answer"
        As an abstract **method**: `Class C contains 1 abstract method … (A::$slug::get)`.

        **Why it matters:** the wording is not sloppiness — it reveals that property hooks are
        stored as get/set methods attached to a property name, which is why one completeness
        check covers both.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

??? question "When may an abstract property be covariant or contravariant?"
    Think before revealing the answer.

    ??? success "Show answer"
        An **abstract or virtual** property requiring only `get` may be **covariant**; one
        requiring only `set` may be **contravariant**. With both operations it is **invariant**
        again.

        **Why it matters:** ordinary properties are invariant because reads want covariance and
        writes want contravariance. 8.4 relaxes it exactly where one operation is absent — the
        rule follows from the reason.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

??? question "May an abstract property provide a hook implementation?"
    Think before revealing the answer.

    ??? success "Show answer"
        Yes — it may implement **one** hook while leaving `get` or `set` declared and
        undefined. It may not implement both, because then nothing would be abstract about it.

        **Why it matters:** it is the property equivalent of a template method: a default `set`
        supplied by the parent, the `get` left to the child.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

## Distinctions

??? question "Abstract class versus interface, on PHP 8.4 — what is the surviving difference?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Stored state and construction.** An abstract class has a constructor, real stored
        properties and private/protected members; an interface has none of those. Since 8.4
        *both* can demand a property, so "properties" is no longer the dividing line.

        **Why it matters:** cheat sheets still print "interfaces cannot have properties",
        which has been wrong since 8.4.0. Answering with *state* rather than *properties* keeps
        you correct on either version.

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "Abstract class versus trait — what is the one difference that decides it?"
    Think before revealing the answer.

    ??? success "Show answer"
        An abstract class is a **type**: you can type-hint it and use `instanceof`. A trait is
        horizontal copy-in reuse and is **not** a type at all.

        **Why it matters:** it also costs you the single `extends` slot, so use an abstract
        class when the relationship is genuinely "is-a" and a trait when it is only shared code.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

??? question "How many classes may a class extend, and how many interfaces may it implement?"
    Think before revealing the answer.

    ??? success "Show answer"
        Exactly **one** class — abstract or not — and **many** interfaces.

        **Why it matters:** the single `extends` slot is a scarce resource. Publishing the
        contract as an interface and the convenience as an abstract base leaves consumers free,
        which is why Symfony ships `AuthenticatorInterface` *and* `AbstractAuthenticator`.

        **Official reference:** https://www.php.net/manual/en/language.oop5.inheritance.php

## Edge cases and traps

??? question "What happens if an implementation calls `parent::f()` where `f()` is abstract?"
    Think before revealing the answer.

    ??? success "Show answer"
        A runtime `Error`: *"Cannot call abstract method A::f()"*. The class links fine — there
        is simply no body to run.

        **Why it matters:** it is a classic refactoring accident. Promoting a concrete parent
        method to `abstract` leaves behind subclasses that used to call `parent::` legitimately.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Which of these can be abstract: a trait method, an anonymous class, an enum?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **trait method** can be abstract (the requirement lands on the using class). An
        **anonymous class** cannot be abstract but may *extend* one. An **enum** cannot be
        abstract at all — `abstract enum` is a parse error.

        **Why it matters:** each is a plausible-looking option, and only the enum case is a
        hard "no" at the syntax level.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

??? question "Does an abstract class that partially implements an interface have to redeclare the missing methods as `abstract`?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** An unimplemented interface method is already an abstract requirement. The class
        must carry the `abstract` keyword, but the members need no keyword at all.

        **Why it matters:** it is exactly how `AbstractAuthenticator` (1 of 5 methods) and
        `DependencyInjection\Extension\Extension` (leaving `load()`) are written in Symfony 8.0.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authenticator/AbstractAuthenticator.php

??? question "Is the parent constructor called automatically when a subclass declares its own?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** If the child declares `__construct()`, the parent's runs only if the child
        calls `parent::__construct()` explicitly.

        **Why it matters:** an abstract base usually initialises shared state in its
        constructor, so forgetting the call leaves typed properties uninitialised and produces
        an `Error` far from the real cause.

        **Official reference:** https://www.php.net/manual/en/language.oop5.decon.php

??? question "What breaks when a library adds an abstract method to a published base class?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Every subclass fails to link** the moment its file is autoloaded — the same breakage
        profile as adding a method to a published interface.

        **Why it matters:** it makes an abstract base as frozen as an interface under a
        backward-compatibility promise, and explains why Symfony adds behaviour via a new
        interface or a concrete default rather than a new abstract method.

        **Official reference:** https://symfony.com/doc/8.0/contributing/code/bc.html

## Symfony practice

??? question "Which kind of abstract class is `AbstractController`?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **helper base with zero abstract methods**. It is abstract only to prevent
        instantiation, while providing `render()`, `json()`, `redirectToRoute()` and a
        protected `$container` property.

        **Why it matters:** it is the concrete proof that "abstract" and "has abstract methods"
        are independent, and it shows state is what an interface could not have provided.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/AbstractController.php

??? question "Why is `Command::execute()` concrete and throwing, rather than abstract?"
    Think before revealing the answer.

    ??? success "Show answer"
        So `Command` can also be used **directly** as a concrete class, with the logic supplied
        through `setCode()`. The price is explicit: a missing override becomes a runtime
        `LogicException` instead of a load-time guarantee.

        **Why it matters:** it is the topic's central design trade-off, documented in Symfony's
        own source — abstract buys detection at load time and costs direct usability.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Console/Command/Command.php

## Memory hooks

??? question "Mnemonic for the two abstract-class error stages"
    Think before revealing the answer.

    ??? success "Show answer"
        **"Blank field = compile. Blank form filed = runtime."** A missing implementation
        breaks the *declaration*; a `new` on the abstract class breaks at *execution* and is
        catchable.

        **Why it matters:** under time pressure the wording of the two errors blurs. This
        phrase keeps the stage and the catchability attached to each one.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Mnemonic for what `abstract` refuses to combine with"
    Think before revealing the answer.

    ??? success "Show answer"
        **"No `final`, no `private`, no body."** Must override, must be visible, must be
        empty of implementation.

        **Why it matters:** three separate compile-time messages collapse into one rule you can
        recall in a second, and each has a matching answer option in question banks.

        **Official reference:** https://www.php.net/manual/en/language.oop5.final.php

---

<small>Back to the lesson: [Abstract Classes](abstract-classes.md) · [Retake the topic exam](abstract-classes-exam.md) · Next topic: [Exception & Error Handling](exceptions.md)</small>
</content>

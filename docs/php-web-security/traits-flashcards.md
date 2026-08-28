# Flashcards — Traits

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Traits](traits.md)** ·
    Practice: **[Guided exercises](traits-exercises.md)** ·
    Test: **[Topic exam](traits-exam.md)**

## Definition and role

??? question "What is a trait, in one sentence?"
    Think before revealing the answer.

    ??? success "Show answer"
        A mechanism for **horizontal** code reuse: a bundle of methods, properties, static
        members and constants that is **copied into** each using class at compile time.

        **Why it matters:** every other rule on this page follows from the word *copied*. The
        trait leaves no runtime object, no type and no delegation — which is why it can neither
        be instantiated nor type-hinted.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

??? question "Can a trait be instantiated with new?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** "It is not possible to instantiate a Trait on its own." Only a class that
        `use`s it can be instantiated.

        **Why it matters:** it is the shortest true/false question the exam can ask about
        traits, and it is the same fact that rules out `instanceof` and type declarations.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

??? question "Is a trait a type? What does instanceof against a trait return?"
    Think before revealing the answer.

    ??? success "Show answer"
        A trait is **not a type**. `$obj instanceof SomeTrait` returns **`false`** — silently,
        without any error. A parameter typed against a trait *parses*, but no object can ever
        satisfy it, so the call raises a `TypeError` at runtime.

        **Why it matters:** the distractor is subtle. "It is a syntax error" is wrong; the
        failure is a runtime `TypeError`, and `instanceof` does not fail at all. When callers
        need a type, pair the trait with an **interface** the class implements.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

??? question "Same keyword, two meanings: what does use mean at the top of a file versus inside a class body?"
    Think before revealing the answer.

    ??? success "Show answer"
        At the **top of a file** (after `namespace`), `use App\Some\Thing;` is a **namespace
        import / alias**. Inside a **class body**, `use SomeTrait;` is **trait composition**.
        A third meaning exists on closures: `function () use ($x) {}` captures a variable.

        **Why it matters:** a favourite distractor is a snippet where the file-level `use`
        imports the trait's fully-qualified name and the class-body `use` composes it. Both
        lines are needed, and they do different things.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.multiple

??? question "Can traits carry state, or only methods?"
    Think before revealing the answer.

    ??? success "Show answer"
        They carry **state too**: instance properties, static properties, static methods, and —
        since **PHP 8.2** — constants.

        **Why it matters:** "traits are just method bags" is a common false belief, and it makes
        the static-property and property-compatibility questions unanswerable.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.properties

## Precedence

??? question "State the trait precedence order."
    Think before revealing the answer.

    ??? success "Show answer"
        **Class > trait > inherited parent.** Members from the current class override trait
        methods, which in turn override inherited methods.

        **Why it matters:** this single line answers more trait exam questions than any other
        fact, and its reversal ("the trait wins over the class") is the most common wrong answer.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.precedence

??? question "A class, its parent and a used trait all define run(). Which runs?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **class's own** `run()`. Not the trait's, not the parent's, and it is not an error.

        **Why it matters:** it is the precedence rule in its most examinable form. The trait
        would have beaten the parent — but only if the class had stayed silent.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.precedence

??? question "Can a trait method call parent::something()?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Yes.** The trait body is copied into the exhibiting class first, so `parent::`
        resolves against *that class's* parent. The manual's own precedence example does
        exactly this.

        **Why it matters:** it shows the trait is not an independent scope. `self::`,
        `static::` and `parent::` all resolve against the destination class, never the trait.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.precedence

??? question "Inside a trait method, what do self::class and static::class resolve to?"
    Think before revealing the answer.

    ??? success "Show answer"
        `self::class` → the class where the `use` statement appears. `static::class` → the
        **runtime** class (late static binding), which may be a subclass.

        **Why it matters:** a trait used by `Base` and called on `Child extends Base` gives
        `Base` for `self` and `Child` for `static`. Neither ever names the trait.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

## Conflict resolution

??? question "Two used traits define the same method and you add no resolution. What happens?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **fatal error** at class-declaration time:
        `Trait method B::m has not been applied as C::m, because of collision with A::m`.

        **Why it matters:** PHP never picks first-wins or last-wins for you. Explicit
        resolution is mandatory, and the failure is compile-time, so no object is ever created.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.conflict

??? question "What does insteadof do, and what goes on each side of it?"
    Think before revealing the answer.

    ??? success "Show answer"
        It **excludes** competing versions. The **surviving** method goes on the left, the
        excluded trait(s) on the right: `A::init insteadof B;` keeps A's `init()` and drops
        B's.

        **Why it matters:** the left/right order is routinely inverted in distractors, which
        silently keeps the wrong implementation instead of failing loudly.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.conflict

??? question "What are the two things the as operator can do?"
    Think before revealing the answer.

    ??? success "Show answer"
        1. **Create an alias** — an additional name for an imported method.
        2. **Change visibility** — `public` / `protected` / `private`.

        Both operands are optional and can be combined:
        `Trait::m as protected alias;`. Since **PHP 8.3** it can also apply `final`.

        **Why it matters:** `as` is additive. It never renames and never removes — the manual
        says it "does not rename the method and it does not affect any other method either."

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.visibility

??? question "What does sayHello as protected; (no new name) do?"
    Think before revealing the answer.

    ??? success "Show answer"
        Changes `sayHello()`'s visibility to `protected` **in place**, keeping its name. No
        extra method appears.

        **Why it matters:** this is the only form of `as` that actually removes a method from
        the public API — because it re-scopes rather than adds.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.visibility

??? question "After sayHello as private myPrivateHello; what is the visibility of sayHello itself?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Still public.** The clause adds a private `myPrivateHello`; the original is untouched.
        The manual annotates its example with exactly this: "sayHello visibility not changed".

        **Why it matters:** developers use this form expecting to hide the method and are
        surprised it is still callable. The exam asks it as "which methods exist, and with what
        visibility?"

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.visibility

??? question "Three traits A, B and D all define m(). What must the insteadof clause look like?"
    Think before revealing the answer.

    ??? success "Show answer"
        It must exclude **every** competitor: `A::m insteadof B, D;`. Naming only `B` still
        fatals, this time on the `D`/`A` collision.

        **Why it matters:** resolving one pair does not resolve the rest. The follow-up error
        message names a trait the developer thought was already handled.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.conflict

??? question "Two traits collide, there is no resolution block, but the class defines the method itself. Fatal or fine?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Fine.** Precedence is applied first: because the class supplies the method, neither
        trait version is inserted, so nothing collides.

        **Why it matters:** the practical hazard is the reverse direction — deleting the class's
        own method later turns a working class into a load-time fatal that points at traits
        nobody touched.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.precedence

??? question "What happens if you alias a trait method that does not exist?"
    Think before revealing the answer.

    ??? success "Show answer"
        A fatal error at compile time:
        `An alias was defined for T::nope but this method does not exist`.

        **Why it matters:** it makes `as` clauses safe to refactor — a renamed trait method
        breaks loudly at load time rather than silently producing a missing alias.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.conflict

??? question "What happens if insteadof names a trait the class did not put in its use statement?"
    Think before revealing the answer.

    ??? success "Show answer"
        Fatal error: `Required Trait B wasn't added to C`. The same applies when you qualify a
        method with a trait that was only reached **indirectly**, through a composed trait —
        qualify it with the trait the class actually listed, or drop the qualifier entirely.

        **Why it matters:** it is the error you hit when a helper trait bundles several others
        and you try to alias one of the inner ones from the class.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.conflict

## Abstract members

??? question "What does an abstract method inside a trait accomplish?"
    Think before revealing the answer.

    ??? success "Show answer"
        It **imposes a requirement on the exhibiting class**: the class must implement it or be
        declared `abstract` itself. Otherwise:
        `Class C contains 1 abstract method and must therefore be declared abstract or
        implement the remaining methods (C::w)`.

        **Why it matters:** it lets a trait depend on behaviour it does not provide — the
        cleanest way to make a trait reusable without hidden `$this->something()` assumptions.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.abstract

??? question "Which visibilities may an abstract trait method have, and since when?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Public, protected and private** — but private only **as of PHP 8.0.0**. Before 8.0
        only public and protected abstract trait methods were supported.

        **Why it matters:** it is a version-pinned detail, and version questions are free marks
        if you know them and unguessable if you do not.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.abstract

??? question "Must the implementing method match the abstract trait method's signature?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Yes, as of PHP 8.0.0** — the concrete method must follow the signature-compatibility
        rules. A mismatch gives
        `Declaration of C::w(): int must be compatible with T::w(): string`. Previously the
        signature could differ.

        **Why it matters:** older code that relied on loose matching breaks on 8.0+, and the
        exam likes contrasting the two eras.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.abstract

## Static members

??? question "Two unrelated classes use a trait with a static property. Do they share it?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** Each using class gets its own copy. Incrementing `X::$counter` leaves
        `Y::$counter` untouched.

        **Why it matters:** this is the headline exam fact. The trait is a compile-time
        template, not a runtime owner of state, so there is nothing for the classes to share.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.static

??? question "What changed in PHP 8.3 about a trait's static property inside an inheritance hierarchy?"
    Think before revealing the answer.

    ??? success "Show answer"
        Before 8.3, a trait's static property was **shared across all classes in the same
        inheritance hierarchy** that used it. As of **8.3.0**, a child class that repeats
        `use T;` gets a **distinct** static from its parent's.

        **Why it matters:** the subclass only gets its own copy if it **repeats the `use`**. A
        subclass that does not simply inherits the parent's static, in every version.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.static

??? question "What happens if you call a static trait method directly on the trait, as in T::m()?"
    Think before revealing the answer.

    ??? success "Show answer"
        It still works, but emits a **deprecation notice** as of **PHP 8.1.0**:
        `Calling static trait method T::m is deprecated, it should only be called on a class
        using the trait`. The same applies to `T::$prop`.

        **Why it matters:** "fatal error" is the tempting wrong answer. Deprecated is not
        removed — the call succeeds in 8.4.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.static

## Properties and constants

??? question "A trait and its using class both declare $x. When is that legal?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only when the definitions are **compatible on every axis**: same visibility, same type,
        same `readonly` modifier, and same **initial value**. Anything else is a fatal:
        `... define the same property ($x) ... the definition differs and is considered
        incompatible`.

        **Why it matters:** the **initial value** is the axis people forget. `public $f = false;`
        in the trait versus `public $f = true;` in the class is fatal even though the types
        match. The same rule governs two traits used by one class.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.properties

??? question "Since which PHP version can a trait declare constants?"
    Think before revealing the answer.

    ??? success "Show answer"
        **PHP 8.2.0.** They may also be `final`, as in
        `final public const FLAG_IMMUTABLE = 5;`.

        **Why it matters:** "traits cannot have constants" was true through 8.1 and is now a
        stale distractor. Do not confuse it with 8.3, which brought the static-property scoping
        change and `as final`.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.constants

??? question "When may a class redeclare a constant its trait already defines?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only when it is **compatible**: same visibility, same initial value, and same
        **finality**. Otherwise the composition fatals, exactly as it does for properties.

        **Why it matters:** the three axes for constants differ slightly from the four for
        properties (no type, plus finality). Keeping the two lists apart is the whole card.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.constants

??? question "What does as final do, since which version, and who is still allowed to override?"
    Think before revealing the answer.

    ??? success "Show answer"
        Since **PHP 8.3.0**, `use T { T::m as final; }` prevents **child classes** from
        overriding `m()`. The class that uses the trait **can** still override it.

        **Why it matters:** that carve-out is the examinable half. `as final` locks the method
        downwards in the hierarchy, not at the point of use — ordinary precedence still lets the
        exhibiting class win.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.final-methods

## Composition and identity

??? question "Can a trait use another trait?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Yes.** "Just as classes can make use of traits, so can other traits." Members flow
        transitively into the final class, and abstract requirements propagate all the way
        down.

        **Why it matters:** it is how a project builds one bundled `AuditKit` from small focused
        traits. The catch: the class can only qualify the trait it listed itself, not the inner
        ones.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.composition

??? question "Inside a trait method, what does __CLASS__ evaluate to?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **using class**. The manual states it directly: "When used inside a trait method,
        `__CLASS__` is the name of the class the trait is used in."

        **Why it matters:** it is the constant you want when building class-scoped identifiers
        from inside a shared trait — which is precisely what Symfony's helper-trait guidance
        relies on.

        **Official reference:** https://www.php.net/manual/en/language.constants.magic.php

??? question "Inside a trait method, what do __TRAIT__ and __METHOD__ evaluate to?"
    Think before revealing the answer.

    ??? success "Show answer"
        `__TRAIT__` → the **declaring trait's** name (not a re-exporting outer trait).
        `__METHOD__` → **`TraitName::methodName`** — it reports the declaring scope, so it names
        the trait, *not* the using class.

        **Why it matters:** sort the constants into two buckets. **Destination:** `__CLASS__`,
        `self`, `static`, `parent`. **Origin:** `__TRAIT__`, `__METHOD__`. Misfiling
        `__METHOD__` is the classic trait identity bug.

        **Official reference:** https://www.php.net/manual/en/language.constants.magic.php

## Tooling and introspection

??? question "What does class_uses() deliberately not include?"
    Think before revealing the answer.

    ??? success "Show answer"
        Traits used by a **parent class** — the manual says so explicitly. It also does not
        flatten traits used by the traits you list. It reports exactly the one hop that class
        wrote down. Recurse with `class_parents()` (and with `class_uses()` on each trait) for
        the full picture.

        **Why it matters:** an empty or short array from `class_uses()` is almost never a bug;
        it is the documented, non-recursive contract.

        **Official reference:** https://www.php.net/manual/en/function.class-uses.php

??? question "Name the introspection API for traits beyond class_uses()."
    Think before revealing the answer.

    ??? success "Show answer"
        `trait_exists()`, `get_declared_traits()`, and on Reflection:
        `ReflectionClass::getTraits()`, `getTraitNames()`, `getTraitAliases()` (returns
        `alias => Trait::method`) and `ReflectionClass::isTrait()`.

        **Why it matters:** `getTraitAliases()` is the only way to see, after the fact, which
        `as` clauses a class applied — the composition is otherwise invisible in the method
        table.

        **Official reference:** https://www.php.net/manual/en/reflectionclass.gettraitaliases.php

??? question "What does ReflectionMethod::getDeclaringClass() return for a method that came from a trait?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **using class**, not the trait. The method genuinely lives in the class after
        compile-time composition.

        **Why it matters:** it is the cleanest single proof that traits are copy-paste at
        compile time rather than runtime delegation — and it explains why no runtime dispatch
        cost exists.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

## Symfony and design

??? question "Name two traits Symfony 8.0 ships and what each is for."
    Think before revealing the answer.

    ??? success "Show answer"
        `MicroKernelTrait` — lets a `Kernel` configure bundles, routes and the container in one
        class. `ServiceMethodsSubscriberTrait` — implements `ServiceSubscriberInterface` by
        reading `#[SubscribedService]` attributes off the class's own methods.

        **Why it matters:** both illustrate the idiomatic pairing: the trait supplies the
        implementation, an **interface** supplies the type. `ServiceSubscriberInterface` is what
        the container matches on; the trait is only the body.

        **Official reference:** https://symfony.com/doc/8.0/configuration/micro_kernel_trait.html

??? question "Why do Symfony helper traits build a service id from __CLASS__ . :: . __FUNCTION__ instead of __METHOD__?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because inside a trait `__METHOD__` expands to `TraitName::methodName`, while the
        container registered the service as `ClassName::methodName`. Symfony's docs warn:
        "the service id cannot be `__METHOD__` as this will include the trait name, not the
        class name."

        **Why it matters:** it is the `__CLASS__`-versus-`__METHOD__` rule with a real
        consequence attached — a lookup that fails at runtime for a reason invisible in the
        trait's source.

        **Official reference:** https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html#service-subscribers-service-subscriber-trait

??? question "Trait, interface or abstract class: which do you reach for, and why?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Interface** when callers need a *type* or a contract. **Abstract class** when there is
        shared state plus a single natural hierarchy. **Trait** when unrelated classes need the
        same *implementation* and inheritance is already spent. Traits and interfaces pair
        naturally: the interface is the type, the trait is the body.

        **Why it matters:** a trait cannot be mocked, swapped or injected at runtime. When the
        behaviour has its own dependencies or lifecycle, composition through a collaborator
        object beats a trait every time.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

??? question "One memory hook for the whole chapter."
    Think before revealing the answer.

    ??? success "Show answer"
        **A trait is a rubber stamp, not a passport.** The ink is copied onto the page at
        compile time (so the class owns the code, `self` and `parent` point at the class, and
        statics are per class), but a stamp proves no identity — hence no type, no
        `instanceof`, no instantiation. And the page's own handwriting always wins over the
        stamp: **class > trait > parent**.

        **Why it matters:** almost every trait question is one of those two halves — *copied*
        or *not a type*. Sorting the question into the right half usually decides the answer
        before you read the options.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

---

## Where to go next

- Back to the lesson: **[Traits](traits.md)**
- Retake the topic exam: **[Topic exam](traits-exam.md)**
- Continue to the next topic: **[Enums](enums.md)**

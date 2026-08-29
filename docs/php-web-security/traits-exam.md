# Topic Exam — Traits

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because traits are examined
    almost entirely through near-misses: a precedence order reversed, an `as` that renames
    instead of re-scoping, a static that looks shared but is not.

    Theory: **[Traits](traits.md)** ·
    Practice: **[Guided exercises](traits-exercises.md)** ·
    Recall: **[Flashcards](traits-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4** (the minimum for Symfony 8).

## Precedence

??? question "Question 1"
    A class, its parent, and a `use`-d trait all define `run()`. Which implementation is
    actually invoked on an instance of the class?

    - A. The class's own `run()`
    - B. The trait's `run()`
    - C. The parent's `run()`
    - D. A fatal error — the situation is ambiguous

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual states the order explicitly: members from the current
        class override trait methods, which in turn override inherited methods. So the
        precedence is **class > trait > inherited parent**, and the class's own `run()` wins.

        **B** is the classic reversal. A trait method *does* beat the parent's, but never the
        using class's own definition — that is the whole point of the "Alternate Precedence
        Order" example in the manual. **C** is the lowest priority of the three: the trait
        already displaced it. **D** is wrong because nothing here is ambiguous; PHP only
        fatals when two *traits* supply the same name with no resolution, which is a
        different situation.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.precedence

??? question "Question 2"
    Two `use`-d traits both define `log()` and you add no resolution block. What happens?

    - A. A fatal error
    - B. The first trait listed wins
    - C. The last trait listed wins
    - D. Both bodies run, in listing order

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** "If two Traits insert a method with the same name, a fatal error is
        produced, if the conflict is not explicitly resolved." PHP 8.4 reports it as:

        ```
        Fatal error: Trait method B::log has not been applied as C::log,
        because of collision with A::log
        ```

        **B** and **C** both invent an implicit ordering rule. PHP deliberately refuses to
        pick for you — silently choosing by declaration order is exactly the mixin ambiguity
        traits were designed to avoid. **D** describes method chaining, which no PHP
        composition mechanism performs. The fix is `insteadof` to choose the survivor, plus
        optionally `as` to keep the loser under another name.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.conflict

??? question "Question 3"
    What does `SyslogLogger::log as protected logToSyslog;` do?

    - A. Aliases the method to `logToSyslog` with `protected` visibility
    - B. Deletes `log()` from the class
    - C. Makes `log()` abstract
    - D. Makes `log()` static

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `as` can rename and re-scope in one clause. Here it **adds** a
        `protected` method named `logToSyslog`. The manual is explicit that `as` "does not
        rename the method and it does not affect any other method either" — the original
        `log()` keeps its own name *and* its own visibility.

        **B** is what `insteadof` does (it excludes a trait's version), not `as`. **C** is
        impossible: `as` accepts a visibility modifier, an alias name, or `final` (8.3+) —
        never `abstract`. **D** likewise: `as` cannot change a method's staticness.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.visibility

??? question "Question 4"
    A `static` property declared in a trait, used by two **unrelated** classes `X` and `Y`, is…

    - A. Separate per using class — `X` and `Y` hold independent copies
    - B. Shared across `X` and `Y`
    - C. Illegal — traits may not declare static properties
    - D. Automatically read-only

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** trait members are *copied into* each using class at compile time, so
        a static property declared in a trait becomes a distinct static of `X` and a distinct
        static of `Y`. Incrementing `X::$counter` leaves `Y::$counter` untouched.

        **B** is the intuition that the trait itself "owns" the state at runtime; it does not
        — a trait is a compile-time template with no runtime container of its own. (There is
        one historical nuance: **before PHP 8.3.0**, a trait's static property *was* shared
        across classes in the same **inheritance hierarchy**. That never applied to unrelated
        classes, which is what this question asks about.) **C** is contradicted by the manual:
        "Traits can define static variables, static methods and static properties." **D**
        invents a modifier PHP never adds implicitly.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.static

## Conflict resolution

??? question "Question 5 · Code analysis"
    Traits `A` and `B` both define `init()`. You want **A's** version kept as `init()` and
    **B's** version reachable as `initLegacy()`. Which resolution block is correct?

    ```php
    // A
    use A, B { A::init insteadof B; B::init as initLegacy; }

    // B
    use A, B { B::init insteadof A; A::init as initLegacy; }

    // C
    use A, B { A::init as initLegacy insteadof B; }

    // D
    use A, B { init insteadof A, B; }
    ```

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `insteadof` names the **surviving** method (`A::init`) and lists the
        trait(s) it excludes (`B`). `as` then re-admits the excluded `B::init` under the new
        name `initLegacy`. Together they match the requirement exactly.

        **B** does the reverse: it keeps B's version as `init()` and aliases A's — the wrong
        version survives. **C** is a syntax error: `as` and `insteadof` are two separate
        clauses and cannot be merged into one statement. **D** omits the trait qualifiers
        `insteadof` requires, and its `insteadof A, B` would exclude *both* candidates,
        leaving nothing to keep.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.conflict

??? question "Question 6 · Trap"
    You write `function f(MyTrait $x) { }` where `MyTrait` is a trait, then call
    `f(new UsesMyTrait())`. What happens?

    - A. A parse error — a trait name is not valid syntax in a type declaration
    - B. It works: the object uses the trait, so it satisfies the type
    - C. The file parses, but the call throws a `TypeError` — a trait is not a type, so no
      object can ever satisfy the declaration
    - D. It works only if the trait declares at least one abstract method

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** this is subtler than the usual "you cannot type-hint a trait" slogan.
        The parser accepts any identifier as a class-type declaration, so the file compiles.
        At call time PHP checks the argument against the named type, finds that a trait is not
        a type at all, and raises:

        ```
        TypeError: f(): Argument #1 ($x) must be of type MyTrait, UsesMyTrait given
        ```

        **A** is wrong about *when* it breaks — a syntax error would have to happen at parse
        time, and it does not. **B** is the core misconception: `use` copies members, it does
        not add a type; correspondingly `$obj instanceof MyTrait` is `false` (silently — it
        does not throw). **D** invents an exception that does not exist; abstract members
        impose requirements on the using class and change nothing about typing. When callers
        need a type, pair the trait with an **interface** and implement it on the class.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

??? question "Question 7"
    What does declaring an `abstract` method inside a trait accomplish?

    - A. It forces the using class to provide an implementation
    - B. It makes the trait instantiable
    - C. Nothing — `abstract` is ignored inside a trait
    - D. It supplies a default empty body

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** "Traits support the use of abstract methods in order to impose
        requirements upon the exhibiting class." A class that uses such a trait without
        implementing the method fails to compile:

        ```
        Fatal error: Class C contains 1 abstract method and must therefore be declared
        abstract or implement the remaining methods (C::w)
        ```

        Public, protected **and private** abstract methods are supported; before PHP 8.0.0
        only public and protected were.

        **B** is impossible under any circumstances — no trait can be instantiated. **C** is
        the opposite of the documented behaviour. **D** confuses `abstract` with an empty
        body: an abstract method has *no* body, only a signature terminated by `;`.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.abstract

??? question "Question 8 · True or false"
    A trait can be instantiated directly with `new`.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — false

        **Explanation:** "It is not possible to instantiate a Trait on its own." A trait is a
        compile-time code-reuse template, not a class and not a type; only a class that
        `use`s it can be instantiated. This is the same fact that makes `instanceof` and type
        declarations useless against a trait.

        **A** is the "a trait is a lightweight class" misconception. A trait has no
        independent existence at runtime: `class_uses()` can tell you a class was *built*
        from one, but there is no trait object to hold.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

??? question "Question 9 · Configuration consequence"
    What does `FileLogger::log as protected;` — with **no** new name — do?

    - A. Changes the visibility of `log()` to `protected`, keeping its name
    - B. Creates an anonymous alias of `log()`
    - C. Removes `log()` from the class
    - D. Makes `log()` abstract

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the alias name in an `as` clause is optional. With the name omitted,
        `as` performs a pure visibility adjustment: the imported `log()` keeps its identifier
        and becomes `protected` in the exhibiting class. The manual's example is
        `use HelloWorld { sayHello as protected; }`.

        Contrast it with `sayHello as private myPrivateHello;`, which *adds* a private
        `myPrivateHello` and leaves the public `sayHello` untouched — visibility changes in
        place only when there is no new name.

        **B** is meaningless: there is no such thing as an anonymous method. **C** is
        `insteadof` territory. **D** is not something `as` can express.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.visibility

??? question "Question 10 · Debugging"
    A class defines `save()`, and a trait it uses also defines `save()`. The developer
    expected the trait's version to run but observes the class's. What is going on?

    - A. The class's own method takes precedence over any trait method — this is defined behaviour
    - B. Undefined behaviour that depends on opcode cache state
    - C. A PHP bug: the trait's version should have won
    - D. It should have been a fatal error; the engine failed to report it

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** precedence is class > trait > inherited parent, so the class's own
        `save()` always shadows the trait's. To reach the trait's implementation deliberately,
        alias it in the `use` block: `use Persistable { save as saveViaTrait; }` and call
        `saveViaTrait()`.

        **B** is wrong — precedence is resolved at compile time and is fully deterministic;
        OPcache never changes it. **C** inverts the documented rule. **D** confuses this with
        a *trait-versus-trait* collision, which is the only trait situation that fatals for
        an unresolved duplicate name.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.precedence

??? question "Question 11 · Multiple answer"
    Which statements about PHP traits are true? (Select all that apply.)

    - A. Method precedence is: the class's own method beats a trait method, which beats an inherited parent method
    - B. Two used traits defining the same method are a fatal error unless resolved with `insteadof`/`as`
    - C. A static property declared in a trait is a separate copy for each unrelated class that uses the trait
    - D. You can type-hint a parameter against a trait, just as against an interface
    - E. When a trait and the using class define the same method, the trait's version wins

    ??? success "Show answer"
        **Correct answer:** A, B and C

        **Explanation:** **A** is the documented precedence order. **B** is the documented
        conflict rule — PHP forces an explicit choice rather than guessing. **C** follows from
        traits being copied into each using class: unrelated classes never share the static.

        **D** is false: a trait is not a type. The declaration parses but nothing can satisfy
        it, so every call raises a `TypeError`; `instanceof` against a trait is likewise always
        `false`. **E** is the reversal of **A** — a trait method overrides an *inherited*
        method, never the exhibiting class's own.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.precedence

## Members: constants, properties, finality

??? question "Question 12 · Code analysis"
    Which PHP version first allowed this, and what does it print?

    ```php
    <?php
    trait ConstantsTrait {
        public const FLAG_MUTABLE = 1;
        final public const FLAG_IMMUTABLE = 5;
    }

    class ConstantsExample { use ConstantsTrait; }

    echo (new ConstantsExample)::FLAG_MUTABLE;
    ```

    - A. PHP 8.0, prints `1`
    - B. PHP 8.2, prints `1`
    - C. PHP 8.3, prints `5`
    - D. Traits may never declare constants; this is a fatal error in every version

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "Traits can, as of PHP 8.2.0, also define constants." The constant is
        copied into `ConstantsExample`, so `::FLAG_MUTABLE` resolves to `1`.

        **A** names the wrong version — 8.0 brought abstract *private* trait methods and
        signature-compatibility enforcement, not trait constants. **C** names the wrong
        version *and* the wrong constant: `FLAG_IMMUTABLE` is `5`, but the code echoes
        `FLAG_MUTABLE`. (PHP 8.3 is the release that changed static-property scoping and added
        `as final`.) **D** was true only up to PHP 8.1.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.constants

??? question "Question 13 · Code analysis"
    Which of the marked lines compile without error?

    ```php
    <?php
    trait PropertiesTrait {
        public $same = true;
        public $different1 = false;
        public bool $different2;
    }

    class PropertiesExample {
        use PropertiesTrait;
        public $same = true;        // line 1
        public $different1 = true;  // line 2
        public string $different2;  // line 3
    }
    ```

    - A. All three lines
    - B. Line 1 only
    - C. Lines 1 and 2
    - D. None of them — redeclaring any trait property is always fatal

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "If a trait defines a property then a class can not define a property
        with the same name unless it is compatible (same visibility and type, `readonly`
        modifier, and initial value), otherwise a fatal error is issued." Line 1 matches on
        every axis, so it is accepted. Line 2 differs in **initial value** (`false` vs `true`)
        and line 3 differs in **type** (`bool` vs `string`); each produces:

        ```
        Fatal error: PropertiesExample and PropertiesTrait define the same property
        ($different1) in the composition of PropertiesExample. However, the definition
        differs and is considered incompatible.
        ```

        **A** ignores the compatibility requirement entirely. **C** overlooks that the initial
        value is part of the comparison — this is the axis most people forget. **D**
        overshoots: an *identical* redeclaration is explicitly allowed. The same rule applies
        between two traits used by the same class, and an analogous rule governs constants
        (same visibility, initial value and finality).

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.properties

??? question "Question 14 · Edge case"
    Since PHP 8.3 you can write `use CommonTrait { CommonTrait::method as final; }`. What
    does the `final` modifier prevent?

    - A. The class that uses the trait from overriding `method()`
    - B. Child classes of the using class from overriding `method()`
    - C. Other traits from declaring a method of the same name
    - D. The method from being aliased a second time

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual is precise here: `as final` "can be used to prevent child
        classes from overriding the method. However, the class that uses the trait can still
        override the method." A subclass that redeclares it gets:

        ```
        Fatal error: Cannot override final method FinalExampleA::method()
        ```

        **A** states the exact case the manual carves out as still legal — the exhibiting
        class's own definition continues to win by ordinary precedence. **C** is unrelated:
        `final` has no bearing on collision detection, which is `insteadof`'s job. **D**
        invents a restriction; `final` constrains inheritance, not the `use` block's syntax.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.final-methods

??? question "Question 15 · Execution order"
    What does this print on PHP 8.4?

    ```php
    <?php
    trait T { public static $counter = 1; }

    class A {
        use T;
        public static function incrementCounter(): void { static::$counter++; }
    }

    class B extends A { use T; }

    A::incrementCounter();
    echo A::$counter, ' ', B::$counter;
    ```

    - A. `2 2`
    - B. `2 1`
    - C. `1 1`
    - D. Fatal error — `B` may not re-use a trait already used by its parent

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "Prior to PHP 8.3.0, static properties defined in a trait were shared
        across all classes in the same inheritance hierarchy which used that trait. As of PHP
        8.3.0, if a child class uses a trait with a static property, it will be considered
        distinct from the one defined in the parent class." Because `B` re-declares
        `use T;`, it gets its own `$counter`, still at its initial `1`, while `A::$counter`
        becomes `2`.

        **A** is the pre-8.3 answer, and remains the answer if `B` does **not** repeat
        `use T;` — in that case `B::$counter` is simply `A`'s inherited static. That
        one-line difference is the whole trap. **C** ignores the increment. **D** invents a
        prohibition: re-using a trait in a subclass is legal, and since 8.3 it is meaningful.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.static

## Identity, composition and tooling

??? question "Question 16 · Code analysis"
    Given `namespace App;` and a trait `Ident` used by class `Base`, what does a call to
    `who()` return for each magic constant?

    ```php
    trait Ident {
        public function who(): array {
            return [__CLASS__, __TRAIT__, __METHOD__];
        }
    }
    class Base { use Ident; }
    ```

    - A. `['App\Base', 'App\Ident', 'App\Base::who']`
    - B. `['App\Base', 'App\Ident', 'App\Ident::who']`
    - C. `['App\Ident', 'App\Ident', 'App\Ident::who']`
    - D. `['App\Base', 'App\Base', 'App\Base::who']`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual states that "when used inside a trait method, `__CLASS__`
        is the name of the class the trait is used in" — so `__CLASS__` is `App\Base`.
        `__TRAIT__` is naturally `App\Ident`. The trap is `__METHOD__`, which resolves to
        **`App\Ident::who`**: it reports the *declaring* scope, which for a copied trait
        method is the trait.

        **A** applies the `__CLASS__` rule to `__METHOD__` as well — the single most common
        mistake here, and it has real consequences (see the Symfony question below). **C**
        gets `__CLASS__` wrong by assuming the trait is the class. **D** gets `__TRAIT__`
        wrong; `__TRAIT__` always names the trait.

        **Official reference:** https://www.php.net/manual/en/language.constants.magic.php

??? question "Question 17 · Scenario"
    Symfony's docs show a `LoggerAware` helper trait for use with
    `ServiceMethodsSubscriberTrait`, and warn that the service id must be
    `__CLASS__.'::'.__FUNCTION__` rather than `__METHOD__`. Why?

    - A. `__METHOD__` is not defined inside a trait
    - B. `__METHOD__` would yield `TraitName::functionName`, but the container registers the
      service under `ClassName::methodName`
    - C. `__METHOD__` is resolved at runtime and is therefore too slow
    - D. `__METHOD__` includes the namespace, which the container strips

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `ServiceMethodsSubscriberTrait` documents that "service ids are
        available as `ClassName::methodName`". Inside a *helper trait*, `__METHOD__` expands to
        the **trait's** name, so the lookup key would not match what was registered. Composing
        `__CLASS__` (which the manual defines as the using class) with `__FUNCTION__` rebuilds
        the correct id. Symfony states it directly: "the service id cannot be `__METHOD__` as
        this will include the trait name, not the class name."

        **A** is false — all magic constants are available inside trait methods. **C** is
        false twice over: magic constants are resolved at *compile* time, and performance is
        not the concern. **D** is backwards; `__CLASS__` also carries the namespace, and the
        container does not strip it.

        **Official reference:** https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html#service-subscribers-service-subscriber-trait

??? question "Question 18 · Code analysis"
    A trait method returns `[self::class, static::class]`. It is used by `Base`, and `Child
    extends Base`. What does `(new Child())->who()` return?

    - A. `['Base', 'Base']`
    - B. `['Base', 'Child']`
    - C. `['Child', 'Child']`
    - D. `['Ident', 'Child']` — `self` resolves to the trait

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the trait's body is copied into `Base`, so `self` binds to the class
        where the `use` statement appears — `Base`. `static` is late static binding and
        resolves to the runtime class, `Child`. Traits change *where* the code lives, not how
        `self` and `static` behave once it lives there.

        **A** treats `static` as if it were `self`, losing late static binding. **C** treats
        `self` as if it were `static`. **D** is the tempting "the trait is the scope" answer,
        but a trait is never a runtime scope: `self` inside a copied method can only name the
        exhibiting class. Note the contrast with the previous question — `__METHOD__` *does*
        report the trait, while `self` does not.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

??? question "Question 19 · Debugging"
    `trait Auditable {}` is used by `Entity`, and `Invoice extends Entity`. A developer runs
    `class_uses('Invoice')` expecting `['Auditable' => 'Auditable']` and gets an empty array.
    Why?

    - A. `class_uses()` only works on objects, never on class-name strings
    - B. `class_uses()` does not include traits used by a parent class
    - C. An empty trait is optimised away by the compiler
    - D. `Invoice` must be instantiated before `class_uses()` can see its traits

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual says `class_uses()` "returns an array with the names of
        the traits that the given `object_or_class` uses. This does however not include any
        traits used by a parent class." To walk the whole hierarchy, combine it with
        `class_parents()` and merge the results.

        **A** is false: the parameter is typed `object|string` and accepts either. **C** is
        false — an empty trait is still a declared trait and is reported for the class that
        directly uses it. **D** is false: the composition is known at class-declaration time,
        and `class_uses()` will even autoload the class first (its second parameter defaults
        to `true`).

        **Official reference:** https://www.php.net/manual/en/function.class-uses.php

??? question "Question 20 · Edge case"
    Three traits `A`, `B` and `D` each define `m()`. The class writes
    `use A, B, D { A::m insteadof B; }`. What happens?

    - A. It compiles — naming one excluded trait is enough
    - B. Fatal error: `D::m` still collides with `A::m`
    - C. Fatal error: `insteadof` may name only one trait
    - D. It compiles, and `D::m` silently wins because it is listed last

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `insteadof` must exclude **every** competing trait. Excluding only
        `B` leaves `D` unresolved, so PHP reports:

        ```
        Fatal error: Trait method D::m has not been applied as C::m,
        because of collision with A::m
        ```

        The correct form lists them together: `A::m insteadof B, D;`.

        **A** is the assumption that resolving one conflict resolves all of them. **C** is
        the opposite error — a comma-separated list is exactly the supported syntax. **D**
        re-introduces the implicit ordering rule PHP refuses to have.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.conflict

??? question "Question 21 · Expert trap"
    Traits `A` and `B` both define `m()`, there is **no** resolution block, but the using
    class defines its own `m()`. What happens?

    ```php
    <?php
    trait A { public function m(): string { return 'A'; } }
    trait B { public function m(): string { return 'B'; } }

    class C {
        use A, B;
        public function m(): string { return 'C'; }
    }

    echo (new C())->m();
    ```

    - A. Fatal error — the `A`/`B` collision is unresolved
    - B. Prints `C`
    - C. Prints `A`
    - D. Prints `B`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** precedence is applied first: because the class declares its own
        `m()`, **neither** trait method is inserted, so there is no collision left to resolve
        and the class compiles cleanly. `C::m()` runs and prints `C`.

        **A** is the natural but wrong generalisation of "duplicate trait methods are fatal" —
        the fatal only fires when two trait methods actually compete for the same slot in the
        class. **C** and **D** would both require a trait method to beat the exhibiting
        class's own, which never happens. The practical consequence is worth remembering:
        removing your own `m()` later can turn a working class into a fatal error at load
        time, with the error pointing at traits you did not touch.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.precedence

??? question "Question 22 · Edge case"
    On PHP 8.4, `trait T { public static function m(): string { return 'x'; } }` is used by a
    class, but someone calls `T::m()` directly on the trait. What is the result?

    - A. Fatal error: a trait has no callable static scope
    - B. It returns `'x'` and emits a deprecation notice
    - C. It returns `'x'` silently — this is fully supported
    - D. `TypeError`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "As of PHP 8.1.0, calling a static method, or accessing a static
        property directly on a trait is deprecated. Static methods and properties should only
        be accessed on a class using the trait." The call still succeeds, with:

        ```
        Deprecated: Calling static trait method T::m is deprecated,
        it should only be called on a class using the trait
        ```

        The parallel message for `T::$p` reads "Accessing static trait property T::$p is
        deprecated".

        **A** overstates it — deprecated is not removed; the behaviour still works in 8.4.
        **C** ignores the 8.1 deprecation, which is exactly what the question tests. **D**
        describes an argument-type failure, which has nothing to do with the calling scope.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.static

??? question "Question 23 · Scenario"
    A trait `HelloWorld` is composed from traits `Hello` and `World`, and class `MyHelloWorld`
    uses only `HelloWorld`. Which two statements are true?

    - A. `$o->sayHello()` and `$o->sayWorld()` both work on `MyHelloWorld`
    - B. `class_uses('MyHelloWorld')` returns `Hello`, `World` and `HelloWorld`
    - C. `class_uses('MyHelloWorld')` returns only `HelloWorld`
    - D. Traits may not use other traits; only classes may

    ??? success "Show answer"
        **Correct answer:** A and C

        **Explanation:** "Just as classes can make use of traits, so can other traits." The
        members flow transitively, so both methods land in `MyHelloWorld` — that is **A**.
        But `class_uses()` reports only the traits named in the class's own `use` statement,
        so it returns `['HelloWorld' => 'HelloWorld']` — that is **C**.

        **B** assumes `class_uses()` flattens the composition; it does not, just as it does
        not climb to parent classes. To enumerate the full set you must recurse with
        `class_uses()` on each trait you find, or use
        `(new ReflectionClass($c))->getTraitNames()` in the same recursive way. **D** is
        contradicted by the manual's "Traits Composed from Traits" section.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.composition

---

## Where to go next

- Back to the lesson: **[Traits](traits.md)**
- Practise the mechanics: **[Guided exercises](traits-exercises.md)**
- Drill the facts: **[Flashcards](traits-flashcards.md)**

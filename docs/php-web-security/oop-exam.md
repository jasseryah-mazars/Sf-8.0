# Topic Exam — Object-Oriented Programming

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because the exam is built on
    near-misses rather than definitions.

    Theory: **[Object-Oriented Programming](oop.md)** ·
    Practice: **[Guided exercises](oop-exercises.md)** ·
    Recall: **[Flashcards](oop-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4**.

## Late static binding

??? question "Question 1"
    Inside a parent factory method, how do `new static()` and `new self()` differ?

    - A. They are identical
    - B. `static` respects the called subclass; `self` is fixed to the class the code is written in
    - C. `self` respects the subclass; `static` is fixed to the parent
    - D. Both are resolved at compile time

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** late static binding makes `static::` resolve to the class recorded at
        the moment of the call — the *called* class. `self::` is replaced with the defining
        class name while the file is compiled, so it can never know about a subclass.

        **A** is wrong precisely because the two answer different questions; they only
        coincide when the called class *is* the defining class. **C** reverses the roles,
        which is the single most common error on this topic. **D** is half right and therefore
        the most dangerous option: `self::` *is* compile-time, but `static::` explicitly is
        not — the manual calls it "late" binding for that reason.

        **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

??? question "Question 2 · Code analysis"
    What does this print?

    ```php
    class A { public static function f(): static { return new static(); } }
    class B extends A {}

    var_dump(B::f() instanceof B);
    ```

    - A. `bool(true)` — `new static()` resolves to the called class `B`
    - B. `bool(false)` — it returns an `A`
    - C. A fatal error, because `f()` is inherited rather than declared on `B`
    - D. `bool(false)` — static methods are not inherited

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `B::f()` records `B` as the called class. The body is found on `A`
        and executed, but `new static()` reads the recorded class and constructs a `B`.

        **B** describes what `new self()` would have done. **C** invents a restriction:
        inheriting a static method is ordinary behaviour and nothing about it is an error.
        **D** is simply false — static methods are inherited like any other public or
        protected member.

        **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

??? question "Question 3 · Execution order"
    Given the code below, what does `B::viaName()` return?

    ```php
    class A {
        public static function who(): string { return static::class; }
        public static function viaSelf(): string { return self::who(); }
        public static function viaName(): string { return A::who(); }
    }
    class B extends A {}
    ```

    - A. `B`, like `B::viaSelf()`
    - B. `A`, because naming a class explicitly is a non-forwarding call
    - C. `A`, because `who()` is declared on `A`
    - D. A fatal error — `A::who()` may not be called from inside `A`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual defines late static binding on *calls*: the engine stores
        the class named in the last **non-forwarding** call. `self::`, `parent::`, `static::`
        and `forward_static_call()` are forwarding — they pass the stored class through, which
        is why `B::viaSelf()` returns `B`. Writing `A::who()` names a class literally, which
        starts a fresh non-forwarding call and overwrites the stored class with `A`.

        **A** ignores the difference between the two call forms — the exact point of the
        question. **C** gives the right answer for the wrong reason: where a method is
        *declared* has no effect on `static::`, as `B::viaSelf()` proves. **D** invents an
        error; calling a class by name from inside itself is perfectly legal.

        **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

??? question "Question 4 · Debugging"
    A named constructor `Model::create()` uses `return new self();`. A subclass call
    `User::create()` returns a `Model`, not a `User`. What is the fix?

    - A. Declare `create()` as `final` so subclasses inherit it correctly
    - B. Add a `self` return type to the method
    - C. Replace `new self()` with `new static()`
    - D. Override `create()` in every subclass

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** `self` was bound at compile time to `Model`, so it always builds a
        `Model`. `new static()` reads the called class — `User` — and builds that instead.

        **A** changes nothing about instantiation: `final` only prevents overriding. **B**
        actively makes it worse by declaring the wrong type as correct; the useful move is
        `: static`, which turns the silent bug into a loud `TypeError`. **D** is boilerplate
        that late static binding exists to eliminate, and it breaks again the moment someone
        adds a subclass without remembering the rule.

        **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

??? question "Question 5 · Trap"
    Which of these forms **resets** the class that late static binding will report?

    - A. `self::method()`
    - B. `parent::method()`
    - C. `Concrete::method()`
    - D. `forward_static_call(['Concrete', 'method'])`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** naming a class explicitly is a **non-forwarding** call, and the
        engine stores that class as the new called class.

        **A**, **B** and **D** are the three keyword-based forwarding forms — together with
        `static::` they are the complete set the manual lists. Each hands the previously
        stored called class through untouched, which is why a chain of `self::` calls still
        reports the original subclass. **D** is the option people miss: the whole purpose of
        `forward_static_call()` is to make a call that behaves like `self::`/`static::` while
        letting you compute the target.

        **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

## Visibility and inheritance

??? question "Question 6 · True or false"
    A child class can directly access `private` members declared on its parent.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — false

        **Explanation:** `private` restricts access to the **declaring class only**. A subclass
        does not inherit the member in any usable sense, which is also why a child may
        redeclare a parent's private method with a completely different signature without
        triggering a compatibility error.

        **A** confuses `private` with `protected`. The precise wording is worth memorising
        from the manual: `protected` members are accessible "within the class itself and by
        inheriting **and parent** classes" — so `protected` reaches upward as well as
        downward, while `private` reaches nowhere but its own class.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "Question 7 · Code analysis"
    Does this class load and run?

    ```php
    final class Amount
    {
        public function __construct(private int $cents) {}

        public function isLargerThan(self $other): bool
        {
            return $this->cents > $other->cents;
        }
    }
    ```

    - A. No — `$other->cents` is private and belongs to a different instance
    - B. Yes — visibility is enforced per class, not per instance
    - C. Only if `$cents` is changed to `protected`
    - D. Only outside `declare(strict_types=1)`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual is explicit that objects of the same type have access to
        each other's private and protected members, "even though they are not the same
        instances", because the implementation details are already known inside that class.
        This is what makes comparison and equality methods on value objects possible without
        getters.

        **A** applies an instance-level intuition PHP does not have. **C** would work but is
        unnecessary, and would needlessly widen the member. **D** is unrelated —
        `strict_types` governs scalar coercion at call sites, not visibility.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "Question 8 · Expert trap"
    Which member is **exempt** from PHP's signature-compatibility rules when overridden?

    - A. Any `static` method
    - B. Any method declared `final` in the parent
    - C. `__construct()`, and `private` methods
    - D. Any method whose parameters are all optional

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** the manual states that the constructor and private methods are exempt
        from signature-compatibility checks and therefore do not emit a fatal error on a
        mismatch. Neither participates in substitutability: you never call a constructor
        polymorphically, and a private method was never visible to the child in the first
        place. A related exemption applies to visibility — every other member may only be
        *relaxed* when overridden, while a **constructor's** visibility may be restricted.

        **A** is false: static methods obey the same variance and compatibility rules as
        instance methods. **B** inverts `final`, which forbids overriding outright rather than
        relaxing the rules. **D** confuses one *permitted change* (a signature may make a
        mandatory parameter optional, or add new optional parameters) with a blanket
        exemption.

        **Official reference:** https://www.php.net/manual/en/language.oop5.basic.php

??? question "Question 9 · Configuration consequence"
    A class is declared `readonly class Money`. Which statement is true?

    - A. Only properties explicitly marked `readonly` become readonly
    - B. Every declared property becomes readonly, dynamic properties are forbidden, and only a `readonly` class may extend it
    - C. It may still declare static properties, since `readonly` applies to instance state only
    - D. Dynamic properties can be re-enabled with `#[\AllowDynamicProperties]`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** a `readonly` class (8.2+) adds the `readonly` modifier to every
        declared property and prevents dynamic property creation. It may be extended if, and
        only if, the child class is also declared `readonly`.

        **A** describes an opt-in the modifier does not have — the point of a readonly class is
        that it is exhaustive. **C** is false: neither untyped nor static properties can be
        `readonly`, so a readonly class cannot declare them at all. **D** is specifically
        forbidden — attempting to add `#[\AllowDynamicProperties]` to a readonly class is a
        **compile-time error**, not a silent no-op.

        **Official reference:** https://www.php.net/manual/en/language.oop5.basic.php

## Constructors, promotion and cloning

??? question "Question 10"
    Which cannot be used as a promoted constructor parameter?

    - A. `public readonly int $x`
    - B. `private ?string $s = null`
    - C. `private callable $fn`
    - D. `protected array $items = []`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** the manual states that object properties may not be typed `callable`
        because of engine ambiguity, and that promoted arguments therefore may not be typed
        `callable` either. Every other type declaration is permitted. Store a `\Closure`
        instead when you need a callable as state.

        **A**, **B** and **D** are all valid: `readonly` is a legal promotion modifier, a
        nullable type with a default is fine, and so is an array with a default.

        **Official reference:** https://www.php.net/manual/en/language.oop5.decon.php

??? question "Question 11 · Multiple choice"
    Select all statements about constructor property promotion that are true in PHP 8.4.

    - A. Any single modifier triggers promotion, not only a visibility keyword
    - B. Attributes on a promoted parameter are replicated to both the property and the parameter
    - C. A default value on a promoted parameter is replicated to both the parameter and the property
    - D. Promotion works in `__construct()` only

    ??? success "Show answer"
        **Correct answers:** A, B and D

        **Explanation:**
        **A** — the manual notes that a visibility modifier is the most likely trigger, but
        "any other single modifier (such as `readonly`) will have the same effect".
        **B** — attributes are duplicated onto both the generated property and the parameter,
        which is why Symfony can read `#[Autowire]` off a promoted constructor argument.
        **D** — promotion is a constructor-only feature; no other method supports it.

        **C** is the false one, and it is a genuinely fine distinction: a default value is
        replicated **only to the argument, not to the property**. The property is therefore
        typed-and-uninitialised until the constructor assigns it, which matters if you ever
        reach it through reflection before construction completes.

        **Official reference:** https://www.php.net/manual/en/language.oop5.decon.php

??? question "Question 12"
    After `$b = clone $a;` where `$a->lines` holds an object, what is `$b->lines`?

    - A. The same object as `$a->lines`, unless `__clone()` copies it
    - B. Always an independent deep copy
    - C. `null`
    - D. A fatal error — objects holding objects cannot be cloned

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `clone` performs a **shallow** copy of every property. Object-typed
        properties are handles, and the copy receives the same handle, so both objects point
        at one instance until `__clone()` explicitly duplicates it.

        **B** is the assumption that causes the bug — PHP has no automatic deep copy, and the
        manual's own example exists to demonstrate this. **C** invents a behaviour: properties
        are copied, never cleared. **D** is false; cloning never errors for this reason. In
        Symfony, `Request::__clone()` is the textbook fix: it clones all seven of its
        `ParameterBag`-family properties.

        **Official reference:** https://www.php.net/manual/en/language.oop5.cloning.php

??? question "Question 13 · Execution order"
    In what order do these happen when `clone $obj` is evaluated?

    - A. `__clone()` runs first, then the properties are copied
    - B. The properties are copied, then `__clone()` runs on the **new** object
    - C. The properties are copied, then `__clone()` runs on the **original** object
    - D. `__clone()` replaces the copy entirely and must return the new object

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the engine allocates a new object, performs the shallow copy of every
        property, and only then — "once the cloning is complete" — calls `__clone()` on the
        newly created object. That is why `$this` inside `__clone()` is the copy and why the
        copy already holds the original's references when the method starts.

        **A** would make `__clone()` useless, since there would be nothing to fix up yet.
        **C** is the dangerous misreading: if `__clone()` ran on the original, every deep-copy
        implementation in existence would corrupt the source object. **D** invents a return
        contract — `__clone()` is declared `void`.

        **Official reference:** https://www.php.net/manual/en/language.oop5.cloning.php

??? question "Question 14 · Edge case"
    A property is declared `public readonly string $id`. Where, if anywhere, may it legally be
    written a **second** time?

    - A. Nowhere — one write, ever
    - B. Inside `__clone()`, on the fresh copy, as of PHP 8.3
    - C. Anywhere inside the declaring class
    - D. Inside `__wakeup()` after unserialization

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** as of PHP 8.3.0 a readonly property may be **reinitialised when
        cloning an object, using the `__clone()` method**. It is the single documented
        exception to the one-write rule.

        **A** was correct for 8.1 and 8.2 and is the intended distractor — a question written
        against an older PHP is testing the version, not the concept. **C** confuses *scope*
        with *count*: the declaring scope controls **where** the one write may happen, not how
        many writes are allowed. **D** invents an exception; `__wakeup()` has no special
        readonly privileges.

        One 8.4 tightening completes the picture: taking a **reference** to a readonly property
        inside `__clone()` (`$ref = &$this->id`) is no longer allowed.

        **Official reference:** https://www.php.net/manual/en/language.oop5.properties.php

??? question "Question 15 · Trap"
    In PHP 8.4, what set-visibility does a `readonly` property have implicitly?

    - A. `private(set)` — only the declaring class may perform the write
    - B. `protected(set)` — child classes may perform the initialisation
    - C. `public(set)` — anyone may perform the single write
    - D. It has none; `readonly` and asymmetric visibility are unrelated

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual is explicit: "Prior to PHP 8.4.0 a readonly property is
        implicitly private-set... As of PHP 8.4.0, readonly properties are implicitly
        `protected(set)`, so may be set from child classes." That may be overridden explicitly
        if a stricter scope is wanted.

        **A** is exactly the pre-8.4 behaviour and is the reason this question exists — most
        material written before 2024 still says `private(set)`. **C** would defeat the purpose
        of `readonly` entirely. **D** is wrong: `readonly` is defined *in terms of* set
        visibility, which is also why `readonly` and property hooks are mutually exclusive
        while `private(set)` and hooks combine freely.

        **Official reference:** https://www.php.net/manual/en/language.oop5.properties.php

## Property hooks and asymmetric visibility (PHP 8.4)

??? question "Question 16 · Code analysis"
    What happens when this class is loaded?

    ```php
    class Report
    {
        public readonly string $slug {
            get => strtolower($this->title);
        }
        public string $title = 'Q1';
    }
    ```

    - A. It loads; the hook simply overrides the readonly read
    - B. Fatal error — hooked properties cannot be readonly
    - C. It loads, but `$slug` is silently treated as virtual and non-readonly
    - D. Fatal error — a `get` hook may not reference another property

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual states plainly that property hooks are **incompatible with
        `readonly`**, and the engine reports `Hooked properties cannot be readonly` while
        compiling the class. The documented alternative is asymmetric visibility: use
        `public private(set)` when you need to restrict a write *and* alter its behaviour.

        **A** and **C** both assume PHP resolves the conflict silently; it refuses instead,
        and it refuses at **link time**, so nothing in the file loads. **D** is false — a hook
        runs in the object's scope and may read any property, call private methods, and even
        trigger another property's hooks.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

??? question "Question 17 · Multiple choice"
    Select all statements that are true about property hooks in PHP 8.4.

    - A. A `set` hook's parameter type must be identical to or wider than the property type
    - B. A property is "virtual" when no hook references the property itself, and stores nothing
    - C. Hooks may be declared on static properties
    - D. Declaring both `get` and `&get` on the same property is a syntax error

    ??? success "Show answer"
        **Correct answers:** A, B and D

        **Explanation:**
        **A** — the `set` type must be the property's type or **contravariant (wider)**: a
        `string` property may accept `string|Stringable`, never only `array`.
        **B** — that is the exact definition of a virtual property; it takes up no memory in
        the object, and an operation whose hook is absent is an error rather than a default.
        **D** — `&get` makes the hook return by reference, and declaring both forms on one
        property is a syntax error. (`&get` combined with `set` is also rejected on a *backed*
        property, since writing through the reference would bypass the `set` hook.)

        **C** is the false one: the manual says there are two hooks available "on non-static
        properties". Hooks are an instance-property feature only.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

??? question "Question 18 · Code analysis"
    Which of these four declarations fails in PHP 8.4?

    ```php
    class A {
        public private(set) string $a = 'x';       // 1
        private(set) string $b = 'x';              // 2
        protected public(set) string $c = 'x';     // 3
        public private(set) static string $d = 'x';// 4
    }
    ```

    - A. Only 3
    - B. Only 4
    - C. 3 and 4
    - D. 2, 3 and 4

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** **3** is a syntax error because the `set` visibility must be the same
        as the read visibility or **more restrictive** — `protected public(set)` widens it.
        **4** fails with `Static property may not have asymmetric visibility`: in PHP 8.4 the
        feature applies to instance properties only. (PHP 8.5 lifts that restriction, but 8.5
        is outside this baseline.)

        **A** misses the static case, **B** misses the widening case. **D** wrongly includes
        **2**: when the read visibility is `public` it may be omitted, so `private(set)` and
        `public private(set)` mean exactly the same thing. Note also that **1** and **2** make
        the property implicitly `final`, and that both require a **typed** property.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

??? question "Question 19 · Debugging"
    A child class fails to load with `Cannot override final property Report::$title`, yet
    nobody wrote `final` anywhere. What is the most likely cause?

    - A. The parent class is declared `final`
    - B. `$title` is declared `private(set)`, which is implicitly final
    - C. The parent declares `$title` as `readonly`
    - D. The child changed the property's type

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual states that a property declared `private(set)` is
        **implicitly final** and may not be redeclared in a child class. That is a soundness
        requirement: a child able to redeclare it could widen the write scope the parent
        deliberately closed.

        **A** would produce a different error entirely — you cannot even extend a final class,
        so the message would name the class, not the property. **C** is wrong: `readonly` does
        not imply `final`, and since 8.4 it is implicitly `protected(set)` precisely so
        children can participate. **D** would produce a type-compatibility error naming the
        types, not a `final` error.

        **Official reference:** https://www.php.net/manual/en/language.oop5.final.php

??? question "Question 20 · Code analysis"
    With `public string $full { get => 'Ada Lovelace'; }` declared alongside a plain
    `public string $first = 'Ada';`, which inspection includes `full`?

    - A. `var_dump($obj)` and `(array) $obj`
    - B. `get_object_vars($obj)` and `json_encode($obj)`
    - C. All four
    - D. None — virtual properties are invisible to every inspection function

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual splits serialization behaviour deliberately. `var_dump`,
        `serialize`, `unserialize`, array casting and `get_mangled_object_vars()` use the
        **raw backing value**; `var_export`, `json_encode()`, `JsonSerializable` and
        `get_object_vars()` go **through the `get` hook**. A virtual property has no backing
        value, so it is absent from the first group and present in the second.

        **A** inverts the two lists. **C** ignores the split entirely. **D** overstates it —
        `json_encode()` on a virtual property is one of the most useful things hooks enable.
        The practical warning: `(array) $obj` and `get_object_vars($obj)`, which developers
        treat as interchangeable, land on **opposite sides** of this table.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

??? question "Question 21 · Edge case"
    An abstract class declares `abstract public string $identifier { get; }`. Is that valid in
    PHP 8.4, and what satisfies it?

    - A. Invalid — only interfaces may declare property requirements
    - B. Valid — a plain readable property or a property with a `get` hook satisfies it
    - C. Valid, but only a property with hooks may satisfy it
    - D. Valid, but abstract properties may only be `public`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** as of PHP 8.4 an abstract class may declare an abstract property, and
        the manual states it "may be satisfied either by a standard property or by a property
        with defined hooks, corresponding to the required operation".

        **A** is false — abstract properties are an abstract-class feature that arrived
        alongside the interface one. **C** adds a restriction that does not exist; a plain
        `public string $identifier = 'x';` satisfies a `{ get; }` requirement. **D** is
        half-true and therefore tempting: an abstract property may be `public` **or
        `protected`**, and a protected one may be satisfied by a property readable or writable
        from protected or public scope.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

## Magic methods and overloading

??? question "Question 22"
    When is the magic method `__get()` invoked?

    - A. On every property read
    - B. Only when reading an inaccessible or undeclared property
    - C. On property writes
    - D. On `isset()` calls

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** overloading is the **fallback** path. A property that exists and is
        visible in the current scope is read directly, and in PHP 8.4 a property with a `get`
        hook is served by the hook — neither ever reaches `__get()`.

        **A** is the misconception that makes people use `__get()` as a universal accessor;
        it never fires for a normal, visible public property. **C** is `__set()`. **D** is
        `__isset()`, which exists as a separate hook precisely so that an existence check does
        not have to materialise the value.

        **Official reference:** https://www.php.net/manual/en/language.oop5.overloading.php

??? question "Question 23"
    Which magic method handles `isset($obj->missing)` when `missing` is inaccessible?

    - A. `__isset()`
    - B. `__get()`
    - C. `__call()`
    - D. `__invoke()`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `isset()` and `empty()` on an inaccessible or non-existing property
        route through `__isset()`. `unset()` on the same property routes through `__unset()`.

        **B** would force the value to be produced just to answer an existence question, which
        is why PHP provides a dedicated hook instead. **C** handles inaccessible **method**
        calls in object context (`__callStatic()` in static context). **D** fires when the
        object itself is used as a function, `$obj(...)`.

        **Official reference:** https://www.php.net/manual/en/language.oop5.overloading.php

??? question "Question 24 · True or false"
    `__toString()` is invoked when you `var_dump()` an object.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — false

        **Explanation:** `var_dump()` consults `__debugInfo()` if it is defined, and otherwise
        shows all public, protected and private properties. `__toString()` fires only in a
        **string context** — `echo`, concatenation, a string cast, an interpolated string.

        **A** generalises "displaying an object" into "stringifying an object". Two related
        facts are worth carrying: any class defining `__toString()` implicitly implements
        `Stringable` since PHP 8.0, and under `declare(strict_types=1)` a `Stringable` object
        is **not** accepted by a `string` type declaration — you must accept
        `string|\Stringable` if you want both.

        **Official reference:** https://www.php.net/manual/en/language.oop5.magic.php

??? question "Question 25 · Expert trap"
    Which statement about magic-method declarations is correct?

    - A. All magic methods must be public, without exception
    - B. A non-public magic method is a fatal error; a mismatched type declaration is a warning
    - C. A non-public magic method emits `E_WARNING`; a type declaration that does not match the documented signature is a fatal error
    - D. Type declarations on magic methods are never checked

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** the manual separates the two severities. All magic methods must be
        `public` **except `__construct()`, `__destruct()` and `__clone()`**, and a violation
        emits an `E_WARNING`. Separately, if type declarations are used they must be
        *identical* to the documented signature, otherwise a **fatal error** is emitted (since
        PHP 8.0) — and `__construct()` / `__destruct()` must declare **no** return type at all.

        **A** forgets the three exceptions. **B** swaps the two severities, which is the whole
        trap: the quiet failure (a `protected __get()` that simply never fires) is the warning,
        and the loud one is the type mismatch. **D** describes pre-8.0 behaviour, when no
        diagnostic was emitted at all.

        **Official reference:** https://www.php.net/manual/en/language.oop5.magic.php

??? question "Question 26 · Code analysis"
    In a class defining `__get()` and `__set()`, what runs for `$a = $obj->b = 8;` when `b` is
    undeclared?

    - A. `__set()` then `__get()`, and `$a` receives whatever `__get()` returned
    - B. Only `__set()`, and `$a` receives `8`
    - C. Only `__get()`
    - D. Neither — chained assignment bypasses overloading entirely

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual notes that `__get()` is **never called when chaining
        assignments together like `$a = $obj->b = 8;`**. The assignment expression evaluates to
        the assigned value, so `$a` is `8` regardless of what `__get()` would have produced.
        The return value of `__set()` is ignored by design.

        **A** is the intuitive but wrong model, and it matters in practice: a `__set()` that
        transforms the value (trimming, casting) will store the transformed value while `$a`
        still holds the raw one. **C** has the direction backwards. **D** is false —
        `__set()` does fire.

        A neighbouring rule from the same page: PHP will not re-enter the **same** overload
        method, so `return $this->foo;` inside `__get()` yields `null` plus an `E_WARNING`
        rather than recursing.

        **Official reference:** https://www.php.net/manual/en/language.oop5.overloading.php

??? question "Question 27 · Multiple choice"
    Select all statements that are true about PHP's magic methods.

    - A. There are exactly 17 magic method names
    - B. If both `__serialize()` and `__sleep()` are defined, only `__serialize()` runs
    - C. Property-overloading methods may declare parameters by reference
    - D. Declaring `__get()` as `static` makes it fire for static property access

    ??? success "Show answer"
        **Correct answers:** A and B

        **Explanation:**
        **A** — the manual enumerates exactly seventeen: `__construct`, `__destruct`, `__call`,
        `__callStatic`, `__get`, `__set`, `__isset`, `__unset`, `__serialize`, `__unserialize`,
        `__sleep`, `__wakeup`, `__toString`, `__invoke`, `__set_state`, `__clone`,
        `__debugInfo`.
        **B** — `__serialize()` takes precedence and `__sleep()` is ignored; symmetrically
        `__unserialize()` wins over `__wakeup()`.

        **C** is false: none of the arguments of these magic methods may be passed by
        reference. **D** is false twice over — property overloading works in **object context
        only**, and declaring one of these methods `static` triggers a warning rather than
        enabling anything.

        **Official reference:** https://www.php.net/manual/en/language.oop5.magic.php

??? question "Question 28 · Configuration consequence"
    A base class defines `__construct(string $name)`. A child defines
    `__construct(string $name, int $age)` and never calls `parent::__construct()`. What
    happens?

    - A. Fatal error at load time — the child constructor is incompatible
    - B. The class loads, and the parent constructor simply never runs
    - C. The parent constructor runs first, then the child's
    - D. Deprecation notice, and the parent constructor runs

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** two independent rules combine here. First, `__construct()` is exempt
        from signature-compatibility checks, so the added parameter is not an error. Second,
        **parent constructors are not called implicitly** when the child defines one — you must
        write `parent::__construct(...)` yourself.

        **A** applies the normal override rules to the one method they do not govern. **C**
        describes the behaviour of some other languages, not PHP; PHP only inherits the
        parent's constructor when the child declares **none**. **D** invents a diagnostic —
        PHP says nothing at all, which is exactly why "parent state is uninitialised" is such a
        common and quiet bug. The same rule applies to `__destruct()`.

        **Official reference:** https://www.php.net/manual/en/language.oop5.decon.php

---

<small>Back to the lesson: [Object-Oriented Programming](oop.md) · [Guided exercises](oop-exercises.md) · [Review flashcards](oop-flashcards.md)</small>

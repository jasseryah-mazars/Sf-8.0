# Topic Exam — Anonymous Functions & Closures

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because the exam is built on
    near-misses rather than definitions.

    Theory: **[Anonymous Functions & Closures](closures.md)** ·
    Practice: **[Guided exercises](closures-exercises.md)** ·
    Recall: **[Flashcards](closures-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4**.

## Capture semantics

??? question "Question 1"
    When does `function () use ($x) {}` capture the value of `$x`?

    - A. At definition time, by value
    - B. At call time, by value
    - C. Always by reference
    - D. Never — it reads the live variable each time it runs

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the `use` list is evaluated while the `function` expression itself
        is being evaluated. The value is copied into the `Closure` object at that instant and
        never re-read. The manual's own example prints `hello` twice after the outer variable
        has been changed to `world`.

        **B** moves the read to call time, which is exactly the misconception the manual
        warns about ("the inherited variable's value is from when the function is defined,
        not when called"). **C** describes `use (&$x)`, the opt-in form — by reference is
        never the default. **D** would make the closure a live view of the outer scope, which
        only the `&` form provides.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

??? question "Question 2"
    Which statement about arrow functions (`fn`) is true?

    - A. They auto-capture the enclosing scope by value
    - B. They require an explicit `use` list
    - C. They can capture an outer variable by reference
    - D. Their body may contain several statements separated by semicolons

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** an arrow function implicitly captures, **by value**, every outer
        variable its expression mentions. The manual describes it as "roughly equivalent to
        performing a `use($x)` for every variable `$x` used inside the arrow function".

        **B** contradicts the whole point of the syntax: automatic capture means there is no
        `use` list to write, and writing one is a parse error. **C** is the single most
        common trap in this topic — a by-value binding "means that it is not possible to
        modify any values from the outer scope". **D** is wrong because the form is fixed at
        `fn (argument_list) => expr`: exactly one expression, whose value is returned.

        **Official reference:** https://www.php.net/manual/en/functions.arrow.php

??? question "Question 3 · True or false"
    An arrow function can capture an outer variable by reference.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — false

        **Explanation:** arrow functions use by-value variable binding, with no `use` list
        and no `&` capture form. `$x = 1; $fn = fn () => $x++; $fn();` leaves `$x` equal to
        `1`, because the increment applies to the captured copy.

        **A** is tempting because `fn (&$x) => $x` *is* valid syntax — but that `&` marks a
        by-reference **parameter**, not a capture. The two features are unrelated, and mixing
        them up is exactly what this question tests. When a callback must write back to the
        enclosing scope, a full closure with `use (&$x)` is the only option.

        **Official reference:** https://www.php.net/manual/en/functions.arrow.php

??? question "Question 4 · Code analysis"
    What do the two calls output?

    ```php
    $base = 10;
    $v = fn (int $n): int => $n + $base;
    $r = function (int $n) use (&$base): int { return $n + $base; };
    $base = 100;

    echo $v(1), ' ', $r(1);
    ```

    - A. `11 101`
    - B. `101 101`
    - C. `11 11`
    - D. `101 11`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the arrow function copied `$base` (`10`) when it was defined, so
        `$v(1)` is `11` no matter what happens to `$base` afterwards. The full closure
        captured a **reference**, so it reads the current `100` and returns `101`.

        **B** assumes the arrow function tracks later mutations — it cannot, by design.
        **C** ignores the `&` and treats both captures as snapshots. **D** swaps the two
        results, which is what happens if you remember that "one of them is live" but not
        which one. The rule to carry: `&` is the *only* thing that makes a capture live.

        **Official reference:** https://www.php.net/manual/en/functions.arrow.php

??? question "Question 5 · Scenario"
    A closure captures `use ($id)` while `$id` is `'A'`. Before the closure is invoked,
    `$id` is set to `'B'`. What does the closure see?

    - A. `'A'` — the value snapshotted at definition time
    - B. `'B'` — the current value at call time
    - C. `null` — captured variables are reset between calls
    - D. It throws, because a captured variable was modified

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `use ($id)` stores a copy inside the closure object at definition
        time. Reassigning the outer `$id` writes to a different storage slot, which the
        closure has no link to. Capturing `use (&$id)` instead would produce `'B'`.

        **B** is the call-time misconception again, restated as a scenario rather than a
        definition. **C** invents a lifecycle PHP does not have: captured values live as long
        as the closure object. **D** invents an error — reassigning an outer variable is an
        ordinary assignment and can never throw because a closure captured it earlier.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

??? question "Question 6 · Code analysis"
    What does this print?

    ```php
    $callbacks = [];

    foreach ([1, 2, 3] as $i) {
        $callbacks[] = function () use (&$i): int { return $i; };
    }

    foreach ($callbacks as $c) {
        echo $c();
    }
    ```

    - A. `123`
    - B. `333`
    - C. `111`
    - D. `000`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** all three closures captured a **reference** to the same `$i`
        variable, which the `foreach` reuses across iterations. After the loop, `$i` holds
        `3`, so every closure reads `3`.

        **A** is what you get by removing the `&`: each closure would then hold its own copy
        of the value at its own iteration. **C** would require the capture to freeze on the
        first iteration only, which matches no capture mode. **D** assumes uninitialised
        state, but `$i` is very much set.

        This is the canonical argument for capturing by value unless you have a specific
        reason: `&` inside a loop shares one variable across every closure you create.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

## Binding, scope and `$this`

??? question "Question 7"
    What does `Closure::bind($c, $obj, Foo::class)` return?

    - A. A new closure bound to `$obj` with `Foo`'s scope
    - B. `void` — it mutates `$c` in place
    - C. The result of invoking `$c`
    - D. A `callable` string

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `Closure::bind()` is the static form of `Closure::bindTo()`. It
        "duplicates a closure with a specific bound object and class scope" and returns the
        new `Closure` — or `null` on failure. The original `$c` is untouched.

        **B** is the most costly distractor in practice: writing `Closure::bind($c, $obj);`
        as a bare statement compiles, does nothing observable, and leaves `$c` unchanged.
        **C** confuses `bind()` with `call()`, which is the only one of the three APIs that
        invokes. **D** describes the legacy `'Class::method'` callable form, which `bind()`
        never produces.

        **Official reference:** https://www.php.net/manual/en/closure.bind.php

??? question "Question 8 · Trap"
    A closure defined inside class `A` reads `$this->value`, where `value` is `private`. You
    call `$c->bindTo(new B())` — `B` is unrelated to `A` and has its own `private $value` —
    and then invoke the result. What happens?

    - A. It reads `B::$value` successfully
    - B. `bindTo()` returns `null`, so the invocation fails immediately
    - C. `bindTo()` succeeds, and the **call** throws `Error: Cannot access private property B::$value`
    - D. `bindTo()` throws a `TypeError` because `B` does not extend `A`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** `bindTo()`'s second parameter, `newScope`, defaults to the string
        `"static"`, which means *keep the closure's current scope*. So `$this` becomes a `B`
        while the scope remains `A`. Binding therefore succeeds; the visibility failure only
        appears when the body actually touches the private member. Passing `B::class` as the
        scope — or using `$c->call(new B())`, which sets the scope from the object — fixes it.

        **A** assumes `$this` alone grants access; it never does. **B** is wrong about the
        timing: `bindTo()` returns a perfectly good closure here, which is precisely why the
        bug is hard to spot. **D** invents a type relationship requirement that does not
        exist — you may bind a closure to an object of any class.

        **Official reference:** https://www.php.net/manual/en/closure.bindto.php

??? question "Question 9"
    A closure reads `$this->secret`, a `private` property. What determines whether that
    access succeeds?

    - A. The closure's bound **scope**, set at creation or via `bindTo`/`bind`/`call`
    - B. The location from which the closure is invoked
    - C. Whether the property is declared `readonly`
    - D. The visibility of the function that calls the closure

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual defines the class scope as the class that "determines
        which private and protected members the anonymous function will be able to access" —
        the visible members are the same as if the closure were a method of that class.

        **B** is the central misconception: PHP resolves visibility from the closure's scope,
        not from the call site, which is why a closure created inside a class can be invoked
        from global code and still read privates. **C** confuses read and write: `readonly`
        restricts writing after initialisation and has nothing to do with read visibility.
        **D** would make visibility depend on the caller, which is not how PHP scopes work
        for methods either.

        **Official reference:** https://www.php.net/manual/en/closure.bindto.php

??? question "Question 10 · Execution order"
    How do `Closure::bind()`, `$c->bindTo()` and `$c->call()` differ?

    - A. `bind` (static) and `bindTo` (instance) return a new bound closure; `call` binds and invokes in one step
    - B. All three invoke the closure immediately
    - C. All three mutate the original closure in place
    - D. `call` returns a new closure without invoking it

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `bind` is the static form and `bindTo` the instance form of the same
        duplication operation; both return a new `Closure` (or `null`) and run nothing.
        `call()` "temporarily binds the closure to `newThis`, and calls it", returning the
        closure's return value.

        **B** is wrong for the first two: rebinding never runs the body. **C** contradicts the
        documented behaviour — the operation duplicates, so the original keeps its own bound
        object and scope. **D** inverts `call()` and `bindTo()`, and is the option chosen by
        anyone who remembers there is "one that is different" but not which way round.

        One extra difference worth carrying: `call()` also sets the **scope** from the class
        of the object it receives, whereas `bindTo($obj)` keeps the existing scope.

        **Official reference:** https://www.php.net/manual/en/closure.call.php

??? question "Question 11 · Code analysis"
    What does this print?

    ```php
    final class Box { private string $secret = 'hidden'; }

    $reader = function (): string { return $this->secret; };
    $bound = Closure::bind($reader, new Box(), Box::class);

    echo $bound();
    ```

    - A. `hidden`
    - B. `Error: Cannot access private property Box::$secret`
    - C. An empty string
    - D. `null`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** both slots are set explicitly: the second argument binds `$this` to
        a `Box` instance, and the third grants the closure `Box`'s scope, so `private` members
        are visible exactly as they would be to a real `Box` method.

        **B** is what you would get if the third argument were omitted — that is the whole
        point of the question. **C** and **D** assume PHP silently degrades on a visibility
        problem; it does not, it throws. Note also that the closure is a full `function`
        rather than an arrow function only for readability: `fn () => $this->secret` would
        behave identically here.

        **Official reference:** https://www.php.net/manual/en/closure.bind.php

??? question "Question 12 · Edge case"
    `$c = static function () { return 1; }; $c = $c->bindTo(new stdClass());` — what is `$c`
    afterwards?

    - A. The same static closure, unchanged
    - B. `null`, with a warning that an instance cannot be bound to a static closure
    - C. A new closure bound to the `stdClass` instance
    - D. A `TypeError` is thrown at the `bindTo()` call

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** declaring a closure `static` prevents automatic binding of the
        current class, and the manual states that "objects may also not be bound to them at
        runtime". `bindTo()` reports failure by returning `null` and emitting
        `Warning: Cannot bind an instance to a static closure`. The scope of a static closure
        *can* still be changed — only the object cannot.

        **A** would be harmless; the reality is worse, because the assignment overwrites your
        closure with `null` and the next invocation dies with
        `Error: Value of type null is not callable`. **C** ignores the restriction entirely.
        **D** is the wrong failure mode: this path warns and returns `null`, it does not
        throw.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php#functions.anonymous-functions.static

## First-class callables and types

??? question "Question 13"
    What does the expression `trim(...)` produce?

    - A. The string `'trim'`
    - B. A `Closure` wrapping `trim`
    - C. The trimmed value of an implicit argument
    - D. A parse error in PHP 8.4

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** first-class callable syntax, added in **PHP 8.1.0**, creates a
        `Closure` object from a callable, with the same semantics as
        `Closure::fromCallable()`. The manual notes explicitly that "the `...` is part of the
        syntax, and not an omission".

        **A** describes the legacy string callable, which `(...)` exists to replace with
        something statically analysable. **C** reads `(...)` as an immediate call, but no
        argument is supplied and nothing is invoked. **D** is wrong on the version: the syntax
        is valid from 8.1 onward, so it is valid in 8.4.

        **Official reference:** https://www.php.net/manual/en/functions.first_class_callable_syntax.php

??? question "Question 14 · Trap"
    Which of these first-class-callable expressions is rejected at **compile time**?

    - A. `$obj?->method(...)`
    - B. `[$obj, 'method'](...)`
    - C. `'strlen'(...)`
    - D. `$obj->$methodName(...)`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual states that the first-class callable syntax cannot be
        combined with the nullsafe operator; `$obj?->method(...)` produces the compile-time
        error `Cannot combine nullsafe operator with Closure creation`. The same is true of
        `new Foo(...)`, because object creation is not a call.

        **B**, **C** and **D** are all listed in the manual as valid forms — an array
        callable, a string callable, and a dynamic method name respectively. `(...)` accepts
        "any expression that can be directly called in the PHP grammar", which covers all
        three.

        **Official reference:** https://www.php.net/manual/en/functions.first_class_callable_syntax.php

??? question "Question 15 · Debugging"
    A service stores an injected factory and fails at runtime:

    ```
    Error: Call to undefined method App\Notifier::transportFactory()
    ```

    The class declares `private \Closure $transportFactory` and the method body reads
    `return $this->transportFactory();`. What is the fix?

    - A. Change the property type to `callable`
    - B. Invoke it as `($this->transportFactory)()`
    - C. Call `$this->transportFactory->__invoke()` — closures have no `__invoke`
    - D. Rebind the closure with `bindTo($this)` before calling it

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `$this->transportFactory()` is method-call syntax, so PHP searches
        the *method* table and finds nothing. Wrapping the property access in parentheses
        forces it to be evaluated first, yielding the closure, which is then invoked. Symfony's
        own service-closure documentation uses exactly this form: `($this->mailer)()`.

        **A** makes things worse: `callable` is not a legal property type, so the class would
        fail to load with `Property ...$transportFactory cannot have type callable`. **C** is
        based on a false premise — `Closure` does have an `__invoke` method, present "for
        consistency with other classes that implement calling magic", although the manual notes
        it is not what actually calls the function. **D** treats a syntax problem as a binding
        problem; the closure's binding is irrelevant to how you write the call.

        **Official reference:** https://symfony.com/doc/8.0/service_container/service_closures.html

??? question "Question 16 · Configuration consequence"
    A Symfony service is wired with `arguments: [!service_closure '@mailer']` and the
    constructor declares `private \Closure $mailer`. What is true?

    - A. The mailer is instantiated when the service is built, and the closure just returns it
    - B. The mailer is instantiated on the first call to the closure, and later calls return that same instance
    - C. A new mailer is instantiated on every call to the closure
    - D. The closure receives the mailer as its first argument on each call

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** service closures exist to defer construction. The documentation
        states that "the service is instantiated the first time the closure is called, while
        all subsequent calls return the same instance, unless the service is not shared", and
        the `ServiceClosureArgument` class describes itself as "a service wrapped in a
        memoizing closure".

        **A** removes the laziness that is the entire feature. **C** describes a *non-shared*
        service, which is the documented exception rather than the rule — the default services
        are shared. **D** inverts the direction: the closure takes no arguments and *returns*
        the service, which is why it is invoked as `($this->mailer)()`.

        The equivalent attribute form is `#[AutowireServiceClosure('mailer')]`, and `'@>mailer'`
        is the documented YAML shortcut for `!service_closure '@mailer'`.

        **Official reference:** https://symfony.com/doc/8.0/service_container/service_closures.html

??? question "Question 17 · Multiple choice"
    Select **all** statements that are true in PHP 8.4.

    - A. `function () use ($x) {}` captures by value at definition time, and `use (&$x)` captures by reference
    - B. Arrow functions auto-capture the enclosing scope by value and cannot capture by reference
    - C. `Closure::bind()` mutates the closure it receives and returns `void`
    - D. An arrow function body may contain several statements separated by semicolons
    - E. `callable` may be used as a class property type

    ??? success "Show answer"
        **Correct answers:** A and B

        **Explanation:**
        **A** — the `use` list is copied when the closure expression is evaluated; prefixing an
        entry with `&` shares a reference instead, in both directions.
        **B** — arrow functions use by-value binding for every outer variable their expression
        mentions, and offer no by-reference capture form at all.

        **C** is false twice over: `bind()` is static, returns a **new** `Closure` (or `null`),
        and never modifies its argument. **D** is false because the arrow function form is
        `fn (argument_list) => expr` — a single expression. **E** is false and is the newest
        distractor of the set: the manual states that "the `callable` type cannot be used as a
        type declaration for class properties. Instead, use a `Closure` type declaration",
        which is why Symfony writes `private \Closure $mailer`.

        **Official reference:** https://www.php.net/manual/en/language.types.callable.php

## Edge cases and internals

??? question "Question 18 · Edge case"
    Which of these is **valid** PHP 8.4?

    - A. `$c = new Closure();`
    - B. `$s = serialize(function () {});`
    - C. `$f = function () use ($this) {};` inside a method
    - D. `$f = function () use ($a, $b,) { return $a + $b; };`

    ??? success "Show answer"
        **Correct answer:** D

        **Explanation:** since **PHP 8.0.0** the list of scope-inherited variables may include
        a trailing comma, which is simply ignored.

        **A** fails: `Closure::__construct` is `private` and "exists only to disallow
        instantiation", so PHP raises `Error: Instantiation of class Closure is not allowed`.
        **B** fails at runtime: closures "cannot be serialized as closures may contain bound
        variables and a specific execution context", and the attempt throws an `Exception`.
        **C** is a compile-time error, `Cannot use $this as lexical variable` — since PHP 7.1
        the `use` list may not contain `$this`, superglobals, or a name already used as a
        parameter. `$this` is already available implicitly anyway.

        **Official reference:** https://www.php.net/manual/en/class.closure.php

??? question "Question 19 · Execution order"
    A file contains only these two lines, and `$undefined` is never assigned:

    ```php
    $f = function () use ($undefined) { return 1; };
    // the closure is never called
    ```

    What does PHP report?

    - A. Nothing — the closure was never invoked
    - B. `Warning: Undefined variable $undefined`, reported at the line where the closure is defined
    - C. `Warning: Undefined variable $undefined`, reported the first time `$f()` runs
    - D. A fatal error at compile time

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the `use` list is read eagerly, while the `function` expression is
        being evaluated. PHP therefore looks up `$undefined` on the definition line, finds
        nothing, warns there, and stores `null`. This is the cleanest available proof that
        capture is not deferred.

        **A** and **C** both assume lazy capture, which is the misconception the whole topic
        revolves around. **D** overstates the severity: an undefined variable is a `Warning`
        in PHP 8, not a fatal error, and nothing about the *syntax* is wrong.

        Contrast with a closure that uses `$undefined` in its **body** without capturing it:
        there the diagnostic appears at call time, because that is when the body runs.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

??? question "Question 20 · Expert trap"
    A closure is created inside a **static** method of class `Reporter` and returned. What
    does `ReflectionFunction` report for it?

    - A. Bound object `Reporter`, scope `Reporter`
    - B. Bound object `null`, scope `Reporter`
    - C. Bound object `null`, scope `null`
    - D. It is automatically marked `static`, so it has neither

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the two slots are filled from different sources. The bound object
        comes from the `$this` in effect when the expression is evaluated — a static method
        has none. The scope comes from the class the expression is *written in*, which is
        `Reporter` either way. The practical consequence: that closure can read `Reporter`'s
        private **static** members even though it has no `$this`.

        **A** invents a `$this` that never existed. **C** is the answer you get by assuming
        "no `$this` means no class context", conflating the two slots. **D** is wrong about
        the `static` flag: `isStatic()` reports whether the `static` **keyword** was written
        on the closure, not whether it happens to lack a bound object — a closure declared in
        a static method without that keyword reports `false`.

        **Official reference:** https://www.php.net/manual/en/closure.bindto.php

---

<small>Back to the lesson: [Anonymous Functions & Closures](closures.md) · [Guided exercises](closures-exercises.md) · [Review flashcards](closures-flashcards.md)</small>

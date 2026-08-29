# Flashcards — Anonymous Functions & Closures

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Anonymous Functions & Closures](closures.md)** ·
    Practice: **[Guided exercises](closures-exercises.md)** ·
    Test: **[Topic exam](closures-exam.md)**

## Definitions and roles

??? question "What runtime type is produced by `function () {}`, `fn () => …` and `strlen(...)`?"
    Think before revealing the answer.

    ??? success "Show answer"
        All three produce an instance of the **`Closure`** class. It is `final`, and its
        constructor is `private`.

        **Why it matters:** it explains why a callback can be stored in a `\Closure`-typed
        property, passed, returned and compared with `instanceof` — and why `new Closure()`
        raises `Error: Instantiation of class Closure is not allowed`.

        **Official reference:** https://www.php.net/manual/en/class.closure.php

??? question "What are the three things a closure carries besides its body?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Captured variables**, a **bound object** (`$this`), and a **class scope**. A fourth
        flag records whether it was declared `static`.

        **Why it matters:** every API in the topic touches exactly one of these. Captured
        variables are fixed forever; the bound object and the scope are what `bindTo`, `bind`
        and `call` change.

        **Official reference:** https://www.php.net/manual/en/closure.bindto.php

??? question "In one sentence: what makes an anonymous function a *closure*?"
    Think before revealing the answer.

    ??? success "Show answer"
        It carries variables inherited from the scope where it was written. The PHP manual
        treats the two terms as synonyms: "anonymous functions, also known as closures".

        **Why it matters:** on the exam, a question saying "closures and anonymous functions
        are different types" is false — there is one class and one mechanism.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

## Capture

??? question "When exactly does `use ($x)` read `$x`?"
    Think before revealing the answer.

    ??? success "Show answer"
        At **definition time** — while the `function` expression is being evaluated. The
        value is copied into the closure object and never re-read.

        **Why it matters:** this single sentence answers a third of the questions on this
        topic. "At call time" and "it reads the live variable" are both wrong.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

??? question "What does adding `&` to a `use` entry change?"
    Think before revealing the answer.

    ??? success "Show answer"
        The closure shares a **reference** with the outer variable instead of copying it, so
        later outer writes are visible inside **and** writes inside are visible outside.

        **Why it matters:** the second half is the one people forget. `&` is how a closure
        accumulates into an outer array or memoizes a result, not merely how it reads fresh
        values.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

??? question "How does an arrow function capture, and can that be changed?"
    Think before revealing the answer.

    ??? success "Show answer"
        Automatically and **by value only**, for every outer variable its expression
        mentions. There is no `use` list and no by-reference capture form.

        **Why it matters:** "arrow functions can capture by reference" is the most frequent
        false statement in this topic's answer options.

        **Official reference:** https://www.php.net/manual/en/functions.arrow.php

??? question "Is `fn (&$x) => $x` valid, and what does the `&` mean there?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Valid.** The `&` marks a by-reference **parameter**, not a capture. `fn &($x) => $x`
        is also valid and marks a by-reference **return**.

        **Why it matters:** it is the sharpest trap available — a legal `&` on an arrow
        function that has nothing to do with capture. Arrow functions support full signatures:
        types, defaults, variadics, by-reference params and returns.

        **Official reference:** https://www.php.net/manual/en/functions.arrow.php

??? question "You capture an object with `use ($obj)`, then mutate the object. Does the closure see the change?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Yes.** By-value capture copies the *handle*, not the object, so mutations are
        visible. Reassigning `$obj` to a **different** object afterwards is not visible.

        **Why it matters:** it draws the real line between "the value is frozen" and "the
        object is frozen". Only the variable's binding is frozen.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

??? question "Three things that may never appear in a `use` list"
    Think before revealing the answer.

    ??? success "Show answer"
        A **superglobal**, **`$this`**, and a name already used as a **parameter** — all
        compile-time errors since PHP 7.1.

        **Why it matters:** `use ($this)` is the plausible-looking one; it fails with
        `Cannot use $this as lexical variable`, because `$this` is already bound implicitly.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

??? question "Where does the return type go on a full closure with a `use` clause?"
    Think before revealing the answer.

    ??? success "Show answer"
        **After** the `use` clause: `function () use ($x): string { … }`.

        **Why it matters:** the manual calls this out explicitly, and writing the return type
        before `use` is a parse error — an easy thing to get wrong when reading code under
        time pressure.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

## Binding and scope

??? question "Bound object versus scope — which one grants access to `private` members?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **scope**. The bound object only decides what `$this` refers to; the scope
        decides which class's private and protected members are visible.

        **Why it matters:** it explains why `bindTo($obj)` alone often fails, and why a
        closure created inside a class can be invoked from global code and still read
        privates. Visibility never depends on the call site.

        **Official reference:** https://www.php.net/manual/en/closure.bindto.php

??? question "What is the default value of `bindTo()`'s `newScope` parameter?"
    Think before revealing the answer.

    ??? success "Show answer"
        The string **`"static"`**, meaning *keep the closure's current scope*.

        **Why it matters:** it is the reason `$c->bindTo(new B())` changes `$this` but not
        the access rights — the most common rebinding bug, and it fails at **call** time, not
        at bind time.

        **Official reference:** https://www.php.net/manual/en/closure.bindto.php

??? question "What do `bindTo()` and `Closure::bind()` return?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **new** `Closure`, or **`null`** on failure. The original closure is never mutated.

        **Why it matters:** both halves are examinable. Forgetting to assign the result is a
        silent no-op; forgetting that `null` is possible turns a failed bind into
        `Error: Value of type null is not callable` somewhere else entirely.

        **Official reference:** https://www.php.net/manual/en/closure.bind.php

??? question "How does `Closure::call()` differ from `bindTo()`, beyond invoking?"
    Think before revealing the answer.

    ??? success "Show answer"
        `call($obj, ...$args)` binds `$this` **and sets the scope from the object's class**,
        then invokes and returns the body's result. `bindTo($obj)` keeps the existing scope.

        **Why it matters:** it is why `$c->call(new Vault())` reads a private property that
        `$c->bindTo(new Vault())()` refuses. Same object, different scope.

        **Official reference:** https://www.php.net/manual/en/closure.call.php

??? question "What does `static function () {}` change, and what can you still do to it?"
    Think before revealing the answer.

    ??? success "Show answer"
        It prevents automatic binding of the current class, and **no object may be bound at
        runtime** — `bindTo($obj)` returns `null` with a warning. Its **scope** can still be
        changed.

        **Why it matters:** `Closure::bind($c, null, A::class)` on a static closure is the
        documented way to reach a class's private **static** members.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php#functions.anonymous-functions.static

??? question "A closure is created inside a static method. What are its bound object and scope?"
    Think before revealing the answer.

    ??? success "Show answer"
        Bound object **`null`** (there is no `$this`), scope **the class** it was written in.
        `isStatic()` is `false` unless the `static` keyword was actually written.

        **Why it matters:** it separates the two slots cleanly — "no `$this`" does not mean
        "no class context", and that closure can still read private statics.

        **Official reference:** https://www.php.net/manual/en/closure.bindto.php

## First-class callables and types

??? question "What does `f(...)` produce, and since which version?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **`Closure`** wrapping the callable, since **PHP 8.1.0**. The `...` is literal
        syntax, not an omission.

        **Why it matters:** `trim(...)` is not a call and not a string — reading `(...)` as an
        immediate invocation is the standard wrong answer.

        **Official reference:** https://www.php.net/manual/en/functions.first_class_callable_syntax.php

??? question "`Closure::fromCallable()` versus `f(...)` — same or different?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Same semantics** as of PHP 8.1.0, per the manual. Both use the scope at the point of
        creation. `fromCallable()` takes a runtime `callable` **value**; `(...)` takes a call
        **expression** and is visible to static analysis.

        **Why it matters:** it is why `$this->privateMethod(...)` works inside a class while
        `[$this, 'privateMethod']` called from outside fails — the scope is captured at
        creation, not at the call.

        **Official reference:** https://www.php.net/manual/en/closure.fromcallable.php

??? question "Two expressions that `(...)` cannot be applied to"
    Think before revealing the answer.

    ??? success "Show answer"
        **`new Foo(...)`** — object creation is not a call — and **`$obj?->method(...)`** —
        the nullsafe operator cannot be combined with closure creation. Both are compile-time
        errors.

        **Why it matters:** everything else is allowed, including `'strlen'(...)`,
        `[$obj, 'method'](...)`, `$obj(...)` and `$obj->$name(...)`, so these two are the only
        exclusions worth memorising.

        **Official reference:** https://www.php.net/manual/en/functions.first_class_callable_syntax.php

??? question "Can a class property be typed `callable`?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No** — `public callable $c;` is a fatal error. Use a **`Closure`** type declaration
        instead. `callable` remains valid on parameters and return types.

        **Why it matters:** it is the language reason Symfony's service closures are declared
        `private \Closure $mailer`, and the failure happens when the class **loads**, not when
        the callback runs.

        **Official reference:** https://www.php.net/manual/en/language.types.callable.php

??? question "How do you invoke a closure stored in a property?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`($this->prop)()`**. Writing `$this->prop()` looks up a **method** and fails with
        `Call to undefined method`.

        **Why it matters:** it is the single most common runtime error when working with
        injected callbacks, and it is exactly the form Symfony's documentation uses for
        service closures.

        **Official reference:** https://symfony.com/doc/8.0/service_container/service_closures.html

## Edge cases and version boundaries

??? question "What happens when you `serialize()` a closure?"
    Think before revealing the answer.

    ??? success "Show answer"
        It throws an **`Exception`**: closures "cannot be serialized as closures may contain
        bound variables and a specific execution context".

        **Why it matters:** it rules closures out of sessions, cache payloads and queued
        messages — and it is a security feature, not just a limitation.

        **Official reference:** https://www.php.net/manual/en/class.closure.php

??? question "How do you write a recursive closure on PHP 8.4?"
    Think before revealing the answer.

    ??? success "Show answer"
        Capture the variable holding it **by reference**:
        `$f = function (int $n) use (&$f): int { … $f($n - 1) … };`

        **Why it matters:** `use ($f)` captures the value at definition, when `$f` is still
        unassigned. `Closure::getCurrent()` removes the need for the reference — but it
        arrived in **PHP 8.5** and does not exist on the 8.4 baseline.

        **Official reference:** https://www.php.net/manual/en/closure.getcurrent.php

??? question "Which PHP versions introduced arrow functions and first-class callable syntax?"
    Think before revealing the answer.

    ??? success "Show answer"
        Arrow functions: **7.4**. First-class callable syntax: **8.1**. `Closure::fromCallable`:
        7.1. Trailing comma in a `use` list: **8.0**.

        **Why it matters:** version questions are cheap to write and cheap to lose. 7.4 and
        8.1 are two releases apart and are routinely swapped in answer options.

        **Official reference:** https://www.php.net/manual/en/functions.arrow.php

??? question "`create_function()` — is it still an option?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** Deprecated in PHP 7.2 and **removed in 8.0**. Anonymous functions replace it
        entirely.

        **Why it matters:** any answer option offering it as an alternative is describing
        PHP 7, and it built code from strings — the security reason it was killed.

        **Official reference:** https://www.php.net/manual/en/function.create-function.php

??? question "How do you inspect what a closure actually holds?"
    Think before revealing the answer.

    ??? success "Show answer"
        `ReflectionFunction`: `getClosureThis()`, `getClosureScopeClass()`, `isStatic()` and
        `getClosureUsedVariables()` (PHP 8.1+).

        **Why it matters:** it turns "why can't this closure see the private property" from
        guesswork into a two-line check of the bound object and the scope.

        **Official reference:** https://www.php.net/manual/en/class.closure.php

## Symfony usage

??? question "What does `!service_closure '@mailer'` inject, and when is the service built?"
    Think before revealing the answer.

    ??? success "Show answer"
        A `\Closure` that returns the service. The service is built on the **first** call, and
        every later call returns that same instance — unless the service is not shared.
        `'@>mailer'` is the documented shortcut, `#[AutowireServiceClosure]` the attribute form.

        **Why it matters:** it is the framework's canonical laziness pattern, and the reason
        the constructor takes `private \Closure $mailer` rather than `MailerInterface`.

        **Official reference:** https://symfony.com/doc/8.0/service_container/service_closures.html

??? question "Where does Symfony 8 use by-reference capture in its own source?"
    Think before revealing the answer.

    ??? success "Show answer"
        `EventDispatcher::optimizeListeners()` builds a `static` closure capturing both
        `&$listener` and `&$closure`, so the first invocation resolves the lazy listener and
        replaces the closure with the resolved callable.

        **Why it matters:** it proves `use (&$x)` is an engineering tool, not a code smell —
        it is how a callback remembers something learned during a call.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/EventDispatcher/EventDispatcher.php

??? question "How does the Twig bridge register a filter callback in Symfony 8?"
    Think before revealing the answer.

    ??? success "Show answer"
        With a first-class callable over its own method:
        `new TwigFilter('trans', $this->trans(...))`.

        **Why it matters:** `(...)` captures the extension class's scope, so even a non-public
        helper can be exposed — something a `'Class::method'` string could never do.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/TranslationExtension.php

## Memory hooks

??? question "One phrase that encodes the whole capture rule"
    Think before revealing the answer.

    ??? success "Show answer"
        **"Photocopy by default, original folder with `&`."** The photocopy is taken when the
        closure is *written*, never when it is *called*.

        **Why it matters:** under time pressure the direction is what people lose. This phrase
        also carries the timing, which is the half most answer options attack.

        **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

??? question "One phrase that encodes the binding rule"
    Think before revealing the answer.

    ??? success "Show answer"
        **"`$this` is the address, the scope is the badge."** The address says where you go;
        the badge says which locked cabinets open.

        **Why it matters:** it makes the `bindTo($obj)` failure obvious in advance — you
        changed the address and kept the old badge.

        **Official reference:** https://www.php.net/manual/en/closure.bindto.php

---

<small>Back to the lesson: [Anonymous Functions & Closures](closures.md) · [Retake the topic exam](closures-exam.md) · Next topic: [Abstract Classes](abstract-classes.md)</small>

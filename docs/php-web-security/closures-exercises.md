# Guided Exercises — Anonymous Functions & Closures

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    a prediction before revealing a hint, and to a full attempt before revealing the
    solution — a capture rule you predicted wrongly and then corrected sticks far better
    than one you read.

    Theory: **[Anonymous Functions & Closures](closures.md)** · Then:
    **[Topic exam](closures-exam.md)**

    All code targets **PHP 8.4**. Most of these run in one file: save the snippet and
    execute `php file.php`. Where an error is expected, that error **is** the observation.

## Exercise 1 · Discover when a closure actually reads the outside world

**Objective:** Establish, by experiment, that capture happens at definition time and not at
call time.

**Context:** A campaign discount rate that changes after the rule has been written.

**Starting point:**

```php
<?php
declare(strict_types=1);

$rate = 0.15;

$byValue = fn (int $cents): int => (int) round($cents * (1 - $rate));
$byRef   = function (int $cents) use (&$rate): int {
    return (int) round($cents * (1 - $rate));
};

$rate = 0.50;

echo $byValue(10000), "\n";
echo $byRef(10000), "\n";
```

**Task:** Write down both numbers **before** running the file. Then run it. Then explain
which line of the script decided each result.

**Expected observation:** `8500` then `5000`. The arrow function ignored the reassignment;
the by-reference closure followed it.

??? tip "Show a hint"
    Ask when PHP could possibly have read `$rate` for the arrow function. Is there any
    moment after line 6 where an arrow function goes back to look at the outer scope again?

??? success "Show the solution"
    ```
    8500
    5000
    ```

    `$byValue` was fixed on line 6: the value `0.15` was copied into the closure object
    right there. Line 11 assigns a new value to the *outer* variable, which the closure no
    longer has any connection to. `$byRef` shares a reference with that outer variable, so
    line 11 is visible to it.

    **Why it works:** an arrow function is documented as being *roughly equivalent to
    performing a `use($x)` for every variable `$x` used inside it*. Both are by-value, and
    by-value means a copy taken while the `function`/`fn` expression is being evaluated.

    **Certification takeaway:** the exam sentence is "captured **at definition time**, by
    value". Anything that says "at call time" or "reads the live variable" is wrong for both
    `use ($x)` and `fn`.

    **Official reference:** https://www.php.net/manual/en/functions.arrow.php

## Exercise 2 · Minimal implementation — one behaviour, three syntaxes

**Objective:** Produce the same result with a full closure, an arrow function and a
first-class callable, and confirm all three are the same type.

**Context:** Uppercasing a list of tags.

**Starting point:**

```php
<?php
declare(strict_types=1);

$tags = ['symfony', 'php', 'closures'];
```

**Task:** Map `$tags` three times — once with `function () {}`, once with `fn`, once with
`strtoupper(...)`. Then prove the three callbacks share a type.

**Expected observation:** Identical output three times, and `instanceof Closure` is `true`
for all three.

??? tip "Show a hint"
    `array_map()` takes a callable. What does the manual say every anonymous function is
    implemented with — and what does `(...)` produce from an existing function name?

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    $tags = ['symfony', 'php', 'closures'];

    $a = array_map(function (string $t): string { return strtoupper($t); }, $tags);
    $b = array_map(fn (string $t): string => strtoupper($t), $tags);
    $c = array_map(strtoupper(...), $tags);

    var_dump($a === $b, $b === $c);   // true, true

    $full  = function (string $t): string { return strtoupper($t); };
    $arrow = fn (string $t): string => strtoupper($t);
    $fcc   = strtoupper(...);

    var_dump(
        $full instanceof Closure,
        $arrow instanceof Closure,
        $fcc instanceof Closure,
    );   // true, true, true
    ```

    **Why it works:** the manual states that anonymous functions "are implemented using the
    `Closure` class", that arrow functions use the same class, and that `CallableExpr(...)`
    "is used to create a `Closure` object from callable". Three syntaxes, one runtime type.

    **Certification takeaway:** `fn`, `function` and `f(...)` are not three kinds of thing.
    They are three ways to obtain the same kind of object, which is why any of them can be
    passed wherever a `\Closure` is type-hinted.

    **Official reference:** https://www.php.net/manual/en/functions.first_class_callable_syntax.php

## Exercise 3 · Inspect what a closure really carries

**Objective:** Look inside the object instead of reasoning about it, and see the three slots
— captured variables, bound object, scope — separately.

**Context:** The same body defined in three places: file scope, an instance method, a static
method.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Reporter
{
    private string $label = 'internal';

    public function make(): Closure
    {
        return function (): string { return $this->label; };
    }

    public static function makeStatic(): Closure
    {
        return function (): string { return 'no $this here'; };
    }
}

$outer = function (): string { return 'file scope'; };
```

**Task:** For each of the three closures, print `getClosureThis()`, the name from
`getClosureScopeClass()`, and `isStatic()` using `ReflectionFunction`. Predict the nine
values first.

**Expected observation:** The instance-method closure has both a bound object and a scope.
The static-method closure has **no** `$this` but **still has the scope `Reporter`**. The
file-scope closure has neither.

??? tip "Show a hint"
    "Bound object" and "scope" are two different slots. A static *method* has no `$this` to
    bind — but it is still written inside a class body. Which slot does that fill?

??? success "Show the solution"
    ```php
    $describe = static function (Closure $c, string $name): void {
        $r = new ReflectionFunction($c);
        printf(
            "%-10s this=%s scope=%s static=%s\n",
            $name,
            $r->getClosureThis() === null ? 'null' : get_class($r->getClosureThis()),
            $r->getClosureScopeClass()?->getName() ?? 'null',
            var_export($r->isStatic(), true),
        );
    };

    $describe((new Reporter())->make(), 'instance');
    $describe(Reporter::makeStatic(), 'staticFn');
    $describe($outer, 'outer');
    ```

    ```
    instance   this=Reporter scope=Reporter static=false
    staticFn   this=null scope=Reporter static=false
    outer      this=null scope=null static=false
    ```

    Note `staticFn`: `isStatic()` is `false` because the closure was not declared with the
    `static` keyword — it simply had no `$this` available to capture. The scope is still
    `Reporter`, so that closure could read `Reporter`'s private **static** members.

    **Why it works:** the scope is set from the *class the expression is written in*; the
    bound object is set from the `$this` in effect at that moment. A static method supplies
    the first and not the second.

    **Certification takeaway:** "no `$this`" and "no scope" are different states, and only
    the scope decides private access. `ReflectionFunction::getClosureUsedVariables()`
    (PHP 8.1+) shows the captured values in the same way.

    **Official reference:** https://www.php.net/manual/en/class.closure.php

## Exercise 4 · Change one variable — drop the `&` from an accumulator

**Objective:** See what by-reference capture is actually for: writing *out* of a closure.

**Context:** An audit trail collected while applying a discount to several orders.

**Starting point:**

```php
<?php
declare(strict_types=1);

$audit = [];

$apply = function (int $cents) use (&$audit): int {
    $out = (int) round($cents * 0.85);
    $audit[] = "$cents -> $out";
    return $out;
};

$apply(10000);
$apply(20000);

var_dump(count($audit));
```

**Task:** Run it, note the count. Then change `use (&$audit)` to `use ($audit)` — one
character removed — and run again. Explain the second result precisely: is the array empty,
or is it a different array?

**Expected observation:** `2` with `&`, `0` without. No error either way.

??? tip "Show a hint"
    Without `&`, the closure received a copy of the array. Copies can be appended to
    perfectly well. The question is *which* array `count()` is looking at afterwards.

??? success "Show the solution"
    With `&`, the closure and the outer scope share one variable, so both appends land in
    the array `count()` inspects: `int(2)`.

    Without `&`, PHP copied the empty array into the closure at definition time. Each call
    appends to the closure's own copy — and PHP arrays are value types, so that copy is
    genuinely a separate array. The outer `$audit` is untouched: `int(0)`. Nothing failed;
    the writes simply went somewhere else.

    **Why it works:** by-value capture stores a value in the closure object. For an array
    that means a real copy. For an **object** it would mean a copy of the *handle*, so
    mutating the object would be visible outside — the difference that makes "objects are
    passed by reference" a dangerous half-truth.

    **Certification takeaway:** `&` is not only about reading fresh values in; it is the
    only way for a closure to write back to the enclosing scope. A silently empty
    accumulator is the signature failure of a missing `&`.

    **Official reference:** https://www.php.net/manual/en/functions.anonymous.php

## Exercise 5 · Diagnose a failure — the closure that "is not a method"

**Objective:** Read two real fatal errors that every developer meets once, and fix both.

**Context:** A service that receives a factory closure, exactly as Symfony's service
closures are injected.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Notifier
{
    public function __construct(private \Closure $transportFactory) {}

    public function send(): string
    {
        return $this->transportFactory();
    }
}

echo (new Notifier(fn (): string => 'sent'))->send();
```

**Task:** Predict the error before running. Then run it and fix it with the smallest
possible edit. Second half: change the constructor property to `private callable
$transportFactory` and predict what happens *and when*.

**Expected observation:** `Error: Call to undefined method Notifier::transportFactory()` for
the first; a fatal error at class-declaration time for the second.

??? tip "Show a hint"
    In `$this->transportFactory()`, what is PHP looking up — a property or a method? And for
    the second half: which type declarations are allowed on properties?

??? success "Show the solution"
    **First failure.** `$this->transportFactory()` is method-call syntax. PHP resolves the
    *method* table, finds nothing, and raises:

    ```
    Error: Call to undefined method Notifier::transportFactory()
    ```

    The minimal fix is a pair of parentheses that force the property to be evaluated first:

    ```php
    public function send(): string
    {
        return ($this->transportFactory)();
    }
    ```

    This is exactly why Symfony's service-closure documentation writes
    `($this->mailer)()` rather than `$this->mailer()`.

    **Second failure.** `private callable $transportFactory` never even reaches a call:

    ```
    Fatal error: Property Notifier::$transportFactory cannot have type callable
    ```

    The manual is explicit: "The `callable` type cannot be used as a type declaration for
    class properties. Instead, use a `Closure` type declaration." `callable` remains valid
    on parameters and return types.

    **Certification takeaway:** two independent rules with one shared symptom — a callback
    stored on an object. Property type must be `\Closure`; invocation must be
    `($this->prop)()`.

    **Official reference:** https://www.php.net/manual/en/language.types.callable.php

## Exercise 6 · Handle the edge cases of rebinding

**Objective:** Explore the three ways `bindTo()` disappoints you, and the one call that does
what people expect `bindTo()` to do.

**Context:** Reading a private property from outside its class.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Vault
{
    private string $secret = 'hidden';
}

$peek = function (): string { return $this->secret; };
```

**Task:** Answer four questions, then verify each. **(a)** What does `$peek->bindTo(new
Vault())` return, and what happens when you call it? **(b)** What does
`Closure::bind($peek, new Vault(), Vault::class)` return? **(c)** What does
`$peek->call(new Vault())` return? **(d)** What does `(static fn () => 1)->bindTo(new
Vault())` return?

**Expected observation:** (a) a closure that throws on call; (b) a working closure; (c) the
string directly; (d) `null`, with a warning.

??? tip "Show a hint"
    Look up the default value of `bindTo()`'s second parameter. It is not "the class of the
    object you just passed".

??? success "Show the solution"
    **(a)** `bindTo()` returns a new `Closure`, but `newScope` defaults to the string
    `"static"`, which means *keep the current scope*. `$peek` was defined at file scope, so
    it has none. `$this` is now a `Vault`, but the closure is not a member of anything:

    ```
    Error: Cannot access private property Vault::$secret
    ```

    Note **when**: at call time, not at bind time. Binding itself succeeded.

    **(b)** Passing the scope explicitly is what unlocks the private member:

    ```php
    $bound = Closure::bind($peek, new Vault(), Vault::class);
    echo $bound();   // hidden
    ```

    `Closure::bind()` is simply the static form of `bindTo()`; it returns a **new** closure
    and leaves `$peek` untouched.

    **(c)** `call()` binds `$this` **and** sets the scope from the object's class, then
    invokes immediately and returns the body's return value:

    ```php
    echo $peek->call(new Vault());   // hidden
    ```

    **(d)** A `static` closure can never carry a bound object. On PHP 8.4 `bindTo()` returns
    `null` and PHP emits `Warning: Cannot bind an instance to a static closure`. Because the
    result is `null` rather than an exception, an unchecked `$c = $c->bindTo($o);` turns your
    closure into `null` and the failure surfaces later as
    `Error: Value of type null is not callable`.

    **Certification takeaway:** three separate facts. `bindTo` keeps the scope by default;
    `call` sets it from the object; a static closure refuses binding and reports it with
    `null`.

    **Official reference:** https://www.php.net/manual/en/closure.bindto.php

## Exercise 7 · Expert challenge — build Symfony's memoizing service closure

**Objective:** Reproduce, from first principles, the lazy-and-once behaviour that
`!service_closure` gives you, using only capture rules.

**Context:** Symfony documents a service closure as: the service "is instantiated the first
time the closure is called, while all subsequent calls return the same instance". The
`ServiceClosureArgument` docblock calls it "a service wrapped in a memoizing closure".
`EventDispatcher` uses the same trick — a `static` closure capturing its own variable by
reference — to resolve listeners lazily.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class HeavyMailer
{
    public function __construct()
    {
        echo "built\n";
    }
}
```

**Task:** Write `lazy(callable $factory): Closure` returning a closure that (1) builds
nothing until first called, (2) prints `built` exactly once across many calls, and (3)
returns the same instance every time. Do it without a class, without `static` local
variables, and without globals — capture rules only. Then explain why `use ($instance)`
cannot work.

**Expected observation:** `built` printed once; `$a === $b === $c` is `true`.

??? tip "Show a hint"
    The closure has to *remember something it learns during a call*. A by-value capture is
    fixed for the object's life. Which capture form lets a closure write back into the
    variable it captured?

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    final class HeavyMailer
    {
        public function __construct()
        {
            echo "built\n";
        }
    }

    function lazy(callable $factory): Closure
    {
        $instance = null;

        return static function () use (&$instance, $factory): object {
            return $instance ??= $factory();
        };
    }

    $mailer = lazy(fn (): HeavyMailer => new HeavyMailer());

    echo "nothing built yet\n";

    $a = $mailer();
    $b = $mailer();
    $c = $mailer();

    var_dump($a === $b, $b === $c);
    ```

    ```
    nothing built yet
    built
    bool(true)
    bool(true)
    ```

    **Why it works:** `$instance` is captured **by reference**, so the assignment performed
    inside the closure on the first call persists in the shared variable and is visible to
    every later call. `$factory` is captured by value, which is correct — it never changes.
    The closure is `static` because it needs no `$this`; declaring that intent also makes it
    impossible to bind an object to it by accident.

    `use ($instance)` cannot work: a by-value capture is written once, when the closure is
    created. The closure could assign to its private copy, but the next call would start
    again from the copy stored in the object, so the instance would be rebuilt every time
    and `$a === $b` would be `false`.

    Symfony's `EventDispatcher::optimizeListeners()` uses a stronger version of the same
    idea — a `static` closure capturing both `&$listener` and `&$closure` so that the first
    invocation replaces the closure itself with the resolved callable. Same mechanism, one
    extra step of self-replacement.

    **Certification takeaway:** by-reference capture is the mechanism behind memoization,
    accumulators and lazy resolution. "Avoid `use (&$x)`" is a style preference, not a rule
    — the standard library and Symfony both rely on it where a closure must remember.

    **Official reference:** https://symfony.com/doc/8.0/service_container/service_closures.html

---

<small>Back to the lesson: [Anonymous Functions & Closures](closures.md) · Next: [Topic exam](closures-exam.md)</small>

# Guided Exercises — Object-Oriented Programming

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    an answer before revealing a hint, and to a full attempt before revealing the solution —
    a class resolution you predicted wrongly and then corrected sticks far better than one
    you read.

    Theory: **[Object-Oriented Programming](oop.md)** · Then: **[Topic exam](oop-exam.md)**

    All code targets **PHP 8.4**. `php -l` only checks syntax; visibility, hook and late
    static binding errors surface when the class actually **loads** or when the line runs.

## Exercise 1 · Discover which class `self` and `static` really name

**Objective:** See that one shared method body answers two different questions.

**Context:** A base class with a static method, and a subclass that adds nothing at all.

**Starting point:**

```php
<?php
declare(strict_types=1);

class Report
{
    public static function definingClass(): string { return self::class; }
    public static function calledClass(): string   { return static::class; }
}

final class PdfReport extends Report {}
```

**Task:** Predict the output of
`echo PdfReport::definingClass(), '|', PdfReport::calledClass();` **before** running it.
Then explain what information each keyword had access to.

**Expected observation:** `Report|PdfReport`. Same call site, same inheritance, two answers.

??? tip "Show a hint"
    One of the two was already replaced with a literal class name while the file was being
    compiled. Ask yourself which one could possibly know that `PdfReport` exists — the file
    declaring `Report` never mentions it.

??? success "Show the solution"
    ```
    Report|PdfReport
    ```

    `self::class` was resolved at **compile time** to the class the line is written in, so it
    prints `Report` no matter who calls it. `static::class` reads the **called class** the
    engine recorded when `PdfReport::calledClass()` was invoked, so it prints `PdfReport`.

    **Why it works:** the engine stores the class named in the last non-forwarding call
    alongside the executing method. `static::`, `static::class` and `get_called_class()` read
    that record; `self::` and `__CLASS__` never do — they carry no runtime component at all.

    **Certification takeaway:** the question is never "which class is this method in" but
    "which question is this keyword asking". `self` asks *where is this written*, `static`
    asks *who was called*.

    **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

## Exercise 2 · Minimal implementation — a subclass-safe named constructor

**Objective:** Write the factory correctly, and see what the wrong version costs.

**Context:** Every value object in a Symfony codebase gets a named constructor sooner or
later. `Symfony\Component\Uid\Uuid::fromString()` is the canonical one.

**Starting point:**

```php
<?php
declare(strict_types=1);

class Report
{
    public function __construct(public string $title) {}

    public static function untitled(): static
    {
        return new self('Untitled');
    }
}

final class PdfReport extends Report {}
```

**Task:** Predict what `PdfReport::untitled()` does. Then make it return a `PdfReport` by
changing exactly one word, and say why the declared return type made the bug loud rather
than silent.

**Expected observation:** the starting point throws a `TypeError`; changing `self` to
`static` makes it return a `PdfReport`.

??? tip "Show a hint"
    Two things are in conflict here: what `new self()` builds, and what `: static` promises.
    Write down the class each of them refers to when the caller is `PdfReport`.

??? success "Show the solution"
    The starting point fails at runtime:

    ```
    TypeError: Report::untitled(): Return value must be of type PdfReport, Report returned
    ```

    The fix is one word:

    ```php
    public static function untitled(): static
    {
        return new static('Untitled');   // subclass-safe
    }
    ```

    **Why it works:** `new self()` was compiled to `new Report()`. `new static()` asks the
    engine for the recorded called class, which is `PdfReport`. The `: static` return type is
    evaluated with the same rule, so the two now agree.

    Notice the class named in the error: `Report::untitled()` — the class where the body is
    *written* — while the expected type is `PdfReport`, the class that was *called*. The
    message is the whole concept in one line.

    **Certification takeaway:** declare `: static` on every inheritable named constructor.
    It costs nothing and converts a silently wrong object into a `TypeError` at the exact
    call site. Symfony does exactly this in `Uuid::fromString(): static`.

    **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

## Exercise 3 · Inspect the result — what a `get` hook changes about introspection

**Objective:** See that PHP 8.4 deliberately reports hooked properties differently depending
on who is asking.

**Context:** One backed property, one virtual property, four inspection functions.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Profile
{
    public string $first = 'Ada';
    public string $last = 'Lovelace';

    public string $full {
        get => $this->first.' '.$this->last;
    }
}

$p = new Profile();
```

**Task:** Predict, for each of `var_dump($p)`, `var_dump((array) $p)`,
`var_dump(get_object_vars($p))` and `echo json_encode($p)`, whether `full` appears. Then run
it and reconcile the differences.

**Expected observation:** `full` is absent from `var_dump()` and the array cast, present in
`get_object_vars()` and `json_encode()`.

??? tip "Show a hint"
    `full` is **virtual** — no hook touches `$this->full`, so the object stores nothing for
    it. Ask which of these four functions could produce a value for a slot that does not
    exist, and what it would have to call to do so.

??? success "Show the solution"
    ```
    var_dump($p)              → first, last                  (raw backing values)
    var_dump((array) $p)      → first, last                  (raw backing values)
    get_object_vars($p)       → first, last, full            (runs the get hook)
    json_encode($p)           → {"first":"Ada","last":"Lovelace","full":"Ada Lovelace"}
    ```

    Properties appear in declaration order, so `full` is last in the two hooked results and
    absent from the two raw ones.

    **Why it works:** the split is documented and intentional. `var_dump`, `serialize`,
    `unserialize`, array casting and `get_mangled_object_vars()` read the **raw backing
    value**, because debugging and persistence want what is actually stored.  `var_export`,
    `json_encode()`, `JsonSerializable` and `get_object_vars()` go **through the `get` hook**,
    because they produce the object's outward-facing representation. A virtual property has
    no backing value at all, so it simply does not appear in the first group.

    **Certification takeaway:** "a virtual property is missing from `var_dump()`" is correct
    behaviour, not a bug. Memorise the two lists as *raw* versus *hooked*, and remember that
    `(array)` and `get_object_vars()` — which people treat as equivalent — land on opposite
    sides.

    **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

## Exercise 4 · Change one variable — from `readonly` to `private(set)`

**Objective:** Feel the difference between "written once" and "written only from here".

**Context:** A `Report` whose title must not be changed from outside, but which needs a
`rename()` method internally.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Report
{
    public function __construct(public readonly string $title) {}

    public function rename(string $title): void
    {
        $this->title = $title;
    }
}
```

**Task:** Predict what `(new Report('a'))->rename('b')` does. Then change **one modifier** so
that `rename()` works while `$report->title = 'x'` from outside still fails. Finally, state
what that change costs you.

**Expected observation:** the starting point throws; `private(set)` fixes it, at the price of
making the property implicitly `final`.

??? tip "Show a hint"
    `readonly` restricts *how many times* the property may be written. What you actually want
    to restrict is *from where*. PHP 8.4 has a separate modifier for exactly that axis.

??? success "Show the solution"
    The starting point throws at the `rename()` call:

    ```
    Error: Cannot modify readonly property Report::$title
    ```

    Swap the modifier:

    ```php
    public function __construct(public private(set) string $title) {}
    ```

    `rename()` now works. From outside:

    ```
    Error: Cannot modify private(set) property Report::$title from global scope
    ```

    **Why it works:** `readonly` allows exactly **one** write, from the declaring scope —
    it is a lifetime restriction. `private(set)` allows **any number** of writes but only
    from inside the declaring class — it is a scope restriction. They are orthogonal tools,
    and the mistake is reaching for `readonly` when you meant encapsulation.

    Two costs to state explicitly. First, `private(set)` makes the property **implicitly
    `final`**: no subclass may redeclare it. Second, asymmetric visibility requires a
    **typed** property, the `set` visibility may never be *wider* than the read visibility,
    and `private( set )` with spaces is a parse error.

    **Certification takeaway:** `readonly` = once, ever. `private(set)` = as often as you
    like, from one place only. And `private(set)` silently implies `final`, which is the
    detail distractors are built on.

    **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

## Exercise 5 · Diagnose a failure from the message alone

**Objective:** Map four real PHP 8.4 fatals back to the rule each one enforced.

**Context:** You are handed only these errors from CI. No source, no stack trace.

**Starting point:**

```
(a) PHP Fatal error: Hooked properties cannot be readonly
(b) PHP Fatal error: Static property may not have asymmetric visibility
(c) PHP Fatal error: Cannot override final property Report::$title
(d) PHP Warning:  The magic method Bag::__get() must have public visibility
```

**Task:** For each one, name the rule that was broken and give the minimal fix. Say which of
the four is **not** fatal, and what that difference implies for the request that triggered it.

**Expected observation:** (a)–(c) stop the class from loading; (d) is only a warning and the
method still exists — but it will not be used as a magic method.

??? tip "Show a hint"
    Three of these are decisions the engine makes while *linking the class*, so nothing
    downstream runs. The fourth is a diagnostic emitted about a declaration the engine
    accepted anyway. Which category does a `Warning` belong to?

??? success "Show the solution"
    **(a)** Property hooks are **incompatible with `readonly`**. Fix: drop `readonly` and use
    asymmetric visibility if you wanted to restrict writes — `public private(set) string $s
    { get => ...; }`.

    **(b)** In PHP 8.4, asymmetric visibility applies to **instance properties only**. Fix:
    make the property non-static, or drop the `(set)` visibility. (PHP 8.5 lifts this, but
    8.5 is outside the 8.4 baseline this exam uses.)

    **(c)** Something made `Report::$title` final. Either it was declared `final` (possible
    on properties since 8.4), or — far more likely — it is `private(set)`, which is
    **implicitly final**. Fix: stop redeclaring it in the child, or change the parent's
    modifier.

    **(d)** Every magic method except `__construct()`, `__destruct()` and `__clone()` must be
    `public`. Fix: `public function __get(...)`.

    **Why it works:** (a), (b) and (c) are structural facts about the class, checked while it
    is **linked**, so the file never finishes loading and the whole application is down.
    (d) is an `E_WARNING`: the class loads, the method exists as an ordinary method, and the
    request completes — but reads of inaccessible properties silently stop routing through
    it. That is the worse failure mode of the two, because it is quiet.

    **Certification takeaway:** learn the severity, not just the rule. Magic-method
    **visibility** is a warning; a magic-method **type declaration** that does not match the
    documented signature is a fatal error. Confusing those two is a classic distractor pair.

    **Official reference:** https://www.php.net/manual/en/language.oop5.magic.php

## Exercise 6 · Handle an edge case — `clone`, shared state and `readonly`

**Objective:** Turn a shallow copy into a genuine one, then use the single legal second write
to a `readonly` property.

**Context:** `Symfony\Component\HttpFoundation\Request::__clone()` exists for exactly this
reason: it clones all seven of its `ParameterBag` properties so a duplicated request cannot
mutate the original.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Snapshot
{
    public function __construct(
        public readonly string $id,
        public readonly \ArrayObject $tags,
    ) {}
}

$a = new Snapshot('snap-1', new \ArrayObject(['draft']));
$b = clone $a;
$b->tags[] = 'published';
```

**Task:** Predict `count($a->tags)`. Then write a `__clone()` that gives the copy its own
`ArrayObject` **and** appends `-copy` to `$id`. Explain why the second half is legal at all,
given that `$id` is `readonly`.

**Expected observation:** `count($a->tags)` is **2** before the fix and **1** after. `$id` may
be reassigned, but only inside `__clone()`.

??? tip "Show a hint"
    `clone` copies property *slots*. Both slots now hold the same `ArrayObject` handle, and
    `readonly` never promised the *object inside* would not change. For the second half, ask
    what PHP 8.3 added to the cloning rules.

??? success "Show the solution"
    ```php
    public function __clone(): void
    {
        $this->id = $this->id.'-copy';    // legal since PHP 8.3, inside __clone only
        $this->tags = clone $this->tags;  // break the shared reference
    }
    ```

    Before the fix, `$a->tags` and `$b->tags` are the same `ArrayObject`, so appending through
    `$b` is visible through `$a`: `count($a->tags) === 2`. After it, each snapshot owns its
    own collection and the count stays at 1.

    **Why it works:** `clone` performs a **shallow** copy of every property, then runs
    `__clone()` **on the new object**. Inside it, `$this` is the copy, which is why the fix-up
    cannot affect the original. `readonly` forbids *modification of the property*, not
    *mutation of the object it points at* — the manual calls that interior mutability — so
    the shared `ArrayObject` was never protected in the first place.

    The `$id` reassignment is legal because **PHP 8.3 allows a readonly property to be
    reinitialised during cloning, from `__clone()`**. It is the only place a second write is
    permitted. PHP 8.4 tightened one detail: you may not take a **reference** to a readonly
    property inside `__clone()` (`$ref = &$this->id`), matching the rule already in force
    during initialisation.

    **Certification takeaway:** three facts, in this order — `clone` is shallow, `__clone()`
    runs afterwards on the copy, and `__clone()` is the sole legal second write to a
    `readonly` property (8.3+). `readonly` on an object property protects the handle, never
    the contents.

    **Official reference:** https://www.php.net/manual/en/language.oop5.cloning.php

## Exercise 7 · Expert challenge — forwarding versus non-forwarding calls

**Objective:** Predict late static binding when the call chain goes through several forms.

**Context:** This is the part of LSB most summaries omit, and it is where the harder exam
questions live. The rule is defined on *calls*, not on keywords.

**Starting point:**

```php
<?php
declare(strict_types=1);

class A
{
    public static function who(): string { return static::class; }

    public static function viaSelf(): string   { return self::who(); }
    public static function viaStatic(): string { return static::who(); }
    public static function viaName(): string   { return A::who(); }
}

class B extends A
{
    public static function viaParent(): string { return parent::who(); }
}
```

**Task:** Predict the output of `B::who()`, `B::viaSelf()`, `B::viaStatic()`, `B::viaParent()`
and `B::viaName()`. Then state the general rule in one sentence, and explain why exactly one
of the five differs from the others.

**Expected observation:** `B`, `B`, `B`, `B` — and `A` for `viaName()`.

??? tip "Show a hint"
    The engine stores a class when a static call is made. Some call forms hand the stored
    value on unchanged, and one form replaces it. Sort the five calls into those two groups
    before predicting anything.

??? success "Show the solution"
    ```
    B::who()        → B
    B::viaSelf()    → B
    B::viaStatic()  → B
    B::viaParent()  → B
    B::viaName()    → A
    ```

    **Why it works:** late static binding stores **the class named in the last non-forwarding
    call**. A call made through `self::`, `parent::`, `static::` or `forward_static_call()` is
    a **forwarding** call: it passes the stored class through untouched, which is why the
    first four all report `B` even though the bodies live on `A`.

    `A::who()` names a class explicitly. That is a **non-forwarding** call, so it starts a new
    resolution and overwrites the stored class with `A`. Nothing about being "inside `A`"
    caused this — writing `B::who()` there would have stored `B` instead.

    The one-sentence rule: **a call through `self`, `parent`, `static` or
    `forward_static_call()` keeps the called class; naming any class explicitly resets it.**

    Two limits from the same manual page complete the picture: in a **non-static** context the
    called class is the class of the `$this` object, and `static::` can only be used to reach
    **static** properties.

    **Certification takeaway:** when a question shows a chain of static calls, do not scan for
    `self` versus `static` in the final method. Walk the chain and find the last call that
    named a class literally — that class is what `static::` will report.

    **Official reference:** https://www.php.net/manual/en/language.oop5.late-static-bindings.php

---

<small>Back to the lesson: [Object-Oriented Programming](oop.md) · Next: [Topic exam](oop-exam.md)</small>

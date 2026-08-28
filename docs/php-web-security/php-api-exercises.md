# Guided Exercises — PHP API (up to 8.4)

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit
    to a prediction before revealing a hint, and to a full attempt before revealing the
    solution — a version you dated wrongly and then corrected sticks far better than one
    you read off a table.

    Theory: **[PHP API (up to 8.4)](php-api.md)** · Then: **[Topic exam](php-api-exam.md)**

    All code targets **PHP 8.4**. `php -l` only checks syntax — every rule in this
    chapter is a *compile* diagnostic raised when the class is declared, so actually run
    the file. Add `-d error_reporting=E_ALL` to see the 8.4 deprecations.

## Exercise 1 · Date the code before you run it

**Objective:** Build the reflex the exam actually tests — reading a feature and naming
its release.

**Context:** One file, five features, five different PHP versions.

**Starting point:**

```php
<?php
declare(strict_types=1);

enum Level: string                                  // (a)
{
    case Low = 'low';
    case High = 'high';
}

final readonly class Reading                        // (b)
{
    public const string UNIT = 'C';                 // (c)

    public function __construct(public float $value) {}
}

function describe(Reading $r): string
{
    return match (true) {                           // (d)
        $r->value > 30.0 => 'hot',
        default => 'mild',
    };
}

final class Sensor
{
    public private(set) ?Reading $last = null;      // (e)
}
```

**Task:** For each marker (a)–(e), name the **minimum PHP version** that can parse it.
Then state the single version this whole file requires.

**Expected observation:** The file's floor is the maximum of the five, not the average —
one 8.4 construct pins the entire file to 8.4.

??? tip "Show a hint"
    Two of the five are 8.1, one is 8.2, one is 8.3 and one is 8.4. The 8.2 one is a
    *class-level* modifier, and the 8.3 one adds a type where none was allowed before.

??? success "Show the solution"
    - **(a)** `enum` — **8.1**.
    - **(b)** `readonly class` — **8.2**. (`readonly` on a *property* is 8.1; on a class
      it is 8.2.)
    - **(c)** `const string UNIT` — typed class constant, **8.3**.
    - **(d)** `match` — **8.0**.
    - **(e)** `public private(set)` — asymmetric visibility, **8.4**.

    The file requires **PHP 8.4**, because the floor is the newest construct present.

    **Why it works:** each syntax was added by a specific RFC in a specific minor
    release, and the parser rejects it outright before then. There is no polyfill for
    syntax — a library can back-port a *function*, never a keyword.

    **Certification takeaway:** the two pairs the exam swaps most often are
    `readonly` property (8.1) vs `readonly class` (8.2), and union types (8.0) vs
    intersection types (8.1). Anchor those four and the rest of the table follows.

    **Official reference:** https://www.php.net/manual/en/migration84.new-features.php

## Exercise 2 · Minimal implementation — replace a getter/setter with a hook

**Objective:** Write your first property hook and see the boilerplate disappear.

**Context:** A cart total that must never go negative.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Cart
{
    private float $rawTotal = 0.0;

    public function getTotal(): float
    {
        return $this->rawTotal;
    }

    public function setTotal(float $v): void
    {
        $this->rawTotal = max(0.0, $v);
    }
}
```

**Task:** Rewrite `Cart` so callers write `$cart->total = -5.0;` and read
`$cart->total`, with the clamp preserved and **no** private backing field. Predict what
`$cart->total` returns after assigning `-5.0`.

**Expected observation:** `float(0)` — the hook clamped the value on the way in.

??? tip "Show a hint"
    You need only a `set` hook: reads have no logic, so leave `get` out and let the
    default read behaviour apply. Then ask yourself what the short `set => expr` form
    does with the expression's result.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    final class Cart
    {
        public float $total = 0.0 {
            set => max(0.0, $value);
        }
    }

    $cart = new Cart();
    $cart->total = -5.0;
    var_dump($cart->total);   // float(0)
    ```

    **Why it works:** the short `set` form writes **the value the expression evaluates
    to** into the property's backing storage. Because the hook's parameter type would be
    the same as the property type, it may be omitted entirely, and the incoming value is
    automatically named `$value`. No `get` hook is declared, so reading a *backed*
    property falls back to the default read.

    **Certification takeaway:** on a backed property, an omitted hook means "default
    behaviour". On a **virtual** property, an omitted hook means the operation **does not
    exist** and using it is an error — the same omission, two opposite outcomes.

    **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

## Exercise 3 · Inspect the result — backed or virtual?

**Objective:** Prove, from the outside, whether a hooked property occupies storage.

**Context:** Two hooked properties on one class, only one of which is virtual.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Cart
{
    public float $total = 0.0 {
        set => max(0.0, $value);
    }

    public float $totalWithVat {
        get => $this->total * 1.2;
    }
}

$cart = new Cart();
$cart->total = 100.0;
```

**Task:** Predict the output of `var_dump((array) $cart)` and of
`echo json_encode($cart)`. They will **not** agree — say which property is missing from
which, and why, before you run it.

**Expected observation:** the array cast shows only `total`; `json_encode()` shows both.

??? tip "Show a hint"
    One of these two tools is a debugging tool and one is a presentation tool. The
    manual assigns each of them to either "raw backing value" or "goes through the `get`
    hook".

??? success "Show the solution"
    ```php
    var_dump((array) $cart);
    // array(1) { ["total"]=> float(100) }

    echo json_encode($cart);
    // {"total":100,"totalWithVat":120}
    ```

    `$totalWithVat` is **virtual**: its hooks never mention `$this->totalWithVat`, so the
    object allocates no slot for it — hence it cannot appear in a raw array cast.
    `$total` is **backed**, because the short `set` writes to it.

    **Why it works:** the manual specifies exactly which mechanisms read raw storage and
    which run the `get` hook. `var_dump()`, `serialize()`, `unserialize()`, array casting
    and `get_mangled_object_vars()` use the **raw value**; `var_export()`,
    `json_encode()`, `get_object_vars()` and `JsonSerializable` use the **`get` hook**.

    **Certification takeaway:** a cast next to a `json_encode()` is the fastest possible
    diagnostic for "is this property backed?". If it appears in the cast, it has storage.

    **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

## Exercise 4 · Change one variable — braced `set` versus arrow `set`

**Objective:** Discover the single most misleading property-hook shape.

**Context:** A temperature object that is *supposed* to be virtual: `$fahrenheit`
should store nothing and derive everything from `$celsius`.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Temperature
{
    public float $celsius = 0.0;

    public float $fahrenheit {
        get => $this->celsius * 9 / 5 + 32;
        set (float $f) => $this->celsius = ($f - 32) * 5 / 9;
    }
}

$t = new Temperature();
$t->fahrenheit = 212.0;
```

**Task:** Run it, then `var_dump((array) $t)`. Predict how many entries the cast shows.
Then change **only** the arrow `set` into a braced `set (float $f) { ... }` and run it
again.

**Expected observation:** with the arrow form the cast shows **two** entries; with the
braced form it shows **one**.

??? tip "Show a hint"
    Re-read what the short `set => expr` form does with the value the expression
    evaluates to. What is the value of the expression `$this->celsius = 100.0`?

??? success "Show the solution"
    With the arrow form:

    ```
    array(2) {
      ["celsius"]=>  float(100)
      ["fahrenheit"]=> float(100)
    }
    ```

    The short `set` writes **the expression's result** into `$fahrenheit`'s own backing
    storage. An assignment expression evaluates to the assigned value, so the object now
    stores `100.0` under `fahrenheit` — a number that is neither Fahrenheit nor ever
    read, because the `get` hook ignores it. The property is **backed**, not virtual.

    The fix is one pair of braces:

    ```php
    public float $fahrenheit {
        get => $this->celsius * 9 / 5 + 32;
        set (float $f) { $this->celsius = ($f - 32) * 5 / 9; }
    }
    ```

    Now neither hook names `$this->fahrenheit`, so the property is genuinely virtual and
    the cast shows only `celsius` — while `json_encode()` still reports both, through the
    `get` hook.

    **Why it works:** "virtual" is decided **syntactically at compile time**: a property
    is backed if any hook references it by exact syntax, and the implicit write performed
    by a short `set` counts. Braces hand the write back to you, so you can send it
    elsewhere.

    **Certification takeaway:** arrow `set` = "modify then store here". Braced `set` =
    "I will decide where this goes". Choosing the arrow for a derived property silently
    doubles the object's memory and stores a meaningless value.

    **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

## Exercise 5 · Diagnose four failures from their messages alone

**Objective:** Turn the 8.4 property rules into a lookup you can run under exam pressure.

**Context:** Four one-line classes, four different compile-time fatals.

**Starting point:**

```
1) Fatal error: Hooked properties cannot be readonly
2) Fatal error: Property with asymmetric visibility C::$p must have type
3) Fatal error: Visibility of property C::$p must not be weaker than set visibility
4) Fatal error: Cannot override final property P::$p
```

**Task:** For each message, write the one-line declaration that produced it and the
minimal fix. For (4), explain why the parent never wrote the word `final`.

**Expected observation:** all four are refused when the class is **declared**, not when
a property is accessed.

??? tip "Show a hint"
    Three of the four are about a single modifier being illegal in combination with
    another. The fourth is about a modifier that *implies* `final` without saying so.

??? success "Show the solution"
    **(1)** `public readonly string $p { get => 'x'; }` — hooks and `readonly` are
    mutually exclusive. Fix: drop `readonly` and use `public private(set)` if you needed
    to restrict writes. The manual explicitly redirects you there.

    **(2)** `public private(set) $p;` — asymmetric visibility requires a **typed**
    property. Fix: `public private(set) string $p;`.

    **(3)** `protected public(set) string $p;` — the write scope may never be *wider*
    than the read scope. Fix: `protected protected(set) string $p;` or
    `public protected(set) string $p;`.

    **(4)** The parent declared `public private(set) string $p;`. A `private(set)`
    property is **automatically `final`**, so no child may redeclare it — not even to
    widen the read visibility. Fix: use `protected(set)` in the parent if subclasses must
    redeclare.

    **Why it works:** all four are structural rules checked while the class is linked, so
    none of them can be reached at runtime and none can be caught. The messages name the
    rule, not the symptom — read the noun.

    **Certification takeaway:** memorise the caveat list as four words —
    **typed**, **not-wider**, **non-static**, **final**. Every asymmetric-visibility
    question is one of those four.

    **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

## Exercise 6 · Handle an edge case — what 8.4 changed about `readonly`

**Objective:** Correct the single most out-of-date `readonly` claim.

**Context:** Most cheat sheets say a `readonly` property can only be written by the
declaring class. On PHP 8.4 that is no longer true.

**Starting point:**

```php
<?php
declare(strict_types=1);

class Base
{
    public readonly string $id;
}

final class Child extends Base
{
    public function __construct()
    {
        $this->id = 'from-child';
    }
}

echo (new Child())->id;
```

**Task:** Predict whether this runs on PHP 8.4, and whether it would have run on
PHP 8.3. Then predict what happens if you add `class Plain extends ReadonlyThing {}`
where `ReadonlyThing` is declared `readonly class`.

**Expected observation:** it prints `from-child` on 8.4; the extra `extends` is a fatal.

??? tip "Show a hint"
    Ask what *implicit set-visibility* `readonly` carries. It is one of the three
    visibility keywords, and 8.4 changed which one.

??? success "Show the solution"
    It prints **`from-child`**. As of **PHP 8.4.0**, `readonly` properties are implicitly
    **`protected(set)`**, so a child class may perform the single initialisation. Prior
    to 8.4 they were implicitly **private-set** and this exact code was an
    `Error: Cannot initialize readonly property Base::$id from scope Child`.

    Everything else about `readonly` is unchanged: it needs a **type**, forbids a
    **default value**, cannot be **static**, allows exactly one write, and does not stop
    interior mutation of a stored object.

    The inheritance question is symmetric and both directions fatal:

    ```
    Fatal error: Non-readonly class B cannot extend readonly class A
    Fatal error: Readonly class B cannot extend non-readonly class A
    ```

    **Why it works:** `readonly` is a *write-count* rule layered on top of a *write-scope*
    rule. 8.4 unified the scope half with the new asymmetric-visibility model, and
    `protected(set)` is the level that lets inheritance work. The `readonly class`
    inheritance rule exists because a plain child could otherwise add a mutable property
    and break the guarantee the parent advertises.

    **Certification takeaway:** on the 8.4 baseline, "only the declaring class may
    initialise a `readonly` property" is **false**. Any option asserting it is describing
    PHP ≤ 8.3.

    **Official reference:** https://www.php.net/manual/en/language.oop5.properties.php

## Exercise 7 · Expert challenge — one class, five releases, zero deprecations

**Objective:** Combine the whole chapter, then justify every modifier you chose.

**Context:** An audit-log entry for a Symfony 8 application. The requirements are
deliberately in tension.

**Starting point:**

```php
<?php
declare(strict_types=1);

enum Severity: string
{
    case Info = 'info';
    case Error = 'error';
}
```

**Task:** Write `final class AuditEntry` satisfying **all** of the following, then answer
the three questions below.

1. `severity` is set once at construction and never changes; it must be readable
   everywhere.
2. `message` is readable everywhere, writable only inside the class, and is always
   trimmed on write.
3. `summary` is readable everywhere, stores nothing, and reads
   `"<severity value>: <message>"`.
4. A static factory `fromRequest(?string $raw)` accepts an untrusted severity string and
   never throws, defaulting to `Severity::Info`.
5. The signature of `fromRequest()` must emit **no deprecation** on PHP 8.4.

Then answer: **(a)** why can `message` not be `readonly`? **(b)** why can no subclass
ever redeclare `message`? **(c)** which of the three properties appears in
`(array) $entry`?

**Expected observation:** exactly one property shows up in the array cast.

??? tip "Show a hint"
    Requirement 2 rules out `readonly` twice over — once for the repeated writes, once
    for the hook. Requirement 5 is about how you type a parameter whose default is
    `null`. Requirement 3 decides backed-versus-virtual on its own.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    enum Severity: string
    {
        case Info = 'info';
        case Error = 'error';
    }

    final class AuditEntry
    {
        public private(set) string $message = '' {
            set => trim($value);
        }

        public string $summary {
            get => $this->severity->value.': '.$this->message;
        }

        public function __construct(
            public readonly Severity $severity = Severity::Info,
        ) {}

        public static function fromRequest(?string $raw): self
        {
            return new self(Severity::tryFrom($raw ?? '') ?? Severity::Info);
        }

        public function record(string $text): void
        {
            $this->message = $text;
        }
    }
    ```

    **(a)** `message` cannot be `readonly` for two independent reasons. `readonly`
    permits exactly **one** write, but `record()` may be called repeatedly. And
    `readonly` is **incompatible with hooks** outright —
    `Fatal error: Hooked properties cannot be readonly`. `public private(set)` gives the
    external immutability that was actually wanted, with unlimited internal writes.

    **(b)** A `private(set)` property is **automatically `final`**. Any subclass
    redeclaration, even one that only widened the read visibility, fails with
    `Cannot override final property`. (`final class` already forbids subclasses here —
    the point is that `private(set)` would forbid it even on a non-final class.)

    **(c)** Only `message`. `summary` is **virtual** — its `get` hook never mentions
    `$this->summary`, so no storage is allocated. `severity` *is* backed and does appear,
    so the cast shows **two** entries in total; among the three declared *hooked or
    restricted* members, `message` is the one whose hook still leaves storage behind.
    `json_encode()`, by contrast, runs the `get` hooks and reports all three.

    **Why it works:** each requirement maps to exactly one feature, and they compose
    because they answer different questions. *How many writes?* → `readonly`.
    *Who may write?* → `private(set)`. *What runs on access?* → hooks. Requirement 5 is
    the 8.4 deprecation: `fromRequest(string $raw = null)` would emit
    `Implicitly marking parameter $raw as nullable is deprecated`, so the parameter is
    typed `?string` explicitly.

    **Certification takeaway:** when a question offers `readonly` and `private(set)` as
    alternatives, decide on *write count* first. If the answer is "more than once,
    internally", `readonly` is eliminated before you even reach the hook rule.

    **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

---

<small>Back to the lesson: [PHP API (up to 8.4)](php-api.md) · Next: [Topic exam](php-api-exam.md)</small>

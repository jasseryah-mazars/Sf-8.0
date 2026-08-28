# Guided Exercises — Interfaces & Type Declarations

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    an answer before revealing a hint, and to a full attempt before revealing the solution —
    a variance rule you predicted wrongly and then corrected sticks far better than one you
    read.

    Theory: **[Interfaces & Type Declarations](interfaces.md)** · Then:
    **[Topic exam](interfaces-exam.md)**

    All code targets **PHP 8.4**. Run snippets with `php -l` for syntax, but note that
    variance errors only surface when the class actually **loads**.

## Exercise 1 · Discover what a contract actually forbids

**Objective:** See that interface compliance is checked at load time, not call time.

**Context:** A `Pricer` contract with one method.

**Starting point:**

```php
<?php
declare(strict_types=1);

interface Pricer
{
    public function price(int $quantity): int;
}

final class FlatPricer implements Pricer
{
    // intentionally missing
}
```

**Task:** Predict what PHP does with this file, and *when*. Then reason about what changes
if the file is only autoloaded, never instantiated.

**Expected observation:** A fatal error naming the unimplemented method — raised while the
class is being declared.

??? tip "Show a hint"
    Ask yourself whether PHP could possibly wait until `price()` is called to notice it is
    missing. What would `instanceof Pricer` have to answer in the meantime?

??? success "Show the solution"
    PHP raises:

    ```
    Fatal error: Class FlatPricer contains 1 abstract method and must therefore be
    declared abstract or implement the remaining methods (Pricer::price)
    ```

    **Why it works:** compliance is verified when the class is **linked** — the moment the
    declaration is compiled, or in a Symfony app the moment the autoloader loads the file.
    Merely autoloading it is enough; no instantiation and no call are required.

    **Certification takeaway:** interface violations are **compile/link-time fatals**, not
    runtime exceptions. This is why a bad signature takes the whole application down instead
    of failing one endpoint — and why you cannot `try/catch` your way past it.

    **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

## Exercise 2 · Minimal implementation, then narrow the return

**Objective:** Confirm covariance by making a return type *more* specific.

**Context:** `Money` and `TaxedMoney extends Money`.

**Starting point:**

```php
<?php
declare(strict_types=1);

class Money {}
class TaxedMoney extends Money {}

interface Pricer
{
    public function price(int $quantity): Money;
}
```

**Task:** Implement `Pricer` twice — once returning `Money`, once returning `TaxedMoney`.
Predict whether each links.

**Expected observation:** Both link. The `TaxedMoney` version is a legal covariant override.

??? tip "Show a hint"
    The caller was promised "at least a `Money`". Does receiving a `TaxedMoney` break that
    promise, or over-deliver on it?

??? success "Show the solution"
    ```php
    final class Plain implements Pricer
    {
        public function price(int $quantity): Money { return new Money(); }
    }

    final class Taxed implements Pricer
    {
        public function price(int $quantity): TaxedMoney { return new TaxedMoney(); }
    }
    ```

    **Why it works:** return types are **covariant** — an implementation may return a
    *subtype* of what the contract declares. Every caller expecting `Money` is satisfied,
    because a `TaxedMoney` **is** a `Money`.

    **Certification takeaway:** narrowing a return is always safe and always legal. The
    memory hook is *give more*.

    **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

## Exercise 3 · Inspect what the class really carries

**Objective:** See that an object records every interface, including inherited ones.

**Context:** Interfaces compose through `extends`.

**Starting point:**

```php
<?php
declare(strict_types=1);

interface Timestamped { public function touchedAt(): \DateTimeImmutable; }
interface Auditable extends Timestamped, \Stringable {}

final class Invoice implements Auditable
{
    public function touchedAt(): \DateTimeImmutable { return new \DateTimeImmutable(); }
    public function __toString(): string { return 'invoice'; }
}
```

**Task:** Predict the full output of `class_implements(new Invoice())` before running it.
How many entries, and which?

**Expected observation:** Three — `Auditable`, `Timestamped` and `Stringable`. Implementing
one interface pulled in its whole ancestry.

??? tip "Show a hint"
    `Auditable` does not declare any method of its own. Does that make it a thin wrapper, or
    does `extends` genuinely merge both parents into the contract?

??? success "Show the solution"
    ```php
    var_dump(array_keys(class_implements(new Invoice())));
    // Auditable, Timestamped, Stringable
    ```

    Every one of these is `true` for `instanceof`, including `Stringable`, which `Invoice`
    never named directly.

    **Why it works:** interface inheritance is **transitive**. At link time the engine
    flattens the ancestry into a single interface set stored on the class, which is exactly
    what makes runtime `instanceof` a cheap set lookup rather than a graph walk.

    **Certification takeaway:** `instanceof` matches the class, all parents, and **every**
    interface in the closure — not just the ones written after `implements`.

    **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

## Exercise 4 · Change one variable: widen the parameter

**Objective:** Confirm contravariance, the rule people reverse most often.

**Context:** `Cart extends Basket`, and a contract that accepts a `Cart`.

**Starting point:**

```php
<?php
declare(strict_types=1);

class Basket {}
class Cart extends Basket {}

interface Pricer
{
    public function price(Cart $cart): int;
}
```

**Task:** Implement `price(Basket $cart): int` — a **wider** parameter. Predict the result.
Then predict the opposite change, `price(PremiumCart $cart)`.

**Expected observation:** Widening links fine. Narrowing is a fatal error.

??? tip "Show a hint"
    The contract promised callers "you may pass a `Cart`". Which of the two changes could
    ever cause such a caller to be refused?

??? success "Show the solution"
    ```php
    final class Flexible implements Pricer
    {
        public function price(Basket $cart): int { return 0; }   // legal: contravariant
    }
    ```

    Narrowing instead produces:

    ```
    Fatal error: Declaration of Strict::price(PremiumCart $cart): int must be
    compatible with Pricer::price(Cart $cart): int
    ```

    **Why it works:** parameters are **contravariant** — an implementation may accept a
    *supertype*. Every caller holding a `Cart` still type-checks, because a `Cart` is a
    `Basket`. Narrowing would turn away callers the contract explicitly allowed.

    **Certification takeaway:** parameters widen, returns narrow. Reversed, both are fatal.
    The mnemonic that survives exam pressure: *give more, ask for less*.

    **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

## Exercise 5 · Diagnose a failure from the message alone

**Objective:** Read a real variance fatal and locate the violation without running anything.

**Context:** You are handed only this error from CI.

**Starting point:**

```
Fatal error: Declaration of CsvExporter::export(Report $r): iterable must be
compatible with Exporter::export(Report $r): \Generator
```

**Task:** Name which rule was broken, which side is too wide, and give the minimal fix.

**Expected observation:** A covariance violation on the **return** type.

??? tip "Show a hint"
    `\Generator` implements `Iterator`, so every `Generator` is `iterable`. Which of the two
    types is the more general one — and which side of the message is yours?

??? success "Show the solution"
    The contract promises a `\Generator`. `CsvExporter` returns `iterable`, which is
    **wider** — an array would satisfy it, and callers relying on `->send()` or `->getReturn()`
    would break. That is a covariance violation.

    Minimal fix — return the promised type or narrower:

    ```php
    public function export(Report $r): \Generator { yield 'a,b,c'; }
    ```

    **Why it works:** in the message the **left** side is your declaration and the **right**
    side is the contract. Compare their generality: a wider *return* breaks covariance, a
    narrower *parameter* breaks contravariance. Here the return widened.

    **Certification takeaway:** these messages are mechanical. Left = yours, right = the
    contract; then ask which is wider and on which side of the signature.

    **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

## Exercise 6 · Handle an edge case — `never`, and interface properties

**Objective:** Explore two rules that look wrong until you see why they hold.

**Context:** Both are current-version behaviour and prime distractor material.

**Starting point:**

```php
<?php
declare(strict_types=1);

interface Serializer
{
    public function serialize(): string;
}

interface HasSlug
{
    public string $slug { get; }
}
```

**Task:** Answer two questions. **(a)** Is `public function serialize(): never` a legal
override of `: string`? **(b)** Can a `readonly` property satisfy `HasSlug::$slug`? Would it
still satisfy a `{ get; set; }` requirement?

**Expected observation:** (a) legal; (b) yes for `{ get; }`, no for `{ set; }`.

??? tip "Show a hint"
    For (a): what values can a `never` function actually return? For (b): what operation does
    `readonly` permanently forbid after initialisation?

??? success "Show the solution"
    **(a) Legal.** `never` is the **bottom type**: the function always throws or exits, so it
    never produces a value that could violate `: string`. It satisfies *every* return
    contract vacuously, which makes it the narrowest possible covariant override.

    ```php
    final class Broken implements Serializer
    {
        public function serialize(): never { throw new \LogicException('unsupported'); }
    }
    ```

    **(b)** A `readonly` property **can** satisfy `{ get; }`:

    ```php
    final class Page implements HasSlug
    {
        public function __construct(public readonly string $slug) {}
    }
    ```

    It **cannot** satisfy `{ set; }`, because `readonly` forbids the write the contract
    requires. Interfaces may declare properties as of **PHP 8.4.0**, and the declaration
    states which operations are demanded.

    **Certification takeaway:** two statements that are now false — "`never` cannot override
    a typed return" and "interfaces cannot have properties". Both are 8.1/8.4 changes and
    both are favourite distractors.

    **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

## Exercise 7 · Expert challenge — one signature, two contracts

**Objective:** Satisfy two interfaces that declare the same method with *different* types.

**Context:** This is the hardest legal case in the topic, and it is in the manual.

**Starting point:**

```php
<?php
declare(strict_types=1);

class Foo {}
class Bar extends Foo {}

interface A { public function myfunc(Foo $arg): Foo; }
interface B { public function myfunc(Bar $arg): Bar; }
```

**Task:** Write a single `MyClass implements A, B`. Then justify why exactly one signature
works, and prove no other combination does.

**Expected observation:** `myfunc(Foo $arg): Bar` is the only legal signature.

??? tip "Show a hint"
    Handle each side separately. The parameter must be wide enough for **both** contracts;
    the return must be narrow enough for **both**. Which concrete type satisfies each?

??? success "Show the solution"
    ```php
    final class MyClass implements A, B
    {
        public function myfunc(Foo $arg): Bar { return new Bar(); }
    }
    ```

    **Why it works:** solve the two axes independently.

    - *Parameter (contravariant, must be equal or wider than both):* `A` demands at least
      `Foo`, `B` at least `Bar`. Since `Bar extends Foo`, `Foo` is wider than both — so `Foo`
      works and `Bar` does not (it would narrow `A`'s parameter).
    - *Return (covariant, must be equal or narrower than both):* `A` allows up to `Foo`, `B`
      requires at most `Bar`. `Bar` is narrower than both — so `Bar` works and `Foo` does not
      (it would widen `B`'s return).

    That leaves exactly one legal pairing: widest parameter, narrowest return. The other
    three combinations each violate one rule.

    **Certification takeaway:** with multiple contracts, the parameter converges on the
    **widest** requirement and the return on the **narrowest**. If those two demands ever
    cross, no legal signature exists and the class cannot be written at all.

    **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

---

<small>Back to the lesson: [Interfaces & Type Declarations](interfaces.md) · Next: [Topic exam](interfaces-exam.md)</small>

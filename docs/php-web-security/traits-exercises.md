# Guided Exercises — Traits

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one, and they
    share a single running example — an invoicing domain that needs auditing behaviour spread
    across unrelated classes. Commit to a prediction before revealing a hint, and to a full
    attempt before revealing the solution. A precedence rule you predicted wrongly and then
    corrected sticks far better than one you read.

    Theory: **[Traits](traits.md)** · Then: **[Topic exam](traits-exam.md)**

    All code targets **PHP 8.4**. Every snippet runs as-is with
    `php file.php`; several are *designed* to fatal, and the error text is part of the lesson.

## Exercise 1 · Discover the precedence order by contradiction

**Objective:** Establish, by experiment rather than by memorising, that a trait method beats
an inherited one but loses to the exhibiting class's own.

**Context:** `Document` is a base class with a `describe()` method. An `Auditable` trait wants
to decorate that description. Two subclasses use the trait; one of them also defines
`describe()` itself.

**Starting point:**

```php
<?php
declare(strict_types=1);

class Document
{
    public function describe(): string { return 'document'; }
}

trait Auditable
{
    public function describe(): string { return 'audited '.parent::describe(); }
}

class Invoice extends Document
{
    use Auditable;
}

class Receipt extends Document
{
    use Auditable;
    public function describe(): string { return 'receipt (own)'; }
}

echo (new Invoice())->describe(), PHP_EOL;
echo (new Receipt())->describe(), PHP_EOL;
```

**Task:** Before running it, write down what each of the two `echo` lines prints. Then run it.
If either prediction was wrong, state which rule you had backwards.

**Expected observation:** Two different winners from the same trait — one line proves the
trait beat the parent, the other proves the class beat the trait.

??? tip "Show a hint"
    There is a second thing worth noticing in the trait body: it calls `parent::describe()`.
    Ask yourself which class `parent` can possibly mean, given that the trait itself has no
    parent and is not part of any hierarchy.

??? success "Show the solution"
    ```
    audited document
    receipt (own)
    ```

    `Invoice` has no `describe()` of its own, so the trait's copy is inserted and it shadows
    `Document::describe()`. `Receipt` declares its own `describe()`, so the trait's version is
    never inserted at all and the class's method runs.

    The `parent::describe()` call works because the trait's body is copied into `Invoice`
    *before* it is executed. At that point `parent` simply means `Invoice`'s parent,
    `Document`. A trait can therefore reference `parent::`, `self::` and `static::` freely —
    they are resolved relative to the exhibiting class, not the trait.

    **Why it works:** the manual states the order without ambiguity: "members from the current
    class override Trait methods, which in turn override inherited methods." Both lines of
    output are that one sentence, split in two.

    **Certification takeaway:** memorise **class > trait > inherited parent**. The exam's
    favourite reversal is "the trait wins over the using class" — it never does. A trait
    method only ever displaces something *inherited*.

    **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.precedence

## Exercise 2 · Compose two traits into one class

**Objective:** Build the minimal working composition: two independent traits, each carrying
both behaviour and state, combined into a single class.

**Context:** Invoices need timestamps and an audit log. Neither concern belongs in a base
class, because receipts, contracts and exports will want them too — and they have no common
ancestor.

**Starting point:**

```php
<?php
declare(strict_types=1);

trait Timestampable
{
    private ?\DateTimeImmutable $touchedAt = null;

    public function touch(): void { $this->touchedAt = new \DateTimeImmutable('2026-01-01'); }
    public function touchedAt(): ?\DateTimeImmutable { return $this->touchedAt; }
}

trait Loggable
{
    /** @var list<string> */
    private array $log = [];

    public function record(string $line): void { $this->log[] = $line; }

    /** @return list<string> */
    public function history(): array { return $this->log; }
}
```

**Task:** Write a `final class Invoice` that uses **both** traits and exposes one method
`issue()` which touches the timestamp and then records a line containing the formatted date.
Print the history.

**Expected observation:** One array entry, `issued at 2026-01-01`. The class body itself
contains no timestamp field and no log array — both arrived from the traits.

??? tip "Show a hint"
    You can write `use Timestampable, Loggable;` on one line or two separate `use` statements
    inside the class body; both are equivalent here. Inside `issue()`, the trait methods are
    ordinary `$this->` calls — nothing about them is special once they have been copied in.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    trait Timestampable
    {
        private ?\DateTimeImmutable $touchedAt = null;

        public function touch(): void { $this->touchedAt = new \DateTimeImmutable('2026-01-01'); }
        public function touchedAt(): ?\DateTimeImmutable { return $this->touchedAt; }
    }

    trait Loggable
    {
        /** @var list<string> */
        private array $log = [];

        public function record(string $line): void { $this->log[] = $line; }

        /** @return list<string> */
        public function history(): array { return $this->log; }
    }

    final class Invoice
    {
        use Timestampable;
        use Loggable;

        public function issue(): void
        {
            $this->touch();
            $this->record('issued at '.$this->touchedAt()->format('Y-m-d'));
        }
    }

    $i = new Invoice();
    $i->issue();
    print_r($i->history());
    ```

    Output:

    ```
    Array
    (
        [0] => issued at 2026-01-01
    )
    ```

    **Why it works:** traits provide **horizontal** composition — "the application of class
    members without requiring inheritance." `Invoice` gained two private properties and four
    methods without extending anything, which is exactly the single-inheritance limitation
    traits exist to relieve.

    **Certification takeaway:** traits carry **state**, not just behaviour. "Traits are only
    for methods" is false: properties, static properties, and — since PHP 8.2 — constants are
    all legal trait members.

    **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.multiple

## Exercise 3 · Inspect what the compiler actually built

**Objective:** Prove that trait members are *copied into* the class rather than delegated to
at runtime, and learn the introspection API for traits.

**Context:** Same `Invoice`, with one addition: `Loggable::record` is aliased to a protected
`write`.

**Starting point:**

```php
<?php
declare(strict_types=1);

trait Timestampable { public function touch(): void {} }
trait Loggable { public function record(string $l): void {} }

final class Invoice
{
    use Timestampable;
    use Loggable { record as protected write; }
}

$rc = new ReflectionClass(Invoice::class);
```

**Task:** Using `$rc` and `class_uses()`, print: the traits used, the trait aliases, and for
every method its visibility **and its declaring class**. Then evaluate
`(new Invoice()) instanceof Timestampable` and predict the result before running it.

**Expected observation:** Every method — including the ones that came from traits — reports
`Invoice` as its declaring class. And the `instanceof` check is `false` without raising
anything.

??? tip "Show a hint"
    `ReflectionMethod::getDeclaringClass()` is the revealing one. If traits were a runtime
    delegation mechanism, it would have to name the trait. Also check how many methods exist
    after the alias: did `record` survive?

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    trait Timestampable { public function touch(): void {} }
    trait Loggable { public function record(string $l): void {} }

    final class Invoice
    {
        use Timestampable;
        use Loggable { record as protected write; }
    }

    $rc = new ReflectionClass(Invoice::class);

    echo 'class_uses: ', implode(', ', class_uses(Invoice::class)), PHP_EOL;
    echo 'getTraitNames: ', implode(', ', $rc->getTraitNames()), PHP_EOL;
    print_r($rc->getTraitAliases());

    foreach ($rc->getMethods() as $m) {
        $vis = $m->isPublic() ? 'public' : ($m->isProtected() ? 'protected' : 'private');
        echo $m->name, ' — ', $vis, ' — declared in ', $m->getDeclaringClass()->getName(), PHP_EOL;
    }

    echo 'instanceof: ', var_export((new Invoice()) instanceof Timestampable, true), PHP_EOL;
    ```

    Output:

    ```
    class_uses: Timestampable, Loggable
    getTraitNames: Timestampable, Loggable
    Array
    (
        [write] => Loggable::record
    )
    touch — public — declared in Invoice
    write — protected — declared in Invoice
    record — public — declared in Invoice
    instanceof: false
    ```

    Three things to read off this output:

    1. **`getDeclaringClass()` says `Invoice` for every method.** The trait left no runtime
       trace in the method table; the code genuinely lives in `Invoice`.
    2. **`record` is still there, still public.** `as` *added* `write`; it did not rename or
       re-scope the original. The manual: `as` "does not rename the method and it does not
       affect any other method either."
    3. **`instanceof` is `false`, not an error.** A trait is not a type, and asking is not
       illegal — it just always answers no. That silence is what makes it a good distractor.

    **Why it works:** trait composition happens at compile time, when the class is declared.
    `class_uses()` and `ReflectionClass::getTraitNames()` read a record of *how the class was
    built*; they do not describe a live relationship.

    **Certification takeaway:** `class_uses()` reports only the traits named in **that class's
    own** `use` statements — never a parent's, and never a trait's own nested traits. When a
    question shows an inheritance chain and asks what `class_uses()` returns, the answer is
    almost always "less than you expected."

    **Official reference:** https://www.php.net/manual/en/function.class-uses.php

## Exercise 4 · Change one variable: alias versus visibility

**Objective:** Isolate the two distinct jobs the `as` operator performs, by changing exactly
one token.

**Context:** The `Loggable::record()` method should not be part of `Invoice`'s public API.
There are two ways to write that, and they do different things.

**Starting point:**

```php
<?php
declare(strict_types=1);

trait Loggable { public function record(string $l): void {} }

// Variant A
final class InvoiceA
{
    use Loggable { record as protected; }
}

// Variant B
final class InvoiceB
{
    use Loggable { record as protected write; }
}
```

**Task:** For each variant, list the method names that exist on the class and their
visibility. Then answer: which variant actually removes `record()` from the public API?

**Expected observation:** Only one of the two variants hides `record()`. The other leaves it
public and adds a second, protected entry point.

??? tip "Show a hint"
    The alias name in an `as` clause is optional. Ask what PHP can possibly do when there is
    no new name to create — and what it does instead when a name *is* supplied.

??? success "Show the solution"
    **Variant A** — `record as protected;` (no new name) changes the visibility **in place**:

    ```
    record — protected
    ```

    **Variant B** — `record as protected write;` **adds** a protected `write` and leaves the
    original untouched:

    ```
    write  — protected
    record — public
    ```

    So only **Variant A** removes `record()` from the public API. Variant B is the manual's
    `sayHello as private myPrivateHello;` case, annotated there with the comment "sayHello
    visibility not changed".

    **Why it works:** `as` has two independent, optional operands — a visibility modifier and
    a new name. Supply only a modifier and it re-scopes the imported method. Supply a name and
    it creates an additional method, optionally with its own visibility, next to the original.

    **Certification takeaway:** `as` never removes anything. If a question asks how to make a
    trait method *disappear* from a class, the answer involves `insteadof` (which excludes a
    trait's version during composition), and even then only in a conflict. And note the third
    operand available since PHP 8.3: `as final`, which blocks *child* classes from overriding
    while still allowing the exhibiting class to.

    **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.visibility

## Exercise 5 · Diagnose a collision, then resolve it

**Objective:** Trigger the trait fatal error deliberately, read it, and fix it with the two
operators that exist for the job.

**Context:** The team adds a second logging trait. Both traits legitimately define `log()`.

**Starting point:**

```php
<?php
declare(strict_types=1);

trait FileLogger   { public function log(string $m): string { return "file: $m"; } }
trait SyslogLogger { public function log(string $m): string { return "syslog: $m"; } }

final class Mailer
{
    use FileLogger, SyslogLogger;
}
```

**Task:** Run it and read the error carefully — note *which* trait it names as "not applied".
Then fix `Mailer` so that `log()` uses the file implementation and the syslog implementation
remains reachable as `logToSyslog()`. Finally, predict what happens if you add
`public function log(string $m): string { return 'own'; }` to `Mailer` and remove the
resolution block.

**Expected observation:** A fatal error at class-declaration time — no object is ever created.
After the fix, both implementations are callable under different names. The final prediction
is the surprising one.

??? tip "Show a hint"
    `insteadof` answers "which one survives?" and takes the *winner* on the left with the
    excluded trait(s) on the right. `as` answers "how do I still reach the loser?" You need
    both, in that order, and they are two separate statements inside one `{ }` block.

    For the last part, re-read Exercise 1: at what point is a trait method inserted, and what
    stops it?

??? success "Show the solution"
    The error:

    ```
    Fatal error: Trait method SyslogLogger::log has not been applied as Mailer::log,
    because of collision with FileLogger::log
    ```

    The fix:

    ```php
    <?php
    declare(strict_types=1);

    trait FileLogger   { public function log(string $m): string { return "file: $m"; } }
    trait SyslogLogger { public function log(string $m): string { return "syslog: $m"; } }

    final class Mailer
    {
        use FileLogger, SyslogLogger {
            FileLogger::log insteadof SyslogLogger;
            SyslogLogger::log as logToSyslog;
        }
    }

    $m = new Mailer();
    echo $m->log('hi'), PHP_EOL;          // file: hi
    echo $m->logToSyslog('hi'), PHP_EOL;  // syslog: hi
    ```

    And the prediction: adding `Mailer::log()` while **removing** the resolution block
    compiles cleanly and prints `own`. Because the class declares its own `log()`, neither
    trait method is inserted, so the two traits never compete for the slot and there is no
    collision to resolve.

    **Why it works:** "If two Traits insert a method with the same name, a fatal error is
    produced, if the conflict is not explicitly resolved." The operative word is *insert* —
    precedence is applied first, and a method the class supplies itself blocks the insertion
    entirely.

    **Certification takeaway:** two facts, and the second is the trap. (1) An unresolved
    trait-versus-trait collision is a **compile-time fatal**, never a silent first-wins or
    last-wins. (2) That fatal disappears the moment the class defines the method itself — and
    reappears if someone later deletes it. If three traits collide, `insteadof` must name them
    all: `A::m insteadof B, D;`.

    **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.conflict

## Exercise 6 · Handle the edge case: static state across using classes

**Objective:** Determine precisely who owns a trait's static property — including the case
PHP 8.3 changed.

**Context:** A counter trait is used by two unrelated classes, and then by a class and one of
its subclasses.

**Starting point:**

```php
<?php
declare(strict_types=1);

trait InstanceCounter
{
    public static int $created = 0;

    public static function born(): void { ++static::$created; }
}

final class Invoice { use InstanceCounter; }
final class Receipt { use InstanceCounter; }

Invoice::born(); Invoice::born(); Receipt::born();
echo 'Invoice=', Invoice::$created, ' Receipt=', Receipt::$created, PHP_EOL;

class Document { use InstanceCounter; }
class Contract extends Document {}                        // does NOT repeat `use`
class Addendum extends Document { use InstanceCounter; }  // repeats `use`

Document::born();
echo 'Document=', Document::$created,
     ' Contract=', Contract::$created,
     ' Addendum=', Addendum::$created, PHP_EOL;
```

**Task:** Predict all five numbers. Pay particular attention to the difference between
`Contract` and `Addendum` — they differ by exactly one line.

**Expected observation:** Unrelated classes never share. Within a hierarchy, whether a
subclass shares depends on whether it repeats the `use` statement.

??? tip "Show a hint"
    A trait is a template that is stamped into a class. Ask how many stamps were applied in
    this file, and to which classes. `Contract` never had the stamp applied — so where does
    its `$created` come from?

??? success "Show the solution"
    ```
    Invoice=2 Receipt=1
    Document=1 Contract=1 Addendum=0
    ```

    - **`Invoice=2 Receipt=1`** — unrelated classes each received their own copy of the static.
      This has always been true and is the headline rule.
    - **`Contract=1`** — `Contract` never repeats `use InstanceCounter;`, so it has no static
      of its own; `Contract::$created` is simply `Document`'s inherited static, which the
      `Document::born()` call incremented.
    - **`Addendum=0`** — `Addendum` repeats the `use`, so since **PHP 8.3.0** it gets a
      **distinct** static, still at its initial `0`. On PHP 8.2 and earlier this printed `1`,
      because a trait's static property was shared across all classes in the same inheritance
      hierarchy that used it.

    **Why it works:** the manual's caution is exact: "Prior to PHP 8.3.0, static properties
    defined in a trait were shared across all classes in the same inheritance hierarchy which
    used that trait. As of PHP 8.3.0, if a child class uses a trait with a static property, it
    will be considered distinct from the one defined in the parent class."

    **Certification takeaway:** answer this in two steps. First, *unrelated* classes always
    hold independent copies — that is the standard exam question. Second, *within a hierarchy*
    the subclass only gets its own copy if it repeats the `use`, and only since 8.3. A
    question that shows `class B extends A` and a repeated `use` is testing the 8.3 change
    specifically.

    **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php#language.oop5.traits.static

## Exercise 7 · Expert challenge: a Symfony-style helper trait

**Objective:** Combine trait composition, abstract requirements, `as final`, and the magic
constants — and hit the identity trap that Symfony's own documentation warns about.

**Context:** Symfony's `ServiceMethodsSubscriberTrait` documents that service ids are
`ClassName::methodName`, and warns that helper traits must build that id from
`__CLASS__.'::'.__FUNCTION__` rather than `__METHOD__`. You are going to find out why, from
first principles, in a self-contained file.

**Starting point:**

```php
<?php
declare(strict_types=1);

trait ChannelName
{
    abstract protected function channel(): string;

    public function debugIdentity(): array
    {
        return ['__CLASS__' => __CLASS__, '__TRAIT__' => __TRAIT__, '__METHOD__' => __METHOD__];
    }
}

trait Stamps
{
    public function stamp(): string { return 'stamped'; }
}

trait AuditKit
{
    use ChannelName, Stamps;
}
```

**Task:** Four parts.

1. Write `final class InvoiceMailer` using **only** `AuditKit`, and make it compile.
2. Inside the `use` block, mark the stamping method `final` so subclasses cannot override it.
   Try writing `Stamps::stamp as final;` first, and read what happens.
3. Print `debugIdentity()` and explain each of the three values.
4. Print `class_uses($mailer)` and explain the result.

**Expected observation:** Part 2 fails on the obvious spelling. Part 3 produces one value that
contradicts the other two, and that contradiction is the Symfony warning.

??? tip "Show a hint"
    For part 1: `AuditKit` composes `ChannelName`, which declares an **abstract** method. Does
    that requirement stop at `AuditKit`, or does it reach `InvoiceMailer`?

    For part 2: the `insteadof`/`as` operators can only name traits the class itself listed in
    its `use` statement. Which traits did `InvoiceMailer` list?

    For part 3: `__CLASS__` and `__TRAIT__` have documented, different rules inside a trait.
    `__METHOD__` follows one of them — the question is which.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    trait ChannelName
    {
        abstract protected function channel(): string;

        public function debugIdentity(): array
        {
            return ['__CLASS__' => __CLASS__, '__TRAIT__' => __TRAIT__, '__METHOD__' => __METHOD__];
        }
    }

    trait Stamps
    {
        public function stamp(): string { return 'stamped'; }
    }

    trait AuditKit
    {
        use ChannelName, Stamps;
    }

    final class InvoiceMailer
    {
        use AuditKit {
            AuditKit::stamp as final;
        }

        protected function channel(): string { return 'mail'; }
    }

    $mailer = new InvoiceMailer();
    print_r($mailer->debugIdentity());
    echo 'class_uses: ', implode(',', class_uses($mailer)), PHP_EOL;
    ```

    Output:

    ```
    Array
    (
        [__CLASS__] => InvoiceMailer
        [__TRAIT__] => ChannelName
        [__METHOD__] => ChannelName::debugIdentity
    )
    class_uses: AuditKit
    ```

    **Part 1.** The abstract requirement propagates through the composition. Omit
    `channel()` and you get `Fatal error: Class InvoiceMailer contains 1 abstract method and
    must therefore be declared abstract or implement the remaining methods
    (InvoiceMailer::channel)`. Note it is declared `protected` — abstract *private*,
    *protected* and *public* trait methods are all legal since PHP 8.0.0.

    **Part 2.** `Stamps::stamp as final;` fails with:

    ```
    Fatal error: Required Trait Stamps wasn't added to InvoiceMailer
    ```

    The `use` block may only qualify traits the class itself listed, and `InvoiceMailer`
    listed `AuditKit`, not `Stamps`. Both `AuditKit::stamp as final;` and the unqualified
    `stamp as final;` work. Once applied, a subclass redeclaring `stamp()` gets
    `Fatal error: Cannot override final method InvoiceMailer::stamp()` — while
    `InvoiceMailer` itself could still have declared its own, by ordinary precedence.

    **Part 3.** Three different rules in one array:

    - `__CLASS__` → **`InvoiceMailer`**. The manual: "When used inside a trait method,
      `__CLASS__` is the name of the class the trait is used in."
    - `__TRAIT__` → **`ChannelName`**, the trait that literally declared the method — not
      `AuditKit`, which merely re-exported it.
    - `__METHOD__` → **`ChannelName::debugIdentity`**. It reports the *declaring* scope, so
      for a trait method it names the trait.

    That last line is the Symfony warning, reproduced from scratch: a helper trait building a
    service id from `__METHOD__` would register `ChannelName::logger` where the container
    expects `InvoiceMailer::logger`. Composing `__CLASS__.'::'.__FUNCTION__` restores the
    intended id.

    **Part 4.** `class_uses($mailer)` returns only `AuditKit`. It does not flatten the
    composition, exactly as it does not climb to parent classes.

    **Why it works:** every one of these behaviours follows from the same principle — trait
    members are *copied* into the exhibiting class at compile time. `__CLASS__`, `self` and
    `parent` are resolved against the destination; `__TRAIT__` and `__METHOD__` record the
    origin; and `class_uses()` records only the one hop that the class itself wrote down.

    **Certification takeaway:** when a question puts magic constants inside a trait, sort them
    into two buckets. **Destination bucket:** `__CLASS__`, `self::class`, `parent::`,
    `static::class`. **Origin bucket:** `__TRAIT__`, `__METHOD__`. Getting `__METHOD__` into
    the wrong bucket is the mistake Symfony documents in its own service-subscriber guide.

    **Official reference:** https://www.php.net/manual/en/language.constants.magic.php

---

## Where to go next

- Back to the lesson: **[Traits](traits.md)**
- Test yourself: **[Topic exam](traits-exam.md)**

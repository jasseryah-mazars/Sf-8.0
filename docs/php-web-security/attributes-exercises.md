# Guided Exercises — Attributes

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one.
    Commit to an answer before revealing a hint, and to a full attempt before
    revealing the solution — an attribute rule you predicted wrongly and then
    corrected sticks far better than one you read.

    Theory: **[Attributes](attributes.md)** · Then: **[Topic exam](attributes-exam.md)**

    All code targets **PHP 8.4** and runs on the CLI with no framework. `php -l`
    will happily accept every broken example here — that is precisely the point of
    Exercise 1.

## Exercise 1 · Discover that an attribute is genuinely inert

**Objective:** Establish that declaring an attribute executes nothing, and that a
declaration PHP will later reject still compiles and runs.

**Context:** One attribute class restricted to methods, deliberately written on a
class.

**Starting point:**

```php
<?php
declare(strict_types=1);

#[Attribute(Attribute::TARGET_METHOD)]
final class Cacheable
{
    public function __construct(public readonly int $ttl = 60)
    {
        echo "Cacheable constructed\n";
    }
}

#[Cacheable(300)]
final class ProductRepository
{
    public function find(int $id): string
    {
        return "product-$id";
    }
}

echo (new ProductRepository())->find(7), "\n";
```

**Task:** Before running it, predict the complete output. Then predict what
`php -l` reports. Say explicitly whether `Cacheable::__construct()` runs.

**Expected observation:** The only line printed is `product-7`. No constructor
runs, and no error mentions the wrong target.

??? tip "Show a hint"
    Ask what the compiler could possibly have to do with `#[Cacheable(300)]`. Does
    it need to know what `Cacheable` is in order to finish compiling the file? If
    it does not need to know, has it any reason to load the class?

??? success "Show the solution"
    Output:

    ```
    product-7
    ```

    `php -l` also passes. `Cacheable` is never autoloaded, its constructor never
    runs, and the fact that `TARGET_METHOD` forbids using it on a class is never
    noticed — because nothing read the attribute.

    **Why it works:** the compiler stores the attribute on the declaration as a
    class **name** plus a list of unevaluated constant-expression arguments. It
    does not resolve the name, so it cannot consult the flags. For user-land
    attributes the entire validation is deferred to
    `ReflectionAttribute::newInstance()`.

    **Certification takeaway:** "the file compiled" and "the class loaded" prove
    nothing about an attribute. A misplaced user-land attribute is invisible until
    someone reads it — possibly forever.

    **Official reference:** https://www.php.net/manual/en/language.attributes.overview.php

## Exercise 2 · Minimal implementation — read the attribute as data

**Objective:** Use `getAttributes()` and confirm it returns descriptors, not
objects.

**Context:** Same `Cacheable`, now used correctly on a method.

**Starting point:**

```php
<?php
declare(strict_types=1);

#[Attribute(Attribute::TARGET_METHOD)]
final class Cacheable
{
    public function __construct(
        public readonly int $ttl = 60,
        public readonly string $pool = 'default',
    ) {
        echo "  [constructor ran]\n";
    }
}

final class ProductRepository
{
    #[Cacheable(ttl: 300)]
    public function find(int $id): string
    {
        return "product-$id";
    }
}

$attr = (new ReflectionMethod(ProductRepository::class, 'find'))
    ->getAttributes(Cacheable::class)[0];

var_dump($attr->getName());
var_dump($attr->getArguments());
var_dump($attr->getTarget());
var_dump($attr->isRepeated());
```

**Task:** Predict all four dumps *and* whether `[constructor ran]` appears. Pay
special attention to `getArguments()`: what does it contain, given that `$pool` has
a default?

**Expected observation:** No constructor message. `getArguments()` contains only
`['ttl' => 300]` — the default for `$pool` is absent.

??? tip "Show a hint"
    `getArguments()` returns *the arguments that were written*, not the arguments
    the constructor would end up with. Who applies a default value: the reflection
    layer, or the constructor?

??? success "Show the solution"
    ```
    string(9) "Cacheable"
    array(1) { ["ttl"] => int(300) }
    int(4)
    bool(false)
    ```

    `[constructor ran]` never prints. `getTarget()` is `4`, which is
    `Attribute::TARGET_METHOD` — the site where the attribute was written.

    Note the key: `ttl` was passed by **name**, so it lands under a string key. Had
    it been written `#[Cacheable(300)]` the array would be `[0 => 300]`.

    **Why it works:** `getAttributes()` builds `ReflectionAttribute` descriptors
    from the compiled record. `getArguments()` evaluates the stored constant
    expressions and returns them verbatim — positional at integer keys, named at
    string keys. Constructor defaults are applied by the constructor, which has not
    been called.

    **Certification takeaway:** `getArguments()` is not "the attribute's state". It
    is the raw argument list. Only `newInstance()` produces an object with defaults
    filled in.

    **Official reference:** https://www.php.net/manual/en/reflectionattribute.getarguments.php

## Exercise 3 · Inspect the result — enumerate every built-in attribute

**Objective:** Prove for yourself which attribute classes PHP itself ships, and
what flags each declares.

**Context:** `#[Attribute]` is applied to attribute classes — including the
engine's own. That makes them discoverable with the very API you are learning.

**Starting point:**

```php
<?php
declare(strict_types=1);

foreach (get_declared_classes() as $class) {
    $rc = new ReflectionClass($class);

    if (!$rc->isInternal()) {
        continue;
    }

    foreach ($rc->getAttributes(Attribute::class) as $marker) {
        printf("%-24s flags=%d\n", $class, $marker->getArguments()[0] ?? 63);
    }
}
```

**Task:** Run it on PHP 8.4. Predict how many classes appear. Then decode each
`flags` value into `TARGET_*` names using the constants on `Attribute`.

**Expected observation:** Six classes on a stock CLI build:
`Attribute`, `ReturnTypeWillChange`, `AllowDynamicProperties`,
`SensitiveParameter`, `Override`, `Deprecated`.

??? tip "Show a hint"
    The flag values are bits: 1, 2, 4, 8, 16, 32 for the six targets and 64 for
    `IS_REPEATABLE`. `22` is not one number to look up — it is `16 + 4 + 2`.

??? success "Show the solution"
    ```
    Attribute                flags=1
    ReturnTypeWillChange     flags=4
    AllowDynamicProperties   flags=1
    SensitiveParameter       flags=32
    Override                 flags=4
    Deprecated               flags=22
    ```

    Decoded: `Attribute` and `AllowDynamicProperties` are `TARGET_CLASS`;
    `ReturnTypeWillChange` and `Override` are `TARGET_METHOD`;
    `SensitiveParameter` is `TARGET_PARAMETER`; and `Deprecated` is
    `22 = 16 + 4 + 2`, i.e. `TARGET_CLASS_CONSTANT | TARGET_METHOD | TARGET_FUNCTION`.

    Two things to notice. First, `Attribute` is itself `TARGET_CLASS` — which is why
    `#[Attribute]` above a function is an immediate fatal error, not a deferred one.
    Second, none of the six sets bit 64, so **no built-in attribute is repeatable**.

    **Why it works:** an attribute class is marked by carrying `#[Attribute]`, and
    that marker is an ordinary attribute readable through Reflection. The flags are
    simply its first constructor argument.

    **Certification takeaway:** the flag values are additive bits.
    `TARGET_ALL = 63` is the sum of the six targets, and `IS_REPEATABLE = 64` sits
    outside it — so "allowed on everything" never implies "allowed twice".

    **Official reference:** https://www.php.net/manual/en/language.attributes.classes.php

## Exercise 4 · Change one variable — add `IS_REPEATABLE`

**Objective:** See that repetition is accepted by the reader and refused only by
the constructor step.

**Context:** One method carrying the same attribute twice.

**Starting point:**

```php
<?php
declare(strict_types=1);

#[Attribute(Attribute::TARGET_METHOD)]
final class Tag
{
    public function __construct(public readonly string $name) {}
}

final class Service
{
    #[Tag('audit')]
    #[Tag('billing')]
    public function run(): void {}
}

$attrs = (new ReflectionMethod(Service::class, 'run'))->getAttributes();

printf("count=%d repeated=%s\n", count($attrs), var_export($attrs[0]->isRepeated(), true));

foreach ($attrs as $a) {
    try {
        printf("instance: %s\n", $a->newInstance()->name);
    } catch (Error $e) {
        printf("error: %s\n", $e->getMessage());
    }
}
```

**Task:** Predict the output. Then change **only** the flags to
`Attribute::TARGET_METHOD | Attribute::IS_REPEATABLE` and predict again.

**Expected observation:** Before the change, `count=2` and two `Error` messages.
After, `count=2` and two successful instances.

??? tip "Show a hint"
    If PHP rejected the repetition at compile time, could `count($attrs)` ever
    print `2`? Let the count tell you which stage the rejection belongs to.

??? success "Show the solution"
    Before:

    ```
    count=2 repeated=true
    error: Attribute "Tag" must not be repeated
    error: Attribute "Tag" must not be repeated
    ```

    After adding `IS_REPEATABLE`:

    ```
    count=2 repeated=true
    instance: audit
    instance: billing
    ```

    `isRepeated()` returns `true` in **both** runs: it reports that the same
    attribute class occurs more than once on this declaration, not whether that is
    legal.

    **Why it works:** the compiler records both occurrences unconditionally.
    `newInstance()` is where the flags are finally consulted, so it is the only
    step that can refuse. Adding the bit changes nothing about what was recorded —
    only what the validator permits.

    **Certification takeaway:** repeating a non-repeatable attribute is an `Error`
    from `newInstance()`, not a parse error, and `getAttributes()` still returns
    every occurrence. Symfony's `#[Route]` sets `IS_REPEATABLE` for exactly this
    reason: one action, two paths.

    **Official reference:** https://www.php.net/manual/en/language.attributes.classes.php

## Exercise 5 · Diagnose a failure from the message alone

**Objective:** Read a real attribute `Error` and locate the mistake without running
anything.

**Context:** You are handed only this stack trace line from a colleague's CI job.

**Starting point:**

```
PHP Fatal error:  Uncaught Error: Attribute "App\Attribute\Auditable"
cannot target property (allowed targets: parameter) in
/app/src/Kernel.php:88
```

**Task:** State which of the two sides is the declaration and which is the usage,
name the two plausible root causes, and give the minimal fix for each. Then explain
why the trace points at `Kernel.php` rather than at the file where the attribute
was written.

**Expected observation:** The attribute permits only `TARGET_PARAMETER` but was
found on a property; the reported file is the *reader*, not the writer.

??? tip "Show a hint"
    The parenthesised list always comes from the `#[\Attribute(...)]` declaration.
    Now ask which construct in PHP makes one written attribute visible both as a
    parameter and as a property.

??? success "Show the solution"
    The words before the parentheses — `cannot target property` — are where the
    attribute was **used**. The parenthesised `allowed targets: parameter` is what
    the `#[\Attribute(...)]` declaration **permits**.

    Two plausible root causes:

    1. The attribute was genuinely written on a plain property. Fix by adding
       `\Attribute::TARGET_PROPERTY` to the flags, or by moving the attribute.
    2. More subtly, it was written on a **promoted constructor property**. One such
       attribute is visible from `ReflectionParameter` (target `32`) *and* from
       `ReflectionProperty` (target `8`). A consumer scanning properties therefore
       hits it with target `property` and fails, while a consumer scanning
       parameters succeeds. Fix by declaring
       `TARGET_PARAMETER | TARGET_PROPERTY` — which is exactly what Symfony's
       `#[Autowire]` does.

    The trace names `Kernel.php` because the `Error` is thrown at the
    `newInstance()` call site — the reader. The file containing the attribute
    compiled without complaint long before.

    **Certification takeaway:** attribute errors point at the consumer, not at the
    annotated code. Trace them by asking "who called `newInstance()`", then compare
    the used target against the declared flags.

    **Official reference:** https://www.php.net/manual/en/reflectionattribute.newinstance.php

## Exercise 6 · Handle an edge case — inheritance and promoted properties

**Objective:** Establish what Reflection reports for subclasses, inherited methods,
traits and promoted properties.

**Context:** Four situations that people habitually assume behave the same way.

**Starting point:**

```php
<?php
declare(strict_types=1);

#[Attribute(Attribute::TARGET_ALL)]
final class Tag
{
    public function __construct(public readonly string $v = '') {}
}

#[Tag('on parent')]
class ParentC
{
    #[Tag('on parent method')]
    public function m(): void {}
}

class ChildC extends ParentC {}

trait Loggable
{
    #[Tag('on trait method')]
    public function log(): void {}
}

final class Uses
{
    use Loggable;
}

final class Promo
{
    public function __construct(#[Tag('promoted')] public string $id = '') {}
}
```

**Task:** Predict each count before running.
**(a)** `(new ReflectionClass(ChildC::class))->getAttributes()`
**(b)** `(new ReflectionMethod(ChildC::class, 'm'))->getAttributes()`
**(c)** `(new ReflectionMethod(Uses::class, 'log'))->getAttributes()`
**(d)** the counts *and* `getTarget()` values from `ReflectionProperty(Promo::class, 'id')`
and from the corresponding `ReflectionParameter`.

**Expected observation:** (a) 0, (b) 1, (c) 1, (d) 1 on each side, with targets 8
and 32 respectively.

??? tip "Show a hint"
    Ask what the attribute is attached *to*, not what class you are querying. An
    inherited method is one method entry shared by both classes. A subclass, on the
    other hand, is a genuinely different class entry.

??? success "Show the solution"
    ```php
    count((new ReflectionClass(ChildC::class))->getAttributes());        // 0
    count((new ReflectionMethod(ChildC::class, 'm'))->getAttributes());  // 1
    count((new ReflectionMethod(Uses::class, 'log'))->getAttributes());  // 1

    $prop  = new ReflectionProperty(Promo::class, 'id');
    $param = (new ReflectionMethod(Promo::class, '__construct'))->getParameters()[0];

    $prop->getAttributes()[0]->getTarget();   // 8  — TARGET_PROPERTY
    $param->getAttributes()[0]->getTarget();  // 32 — TARGET_PARAMETER
    ```

    **(a)** Class-level attributes are **not** inherited. `ChildC` is its own class
    entry with its own (empty) attribute list. The same is true of a class
    implementing an attributed interface.

    **(b) and (c)** An inherited method and a trait-imported method are the same
    method entry, carrying its own attributes wherever it is reachable from.

    **(d)** A promoted constructor property produces two reflection views of one
    written attribute, each reporting its own target. If `Tag` allowed only
    `TARGET_PARAMETER`, `newInstance()` would succeed from `$param` and throw
    `cannot target property` from `$prop`.

    **Why it works:** attributes are stored on the specific declaration the
    compiler saw. Inheritance copies method entries, not class metadata, and
    promotion creates two declarations from one piece of syntax.

    **Certification takeaway:** "the parent has the attribute, so the child has it"
    is false. Frameworks that need base-type behaviour — Symfony's
    `#[Autoconfigure]` — register an `instanceof` rule in the container instead of
    relying on attribute inheritance.

    **Official reference:** https://www.php.net/manual/en/reflectionclass.getattributes.php

## Exercise 7 · Expert challenge — an attribute hierarchy read like Symfony reads it

**Objective:** Build a miniature version of Symfony's autoconfiguration read: a base
attribute, a subclass, one `IS_INSTANCEOF` query, and proof that `newInstance()` is
not memoised.

**Context:** `AutoconfigureTag` extends `Autoconfigure`, and one
`getAttributes(Autoconfigure::class, IS_INSTANCEOF)` call finds both. Reproduce that
mechanism from scratch.

**Starting point:**

```php
<?php
declare(strict_types=1);

#[Attribute(Attribute::TARGET_CLASS | Attribute::IS_REPEATABLE)]
class Configure
{
    /** @param array<string, mixed> $options */
    public function __construct(public readonly array $options = []) {}
}

#[Attribute(Attribute::TARGET_CLASS | Attribute::IS_REPEATABLE)]
final class ConfigureTag extends Configure
{
    public function __construct(string $name)
    {
        parent::__construct(['tag' => $name]);
    }
}

#[Configure(['public' => true])]
#[ConfigureTag('app.handler')]
final class MailHandler {}
```

**Task:** Write the reader. It must **(1)** collect every `Configure` *or*
`ConfigureTag` on `MailHandler` with a single `getAttributes()` call, **(2)** merge
their `options` into one array, and **(3)** prove that calling `newInstance()`
twice on the same descriptor yields two distinct objects. Then explain why the
exact-match form of the query would be wrong here.

**Expected observation:** Two attributes found, merged options
`['public' => true, 'tag' => 'app.handler']`, and `$a !== $b` for two calls on one
descriptor.

??? tip "Show a hint"
    `$flags` is only honoured when `$name` is supplied. And ask yourself whether a
    `ReflectionAttribute` is a cache or a recipe — if it were a cache, what would
    two calls return?

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    $rc = new ReflectionClass(MailHandler::class);

    $descriptors = $rc->getAttributes(
        Configure::class,
        ReflectionAttribute::IS_INSTANCEOF,
    );

    printf("found %d\n", count($descriptors));

    $options = [];
    foreach ($descriptors as $descriptor) {
        $options = array_merge($options, $descriptor->newInstance()->options);
    }
    print_r($options);

    $a = $descriptors[0]->newInstance();
    $b = $descriptors[0]->newInstance();
    var_dump($a === $b);
    ```

    Output:

    ```
    found 2
    Array ( [public] => 1 [tag] => app.handler )
    bool(false)
    ```

    **Why it works:** `IS_INSTANCEOF` swaps the filter from an exact class-name
    comparison to an `instanceof` check, so a query for the base class also matches
    every subclass. With the default `$flags = 0`, `getAttributes(Configure::class)`
    would return **one** descriptor and silently drop `ConfigureTag` — the bug this
    flag exists to prevent.

    `$a === $b` is `false` because a `ReflectionAttribute` is a recipe, not a cache:
    each `newInstance()` re-runs the constructor. Frameworks cache the outcome
    themselves — Symfony reads these attributes once during container compilation
    and writes the result into the compiled container.

    Beware one detail if you adapt this: `ConfigureTag` is `final` and changes the
    constructor signature. Subclassing an attribute is only safe when the base
    class is not `final` — which is precisely why `Symfony\Component\Routing\Attribute\Route`
    and `Autoconfigure` are non-final while `AsCommand` is final.

    **Certification takeaway:** exact-match filtering plus an attribute hierarchy is
    a silent-failure combination. When subclassing is possible, query the base class
    with `ReflectionAttribute::IS_INSTANCEOF` — and never assume `newInstance()`
    caches.

    **Official reference:** https://www.php.net/manual/en/class.reflectionattribute.php

---

<small>Back to the lesson: [Attributes](attributes.md) · Next: [Topic exam](attributes-exam.md)</small>

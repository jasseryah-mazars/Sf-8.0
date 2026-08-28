# Guided Exercises — Enums

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    an answer before revealing a hint, and to a full attempt before revealing the solution —
    a behaviour you predicted wrongly and then corrected sticks far better than one you read.

    Theory: **[Enums](enums.md)** · Then: **[Topic exam](enums-exam.md)**

    All code targets **PHP 8.4** and **Symfony 8.0**. Save each snippet to a file and run it
    with `php file.php`; several exercises are *supposed* to produce an error, and reading
    that error is the point.

The running example is a small order-management domain: an order has a status, the status is
shown to a human, stored in a database, and accepted from a URL.

## Exercise 1 · Discover what a backed enum adds to a pure one

**Objective:** See, before any theory, exactly which members exist on a pure enum and which
appear only when the enum is backed.

**Context:** Two enums modelling the same idea, one pure and one backed.

**Starting point:**

```php
<?php
declare(strict_types=1);

enum PureStatus
{
    case Draft;
    case Published;
}

enum Status: string
{
    case Draft = 'draft';
    case Published = 'published';
}

var_dump(PureStatus::Draft instanceof UnitEnum);
var_dump(PureStatus::Draft instanceof BackedEnum);
var_dump(Status::Draft instanceof BackedEnum);
var_dump(PureStatus::Draft->name, Status::Draft->name, Status::Draft->value);
```

**Task:** Predict the four `var_dump()` outputs *before* running the file. Then add a fifth
line, `var_dump(PureStatus::Draft->value);`, predict what it does, and run again.

**Expected observation:** The first four lines confirm the interface split. The fifth line
does **not** stop the script.

??? tip "Show a hint"
    Ask yourself what kind of failure reading a property that was never declared normally is
    in PHP. Is a missing property an `Error`, or something quieter? The answer decides whether
    a bug like this shows up in your test suite or in production three weeks later.

??? success "Show the solution"
    The first four dumps print `true`, `false`, `true`, then `"Draft"`, `"Draft"`, `"draft"`.

    The fifth line prints:

    ```
    Warning: Undefined property: PureStatus::$value in ... on line ...
    NULL
    ```

    **Why it works:** the engine applies `UnitEnum` to **every** enum — that is where `name`
    and the static `cases()` come from — and additionally applies `BackedEnum` to an enum
    declared with a backing type, which is where `value`, `from()` and `tryFrom()` come from.
    A pure enum simply has no `value` property, so reading it is an ordinary undefined-property
    read: a warning, and `null`.

    **Certification takeaway:** "pure enums have no `->value`" is not a style rule with a loud
    failure — it is a **silent `null`**. Any code path that reads `->value` on a value that
    might be a pure enum can propagate `null` into a database column or a URL without raising
    anything.

    **Official reference:** https://www.php.net/manual/en/language.enumerations.basics.php

## Exercise 2 · Implement the status enum your domain actually needs

**Objective:** Write a backed enum that carries behaviour, without reaching for properties.

**Context:** Orders need a machine value for storage, a human label for the UI, and a rule:
only `Draft` and `Published` may still be edited.

**Starting point:**

```php
<?php
declare(strict_types=1);

enum Status: string
{
    case Draft = 'draft';
    case Published = 'published';
    case Archived = 'archived';
}
```

**Task:** Add, without adding a single property:

1. a `label(): string` method returning `Draft`, `Published` or `Archived` as a human string;
2. an `isEditable(): bool` method that is `true` only for `Draft` and `Published`;
3. a constant `DEFAULT` that aliases the `Draft` case;
4. a static method `fromLabel(string $label): self` that maps a label back to a case.

Then print the label of every case with a `foreach` over `cases()`.

**Expected observation:** The enum behaves like a small immutable value object, and
`Status::DEFAULT === Status::Draft` is `true`.

??? tip "Show a hint"
    Inside a method, `$this` is the case, so `match ($this) { … }` is the natural body. For the
    static method you need to search the cases: `cases()` returns the list, and each element
    exposes the data you want to match on.

??? success "Show the solution"

    ```php
    <?php
    declare(strict_types=1);

    enum Status: string
    {
        case Draft = 'draft';
        case Published = 'published';
        case Archived = 'archived';

        public const DEFAULT = self::Draft;

        public function label(): string
        {
            return match ($this) {
                self::Draft => 'Draft',
                self::Published => 'Published',
                self::Archived => 'Archived',
            };
        }

        public function isEditable(): bool
        {
            return match ($this) {
                self::Draft, self::Published => true,
                self::Archived => false,
            };
        }

        public static function fromLabel(string $label): self
        {
            foreach (self::cases() as $case) {
                if ($case->label() === $label) {
                    return $case;
                }
            }

            throw new ValueError(
                \sprintf('"%s" is not a valid label for enum Status', $label)
            );
        }
    }

    var_dump(Status::DEFAULT === Status::Draft);

    foreach (Status::cases() as $case) {
        printf("%-10s %-10s %s\n", $case->name, $case->value, $case->label());
    }

    var_dump(Status::fromLabel('Published') === Status::Published);
    ```

    **Why it works:** enums may declare methods, static methods and constants, and a constant
    may refer to a case — that is exactly what `public const DEFAULT = self::Draft;` does. The
    static method is the documented pattern for an "alternative constructor": the engine only
    gives you `from()`/`tryFrom()` for the *backing* value, so any other lookup key is yours to
    write. Throwing `ValueError` mirrors the engine's own convention for `from()`.

    **Certification takeaway:** everything an enum case "knows" comes from `name`, `value`,
    a method, or a constant. If a modelling exercise seems to need a property, the answer is a
    method — or a second enum.

    **Official reference:** https://www.php.net/manual/en/language.enumerations.constants.php

## Exercise 3 · Inspect what a case really is

**Objective:** Observe that a case is an object, that it is a singleton, and how each output
function represents it.

**Context:** The `Status` enum from Exercise 2, without the methods.

**Starting point:**

```php
<?php
declare(strict_types=1);

enum Status: string
{
    case Draft = 'draft';
    case Published = 'published';
}

$a = Status::Draft;
$b = Status::from('draft');

var_dump($a === $b);
var_dump($a == 'draft');
var_dump(Status::cases());
var_dump(array_column(Status::cases(), 'value', 'name'));
echo serialize($a), "\n";
var_dump(unserialize(serialize($a)) === $a);
echo json_encode(['status' => $a]), "\n";
print_r($a);
echo "\n";
var_dump(Status::Draft < Status::Published);
```

**Task:** Run the file and account for **every** line of output. Two of them usually surprise
people: the loose comparison against the backing string, and the relational comparison.

**Expected observation:** Identity holds through `from()` and through a serialize/unserialize
round trip; the loose comparison and the relational comparison are both `false`.

??? tip "Show a hint"
    Two of these outputs are about *what a case is* (an object), not about *what it holds*.
    Ask what `==` and `<` mean when the left operand is an object and the right operand is a
    string, or when both are objects of the same class.

??? success "Show the solution"
    Output, line by line:

    - `bool(true)` — `from()` returns the existing singleton, never a copy.
    - `bool(false)` — an enum case is an object; it never loosely equals its backing scalar.
      Compare `$a->value == 'draft'` if that is what you meant.
    - The `cases()` dump is a **packed array** (`[0]`, `[1]`) of `enum(Status::Draft)` values in
      declaration order.
    - `array_column(..., 'value', 'name')` yields `['Draft' => 'draft', 'Published' => 'published']`
      — the standard trick for building a name→value map.
    - `E:12:"Status:Draft";` — enums have their own serialization code, `E`, storing the *case
      name*, not the object graph.
    - `bool(true)` — deserialization restores the singleton, so identity survives.
    - `{"status":"draft"}` — a backed enum is JSON-encoded as its scalar value only.
    - `print_r` shows `Status Enum:string ( [name] => Draft [value] => draft )`.
    - `bool(false)` — relational comparison is not meaningful on objects, so `<` and `>` are
      always `false` between enum cases.

    **Why it works:** cases are singleton objects of the enum class. Every route back to a case
    — a constant, `from()`, `cases()`, deserialization — returns the *same* instance, which is
    what makes `===` the correct and always-safe comparison.

    **Certification takeaway:** `===` yes, `==` against a scalar no, `<`/`>` never. Sorting a
    list of cases requires sorting on `->value` or on the declaration index from `cases()`.

    **Official reference:** https://www.php.net/manual/en/language.enumerations.serialization.php

## Exercise 4 · Change one variable: drop the backing type

**Objective:** Measure the blast radius of "pure vs backed" by changing exactly one token.

**Context:** The file from Exercise 3, with one edit.

**Starting point:** Take the Exercise 3 file and change the declaration to a pure enum:

```php
enum Status
{
    case Draft;
    case Published;
}
```

**Task:** Before running, list which of the ten output lines will change, and how. Then run it
and compare. Finally, answer: which single Symfony feature does this edit break outright?

**Expected observation:** The file no longer even reaches the later lines — one earlier line
now fails hard, and one of the JSON lines fails differently from how most people predict.

??? tip "Show a hint"
    Two of the operations in that file are declared on `BackedEnum`, not on `UnitEnum`. What
    happens when you call a static method that does not exist on the class? And separately:
    what does the manual say about JSON-encoding an enum that has no scalar?

??? success "Show the solution"
    The first hard failure is `Status::from('draft')`:

    ```
    Fatal error: Uncaught Error: Call to undefined method Status::from()
    ```

    Removing that line to continue, the other changes are:

    - `case Draft = 'draft';` cannot stay — a pure enum case must not have a value
      (`Fatal error: Case Draft of non-backed enum Status must not have a value`), which is why
      the declaration above drops the values too.
    - `array_column(Status::cases(), 'value', 'name')` returns an empty array: there is no
      `value` property to read.
    - `serialize()` still works (`E:12:"Status:Draft";`) — the `E` code stores the **name**, so
      pure enums serialize natively.
    - `json_encode()` now fails: `json_last_error_msg()` reports
      `Non-backed enums have no default serialization`, and `json_encode()` returns `false`
      (or throws `\JsonException` with `JSON_THROW_ON_ERROR`). Implementing `JsonSerializable`
      is the documented way to override that.
    - `print_r` prints `Status Enum ( [name] => Draft )` — no `value` line.

    The Symfony feature this breaks outright is **Doctrine persistence**: `#[ORM\Column(enumType: …)]`
    requires a backed enum, since Doctrine stores the scalar value. Routing is broken too —
    `BackedEnumValueResolver` only handles arguments whose type is a subclass of `BackedEnum`.
    `EnumType` in Forms is the survivor: it builds its choices from `cases()`, which pure enums
    have.

    **Why it works:** the backing type is not decoration. It is what puts the case on the
    `BackedEnum` interface, and every integration that has to move the value across a boundary
    (database column, URL segment, JSON document) depends on that interface.

    **Certification takeaway:** choose backed the moment the value must round-trip through a
    datastore, a URL, JSON or a form; choose pure only for values that never leave the process.

    **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

## Exercise 5 · Diagnose a failure: the enum that refuses to load

**Objective:** Read two load-time enum errors and know which rule each one enforces.

**Context:** A colleague wants each case to carry a badge colour and writes this.

**Starting point:**

```php
<?php
// lint-skip — this file is an intentional fatal-error demo.
declare(strict_types=1);

trait HasBadge
{
    public string $badgeColor = 'grey';

    public function badge(): string
    {
        return $this->badgeColor;
    }
}

enum Status: string
{
    use HasBadge;

    case Draft = 'draft';
    case Published = 'published';
}

var_dump(Status::Draft->badge());
```

**Task:** Predict the error, then run the file. Next, fix it *without* removing the trait, so
that `Status::Draft->badge()` still returns `'grey'` and
`Status::Published->badge()` returns `'green'`. Finally, introduce a second failure on purpose:
give both cases the backing value `'draft'` and read the new error.

**Expected observation:** The first failure names *properties*, not the trait. The second
failure names both conflicting cases.

??? tip "Show a hint"
    The trait is not the problem — one member of it is. Which member could not have been
    written directly inside the enum either? And once you know that, what enum member can
    produce a per-case value without storing anything?

??? success "Show the solution"
    The first run fails at **load time**:

    ```
    Fatal error: Enum Status cannot include properties
    ```

    A trait used by an enum may declare methods, static methods and constants — never
    properties, because that would give a case state. The fix keeps the trait and moves the
    per-case data into a `match`:

    ```php
    <?php
    declare(strict_types=1);

    trait HasBadge
    {
        public function badge(): string
        {
            return match ($this) {
                Status::Published => 'green',
                default => 'grey',
            };
        }
    }

    enum Status: string
    {
        use HasBadge;

        case Draft = 'draft';
        case Published = 'published';
    }

    var_dump(Status::Draft->badge(), Status::Published->badge());
    ```

    Duplicating the backing value gives the second error, raised when the enum is linked:

    ```
    Error: Duplicate value in enum Status for cases Draft and Published
    ```

    **Why it works:** both rules protect the same invariant. No properties keeps each case a
    stateless singleton, so `===` is meaningful. Unique backing values keep `from()` a
    well-defined inverse of `->value` — with duplicates, `from('draft')` would have no single
    right answer.

    **Certification takeaway:** enum violations are **load-time** failures, not runtime ones.
    The message names the rule, not your intent: "cannot include properties" is about the
    property wherever it came from, including a trait; "Duplicate value" names both cases.

    **Official reference:** https://www.php.net/manual/en/language.enumerations.traits.php

## Exercise 6 · Handle the edge case: untrusted input and strict types

**Objective:** Choose between `from()` and `tryFrom()` deliberately, and see how
`declare(strict_types=1)` changes the failure mode of the same call.

**Context:** Two sources feed the same enum: a trusted database column and an untrusted query
string.

**Starting point:**

```php
<?php
declare(strict_types=1);

enum Priority: int
{
    case Low = 1;
    case High = 2;
}

$fromDatabase = 2;          // trusted: the column has a CHECK constraint
$fromQueryString = '2';     // untrusted: everything from a URL is a string

var_dump(Priority::from($fromDatabase));
var_dump(Priority::from($fromQueryString));
```

**Task:** Predict what the second call does under `strict_types=1`. Then delete the
`declare()` line and predict again. Finally, rewrite the untrusted branch so that it never
throws, defaults to `Priority::Low`, and works under `strict_types=1`.

**Expected observation:** The same call is a `TypeError` in one file and a successful lookup in
the other — the *value* never changed, only the typing mode.

??? tip "Show a hint"
    `from()` and `tryFrom()` are ordinary typed methods: `from(int|string $value)`, specialised
    to the enum's own backing type. Strict mode does not coerce arguments. And note that
    `tryFrom()` does not rescue you from a *type* error — it only rescues you from a *value*
    error.

??? success "Show the solution"
    With `declare(strict_types=1)`, the second call throws:

    ```
    TypeError: Priority::from(): Argument #1 ($value) must be of type int, string given
    ```

    Remove the `declare()` line and the same call returns `enum(Priority::High)`: in weak mode
    the numeric string `'2'` is coerced to `2`. (A non-numeric string such as `'abc'` still
    throws a `TypeError` even in weak mode, and a float with a fractional part is coerced with
    a deprecation notice.)

    The safe untrusted branch casts explicitly, then uses `tryFrom()`:

    ```php
    <?php
    declare(strict_types=1);

    enum Priority: int
    {
        case Low = 1;
        case High = 2;
    }

    function priorityFromQuery(?string $raw): Priority
    {
        if (null === $raw || '' === $raw || !ctype_digit($raw)) {
            return Priority::Low;
        }

        return Priority::tryFrom((int) $raw) ?? Priority::Low;
    }

    var_dump(priorityFromQuery('2'));      // Priority::High
    var_dump(priorityFromQuery('99'));     // Priority::Low  (no such case)
    var_dump(priorityFromQuery('abc'));    // Priority::Low  (not even an int)
    var_dump(priorityFromQuery(null));     // Priority::Low  (missing)
    ```

    **Why it works:** `tryFrom()` answers the *value* question ("is there a case for this?")
    and returns `null` when there is not, which `??` turns into a default. It does not answer
    the *type* question — under strict types you must produce an `int` yourself, and the
    `ctype_digit()` guard is what makes that cast honest.

    **Certification takeaway:** `from()` for trusted input where a miss must stop the program;
    `tryFrom()` + `??` for untrusted input. And never write `Priority::from($x) ?? $default` —
    `from()` never returns `null`, so the `??` is dead code hiding an uncaught `\ValueError`.

    **Official reference:** https://www.php.net/manual/en/backedenum.tryfrom.php

## Exercise 7 · Expert challenge: wire the enum through Symfony end to end

**Objective:** Predict the exact HTTP status of four requests against one controller, and
explain which component decides each one.

**Context:** A Symfony 8.0 controller exposing orders by status, restricted to two of the three
cases, plus a form on the same enum.

**Starting point:**

```php
<?php
declare(strict_types=1);

namespace App\Controller;

use App\Enum\Status;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\MapQueryParameter;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Routing\Requirement\EnumRequirement;

final class OrderController extends AbstractController
{
    #[Route('/orders/{status}', name: 'orders_by_status', requirements: [
        'status' => new EnumRequirement([Status::Draft, Status::Published]),
    ])]
    public function byStatus(Status $status): Response
    {
        return new Response($status->value);
    }

    #[Route('/orders', name: 'orders_list')]
    public function list(#[MapQueryParameter] ?Status $status = null): Response
    {
        return new Response($status?->value ?? 'all');
    }
}
```

**Task:** For each request, give the status code **and** name the component that produced it:

1. `GET /orders/draft`
2. `GET /orders/archived` (a real case of `Status`, excluded by the requirement)
3. `GET /orders/bogus`
4. `GET /orders?status=bogus`

Then explain what changes in answer 2 if the requirement is written
`new EnumRequirement(Status::class)` instead, and what the `orders_by_status` route would do if
`Status` were a **pure** enum.

**Expected observation:** Three different components can produce a 404 here, at three different
moments of the request.

??? tip "Show a hint"
    Walk the request in order: the router matches the path against a regular expression, *then*
    the argument resolvers run, *then* your controller executes. `EnumRequirement` contributes
    to the first stage; `BackedEnumValueResolver` and `QueryParameterValueResolver` to the
    second.

??? success "Show the solution"

    1. **200.** The path matches the requirement's regular expression, `BackedEnumValueResolver`
       resolves `Status::from('draft')`, and the controller returns `draft`.
    2. **404 from the router.** `EnumRequirement([Status::Draft, Status::Published])` compiles
       to the pattern `draft|published`, so `/orders/archived` never matches this route. The
       controller is never called and no resolver runs.
    3. **404 from the router as well**, for the same reason — the value fails the requirement
       first. Remove the requirement and it becomes a 404 from
       `BackedEnumValueResolver`, which catches the `\ValueError` from `from()` and throws
       `NotFoundHttpException`. Same status, different origin, and the exception message
       differs.
    4. **404 from `QueryParameterValueResolver`.** It calls `Status::from('bogus')`, catches the
       `\ValueError` into `null`, and then throws an `HttpException` using
       `MapQueryParameter::$validationFailedStatusCode`, whose default is
       `Response::HTTP_NOT_FOUND`. Passing `flags: \FILTER_NULL_ON_FAILURE` would instead leave
       `$status` as `null` and return `all`.

    With `new EnumRequirement(Status::class)`, request 2 becomes a **200**: the requirement then
    lists every case's backing value, so `archived` matches and resolves normally.

    If `Status` were a pure enum, `BackedEnumValueResolver` would skip the argument entirely
    (its first guard is `is_subclass_of($argument->getType(), \BackedEnum::class)`), the
    argument would stay unresolved, and the kernel would fail with "could not be resolved" —
    a 500-class failure, not a 404. `EnumRequirement` would also refuse the class up front,
    since it requires a `BackedEnum`.

    **Why it works:** each layer converts a different kind of "invalid" into 404. The router
    rejects values that do not match the compiled pattern; the value resolvers reject values
    that match the pattern but no case. Understanding *which* layer answered is what lets you
    debug a route that 404s for the wrong reason.

    **Certification takeaway:** a bad backed-enum value is a 404 in routing, in
    `#[MapQueryParameter]`, and in `EnumRequirement` — never an unhandled 500. Restricting the
    accepted subset is a **routing** concern (`EnumRequirement`), not a controller concern.

    **Official reference:** https://symfony.com/doc/8.0/controller/value_resolver.html#built-in-value-resolvers

---

<small>Back to the lesson: [Enums](enums.md) · Next: [Topic exam](enums-exam.md)</small>

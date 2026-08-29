# Guided Exercises — Exception & Error Handling

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    an answer before revealing a hint, and to a full attempt before revealing the solution —
    a `finally` rule you predicted wrongly and then corrected sticks far better than one you
    read.

    Theory: **[Exception & Error Handling](exceptions.md)** · Then:
    **[Topic exam](exceptions-exam.md)**

    All code targets **PHP 8.4**. Every snippet runs as a standalone file with
    `php file.php`; run them, do not just read them, because most of this chapter is about
    *ordering*, and ordering is what you get wrong in your head.

## Exercise 1 · Discover which net catches which fault

**Objective:** See with your own eyes that `catch (\Exception)` is not a universal net.

**Context:** One function, two very different failure modes.

**Starting point:**

```php
<?php
declare(strict_types=1);

function importAmount(string $payload): int
{
    $data = json_decode($payload, true, flags: \JSON_THROW_ON_ERROR);

    return intdiv($data['total'], $data['count']);
}

foreach (['not json', '{"total": 10, "count": 0}'] as $payload) {
    try {
        echo importAmount($payload), "\n";
    } catch (\Exception $e) {
        echo 'caught ', $e::class, "\n";
    }
}
```

**Task:** Before running: predict the output for **each** of the two payloads. Then run the
file and compare.

**Expected observation:** The first payload is caught and reported. The second one is not
caught at all — the script dies with a fatal error.

??? tip "Show a hint"
    Ask what class each failure actually produces, then ask whether that class is an
    `instanceof \Exception`. `get_parent_class()` on the class name settles it in one line.

??? success "Show the solution"
    Output:

    ```
    caught JsonException
    PHP Fatal error: Uncaught DivisionByZeroError: Division by zero
    ```

    `json_decode()` with `JSON_THROW_ON_ERROR` throws a `JsonException`, which extends
    `Exception` — caught. `intdiv($x, 0)` throws a `DivisionByZeroError`, whose ancestry is
    `DivisionByZeroError` → `ArithmeticError` → `Error`. `Error` does **not** extend
    `Exception`; both merely implement `Throwable`.

    Widen the net to see the difference:

    ```php
    } catch (\Throwable $e) {
        echo 'caught ', $e::class, "\n";
    }
    ```

    **Why it works:** `catch` is an ordered `instanceof` test. `DivisionByZeroError
    instanceof \Exception` is `false`, so the block is skipped and the throwable keeps
    unwinding until it leaves the script.

    **Certification takeaway:** `Error` and `Exception` are **siblings** under `Throwable`,
    never parent and child. Only `\Throwable` — or the specific `Error` class — catches an
    engine fault.

    **Official reference:** https://www.php.net/manual/en/language.errors.php7.php

## Exercise 2 · Minimal implementation — a custom exception that carries data

**Objective:** Write a domain exception that a handler can act on without parsing strings.

**Context:** A wallet refuses a debit. The caller needs to know *by how much* it failed.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Wallet
{
    public function __construct(private int $balanceCents) {}

    public function debit(int $amountCents): void
    {
        // TASK: refuse the debit with a meaningful exception
        $this->balanceCents -= $amountCents;
    }
}
```

**Task:** Create an `InsufficientFunds` exception that extends the right SPL class, carries
the shortfall as typed data, and accepts an optional `$previous`. Then throw it from
`debit()` and catch it, printing the shortfall from the object rather than from the message.

**Expected observation:** The handler reads an `int`, not a substring of a sentence.

??? tip "Show a hint"
    Is an overdraft a bug in the calling code, or an unpredictable run-time condition? That
    answer chooses between the `LogicException` family and the `RuntimeException` family.
    And remember the manual's advice about `parent::__construct()`.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    final class InsufficientFunds extends \DomainException
    {
        public function __construct(
            public readonly int $shortfallCents,
            ?\Throwable $previous = null,
        ) {
            parent::__construct("Short by {$shortfallCents} cents", 0, $previous);
        }
    }

    final class Wallet
    {
        public function __construct(private int $balanceCents) {}

        public function debit(int $amountCents): void
        {
            if ($amountCents > $this->balanceCents) {
                throw new InsufficientFunds($amountCents - $this->balanceCents);
            }

            $this->balanceCents -= $amountCents;
        }
    }

    try {
        (new Wallet(500))->debit(1200);
    } catch (InsufficientFunds $e) {
        printf("top up %d cents\n", $e->shortfallCents);
    }
    ```

    **Why it works:** `\DomainException` extends `LogicException` — debiting more than the
    balance violates a domain rule the caller was supposed to respect. Calling
    `parent::__construct()` is what populates `message`, `code` and `previous`; the manual
    recommends it explicitly for any subclass that redefines the constructor. The public
    `readonly` promoted property gives handlers structured data.

    **Certification takeaway:** SPL splits application exceptions into `LogicException`
    (a bug: `Domain`, `InvalidArgument`, `Length`, `OutOfRange`, `BadFunctionCall`) and
    `RuntimeException` (a run-time condition: `OutOfBounds`, `Overflow`, `Range`,
    `Underflow`, `UnexpectedValue`). Picking the right family is a design decision the exam
    tests.

    **Official reference:** https://www.php.net/manual/en/spl.exceptions.php

## Exercise 3 · Inspect the result — walk the `previous` chain

**Objective:** Prove that chaining preserves the root cause, and learn to read the chain.

**Context:** Three layers, each translating the failure into its own vocabulary.

**Starting point:**

```php
<?php
declare(strict_types=1);

function parse(string $raw): array
{
    return json_decode($raw, true, flags: \JSON_THROW_ON_ERROR);
}

function loadConfig(string $raw): array
{
    try {
        return parse($raw);
    } catch (\JsonException $e) {
        throw new \RuntimeException('Config file is not valid JSON', previous: $e);
    }
}

function boot(string $raw): void
{
    try {
        loadConfig($raw);
    } catch (\RuntimeException $e) {
        throw new \LogicException('Application cannot start', previous: $e);
    }
}
```

**Task:** Call `boot('nope')`, catch the outermost throwable, and print the **whole** chain:
class name and message for every link. How many links are there, and which one names the
real cause?

**Expected observation:** Three links. The last one is the `JsonException` that actually
knows what went wrong.

??? tip "Show a hint"
    `getPrevious()` returns `?\Throwable`. A `do`/`while` or a plain `while` assignment loop
    walks it until it returns `null`.

??? success "Show the solution"
    ```php
    try {
        boot('nope');
    } catch (\Throwable $e) {
        $depth = 0;
        do {
            printf("%d: %s — %s\n", $depth++, $e::class, $e->getMessage());
        } while ($e = $e->getPrevious());
    }
    ```

    Output:

    ```
    0: LogicException — Application cannot start
    1: RuntimeException — Config file is not valid JSON
    2: JsonException — Syntax error
    ```

    **Why it works:** every throwable constructor takes `?\Throwable $previous` as its third
    argument, and `getPrevious()` is a `final` accessor on `Exception`, so the chain is
    guaranteed to be readable. Each layer stays honest about its own abstraction while the
    evidence travels intact.

    **Certification takeaway:** rethrowing without `previous:` is not a style problem, it is
    data loss — the only object that knew the file and line of the original failure is
    discarded. Symfony's profiler renders exactly this chain.

    **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.extending

## Exercise 4 · Change one variable — put a `return` inside `finally`

**Objective:** Observe `finally` overriding both a `return` and a pending exception.

**Context:** A cleanup block that quietly changes the meaning of the function.

**Starting point:**

```php
<?php
declare(strict_types=1);

function a(): string
{
    try {
        return 'from try';
    } finally {
        echo "cleanup\n";
    }
}

function b(): string
{
    try {
        return 'from try';
    } finally {
        return 'from finally';
    }
}

function c(): string
{
    try {
        throw new \RuntimeException('boom');
    } finally {
        return 'from finally';
    }
}

echo a(), "\n";
echo b(), "\n";
echo c(), "\n";
```

**Task:** Predict all three results, including whether `c()` throws. Then run it.

**Expected observation:** `a()` prints the cleanup **before** returning `from try`. `b()`
returns `from finally`. `c()` does **not** throw at all — it returns `from finally`.

??? tip "Show a hint"
    The manual says the `try` block's `return` is *evaluated* where it is written, but the
    value is only handed back after `finally` has run. Now ask: what happens if `finally`
    produces its own result in the meantime?

??? success "Show the solution"
    ```
    cleanup
    from try
    from finally
    from finally
    ```

    **Why it works:** the manual states two rules. First, a `return` inside `try` or `catch`
    is evaluated immediately but returned only after `finally` completes — which is why
    `a()` prints `cleanup` first and still returns `from try`. Second, if `finally` itself
    contains a `return`, **its** value is the one returned. In `c()` that second rule
    outranks the pending exception: the `RuntimeException` is discarded and the caller never
    learns the function failed.

    **Certification takeaway:** `finally` always runs, and a `return` there wins over a
    `return` **and** over a `throw` from `try`. That is why "no `return` inside `finally`" is
    a hard rule rather than a preference — it silently converts failures into successes.

    **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.finally

## Exercise 5 · Diagnose a failure — a class that refuses to be throwable

**Objective:** Read an unfamiliar fatal error and name the rule it enforces.

**Context:** Someone wanted a throwable that is not an `Exception` and not an `Error`, so
they implemented the interface directly and supplied every method.

**Starting point:**

```
PHP Fatal error: Class ApiFailure cannot implement interface Throwable,
extend Exception or Error instead in /app/src/ApiFailure.php on line 5
```

```php
final class ApiFailure implements \Throwable
{
    public function getMessage(): string { return 'api failed'; }
    // …every other Throwable method implemented correctly…
}
```

**Task:** Explain why implementing every method is not enough, give the minimal fix, and
then explain why `Symfony\Component\HttpKernel\Exception\HttpExceptionInterface` is allowed
to declare `extends \Throwable`.

**Expected observation:** The fatal is raised at class-declaration time, regardless of how
complete the implementation is.

??? tip "Show a hint"
    The restriction is on **classes**, and the error message names the two permitted base
    classes. Is `HttpExceptionInterface` a class?

??? success "Show the solution"
    The minimal fix is to extend one of the two roots:

    ```php
    <?php
    declare(strict_types=1);

    final class ApiFailure extends \RuntimeException
    {
    }
    ```

    **Why it works:** the manual is explicit — *PHP classes cannot implement the `Throwable`
    interface directly, and must instead extend `Exception`*. Every throwable needs internal
    engine state (the captured trace, the file and line, the `previous` slot) that only the
    built-in base classes provide, so a userland class that merely reproduces the method
    signatures could never behave correctly. The engine therefore rejects it while the class
    is being declared, before any instance exists.

    The restriction applies to `implements` on a **class**. An **interface** may freely
    `extends \Throwable`, which is precisely what Symfony does:

    ```php
    interface HttpExceptionInterface extends \Throwable
    {
        public function getStatusCode(): int;
        public function getHeaders(): array;
    }
    ```

    Concrete classes then satisfy it by extending a real throwable *and* implementing the
    interface — `class HttpException extends \RuntimeException implements
    HttpExceptionInterface`.

    **Certification takeaway:** "a class may implement `Throwable` if it implements all its
    methods" is false. "An interface may extend `Throwable`" is true, and it is the
    mechanism behind every framework-specific throwable contract.

    **Official reference:** https://www.php.net/manual/en/class.throwable.php

## Exercise 6 · Handle an edge case — when `try` and `finally` both throw

**Objective:** Predict which exception survives, and where the other one goes.

**Context:** Cleanup code is not exempt from failing.

**Starting point:**

```php
<?php
declare(strict_types=1);

try {
    try {
        throw new \Exception(message: 'Third', previous: new \Exception('Fourth'));
    } finally {
        throw new \Exception(message: 'First', previous: new \Exception('Second'));
    }
} catch (\Exception $e) {
    // TASK: print the whole chain here
}
```

**Task:** Predict which message the outer `catch` sees, then predict the **full** four-link
chain in order. Write the loop and verify.

**Expected observation:** The `finally` exception wins, and the `try` exception is appended
to the end of its chain.

??? tip "Show a hint"
    Two independent chains exist before the collision: `First → Second` and
    `Third → Fourth`. The engine has to join them somewhere. Which end of which chain is
    free?

??? success "Show the solution"
    ```php
    } catch (\Exception $e) {
        do {
            echo $e->getMessage(), "\n";
        } while ($e = $e->getPrevious());
    }
    ```

    Output:

    ```
    First
    Second
    Third
    Fourth
    ```

    **Why it works:** the manual states the rule directly — if both the `try` block and the
    `finally` block throw, the exception thrown from `finally` is the one that propagates,
    and the exception from `try` is used as its **previous**. The engine appends it at the
    *tail* of the `finally` chain, so `Second` (already `First`'s previous) keeps its place
    and `Third` — with its own `Fourth` still attached — is grafted after it.

    The practical consequence: an exception thrown from cleanup **masks** the original
    failure in the message you see first, but does not destroy it. Always read the chain.

    **Certification takeaway:** `finally` wins on both mechanisms — a `return` there
    overrides `try`'s outcome, and a `throw` there overrides `try`'s exception while
    demoting it to `previous`.

    **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.finally

## Exercise 7 · Expert challenge — build a three-layer failure boundary

**Objective:** Cover the three disjoint failure populations with the three correct hooks,
and prove each hook's blind spot.

**Context:** A long-running CLI worker must never die silently. Three mechanisms exist and
none of them overlaps: `set_error_handler()` for legacy diagnostics,
`set_exception_handler()` for uncaught throwables, `register_shutdown_function()` +
`error_get_last()` for fatals.

**Starting point:**

```php
<?php
declare(strict_types=1);

// TASK: install the three hooks here, then trigger each population in turn.

trigger_error('legacy warning', \E_USER_WARNING);   // population 1
throw new \RuntimeException('nobody catches me');   // population 2
// population 3: a real E_ERROR, e.g. exhausting the memory limit
```

**Task:** Install all three hooks. Convert diagnostics to `\ErrorException` so they become
catchable, log uncaught throwables, and inspect the fatal post-mortem. Then answer three
questions: does `error_reporting(0)` disable your error handler? does `@` bypass it? and
which error levels can `set_error_handler()` never receive?

**Expected observation:** Each hook fires for exactly one population, and none of them
covers another's.

??? tip "Show a hint"
    Read the return value of `set_error_handler()` and the meaning of its second parameter.
    Then recall that the manual lists, by name, the levels a user handler cannot receive —
    they are all the compile-time and core levels.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    // 1. Legacy diagnostics -> throwables, so try/catch works uniformly.
    set_error_handler(static function (int $level, string $msg, string $file, int $line): bool {
        throw new \ErrorException($msg, 0, $level, $file, $line);
    });

    // 2. Last resort for anything that escaped every catch.
    set_exception_handler(static function (\Throwable $e): void {
        error_log(\sprintf('uncaught %s: %s', $e::class, $e->getMessage()));
    });

    // 3. Post-mortem for fatals no handler can intercept.
    register_shutdown_function(static function (): void {
        $err = error_get_last();
        if (null !== $err && 0 !== ($err['type'] & (\E_ERROR | \E_PARSE | \E_CORE_ERROR | \E_COMPILE_ERROR))) {
            error_log(\sprintf('fatal: %s in %s:%d', $err['message'], $err['file'], $err['line']));
        }
    });

    try {
        trigger_error('legacy warning', \E_USER_WARNING);
    } catch (\ErrorException $e) {
        printf("converted, severity=%d\n", $e->getSeverity());   // 512 = E_USER_WARNING
    }
    ```

    **Why it works:** each hook covers one population and only one.

    - `set_error_handler(?callable $callback, int $error_levels = E_ALL): ?callable`
      receives traditional diagnostics. Throwing `\ErrorException` from it is the manual's
      own documented technique, and `getSeverity()` preserves the original `E_*` level.
    - `set_exception_handler()` is called *in place of* a `catch` block when a throwable
      reaches global scope. It runs once, and the script terminates afterwards.
    - Shutdown functions plus `error_get_last()` are the only way to observe a fatal.
      Nothing can resume execution at that point.

    The three answers:

    - **`error_reporting(0)` does not disable your handler.** The manual states that
      `error_reporting` settings have no effect on whether the callback is invoked — only
      the `$error_levels` mask filters it. Your handler can still *read*
      `error_reporting()` and choose to return `false`.
    - **`@` does not bypass it either.** A registered handler is still called for a
      suppressed diagnostic; only the built-in display is suppressed. Since PHP 8.0.0, `@`
      no longer hides the critical errors that terminate the script.
    - **Levels a user handler can never receive:** `E_ERROR`, `E_PARSE`, `E_CORE_ERROR`,
      `E_CORE_WARNING`, `E_COMPILE_ERROR` and `E_COMPILE_WARNING`, independent of where they
      were raised. That is exactly why layer 3 exists.

    Symfony packages all three in one place:
    `Symfony\Component\ErrorHandler\ErrorHandler::register()` installs an error handler, an
    exception handler and a shutdown function, converts thrown levels into
    `\ErrorException`, and logs uncaught throwables as `E_ERROR`.

    **Certification takeaway:** three populations, three hooks, zero overlap. Any answer
    claiming one mechanism covers another's territory is wrong — and "`set_error_handler`
    handles uncaught exceptions" is the most frequent version of that wrong answer.

    **Official reference:** https://www.php.net/manual/en/function.set-error-handler.php

---

<small>Back to the lesson: [Exception & Error Handling](exceptions.md) · Next: [Topic exam](exceptions-exam.md)</small>

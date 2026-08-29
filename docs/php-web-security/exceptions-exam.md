# Topic Exam — Exception & Error Handling

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because the exam is built on
    near-misses rather than definitions.

    Theory: **[Exception & Error Handling](exceptions.md)** ·
    Practice: **[Guided exercises](exceptions-exercises.md)** ·
    Recall: **[Flashcards](exceptions-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4** and **Symfony 8.0**.

## The Throwable hierarchy

??? question "Question 1"
    Which single `catch` clause catches **both** a `TypeError` and a `RuntimeException`?

    - A. `catch (\Exception $e)`
    - B. `catch (\Throwable $e)`
    - C. `catch (\Error $e)`
    - D. `catch (\LogicException $e)`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `Throwable` is the interface both branches implement, so it is the
        only type that matches objects from each of them.

        **A** catches the `RuntimeException` but not the `TypeError`: `TypeError` extends
        `Error`, and `Error` does not extend `Exception`. **C** is the mirror image — it
        catches the `TypeError` and misses the `RuntimeException`. **D** catches neither:
        `LogicException` and `RuntimeException` are *sibling* subclasses of `Exception`, so a
        `RuntimeException` is not a `LogicException`.

        **Official reference:** https://www.php.net/manual/en/class.throwable.php

??? question "Question 2 · Internals"
    Which inheritance chain is correct?

    - A. `DivisionByZeroError` → `ArithmeticError` → `Error` → implements `Throwable`
    - B. `DivisionByZeroError` → `RuntimeException` → `Exception` → implements `Throwable`
    - C. `TypeError` → `Exception` → implements `Throwable`
    - D. `ValueError` → `LogicException` → implements `Throwable`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual's `Error` hierarchy lists `ArithmeticError` under `Error`
        and `DivisionByZeroError` under `ArithmeticError`. `Error` implements `Throwable`; it
        does not extend anything else.

        **B** routes an engine fault through the application branch — `DivisionByZeroError`
        has nothing to do with `RuntimeException`. **C** makes the classic mistake of
        assuming `Exception` is the universal root; `TypeError` extends `Error`. **D** is
        wrong twice: `ValueError` extends `Error` directly, and `LogicException` lives on the
        `Exception` arm.

        Two placements inside the `Error` arm are worth memorising because they are one level
        deeper than people expect: `ArgumentCountError` extends **`TypeError`**, and
        `ParseError` extends **`CompileError`**.

        **Official reference:** https://www.php.net/manual/en/language.errors.php7.php

??? question "Question 3 · Multiple choice"
    Which of the following are subclasses of `Error` rather than of `Exception`? (select all
    that apply)

    - A. `TypeError`
    - B. `ValueError`
    - C. `RuntimeException`
    - D. `ErrorException`
    - E. `UnhandledMatchError`

    ??? success "Show answer"
        **Correct answers:** A, B and E

        **Explanation:**
        **A** — `TypeError` is raised by the engine when an argument, return value or
        property receives the wrong type.
        **B** — `ValueError` is raised when the type is correct but the value is impossible,
        such as a chunk size of `0`.
        **E** — `UnhandledMatchError` is raised when a `match` expression has no matching arm
        and no `default`. The manual lists all three directly under `Error`.

        **C** is a distractor by name only: `RuntimeException` extends `Exception`, and its
        SPL children (`OutOfBounds`, `Overflow`, `Range`, `Underflow`, `UnexpectedValue`) do
        too. **D** is the sharpest trap on the page: despite the word *Error*,
        `ErrorException` extends **`Exception`**. It exists to wrap a legacy diagnostic
        inside the exception branch, and `getSeverity()` returns the original `E_*` level.

        **Official reference:** https://www.php.net/manual/en/reserved.exceptions.php

??? question "Question 4 · True or false"
    A class may implement `\Throwable` directly, provided it implements every method the
    interface declares.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — false

        **Explanation:** the manual states it explicitly: *PHP classes cannot implement the
        `Throwable` interface directly, and must instead extend `Exception`*. Declaring
        `class ApiFailure implements \Throwable` fails while the class is being declared,
        with `Class ApiFailure cannot implement interface Throwable, extend Exception or
        Error instead`. Supplying all eight methods changes nothing — every throwable needs
        engine-managed internal state (the captured trace, file, line and `previous` slot)
        that only the built-in base classes carry.

        **A** is the intuitive-but-wrong answer, and the reasoning "an interface is just a
        set of signatures" is exactly what the question is testing. The rule applies to
        **classes** only: an **interface** may freely `extends \Throwable`, which is what
        `Symfony\Component\HttpKernel\Exception\HttpExceptionInterface` does.

        **Official reference:** https://www.php.net/manual/en/class.throwable.php

??? question "Question 5 · Edge case"
    `OutOfRangeException` and `OutOfBoundsException` differ in which way?

    - A. They are aliases of each other
    - B. `OutOfRangeException` extends `LogicException`, `OutOfBoundsException` extends `RuntimeException`
    - C. `OutOfRangeException` extends `Error`, `OutOfBoundsException` extends `Exception`
    - D. Both extend `RuntimeException`, but only one is in SPL

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the SPL exception tree splits the two deliberately.
        `OutOfRangeException` sits under `LogicException` — it signals an index the
        programmer should have known was invalid, detectable by reading the code.
        `OutOfBoundsException` sits under `RuntimeException` — it signals a key that turned
        out not to exist at run time.

        **A** is wrong: they are distinct classes in different families, and catching one
        never catches the other. **C** puts an SPL class on the `Error` arm; every SPL
        exception is on the `Exception` arm. **D** invents a distinction — both are SPL
        classes, and only one of them is a `RuntimeException`.

        **Official reference:** https://www.php.net/manual/en/spl.exceptions.php

## try / catch / finally

??? question "Question 6"
    A `return` statement inside a `finally` block…

    - A. Overrides any `return` or pending `throw` from the `try` block
    - B. Is a syntax error
    - C. Is ignored when `try` already returned
    - D. Runs before the `try` block

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual describes both halves of the rule. A `return` inside
        `try` or `catch` is *evaluated* where it is written, but its value is handed back
        only after `finally` has run — and if `finally` also contains a `return`, the value
        from `finally` is the one returned. The same precedence applies to a pending
        exception: a `return` in `finally` discards it, so the caller sees a normal return
        for a call that actually failed.

        **B** is wrong — it is perfectly valid syntax, which is exactly why it is dangerous.
        **C** inverts the precedence: `finally` wins, not `try`. **D** contradicts the name
        and the semantics; `finally` runs after `try` and after any `catch`.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.finally

??? question "Question 7 · Execution order"
    What does this script print?

    ```php
    try {
        try {
            throw new \Exception(message: 'Third', previous: new \Exception('Fourth'));
        } finally {
            throw new \Exception(message: 'First', previous: new \Exception('Second'));
        }
    } catch (\Exception $e) {
        do { echo $e->getMessage(), ' '; } while ($e = $e->getPrevious());
    }
    ```

    - A. `Third Fourth`
    - B. `First Second`
    - C. `First Second Third Fourth`
    - D. `Third Fourth First Second`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** the manual gives this exact case. When the `try` block and the
        `finally` block both throw, the exception thrown from **`finally`** is the one that
        propagates, and the exception from `try` is used as its **previous**. The engine
        appends it at the tail of the existing chain, so `First → Second` keeps its shape and
        `Third → Fourth` is grafted after `Second`.

        **A** assumes the `try` exception wins — it does not, it is demoted. **B** assumes
        the `try` exception is destroyed rather than chained; it is preserved, which is the
        whole point of the rule. **D** reverses the precedence, putting the demoted chain
        first.

        The practical lesson: an exception thrown from cleanup **masks** the original failure
        in the first message you read, so always walk `getPrevious()` to the end.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.finally

??? question "Question 8 · Code analysis"
    What happens when this runs?

    ```php
    try {
        intdiv(1, 0);
    } catch (\Exception $e) {
        echo 'caught';
    }
    ```

    - A. It prints `caught`
    - B. The `DivisionByZeroError` is uncaught and the script terminates with a fatal error
    - C. It returns `0` silently
    - D. It emits a warning and execution continues

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `intdiv()` throws a `DivisionByZeroError` when the divisor is `0`.
        Its ancestry is `DivisionByZeroError` → `ArithmeticError` → `Error`, and `Error` is
        not an `Exception`, so the `catch` clause never matches. With no other handler the
        throwable reaches global scope and PHP emits
        `Fatal error: Uncaught DivisionByZeroError: Division by zero`.

        **A** assumes `\Exception` is the universal root. **C** describes pre-PHP-8
        behaviour of the `/` and `%` operators, which returned `false` with a warning; modern
        PHP throws for `1/0`, `1%0` and `intdiv(1, 0)` alike. **D** is the same outdated
        model. The fix is `catch (\DivisionByZeroError $e)` or `catch (\Throwable $e)`.

        **Official reference:** https://www.php.net/manual/en/language.errors.php7.php

??? question "Question 9 · Code analysis"
    Which block runs, and does PHP complain about the ordering?

    ```php
    try {
        throw new \LogicException('x');
    } catch (\Throwable $e) {
        echo 'A';
    } catch (\LogicException $e) {
        echo 'B';
    }
    ```

    - A. `B` — PHP picks the most specific matching type
    - B. Nothing — PHP raises a compile error for the unreachable block
    - C. `A` — the first matching block wins, and the second is unreachable but not an error
    - D. `AB` — every matching block runs in order

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** the manual is explicit that *the first `catch` block a thrown
        exception encounters that matches the type of the thrown object will handle the
        object*. `LogicException` is an `instanceof \Throwable`, so the first block matches
        and prints `A`. The second block is dead code, and PHP raises nothing at all for it.

        **A** describes overload resolution in other languages; PHP does no specificity
        ranking, only source order. **B** invents a diagnostic — this is precisely why the
        bug is hard to spot, since nothing warns you. **D** would make `catch` behave like a
        list of observers; only one block ever runs.

        The rule to carry: order `catch` blocks from **specific to general**, always.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php

??? question "Question 10 · Multiple choice"
    Which of these statements about `catch` and `throw` syntax are true in PHP 8.4? (select
    all that apply)

    - A. `catch (\TypeError | \ValueError $e)` has been valid since PHP 7.1.0
    - B. `catch (\RuntimeException)` without a variable has been valid since PHP 8.0.0
    - C. `throw` may be used as an expression, since PHP 8.0.0
    - D. A `try` block with neither `catch` nor `finally` is valid

    ??? success "Show answer"
        **Correct answers:** A, B and C

        **Explanation:**
        **A** — multi-catch with the pipe character arrived in **7.1.0**, for handling
        exceptions from unrelated hierarchies in one block.
        **B** — omitting the caught variable arrived in **8.0.0**; the block still executes,
        it simply has no access to the object.
        **C** — `throw` became an expression in **8.0.0**, which is what allows
        `$x ?? throw new \InvalidArgumentException()` and `default => throw ...` inside a
        `match`.

        **D** is the false one: the manual states that each `try` must have at least one
        corresponding `catch` **or** `finally` block. `try` alone is a syntax error, while
        `try` + `finally` with no `catch` is a perfectly normal cleanup shape.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php

??? question "Question 11 · Scenario"
    You catch a `JsonException` and rethrow with
    `throw new \RuntimeException('Bad payload', previous: $e);`. Why pass `previous`?

    - A. To preserve the root cause and its file, line and trace, retrievable via `getPrevious()`
    - B. It is required syntax when rethrowing
    - C. It suppresses the original exception so it is not logged twice
    - D. It merges the two messages into one string automatically

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the third constructor parameter of every throwable is
        `?\Throwable $previous`. Chaining lets each layer speak its own vocabulary while the
        original evidence travels intact, readable with the `final` accessor
        `getPrevious()`. Symfony's profiler renders that chain, and `FlattenException`
        walks it when building an error page.

        **B** is wrong — chaining is entirely optional, which is why forgetting it is so
        common. **C** inverts the meaning: `previous` *retains* the original rather than
        suppressing it. **D** invents behaviour: `getMessage()` still returns only the
        message you passed, and nothing concatenates the two.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.extending

??? question "Question 12 · Expert trap"
    What does `intdiv(\PHP_INT_MIN, -1)` throw?

    - A. `DivisionByZeroError`
    - B. `ArithmeticError`
    - C. `ValueError`
    - D. Nothing — it returns `\PHP_INT_MIN`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the mathematical result is `|PHP_INT_MIN|`, which is one greater
        than `PHP_INT_MAX` and therefore not representable as an `int`. The manual documents
        this case separately from division by zero: `intdiv()` throws an `ArithmeticError`
        with the message `Division of PHP_INT_MIN by -1 is not an integer`.

        **A** is the trap: a handler written as `catch (\DivisionByZeroError $e)` around
        `intdiv()` looks complete and silently misses this case, because
        `DivisionByZeroError` is a *child* of `ArithmeticError`, not the other way round.
        **C** confuses the branches — the arguments are valid `int` values, so no `ValueError`
        applies. **D** assumes silent overflow; `intdiv()` refuses rather than lying.

        Catch `\ArithmeticError` to cover both failure modes of `intdiv()` at once.

        **Official reference:** https://www.php.net/manual/en/function.intdiv.php

## Errors, handlers and levels

??? question "Question 13"
    What can `set_error_handler()` intercept?

    - A. Traditional diagnostics: warnings, notices, deprecations and `trigger_error()` calls
    - B. Uncaught exceptions
    - C. Fatal `E_ERROR` conditions
    - D. Parse errors

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `set_error_handler()` replaces the standard handler for the
        traditional error-reporting mechanism, which is what most internal functions still
        use. Its signature is
        `set_error_handler(?callable $callback, int $error_levels = E_ALL): ?callable`, and
        it returns the previously active handler.

        **B** belongs to `set_exception_handler()`, a completely separate mechanism for
        throwables that reached global scope uncaught. **C** and **D** name two of the levels
        the manual states cannot be handled by a user-defined function at all: `E_ERROR`,
        `E_PARSE`, `E_CORE_ERROR`, `E_CORE_WARNING`, `E_COMPILE_ERROR` and
        `E_COMPILE_WARNING`. Those need `register_shutdown_function()` plus
        `error_get_last()` for post-mortem inspection.

        **Official reference:** https://www.php.net/manual/en/function.set-error-handler.php

??? question "Question 14 · Debugging"
    A custom error handler is registered. A developer then writes
    `$v = @$data['missing'];` and separately sets `error_reporting(0)`. Which statement
    describes what actually happens?

    - A. Neither `@` nor `error_reporting(0)` prevents the custom handler from being called
    - B. `@` prevents the handler from being called, but `error_reporting(0)` does not
    - C. `error_reporting(0)` prevents the handler from being called, but `@` does not
    - D. Both prevent the handler from being called

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** two separate manual statements combine here. On the `@` operator:
        *if a custom error handler function is set with `set_error_handler()`, it will still
        be called even though the diagnostic has been suppressed*. On `set_error_handler()`:
        *`error_reporting()` settings will have no effect and the error handler will be
        called regardless* — only the `$error_levels` mask passed as the second argument
        filters it.

        **B**, **C** and **D** each grant one or both of these a gating power they do not
        have. `@` only suppresses the built-in *display*; `error_reporting()` only controls
        what the *standard* handler reports. Your handler can read `error_reporting()` and
        return `false` to let the standard handler take over, but that is a choice you make
        inside the callback, not something the engine does for you.

        Also worth knowing: since PHP 8.0.0, `@` no longer silences the critical errors that
        terminate the script, and it never had any effect on a thrown exception.

        **Official reference:** https://www.php.net/manual/en/language.operators.errorcontrol.php

??? question "Question 15"
    Under `declare(strict_types=1)`, passing a `string` to a parameter declared `int`
    throws…

    - A. `TypeError`, which is a subclass of `Error`
    - B. `InvalidArgumentException`
    - C. Only an `E_WARNING`
    - D. `ValueError`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** strict typing disables scalar coercion at the call site, so a
        mismatched argument type is rejected with a `TypeError`. `TypeError` extends `Error`,
        which means the failure lands on the engine branch of the hierarchy.

        **B** is an SPL `LogicException` that *you* throw deliberately; the engine never
        raises it. **C** describes PHP 5 behaviour for many type problems — modern PHP throws
        instead. **D** confuses the two engine types: `ValueError` is raised when the type is
        correct but the value is impossible, such as a negative length.

        The examinable consequence: an upstream `catch (\Exception $e)` will **not** catch
        this. Use `\Throwable` at the boundary, or better, fix the call.

        **Official reference:** https://www.php.net/manual/en/language.types.declarations.php

## Symfony integration

??? question "Question 16 · Scenario"
    A Symfony 8 controller lets a plain `\RuntimeException` escape, and no listener on
    `kernel.exception` sets a response. What HTTP status code does the client receive?

    - A. 400
    - B. 404
    - C. 500
    - D. 200, with the exception rendered in the body

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** Symfony decides the status code with a short cascade. If a listener
        sets a `Response` whose status is a client error, server error or redirect, that
        status is used. Otherwise, if the throwable is an instance of
        `HttpExceptionInterface`, `getStatusCode()` supplies the status and `getHeaders()`
        supplies extra headers. If neither applies — exactly this case — the status is
        **500**.

        **A** would require the exception to implement `RequestExceptionInterface`, which
        `FlattenException` maps to 400. **B** would require a `NotFoundHttpException`, which
        *does* implement `HttpExceptionInterface`. **D** is never the behaviour: an uncaught
        throwable is an error condition, and in production Symfony renders a generic error
        page rather than exception details.

        To get a specific code from your own exception without extending Symfony's classes,
        add `#[WithHttpStatus(422)]` to the exception class or configure
        `framework.exceptions`.

        **Official reference:** https://symfony.com/doc/8.0/reference/events.html#kernel-exception

??? question "Question 17 · Configuration consequence"
    Given this configuration, what happens to a thrown `\RuntimeException`?

    ```yaml
    framework:
        exceptions:
            Exception:
                log_level: 'debug'
                status_code: 404
            RuntimeException:
                log_level: 'debug'
                status_code: 422
    ```

    - A. It gets status 422, because `RuntimeException` is the more specific entry
    - B. It gets status 404, because the first entry matching `instanceof` wins
    - C. It gets status 500, because two entries conflict
    - D. The container fails to compile because the entries overlap

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the documentation states that the order in which exceptions are
        configured is important, because Symfony uses the configuration of the **first**
        exception that matches `instanceof`. `ErrorListener` iterates the mapping and breaks
        on the first match. Since `\RuntimeException` *is* an `\Exception`, the `Exception`
        entry matches first and the `RuntimeException` entry is never reached — it is dead
        configuration.

        **A** applies specificity ranking that Symfony does not perform, mirroring the same
        mistake as ordering `catch` blocks general-to-specific. **C** invents a conflict
        resolution step. **D** invents a compile-time validation that does not exist — the
        configuration is accepted and simply behaves in a way the author did not intend.

        The fix is to list the most specific classes first, exactly as with `catch` blocks.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#exceptions

---

<small>Back to the lesson: [Exception & Error Handling](exceptions.md) · [Guided exercises](exceptions-exercises.md) · [Review flashcards](exceptions-flashcards.md)</small>

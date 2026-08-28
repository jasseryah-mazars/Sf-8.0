# Flashcards — Exception & Error Handling

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Exception & Error Handling](exceptions.md)** ·
    Practice: **[Guided exercises](exceptions-exercises.md)** ·
    Test: **[Topic exam](exceptions-exam.md)**

## Definitions and roles

??? question "What is `Throwable`, and what is its relationship to `Error` and `Exception`?"
    Think before revealing the answer.

    ??? success "Show answer"
        `Throwable` is the **interface** every throwable object implements. `Error` and
        `Exception` are two independent classes that implement it — **siblings**, not parent
        and child.

        **Why it matters:** it is the single fact the whole topic rests on. Because they are
        siblings, `catch (\Exception)` can never match an `Error`, and only `\Throwable`
        covers both arms.

        **Official reference:** https://www.php.net/manual/en/class.throwable.php

??? question "What does a `catch` clause actually do, mechanically?"
    Think before revealing the answer.

    ??? success "Show answer"
        It performs an `instanceof` test against the thrown object, and the **first**
        matching clause in written order handles it. No specificity ranking happens.

        **Why it matters:** it explains both why `catch (\Exception)` misses `Error` and why
        `catch (\Throwable)` written first makes every later clause dead code — silently,
        with no diagnostic from PHP.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php

??? question "Which interface does `Throwable` itself extend, and since when?"
    Think before revealing the answer.

    ??? success "Show answer"
        `Stringable`, as of **PHP 8.0.0**.

        **Why it matters:** it guarantees every throwable has a usable `__toString()`, which
        is also the one method on `Exception` that is *not* `final` and can therefore be
        overridden in a custom exception.

        **Official reference:** https://www.php.net/manual/en/class.throwable.php

## The Error branch

??? question "Name the direct children of `Error` listed by the manual."
    Think before revealing the answer.

    ??? success "Show answer"
        `ArithmeticError`, `AssertionError`, `CompileError`, `TypeError`, `ValueError`,
        `UnhandledMatchError` and `FiberError`.

        **Why it matters:** it is a closed list in the manual, so a question can legitimately
        ask you to spot the intruder. `RuntimeException` and `JsonException` are the usual
        intruders.

        **Official reference:** https://www.php.net/manual/en/language.errors.php7.php

??? question "Where do `ArgumentCountError` and `ParseError` sit in the hierarchy?"
    Think before revealing the answer.

    ??? success "Show answer"
        `ArgumentCountError` extends **`TypeError`**. `ParseError` extends **`CompileError`**.
        Neither extends `Error` directly.

        **Why it matters:** both are one level deeper than people remember, so
        `catch (\TypeError)` *does* catch a missing-argument error, and
        `catch (\CompileError)` *does* catch a `ParseError` from `eval()`.

        **Official reference:** https://www.php.net/manual/en/language.errors.php7.php

??? question "`TypeError` versus `ValueError` — what is the distinction?"
    Think before revealing the answer.

    ??? success "Show answer"
        `TypeError`: the **type** is wrong. `ValueError`: the type is right but the **value**
        is impossible — for example a chunk size of `0` or a negative length.

        **Why it matters:** both are `Error` subclasses, so neither is caught by
        `catch (\Exception)`, and answer options routinely swap them.

        **Official reference:** https://www.php.net/manual/en/reserved.exceptions.php

??? question "Which throwable does `intdiv(\PHP_INT_MIN, -1)` raise?"
    Think before revealing the answer.

    ??? success "Show answer"
        `ArithmeticError` — **not** `DivisionByZeroError`. The exact result is not
        representable as an `int`.

        **Why it matters:** `catch (\DivisionByZeroError)` around `intdiv()` looks complete
        and misses this case. `catch (\ArithmeticError)` covers both, because
        `DivisionByZeroError` is its child.

        **Official reference:** https://www.php.net/manual/en/function.intdiv.php

## The Exception branch

??? question "Name the two SPL families and their members."
    Think before revealing the answer.

    ??? success "Show answer"
        `LogicException`: `BadFunctionCallException` (→ `BadMethodCallException`),
        `DomainException`, `InvalidArgumentException`, `LengthException`,
        `OutOfRangeException`.
        `RuntimeException`: `OutOfBoundsException`, `OverflowException`, `RangeException`,
        `UnderflowException`, `UnexpectedValueException`.

        **Why it matters:** eleven classes, one closed list in the manual. Choosing the right
        family is a design question the exam asks, and `Logic` means "a bug you could have
        prevented" while `Runtime` means "a condition you could not".

        **Official reference:** https://www.php.net/manual/en/spl.exceptions.php

??? question "`OutOfRangeException` or `OutOfBoundsException` — which is a `LogicException`?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`OutOfRangeException`** is the `LogicException` (an invalid index, detectable by
        reading the code). `OutOfBoundsException` is the `RuntimeException` (a key that
        turned out not to exist at run time).

        **Why it matters:** the names are nearly interchangeable in English and sit in
        different families, which makes them a reliable exam pair.

        **Official reference:** https://www.php.net/manual/en/spl.exceptions.php

??? question "Which branch does `ErrorException` belong to?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **`Exception`** branch — `ErrorException extends Exception` — despite the word
        *Error* in the name. It adds `getSeverity()`, which returns the original `E_*` level.

        **Why it matters:** it is the bridge between the legacy diagnostic system and the
        throwable world, and its name makes it the single best distractor in a
        "which of these extend `Error`" question.

        **Official reference:** https://www.php.net/manual/en/class.errorexception.php

## try / catch / finally

??? question "When does `finally` run?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Always** — after `try`, after any matching `catch`, after a `return` in either, and
        while an unhandled exception unwinds through the frame.

        **Why it matters:** it is what makes `try` + `finally` with no `catch` the canonical
        shape for releasing a lock, handle or transaction while still letting the failure
        propagate.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.finally

??? question "What does a `return` inside `finally` do to a `return` in `try`?"
    Think before revealing the answer.

    ??? success "Show answer"
        It **overrides** it. The `try` return is evaluated where written, but the value is
        handed back only after `finally` runs — and if `finally` returns, that value wins.

        **Why it matters:** the same precedence discards a pending **exception**, silently
        converting a failed call into a successful one. That is why "no `return` in
        `finally`" is a hard rule.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.finally

??? question "`try` throws and `finally` throws. Which one reaches the caller?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **`finally`** exception propagates, and the `try` exception becomes its
        `previous` — appended at the tail of the chain.

        **Why it matters:** a failing cleanup block *masks* the real failure in the first
        message you read, but does not destroy it. Always walk `getPrevious()` to the end.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.finally

??? question "Is `try` with neither `catch` nor `finally` valid?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** Each `try` must have at least one corresponding `catch` **or** a `finally`
        block. `try` + `finally` alone is valid; `try` alone is a syntax error.

        **Why it matters:** it is the rule that makes the cleanup-without-handling pattern
        legitimate rather than a workaround.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php

## Version changes — prime distractor material

??? question "Since which versions: multi-catch `A|B`, variable-less `catch`, `throw` as an expression?"
    Think before revealing the answer.

    ??? success "Show answer"
        Multi-catch `A|B`: **7.1.0**. Omitting the caught variable: **8.0.0**. `throw` as an
        expression: **8.0.0**.

        **Why it matters:** the two 8.0 features are frequently attributed to 7.4, and the
        7.1 one to 8.0. A question set on a wrong version is testing the version, not the
        concept.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php

??? question "What is the value of `E_ALL` in PHP 8.4, and what changed?"
    Think before revealing the answer.

    ??? success "Show answer"
        **30719.** It was **32767** before 8.4, because `E_STRICT` (value 2048) is unused and
        has been deprecated as of PHP 8.4.0.

        **Why it matters:** it is a concrete, checkable 8.4 change, and it also explains why
        `E_ALL & ~E_STRICT` is now a meaningless expression.

        **Official reference:** https://www.php.net/manual/en/errorfunc.constants.php

## Handlers and legacy errors

??? question "Which three mechanisms cover which three failure populations?"
    Think before revealing the answer.

    ??? success "Show answer"
        `set_error_handler()` → traditional diagnostics (warnings, notices, deprecations,
        `trigger_error()`). `set_exception_handler()` → **uncaught** throwables.
        `register_shutdown_function()` + `error_get_last()` → post-mortem on a fatal.

        **Why it matters:** they do not overlap at all. "`set_error_handler()` handles
        uncaught exceptions" is the most common wrong answer in this topic.

        **Official reference:** https://www.php.net/manual/en/function.set-error-handler.php

??? question "Which error levels can `set_error_handler()` never receive?"
    Think before revealing the answer.

    ??? success "Show answer"
        `E_ERROR`, `E_PARSE`, `E_CORE_ERROR`, `E_CORE_WARNING`, `E_COMPILE_ERROR` and
        `E_COMPILE_WARNING` — independent of where they were raised.

        **Why it matters:** it is a closed list in the manual, and it is exactly why the
        shutdown-function layer is not optional in a production error handler.

        **Official reference:** https://www.php.net/manual/en/function.set-error-handler.php

??? question "Does `error_reporting(0)` stop a registered error handler from being called?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** The manual states that `error_reporting` settings have no effect and the
        handler is called regardless. Only the `$error_levels` mask — the second argument to
        `set_error_handler()` — filters it.

        **Why it matters:** people silence diagnostics with `error_reporting(0)` and are
        surprised their handler still throws. The handler *can* read `error_reporting()` and
        return `false` to defer to the standard handler, but that is a choice in your code.

        **Official reference:** https://www.php.net/manual/en/function.set-error-handler.php

??? question "Does the `@` operator stop an exception, and does it hide a diagnostic from a custom handler?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No** to both. `@` suppresses only the *display* of a diagnostic, a registered
        custom error handler is still called, and since PHP 8.0.0 it no longer silences the
        critical errors that terminate the script. It has never had any effect on a thrown
        exception.

        **Why it matters:** `@` is routinely misused as a catch-all. It is not one, and
        `error_get_last()['message']` is how you read what it muted.

        **Official reference:** https://www.php.net/manual/en/language.operators.errorcontrol.php

??? question "What does `set_error_handler()` return, and how do you undo it?"
    Think before revealing the answer.

    ??? success "Show answer"
        It returns the **previously active handler** as a `callable`, or `null` if the
        built-in one was active. Undo it with `restore_error_handler()`, which pops the
        internal stack.

        **Why it matters:** the manual explicitly cautions against "restoring" by passing the
        returned handler back into `set_error_handler()` — that pushes another entry instead
        of removing one, growing the stack without bound and resetting the level mask to
        `E_ALL`.

        **Official reference:** https://www.php.net/manual/en/function.set-error-handler.php

## Edge cases and traps

??? question "Can a class implement `\Throwable` directly?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** A class must extend `Exception` or `Error`. An **interface**, however, may
        `extends \Throwable`.

        **Why it matters:** the fatal message names the fix — `extend Exception or Error
        instead` — and the interface exception is what allows
        `HttpExceptionInterface extends \Throwable` in Symfony.

        **Official reference:** https://www.php.net/manual/en/class.throwable.php

??? question "Can a throwable be cloned?"
    Think before revealing the answer.

    ??? success "Show answer"
        **No.** `Exception::__clone()` is declared `final private`, so `clone $e` fails.

        **Why it matters:** an "immutable copy with a new message" is not available; you
        build a **new** exception and chain the old one as `previous` instead.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.extending

??? question "Which `Exception` methods are `final`?"
    Think before revealing the answer.

    ??? success "Show answer"
        `getMessage()`, `getCode()`, `getFile()`, `getLine()`, `getTrace()`,
        `getPrevious()` and `getTraceAsString()`. Only `__toString()` is overridable.

        **Why it matters:** a custom exception cannot lie about its message or trace, so
        extra behaviour has to arrive through new properties and methods — which is why
        carrying typed data on the exception is the recommended design.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.extending

??? question "Does `getCode()` always return an `int`?"
    Think before revealing the answer.

    ??? success "Show answer"
        It returns `int` for `Exception` and `Error`, but a subclass may return another type:
        `PDOException::getCode()` returns a **`string`** SQLSTATE.

        **Why it matters:** code that assumes an integer code breaks on database exceptions,
        and this is a documented exception to the interface's declared return type.

        **Official reference:** https://www.php.net/manual/en/class.throwable.php

## Symfony integration

??? question "How does Symfony decide the HTTP status code for an uncaught throwable?"
    Think before revealing the answer.

    ??? success "Show answer"
        If a listener sets a `Response` that is a client error, server error or redirect,
        that status is used. Otherwise, if the throwable implements `HttpExceptionInterface`,
        `getStatusCode()` and `getHeaders()` are used. Otherwise **500**.

        **Why it matters:** it explains why a plain `\RuntimeException` from a controller is
        a 500 while a `NotFoundHttpException` is a 404 — one implements the interface and the
        other does not.

        **Official reference:** https://symfony.com/doc/8.0/reference/events.html#kernel-exception

??? question "How do you give your own exception class an HTTP status without extending Symfony's?"
    Think before revealing the answer.

    ??? success "Show answer"
        Put `#[WithHttpStatus(422, ['Retry-After' => 10])]` on the exception class — or on an
        interface it implements — or map it under `framework.exceptions` in configuration.

        **Why it matters:** it keeps domain exceptions free of framework base classes.
        `ErrorListener` applies the attribute only when the throwable is not already an
        `HttpExceptionInterface`, and wraps it in an `HttpException` whose `previous` is your
        original exception.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#exceptions

??? question "In `framework.exceptions`, why does the order of entries matter?"
    Think before revealing the answer.

    ??? success "Show answer"
        Symfony uses the configuration of the **first** entry matching `instanceof`. Listing
        `Exception` before `RuntimeException` makes the `RuntimeException` entry unreachable.

        **Why it matters:** it is the exact same specific-before-general rule as ordering
        `catch` blocks, and it fails just as silently — nothing warns you.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#exceptions

## Memory hooks

??? question "One sentence that encodes the whole hierarchy"
    Think before revealing the answer.

    ??? success "Show answer"
        **"`Throwable` is the cable; `Error` and `Exception` are two different sockets
        plugged into it."** Listening on one socket never picks up the other.

        **Why it matters:** under time pressure the thing people lose is the *shape* of the
        tree, not the class names. This phrasing makes the sibling relationship the memorable
        part.

        **Official reference:** https://www.php.net/manual/en/class.throwable.php

??? question "One sentence that encodes every `finally` rule"
    Think before revealing the answer.

    ??? success "Show answer"
        **"`finally` always runs, and `finally` always wins."** It runs on return, on throw
        and while unwinding; and its `return` beats `try`'s return, while its `throw` beats
        `try`'s throw (demoting it to `previous`).

        **Why it matters:** three separately examinable behaviours collapse into one phrase
        you can recall in seconds.

        **Official reference:** https://www.php.net/manual/en/language.exceptions.php#language.exceptions.finally

---

<small>Back to the lesson: [Exception & Error Handling](exceptions.md) · [Retake the topic exam](exceptions-exam.md) · Next topic: [Traits](traits.md)</small>

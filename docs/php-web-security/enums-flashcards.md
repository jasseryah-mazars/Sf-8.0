# Flashcards — Enums

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Enums](enums.md)** ·
    Practice: **[Guided exercises](enums-exercises.md)** ·
    Test: **[Topic exam](enums-exam.md)**

## Definitions and kinds

??? question "What is a PHP enum, in one sentence?"
    Think before revealing the answer.

    ??? success "Show answer"
        A custom type limited to a **fixed, discrete set of values**, implemented as a class
        whose cases are single-instance objects of that class.

        **Why it matters:** because cases are real objects, they can be type-checked, passed
        anywhere an object is accepted, and carry methods — which is what separates an enum from
        a bag of class constants.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.overview.php

??? question "Pure enum vs backed enum — the one-line distinction?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **pure** enum has cases with no scalar equivalent; a **backed** enum declares a backing
        type (`enum X: string`) and every case has a unique explicit scalar value.

        **Why it matters:** a backed enum may contain only backed cases and a pure enum only
        pure cases — mixing them is a fatal error, and the choice decides whether the value can
        cross a boundary (database, URL, JSON) at all.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Which interfaces does the engine apply to enums, and what does each add?"
    Think before revealing the answer.

    ??? success "Show answer"
        `UnitEnum` on **every** enum — the `name` property and the static `cases()`. `BackedEnum`
        (which extends `UnitEnum`) additionally on backed enums — the read-only `value` property
        plus `from()` and `tryFrom()`.

        **Why it matters:** both interfaces are engine-applied, cannot be implemented by
        user-defined classes, and their methods cannot be overridden. They exist for type checks
        — including Symfony's own `is_subclass_of($type, \BackedEnum::class)` guards.

        **Official reference:** https://www.php.net/manual/en/class.backedenum.php

??? question "Which backing types may a backed enum use?"
    Think before revealing the answer.

    ??? success "Show answer"
        `int` **or** `string`, exactly one of them. No union, no `float`, no `bool`; the fatal
        error reads `Enum backing type must be int or string, … given`.

        **Why it matters:** it is a favourite distractor. `enum X: int|string` looks plausible
        under modern union-type syntax and is rejected outright.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Does PHP auto-generate backing values, the way some languages number cases from 0?"
    Think before revealing the answer.

    ??? success "Show answer"
        No. Every case of a backed enum must define its value **explicitly**, and the values
        must be unique.

        **Why it matters:** it kills two ideas at once — that `Suit::Hearts` equals `"0"`, and
        that adding a case in the middle silently renumbers stored data.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

## The engine API

??? question "`from()`: what does it return, and what does it do on a miss?"
    Think before revealing the answer.

    ??? success "Show answer"
        Returns the matching case instance; on no match it **throws `\ValueError`**
        (`"X" is not a valid backing value for enum Suit`). It never returns `null`.

        **Why it matters:** writing `Suit::from($x) ?? $default` is dead code that hides an
        uncaught `\ValueError`. `from()` is for input you trust.

        **Official reference:** https://www.php.net/manual/en/backedenum.from.php

??? question "`tryFrom()`: what does it return, and when would you prefer it?"
    Think before revealing the answer.

    ??? success "Show answer"
        Returns the matching case or **`null`**. Prefer it for untrusted input, typically as
        `Suit::tryFrom($raw) ?? Suit::Spades`.

        **Why it matters:** it is the only member of the enum API that answers a miss with
        `null` — everything else either throws or returns a real case.

        **Official reference:** https://www.php.net/manual/en/backedenum.tryfrom.php

??? question "Does `tryFrom()` protect you from a wrong argument *type*?"
    Think before revealing the answer.

    ??? success "Show answer"
        No. It rescues a bad **value**, not a bad **type**. Under `strict_types=1`, passing a
        `string` to an `int`-backed enum's `tryFrom()` throws `\TypeError`; in weak mode a
        non-numeric string throws `\TypeError` too.

        **Why it matters:** "wrap it in `tryFrom()` and it can't blow up" is false. Cast or
        guard the type first, then let `tryFrom()` answer the value question.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "How do `from()`/`tryFrom()` behave in weak typing mode versus strict mode?"
    Think before revealing the answer.

    ??? success "Show answer"
        Weak mode coerces `int`/`string`/`float` to the backing type; strict mode throws
        `\TypeError` for a mismatch (e.g. an `int` given to a string-backed enum), and for a
        `float` in **both** modes' equivalent of a wrong type.

        **Why it matters:** the *same* call, `Priority::from('2')`, is a `TypeError` in a file
        with `declare(strict_types=1)` and a successful lookup in one without it.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "What exactly does `cases()` return?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **packed** (list) array of the enum's case **instances**, in **declaration order** —
        not names, not values.

        **Why it matters:** it is available on pure enums too, which is why `EnumType` can build
        a form from any enum. Names and values come from `array_column($x::cases(), 'name')`
        and `array_column($x::cases(), 'value')`.

        **Official reference:** https://www.php.net/manual/en/unitenum.cases.php

??? question "May you declare your own `cases()`, `from()` or `tryFrom()` on an enum?"
    Think before revealing the answer.

    ??? success "Show answer"
        No — a fatal error (`Cannot redeclare S::cases()`). Those are engine-provided. Give your
        alternative constructor or filtered listing a different name.

        **Why it matters:** the exam likes the idea of "overriding `cases()` to hide a case"; the
        language forbids it, so the answer is always a new method such as `active()`.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.listing.php

## What an enum may and may not contain

??? question "List what an enum body legally supports."
    Think before revealing the answer.

    ??? success "Show answer"
        Public/private/protected **methods** and **static methods**, **constants** at any
        visibility, implementing **any number of interfaces**, **traits** (methods, static
        methods and constants only), and **attributes** on the enum and on its cases.

        **Why it matters:** everything a case "carries" must come from `name`, `value`, a method
        or a constant — there is no other slot.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.object-differences.php

??? question "List what an enum may never have."
    Think before revealing the answer.

    ??? success "Show answer"
        Constructors and destructors, inheritance (neither extending nor being extended),
        instance **or** static **properties**, cloning, and magic methods other than the three
        allowed ones. Enums must also be declared before use.

        **Why it matters:** every one of these follows from a single invariant — a case is a
        stateless singleton. Learn the invariant and you can re-derive the list.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.object-differences.php

??? question "Which magic methods *are* allowed on an enum?"
    Think before revealing the answer.

    ??? success "Show answer"
        `__call()`, `__callStatic()` and `__invoke()`. Everything else — including
        `__construct()`, `__toString()`, `__get()` and `__clone()` — is a fatal error.

        **Why it matters:** an enum can therefore never be `Stringable`; `(string) Suit::Hearts`
        throws `Error: Object of class Suit could not be converted to string`. Use
        `->value` explicitly.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.object-differences.php

??? question "What is the caveat when an enum uses a trait?"
    Think before revealing the answer.

    ??? success "Show answer"
        The trait must contain **no properties** — only methods, static methods and constants. A
        property in the trait produces the same fatal error as one written inline:
        `Enum … cannot include properties`.

        **Why it matters:** traits are the only sharing mechanism available to enums, since
        inheritance is impossible — so knowing their one restriction matters more than usual.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.traits.php

??? question "Are enums final? Can you write `final enum`?"
    Think before revealing the answer.

    ??? success "Show answer"
        Enums are **implicitly final** (`ReflectionClass::isFinal()` is `true`), and writing
        `final enum` is a **parse error**.

        **Why it matters:** the reason is `match` exhaustiveness — a subtype could add a case
        that existing `match` expressions do not cover, so the language forbids subtyping
        entirely.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.object-differences.php

??? question "Can an enum constant refer to a case?"
    Think before revealing the answer.

    ??? success "Show answer"
        Yes: `public const Huge = self::Large;`. This is the documented way to create an
        **alias**, and `Size::Huge === Size::Large` is `true`.

        **Why it matters:** it is the correct answer to "how do I give a case a second name?" —
        never by duplicating a backing value, which is an `Error`.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.constants.php

??? question "Where may an enum case appear in a constant expression, and where may it not?"
    Think before revealing the answer.

    ??? success "Show answer"
        Allowed: class-constant values, property defaults, static-variable defaults, parameter
        defaults, global constants. Not allowed: anything requiring execution — a method call, a
        property fetch, or an `ArrayAccess` offset such as `Direction::Up['short']`
        (`Cannot use [] on objects in constant expression`). A case value may not be built from
        another enum case.

        **Why it matters:** `function query(SortOrder $o = SortOrder::Asc)` is idiomatic, and
        knowing the boundary explains why one very similar-looking line fatals.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.expressions.php

## Comparison, identity and control flow

??? question "Why is `===` always the right comparison for enum cases?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because each case is a **singleton**: `Suit::Hearts`, `Suit::from('H')`,
        `Suit::cases()[0]` and `unserialize(serialize(Suit::Hearts))` are all the *same* object.

        **Why it matters:** with no per-instance state there is nothing for `==` to compare
        differently, so `===` is both correct and the clearest statement of intent.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.basics.php

??? question "Is `Suit::Hearts == 'H'` true for a string-backed enum?"
    Think before revealing the answer.

    ??? success "Show answer"
        No — `false`. A case is an object and never loosely equals its backing scalar. Compare
        `Suit::Hearts->value === 'H'`.

        **Why it matters:** it is the most common "it worked in my head" bug when migrating from
        string constants to enums, and it fails silently rather than throwing.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.basics.php

??? question "What do `<` and `>` return between two enum cases?"
    Think before revealing the answer.

    ??? success "Show answer"
        Always `false` — relational comparison is not meaningful on objects.

        **Why it matters:** sorting cases with `usort($cases, fn($a, $b) => $a > $b)` silently
        does nothing. Sort on `->value`, or on the declaration index from `cases()`.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.basics.php

??? question "What does `match` do on an enum when no arm matches and there is no `default`?"
    Think before revealing the answer.

    ??? success "Show answer"
        Throws `\UnhandledMatchError: Unhandled match case of type Suit`.

        **Why it matters:** omitting `default` on purpose is the idiom that makes adding a case
        fail loudly at every place that has not been updated — the enum's main safety benefit.

        **Official reference:** https://www.php.net/manual/en/control-structures.match.php

## Serialization, reflection and tooling

??? question "How does `serialize()` represent an enum case, and does identity survive?"
    Think before revealing the answer.

    ??? success "Show answer"
        With a dedicated `"E"` code storing the case **name**: `E:11:"Suit:Hearts";`.
        `unserialize(serialize(Suit::Hearts)) === Suit::Hearts` is `true`, because
        deserialization restores the existing singleton. An unknown enum/case emits a warning
        and returns `false`.

        **Why it matters:** pure enums serialize natively too — it is **JSON**, not `serialize()`,
        that needs a backing value. The `allowed_classes` option of `unserialize()` does not
        affect enums.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.serialization.php

??? question "What does `json_encode()` do with a pure enum and with a backed enum?"
    Think before revealing the answer.

    ??? success "Show answer"
        A backed enum encodes as its **scalar value only**. A pure enum has no default JSON
        serialization: encoding fails (`Non-backed enums have no default serialization`).
        Implementing `JsonSerializable` overrides either behaviour.

        **Why it matters:** this is the practical reason API DTOs use backed enums — and the
        reason a pure enum sneaking into a JSON response breaks the whole payload, not one field.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.serialization.php

??? question "Are `name` and `value` writable?"
    Think before revealing the answer.

    ??? success "Show answer"
        No, both are read-only: assignment throws
        `Error: Cannot modify readonly property Suit::$value`, and taking a reference to
        `->value` fails with "Cannot indirectly modify readonly property".

        **Why it matters:** the whole process shares one instance per case, so a writable
        property would let one caller mutate every other caller's value.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Which attribute target covers an enum **case**, and how do you read it back?"
    Think before revealing the answer.

    ??? success "Show answer"
        `Attribute::TARGET_CLASS_CONSTANT` (cases are class constants); `Attribute::TARGET_CLASS`
        covers the enum type itself. Read it with `ReflectionEnum::getCase()`, which returns a
        `ReflectionEnumBackedCase` or `ReflectionEnumUnitCase` exposing `getAttributes()`.

        **Why it matters:** it is the clean way to attach per-case metadata (labels, icons,
        permissions) without a `match` in every consumer.

        **Official reference:** https://www.php.net/manual/en/class.reflectionenum.php

??? question "`enum_exists()` versus `class_exists()` on an enum?"
    Think before revealing the answer.

    ??? success "Show answer"
        Both return `true` for an enum (an enum *is* a class), but `enum_exists()` returns `true`
        **only** for enums. Both take an `$autoload` flag defaulting to `true`.

        **Why it matters:** it is how Symfony's `EnumType` validates its `class` option —
        `setAllowedValues('class', enum_exists(...))` — so a plain class is rejected.

        **Official reference:** https://www.php.net/manual/en/function.enum-exists.php

## Symfony integration

??? question "What does `BackedEnumValueResolver` do, and at which priority is it registered?"
    Think before revealing the answer.

    ??? success "Show answer"
        It resolves a controller argument typed as a backed enum from the matching **request
        attribute** (a route path parameter), calling `$enumType::from($value)` and converting
        `\ValueError`/`\TypeError` into `NotFoundHttpException`. It is tagged
        `controller.argument_value_resolver` with **priority 100**.

        **Why it matters:** an invalid enum in a URL is a plain **404**, not a 500 — the single
        most testable Symfony fact about enums.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Controller/ArgumentResolver/BackedEnumValueResolver.php

??? question "Name the three cases where `BackedEnumValueResolver` declines to resolve an argument."
    Think before revealing the answer.

    ??? success "Show answer"
        When the argument type is not a subclass of `BackedEnum` (so: pure enums), when the
        argument is **variadic**, and when the request attribute with that name does not exist —
        the last one deliberately lets `DefaultValueResolver` supply a default.

        **Why it matters:** it explains why `list(OrderStatusEnum $status = OrderStatusEnum::Paid)`
        works with no route parameter, and why a **pure** enum type-hint fails with "could not be
        resolved" instead of a 404.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Controller/ArgumentResolver/BackedEnumValueResolver.php

??? question "What does `EnumRequirement` produce, and what can you pass to it?"
    Think before revealing the answer.

    ??? success "Show answer"
        A route requirement string: each case's `->value`, `preg_quote()`d and joined with `|`.
        Pass a backed-enum **class-string** (all cases) or a **list of cases** (a subset).
        Anything else throws `InvalidArgumentException`.

        **Why it matters:** it moves the "which values are acceptable" decision into **routing**,
        so a rejected value never reaches a resolver or your controller.

        **Official reference:** https://symfony.com/doc/8.0/routing.html#backed-enum-parameters

??? question "Which `EnumType` option is required, and where do its choices and labels come from?"
    Think before revealing the answer.

    ??? success "Show answer"
        `class` is required and must pass `enum_exists()`. `choices` defaults to
        `$options['class']::cases()`; `choice_label` uses each case's `name`, or
        `TranslatableInterface::trans()` when the enum implements it; `choice_value` is derived
        from `->value` **only** for backed enums. Its parent type is `ChoiceType`.

        **Why it matters:** a hand-written `ChoiceType` mirroring the enum drifts the moment a
        case is added; `EnumType` cannot.

        **Official reference:** https://symfony.com/doc/8.0/reference/forms/types/enum.html

??? question "How is an enum mapped onto a Doctrine column in Symfony 8?"
    Think before revealing the answer.

    ??? success "Show answer"
        With the `enumType` option: `#[ORM\Column(enumType: Suit::class)]`. Only **backed** enums
        may be used for entity properties, because Doctrine persists their scalar values.

        **Why it matters:** `enumType` and `type` are different options — `type` is the *column*
        type, `enumType` the PHP enum used to hydrate it.

        **Official reference:** https://symfony.com/doc/8.0/doctrine.html#entity-field-types

??? question "`#[MapQueryParameter]` on a backed-enum argument receives an invalid value. Default outcome?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **404**: the resolver catches the `\ValueError` from `from()` into `null` and then
        throws an `HttpException` with `MapQueryParameter::$validationFailedStatusCode`, which
        defaults to `Response::HTTP_NOT_FOUND`. Passing `flags: \FILTER_NULL_ON_FAILURE` yields
        `null` instead.

        **Why it matters:** query-string enums fail the same way route enums do, which is not
        obvious — and the status is configurable per argument.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Attribute/MapQueryParameter.php

??? question "How does the Serializer handle an unknown backing value when denormalizing?"
    Think before revealing the answer.

    ??? success "Show answer"
        `BackedEnumNormalizer` throws `NotNormalizableValueException` (carrying the
        deserialization path). Set the context option `BackedEnumNormalizer::ALLOW_INVALID_VALUES`
        to get `null` instead — including when the data is neither an `int` nor a `string`.

        **Why it matters:** it is the difference between a 422-style validation report and a
        silently `null` field in a deserialized DTO.

        **Official reference:** https://symfony.com/doc/8.0/serializer.html

??? question "How do you reach an enum from a Twig template?"
    Think before revealing the answer.

    ??? success "Show answer"
        With the `enum()` function (Twig 3.15+): `enum('App\\Status').Draft.value`,
        `enum('App\\Status').cases`, `enum('App\\Status').from('draft')`. A string literal
        argument is validated at compile time.

        **Why it matters:** it removes the habit of passing a hand-built array of labels into
        every template just to render a status.

        **Official reference:** https://twig.symfony.com/doc/3.x/functions/enum.html

## Traps and memory hooks

??? question "What is the failure mode of reading `->value` on a **pure** enum case?"
    Think before revealing the answer.

    ??? success "Show answer"
        A `Warning: Undefined property: Level::$value`, and the expression evaluates to `null`.
        It is **not** an `Error` and does not stop execution.

        **Why it matters:** the bug is silent by default, so it reaches storage or a response
        body instead of a stack trace. Type-hint `BackedEnum` when you intend to read `->value`.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.basics.php

??? question "Two cases share the same backing value. When and how does PHP complain?"
    Think before revealing the answer.

    ??? success "Show answer"
        At **class-link time**, with `Error: Duplicate value in enum Suit for cases Hearts and
        Spades` — before any call, as soon as the enum is loaded.

        **Why it matters:** unique values are what make `from()` a well-defined inverse of
        `->value`; the alias you actually wanted is a constant.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Memory hook for `from()` versus `tryFrom()`?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`from()` is furious — it throws. `tryFrom()` merely tries — it returns `null`.**
        Trusted input gets `from()`; untrusted input gets `tryFrom()` plus `??`.

        **Why it matters:** every Symfony integration is built on `from()` and wraps it in a
        `try`/`catch` for you — routing, `#[MapQueryParameter]` and the Serializer each turn that
        `\ValueError` into their own kind of failure.

        **Official reference:** https://www.php.net/manual/en/backedenum.from.php

---

<small>Back to the lesson: [Enums](enums.md) · [Retake the topic exam](enums-exam.md) · Continue to the next topic: [Namespaces & Autoloading](namespaces.md)</small>

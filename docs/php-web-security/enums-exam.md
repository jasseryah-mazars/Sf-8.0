# Topic Exam — Enums

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because the exam is built on
    near-misses rather than definitions.

    Theory: **[Enums](enums.md)** ·
    Practice: **[Guided exercises](enums-exercises.md)** ·
    Recall: **[Flashcards](enums-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4** and **Symfony 8.0**.

## The two enum kinds and their API

??? question "Question 1"
    `Status` is a string-backed enum with cases `Draft = 'draft'` and `Published = 'published'`.
    What does `Status::from('missing')` do?

    - A. Returns `null`
    - B. Throws `\ValueError`
    - C. Returns a new anonymous case
    - D. Returns `false`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `BackedEnum::from()` maps a scalar to the matching case; when no case
        matches it throws `\ValueError` with the message
        `"missing" is not a valid backing value for enum Status`. The method is meant for
        *trusted* input, where a missing value should stop the application.

        **A** describes `tryFrom()`, the sibling method — it is the only member of this API that
        returns `null` on a miss. **C** is impossible: an enum's cases are fixed at declaration
        time and are singletons, so no new instance can ever be produced. **D** confuses enums
        with older "return `false` on failure" PHP APIs; `from()` has a `static` return type and
        never returns a scalar.

        **Official reference:** https://www.php.net/manual/en/backedenum.from.php

??? question "Question 2"
    Which interface do **only backed** enums implement?

    - A. `BackedEnum`
    - B. `UnitEnum`
    - C. `Stringable`
    - D. `Countable`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the engine applies `UnitEnum` to *every* enum and additionally applies
        `BackedEnum` (which itself extends `UnitEnum`) to backed enums. `BackedEnum` is what adds
        the read-only `value` property plus `from()` and `tryFrom()`.

        **B** is applied to pure enums too, so it does not discriminate. **C** is never automatic:
        an enum cannot even declare `__toString()`, so it is not `Stringable` unless… it simply
        cannot be — declaring the magic method is a fatal error. **D** is unrelated; an enum is not
        countable unless you implement `Countable` yourself, and that has nothing to do with being
        backed.

        **Official reference:** https://www.php.net/manual/en/class.backedenum.php

??? question "Question 3"
    ```php
    enum Level
    {
        case Low;
        case High;
    }

    echo Level::Low->value;
    ```
    What happens on the last line?

    - A. Fatal `Error: Cannot access property on enum`
    - B. Prints `0`, the case index
    - C. A warning `Undefined property: Level::$value`, and the expression is `null`
    - D. Prints `Low`, falling back to the case name

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** only *backed* cases get a `value` property. A pure enum case has `name`
        and nothing else, so reading `->value` is an ordinary undefined-property read: PHP emits
        `Warning: Undefined property: Level::$value` and evaluates to `null`. That is the nastiest
        shape of this bug — it does not stop execution, it silently poisons a value.

        **A** overstates it: no `Error` is thrown, which is exactly why the bug survives to
        production. **B** invents a scalar backing; the manual is explicit that `Suit::Hearts` is
        *not* equal to `"0"` and that pure cases have no intrinsic scalar. **D** invents a
        fallback: `name` and `value` are separate properties and neither substitutes for the other.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.basics.php

??? question "Question 4"
    Which of the following can an enum declaration contain? (choose three)

    - A. Public, private and protected methods
    - B. Class constants, including one that refers to a case
    - C. Instance or static properties
    - D. Static methods used as alternative constructors

    ??? success "Show answer"
        **Correct answer:** A, B, D

        **Explanation:** the manual's "Differences from objects" list is explicit about what an
        enum keeps and what it loses. It keeps public/private/protected methods and static methods
        (private and protected are equivalent to each other in practice, since inheritance is
        impossible), constants — and a constant may alias a case, as in
        `public const Huge = self::Large;` — plus interface implementation and attributes.

        **C** is the excluded one: `Enum S cannot include properties` is a fatal error for both
        instance and static properties, because cases must be stateless singletons. Everything a
        case "carries" must therefore come from its `name`, its `value`, or a method.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.object-differences.php

??? question "Question 5"
    What can an enum **case** never have?

    - A. Methods
    - B. Constants
    - C. Implemented interfaces
    - D. Non-constant instance state

    ??? success "Show answer"
        **Correct answer:** D

        **Explanation:** enum cases are singleton instances of the enum type. Allowing per-instance
        state would mean two references to `Suit::Hearts` could diverge, which would destroy the
        guarantee that identity comparison (`===`) answers "is this the same case?". PHP therefore
        forbids properties outright.

        **A** is allowed — methods are declared on the enum and available on every case, with
        `$this` bound to the case. **B** is allowed: enums may declare constants at any visibility.
        **C** is allowed and common: `enum Suit: string implements HasColor` puts the interface
        after the backing type, and every case then satisfies that type check.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.methods.php

## Declaration rules and load-time failures

??? question "Question 6"
    ```php
    enum Priority: int|string
    {
        case Low = 1;
        case High = 'high';
    }
    ```
    What happens?

    - A. It works: a union-backed enum accepts both scalar types
    - B. Fatal error — the backing type must be `int` or `string`, not a union
    - C. It works, but `from()` is disabled
    - D. Only the first case is registered

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** PHP rejects the declaration with
        `Fatal error: Enum backing type must be int or string, string|int given`. The manual states
        the rule directly: a backed enum supports a **single** backing type at a time, `int` or
        `string`, and never a union.

        **A** is the exact misconception the rule exists to kill. **C** invents a partial
        degradation that PHP never performs — the declaration is refused, so nothing is available.
        **D** invents per-case tolerance; enum validity is decided for the whole declaration.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Question 7"
    ```php
    enum Suit: string
    {
        case Hearts = 'H';
        case Spades = 'H';
    }

    var_dump(Suit::Hearts);
    ```
    What is the outcome?

    - A. The second declaration silently overwrites the first
    - B. `Suit::Spades` becomes an alias of `Suit::Hearts`
    - C. `Error: Duplicate value in enum Suit for cases Hearts and Spades`
    - D. Nothing — duplicates are only detected by `from()`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** backing values must be unique. PHP raises
        `Error: Duplicate value in enum Suit for cases Hearts and Spades` when the enum is linked
        (the `var_dump()` line is what forces the class to load in this snippet). Uniqueness is
        what makes `from()` a well-defined inverse of `->value`.

        **A** would make `from('H')` ambiguous, which is precisely what PHP refuses. **B** is close
        to a real feature but the wrong mechanism: aliasing is done with a **constant**
        (`const Trump = self::Hearts;`), never with a duplicated backing value. **D** misplaces the
        check: it happens at class-link time, before any call.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Question 8"
    True or false: an enum may be declared `final enum Suit { … }` to signal that it cannot be
    extended.

    - A. True — `final` is optional but allowed, and good style
    - B. False — the parser rejects `final enum`; enums are implicitly final
    - C. True, but only for backed enums
    - D. False — enums are not final; they may be extended by another enum

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `final enum A { case X; }` is a **parse error**. Enums are already final:
        `ReflectionClass::isFinal()` returns `true` for any enum, and a class trying to extend one
        fails with `Class B cannot extend final class A`. The manual explains why — a `match` over
        an enum's cases is exhaustive only if no subtype can add a case later.

        **A** is wrong at the syntax level, not merely at the style level. **C** invents a
        distinction; pure and backed enums are equally final. **D** contradicts the language:
        `enum B extends A` is a parse error, and enums may neither extend nor be extended.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.object-differences.php

??? question "Question 9"
    Which of these enum bodies is **illegal**?

    - A. `use CountsThings;` where the trait declares only methods and constants
    - B. `use HasLabel;` where the trait declares `public string $label = '';`
    - C. `public const DEFAULT = self::Draft;`
    - D. `public static function fromLength(int $cm): self { … }`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** enums may use traits, but a trait used in an enum must contain **no
        properties** — only methods, static methods and constants. A trait carrying a property
        triggers the same fatal error as declaring the property inline:
        `Enum S cannot include properties`.

        **A** is the supported case and is the idiomatic way to share behaviour between enums,
        since inheritance is unavailable. **C** is explicitly legal — an enum constant may refer to
        a case, creating an alias. **D** is the manual's own example: static methods on an enum act
        as alternative constructors.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.traits.php

??? question "Question 10"
    An enum declares `public static function cases(): array { return []; }` in order to filter the
    list. What happens?

    - A. It overrides the engine implementation, which is the documented extension point
    - B. Fatal error: `Cannot redeclare S::cases()`
    - C. It is ignored; the engine version always wins
    - D. It works, but `EnumType` keeps using the engine version

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `cases()`, `from()` and `tryFrom()` are provided by the engine through
        `UnitEnum`/`BackedEnum`, and the manual states that manually defining them is a fatal
        error. PHP reports `Fatal error: Cannot redeclare S::cases()`. Filtering belongs in a
        differently named static method, e.g. `public static function active(): array`.

        **A** inverts the rule: those interfaces exist *only* for type checks and may not be
        re-implemented. **C** describes silent tolerance PHP does not offer. **D** implies the
        declaration succeeds; it never gets that far, because the enum cannot be loaded at all.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.listing.php

## Typing, coercion and comparison

??? question "Question 11"
    ```php
    <?php
    declare(strict_types=1);

    enum Suit: string
    {
        case Hearts = 'H';
    }

    Suit::from(1);
    ```
    Which exception is thrown?

    - A. `\ValueError`, because `1` matches no case
    - B. `\TypeError`, because a string-backed enum's `from()` requires a string
    - C. `\InvalidArgumentException`
    - D. None — `1` is coerced to `'1'`, then `\ValueError` is thrown

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `from()` and `tryFrom()` follow the normal weak/strong typing rules. Under
        `strict_types=1`, passing an `int` to a string-backed enum's `from()` is a type violation
        before any lookup happens:
        `TypeError: Suit::from(): Argument #1 ($value) must be of type string, int given`.

        **A** would be the answer only in weak mode, where the `int` is coerced to `'1'` first and
        *then* fails to match. **C** is a userland SPL exception the engine never throws here. **D**
        describes exactly the weak-mode behaviour, which `declare(strict_types=1)` disables — the
        line is at the top of the file precisely so this distractor is tempting.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Question 12"
    A file has **no** `declare(strict_types=1)`. `Num` is an `int`-backed enum with `One = 1`.
    What does `Num::from('1')` return?

    - A. `null`
    - B. `Num::One`
    - C. It throws `\TypeError`
    - D. It throws `\ValueError`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** in weak typing mode the numeric string `'1'` is coerced to the `int` `1`,
        which matches `Num::One`. The manual spells this out: in weak mode passing an `int` or
        `string` is acceptable and the value is coerced; a `float` is coerced too.

        **A** describes `tryFrom()` on a genuine miss, which this is not. **C** would be the strict
        mode answer for this same call. **D** would require the coerced value to match no case —
        `Num::from('7')` would indeed throw `\ValueError`, but `'1'` matches. Note that a
        non-numeric string such as `'abc'` still throws `\TypeError` even in weak mode.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.backed.php

??? question "Question 13"
    Which comparisons evaluate to `true`? (choose two)

    - A. `Suit::Hearts === Suit::from('H')`
    - B. `Suit::Hearts == 'H'`
    - C. `Suit::Hearts === unserialize(serialize(Suit::Hearts))`
    - D. `Suit::Hearts < Suit::Spades`

    ??? success "Show answer"
        **Correct answer:** A, C

        **Explanation:** every case is a singleton object, so any route back to the same case —
        `from()`, a constant alias, `cases()`, deserialization — yields the *same* instance, and
        `===` is `true`. Serialization uses a dedicated `"E"` code (`E:11:"Suit:Hearts";`) whose
        whole purpose is to restore the existing singleton rather than build a copy.

        **B** is false: an enum case is an object and never loosely equals its backing scalar. You
        must compare `Suit::Hearts->value == 'H'` if that is what you mean. **D** is false, and so
        is `>`: relational comparison is not meaningful on objects, so the manual states these
        comparisons always return `false` for enum values — which makes `usort()` on cases a silent
        no-op unless you sort on `->value` or on `array_search()` positions.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.serialization.php

??? question "Question 14"
    ```php
    enum Suit { case Hearts; case Spades; }

    function describe(Suit $s): string
    {
        return match ($s) {
            Suit::Hearts => 'red',
        };
    }

    describe(Suit::Spades);
    ```
    What happens?

    - A. Returns `null`, since no arm matched
    - B. Returns `'red'`, because `match` falls through to the first arm
    - C. `\UnhandledMatchError` is thrown
    - D. A `TypeError`, because the return type is `string`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** `match` is exhaustive by design: with no matching arm and no `default`,
        it throws `\UnhandledMatchError: Unhandled match case of type Suit`. Pairing `match` with
        an enum and deliberately omitting `default` is the standard way to make a *new* case break
        loudly at the exact place that has not been updated.

        **A** describes `switch` semantics with no matching `case` (which simply does nothing),
        not `match`. **B** invents fall-through; `match` never falls through and uses identity
        comparison. **D** misreads the order of events: the `\UnhandledMatchError` is thrown while
        evaluating `match`, so the return type is never reached.

        **Official reference:** https://www.php.net/manual/en/control-structures.match.php

??? question "Question 15"
    `Suit` is a string-backed enum and `$suit = Suit::Hearts;`. Which statement is true?

    - A. `$suit->value = 'X';` silently changes the case for the whole process
    - B. `$suit->value = 'X';` throws `Error: Cannot modify readonly property`
    - C. `clone $suit` returns a second, independent instance
    - D. `new Suit()` returns the first declared case

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `name` and `value` are read-only. Writing to either throws
        `Error: Cannot modify readonly property Suit::$value`, and even taking a reference
        (`$ref = &$suit->value;`) fails with "Cannot indirectly modify readonly property".

        **A** is what the read-only rule prevents — and it would be catastrophic, since every
        holder of that case shares the one instance. **C** is false: cloning an enum case throws
        `Error: Trying to clone an uncloneable object of class Suit`, because cases must remain
        singletons. **D** is false: `new Suit()` throws `Error: Cannot instantiate enum Suit`, and
        so does `ReflectionClass::newInstanceWithoutConstructor()`.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.object-differences.php

## Listing, serialization and reflection

??? question "Question 16"
    What exactly does `Suit::cases()` return?

    - A. An associative array keyed by case name
    - B. A packed (list) array of case instances, in declaration order
    - C. An array of the backing values
    - D. An array of case names as strings

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `UnitEnum::cases()` returns a packed array of all cases **in order of
        declaration** — real case objects, not scalars. It exists on pure enums too, which is why
        `EnumType` can populate a form from any enum.

        **A** is a common wish, obtained with `array_column(Suit::cases(), null, 'name')`. **C** is
        what `array_column(Suit::cases(), 'value')` gives you and only works for backed enums.
        **D** is what `array_column(Suit::cases(), 'name')` gives you. All three wrong answers
        describe one-liners you write *from* `cases()`; none is what `cases()` itself returns.

        **Official reference:** https://www.php.net/manual/en/unitenum.cases.php

??? question "Question 17"
    `Level` is a pure enum and `Suit` is a string-backed enum. What does `json_encode()` do with
    each?

    - A. Both encode as their case name
    - B. `Suit::Hearts` encodes as `"H"`; `Level::Low` fails to encode
    - C. Both encode as an object with `name` and `value` keys
    - D. Both fail unless the enum implements `JsonSerializable`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** a backed enum is represented **by its scalar value only**, in the
        appropriate JSON type. A pure enum has no default JSON serialization: `json_encode()`
        fails with `Non-backed enums have no default serialization` (returning `false`, or throwing
        `\JsonException` with `JSON_THROW_ON_ERROR`). Implementing `JsonSerializable` overrides the
        behaviour of either kind.

        **A** invents name-based encoding — that is what PHP's *native* `serialize()` records, not
        what `json_encode()` emits. **C** invents object encoding; enums are deliberately encoded
        as flat scalars so they round-trip through APIs. **D** is half-right: `JsonSerializable` is
        only *required* for pure enums, while a backed enum already works.

        **Official reference:** https://www.php.net/manual/en/language.enumerations.serialization.php

??? question "Question 18"
    You want to read a custom attribute attached to an enum **case** through Reflection. Which
    attribute target must the attribute class declare, and which Reflection class exposes the
    case?

    - A. `Attribute::TARGET_CLASS` and `ReflectionClass`
    - B. `Attribute::TARGET_PROPERTY` and `ReflectionProperty`
    - C. `Attribute::TARGET_CLASS_CONSTANT` and `ReflectionEnumBackedCase` / `ReflectionEnumUnitCase`
    - D. `Attribute::TARGET_ALL` only; cases are not reflectable individually

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** cases are implemented as class constants, so the class-constant target
        covers them, and `ReflectionEnum::getCase()` returns a `ReflectionEnumBackedCase` (backed)
        or `ReflectionEnumUnitCase` (pure) on which `getAttributes()` works. This is the mechanism
        behind "give each case a label without a `match`".

        **A** targets the **enum type itself**, which is legitimate but a different target — an
        attribute declared `TARGET_CLASS` cannot be applied to a case. **B** is impossible: enums
        cannot have properties at all. **D** is doubly wrong: `TARGET_ALL` would work but is not
        *required*, and cases are very much reflectable.

        **Official reference:** https://www.php.net/manual/en/class.reflectionenum.php

??? question "Question 19"
    Which expression is **rejected** in a constant expression?

    - A. `class Foo { const D = Direction::Down; }`
    - B. `function f(SortOrder $o = SortOrder::Asc) {}`
    - C. `class Foo { const U = Direction::Up['short']; }` where the enum implements `ArrayAccess`
    - D. `enum Size { case Large; public const Huge = self::Large; }`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** cases are constants on the enum, so they may appear in class-constant
        values, property defaults, static-variable defaults and parameter defaults. What is refused
        is anything that would require *running code*: an `ArrayAccess` offset on an enum in a
        constant expression fails with `Error: Cannot use [] on objects in constant expression`,
        because PHP cannot guarantee determinism or freedom from side effects. The same expression
        outside a constant context is perfectly legal.

        **A** and **B** are both documented as allowed. **D** is the manual's own example of a
        constant aliasing a case. Only **C** crosses from "a value known at compile time" into "a
        method call".

        **Official reference:** https://www.php.net/manual/en/language.enumerations.expressions.php

## Symfony integration

??? question "Question 20"
    A controller action is declared `public function show(Status $status): Response` where `Status`
    is a backed enum, and a request arrives with a `{status}` route value matching no case. What
    does the client receive?

    - A. A 404 Not Found — the resolver catches the `\ValueError` and raises `NotFoundHttpException`
    - B. A 500 Internal Server Error from an uncaught `\ValueError`
    - C. A 200 response with `$status` resolved to `null`
    - D. A 200 response with `$status` resolved to the first declared case

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `BackedEnumValueResolver` calls `$enumType::from($value)` inside a
        `try`/`catch (\ValueError|\TypeError)` and rethrows as `NotFoundHttpException`. An invalid
        enum value in a URL is therefore an ordinary 404, handled like any missing resource — not
        an error page.

        **B** is what would happen if the resolver did not catch, which is exactly the design
        decision the source makes explicit. **C** cannot happen for a non-nullable argument: the
        resolver returns `[null]` only when the request attribute itself is `null`. **D** invents a
        silent fallback that would hide bad URLs and produce wrong pages.

        **Official reference:** https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/HttpKernel/Controller/ArgumentResolver/BackedEnumValueResolver.php

??? question "Question 21"
    In which of these situations does `BackedEnumValueResolver` **not** produce a value? (choose two)

    - A. The controller argument is type-hinted with a **pure** enum
    - B. The route defines `{suit}` and the argument is `Suit $suit` (backed)
    - C. The request attribute `suit` does not exist at all
    - D. The request attribute already holds a `Suit` instance

    ??? success "Show answer"
        **Correct answer:** A, C

        **Explanation:** the resolver's first guard is
        `is_subclass_of($argument->getType(), \BackedEnum::class)` — a pure enum fails it and the
        resolver returns `[]`, so the argument stays unresolved and the kernel reports that the
        controller argument could not be resolved. Its third guard returns `[]` when
        `$request->attributes` has no entry with the argument's name, deliberately letting
        `DefaultValueResolver` supply a default (which is what makes
        `list(OrderStatusEnum $status = OrderStatusEnum::Paid)` work) or letting the resolver chain
        fail with a meaningful message.

        **B** is the normal path: the value is looked up and converted with `from()`. **D** also
        produces a value — if the attribute is already a `BackedEnum`, it is returned as-is, which
        is why a custom listener may pre-convert route values without breaking anything.

        **Official reference:** https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/HttpKernel/Controller/ArgumentResolver/BackedEnumValueResolver.php

??? question "Question 22"
    You want `/cards/{suit}` to accept only `D` and `S` out of a four-case `Suit` enum, and to 404
    on every other value **at routing time**. What do you write?

    - A. `requirements: ['suit' => new EnumRequirement([Suit::Diamonds, Suit::Spades])]`
    - B. `requirements: ['suit' => Suit::class]`
    - C. Nothing — `BackedEnumValueResolver` already restricts the route to a subset
    - D. `requirements: ['suit' => new EnumRequirement(Suit::class)]`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `EnumRequirement` accepts either an enum class-string or a list of cases,
        and compiles them into a regular expression by `preg_quote()`-ing each `->value` and
        joining with `|`. Passing an explicit list restricts the route to those two backing values,
        so any other value fails to match the route and yields a 404 from the router.

        **B** passes a raw class-string as a regular expression: the route would then only match a
        literal path segment spelling the class name. **C** is wrong on two counts — the resolver
        runs *after* routing, and it allows every case of the enum, not a subset. **D** is valid
        syntax but allows **all four** cases, which is not what the question asked for.

        **Official reference:** https://symfony.com/doc/8.0/routing.html#backed-enum-parameters

??? question "Question 23"
    Which statements about the Form `EnumType` are correct? (choose two)

    - A. The `class` option is required and must name an existing enum
    - B. `choices` defaults to `$options['class']::cases()`
    - C. `EnumType` extends `TextType`
    - D. The `class` option accepts any class implementing `Stringable`

    ??? success "Show answer"
        **Correct answer:** A, B

        **Explanation:** `EnumType::configureOptions()` calls `setRequired(['class'])` with
        `setAllowedValues('class', enum_exists(...))`, and defaults `choices` to
        `$options['class']::cases()`. It also derives `choice_label` from each case's `name` (or
        from `TranslatableInterface::trans()` when the enum implements it) and defines
        `choice_value` from `->value` **only for backed enums**.

        **C** is wrong: `getParent()` returns `ChoiceType`, which is why every `ChoiceType` option
        — `expanded`, `multiple`, `placeholder` — is available. **D** is wrong: the allowed-values
        callback is `enum_exists(...)`, so a plain class is rejected even if it is `Stringable`.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Extension/Core/Type/EnumType.php

??? question "Question 24"
    An entity property must persist an enum with Doctrine. Which statement is correct?

    - A. Any enum works; Doctrine stores the case name for pure enums
    - B. Only backed enums can be mapped, using `#[ORM\Column(enumType: Suit::class)]`
    - C. Enums require a custom Doctrine type; there is no built-in option
    - D. `#[ORM\Column(type: Suit::class)]` is the correct mapping

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the `enumType` option of `#[ORM\Column]` binds a column to a PHP enum, and
        the Symfony documentation notes that **only backed enums** may be used for entity
        properties, because Doctrine persists their scalar values.

        **A** contradicts that note — a pure enum has no scalar to store. **C** is wrong: the
        `enumType` option is built in, and writing a custom Doctrine type for this is unnecessary
        work. **D** confuses two different options: `type` selects the *column* type (`string`,
        `integer`, …) while `enumType` names the PHP enum used to hydrate it.

        **Official reference:** https://symfony.com/doc/8.0/doctrine.html#entity-field-types

??? question "Question 25"
    ```php
    #[Route('/orders')]
    public function list(
        #[MapQueryParameter] ?Status $status = null,
    ): Response { /* … */ }
    ```
    A request arrives with `?status=bogus`, where `bogus` is not a valid backing value. What is the
    default outcome?

    - A. `$status` is `null` and the action runs normally
    - B. A 404 response
    - C. A 422 Unprocessable Content response
    - D. A 500 error from an uncaught `\ValueError`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `QueryParameterValueResolver` runs `$type::from($value)` inside a
        `catch (\ValueError)` that turns the failure into `null`, then — because
        `MapQueryParameter::$validationFailedStatusCode` defaults to `Response::HTTP_NOT_FOUND` —
        throws an `HttpException` with that status. So an invalid *query* enum behaves like an
        invalid *route* enum: 404.

        **A** is what you get only by passing `FILTER_NULL_ON_FAILURE` in the attribute's `flags`;
        the nullable type alone governs a **missing** parameter, not an invalid one. **C** is the
        status used by `#[MapRequestPayload]` validation failures, and is available here only by
        setting `validationFailedStatusCode` explicitly. **D** is prevented by the `catch`.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Attribute/MapQueryParameter.php

??? question "Question 26"
    A JSON payload is deserialized into a DTO with a backed-enum property, and the incoming value
    matches no case. What does the Serializer do by default, and how do you change it?

    - A. It sets the property to `null`; there is no option to change that
    - B. It throws `NotNormalizableValueException`; set `BackedEnumNormalizer::ALLOW_INVALID_VALUES` to get `null`
    - C. It falls back to the first case; disable it with `skip_null_values`
    - D. It throws `\ValueError` straight from `from()`, uncaught

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `BackedEnumNormalizer::denormalize()` calls `$type::from($data)` and
        converts `\ValueError`/`\TypeError` into a `NotNormalizableValueException` carrying the
        deserialization path. Passing the context option
        `BackedEnumNormalizer::ALLOW_INVALID_VALUES` makes it return `null` instead — including
        when the payload is neither an `int` nor a `string`.

        **A** inverts the default and denies an option that exists. **C** invents a silent
        fallback; `skip_null_values` is a *normalization* option about omitting `null` properties.
        **D** is wrong about the exception type: the normalizer catches the engine error precisely
        so the Serializer can report a proper violation path.

        **Official reference:** https://symfony.com/doc/8.0/serializer.html

??? question "Question 27"
    A teammate validates a raw string coming from a CSV import against an enum. Which approach is
    the most direct and correct?

    - A. `#[Assert\Type(Suit::class)]` on the raw `string $suit` property
    - B. `#[Assert\Choice(callback: 'validSuitValues')]` where the callback returns `array_column(Suit::cases(), 'value')`
    - C. `#[Assert\Valid]` on the raw string property
    - D. No constraint is needed — PHP validates strings against enums automatically

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the value under validation is still a **string**, so the constraint must
        compare it against the enum's *backing values*. `Choice` accepts a `callback` returning the
        allowed list, and `array_column(Suit::cases(), 'value')` derives that list from the enum
        itself, so adding a case never leaves the validator behind.

        **A** checks `instanceof Suit`, which a string can never satisfy — and the `Type`
        documentation says the constraint is meant for *untyped* values; once the property is typed
        `Suit`, PHP rejects a wrong type before validation runs. **C** cascades validation into a
        nested object and does nothing for a scalar. **D** is only true once the value has actually
        been *converted*: a raw string is not checked against anything until `from()`, `tryFrom()`
        or a type declaration touches it.

        **Official reference:** https://symfony.com/doc/8.0/reference/constraints/Choice.html

---

<small>Back to the lesson: [Enums](enums.md) · [Guided exercises](enums-exercises.md) · [Review flashcards](enums-flashcards.md)</small>

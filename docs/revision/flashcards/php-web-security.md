# Flashcards — PHP & Web Security

46 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. What does the backed-enum method `Suit::tryFrom('X')` return when 'X' is not a valid case?"
    **✅ null**

    tryFrom() returns null for an unknown value; only from() throws a \ValueError. This distinction is a frequent exam trap.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.enumerations.backed.php)

??? question "2. Which statement about the `match` expression is correct?"
    **✅ It compares with === and throws \UnhandledMatchError when nothing matches and there is no default**

    match is strict (===), returns a value, has no fall-through, and errors with \UnhandledMatchError when unmatched without a default arm.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/control-structures.match.php)

??? question "3. In PHP 8.4, what does `public private(set) int $n;` mean?"
    **✅ n can be read from anywhere but written only inside the class**

    Asymmetric visibility (8.4) sets a stricter write scope than read scope; public read, private write.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.visibility.php)

??? question "4. Which is a syntactically valid DNF type declaration?"
    **✅ (Countable&Traversable)|null**

    Disjunctive Normal Form requires each intersection group to be parenthesised and then OR-ed together.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

??? question "5. What does `json_validate($string)` return?"
    **✅ A bool indicating whether the string is valid JSON**

    json_validate() (8.3) only reports validity as a bool, using less memory than json_decode() for large payloads.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.json-validate.php)

??? question "6. Inside a parent factory method, how do `new static()` and `new self()` differ?"
    **✅ static respects the called subclass (late static binding); self is fixed to the defining class**

    Late static binding makes static:: resolve to the runtime class, so new static() returns a subclass instance where new self() would not.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.late-static-bindings.php)

??? question "7. After `$b = clone $a;` where `$a->list` is an object, what is `$b->list`?"
    **✅ The same object as $a->list unless __clone() copies it**

    clone performs a shallow copy; object-typed properties remain shared until __clone() deep-copies them.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.cloning.php)

??? question "8. When is the magic method `__get()` invoked?"
    **✅ Only when reading an inaccessible or undefined property**

    __get() fires only for inaccessible/undefined properties; accessible ones are read directly and isset() uses __isset().

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.overloading.php)

??? question "9. Which cannot be used as a promoted constructor parameter?"
    **✅ private callable $fn**

    callable is not a valid property type, so it cannot be a promoted property.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.decon.php)

??? question "10. Inside `namespace App;`, an unqualified function call `count($x)` resolves to…"
    **✅ App\count if it exists, otherwise the global \count**

    Function and constant calls fall back to the global namespace; class names do not.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.namespaces.rules.php)

??? question "11. What does the statement `use App\Service\Mailer;` do?"
    **✅ Creates a compile-time alias so `Mailer` refers to the FQCN**

    use is a compile-time alias only; the file is loaded later by the autoloader when the class is first used.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.namespaces.importing.php)

??? question "12. Under PSR-4 rule `"App\\": "src/"`, where does `App\Foo\Bar` live?"
    **✅ src/Foo/Bar.php**

    The prefix App\\ maps to src/, so only the remaining segments form the path; PSR-4 is case-sensitive on Linux.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/psr-4/)

??? question "13. Inside `namespace App;`, which correctly references the global DateTimeImmutable class?"
    **✅ new \DateTimeImmutable()**

    Class names do not fall back to the global namespace, so a leading backslash or a use import is required.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.namespaces.rules.php)

??? question "14. A child overrides a method whose parent return type is `Animal`. Which return type is legal?"
    **✅ Cat, a subclass of Animal (covariant return)**

    Return types are covariant, so a child may return a more specific type but never a wider one.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.variance.php)

??? question "15. Intersection types such as `A&B` may combine…"
    **✅ Only class or interface types**

    Intersection types require object (class/interface) types; scalars are not permitted.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

??? question "16. What does `'text' instanceof SomeClass` evaluate to?"
    **✅ false**

    instanceof on a non-object simply returns false; it does not throw.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.operators.type.php)

??? question "17. Can a single class implement two interfaces that declare the same method signature?"
    **✅ Yes, one compatible implementation satisfies both**

    Identical/compatible signatures are not a conflict; a single method implementation fulfils both contracts.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.interfaces.php)

??? question "18. When does `function () use ($x) {}` capture the value of `$x`?"
    **✅ At definition time, by value**

    use captures by value at the moment the closure is defined; prefix with & to capture by reference instead.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.anonymous.php)

??? question "19. Which statement about arrow functions (fn) is true?"
    **✅ They auto-capture the enclosing scope by value**

    Arrow functions auto-capture by value and consist of a single expression; they have no use list and cannot capture by reference.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.arrow.php)

??? question "20. What does `Closure::bind($c, $obj, Foo::class)` return?"
    **✅ A new closure bound to $obj with Foo's scope**

    Closure::bind is static and returns a new closure; the scope argument grants access to Foo's private/protected members.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/closure.bind.php)

??? question "21. What does the expression `trim(...)` produce?"
    **✅ A Closure wrapping the trim function**

    First-class callable syntax (8.1+) creates a Closure from any callable.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.first_class_callable_syntax.php)

??? question "22. A concrete class inherits an abstract method but does not implement it. What happens?"
    **✅ Fatal error unless the class itself is declared abstract**

    Any unimplemented abstract method forces the class to be abstract too.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.abstract.php)

??? question "23. Which feature can an abstract class have that an interface cannot?"
    **✅ Properties and a constructor**

    Abstract classes can hold state and a constructor; interfaces are pure contracts (constants only).

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.interfaces.php)

??? question "24. How many abstract classes can a class extend?"
    **✅ Exactly one**

    PHP has single class inheritance; interfaces provide multiple type inheritance.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.inheritance.php)

??? question "25. A class, its parent, and a used trait all define `run()`. Which implementation is used?"
    **✅ The class's own run()**

    Precedence is class method > trait method > inherited parent method.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "26. Two used traits define the same method and you add no resolution. Result?"
    **✅ Fatal error**

    Unresolved trait method conflicts are a fatal error; resolve them with insteadof and/or as.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "27. A `static` property declared in a trait, used by classes X and Y, is…"
    **✅ Separate per using class (X and Y have independent copies)**

    Static trait state is bound to each using class independently, not shared across all of them.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "28. What does `LoggerTrait::log as protected writeLog;` do?"
    **✅ Aliases the method to writeLog with protected visibility**

    The as operator can rename a trait method and change its visibility at the same time.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "29. Which catch clause catches BOTH a TypeError and a RuntimeException?"
    **✅ catch (\Throwable $e)**

    Throwable is the only common ancestor of both Error (TypeError) and Exception (RuntimeException).

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.throwable.php)

??? question "30. A `return` inside a `finally` block…"
    **✅ Overrides any return or throw from the try block**

    finally always runs last and a return there wins, which is why it is discouraged (it can swallow exceptions).

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.exceptions.php)

??? question "31. What can `set_error_handler()` intercept?"
    **✅ Traditional warnings, notices and deprecations**

    It handles traditional (non-fatal) errors; use set_exception_handler for uncaught exceptions and shutdown functions for fatals.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.set-error-handler.php)

??? question "32. Under `declare(strict_types=1)`, passing a string to an int parameter throws…"
    **✅ TypeError (a subclass of Error)**

    Strict typing rejects the wrong scalar type with a TypeError, which is an Error, not an Exception.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

??? question "33. Which call reliably reports whether an extension is loaded?"
    **✅ extension_loaded('intl')**

    extension_loaded() returns a boolean indicating whether the named module is loaded.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.extension-loaded.php)

??? question "34. For a UTF-8 string, `strlen('é')` returns…"
    **✅ 2 (it counts bytes)**

    strlen counts bytes and 'é' is two bytes in UTF-8; use mb_strlen for a character count.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/book.mbstring.php)

??? question "35. What does the opcache extension cache?"
    **✅ Compiled PHP bytecode in shared memory**

    OPcache stores precompiled script bytecode to skip recompilation on each request; it is not an application data cache.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/book.opcache.php)

??? question "36. How do you make `composer install` fail on a host lacking the intl extension?"
    **✅ Add "ext-intl": "*" to the require section**

    ext-* platform requirements are verified at install time and fail fast when missing.

    :material-book-open-variant: [Docs](https://getcomposer.org/doc/articles/composer-platform-dependencies.md)

??? question "37. Which methods must a class implement to satisfy the Iterator interface?"
    **✅ current, key, next, rewind, valid**

    Iterator defines exactly those five methods; IteratorAggregate needs only getIterator().

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.iterator.php)

??? question "38. Which statement about a generator is true?"
    **✅ It is a single-use Iterator that produces values lazily**

    Generators yield lazily and are consumed once; they cannot be rewound after being iterated.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.generators.php)

??? question "39. Which SPL structure maps data keyed by an object instance?"
    **✅ SplObjectStorage**

    SplObjectStorage keys by object identity and can attach arbitrary data per object.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.splobjectstorage.php)

??? question "40. Enabling `$obj[$key]` array-style access on an object requires implementing…"
    **✅ ArrayAccess**

    ArrayAccess provides offsetGet/Set/Exists/Unset for bracket syntax.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.arrayaccess.php)

??? question "41. For SplPriorityQueue, the ordering among elements of equal priority is…"
    **✅ Unspecified / not stable**

    Equal-priority ordering in SplPriorityQueue is implementation-defined and not stable.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.splpriorityqueue.php)

??? question "42. What is Twig's default defence against XSS?"
    **✅ Context-aware auto-escaping of output variables**

    Twig HTML-escapes variables by default; the |raw filter opts out and reintroduces the risk.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html)

??? question "43. Which technique best prevents SQL injection?"
    **✅ Prepared statements with bound parameters**

    Binding sends data separately from the SQL text, so input can never alter the query structure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "44. Session fixation is primarily mitigated by…"
    **✅ Regenerating the session id on login**

    Migrating to a new session id at authentication invalidates any attacker-planted id. Symfony does this automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "45. Which response header defends against clickjacking?"
    **✅ X-Frame-Options: DENY (or CSP frame-ancestors)**

    X-Frame-Options / CSP frame-ancestors forbid the page from being framed by another site.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "46. What is the correct way to store user passwords?"
    **✅ password_hash() with bcrypt or argon2id**

    Adaptive, salted hashing (bcrypt/argon2id) resists brute-force; the salt is embedded in the hash and verified with password_verify().

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.password-hash.php)

---

<small>Back to [Flashcards](index.md) · [PHP & Web Security](../../php-web-security/index.md)</small>

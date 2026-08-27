# Flashcards — PHP & Web Security

112 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

??? question "1. What does the backed-enum method `Suit::tryFrom('X')` return when 'X' is not a valid case?"
    **✅ null**

    tryFrom() returns null for an unknown value; only from() throws a \ValueError. "false" is wrong because backed enums never coerce to a bool, and "first case" is wrong because there is no implicit default. Internally both call the same lookup but from() escalates a miss to an exception while tryFrom() swallows it. Misconception: developers assume the two are interchangeable — use tryFrom() for untrusted input.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.enumerations.backed.php)

??? question "2. Which statement about the `match` expression is correct?"
    **✅ It compares with === and throws \UnhandledMatchError when nothing matches and there is no default**

    match is strict (===), returns a value, has no fall-through, and errors with \UnhandledMatchError when unmatched without a default arm. The fall-through and loose-comparison options describe switch, not match. "Cannot return a value" is false — match is an expression, unlike the switch statement. Misconception: treating match like a typed switch; the strict comparison means '1' does not match 1.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/control-structures.match.php)

??? question "3. In PHP 8.4, what does `public private(set) int $n;` mean?"
    **✅ n can be read from anywhere but written only inside the class**

    Asymmetric visibility (8.4) sets a stricter write scope than read scope; here read is public, write is private. It is not readonly: readonly blocks writes even internally after the first initialisation, whereas private(set) still allows repeated internal writes. It remains publicly readable, so "invisible outside" is wrong, and it says nothing about static. Misconception: equating private(set) with readonly.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.visibility.php)

??? question "4. Which is a syntactically valid DNF type declaration?"
    **✅ (Countable&Traversable)|null**

    Disjunctive Normal Form requires each intersection group to be parenthesised and then OR-ed together. A bare `A|B&C` mixes the two without parentheses and is a parse error. `?` (nullable sugar) cannot be combined with an intersection, so both `?Countable&Traversable` and `Countable&?Traversable` are invalid. Misconception: that you can sprinkle `?` anywhere; in DNF you write `|null` explicitly outside the group.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

??? question "5. What does `json_validate($string)` return?"
    **✅ A bool indicating whether the string is valid JSON**

    json_validate() (8.3) only reports validity as a bool, using less memory than json_decode() for large payloads because it never materialises the structure. It never returns the decoded array or object — that is json_decode()'s job — and it does not return null on success. Misconception: expecting a decoded value; if you need the data, still call json_decode() afterwards.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.json-validate.php)

??? question "6. True or False: a `readonly` property may declare a default value in its definition."
    **✅ False**

    A readonly property must be typed and cannot have a default; it is initialised exactly once from within the declaring class scope. A default would count as an initialisation the class could never override in the constructor, so PHP forbids it. Misconception: treating readonly like a normal typed property that merely blocks external writes — it also rejects defaults and cannot be static or untyped.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.properties.php)

??? question "7. Given `public float $fahrenheit { get => $this->celsius * 9/5 + 32; }` with `$celsius = 100.0`, what is `$obj->fahrenheit`?"
    **✅ 212.0 — a virtual property computed by the get hook**

    Property hooks (8.4) let a get hook compute a value on read; here it returns 100*9/5+32 = 212.0. There is no backing field for fahrenheit (it is virtual) yet reading it is valid — the hook supplies the value, so neither null nor a TypeError occurs. It returns the computed number, not the raw celsius. Misconception: assuming a hooked property still needs a stored value; a purely virtual property derives it each read.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.property-hooks.php)

??? question "8. How does the nullsafe operator `$a?->b()?->c` behave when `$a` is null?"
    **✅ The whole chain short-circuits and the expression evaluates to null**

    `?->` short-circuits the rest of the chain to null the moment an operand is null, so b() and c are never evaluated. It is not `??`: it does not supply a fallback value, it just stops. It does not throw, and it cannot appear on the left of an assignment. Misconception: confusing `?->` (null-safe method/property access) with `??` (null coalescing) — they solve different problems.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.basic.php)

??? question "9. Which PHP release introduced property hooks and asymmetric visibility?"
    **✅ PHP 8.4**

    Both headline features arrived in 8.4. 8.1 added enums, readonly properties and first-class callables; 8.2 added readonly classes and DNF types; 8.3 added typed class constants, #[\\Override] and json_validate(). The exam probes which version added what. Misconception: dating property hooks to 8.1 alongside readonly — they are three years apart.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/migration84.new-features.php)

??? question "10. Which statements about enums are correct? (choose two)"
    **✅ Enum cases are singletons, so === identity comparison always works ; Enums cannot hold non-constant instance state**

    Cases are singletons so `Suit::Hearts === Suit::Hearts` holds, and enums cannot carry per-instance mutable state (only constants, methods and interfaces). Not every enum is backed — pure enums have cases with no scalar `->value`; only backed enums expose one. Because they are stateless singletons they cannot declare mutable properties. Misconception: adding object-like state to an enum.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.enumerations.php)

??? question "11. What happens at runtime when `Suit::from('Z')` is called and 'Z' is not a valid backing value?"
    **✅ It throws \ValueError**

    from() is the strict lookup: an unknown value throws \\ValueError. That is the mirror image of tryFrom(), which returns null. It never falls back to the first case nor warns-and-returns-false. Best practice: wrap from() in try/catch for untrusted input, or use tryFrom(). Misconception: assuming from() degrades gracefully like tryFrom() — it deliberately fails loud.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.enumerations.backed.php)

??? question "12. You expose a public method and callers use named arguments. Why is renaming a parameter now risky?"
    **✅ The parameter name becomes part of the public API, so renaming it is a BC break**

    With named arguments (8.0) callers write `foo(limit: 10)`, so the parameter identifier is part of your contract; renaming it breaks every named call. Named arguments are the opposite of positional. PHP does not forbid renaming — it simply becomes a semantic BC break. They work on any function/method, not just constructors. Misconception: thinking parameter names are private implementation detail.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.arguments.php)

??? question "13. Inside a parent factory method, how do `new static()` and `new self()` differ?"
    **✅ static respects the called subclass (late static binding); self is fixed to the defining class**

    Late static binding makes static:: resolve to the runtime (called) class, so `new static()` returns a subclass instance where `new self()` always returns the defining class. They are not identical, self does not track the subclass, and only self is resolved at compile time (static is resolved at runtime). Misconception: using self in an inheritable named constructor and wondering why subclasses get the parent type.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.late-static-bindings.php)

??? question "14. After `$b = clone $a;` where `$a->list` is an object, what is `$b->list`?"
    **✅ The same object as $a->list unless __clone() copies it**

    clone performs a shallow copy; object-typed properties remain shared references until __clone() explicitly deep-copies them. It is never an automatic deep copy, it is not nulled, and cloning does not error. Misconception: assuming clone recursively duplicates nested objects — you must implement __clone() to avoid shared mutable state between copies.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.cloning.php)

??? question "15. When is the magic method `__get()` invoked?"
    **✅ Only when reading an inaccessible or undefined property**

    __get() fires only for inaccessible/undefined properties; accessible ones are read directly, so it is not called on every read. Writes trigger __set(), and isset() on an inaccessible property triggers __isset(), not __get(). Misconception: using __get() as a universal accessor — it never runs for a normal public property that exists.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.overloading.php)

??? question "16. Which cannot be used as a promoted constructor parameter?"
    **✅ private callable $fn**

    callable is not a valid property type, so it cannot be a promoted property (a promoted parameter also declares a property). readonly, nullable and array typed parameters with defaults are all valid promotions. Misconception: thinking any parameter type can be promoted — use \\Closure instead of callable when you need to store it as a property.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.decon.php)

??? question "17. `class A { static function f() { return new static(); } } class B extends A {}` — what is `B::f() instanceof B`?"
    **✅ true — new static() resolves to the called class B**

    `new static()` uses late static binding, so calling B::f() constructs a B, making the check true. Had f() used `new self()` it would return an A and the check would be false. Inherited static methods are perfectly legal, so there is no error, and static methods are inherited. Misconception: believing the defining class (A) always wins; the runtime call target drives static::.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.late-static-bindings.php)

??? question "18. True or False: `__toString()` is invoked when you `var_dump()` an object."
    **✅ False**

    var_dump() consults __debugInfo() (if defined), not __toString(). __toString() fires only when the object is used in a string context (echo, concatenation, string casts) and implies the Stringable interface. Misconception: assuming any "display" operation calls __toString() — dump and print_r inspect structure, they do not stringify the object.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.magic.php)

??? question "19. Which magic method handles `isset($obj->missing)` when `missing` is inaccessible?"
    **✅ __isset()**

    isset()/empty() on an inaccessible or undefined property route through __isset(); the engine does not call __get() for the existence check. __call() handles inaccessible method calls and __invoke() handles using an object as a function. Misconception: expecting __get() to fire for isset() — that would force materialising the value, which is why a dedicated __isset() hook exists.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.overloading.php)

??? question "20. True or False: a child class can directly access `private` members declared on its parent."
    **✅ False**

    private restricts access to the declaring class only; a subclass cannot see a parent's private members. Use protected to expose members to subclasses. Misconception: treating private and protected as interchangeable — protected = class + subclasses, private = declaring class only, even within the same hierarchy.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.visibility.php)

??? question "21. A named constructor `Model::create()` uses `return new self();`. Subclass calls `User::create()` but gets a Model, not a User. What is the fix?"
    **✅ Replace `new self()` with `new static()` to honour late static binding**

    self is bound at compile time to the defining class (Model), so it always builds a Model. new static() resolves to the runtime call target (User), fixing the factory. final only prevents overriding and would not change the instantiated type; a `self` return type would actually worsen it by declaring the wrong type; overriding in every subclass is boilerplate the LSB approach avoids. Misconception: that return types influence which class is instantiated.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.late-static-bindings.php)

??? question "22. Which features does constructor property promotion support?"
    **✅ Visibility, readonly, types, defaults and attributes**

    A promoted parameter both declares and assigns the property and may carry visibility, readonly, a type, a default and attributes. It works only in __construct (not arbitrary methods), requires a valid property type (callable is not one), and untyped/public-only is not a limitation. Misconception: thinking promotion is a stripped-down shortcut — it is the full property declaration inline.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.decon.php)

??? question "23. Inside `namespace App;`, an unqualified function call `count($x)` resolves to…"
    **✅ App\count if it exists, otherwise the global \count**

    Unqualified function and constant calls try the current namespace first, then fall back to the global namespace — so a local App\\count would win, else \\count runs. It is never "always App\\count" nor a fatal error, and the global-only option ignores the local-first rule. This fallback is exactly why \\count() micro-optimises the lookup. Misconception: assuming the fallback also applies to class names — it does not.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.namespaces.rules.php)

??? question "24. What does the statement `use App\Service\Mailer;` do?"
    **✅ Creates a compile-time alias so `Mailer` refers to the FQCN**

    use is a pure compile-time alias; it neither loads a file, instantiates, nor registers a loader. The file is only required later by the autoloader when the class is first referenced at runtime. Misconception: believing use triggers I/O — it is resolved entirely by the compiler and costs nothing at runtime.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.namespaces.importing.php)

??? question "25. Under PSR-4 rule mapping prefix `App\` to `src/`, where does `App\Foo\Bar` live?"
    **✅ src/Foo/Bar.php**

    PSR-4 strips the mapped prefix (App\\), replaces \\ with /, and appends .php, giving src/Foo/Bar.php. The App segment is not repeated under src/, the mapping is case-sensitive on Linux (so lowercase is wrong), and the src/ base directory is mandatory. Misconception: keeping the prefix in the path — the prefix maps to the base dir and disappears from it.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/psr-4/)

??? question "26. Inside `namespace App;`, which correctly references the global DateTimeImmutable class?"
    **✅ new \DateTimeImmutable()**

    Class names do not fall back to the global namespace, so an unqualified `new DateTimeImmutable()` looks for App\\DateTimeImmutable and fails; you need a leading backslash or a use import. App\\DateTimeImmutable does not exist, and `global\\` is not valid syntax. Misconception: assuming the function/constant global fallback also covers classes — it never does.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.namespaces.rules.php)

??? question "27. A composer.json maps the PSR-4 prefix `App\` to `src/`. Where is `App\Repository\UserRepository` autoloaded from?"
    **✅ src/Repository/UserRepository.php**

    Composer strips the App\\ prefix (mapped to src/), converts remaining separators to directories and appends .php, yielding src/Repository/UserRepository.php. The prefix is not duplicated under src/, application code is not under vendor/ (that is for third-party packages), and the base dir is src/ not app/. Misconception: expecting the namespace root folder to appear inside the base directory.

    :material-book-open-variant: [Docs](https://getcomposer.org/doc/04-schema.md#psr-4)

??? question "28. True or False: `use App\Foo;` also imports the sub-namespace class `App\Foo\Bar`."
    **✅ False**

    A use statement imports exactly one name (here Foo). To use Bar you write `use App\\Foo\\Bar;` or reference it as `Foo\\Bar` after importing Foo. Imports are not recursive over sub-namespaces. Misconception: thinking use brings in a whole namespace tree — it aliases a single symbol; grouped imports `use App\\Foo\\{Bar, Baz};` list each explicitly.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.namespaces.importing.php)

??? question "29. What does `composer dump-autoload --optimize` produce for production?"
    **✅ A static classmap so no per-class filesystem stat is needed**

    --optimize converts PSR-4 rules into an explicit class-to-file map, so the loader looks up a path in an array instead of probing the filesystem — faster in production. It does not minify sources, does not build a service container (that is Symfony's job), and PSR-4 still works as a fallback for classes not in the map (unless --classmap-authoritative). Misconception: confusing autoload optimisation with application caching.

    :material-book-open-variant: [Docs](https://getcomposer.org/doc/articles/autoloader-optimization.md)

??? question "30. Inside `namespace App;` you write `new DateTime()` with no import. What happens?"
    **✅ A fatal Error: class App\DateTime not found**

    Unqualified class names resolve only against the current namespace and use imports — there is no global fallback for classes — so PHP looks for App\\DateTime and throws a not-found Error. It does not silently use the global class, there is no deprecation path, and it parses fine (the error is at resolution/runtime). Fix with `new \\DateTime()` or `use DateTime;`. Misconception: expecting the function-style global fallback for classes.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.namespaces.rules.php)

??? question "31. What does `use function App\Support\slugify;` at the top of a file do?"
    **✅ Aliases the namespaced function so you can call slugify() unqualified**

    `use function` imports a namespaced function so it can be called unqualified; likewise `use const` imports constants. It does not import a class (that is a plain use), it does not define anything, and function imports are entirely valid. Misconception: believing use only works for classes — the function and const forms exist precisely because of the global fallback rules.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.namespaces.importing.php)

??? question "32. A child overrides a method whose parent return type is `Animal`. Which return type is legal?"
    **✅ Cat, a subclass of Animal (covariant return)**

    Return types are covariant, so a child may return a more specific (narrower) type such as Cat, but never a wider one. object and mixed are both wider than Animal and would break substitutability, and adding an unrelated union member also widens the return. Misconception: reversing the rule — parameters (not returns) are the ones that may widen.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.variance.php)

??? question "33. Intersection types such as `A&B` may combine…"
    **✅ Only class or interface types**

    Intersection types require object (class/interface) types, because a value must satisfy all members simultaneously — a scalar cannot be two class types at once. Scalars and enum-only restrictions are therefore wrong. Misconception: writing `int&string`, which is meaningless and a compile error; use unions for alternatives among scalars.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

??? question "34. What does `'text' instanceof SomeClass` evaluate to?"
    **✅ false**

    instanceof on a non-object simply returns false; it never throws and never returns null or true for a string. This makes it safe to use as a guard without first checking is_object(). Misconception: assuming instanceof errors on scalars — it is deliberately total, returning false for anything that is not an instance.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.operators.type.php)

??? question "35. Can a single class implement two interfaces that declare the same method signature?"
    **✅ Yes, one compatible implementation satisfies both**

    Identical or compatible signatures are not a conflict; a single method body fulfils both contracts. It is not always a conflict, insteadof is a trait mechanism (not for interfaces), and it applies to instance methods too. Misconception: importing the trait-collision rules into interfaces — interfaces only demand a compatible signature, they carry no bodies to clash.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.interfaces.php)

??? question "36. A parent method is `handle(Cat $c)`. Which override signature is legal under contravariance?"
    **✅ handle(Animal $c) — widening the parameter is allowed**

    Parameter types are contravariant: a child may accept a wider (more general) type such as Animal, preserving substitutability. Narrowing to Kitten would reject values the parent accepted (illegal), an unrelated type breaks the contract, and dropping a required parameter changes arity. Misconception: applying the covariant (narrowing) rule to parameters — returns narrow, parameters widen.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.variance.php)

??? question "37. True or False: an interface may declare (non-constant) properties."
    **✅ False**

    Interfaces are pure contracts: they may declare method signatures and constants (typed since 8.3) but never properties, because they carry no state. If you need shared state, use an abstract class. Misconception: treating an interface like an abstract class — only abstract classes hold properties and a constructor.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.interfaces.php)

??? question "38. A parent declares `serialize(): string`. Is overriding it with `serialize(): never` legal?"
    **✅ Yes — never is the bottom type and is a valid covariant return**

    never is the bottom type: a method that always throws or exits satisfies any return contract, so `: never` is a valid covariant narrowing of `: string`. never is not unrelated (it is a subtype of every type), it is not restricted to void methods, and the parent need not also return never. Misconception: thinking never only marks infinite loops/exit; it is a genuine type in the variance lattice.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

??? question "39. What does the type declaration `(Countable&Traversable)|null` require of an argument?"
    **✅ An object implementing both Countable and Traversable, or null**

    A DNF type groups the intersection: the value must implement both interfaces (the & group) OR be null. "Either/or" describes a plain union, which this is not inside the parentheses. Scalars cannot satisfy an interface intersection, and it clearly accepts non-null objects too. Misconception: reading the | as applying to each interface individually rather than to the whole parenthesised group.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

??? question "40. Which statements about interfaces are correct? (choose two)"
    **✅ An interface may extend several parent interfaces ; Interface constants may be typed since PHP 8.3**

    Interfaces support multiple `extends` (multiple inheritance of type) and, since 8.3, typed constants. They never carry method bodies (that is a trait/abstract class feature — PHP has no default interface methods), and a class may implement many interfaces. Misconception: importing "default methods" from other languages — PHP interfaces are body-less.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.interfaces.php)

??? question "41. An interface declares `const string VERSION`. An implementing class overrides it with `const int VERSION = 8;`. What happens?"
    **✅ A fatal error — the overriding constant must keep a compatible (string) type**

    Typed class constants (8.3) enforce the declared type on overrides, so redeclaring a string constant as int is a fatal type error. Types are not advisory, there is no silent coercion of the constant value, and it is a hard error, not a deprecation. Misconception: assuming interface constants can be freely overridden — untyped ones can vary in value, but a typed constant pins the type.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.constants.php)

??? question "42. When does `function () use ($x) {}` capture the value of `$x`?"
    **✅ At definition time, by value**

    use captures by value at the moment the closure is defined, taking a snapshot; it is not captured at call time and does not track the live variable. To share and observe later mutations, capture by reference with `use (&$x)`. Misconception: expecting a closure to see a variable's value as it is when the closure runs — the value is frozen at definition.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.anonymous.php)

??? question "43. Which statement about arrow functions (fn) is true?"
    **✅ They auto-capture the enclosing scope by value**

    Arrow functions auto-capture used outer variables by value and consist of a single expression. They have no use list (that is what "auto" means), cannot capture by reference, and cannot hold multiple statements — use a full closure for that. Misconception: expecting fn to behave like a full closure with `use (&...)`; it is deliberately restricted.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.arrow.php)

??? question "44. What does `Closure::bind($c, $obj, Foo::class)` return?"
    **✅ A new closure bound to $obj with Foo's scope**

    Closure::bind is static and returns a new closure; the original $c is unchanged (closures are immutable in their binding). The scope argument (Foo::class) grants access to Foo's private/protected members. It does not invoke the closure or produce a string. Misconception: thinking bind mutates the closure in place — always assign the returned closure.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/closure.bind.php)

??? question "45. What does the expression `trim(...)` produce?"
    **✅ A Closure wrapping the trim function**

    First-class callable syntax (8.1+) turns any callable into a Closure, so trim(...) yields a Closure object. It is not the string 'trim', it does not call trim (no argument is passed), and it is valid syntax in 8.4. It is the type-safe modern replacement for 'trim' or Closure::fromCallable('trim'). Misconception: reading `(...)` as an immediate call.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.first_class_callable_syntax.php)

??? question "46. `$base=10; $v=fn($n)=>$n+$base; $r=function($n)use(&$base){return $n+$base;}; $base=100;` — what are `$v(1)` and `$r(1)`?"
    **✅ 11 and 101**

    The arrow function captured $base by value at definition (10), so $v(1)=11 regardless of the later reassignment. The full closure captured by reference (&$base), so it sees $base=100 and returns 101. Both-101 ignores the by-value snapshot; both-11 ignores the reference; the last option swaps them. Misconception: assuming fn tracks later mutations — only `use (&$x)` does.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.arrow.php)

??? question "47. A closure reads `$this->secret` (a private property). What determines whether that access succeeds?"
    **✅ The closure's bound scope, set at creation or via bindTo/bind**

    A closure's access to private/protected members depends on its scope, fixed when it is created (inside a method) or reassigned via bindTo/bind/call — not on where it is later called. readonly governs writes, not read access, and the caller's own visibility is irrelevant. Misconception: thinking private access is decided at the call site — it is the closure's scope that matters.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/closure.bindto.php)

??? question "48. How do `Closure::bind`, `$c->bindTo` and `$c->call` differ?"
    **✅ bind (static) and bindTo (instance) return a new bound closure; call binds and invokes in one step**

    bind is the static form and bindTo the instance form; both return a fresh bound closure without calling it. call binds a new $this and scope and invokes immediately, returning the result. Only call runs the closure, none mutate the original (closures are immutable in their binding), and call does not return an un-invoked closure. Misconception: expecting bindTo to also execute — it only rebinds.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/closure.call.php)

??? question "49. True or False: an arrow function can capture an outer variable by reference."
    **✅ False**

    Arrow functions always auto-capture by value and have no mechanism for by-reference capture (no use list, no `&`). If you need a reference, use a full closure with `use (&$x)`. Misconception: assuming fn is just shorter syntax with the same power — it is intentionally limited to by-value, single-expression bodies.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.arrow.php)

??? question "50. `$reader = fn () => $this->secret; $bound = Closure::bind($reader, new Box(), Box::class); echo $bound();` where Box has `private $secret='hidden'`. Output?"
    **✅ hidden**

    Passing Box::class as the scope grants the rebound closure access to Box's private property, so it prints "hidden". Without the scope argument the private read would fail — but here it is supplied, so no Error, no null, no empty string. Misconception: thinking $this alone grants access; you must also pass the scope to unlock private/protected members.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/closure.bind.php)

??? question "51. A closure captures `use ($id)` when $id='A', then $id is set to 'B' before the closure runs. What does it see?"
    **✅ 'A' — the value snapshotted at definition time**

    `use ($id)` captures by value when the closure is defined, so it keeps 'A' even though $id later becomes 'B'. To observe the update you would capture by reference `use (&$id)`. Captured variables are not reset to null, and reassigning the outer variable never throws. Misconception: treating use like a live binding rather than a snapshot.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.anonymous.php)

??? question "52. A concrete class inherits an abstract method but does not implement it. What happens?"
    **✅ Fatal error unless the class itself is declared abstract**

    Any unimplemented abstract method forces the class to be abstract too; otherwise PHP raises a fatal error. It never silently returns null or runs normally, and it is a hard error not a deprecation. Misconception: assuming an unimplemented abstract method is merely optional — a concrete class must implement every inherited abstract method.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.abstract.php)

??? question "53. Which feature can an abstract class have that an interface cannot?"
    **✅ Properties and a constructor**

    Abstract classes can hold state (properties) and a constructor; interfaces are pure contracts and can hold neither. Neither supports multiple parents (only interfaces allow multiple extends of interfaces), both can declare public method signatures, and both can hold constants. Misconception: thinking abstract classes are just interfaces with bodies — they add state and construction.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.interfaces.php)

??? question "54. How many abstract classes can a class extend?"
    **✅ Exactly one**

    PHP has single class inheritance, so a class extends exactly one class (abstract or not). Interfaces provide multiple type inheritance instead. "Zero" is wrong for a class that does extend one, and "two" contradicts single inheritance. Misconception: hoping abstract classes offer multiple inheritance — they do not; compose or use interfaces/traits.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.inheritance.php)

??? question "55. `abstract class A {} new A();` — what does this produce?"
    **✅ A fatal Error: Cannot instantiate abstract class A**

    Abstract classes cannot be instantiated directly; `new A()` throws a fatal Error at runtime. It does not create an instance or return null, and it parses fine (the failure is at instantiation). Instantiate a concrete subclass instead. Misconception: thinking an abstract class with no abstract methods can still be new-ed — the abstract keyword alone blocks it.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.abstract.php)

??? question "56. In the template method pattern, why is the public skeleton method often marked `final`?"
    **✅ To stop subclasses overriding the algorithm skeleton, restricting them to the abstract hooks**

    The template method fixes the invariant algorithm and defers only the variable steps to abstract hooks; marking it final protects those invariants from being overridden. It does the opposite of allowing full replacement; abstract methods cannot be final (they must be overridden); and final has nothing to do with instantiability. Misconception: leaving the skeleton overridable, which lets subclasses break the pattern.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.abstract.php)

??? question "57. True or False: declaring `abstract public function run(): void {}` (with a body) is valid."
    **✅ False**

    An abstract method declares a signature only and must not have a body; adding `{}` is a parse error. If you want a default body, drop abstract and make it a concrete (optionally overridable) method. Misconception: confusing an abstract method (no body, must be implemented) with a concrete method that happens to be empty.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.abstract.php)

??? question "58. `abstract class Exporter { abstract protected function format(array $d): string; final public function export(array $d): string { return 'BEGIN'.$this->format($d).'END'; } }` — what role does export() play?"
    **✅ It is the template method: a fixed skeleton calling the abstract hook format()**

    export() is a concrete, final template method that defines the fixed wrapping and defers the variable step to the abstract format() hook — a textbook template method. It is not itself abstract (it has a body), not a factory, and calling an abstract method from a concrete one is perfectly legal because concrete subclasses supply format(). Misconception: thinking you cannot call an abstract method internally.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.abstract.php)

??? question "59. You need several unrelated classes to share only a contract (no state, and some already extend other classes). Which do you choose?"
    **✅ An interface — it needs no state and allows multiple type inheritance**

    An interface fits: no shared state is needed and classes can implement many interfaces even while extending another class. An abstract class would consume the single inheritance slot some classes already use. A trait is not a type (cannot be type-hinted). A final class cannot be extended at all. Misconception: reaching for an abstract class by default when only a contract is required.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.interfaces.php)

??? question "60. Which statements about abstract classes are correct? (choose two)"
    **✅ A single abstract method forces the whole class to be abstract ; An overriding method must obey variance rules (covariant return, contravariant params)**

    One abstract method makes the class abstract, and implementations of an abstract method must respect variance just like interface/parent overrides. Abstract classes can define constructors (called via parent::__construct in subclasses), and the abstract keyword blocks instantiation regardless of whether abstract methods exist. Misconception: thinking a body-less-method count or constructor presence changes instantiability.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.abstract.php)

??? question "61. A class, its parent, and a used trait all define `run()`. Which implementation is used?"
    **✅ The class's own run()**

    Precedence is class method > trait method > inherited parent method, so the class's own run() wins. The trait would only win over the inherited parent (not over the class itself), the parent is lowest priority, and this is not an error because there is a clear winner. Misconception: assuming a trait overrides everything — it overrides the parent but not the using class's own method.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "62. Two used traits define the same method and you add no resolution. Result?"
    **✅ Fatal error**

    Unresolved trait method collisions are a fatal error; PHP does not pick first or last, and it never chains both. Resolve with `insteadof` (choose one) and optionally `as` (alias the other). Misconception: expecting a silent ordering rule like some languages — PHP forces explicit resolution.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "63. A `static` property declared in a trait, used by classes X and Y, is…"
    **✅ Separate per using class (X and Y have independent copies)**

    Traits are copied into each using class at compile time, so a static property becomes a distinct static of X and of Y — not shared across them. Static trait members are legal and not implicitly read-only. Misconception: treating the trait as a single shared owner of the static state; the trait is a template, not a runtime container.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "64. What does `LoggerTrait::log as protected writeLog;` do?"
    **✅ Aliases the method to writeLog with protected visibility**

    The `as` operator can rename a trait method and change its visibility at once, creating protected writeLog. The original log remains available (it is not deleted), and as never changes a method to abstract or static. Misconception: thinking `as` replaces the original — it adds an alias; use `insteadof` to exclude a colliding version.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "65. Traits A and B both define `init()`. You want A's version kept and B's exposed as `initLegacy()`. Which resolution is correct?"
    **✅ use A, B { A::init insteadof B; B::init as initLegacy; }**

    insteadof selects A::init as the surviving init(), and as aliases the excluded B::init to initLegacy — exactly matching the requirement. The second option keeps B (wrong version). The third has invalid syntax mixing as and insteadof in one clause. The fourth lacks the trait qualifiers insteadof requires. Misconception: believing as alone resolves a collision — you still need insteadof to pick the winner.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "66. Why can you not write a type hint `function f(MyTrait $x)`?"
    **✅ A trait is not a type; it is copied into classes and cannot be type-hinted or used with instanceof**

    Traits provide horizontal code reuse but are not types, so they cannot appear in a type declaration or instanceof check. There is no trait hinting keyword, no "abstract trait" exception, and no static-only allowance. Pair a trait with an interface when callers need a type. Misconception: treating a trait like an interface — only the interface is the contract/type.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "67. What does declaring an `abstract` method inside a trait accomplish?"
    **✅ It forces the using class to implement that method**

    An abstract trait method imposes a contract on the using class, which must provide an implementation — like an interface method but copied in. Traits are never instantiable, abstract is fully honoured inside traits, and an abstract method has no body. Misconception: assuming traits can only supply concrete methods — they can also demand methods from the host class.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "68. True or False: a trait can be instantiated directly with `new`."
    **✅ False**

    A trait is a compile-time code-reuse template, not a class or a type, so it cannot be instantiated; only a class that `use`s the trait can be. This is why traits are neither types nor objects. Misconception: viewing a trait as a lightweight class — it has no independent existence at runtime.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "69. What does `FileLogger::log as protected;` (no new name) do?"
    **✅ Changes the visibility of log() to protected without renaming it**

    `as` can be used purely to change visibility when no new name follows, so log() becomes protected but keeps its name. It is not an anonymous alias, does not remove the method, and does not make it abstract. Misconception: thinking as always renames — the alias name is optional, leaving only a visibility change.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "70. A class defines `save()`, and a trait it uses also defines `save()`. A developer expects the trait's version to run but gets the class's. Why?"
    **✅ The class's own method takes precedence over any trait method**

    Trait precedence is class > trait > inherited parent, so the class's own save() always overrides the trait's. This is defined, expected behaviour, not a bug or error. To use the trait's version, alias it with `as` (e.g. `Trait::save as saveViaTrait;`). Misconception: assuming a trait method overrides the host class's own method — it only overrides inherited ones.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

??? question "71. Which catch clause catches BOTH a TypeError and a RuntimeException?"
    **✅ catch (\Throwable $e)**

    Throwable is the only common ancestor of both Error (TypeError) and Exception (RuntimeException). catch(\\Exception) misses the TypeError, catch(\\Error) misses the RuntimeException, and LogicException catches neither. Misconception: assuming \\Exception is the root of everything — it is not; \\Throwable is.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.throwable.php)

??? question "72. A `return` inside a `finally` block…"
    **✅ Overrides any return or throw from the try block**

    finally always runs last, and a return there wins — it overrides both a return and a pending throw from try, which is why it can silently swallow exceptions and is discouraged. It is valid syntax, never ignored, and finally runs after try, not before. Misconception: thinking finally is just cleanup that cannot alter the result — a return in it changes the outcome.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.exceptions.php)

??? question "73. What can `set_error_handler()` intercept?"
    **✅ Traditional warnings, notices and deprecations**

    It handles traditional (non-fatal) engine errors like warnings/notices/ deprecations, often converting them to ErrorException. Uncaught exceptions go to set_exception_handler, and fatal E_ERROR/parse errors are caught via register_shutdown_function + error_get_last, not the error handler. Misconception: expecting one handler for both errors and exceptions — they are separate mechanisms.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.set-error-handler.php)

??? question "74. Under `declare(strict_types=1)`, passing a string to an int parameter throws…"
    **✅ TypeError (a subclass of Error)**

    Strict typing rejects the wrong scalar type with a TypeError, which extends Error (not Exception). It is not InvalidArgumentException (an application Exception you throw yourself), not a mere warning, and not ValueError (which signals a correctly-typed but out-of-range value). Misconception: expecting catch(\\Exception) to catch it — it is an Error, so use \\Throwable.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

??? question "75. True or False: `catch (\Exception $e)` will catch a `TypeError`."
    **✅ False**

    TypeError extends Error, and Error is a separate branch from Exception under Throwable, so catch(\\Exception) never catches it. To catch both branches use catch(\\Throwable). Misconception: believing Exception is the universal base type — Throwable is the interface both Error and Exception implement.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.throwable.php)

??? question "76. `try { intdiv(1, 0); } catch (\Exception $e) { echo 'caught'; }` — what happens?"
    **✅ The DivisionByZeroError is uncaught and the script fails**

    intdiv(1, 0) throws DivisionByZeroError, which extends ArithmeticError → Error, not Exception — so the catch(\\Exception) block does not match and the error propagates uncaught. It does not print 'caught', does not return 0, and modern PHP throws rather than warning. Fix by catching \\DivisionByZeroError or \\Throwable. Misconception: assuming division errors are Exceptions.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.divisionbyzeroerror.php)

??? question "77. In the Throwable hierarchy, which chain is correct?"
    **✅ DivisionByZeroError → ArithmeticError → Error → Throwable**

    DivisionByZeroError extends ArithmeticError, which extends Error, which implements Throwable. The engine-fault classes (TypeError, ValueError, ArithmeticError) live under Error, never under Exception — so the other chains, which route them through Exception/RuntimeException/LogicException, are wrong. Misconception: mixing the Error and Exception branches; they share only the Throwable interface.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.throwable.php)

??? question "78. Does the `@` error-suppression operator stop a thrown exception from propagating?"
    **✅ No — @ only mutes traditional errors/warnings, not thrown exceptions**

    @ suppresses the reporting of traditional errors (warnings/notices); a thrown exception still propagates and must be caught with try/catch. It does not swallow exceptions, does not special-case Error subclasses, and its behaviour is not tied to try blocks. Misconception: using @ as a catch-all — it only affects the legacy error-reporting path.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.operators.errorcontrol.php)

??? question "79. Which of these are `Error` subclasses rather than `Exception` subclasses? (choose two)"
    **✅ TypeError ; ValueError**

    TypeError and ValueError extend Error (engine-level faults). RuntimeException and JsonException extend Exception (application-level conditions). The two branches meet only at the Throwable interface. Misconception: grouping ValueError with the application exceptions because it sounds like a validation issue — it is an Error thrown by the engine for out-of-range values.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/reserved.exceptions.php)

??? question "80. You catch a JsonException and rethrow with `throw new RuntimeException('Bad', previous: $e);`. Why pass `previous`?"
    **✅ To preserve the root cause and its stack trace, retrievable via getPrevious()**

    Passing the original as previous chains the exceptions, keeping the root cause and its trace accessible through getPrevious() — vital for debugging. It is optional, not required syntax; it does not suppress the original (it retains it) nor auto-merge messages. Misconception: discarding the caught exception when wrapping, which loses the original diagnostic trail.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/exception.getprevious.php)

??? question "81. Which call reliably reports whether an extension is loaded?"
    **✅ extension_loaded('intl')**

    extension_loaded() returns a bool indicating whether the named module is loaded. include expects a file path (not a module), require_extension() is not a real function, and ini_get() reads an INI directive, not module presence. Misconception: guessing at helper names — the canonical runtime check is extension_loaded(), with function_exists()/class_exists() for specific symbols.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.extension-loaded.php)

??? question "82. For a UTF-8 string, `strlen('é')` returns…"
    **✅ 2 (it counts bytes)**

    strlen counts bytes, and 'é' is two bytes in UTF-8, so it returns 2. It is not 1 (that would be the character count via mb_strlen), not 0, and not 4. Use mb_strlen($s, 'UTF-8') for a character count. Misconception: assuming strlen is character-aware — it is byte-based, which breaks length checks on non-ASCII input.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/book.mbstring.php)

??? question "83. What does the opcache extension cache?"
    **✅ Compiled PHP bytecode in shared memory**

    OPcache stores precompiled script bytecode in shared memory to skip recompilation on every request — the biggest production speedup. It is not an application data cache: query results, HTTP responses and rendered templates are cached by other layers. Misconception: treating OPcache as a general cache; it caches only opcodes, not your data.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/book.opcache.php)

??? question "84. How do you make `composer install` fail on a host lacking the intl extension?"
    **✅ Add "ext-intl": "*" to the require section**

    ext-* platform requirements in require are verified at install time and fail fast when the extension is missing. autoload is for class maps, not platform gating; an env var does not enforce it; and Composer does not auto-require extensions your code happens to use. Misconception: expecting Composer to infer extension needs — you must declare them explicitly.

    :material-book-open-variant: [Docs](https://getcomposer.org/doc/articles/composer-platform-dependencies.md)

??? question "85. What is the classic gotcha with `ctype_digit(123)` (passing an integer)?"
    **✅ Small integers are interpreted as ASCII codes, not their digits, giving surprising results**

    ctype functions treat an int argument in the range -128..255 as an ASCII character code, so ctype_digit(123) checks character code 123 ('{'), not the digits "123" — a false negative. It does not always return true, does not throw, and does not stringify (that is exactly the assumption that bites you). Pass strings: ctype_digit('123') is true. Misconception: assuming numeric arguments are auto-cast to their textual form.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.ctype-digit.php)

??? question "86. In composer.json, what does a `require` block listing `ext-mbstring`, `ext-intl`, `ext-ctype` enforce?"
    **✅ install/update fails on any host missing those extensions**

    Listing ext-* under require makes them platform requirements checked at install/update time, failing fast if absent. Composer cannot download or compile C extensions (they must exist on the host); the requirement is not dev-only; and it does not disable polyfills (polyfills are separate packages). Misconception: expecting Composer to provide the extension — ext-* only gates, it does not install.

    :material-book-open-variant: [Docs](https://getcomposer.org/doc/articles/composer-platform-dependencies.md)

??? question "87. What do `strlen('café')` and `mb_strlen('café', 'UTF-8')` return respectively?"
    **✅ 5 and 4**

    strlen counts bytes: 'é' is 2 bytes in UTF-8, so 'café' is 5 bytes. mb_strlen counts characters, giving 4. The other options assume both count the same way, which is the exact trap. Use mb_* for user-facing length checks. Misconception: believing strlen and mb_strlen are interchangeable on non-ASCII text.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.mb-strlen.php)

??? question "88. True or False: OPcache can be used as a cache for application data such as query results."
    **✅ False**

    OPcache caches only compiled bytecode (opcodes) in shared memory; it is not an application data store. For query results or computed values use a cache layer (APCu, Redis, Symfony Cache). Misconception: conflating the bytecode cache with a key/value data cache because both are "caches".

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/book.opcache.php)

??? question "89. You deploy a code change to a server running `opcache.validate_timestamps=0` but forget to reset OPcache. What do requests serve?"
    **✅ The stale, previously-cached bytecode — OPcache never notices the file changed**

    With validate_timestamps=0, OPcache trusts its cached bytecode unconditionally and never stats the source file to check for changes. Forgetting to reset/clear OPcache (or restart PHP-FPM) after a deploy means every request keeps serving the OLD compiled code indefinitely, silently, with no error — exactly why the setting is only safe for immutable deploys that reset OPcache as part of the release step.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/opcache.configuration.php)

??? question "90. Which methods must a class implement to satisfy the Iterator interface?"
    **✅ current, key, next, rewind, valid**

    Iterator defines exactly those five methods. getIterator() belongs to IteratorAggregate; count/offsetGet belong to Countable/ArrayAccess; and there is no prev() in the contract. Misconception: mixing Iterator with IteratorAggregate — the latter needs only getIterator(), which usually returns a generator.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.iterator.php)

??? question "91. Which statement about a generator is true?"
    **✅ It is a single-use Iterator that produces values lazily**

    A generator yields values lazily one at a time and is a built-in Iterator, but it is single-use: once consumed it cannot be rewound. It never materialises the whole sequence (that is its memory advantage) and does not implement ArrayAccess. Misconception: iterating a generator twice and expecting values the second time — it is exhausted.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.generators.php)

??? question "92. Which SPL structure maps data keyed by an object instance?"
    **✅ SplObjectStorage**

    SplObjectStorage keys by object identity (spl_object_id) and can attach arbitrary data per object. SplStack (LIFO), SplQueue (FIFO) and SplFixedArray (integer-indexed) are not object-keyed maps. It is ideal for "have I seen this instance?" without polluting the object. Misconception: trying to use an object as a plain array key, which is illegal.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.splobjectstorage.php)

??? question "93. Enabling `$obj[$key]` array-style access on an object requires implementing…"
    **✅ ArrayAccess**

    ArrayAccess provides offsetGet/offsetSet/offsetExists/offsetUnset for bracket syntax. Countable enables count(), Iterator enables foreach, and Stringable enables string casting — none give bracket access. Misconception: assuming one collection interface covers all behaviours; each native behaviour has its own interface.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.arrayaccess.php)

??? question "94. For SplPriorityQueue, the ordering among elements of equal priority is…"
    **✅ Unspecified / not stable**

    Equal-priority ordering in SplPriorityQueue is implementation-defined and not stable, so you cannot rely on FIFO, LIFO or alphabetical order among ties. If insertion order matters for equal priorities, encode it into the priority yourself. Misconception: assuming a heap preserves insertion order for equal keys — heaps are not stable sorts.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.splpriorityqueue.php)

??? question "95. Why can you not implement `Traversable` directly, and what does `IteratorAggregate::getIterator()` return?"
    **✅ Traversable is an internal marker interface; getIterator() must return a Traversable (e.g. an Iterator or generator)**

    Traversable is an engine-internal marker (the base of Iterator and IteratorAggregate) that userland cannot implement directly — you implement one of its children. getIterator() must return a Traversable, commonly an Iterator or a generator (via yield). It does not return a plain array, void, or a Countable. Misconception: trying to `implements Traversable` directly, which is a fatal error.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.traversable.php)

??? question "96. A generator is iterated once in a foreach, then a second foreach runs over the same generator. What does the second loop yield?"
    **✅ Nothing — the generator is already consumed and cannot rewind**

    A generator is single-use; after the first iteration it is exhausted and a second foreach yields nothing (attempting to rewind an already-started generator would itself error, but simply continuing produces no values). It does not restart or reverse. Wrap the source in an IteratorAggregate that returns a fresh generator each time if you need re-iteration. Misconception: treating a generator like an array you can loop repeatedly.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.generators.php)

??? question "97. Calling `count($obj)` on a plain object that does not implement Countable results in…"
    **✅ A TypeError — count() requires an array or a Countable**

    Since PHP 8.0, count() on a non-countable throws a TypeError; older versions only warned and returned 1. It does not count properties, does not return 1, and does not return 0. Implement Countable (a count() method) to make count() work on your object. Misconception: relying on the legacy "returns 1" behaviour, which is now a hard error.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.countable.php)

??? question "98. True or False: a plain PHP array can use an object as a key."
    **✅ False**

    Array keys may only be integers or strings, so objects cannot be array keys — attempting it raises an error. Use SplObjectStorage (or a WeakMap) when you need to key data by an object instance. Misconception: expecting PHP to hash objects into array keys like some languages; it does not.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.array.php)

??? question "99. Match the SPL structures to their discipline. Which pairings are correct? (choose two)"
    **✅ SplStack is LIFO ; SplQueue is FIFO**

    SplStack is last-in-first-out and SplQueue is first-in-first-out (both built on SplDoublyLinkedList). SplFixedArray has a fixed size (it does not grow dynamically) and uses less memory for dense integer-indexed data. SplMinHeap returns the smallest element first (SplMaxHeap returns the largest). Misconception: assuming a fixed array auto-resizes or confusing min/max heap ordering.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/spl.datastructures.php)

??? question "100. You want a collection usable in `foreach` without hand-writing five Iterator methods. What is the idiomatic approach?"
    **✅ Implement IteratorAggregate and `yield from $this->items;` in getIterator()**

    IteratorAggregate needs only getIterator(); returning a generator with `yield from` delegates iteration in one line, since a generator is itself an Iterator. Implementing Iterator directly is exactly the five-method chore you want to avoid; ArrayAccess gives bracket access, not foreach; and extending SplStack changes the type/semantics unnecessarily. Misconception: thinking foreach support always requires the full Iterator contract.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.iteratoraggregate.php)

??? question "101. What is Twig's default defence against XSS?"
    **✅ Context-aware auto-escaping of output variables**

    Twig HTML-escapes variables by default (context-aware), so injected markup renders as inert text. It does not strip tags (it encodes them), does not send CSP (a separate, complementary defence), and does not encrypt output. The |raw filter opts out and reintroduces the risk. Misconception: thinking escaping removes content — it encodes it so the browser treats it as data.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html)

??? question "102. Which technique best prevents SQL injection?"
    **✅ Prepared statements with bound parameters**

    Binding sends the data separately from the SQL text, so input can never alter the query structure. addslashes is fragile and charset-dependent, a WAF is defence-in-depth not a fix, and HTML-escaping addresses XSS, not SQL. Symfony apps use PDO/DBAL with bound parameters. Misconception: believing escaping input is equivalent to parameterisation — only binding structurally separates code from data.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

??? question "103. Session fixation is primarily mitigated by…"
    **✅ Regenerating the session id on login**

    Migrating to a new session id at authentication invalidates any attacker-planted id — Symfony does this automatically on login. Longer ids help against guessing (not fixation), logout-only deletion leaves the login window open, and encoding an id changes nothing about the attack. Misconception: conflating fixation (attacker sets the id pre-login) with hijacking (attacker steals the cookie) — they need different defences.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

??? question "104. Which response header defends against clickjacking?"
    **✅ X-Frame-Options: DENY (or CSP frame-ancestors)**

    X-Frame-Options: DENY (or CSP frame-ancestors 'none') forbids the page from being framed, defeating invisible-iframe clickjacking. X-Content-Type-Options stops MIME sniffing, Referrer-Policy limits referer leakage, and Accept-Language is a request header. Misconception: assuming any security header helps against any attack — each header targets a specific threat.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

??? question "105. What is the correct way to store user passwords?"
    **✅ password_hash() with bcrypt or argon2id**

    Adaptive, salted hashing (bcrypt/argon2id via password_hash()) resists brute-force; the per-hash salt is embedded and checked with password_verify(). A static salt plus fast SHA-256 is brute-forceable, MD5 is broken, and reversible encryption defeats the point (a breach reveals plaintext). Misconception: adding your own salt to password_hash() — it generates and embeds one for you.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.password-hash.php)

??? question "106. Why is HTML auto-escaping insufficient when a value is placed inside a `<script>` block or a URL attribute?"
    **✅ Each context needs its own encoding (js/url); HTML escaping does not neutralise script or URL payloads**

    XSS defence must be context-aware: a value safe as HTML text can still break out inside JavaScript or a URL, so you need the js or url escaping strategy there. HTML escaping is not universally sufficient, Twig does not silently disable escaping in script tags, and URLs routinely carry user data (which must be url-encoded). Misconception: treating one escaping strategy as a cure-all across all output contexts.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html)

??? question "107. In Twig, `{{ comment }}` renders the value `<script>alert(1)</script>`. What is output and why is it safe?"
    **✅ &lt;script&gt;alert(1)&lt;/script&gt; — escaped to inert text, so the script never runs**

    Twig auto-escapes to HTML entities, so the browser shows the literal text and executes nothing. It does not run the script (that would require |raw), does not strip the tag (it encodes it), and does not error on the content. Only |raw on this value would reintroduce the XSS. Misconception: assuming the tag is removed rather than entity-encoded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html)

??? question "108. In framework.yaml, which session cookie settings harden against hijacking and CSRF?"
    **✅ cookie_secure: auto, cookie_httponly: true, cookie_samesite: lax**

    Secure (auto = on when HTTPS) keeps the cookie off plain HTTP, HttpOnly blocks JS access (anti-theft via XSS), and SameSite=lax curbs CSRF by not sending the cookie on cross-site navigations. The second option disables every protection; lifetime and domain settings alone do not harden against these attacks. Misconception: thinking SameSite=None (without Secure) is a safe default — it widens exposure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/session.html)

??? question "109. How do the `HttpOnly` and `Secure` cookie flags differ?"
    **✅ HttpOnly blocks JavaScript access to the cookie; Secure restricts it to HTTPS connections**

    HttpOnly hides the cookie from document.cookie (mitigating theft via XSS); Secure ensures the cookie is only sent over TLS (mitigating network sniffing). They solve different problems, are not synonyms, and the third option swaps their meanings. Neither affects lifetime (that is Max-Age/ Expires). Misconception: assuming one flag covers both JS access and transport security.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/session.html)

??? question "110. True or False: a CSRF token is an authentication mechanism."
    **✅ False**

    A CSRF token proves a state-changing request originated from your own form/session, not that a particular user is authenticated — those are separate concerns. Authentication establishes identity; the CSRF token defends already-authenticated sessions from forged cross-site requests. Misconception: treating CSRF tokens as login/identity checks rather than request-origin proof for state-changing actions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/csrf.html)

??? question "111. Which pairings of threat and Symfony/PHP defence are correct? (choose two)"
    **✅ XSS is mitigated by Twig context-aware auto-escaping ; SQL injection is mitigated by prepared statements with bound parameters**

    XSS→output escaping and SQLi→parameter binding are the canonical pairings. CSRF is mitigated by tokens plus SameSite cookies (not output escaping, which addresses XSS), and clickjacking is mitigated by X-Frame-Options/CSP (password hashing protects stored credentials, an unrelated concern). Misconception: assuming one defence generalises across threats — each attack has its own countermeasure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

??? question "112. A developer verifies passwords with `if ($hash == $storedHash)`. What is wrong and what is the fix?"
    **✅ == is non-constant-time (timing attack) and re-hashes wrongly; use password_verify()/hash_equals()**

    Comparing hashes with == (or ===) leaks timing information and does not re-derive the hash from the candidate password; you must call password_verify($plain, $storedHash), which is constant-time and handles the embedded salt. hash_equals() is the constant-time primitive for comparing known strings. === does not fix the timing leak, and md5 is broken. Misconception: treating password checking as a plain string comparison.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.password-verify.php)

---

<small>Back to [Flashcards](index.md) · [PHP & Web Security](../../php-web-security/index.md)</small>

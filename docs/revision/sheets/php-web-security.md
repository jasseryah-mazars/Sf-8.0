# Revision Sheet — PHP & Web Security

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [PHP & Web Security](../../php-web-security/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Une **fiche imprimable, tenant sur une page**, qui résume chaque sous-chapitre de PHP & Web Security en quelques puces "à retenir" suivies d'une ligne "Cheat" très dense.

**Pourquoi ça existe ?** Dans les derniers jours avant l'examen, on veut un support papier ou PDF unique par domaine — pas 10 onglets de navigateur ouverts. Cette fiche condense un domaine entier sur une seule page imprimable.

**🏠 Analogie de la vraie vie :** C'est la **fiche de révision recto-verso** qu'un étudiant prépare avant un examen universitaire : tout le cours du semestre réduit à une page, à relire dans le métro le matin de l'épreuve.

**Symfony dans la vraie vie :** Chaque puce "à retenir" → une règle déjà apprise en détail dans le chapitre / La ligne "Cheat:" → la version ultra-compacte, presque un aide-mémoire de syntaxe / Lien "Full detail" → retour au chapitre complet si un point ne "sonne" plus familier.

**⚠️ Erreur fréquente :** Imprimer cette fiche *avant* d'avoir étudié PHP & Web Security en détail, en espérant apprendre directement dessus — le format est trop dense pour un premier apprentissage, il ne fonctionne qu'en rappel.

**🧠 Comment le mémoriser :** *« Une page, un domaine, la veille de l'examen »* — cette fiche est le tout dernier support à consulter, pas le premier.

## Abstract Classes
- An abstract class cannot be instantiated; any class with one unimplemented abstract member
  must itself be `abstract`.
- Two failure moments: missing implementation is a **link-time** fatal; `new` on an abstract
  class is a **runtime** `Error` you can catch.
- An abstract class with zero abstract methods is still not instantiable — `AbstractController`
  and `AbstractType` are exactly that.
- Implementing an abstract member is an override: covariant return, contravariant parameters,
  visibility equal or wider, extra parameters optional only.
- `abstract` excludes `final` and `private`, and forbids a method body.
- PHP 8.4 adds abstract **properties** (`public`/`protected`), satisfied by a plain or hooked
  property that provides the demanded `get`/`set` operation.
- Template method: `final` skeleton in the parent, abstract hooks for the variable steps.

**Cheat:** One abstract member ⇒ whole class `abstract`, or **compile-time** fatal. `new Abstract…` ⇒ **runtime** `Error`, catchable. Different gate, different stage. Zero abstract methods + `abstract` keyword ⇒ still not instantiable. `abstract` never combines with `final`; never `private`; never a body. Override rules apply: return narrows, parameters widen, visibility widens, extra params must be optional. 8.4: `abstract public string $p { get; }` — public or protected only. Properties invariant, except abstract/virtual get-only (covariant) or set-only (contravariant). Template method = `final` skeleton + `abstract` hooks. `extends` one class, `implements` many interfaces.

## Attributes
- An attribute is compiled metadata: a class name plus constant-expression
  arguments. It never runs by itself.
- `getAttributes()` returns descriptors and validates nothing; `getArguments()`
  evaluates the arguments; `newInstance()` autoloads, validates target and
  repetition, then constructs — and returns a new object every call.
- For user-land attributes every failure is an `Error` at `newInstance()`; only
  built-ins such as `#[\Override]` are checked by the compiler.
- `TARGET_ALL` is 63 and `IS_REPEATABLE` is a separate bit, 64; `TARGET_CLASS`
  covers interfaces, traits and enums, and `TARGET_CLASS_CONSTANT` covers enum cases.
- Attributes are not inherited by subclasses or implementers; `IS_INSTANCEOF` filters
  by `instanceof` and only works when a name is passed.
- Symfony's `#[Route]`, `#[AsCommand]`, `#[AsEventListener]`, `#[Autoconfigure]` and
  `#[Autowire]` are plain attribute classes read through exactly this API.

**Cheat:** Declare: `#[\Attribute(TARGET_* | IS_REPEATABLE)]`; default is `TARGET_ALL`, not repeatable. `TARGET_ALL = 63`, `IS_REPEATABLE = 64` — separate bits. Read: `getAttributes(?string $name = null, int $flags = 0): array`; flags need `$name`. `ReflectionAttribute`: `getName()`, `getArguments()`, `getTarget()`, `isRepeated()`, `newInstance()`, plus `$name` (8.4). Wrong target / repetition → `Error` at **`newInstance()`** for user-land attributes. `#[\Override]`, `#[\Attribute]`, `#[\SensitiveParameter]` → checked by the compiler. Class constants targetable since **8.0**; `new` in arguments since **8.1**. Attributes are **not** inherited by subclasses.

## Anonymous Functions & Closures
- Anonymous functions, arrow functions and `f(...)` all produce instances of the `final`
  class `Closure`; its constructor is `private`.
- `use ($x)` copies at **definition time**; `use (&$x)` shares a reference; `fn`
  auto-captures by value and cannot do otherwise.
- A closure carries a **bound object** and a **scope**; private access is decided by the
  scope alone.
- `bindTo`/`Closure::bind` return a **new** closure (or `null`); `call()` binds and invokes
  in one step and also sets the scope.
- `newScope` defaults to `"static"` — keep the current scope — which is why rebinding alone
  rarely grants private access.
- Symfony injects `\Closure` for lazy, memoized services, and registers Twig callbacks with
  `$this->method(...)`.

**Cheat:** `use ($x)` = copy at definition · `use (&$x)` = live reference · `fn` = copy, always. `fn (&$x)` is a by-reference **parameter**, not a capture. `fn` has no `use` list. Return type goes **after** the `use` clause. Forbidden in `use`: superglobals, `$this`, a name shared with a parameter. `bindTo`/`bind` → new closure or `null`. `call($obj, …)` → binds, sets scope, invokes. `newScope` default is `"static"` = keep the current scope. `static` closure: no `$this` ever; `bindTo($obj)` → `null`. `new Closure()`, `serialize($closure)`, `new Foo(...)`, `$o?->m(...)` — all rejected. `callable` on a property = fatal; use `\Closure`. Symfony: `!service_closure '@id'` / `'@>id'` / `#[AutowireServiceClosure]`, invoked as `($this->prop)()`.

## Enums
- Pure enums implement `UnitEnum` (`name`, `cases()`); backed enums additionally implement
  `BackedEnum` (`value`, `from()`, `tryFrom()`).
- `from()` throws `\ValueError` on a miss and `\TypeError` on a wrong type under strict mode;
  `tryFrom()` returns `null` on a miss only.
- Cases are singletons of a final class, so `===` is exact and survives `from()`, `cases()` and
  serialization.
- An enum may have methods, static methods, constants, interfaces, traits and attributes — never
  properties, inheritance, `new` or `clone`.
- The backing type is `int` or `string`, values are explicit and unique, and `cases()` preserves
  declaration order.
- Symfony turns an invalid backed-enum value into a **404** in routing and in
  `#[MapQueryParameter]`; `EnumType` builds a form from `::cases()`; Doctrine maps it with
  `enumType`; the Serializer normalizes it to its scalar.

**Cheat:** `enum X { case A; }` — pure. `enum X: string { case A = 'a'; }` — backed. `int`/`string` only, values explicit and unique. `UnitEnum`: `->name`, `cases()` (declaration order). `BackedEnum` (backed only): `->value`, `from()` (**throws `\ValueError`**), `tryFrom()` (**`null`**). Strict types: wrong scalar type → `\TypeError` before any lookup. Allowed: methods, static methods, constants (may alias a case), interfaces, traits without properties, attributes, `__call`/`__callStatic`/`__invoke`. Forbidden: properties, `__construct`, inheritance, `final enum`, `clone`, `new`, redeclaring `cases()`/`from()`/`tryFrom()`. `===` yes; `==` against the scalar is `false`; `<`/`>` always `false`. `serialize()` → `E:11:"Suit:Hearts";` and identity survives. `json_encode()` → scalar for backed, **failure** for pure. Symfony: `BackedEnumValueResolver` (priority 100) → 404; `EnumRequirement` → 404 at routing; `#[MapQueryParameter]` → 404 by default; `EnumType` needs `class`; Doctrine needs `enumType` and a backed enum.

## Exception & Error Handling
- `Throwable` is an interface; `Error` and `Exception` are **siblings** implementing it, so
  `catch (\Exception)` never catches an `Error`.
- `finally` always runs, including while unwinding; a `return` or a `throw` inside it
  overrides whatever `try` was doing.
- Chain with `previous:` when rethrowing, and read the chain with `getPrevious()`.
- Multi-catch `A|B` since 7.1.0; variable-less `catch` and `throw` as an expression since
  8.0.0.
- `set_error_handler` (legacy diagnostics), `set_exception_handler` (uncaught throwables)
  and shutdown functions (fatals) are three separate mechanisms.
- Symfony maps `HttpExceptionInterface::getStatusCode()` to the response status, and 500
  for anything else.

**Cheat:** `Throwable` → `Error` | `Exception`. Siblings. `catch (\Exception)` misses `Error`. `Error` arm: `TypeError` → `ArgumentCountError`, `ValueError`, `ArithmeticError` → `DivisionByZeroError`, `CompileError` → `ParseError`, `UnhandledMatchError`, `AssertionError`, `FiberError`. `Exception` arm: `ErrorException`, `LogicException` (`Domain`, `InvalidArgument`, `Length`, `OutOfRange`, `BadFunctionCall` → `BadMethodCall`), `RuntimeException` (`OutOfBounds`, `Overflow`, `Range`, `Underflow`, `UnexpectedValue`). `finally` always runs. `return` in `finally` wins. `throw` in `finally` wins, and the `try` exception becomes its `previous`. `A|B` = 7.1.0 · variable-less `catch` = 8.0.0 · `throw` expression = 8.0.0 · `Throwable extends Stringable` = 8.0.0. `set_error_handler` ≠ `set_exception_handler` ≠ `register_shutdown_function`. Cannot `implements \Throwable` on a class. Cannot `clone` a throwable. `E_ALL` = 30719 in 8.4. `intdiv(\PHP_INT_MIN, -1)` = `ArithmeticError`. Symfony: `HttpExceptionInterface::getStatusCode()`, else 500.

## PHP Extensions
- Symfony needs `ctype`, `iconv`, `mbstring`, `intl` (declared as `ext-*`).
- `extension_loaded()` is the runtime check; `ext-*` is the install-time gate.
- `strlen`=bytes, `mb_strlen`=characters — matters for UTF-8.
- `opcache` = bytecode cache; the top production speedup.

**Cheat:** `php -m` lists modules; `php --ri ext` shows config. Require: `"ext-mbstring": "*"` etc. in composer.json. `mb_*` for text; `ctype_*` beware integer-as-ASCII gotcha. Prefer native ext over Symfony polyfill.

## Interfaces & Type Declarations
- Returns covariant (narrow), parameters contravariant (widen); violations are fatal at load.
- Interfaces give multiple inheritance of type; abstract classes do not.
- Intersection = all, class types only; union = any; DNF combines them (8.2).
- Interface constants are overridable since 8.1; interfaces may require properties since 8.4.
- `instanceof` covers class + parents + interfaces, and is `false` on non-objects.

**Cheat:** Covariant return, contravariant param — reverse = fatal error at class load. `A&B` class types only; `(A&B)|null` = DNF (8.2); `never` return-only (8.1). Interface: constants (typed 8.3, overridable 8.1), **properties 8.4**, multiple `extends`. `instanceof` never throws on non-objects. `readonly` satisfies `{ get; }` but never `{ set; }`.

## Namespaces & Autoloading
- Names are resolved by shape: unqualified, qualified, fully qualified, relative. Qualified
  is still relative — only a leading `\` is absolute.
- Unqualified **functions and constants** fall back to the global namespace; **class names
  never do**.
- PHP keeps **three** import tables — classes, functions, constants — and they never leak
  into each other.
- `use` is a compile-time alias: no I/O, no autoload, no effect on dynamic names.
- PSR-4 strips the prefix, converts `\` to `/`, appends `.php`, and resolves against the
  base directory; the prefix never appears in the path.
- In Symfony, the FQCN is simultaneously the file path (via PSR-4), the service id, and the
  autowiring key.

**Cheat:** `declare` may precede `namespace`; nothing else may, not even whitespace. `\Foo` absolute · `Sub\Foo` relative · `Foo` unqualified · `namespace\Foo` relative to the current namespace. Verbs fall back, nouns do not: functions and constants reach global; classes fatal. Three tables: `use` · `use function` · `use const`. Group: `use App\{A, B as C};`. `use` = compile-time nickname. Autoload fires on first *use*, not on the import. Dynamic class names: no alias, always fully qualified, double the `\` in strings. PSR-4: strip prefix → `\` becomes `/` → add `.php`. Prefix ends with `\`. Production: `composer dump-autoload --no-dev --classmap-authoritative`. Symfony: `App\` → `src/`; service id = FQCN; autowiring matches the id exactly.

## Object-Oriented Programming
- `static::` = late static binding, resolved to the **called** class; `self::` = compile-time,
  the **defining** class. `self::`, `parent::`, `static::` and `forward_static_call()` forward
  the called class; naming a class explicitly resets it.
- `clone` is shallow; `__clone()` runs on the copy afterwards and is the only place a
  `readonly` property may be written a second time (8.3+).
- Magic methods fire only for inaccessible or undeclared members, must be `public` except the
  three construct/destruct/clone cases, and must match the documented signature exactly.
- Promotion declares and assigns in one step, supports any single modifier, forbids `callable`,
  and copies a default value to the parameter only.
- PHP 8.4 adds property hooks (backed vs virtual), asymmetric visibility, abstract properties
  and `final` properties — and makes `readonly` implicitly `protected(set)`.

**Cheat:** `new static()` for subclass-safe factories, and always declare `: static`. Forwarding: `self::` `parent::` `static::` `forward_static_call()`. Everything else resets LSB. 17 magic methods; all public except `__construct`, `__destruct`, `__clone`. `callable` cannot be promoted; `readonly` needs a type, forbids a default, forbids `static`. 8.4: hooks (`get`/`set`, non-static, no `readonly`), `private(set)` (implicitly `final`, typed only, no static), abstract properties, `final` properties, `readonly` = implicitly `protected(set)`. `var_dump`/`serialize`/`(array)` → raw value. `json_encode`/`get_object_vars`/`var_export` → `get` hook. Visibility: `private` = declaring class only; `protected` = class + children **+ parents**.

## PHP API (up to 8.4)
- Symfony 8 requires **PHP 8.4+**; the exam expects you to date a feature on sight.
- 8.0 `match`/attributes · 8.1 enums/`readonly`/`f(...)` · 8.2 `readonly class`/DNF ·
  8.3 typed constants/`#[\Override]` · 8.4 hooks/asymmetric visibility/lazy objects.
- A hooked property is **backed** if a hook names it, **virtual** otherwise.
- `readonly` = one write and, **since 8.4**, `protected(set)`. `private(set)` = many
  internal writes, and implicitly `final`.
- `from()` throws `\ValueError`, `tryFrom()` returns `null`; `match` is strict and
  throws `\UnhandledMatchError`.
- `f(string $a = null)` is **deprecated in 8.4** — write `?string`.

**Cheat:** 8.0 `match`, attributes, promotion, `?->`, named args, union · 8.1 enums, `readonly`, `f(...)`, `never`, intersection, `new` in init · 8.2 `readonly class`, DNF, standalone `true`/`false`/`null` · 8.3 typed constants, `#[\Override]`, `json_validate()` · 8.4 hooks, `private(set)`, lazy objects, `new X()->y()`. Backed ⇔ a hook writes `$this->prop`. Virtual ⇔ it does not ⇔ no storage. `readonly` since 8.4 = `protected(set)`; hooks + `readonly` = fatal. `private(set)`: typed only, non-static, never wider than read, implicitly `final`. `match` strict + throws; two `default` arms = fatal. `array_all([])` is `true`; `array_any([])` is `false`; `array_find()` misses = `null`. `#[\Deprecated]` → function/method/class constant → `E_USER_DEPRECATED`. `T $x = null` deprecated in 8.4 → write `?T`.

## SPL — Standard PHP Library
- `Iterator` = 5 methods; `IteratorAggregate` = delegate via `getIterator()`.
- Generators are lazy, single-use iterators — great for memory.
- `SplObjectStorage` keys by object identity; arrays cannot.
- Pick the SPL structure by discipline: LIFO/FIFO/heap/priority.

**Cheat:** `foreach` needs `Traversable` (Iterator or IteratorAggregate). `count($o)` needs `Countable`; `$o[$k]` needs `ArrayAccess`. `yield` → Generator (Iterator); `yield from` delegates. Stack=LIFO, Queue=FIFO, Heap=ordered, PriorityQueue=value+priority (unstable).

## Traits
- Traits are **compile-time horizontal reuse**: members are copied into the class, leaving no
  runtime trace — and are therefore **not types**.
- Precedence is **class > trait > inherited parent**, and it is evaluated *before* collisions.
- Two traits offering one name is a **fatal error**; `insteadof` picks the survivor (listing every
  competitor) and `as` re-admits or re-scopes.
- `as` is additive: only `m as protected;` without a new name changes visibility in place.
- Static trait properties are **per using class**; within a hierarchy they are distinct only since
  8.3, and only if the child repeats `use`.
- Version pins: abstract private + signature compatibility (8.0), static-on-trait deprecation
  (8.1), constants (8.2), static scoping and `as final` (8.3).

**Cheat:** Precedence: **class > trait > parent** — evaluated *before* collision detection. `use A, B { A::m insteadof B, D; B::m as protected mLegacy; }`. `m as protected;` → re-scopes in place. `m as protected x;` → adds `x`, original intact. `m as final;` (8.3) → blocks **children**, not the using class. Static trait property = per using class; a child needs its own `use` for a distinct copy (8.3). Constants in traits since **8.2**; property/constant redeclaration must be *identical*. `__CLASS__` = using class · `__TRAIT__` / `__METHOD__` = the trait. `instanceof Trait` → `false`, silently. No type-hint, no `new`, no `implements`. `class_uses()` = this class's own `use` statements only.

## Web Security Fundamentals
- Each threat maps to one Symfony defence — learn the pairing.
- Escape output **in context**; bind SQL parameters; regenerate sessions on login.
- Cookies: `Secure` + `HttpOnly` + `SameSite`; add HSTS + CSP + `nosniff`.
- Store passwords with `password_hash` (bcrypt/argon2id), verify constant-time.

**Cheat:** XSS→Twig escaping · CSRF→token+SameSite · SQLi→prepared statements. Fixation→session migrate on login · Hijack→Secure/HttpOnly/HTTPS. Clickjacking→`X-Frame-Options`/CSP `frame-ancestors`. Passwords→`PASSWORD_ARGON2ID`/`BCRYPT`; verify with `password_verify`.

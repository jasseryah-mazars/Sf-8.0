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
- PHP's core is small; capability lives in **extensions**, classified by the manual as
  core, bundled, external or PECL.
- `extension_loaded()` is the runtime check and is case-insensitive; `phpversion($ext)`
  gives presence plus version; `function_exists()` cannot tell native from polyfilled.
- OPcache registers as **`Zend OPcache`**, loads with `zend_extension=`, and caches
  **bytecode only**.
- `strlen` = bytes, `mb_strlen` = code points, `grapheme_strlen` = grapheme clusters —
  the same three levels Symfony exposes as `ByteString`, `CodePointString`,
  `UnicodeString`.
- `ctype_digit('')` is `false`; `ctype_digit(123)` is `false`; `ctype_digit(1234)` is
  `true`; non-string arguments are deprecated since PHP 8.1.
- `iconv` binds the host's conversion facility (`//TRANSLIT`, `//IGNORE`, host-dependent);
  `mbstring` ships its own tables and behaves identically everywhere.
- `pdo` is an interface; each database needs its own driver extension, loaded after PDO.
- `ext-*` in `composer.json` gates resolution, not reality; only
  `composer check-platform-reqs` inspects the real host.
- Symfony's documented requirements are Ctype, iconv, PCRE, Session, SimpleXML and
  Tokenizer — mbstring and intl are covered by polyfills, and the ICU polyfill is limited
  to the `en` locale.

**Cheat:** `php -m` lists modules (two sections); `php --ri "Zend OPcache"` shows one config. `extension_loaded('Zend OPcache')` — **not** `'opcache'`. Case-insensitive. `phpversion($ext)` → version string or `false`. `get_loaded_extensions(true)` → Zend only. `strlen('café')` = 5 · `mb_strlen('café','UTF-8')` = 4 · `grapheme_strlen` counts what you see. `mb_convert_encoding($str, $to, $from)` vs `iconv($from, $to, $str)` — mirrored. `//TRANSLIT` approximates · `//IGNORE` drops · neither → `E_NOTICE` + `false`. `ctype_digit('')` = false · `(123)` = false · `(1234)` = true · non-string deprecated since 8.1. `mb_*` invalid encoding → `ValueError` since PHP 8.0. Composer: `"ext-intl": "*"` gates · `show -p` lists · `check-platform-reqs` verifies the real host. Polyfills: `provide` satisfies `ext-*`; `polyfill-intl-icu` is **`en` only**. Symfony requires: Ctype, iconv, PCRE, Session, SimpleXML, Tokenizer. Monorepo declares only `ext-xml`. OPcache defaults: `enable=1`, `enable_cli=0`, `memory=128`, `interned=8`, `max_files=10000`, `validate_timestamps=1`, `revalidate_freq=2`, `jit=disable` (8.4). Symfony recommends: `memory=256`, `max_files=32531`, `interned=32`, `validate_timestamps=0` + reset. Preload: functions/classes/interfaces/traits, **not constants**; no Windows; restart to clear.

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
- `foreach` needs `Traversable`; the only two ways in are `Iterator` (five methods, you drive)
  and `IteratorAggregate` (one method, you delegate), and no class may have both.
- `count($o)` needs `Countable`; `$o[$k]` needs `ArrayAccess`; `"$o"` needs `__toString()`
  (`Stringable`); `json_encode($o)` is customised by `JsonSerializable`.
- `isset()` and `??` on an `ArrayAccess` object call `offsetExists()` first, and reach
  `offsetGet()` only when it returned `true`.
- A generator is a lazy, forward-only, **single-use** `Iterator`; calling the function runs
  nothing until the first advance.
- `yield from` preserves inner keys and `iterator_to_array()` preserves keys by default —
  together they are the classic silent data-loss trap.
- Pick the structure by discipline: `SplStack` LIFO, `SplQueue` FIFO, `SplHeap` ordered,
  `SplPriorityQueue` value + priority (unstable on ties), `SplObjectStorage` keyed by object
  identity.
- Iterating a heap consumes it; iterating a linked list or an object storage does not.

**Cheat:** `foreach` order: `rewind`, `valid`, `current`, `key`, body, `next`, `valid`, … `Iterator` = 5 methods · `IteratorAggregate` = `getIterator(): Traversable` · never both. `iterable` = `array|Traversable`. Generator: lazy, forward-only, single-use; second traversal **throws**. `yield from` keeps inner keys · `iterator_to_array()` keeps keys by default. `getReturn()` only after completion · `send()` needs no priming and returns the next yielded value. `isset($o[$k])` → `offsetExists` · `empty($o[$k])` → `offsetExists` then maybe `offsetGet` · `$o[] = $v` → `offsetSet(null, $v)`. Stack = LIFO, Queue = FIFO (same base class), Heap = ordered and **consumed by `foreach`**, PriorityQueue = max heap, unstable on ties, `EXTR_DATA` by default. `SplObjectStorage` = object → data map or object set, keyed by identity. `SplFixedArray` = integer keys, fixed size, less memory, `OutOfBoundsException` on 8.4. Decorators: `IteratorIterator` converts, `LimitIterator(offset, limit)` slices, `CallbackFilterIterator($current, $key, $iterator)` selects, `RecursiveIteratorIterator` flattens (`LEAVES_ONLY` by default), `AppendIterator` concatenates without renumbering.

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
- Every threat is one boundary crossing where data is read as instructions; every defence
  makes that boundary explicit.
- Escape at **output**, in the **destination's** context. Twig picks the strategy per
  template from the file name, at compile time.
- `|raw` disables escaping and sanitises nothing.
- Bind every value in SQL and DQL; allow-list identifiers, which cannot be bound.
- CSRF tokens prove the request came from your page. `SameSite=Lax` narrows the window but
  still allows cross-site top-level `GET`.
- Session id migration on login defeats fixation; `HttpOnly` + `Secure` + HTTPS defeat
  hijacking.
- Store passwords with `password_hash()` or a Symfony hasher; verify with a verify function,
  never with `===`.
- Symfony ships escaping, CSRF, bound parameters and session migration on by default — and
  no security headers, no HTTPS enforcement, no redirect validation.

**Cheat:** XSS→contextual escaping · CSRF→token + `SameSite` · SQLi→bound parameters. Fixation→`migrate(true)` on login · Hijack→`HttpOnly` + `Secure` + HTTPS. Clickjacking→CSP `frame-ancestors` (preferred) or `X-Frame-Options`. Twig strategy from the file name, at compile time: `js`/`json`→`js`, `css`→`css`, `txt`→**none**, else `html`. Defaults: `session_fixation_strategy: MIGRATE`, `cookie_httponly: true`, `cookie_samesite: lax`, `cookie_secure` **none**, `use_strict_mode: 1`, `allow_extra_fields: false`. Passwords: `'auto'` = bcrypt today, cost 13; bcrypt truncates at 72 bytes; PHP 8.4 default cost 12; salt embedded and an explicit one ignored. Rehash on successful login → `PasswordUpgraderInterface::upgradePassword()`. `hash_equals($known, $userSupplied)` — secret first. Symfony sends **no** security headers. That is always your listener.

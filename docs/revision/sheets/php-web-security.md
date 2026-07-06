# Revision Sheet — PHP & Web Security

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [PHP & Web Security](../../php-web-security/index.md).

## Abstract Classes
- Abstract classes = partial implementation + shared state; not instantiable.
- Any abstract method makes the whole class abstract.
- Template method: fixed skeleton (often `final`) + abstract hooks.
- One abstract parent, many interfaces.

**Cheat:** `abstract` method = no body; subclass must implement (variance applies). Can have ctor/props/constants; cannot be `new`-ed. Template method: `final` skeleton → abstract hooks. `extends` one class, `implements` many interfaces.

## Anonymous Functions & Closures
- Closures are `Closure` instances carrying a bound `$this` and a scope.
- `use` = by value at definition (or `&` for reference); `fn` = auto by value.
- Rebind with `bindTo`/`bind`/`call`; scope controls private access.
- `f(...)` and `Closure::fromCallable()` build closures from any callable.

**Cheat:** `fn (x) => expr` — auto-capture by value, single expr, no `&`. `function () use (&$x) {}` — by reference. `bindTo($obj, $scope)` / `bind()` (static) / `call($obj)`. `strlen(...)` == `Closure::fromCallable('strlen')`.

## Exception & Error Handling
- `Throwable` = `Error` ∪ `Exception`; catch `\Throwable` for both.
- `finally` always runs; avoid `return` inside it.
- Chain with `previous:` to keep the root cause.
- `set_error_handler` ≠ exceptions ≠ fatals — different mechanisms.

**Cheat:** `Error`: `TypeError`, `ValueError`, `DivisionByZeroError`, `ParseError`. `Exception`: `RuntimeException`, `LogicException`, `JsonException`. Multi-catch: `catch (A | B $e)`; variable optional (8.0+). `set_error_handler` → warnings; `set_exception_handler` → uncaught throws.

## PHP Extensions
- Symfony needs `ctype`, `iconv`, `mbstring`, `intl` (declared as `ext-*`).
- `extension_loaded()` is the runtime check; `ext-*` is the install-time gate.
- `strlen`=bytes, `mb_strlen`=characters — matters for UTF-8.
- `opcache` = bytecode cache; the top production speedup.

**Cheat:** `php -m` lists modules; `php --ri ext` shows config. Require: `"ext-mbstring": "*"` etc. in composer.json. `mb_*` for text; `ctype_*` beware integer-as-ASCII gotcha. Prefer native ext over Symfony polyfill.

## Interfaces & Type Declarations
- Returns covariant (narrow), parameters contravariant (widen).
- Interfaces give multiple inheritance of type; abstract classes do not.
- Intersection = all interfaces; union = any type; DNF combines them.
- `instanceof` covers class + parents + interfaces, false on non-objects.

**Cheat:** Covariant return, contravariant param — reverse = fatal error. `A&B` interfaces only; `(A&B)|null` = DNF (8.2). Interface: constants only (typed 8.3), no properties, multiple `extends`. `instanceof` never throws on non-objects.

## Namespaces & Autoloading
- Functions/constants fall back to global; **classes do not**.
- `use` is a compile-time alias, not a file load.
- PSR-4 maps prefix → base dir; strip prefix, `\`→`/`, add `.php`.
- `composer dump-autoload --optimize` for production.

**Cheat:** `namespace` + `declare` first; nothing before them. `\Foo` = fully qualified; `Foo` = current ns (class) or global (function). Grouped: `use App\{A, B, C};` · function: `use function`; const: `use const`. PSR-4: `App\ → src/`, case-sensitive on Linux.

## Object-Oriented Programming
- `static::` = late static binding (runtime); `self::` = compile-time.
- `clone` is shallow — use `__clone` for deep copies.
- Magic methods fire only for inaccessible/undefined members.
- Promotion declares + assigns; supports visibility, `readonly`, defaults.

**Cheat:** `new static()` for subclass-safe factories. Magic: `__get/__set/__isset/__unset/__call/__callStatic/__invoke/__toString/__clone`. `callable` cannot be promoted; readonly needs a type + no default. Visibility: private = declaring class only; protected = + subclasses.

## PHP API (up to 8.4)
- Know each feature's **version** and exact semantics; the exam probes edges.
- `match`/enum/`readonly` are everywhere in Symfony 8 code — read them fluently.
- PHP 8.4 headline items: **property hooks** and **asymmetric visibility**.
- `from()` throws, `tryFrom()` returns `null`; `match` is strict.

**Cheat:** 8.1: enums, `readonly` prop, `f(...)`, `never`, `new` in init. 8.2: `readonly class`, DNF types, `true`/`false`/`null` types. 8.3: typed constants, `#[\Override]`, `json_validate()`. 8.4: property hooks, asymmetric visibility (`private(set)`), `new` w/o `()`. `match`===strict + throws; `tryFrom`=null, `from`=`\ValueError`.

## SPL — Standard PHP Library
- `Iterator` = 5 methods; `IteratorAggregate` = delegate via `getIterator()`.
- Generators are lazy, single-use iterators — great for memory.
- `SplObjectStorage` keys by object identity; arrays cannot.
- Pick the SPL structure by discipline: LIFO/FIFO/heap/priority.

**Cheat:** `foreach` needs `Traversable` (Iterator or IteratorAggregate). `count($o)` needs `Countable`; `$o[$k]` needs `ArrayAccess`. `yield` → Generator (Iterator); `yield from` delegates. Stack=LIFO, Queue=FIFO, Heap=ordered, PriorityQueue=value+priority (unstable).

## Traits
- Traits = compile-time horizontal reuse; not types.
- Precedence: class > trait > parent.
- Resolve trait clashes with `insteadof` (pick one) and `as` (alias/visibility).
- Static trait members are per-using-class, not shared.

**Cheat:** `use A, B { A::m insteadof B; B::m as bMethod; }`. `as protected` / `as public` changes visibility. Cannot type-hint a trait; pair it with an interface. Abstract trait methods force the using class to implement them.

## Web Security Fundamentals
- Each threat maps to one Symfony defence — learn the pairing.
- Escape output **in context**; bind SQL parameters; regenerate sessions on login.
- Cookies: `Secure` + `HttpOnly` + `SameSite`; add HSTS + CSP + `nosniff`.
- Store passwords with `password_hash` (bcrypt/argon2id), verify constant-time.

**Cheat:** XSS→Twig escaping · CSRF→token+SameSite · SQLi→prepared statements. Fixation→session migrate on login · Hijack→Secure/HttpOnly/HTTPS. Clickjacking→`X-Frame-Options`/CSP `frame-ancestors`. Passwords→`PASSWORD_ARGON2ID`/`BCRYPT`; verify with `password_verify`.

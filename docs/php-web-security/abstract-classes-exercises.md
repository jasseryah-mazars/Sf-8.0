# Guided Exercises — Abstract Classes

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    a prediction before revealing a hint, and to a full attempt before revealing the solution.
    Every exercise here deliberately produces an error at some point — the error message *is*
    the lesson, because the exam asks you to recognise them by wording and by stage.

    Theory: **[Abstract Classes](abstract-classes.md)** · Then:
    **[Topic exam](abstract-classes-exam.md)**

    All code targets **PHP 8.4**. `php -l` checks syntax only; a missing implementation is
    detected when the class **loads**, so run the files rather than linting them.

## Exercise 1 · Discover the two failure stages

**Objective:** See that "unimplemented abstract member" and "instantiated an abstract class"
are two different errors, at two different stages, with two different catchabilities.

**Context:** A base class with one mandatory blank, and two ways of getting it wrong.

**Starting point:**

```php
<?php
// lint-skip — this snippet is deliberately broken; that is the exercise
declare(strict_types=1);

abstract class Importer
{
    abstract protected function parse(string $raw): array;
}

final class CsvImporter extends Importer
{
    // intentionally empty
}
```

**Task:** Predict what PHP does with this file and *when*. Then, separately, predict what
happens for a **correct** subclass if someone writes `new Importer()`. Finally, decide which
of the two failures — if either — can be wrapped in `try { … } catch (\Error $e) { … }`.

**Expected observation:** Two distinct errors. One prevents the file from loading at all; the
other is a normal runtime `Error`.

??? tip "Show a hint"
    Ask when PHP could possibly discover each problem. One is visible from the *declaration
    alone*; the other requires a `new` expression to actually execute. Errors raised while
    compiling a declaration have no surrounding code running yet — so what could catch them?

??? success "Show the solution"
    The file above never finishes loading:

    ```
    Fatal error: Class CsvImporter contains 1 abstract method and must therefore be
    declared abstract or implement the remaining methods (Importer::parse)
    ```

    Instantiating the base class is a different story:

    ```php
    abstract class Importer {}

    try {
        new Importer();
    } catch (\Error $e) {
        echo $e->getMessage();   // Cannot instantiate abstract class Importer
    }
    ```

    That prints the message. It is a genuine, catchable `\Error`.

    **Why it works:** the completeness check runs while the class is **linked** — when the
    declaration is compiled or the autoloader loads the file. There is no user code on the
    stack to catch anything. The instantiation check is a single flag test performed by the
    `new` opcode at **runtime**, so it throws an ordinary `Error` like any other.

    **Certification takeaway:** "missing implementation" is a compile/link-time fatal you
    cannot catch. "Cannot instantiate abstract class" is a runtime `Error` you can. Answer
    options that merge the two are the most common distractor in this topic.

    **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

## Exercise 2 · Minimal implementation — build a template method

**Objective:** Write the smallest correct abstract base: fixed skeleton, one abstract hook.

**Context:** Two importers must share the reading and counting logic and differ only in
parsing.

**Starting point:**

```php
<?php
declare(strict_types=1);

abstract class Importer
{
    public function __construct(protected readonly string $source) {}

    // TASK: add the abstract hook and the final skeleton here
}
```

**Task:** Add `abstract protected function parse(string $raw): array;` and a
`final public function import(): int` that reads the file, calls `parse()` and returns the row
count. Then write `CsvImporter`. Before running it, answer: is a **concrete** method allowed
to call an **abstract** one?

**Expected observation:** It works, and yes — a concrete method calling an abstract one is the
whole point of the pattern.

??? tip "Show a hint"
    `import()` only ever runs on an instance, and only concrete subclasses can be instances.
    So by the time `$this->parse()` executes, is there any possible receiver that lacks an
    implementation?

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    abstract class Importer
    {
        public function __construct(protected readonly string $source) {}

        abstract protected function parse(string $raw): array;

        final public function import(): int
        {
            $rows = $this->parse(file_get_contents($this->source) ?: '');

            return \count($rows);
        }
    }

    final class CsvImporter extends Importer
    {
        protected function parse(string $raw): array
        {
            return array_map(
                static fn (string $line): array => explode(',', $line),
                explode("\n", trim($raw)),
            );
        }
    }
    ```

    **Why it works:** `import()` is the **template method** — a fixed algorithm that defers
    exactly one step. Calling `$this->parse()` from it is safe because an abstract class can
    never be instantiated, so `$this` is always a concrete subclass that has supplied the
    method. Marking `import()` `final` means a subclass may customise the step but never the
    skeleton.

    **Certification takeaway:** template method = `final` concrete skeleton + `abstract`
    hooks. "It is invalid because it calls an abstract method" is a distractor: the call is
    legal and idiomatic.

    **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

## Exercise 3 · Inspect what the class really carries

**Objective:** Prove with Reflection that `abstract` on the class and `abstract` on a method
are two independent flags.

**Context:** Symfony's `AbstractController` declares **no** abstract method, yet it is
abstract. Reproduce that shape and inspect it.

**Starting point:**

```php
<?php
declare(strict_types=1);

abstract class HelperBase
{
    public function help(): string { return 'shared'; }
}

abstract class WithHook
{
    abstract public function hook(): string;
}
```

**Task:** For both classes, predict the values of `isAbstract()`, `isInstantiable()` and
`count(getMethods(ReflectionMethod::IS_ABSTRACT))` before running the code. Then explain what
prevents `new HelperBase()`.

**Expected observation:** Both are abstract and non-instantiable, but only `WithHook` has an
abstract method. The class flag alone blocks instantiation.

??? tip "Show a hint"
    Are the two questions "does this class owe anything?" and "may this class be
    instantiated?" the same question? Try to describe a class where the answers differ.

??? success "Show the solution"
    ```php
    foreach ([HelperBase::class, WithHook::class] as $fqcn) {
        $r = new ReflectionClass($fqcn);
        printf(
            "%s: abstract=%d instantiable=%d abstractMethods=%d\n",
            $fqcn,
            (int) $r->isAbstract(),
            (int) $r->isInstantiable(),
            \count($r->getMethods(ReflectionMethod::IS_ABSTRACT)),
        );
    }
    // HelperBase: abstract=1 instantiable=0 abstractMethods=0
    // WithHook:   abstract=1 instantiable=0 abstractMethods=1
    ```

    **Why it works:** the `abstract` keyword sets a flag on the **class entry**, and `new`
    consults only that flag. Abstract *members* are a separate mechanism: they are entries in
    the method table with no body, and they are counted only when a subclass is linked. A
    class can carry the class flag with an empty debt — which is exactly what
    `AbstractController` and `AbstractType` do, both of which declare zero abstract methods
    and exist only to be extended.

    **Certification takeaway:** "an abstract class must contain at least one abstract method"
    is **false**. The keyword alone makes the class non-instantiable, and real framework code
    relies on that.

    **Official reference:** https://www.php.net/manual/en/reflectionclass.isabstract.php

## Exercise 4 · Change one variable — visibility, then parameters

**Objective:** Confirm that implementing an abstract method is an ordinary override, subject
to every override rule.

**Context:** Start from the working `Importer`/`CsvImporter` pair from Exercise 2.

**Starting point:**

```php
abstract class Importer
{
    abstract protected function parse(string $raw): array;
}
```

**Task:** Make four independent changes to `CsvImporter::parse()` and predict each result
before running:

1. declare it `public` instead of `protected`;
2. declare it `private`;
3. add a trailing `string $delimiter = ','` parameter;
4. add a trailing `string $delimiter` parameter with **no** default.

**Expected observation:** 1 and 3 are legal; 2 and 4 are fatal, and the two messages name
different rules.

??? tip "Show a hint"
    For each change ask: could a caller who only knows the *parent's* signature still make a
    call that works? Whichever change turns a previously valid call into an invalid one is the
    illegal one.

??? success "Show the solution"
    **1 — `public`: legal.** Visibility may be relaxed. The manual states that visibility
    *"can be relaxed … but they cannot be restricted"*.

    **2 — `private`: fatal.**

    ```
    Fatal error: Access level to CsvImporter::parse() must be protected
    (as in class Importer) or weaker
    ```

    **3 — optional extra parameter: legal.** The manual's own abstract-class example shows a
    child adding `$separator = "."` to a parent signature that never had it. Every call using
    the parent's signature still works.

    **4 — required extra parameter: fatal.**

    ```
    Fatal error: Declaration of CsvImporter::parse(string $raw, string $delimiter): array
    must be compatible with Importer::parse(string $raw): array
    ```

    **Why it works:** an implementation of an abstract method is an override, so the same
    three families of rule apply: variance on types (return narrows, parameters widen),
    visibility equal or wider, and parameter list compatible — extra parameters allowed only
    when optional, because the parent's contract advertised a call with fewer arguments.

    **Certification takeaway:** the *direction that keeps every existing call valid* is always
    the legal one. Widening visibility and adding an optional parameter both keep old calls
    working; narrowing visibility and requiring a new argument both break them.

    **Official reference:** https://www.php.net/manual/en/language.oop5.inheritance.php

## Exercise 5 · Diagnose a failure from the message alone

**Objective:** Map an error message to its stage and its rule without running anything.

**Context:** Four messages arrive from CI on the same pull request. No source is attached.

**Starting point:**

```
1) Fatal error: Class ReportBuilder contains 2 abstract methods and must therefore be
   declared abstract or implement the remaining methods (Builder::header, Builder::footer)
2) Fatal error: Cannot use the final modifier on an abstract method
3) PHP Fatal error: Uncaught Error: Cannot instantiate abstract class Builder
4) PHP Fatal error: Uncaught Error: Cannot call abstract method Builder::render()
```

**Task:** For each message, state the **stage** (compile, link, runtime), whether it is
catchable, and the minimal fix.

**Expected observation:** Two are uncatchable declaration-time errors; two are catchable
runtime `Error`s.

??? tip "Show a hint"
    Sort them by one question: does this message require any code to have *executed*? Messages
    prefixed `Uncaught Error:` were thrown by a running opcode; the others were emitted while
    the declaration was being processed.

??? success "Show the solution"
    **1 — link time, uncatchable.** `ReportBuilder` inherits two unimplemented methods. Fix:
    implement `header()` and `footer()`, or declare `ReportBuilder` abstract and let its own
    children do it.

    **2 — compile time, uncatchable.** `abstract` and `final` contradict each other:
    "must override" against "may not override". Fix: drop one. The same conflict on a class
    reads *"Cannot use the final modifier on an abstract class"*.

    **3 — runtime, catchable `\Error`.** Someone wrote `new Builder()` — or called a
    `new static()` factory *on the abstract class itself*. Fix: instantiate a concrete
    subclass.

    **4 — runtime, catchable `\Error`.** An implementation called `parent::render()` where
    `render()` is abstract in the parent, so there is no body to run. Fix: remove the
    `parent::` call, or give the parent a concrete default and stop marking it abstract.

    **Why it works:** the two stages produce structurally different output. A declaration-time
    fatal is emitted by the engine while processing a class and aborts the script with no
    exception object. A runtime failure is a real `Error` object, which is why messages 3 and
    4 are prefixed `Uncaught Error:` — an exception nobody caught.

    **Certification takeaway:** read the prefix first. `Uncaught Error:` means runtime and
    catchable; a bare `Fatal error:` naming a declaration means compile or link time and
    uncatchable.

    **Official reference:** https://www.php.net/manual/en/language.oop5.final.php

## Exercise 6 · Handle an edge case — abstract properties (PHP 8.4)

**Objective:** Explore the newest rule in the topic and the three ways a subclass may satisfy
it.

**Context:** Abstract properties arrived in **PHP 8.4.0** and may be `public` or `protected`.

**Starting point:**

```php
<?php
declare(strict_types=1);

abstract class Entity
{
    abstract public string $label { get; }

    abstract protected string $slug { get; set; }
}
```

**Task:** Answer four questions, then verify each. **(a)** Can `$label` be satisfied by a
plain `public string $label = 'x';`, even though that is also writeable? **(b)** Can it be
satisfied by `protected string $label`? **(c)** Can `$slug` be satisfied by a `public` property
instead of a `protected` one? **(d)** What error appears if a subclass provides neither?

**Expected observation:** (a) yes, (b) no, (c) yes, (d) an error that counts the property as an
abstract **method**.

??? tip "Show a hint"
    Two of these are the same rule you already know from methods — providing *more* than the
    contract demands is safe, providing *less* is not. For (d), ask what a property hook must
    be represented as internally for the engine to track it at all.

??? success "Show the solution"
    **(a) Yes.** A plain public property provides a public `get`, and also a `set` the contract
    never asked about. Over-delivering is always legal.

    ```php
    final class Post extends Entity
    {
        public string $label = 'Post';
        protected string $slug = 'post';
    }
    ```

    **(b) No.** Visibility may not be narrowed:

    ```
    Fatal error: Access level to Post::$label must be public (as in class Entity)
    ```

    **(c) Yes.** The manual is explicit that *"a protected abstract property may be satisfied
    by a property that is readable/writeable from either protected or public scope"*, and that
    expanding visibility from protected to public is fine.

    **(d)** Omitting `$label` entirely gives:

    ```
    Fatal error: Class Post contains 1 abstract method and must therefore be declared
    abstract or implement the remaining methods (Entity::$label::get)
    ```

    **Why it works:** the requirement is reported as `Entity::$label::get` and counted among
    "abstract methods", which is the engine telling you how hooks are stored — `get`/`set` are
    methods attached to a property name. That is also why an abstract property on an abstract
    class may implement **one** hook but must leave the other declared and undefined: an
    abstract member with every operation implemented would owe nothing.

    **Certification takeaway:** "only methods can be abstract" was true up to PHP 8.3 and is
    false on the 8.4 baseline. Abstract properties are `public` or `protected` only, may be
    satisfied by a plain or hooked property, and follow the same widen-never-narrow visibility
    rule as methods.

    **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

## Exercise 7 · Expert challenge — abstract, or a throwing default?

**Objective:** Reproduce the two designs Symfony actually ships, and argue the trade-off from
the error each one produces.

**Context:** `AbstractAuthenticator implements AuthenticatorInterface` provides only
`createToken()` and leaves the other four interface methods unimplemented — without ever
writing the word `abstract` on them. `Command::execute()` takes the opposite route: it is
concrete and throws `LogicException('You must override the execute() method in the concrete
command class.')`, and the source comment explains that this is so `Command` can also be used
directly with `setCode()`.

**Starting point:**

```php
<?php
declare(strict_types=1);

interface Handler
{
    public function supports(string $type): bool;

    public function handle(string $payload): string;
}
```

**Task:** Build both designs.

1. `AbstractHandler implements Handler` that implements only `supports()` and leaves
   `handle()` alone. Do **not** redeclare `handle()` as abstract. Then write a subclass that
   forgets `handle()` and record the error.
2. `LenientHandler implements Handler` where `handle()` is concrete and throws
   `\LogicException`. Write a subclass that forgets to override it and record what happens.

Then state, in one sentence each, what each design guarantees and what it costs.

**Expected observation:** Design 1 fails when the subclass **loads**. Design 2 loads happily
and fails only when `handle()` is actually reached.

??? tip "Show a hint"
    An interface method that no class in the hierarchy has implemented is already an abstract
    requirement — the keyword adds nothing. So what is the difference between "no
    implementation exists" and "an implementation exists that throws"?

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    interface Handler
    {
        public function supports(string $type): bool;

        public function handle(string $payload): string;
    }

    abstract class AbstractHandler implements Handler
    {
        public function supports(string $type): bool
        {
            return 'default' === $type;
        }
        // handle() is deliberately absent: still a requirement, no keyword needed
    }

    abstract class LenientHandler implements Handler
    {
        public function supports(string $type): bool
        {
            return true;
        }

        public function handle(string $payload): string
        {
            throw new \LogicException('You must override handle() in the concrete class.');
        }
    }
    ```

    A subclass of `AbstractHandler` that omits `handle()` never loads:

    ```
    Fatal error: Class MyHandler contains 1 abstract method and must therefore be declared
    abstract or implement the remaining methods (Handler::handle)
    ```

    A subclass of `LenientHandler` that omits it loads fine, is registered as a service fine,
    passes a smoke test fine — and throws `LogicException` the first time a request reaches
    that code path.

    **Why it works:** an unimplemented interface method is *already* an abstract entry in the
    method table, so `AbstractHandler` must be declared `abstract` even though it never uses
    the keyword on a member. That is exactly the shape of `AbstractAuthenticator`, which
    implements 1 of the interface's 5 methods, and of
    `Symfony\Component\DependencyInjection\Extension\Extension`, which leaves
    `ExtensionInterface::load()` to each bundle.

    The trade-off in one line each. **Abstract** buys a *load-time* guarantee that the step
    exists, and costs you the ability to use the base class directly. **A throwing default**
    buys that flexibility — `Command` can be used concretely via `setCode()` — and downgrades
    the guarantee to a *runtime* exception on one code path.

    **Certification takeaway:** an abstract class does not need to write `abstract` on
    anything; partially implementing an interface is enough to require the keyword on the
    class. And "abstract versus a throwing default" is a real design decision about *when* the
    mistake is detected, not a style preference.

    **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authenticator/AbstractAuthenticator.php

---

<small>Back to the lesson: [Abstract Classes](abstract-classes.md) · Next: [Topic exam](abstract-classes-exam.md)</small>
</content>

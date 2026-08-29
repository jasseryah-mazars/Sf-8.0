# Topic Exam — Abstract Classes

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because the exam is built on
    near-misses rather than definitions.

    Theory: **[Abstract Classes](abstract-classes.md)** ·
    Practice: **[Guided exercises](abstract-classes-exercises.md)** ·
    Recall: **[Flashcards](abstract-classes-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4**.

## What `abstract` enforces

??? question "Question 1"
    A concrete class inherits an abstract method but does not implement it. What is the
    result?

    - A. Fatal error unless the class is itself declared `abstract`
    - B. The method silently returns `null` when called
    - C. It runs normally until the method is called
    - D. A deprecation notice

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual states that *"any class that contains at least one
        abstract method or property must also be abstract"*. PHP verifies this while linking
        the class and aborts with
        `Class X contains 1 abstract method and must therefore be declared abstract or
        implement the remaining methods (…)`.

        **B** invents a fallback PHP does not provide — an abstract method has no body at all,
        so there is nothing to return. **C** assumes the check is deferred to the call; it is
        not, and merely autoloading the file is enough to trigger the error. **D** understates
        the severity: this is a hard fatal, never a deprecation.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Question 2"
    In PHP 8.4, which of these can an abstract class do that an interface cannot?

    - A. Declare a constructor and hold stored instance state
    - B. Have multiple parents
    - C. Declare public method signatures
    - D. Declare constants

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** an abstract class is a class — it may define `__construct()`,
        promoted and plain properties that actually **store** values, and `private`/`protected`
        members. An interface can do none of that: it has no constructor and stores nothing.

        **B** is backwards: a class `extends` exactly **one** class, abstract or not, while an
        interface may `extends` several other interfaces. **C** is shared — both declare public
        method signatures. **D** is shared too; both may declare constants, typed since 8.3.

        One nuance that used to make this question easier and no longer does: **as of PHP 8.4
        an interface may declare properties** (`public string $slug { get; }`). So "only an
        abstract class can mention a property" is now false. The surviving distinction is
        *stored state and construction*, not the word "property".

        **Official reference:** https://www.php.net/manual/en/language.oop5.interfaces.php

??? question "Question 3"
    The template method pattern is best expressed in PHP by…

    - A. A concrete, often `final`, method that calls abstract hooks
    - B. An interface with no method bodies
    - C. A trait containing only static methods
    - D. A closure stored in a property

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the pattern fixes an invariant algorithm in the parent and defers only
        the variable steps. That requires a **body** in the parent (so an abstract class, not
        an interface) and a way to force the steps (abstract methods). `final` on the skeleton
        prevents a subclass from replacing the algorithm rather than customising a step.

        **B** cannot express it: an interface has no bodies, so there is no skeleton to fix.
        **C** is a different mechanism — a trait is horizontal copy-in reuse and is not a type,
        and static methods cannot participate in the polymorphic dispatch the pattern relies
        on. **D** describes a strategy/callback design, which is the *alternative* to the
        template method: Symfony's `Command::setCode()` is exactly that alternative.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Question 4"
    How many abstract classes can a single class extend?

    - A. Any number
    - B. Exactly one
    - C. Zero
    - D. Two

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** PHP has single class inheritance. A class `extends` exactly one class,
        and whether that class is abstract changes nothing. Multiple inheritance of *type* is
        provided by interfaces, and horizontal code reuse by traits.

        **A** describes interfaces, not classes. **C** is wrong as a general rule: a class may
        certainly extend one abstract class — and in Symfony most controllers do. **D** is the
        "PHP is a bit like C++" trap; no number other than one is possible.

        **Official reference:** https://www.php.net/manual/en/language.oop5.inheritance.php

## Failure stages

??? question "Question 5 · Code analysis"
    What does this script output?

    ```php
    abstract class Report {}

    try {
        new Report();
    } catch (\Error $e) {
        echo 'caught: ', $e->getMessage();
    }
    ```

    - A. Nothing — the script dies with an uncatchable fatal error
    - B. `caught: Cannot instantiate abstract class Report`
    - C. A `TypeError` is thrown instead and is not caught
    - D. Nothing — `Report` has no abstract methods, so `new` succeeds

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** instantiation is checked at **runtime** by the `new` opcode, which
        consults a single flag on the class entry and throws an ordinary `\Error`. Being a
        real exception object, it is catchable like any other.

        **A** confuses this with the *other* abstract-class failure: an unimplemented abstract
        member is a link-time fatal with no exception object, and that one truly cannot be
        caught. **C** names the wrong class — `TypeError` is a subclass of `Error` used for
        argument/return type failures, not for instantiation. **D** is the most tempting
        distractor: the `abstract` keyword blocks instantiation **on its own**, with or without
        abstract members.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Question 6 · Execution order"
    At which stage is each of these detected: (i) a subclass that leaves an abstract method
    unimplemented, and (ii) a `new` on an abstract class?

    - A. Both at runtime
    - B. Both while the class is linked
    - C. (i) while the class is linked, (ii) at runtime
    - D. (i) at runtime, (ii) while the class is linked

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** the completeness check runs when the class declaration is **linked** —
        compiled, or loaded by the autoloader — because the engine can count the remaining
        abstract entries in the method table from the declaration alone. The instantiation
        check needs a `new` expression to actually execute, so it happens at **runtime**.

        **A** would mean a half-defined class could exist and answer `instanceof` truthfully,
        which the engine refuses to allow. **B** is impossible for (ii): the engine cannot know
        at declaration time whether anyone will ever write `new`. **D** simply inverts the
        correct pairing, and is the version most often chosen under time pressure.

        The practical consequence is the blast radius. (i) takes the whole application down the
        moment the file is autoloaded; (ii) fails only the request that executed the `new`.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Question 7 · Debugging"
    CI reports:

    ```
    Fatal error: Access level to CsvImporter::parse() must be protected
    (as in class Importer) or weaker
    ```

    What was done wrong, and what is the minimal fix?

    - A. The implementation narrowed the visibility — declare it `protected` or `public`
    - B. The return type was widened — narrow it back
    - C. `CsvImporter` must be declared `abstract`
    - D. `parse()` must be declared `final` in the parent

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** implementing an abstract method is an override, and the manual states
        that visibility *"can be relaxed … but cannot be restricted"*. The message names the
        parent's level (`protected`) and says "or weaker", meaning `protected` or `public` are
        both acceptable. Someone wrote `private function parse()`.

        **B** describes a variance violation, which produces a completely different message
        beginning `Declaration of … must be compatible with …`. **C** would only be relevant if
        a method were missing entirely; here it exists, with the wrong visibility. **D** is
        contradictory — `final` on an abstract method is itself rejected with
        *"Cannot use the final modifier on an abstract method"*.

        **Official reference:** https://www.php.net/manual/en/language.oop5.visibility.php

## Modifiers and signatures

??? question "Question 8 · True or false"
    Declaring `abstract public function run(): void {}` — an abstract method with an empty
    body — is valid PHP.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — false

        **Explanation:** an abstract method *"simply declares the method's signature"* and
        cannot define an implementation. Any body, even an empty one, is rejected:

        ```
        Fatal error: Abstract function A::run() cannot contain body
        ```

        Two details worth being precise about, because both appear as distractors. First, this
        is a **compile-time fatal error**, not a *parse error* — the file parses cleanly, and
        the compiler rejects the declaration afterwards. Second, the fix is not to "empty the
        body further": if you want a default implementation, drop `abstract` and write an
        ordinary concrete method, which is exactly what `Command::execute()` does.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Question 9 · Multiple choice"
    Select all statements that are true in PHP 8.4.

    - A. `abstract final class C {}` is rejected by the compiler
    - B. `abstract private function f();` is rejected by the compiler
    - C. An abstract class must contain at least one abstract method
    - D. An abstract class may declare a constructor, constants and `final` methods

    ??? success "Show answer"
        **Correct answers:** A, B and D

        **Explanation:**
        **A** — `abstract` means "a subclass must override this", `final` means "a subclass may
        not". PHP rejects the combination by name:
        *"Cannot use the final modifier on an abstract class"*, and the equivalent message for
        a method.
        **B** — an abstract method declaration may only state `public` or `protected`. A
        `private` member is invisible to the subclass that would have to implement it, so the
        compiler reports *"Abstract function A::f() cannot be declared private"*.
        **D** — an abstract class is an ordinary class in every respect except instantiability.
        `Symfony\Component\DependencyInjection\Extension\Extension` is abstract and contains a
        `final public function getProcessedConfigs()`.

        **C** is the false one, and the most useful thing on this page to remember:
        `AbstractController` and `AbstractType` both declare **zero** abstract methods. The
        keyword alone makes a class non-instantiable.

        **Official reference:** https://www.php.net/manual/en/language.oop5.final.php

??? question "Question 10 · Code analysis"
    `Importer` declares `abstract protected function parse(string $raw): array;`. Which of
    these implementations in a subclass links successfully?

    ```php
    // 1
    public function parse(string $raw): array { return []; }
    // 2
    private function parse(string $raw): array { return []; }
    // 3
    protected function parse(string $raw, string $sep = ','): array { return []; }
    // 4
    protected function parse(string $raw, string $sep): array { return []; }
    ```

    - A. Only 1
    - B. 1 and 3
    - C. 1, 3 and 4
    - D. All four

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** implementing an abstract method is an override, so three rule families
        apply at once.

        **1 links:** visibility may be *relaxed*, and `protected` → `public` is a relaxation.
        **2 fails:** narrowing to `private` gives *"Access level to … must be protected (as in
        class Importer) or weaker"*. **3 links:** the manual's own example shows a child adding
        an optional parameter absent from the parent's signature; every call written against
        the parent still type-checks. **4 fails:** a **required** extra parameter breaks those
        calls, producing *"Declaration of … must be compatible with …"*.

        **A** forgets that optional parameters may be added. **C** conflates optional with
        required. **D** ignores both the visibility and the parameter rule.

        **Official reference:** https://www.php.net/manual/en/language.oop5.inheritance.php

??? question "Question 11 · Code analysis"
    Given `class TypedRows extends Rows` and `class TypedRaw extends Raw`, which of these
    implementations of an abstract method is legal?

    - A. Parent declares `: TypedRows`, the implementation declares `: Rows`
    - B. Parent declares `: Rows`, the implementation declares `: TypedRows`
    - C. Parent declares `(Raw $raw)`, the implementation declares `(TypedRaw $raw)`
    - D. Any signature — abstract methods are exempt from variance rules

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual is explicit that implementations of an abstract method
        *"follow the usual inheritance and signature compatibility rules"*. Return types are
        **covariant**, so an implementation may return a *narrower* type: `TypedRows` where
        `Rows` was promised over-delivers and every caller stays satisfied.

        **A** widens the return, which breaks every caller relying on `TypedRows`. **C**
        narrows a parameter, which refuses callers the contract explicitly allowed —
        parameters are **contravariant** and may only widen. **D** is the headline trap: there
        is no variance exemption for abstract methods; they are ordinary overrides.

        **Official reference:** https://www.php.net/manual/en/language.oop5.variance.php

## PHP 8.4 and edge cases

??? question "Question 12 · Edge case"
    Which statement about abstract properties in PHP 8.4 is correct?

    - A. They may be declared `public`, `protected` or `private`
    - B. They may be `public` or `protected`, and may be satisfied by a plain or a hooked property
    - C. They must always be satisfied by a property with hooks
    - D. They do not exist — only methods can be abstract

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** *"As of PHP 8.4, an abstract class may declare an abstract property,
        either public or protected"*, and *"an abstract property may be satisfied either by a
        standard property or by a property with defined hooks, corresponding to the required
        operation"*. Visibility follows the usual rule: a `protected` requirement may be
        satisfied from protected **or** public scope, but a `public` requirement may not be met
        by a `protected` property.

        **A** adds `private`, which is excluded for the same reason as private abstract
        methods — a subclass could not see it. **C** over-restricts: a plain
        `public string $label = 'x';` satisfies `abstract public string $label { get; }`
        perfectly, and the extra write capability it also provides is harmless. **D** was true
        up to PHP 8.3 and is the most convincing distractor on the 8.4 baseline.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Question 13 · Trap"
    An abstract class declares `abstract public string $slug { get; }`. A subclass provides
    nothing. What does the error message call the missing member?

    - A. A missing property, reported as `A::$slug`
    - B. An abstract **method**, reported as `A::$slug::get`
    - C. A missing hook, reported as `A::get`
    - D. Nothing — unimplemented abstract properties are silently `null`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the engine emits
        `Class C contains 1 abstract method and must therefore be declared abstract or
        implement the remaining methods (A::$slug::get)`. The requirement is counted among
        *abstract methods* and named with the `::get` suffix, which reveals the implementation
        detail: property hooks are stored as methods attached to a property name.

        **A** looks right but is not what the engine prints — and the distinction matters,
        because the wording tells you a property requirement and a method requirement are the
        same mechanism. **C** drops the property name, which the message always includes.
        **D** invents a silent fallback; the whole point of `abstract` is that there is none.

        **Official reference:** https://www.php.net/manual/en/language.oop5.property-hooks.php

??? question "Question 14 · Edge case"
    Which of these is **not** valid PHP 8.4?

    - A. A trait declaring an abstract method
    - B. An anonymous class extending an abstract class
    - C. `abstract enum Status {}`
    - D. `abstract readonly class Money {}`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** `abstract enum` is a **parse error** —
        *"syntax error, unexpected token \"enum\""*. An enum has a fixed, fully known set of
        cases, which is the opposite of leaving something to a subclass; enums cannot be
        extended at all.

        **A** is valid and idiomatic: a trait's abstract method is a requirement on the class
        that `use`s it, and the resulting error names the *using* class (`C::f`), not the
        trait. **B** is valid and is the shortest way to write a one-off implementation in a
        test. **D** is valid — readonly classes arrived in 8.2 and combine with `abstract`.
        Note the constraint that comes with it: a readonly class may not extend a non-readonly
        one, and a non-readonly class may not extend a readonly one.

        **Official reference:** https://www.php.net/manual/en/language.oop5.traits.php

## Design and Symfony practice

??? question "Question 15 · Code analysis"
    `AbstractAuthenticator implements AuthenticatorInterface` and defines only
    `createToken()`. The interface requires five methods. Must the class be declared
    `abstract`, and must the four remaining methods be redeclared with the `abstract` keyword?

    - A. Yes to both — every unimplemented method must be redeclared `abstract`
    - B. Yes it must be abstract; no, the interface methods are already requirements
    - C. No to both — implementing part of an interface is enough
    - D. No — only the class needs the keyword when it declares its *own* abstract members

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** an interface method that no class in the hierarchy has implemented is
        already an abstract entry in the method table. The class therefore *contains* abstract
        members and must carry the keyword, but redeclaring them is unnecessary. That is
        exactly how Symfony ships it: `AbstractAuthenticator` writes the word `abstract` only
        on the class, and `Symfony\Component\DependencyInjection\Extension\Extension` does the
        same, leaving `ExtensionInterface::load()` to each bundle.

        **A** invents a requirement; redeclaring is legal but purely documentary. **C** ignores
        the fact that the debt is still outstanding — such a class cannot be instantiated and
        will not link without the keyword. **D** is the same mistake stated differently:
        inherited requirements count exactly like locally declared ones.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authenticator/AbstractAuthenticator.php

??? question "Question 16 · Expert trap"
    A class implements an abstract method `render()` and its body begins with
    `return parent::render();`. What happens?

    - A. Compile-time fatal error when the class is declared
    - B. Runtime `Error`: `Cannot call abstract method A::render()`
    - C. It returns `null`, because an abstract method has an empty body
    - D. Infinite recursion — `parent::render()` dispatches back to the child

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the class itself is perfectly well formed — it implements everything it
        owes, so it links without complaint. The problem only appears when the method actually
        runs and reaches a `parent::` call to something that has no body:
        `Uncaught Error: Cannot call abstract method A::render()`. Being an `Error`, it is
        catchable.

        **A** is the trap: nothing in the declaration is wrong, so no declaration-time check can
        fire. **C** repeats the "abstract means empty" misconception — there is no body at all,
        not an empty one. **D** misreads `parent::`, which is an explicit non-virtual call to
        the parent's implementation; it never dispatches back down to the child.

        This is a common refactoring accident: a concrete parent method is promoted to
        `abstract`, and a subclass that used to legitimately call `parent::` is left behind.

        **Official reference:** https://www.php.net/manual/en/language.oop5.abstract.php

??? question "Question 17 · Scenario"
    A shared library ships an abstract base class. In a minor release, the maintainer adds one
    new `abstract` method to it. What happens to applications that extend it?

    - A. Nothing until the new method is called
    - B. Every existing subclass fails to link, with a fatal error the moment its file is autoloaded
    - C. PHP inserts a default no-op implementation inherited from the base class
    - D. Only subclasses that also implement an interface are affected

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** adding an abstract method adds debt to every descendant at once. Each
        subclass now contains one unimplemented abstract member and fails the link-time
        completeness check as soon as it is autoloaded — before any call, and with no way to
        catch it. This is the same breakage profile as adding a method to a published
        interface, which is why both are major-version changes under Symfony's
        [backward-compatibility promise](../architecture/bc-promise.md).

        **A** assumes laziness the engine does not have. **C** describes the *alternative*
        design the maintainer could have chosen — a concrete method with a default (or throwing)
        body, as `Command::execute()` does — but PHP never inserts one for you. **D** is
        unrelated: interfaces are a separate mechanism and change nothing here.

        **Official reference:** https://symfony.com/doc/8.0/contributing/code/bc.html

---

<small>Back to the lesson: [Abstract Classes](abstract-classes.md) · [Guided exercises](abstract-classes-exercises.md) · [Review flashcards](abstract-classes-flashcards.md)</small>
</content>

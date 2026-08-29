# Flashcards — SPL, Iteration & Generators

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[SPL — Standard PHP Library](spl.md)** ·
    Practice: **[Guided exercises](spl-exercises.md)** ·
    Test: **[Topic exam](spl-exam.md)**

## Definitions and roles

??? question "What does the SPL actually give you, in one sentence?"
    Think before revealing the answer.

    ??? success "Show answer"
        A set of **interfaces** that let your objects use native syntax (`foreach`, `count()`,
        `$obj[$k]`), plus ready-made **data structures** and **iterator decorators** built on
        those interfaces.

        **Why it matters:** it frames every question on the topic. If the question is about
        syntax, the answer is an interface; if it is about order or memory, the answer is a
        structure or an iterator.

        **Official reference:** https://www.php.net/manual/en/book.spl.php

??? question "What is `Traversable`, and why can you not implement it on a concrete class?"
    Think before revealing the answer.

    ??? success "Show answer"
        The empty marker interface that `foreach` looks for. The manual calls it an "abstract
        base interface that cannot be implemented alone" — it must be reached through
        `Iterator` or `IteratorAggregate`. Since PHP 8.0 an **abstract** class may declare
        `implements Traversable`, but its concrete children must still pick one of the two.

        **Why it matters:** `iterable` is `array|Traversable`, and every SPL iterator type
        hint in Symfony resolves to it. Trying to implement it directly is a fatal error, not
        a warning.

        **Official reference:** https://www.php.net/manual/en/class.traversable.php

??? question "Name the five methods of `Iterator`, in the order `foreach` calls them."
    Think before revealing the answer.

    ??? success "Show answer"
        `rewind()`, then `valid()`, `current()`, `key()`, then per step `next()`, `valid()`,
        `current()`, `key()`.

        **Why it matters:** execution-order questions are answered from this single line.
        Note `valid()` runs once more than there are elements — the final `false` is what ends
        the loop.

        **Official reference:** https://www.php.net/manual/en/class.iterator.php

??? question "How many methods does `IteratorAggregate` require, and what must the return type be?"
    Think before revealing the answer.

    ??? success "Show answer"
        Exactly one: `getIterator(): Traversable`. Returning an `array` is a runtime
        `TypeError`; returning a `Generator` is fine because `Generator` implements `Iterator`.

        **Why it matters:** one method versus five is the reason almost every Symfony
        collection (`Finder`, `ParameterBag`, forms) is an aggregate rather than an iterator.

        **Official reference:** https://www.php.net/manual/en/class.iteratoraggregate.php

??? question "Can a class implement both `Iterator` and `IteratorAggregate`?"
    Think before revealing the answer.

    ??? success "Show answer"
        No. PHP refuses at compile time: *Class X cannot implement both Iterator and
        IteratorAggregate at the same time*.

        **Why it matters:** it kills the "why not both?" distractor instantly. The engine would
        have no rule for choosing between iterating the object and iterating its delegate.

        **Official reference:** https://www.php.net/manual/en/class.iteratoraggregate.php

??? question "Which interface does `count($obj)` need, and what happens without it?"
    Think before revealing the answer.

    ??? success "Show answer"
        `Countable`, with a `count(): int` method. Without it, PHP 8 throws
        `TypeError: count(): Argument #1 ($value) must be of type Countable|array`.

        **Why it matters:** the pre-8.0 answer was "a warning and the value 1" — an outdated
        answer that still appears in question banks.

        **Official reference:** https://www.php.net/manual/en/class.countable.php

??? question "What does `Stringable` do that no other interface does?"
    Think before revealing the answer.

    ??? success "Show answer"
        It marks a class as having `__toString()` — and it is applied **implicitly** to any
        class defining that method, though the manual says it can and should be declared
        explicitly. Its purpose is the `string|Stringable` parameter type.

        **Why it matters:** it is the one predefined interface you can satisfy by accident,
        which makes "must be declared explicitly to work" a reliable false statement.

        **Official reference:** https://www.php.net/manual/en/class.stringable.php

??? question "What does `JsonSerializable` control?"
    Think before revealing the answer.

    ??? success "Show answer"
        What `json_encode()` sees: the `jsonSerialize()` return value is encoded instead of the
        object's public properties. `SplFixedArray` implements it as of PHP 8.1.

        **Why it matters:** it is the fourth "native syntax" interface next to `ArrayAccess`,
        `Countable` and the iteration pair — one interface, one language feature.

        **Official reference:** https://www.php.net/manual/en/class.jsonserializable.php

## ArrayAccess mechanics

??? question "Name the four `ArrayAccess` methods and the syntax that triggers each."
    Think before revealing the answer.

    ??? success "Show answer"
        `offsetGet()` for a read `$o[$k]`, `offsetSet()` for a write `$o[$k] = $v` (and for the
        append form `$o[] = $v`, where `$offset` arrives as `null`), `offsetExists()` for
        `isset()`/`empty()`, `offsetUnset()` for `unset()`.

        **Why it matters:** the append case is the one people forget; the `null` offset is the
        documented signal to push.

        **Official reference:** https://www.php.net/manual/en/class.arrayaccess.php

??? question "Which methods run for `isset($o['k'])` versus `empty($o['k'])` on an `ArrayAccess` object?"
    Think before revealing the answer.

    ??? success "Show answer"
        `isset()` calls **only** `offsetExists()`. `empty()` calls `offsetExists()` first, and
        `offsetGet()` **only if** `offsetExists()` returned `true`.

        **Why it matters:** it is a documented, testable difference, and it explains why
        `empty()` on a missing key never touches your getter.

        **Official reference:** https://www.php.net/manual/en/arrayaccess.offsetexists.php

??? question "What does `$o['k'] ?? 'default'` do on an `ArrayAccess` object?"
    Think before revealing the answer.

    ??? success "Show answer"
        It behaves like `isset()` on the left-hand side: `offsetExists('k')` first, then
        `offsetGet('k')` only if that returned `true`. If your `offsetExists()` is written with
        `isset()`, a stored `null` reports "absent" and the default wins.

        **Why it matters:** implement `offsetExists()` with `array_key_exists()` whenever
        `null` is a legitimate stored value, or `??` will silently lie about your data.

        **Official reference:** https://www.php.net/manual/en/arrayaccess.offsetexists.php

## Generators

??? question "What does calling a function that contains `yield` actually do?"
    Think before revealing the answer.

    ??? success "Show answer"
        It runs **none** of the body. It immediately returns a `Generator` object; the body
        starts executing on the first advance (`current()`, `next()`, `send()` or `foreach`).

        **Why it matters:** it is why Symfony's `LazyIterator::getIterator()` is a generator —
        the expensive work is deferred to the moment the consumer loops.

        **Official reference:** https://www.php.net/manual/en/language.generators.overview.php

??? question "Is `Generator` an `Iterator`, an `IteratorAggregate`, or neither?"
    Think before revealing the answer.

    ??? success "Show answer"
        `final class Generator implements Iterator`. You cannot extend it, cannot `new` it, and
        cannot make your own class "a generator" — only the `yield` keyword produces one.

        **Why it matters:** it is why a generator can be passed straight to `LimitIterator`
        (which demands an `Iterator`) while an `IteratorAggregate` cannot.

        **Official reference:** https://www.php.net/manual/en/class.generator.php

??? question "What exactly happens on a second `foreach` over an already-consumed generator?"
    Think before revealing the answer.

    ??? success "Show answer"
        `Exception: Cannot traverse an already closed generator`. It does **not** silently
        iterate zero times. An explicit `rewind()` after advancing gives the sibling message
        *Cannot rewind a generator that was already run*.

        **Why it matters:** "nothing happens" is the popular wrong answer, and the two distinct
        messages are used to build near-miss distractors.

        **Official reference:** https://www.php.net/manual/en/language.generators.comparison.php

??? question "How do you make a lazy sequence re-iterable without buffering it?"
    Think before revealing the answer.

    ??? success "Show answer"
        Wrap the **factory**, not the generator: an `IteratorAggregate` whose `getIterator()`
        calls the factory and returns a fresh `Generator` each time. Symfony ships exactly
        that as `RewindableGenerator` (`IteratorAggregate` + `Countable`).

        **Why it matters:** it is the canonical fix for "handlers iterated twice", and the
        reason a tagged-service iterator survives a second `foreach`.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/Argument/RewindableGenerator.php

??? question "What keys does a generator produce when you never yield one explicitly?"
    Think before revealing the answer.

    ??? success "Show answer"
        Sequential integers starting at `0`, "just as with a non-associative array". You can
        yield your own with `yield $key => $value`.

        **Why it matters:** those auto-keys are what collide during `yield from` delegation and
        during `iterator_to_array()`.

        **Official reference:** https://www.php.net/manual/en/language.generators.syntax.php

??? question "Does `yield from` renumber the keys of the inner iterable?"
    Think before revealing the answer.

    ??? success "Show answer"
        No — it **preserves** them, and the outer generator keeps its own counter running. So
        the same key can appear twice in one sequence.

        **Why it matters:** the manual attaches an explicit caution to this: converting such a
        generator with `iterator_to_array()` (keys preserved by default) silently drops the
        earlier duplicates.

        **Official reference:** https://www.php.net/manual/en/language.generators.syntax.php

??? question "What does `yield from` evaluate to?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **return value of the inner generator** — `$result = yield from inner();` gives you
        whatever `inner()` returned after its last `yield`.

        **Why it matters:** it is how generator delegation carries a final result back, the
        mechanism behind coroutine-style code and the reason `return` inside a generator is
        not dead code.

        **Official reference:** https://www.php.net/manual/en/language.generators.syntax.php

??? question "When is `Generator::getReturn()` legal?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only after the generator has finished. Calling it earlier throws *Cannot get return
        value of a generator that hasn't returned*.

        **Why it matters:** the exam pairs it with a half-consumed generator to see whether you
        know it throws rather than returning `null`.

        **Official reference:** https://www.php.net/manual/en/generator.getreturn.php

??? question "What does `Generator::send($v)` do, and do you need to prime the generator first?"
    Think before revealing the answer.

    ??? success "Show answer"
        It makes `$v` the value of the currently paused `yield` expression, resumes execution,
        and **returns the next yielded value**. No priming is needed: the manual states that if
        the generator has not started, `send()` advances it to the first `yield` itself.

        **Why it matters:** "you must call `next()` first, like in Python" is a documented
        non-requirement, which makes it a clean false statement.

        **Official reference:** https://www.php.net/manual/en/generator.send.php

??? question "What is the default of `iterator_to_array()`'s second parameter?"
    Think before revealing the answer.

    ??? success "Show answer"
        `preserve_keys: true`. Duplicate keys therefore overwrite each other and the result can
        be shorter than the iterator. Pass `false` to renumber and keep every value. Since PHP
        8.2 the first parameter also accepts a plain `array`.

        **Why it matters:** it is half of the most-asked generator trap; the other half is that
        `yield from` preserves keys.

        **Official reference:** https://www.php.net/manual/en/function.iterator-to-array.php

## Data structures

??? question "What do `SplStack` and `SplQueue` have in common, and what separates them?"
    Think before revealing the answer.

    ??? success "Show answer"
        Both **extend `SplDoublyLinkedList`**. `SplStack` sets the iterator mode to
        `IT_MODE_LIFO`, `SplQueue` to `IT_MODE_FIFO`; `SplQueue` adds the
        `enqueue()`/`dequeue()` vocabulary.

        **Why it matters:** "same class, different iteration constant" answers any question
        about their relationship, and explains why both also give you `ArrayAccess`,
        `Countable` and `Iterator`.

        **Official reference:** https://www.php.net/manual/en/class.spldoublylinkedlist.php

??? question "Does `foreach` empty an `SplStack`? Does it empty an `SplMinHeap`?"
    Think before revealing the answer.

    ??? success "Show answer"
        Stack: **no** — the linked list defaults to `IT_MODE_KEEP`, so `count()` is unchanged
        (`IT_MODE_DELETE` opts into destructive iteration). Heap: **yes** — heap iteration
        extracts the root each step, so the heap is empty when the loop ends.

        **Why it matters:** one code-analysis question can test both in the same snippet.
        `clone` the heap first if you need its contents twice.

        **Official reference:** https://www.php.net/manual/en/class.splheap.php

??? question "What must `SplHeap::compare($a, $b)` return, and which ordering does `$a <=> $b` give?"
    Think before revealing the answer.

    ??? success "Show answer"
        `protected int compare(mixed $value1, mixed $value2)` — positive when `value1` is
        greater, `0` when equal, negative otherwise. The greatest element sits at the root, so
        `$a <=> $b` builds a **max-heap** and `$b <=> $a` a min-heap.

        **Why it matters:** one flipped spaceship operator inverts the whole structure, and
        throwing from `compare()` can corrupt the heap (recoverable only via
        `recoverFromCorruption()`).

        **Official reference:** https://www.php.net/manual/en/splheap.compare.php

??? question "What is the order of two `SplPriorityQueue` entries inserted with the same priority?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Undefined.** The manual says it "may differ from the order in which they have been
        inserted" — the class is a max heap, not a stable sort. Force determinism with a
        composite priority such as `[$priority, $decreasingSerial]`.

        **Why it matters:** "FIFO among equals" is the single most attractive wrong answer on
        this class, and the composite-priority fix is the expected expert response.

        **Official reference:** https://www.php.net/manual/en/class.splpriorityqueue.php

??? question "What do `EXTR_DATA`, `EXTR_PRIORITY` and `EXTR_BOTH` change, and which is the default?"
    Think before revealing the answer.

    ??? success "Show answer"
        They set what `current()`, `top()` and `extract()` return: the payload, the priority, or
        an associative array `['data' => …, 'priority' => …]`. **`EXTR_DATA` is the default.**

        **Why it matters:** `EXTR_BOTH` returns a *named* array — a distractor showing `[0]`
        and `[1]` is wrong about the shape, not only about the mode.

        **Official reference:** https://www.php.net/manual/en/splpriorityqueue.setextractflags.php

??? question "Two things `SplObjectStorage` can be — and what its keys really are."
    Think before revealing the answer.

    ??? success "Show answer"
        A **set** of objects (ignore the data) and a **map** from object to data. The key is
        object **identity**, the same identity `spl_object_id()` reports — not equality, not a
        hash of the contents.

        **Why it matters:** it is the only standard container that can key by object; plain
        array keys are `int|string` only.

        **Official reference:** https://www.php.net/manual/en/class.splobjectstorage.php

??? question "What is the relationship between `attach()` and `offsetSet()` on `SplObjectStorage`?"
    Think before revealing the answer.

    ??? success "Show answer"
        They are **aliases** — `$s->attach($o, $d)` and `$s[$o] = $d` are the same call. Both
        replace the data if the object is already stored, leaving `count()` unchanged. Same
        pairing for `detach()`/`offsetUnset()` and `contains()`/`offsetExists()`. The manual
        marks the three older spellings as deprecated from PHP 8.5; on the PHP 8.4 baseline
        both remain valid.

        **Why it matters:** a question can use either spelling, and "attaching twice makes
        count 2" is false because a set stores each identity once.

        **Official reference:** https://www.php.net/manual/en/splobjectstorage.attach.php

??? question "During `foreach` over an `SplObjectStorage`, what is the value — and where is the attached data?"
    Think before revealing the answer.

    ??? success "Show answer"
        The value is the **object**; the keys are sequential integers. The attached data comes
        from `getInfo()` (or equivalently `$storage[$object]`).

        **Why it matters:** the intuitive guess — "the loop gives me object ⇒ data pairs" — is
        wrong, and reading `getInfo()` is the documented way to pair them up.

        **Official reference:** https://www.php.net/manual/en/class.splobjectstorage.php

??? question "Three things that make `SplFixedArray` different from a plain array."
    Think before revealing the answer.

    ??? success "Show answer"
        Fixed size (resize explicitly with `setSize()`), **integer keys only** within range, and
        lower memory use. On PHP 8.4 an out-of-range index throws `OutOfBoundsException` and a
        non-integer key throws `TypeError`.

        **Why it matters:** it is the only SPL structure whose selling point is memory, and its
        exception types changed across 8.1 and 8.4 — prime version-trap material.

        **Official reference:** https://www.php.net/manual/en/class.splfixedarray.php

??? question "Which iteration interface does `SplFixedArray` implement today, and which did it implement before?"
    Think before revealing the answer.

    ??? success "Show answer"
        `IteratorAggregate` since PHP 8.0; it implemented `Iterator` before that. It also
        implements `ArrayAccess`, `Countable` and (since 8.1) `JsonSerializable`.

        **Why it matters:** code calling `$fixed->rewind()` or `$fixed->current()` broke on the
        8.0 upgrade — a concrete example of an interface change being a BC break.

        **Official reference:** https://www.php.net/manual/en/class.splfixedarray.php

## Iterator decorators

??? question "Which decorator turns any `Traversable` into an `Iterator`, and when do you need it?"
    Think before revealing the answer.

    ??? success "Show answer"
        `IteratorIterator`. You need it whenever a decorator demands an `Iterator` — such as
        `LimitIterator` or `FilterIterator` — and all you have is an `IteratorAggregate`.

        **Why it matters:** Symfony's `Finder` does exactly this before appending lazy
        sub-iterators to an `AppendIterator`.

        **Official reference:** https://www.php.net/manual/en/class.iteratoriterator.php

??? question "What are `LimitIterator`'s constructor parameters and their defaults?"
    Think before revealing the answer.

    ??? success "Show answer"
        `__construct(Iterator $iterator, int $offset = 0, int $limit = -1)` — `-1` meaning "no
        limit". It **forwards the inner keys unchanged**, and throws a `ValueError` for a
        negative offset or a limit below `-1`.

        **Why it matters:** "the keys get renumbered" is a common wrong assumption, and the
        offset/limit pair is easy to swap under time pressure.

        **Official reference:** https://www.php.net/manual/en/limititerator.construct.php

??? question "What does a `CallbackFilterIterator` callback receive and return?"
    Think before revealing the answer.

    ??? success "Show answer"
        Up to three arguments — `$current`, `$key`, `$iterator` — and returns `true` to
        **accept** the element. Rejected elements are skipped but the surviving keys are
        preserved, so the result is sparse.

        **Why it matters:** the argument order (value first, key second) is the inverse of many
        array callbacks, and the return polarity is an easy trap to invert.

        **Official reference:** https://www.php.net/manual/en/callbackfilteriterator.construct.php

??? question "What is `RecursiveIteratorIterator`'s default mode, and what are the alternatives?"
    Think before revealing the answer.

    ??? success "Show answer"
        `LEAVES_ONLY` — containers are traversed but never emitted. `SELF_FIRST` emits a parent
        before its children; `CHILD_FIRST` emits children before the parent. The optional third
        argument accepts `CATCH_GET_CHILD` to swallow exceptions from `getChildren()`.

        **Why it matters:** "my directories are missing" is always the default mode. Symfony's
        `Finder` chooses `SELF_FIRST` so directory filters can run before descending.

        **Official reference:** https://www.php.net/manual/en/recursiveiteratoriterator.construct.php

??? question "`AppendIterator` versus `MultipleIterator` — what is the difference?"
    Think before revealing the answer.

    ??? success "Show answer"
        `AppendIterator` runs its inner iterators **one after another** (concatenation);
        `MultipleIterator` runs them **in parallel**, emitting one tuple per step, governed by
        `MIT_NEED_ALL`/`MIT_NEED_ANY` and `MIT_KEYS_NUMERIC`/`MIT_KEYS_ASSOC`.

        **Why it matters:** sequence versus zip is the whole distinction, and `AppendIterator`
        does not renumber keys — converting it with `iterator_to_array()` loses colliding ones.

        **Official reference:** https://www.php.net/manual/en/class.multipleiterator.php

??? question "What does `CachingIterator` buy you over the iterator it wraps?"
    Think before revealing the answer.

    ??? success "Show answer"
        It reads one element ahead, so `hasNext()` can tell you whether the current element is
        the last one — the classic "no separator after the final item" problem. With
        `FULL_CACHE` it also keeps everything it has seen.

        **Why it matters:** it is the SPL answer to look-ahead, which a plain `Iterator` cannot
        provide because it only knows the current position.

        **Official reference:** https://www.php.net/manual/en/class.cachingiterator.php

??? question "Which SPL pieces does Symfony's `Finder` compose?"
    Think before revealing the answer.

    ??? success "Show answer"
        `Finder` is an `\IteratorAggregate` + `\Countable`. Its walk uses a
        `RecursiveDirectoryIterator` flattened by a `\RecursiveIteratorIterator` in
        `SELF_FIRST` mode, combined through `\AppendIterator` and `\IteratorIterator` over a
        lazy generator, and `count()` is `iterator_count($this->getIterator())`.

        **Why it matters:** it is the reference implementation of "compose iterators, never
        materialise" — and a realistic source of Symfony-flavoured SPL questions.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Finder/Finder.php

## Mnemonics

??? question "One phrase for choosing between `Iterator` and `IteratorAggregate`."
    Think before revealing the answer.

    ??? success "Show answer"
        **"Drive it yourself, or hand over the keys."** `Iterator` = you drive, five methods.
        `IteratorAggregate` = you hand over an iterator, one method.

        **Why it matters:** it also encodes the exclusivity — you cannot both drive and hand
        over the keys, which is why implementing both is a fatal error.

        **Official reference:** https://www.php.net/manual/en/class.iteratoraggregate.php

??? question "One phrase for the generator lifecycle."
    Think before revealing the answer.

    ??? success "Show answer"
        **"One reel, one showing."** A generator is a single pass: it plays lazily, and once it
        has run out it is closed — traversing it again throws. To watch again, thread a new
        reel by calling the function again.

        **Why it matters:** it carries laziness *and* single use, the two facts every generator
        question is built on.

        **Official reference:** https://www.php.net/manual/en/language.generators.comparison.php

??? question "One phrase for what `foreach` does to each SPL container."
    Think before revealing the answer.

    ??? success "Show answer"
        **"Heaps and priority queues are eaten; lists and storages are visited."** Heap-family
        iteration extracts; `SplDoublyLinkedList` (stack/queue) and `SplObjectStorage`
        iteration leaves the contents in place.

        **Why it matters:** the `count()` after the loop is exactly what code-analysis
        questions print.

        **Official reference:** https://www.php.net/manual/en/class.splheap.php

---

<small>Back to the lesson: [SPL — Standard PHP Library](spl.md) · [Retake the topic exam](spl-exam.md) · Continue to the next topic: [Web Security Fundamentals](web-security.md)</small>

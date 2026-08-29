# Topic Exam — SPL, Iteration & Generators

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because this topic is tested
    through near-misses: `Iterator` vs `IteratorAggregate`, `attach()` vs `offsetSet()`,
    "consumes the structure" vs "leaves it intact".

    Theory: **[SPL — Standard PHP Library](spl.md)** ·
    Practice: **[Guided exercises](spl-exercises.md)** ·
    Recall: **[Flashcards](spl-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4**, the minimum version required by Symfony 8.

## The iteration interfaces

??? question "Question 1"
    Which methods must a class implement to satisfy the `Iterator` interface?

    - A. `current`, `key`, `next`, `rewind`, `valid`
    - B. `getIterator`
    - C. `count`, `offsetGet`
    - D. `next`, `prev`, `valid`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `Iterator` declares exactly five methods — `current()`, `key()`,
        `next()`, `rewind()` and `valid()`. Miss one and the class is abstract-by-omission:
        PHP raises a fatal error at compile time.

        **B** is the whole of `IteratorAggregate`, the *other* branch of `Traversable`, not
        `Iterator`. **C** mixes `Countable::count()` with `ArrayAccess::offsetGet()` — two
        unrelated interfaces that have nothing to do with `foreach`. **D** invents `prev()`:
        SPL iteration is forward-only, and no predefined iteration interface declares a
        backwards step (`SplDoublyLinkedList` has `prev()`, but that is a class method, not
        part of `Iterator`).

        **Official reference:** https://www.php.net/manual/en/class.iterator.php

??? question "Question 2 · Execution order"
    A class implements `Iterator` and logs every call. Which sequence does the engine
    produce for the **first** pass of `foreach ($it as $k => $v) { ... }`?

    - A. `rewind`, `current`, `key`, `valid`
    - B. `rewind`, `valid`, `current`, `key`
    - C. `valid`, `rewind`, `current`, `key`
    - D. `rewind`, `next`, `valid`, `current`, `key`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `foreach` first calls `rewind()` once, then `valid()` to ask whether
        there is anything at the cursor, and only then reads `current()` and `key()` for the
        loop body. Each following pass is `next()`, `valid()`, `current()`, `key()`, and the
        loop ends after a `next()`/`valid()` pair that returns `false`. The manual prints
        exactly this trace in the `Iterator` example.

        **A** omits `valid()` before the first read — that would read a cursor nobody checked,
        and an empty collection would explode. **C** inverts the two opening calls: `rewind()`
        is what makes the cursor meaningful, so it must come first. **D** inserts a `next()`
        before the first element, which would silently skip element zero.

        **Official reference:** https://www.php.net/manual/en/class.iterator.php

??? question "Question 3 · True or false"
    A concrete (non-abstract) class may declare `implements Traversable` directly, as long as
    it also defines `current()` and `valid()`.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — false

        **Explanation:** `Traversable` is documented as an "abstract base interface that
        cannot be implemented alone"; it must be reached through `Iterator` or
        `IteratorAggregate`. Writing `class T implements Traversable {}` is a fatal error:
        *Class T must implement interface Traversable as part of either Iterator or
        IteratorAggregate*. Adding `current()`/`valid()` changes nothing — the engine checks
        the *interface* graph, not the method names.

        The precise 8.0+ nuance the exam can build on: since PHP 8.0 an **abstract** class may
        write `implements Traversable`, but every concrete class extending it must still
        implement `Iterator` or `IteratorAggregate`. So the restriction is relaxed for
        abstract declarations only, which is why option A stays false.

        **Official reference:** https://www.php.net/manual/en/class.traversable.php

??? question "Question 4 · Code analysis"
    ```php
    final class Feed implements IteratorAggregate
    {
        public function getIterator(): Traversable
        {
            return ['a', 'b'];
        }
    }

    foreach (new Feed() as $item) { echo $item; }
    ```
    What happens?

    - A. It prints `ab` — arrays are iterable, so PHP accepts them.
    - B. A `TypeError`: the return value must be of type `Traversable`, array returned.
    - C. It prints nothing and the loop is skipped.
    - D. A fatal error at compile time, before the loop runs.

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `getIterator()` is declared `: Traversable`, and an `array` is not a
        `Traversable` — it is a primitive type that `foreach` handles by a different code
        path. The return type is checked when the method actually returns, so the failure is a
        runtime `TypeError`: *Feed::getIterator(): Return value must be of type Traversable,
        array returned*. Wrap it (`new ArrayIterator([...])`) or `yield from` it instead.

        **A** confuses "iterable" (`array|Traversable`) with `Traversable`: only the second is
        an interface an object can satisfy. **C** describes what a silently-empty iterator
        would do; PHP does not silently discard a type violation. **D** is wrong about
        *when*: return types are enforced at call time, not at compile time, so the class
        declaration itself is perfectly legal.

        **Official reference:** https://www.php.net/manual/en/class.iteratoraggregate.php

??? question "Question 5 · Multiple answers"
    Which statements about `IteratorAggregate` are correct? (Choose all that apply.)

    - A. It requires exactly one method, `getIterator()`.
    - B. `getIterator()` may return a `Generator`, because a generator is a `Traversable`.
    - C. `getIterator()` is called once per `foreach` over the object.
    - D. A class may implement both `Iterator` and `IteratorAggregate` to get both behaviours.

    ??? success "Show answer"
        **Correct answer:** A, B and C

        **Explanation:** **A** — `IteratorAggregate` declares only `getIterator(): Traversable`.
        **B** — a generator function returns a `Generator`, and `Generator` is `final` and
        `implements Iterator`, therefore a `Traversable`; `yield from $this->items;` inside
        `getIterator()` is the idiomatic one-method collection. **C** — each `foreach` over
        the object calls `getIterator()` again, which is exactly why an aggregate that builds
        a fresh generator each time is re-iterable while a bare generator is not.

        **D** is wrong: `Iterator` and `IteratorAggregate` are mutually exclusive by design.
        PHP rejects a class implementing both with *Class X cannot implement both Iterator and
        IteratorAggregate at the same time* — the engine would not know whether to iterate the
        object itself or the delegate.

        **Official reference:** https://www.php.net/manual/en/class.iteratoraggregate.php

## ArrayAccess and Countable

??? question "Question 6"
    Enabling the `$obj[$key]` syntax on your own class requires implementing…

    - A. `ArrayAccess`
    - B. `Countable`
    - C. `Iterator`
    - D. `Stringable`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `ArrayAccess` is the interface that maps bracket syntax onto four
        methods: `offsetExists()`, `offsetGet()`, `offsetSet()` and `offsetUnset()`. Nothing
        else in PHP unlocks `$obj[$k]` — there is no magic method for dimensions.

        **B** unlocks `count($obj)` only. **C** unlocks `foreach` only. **D** unlocks string
        contexts (`"$obj"`, `string|Stringable` parameters) only. Each interface buys exactly
        one syntax, which is the design point of the SPL predefined interfaces.

        **Official reference:** https://www.php.net/manual/en/class.arrayaccess.php

??? question "Question 7 · Code analysis"
    ```php
    $bag = new Bag();          // implements ArrayAccess, logs every call
    var_dump(isset($bag['a']));
    ```
    Which method(s) does the engine call?

    - A. `offsetGet('a')` only
    - B. `offsetExists('a')` only
    - C. `offsetExists('a')` then `offsetGet('a')`
    - D. `offsetGet('a')` then a null check

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual states it explicitly: `offsetExists()` "is executed when
        using `isset()` or `empty()` on objects implementing `ArrayAccess`". For `isset()`
        that is the *only* call — the return value is cast to `bool` and returned.

        **C** describes `empty($bag['a'])`, not `isset()`: `empty()` calls `offsetExists()`
        first and then `offsetGet()` **only if** `offsetExists()` returned `true`. **A** and
        **D** describe a plain read (`$bag['a']`), which calls `offsetGet()` and never
        consults `offsetExists()` — which is why reading a missing offset on your own class
        raises whatever *your* `offsetGet()` decides to raise, not a PHP warning.

        **Official reference:** https://www.php.net/manual/en/arrayaccess.offsetexists.php

??? question "Question 8 · Expert trap"
    ```php
    // offsetExists() is implemented as: return isset($this->data[$offset]);
    // $this->data === ['n' => null]
    var_dump($bag['n'] ?? 'default');
    ```
    What is printed, and which methods are called?

    - A. `NULL` — `offsetGet()` is called and returns `null`.
    - B. `string(7) "default"` — `offsetExists()` returns `false`, so `offsetGet()` is never called.
    - C. `string(7) "default"` — `offsetExists()` then `offsetGet()` are both called.
    - D. A warning "Undefined array key" then `NULL`.

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `??` behaves like `isset()` on the left-hand side, so on an
        `ArrayAccess` object it calls `offsetExists()` first and only reaches `offsetGet()`
        when that returned `true`. Here `offsetExists()` was implemented with `isset()`, and
        `isset($this->data['n'])` is `false` for a stored `null` — so the operator short-
        circuits to `'default'` and `offsetGet()` is never entered. The bug class this creates
        is real: a legitimately stored `null` becomes indistinguishable from a missing key.
        Implement `offsetExists()` with `array_key_exists()` when `null` is a valid value.

        **A** would be true only if `??` read the value directly, which it does not. **C** is
        the call sequence you get when the key *does* exist — with a stored `null` the answer
        would still be `'default'`, but for the different reason that `offsetGet()` returned
        `null`. **D** describes plain array behaviour; `??` deliberately suppresses that
        warning, and objects never emit it anyway.

        **Official reference:** https://www.php.net/manual/en/arrayaccess.offsetexists.php

??? question "Question 9 · Debugging"
    `count($collection)` throws `TypeError: count(): Argument #1 ($value) must be of type
    Countable|array, Collection given`. What is the minimal fix?

    - A. Implement `Countable` and its `count(): int` method.
    - B. Implement `ArrayAccess`.
    - C. Add a public `size()` method.
    - D. Cast the object to an array first: `count((array) $collection)`.

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** since PHP 8.0 `count()` accepts only `Countable|array`; anything else
        is a `TypeError` rather than the old warning. Implementing `Countable` with a
        `count(): int` method is the whole fix, and it is what makes `count($collection)`,
        Twig's `|length` and `assertCount()` all work at once.

        **B** unlocks bracket syntax, not `count()`. **C** adds a method the engine will never
        look for — `count()` dispatches on the interface, not on a name convention. **D**
        "works" but silently counts *properties*, not items: casting an object to an array
        exposes its property table, so a collection holding one array property would report
        `1`. It is a wrong answer that produces a plausible number, which is what makes it
        dangerous in review.

        **Official reference:** https://www.php.net/manual/en/class.countable.php

## Generators

??? question "Question 10"
    Which statement about a generator is correct?

    - A. It is a single-use, forward-only `Iterator` that produces values lazily.
    - B. It builds the complete array first and then hands it to `foreach`.
    - C. It can be rewound freely at any point.
    - D. It implements `ArrayAccess`, so `$gen[0]` reads the first value.

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** calling a function that contains `yield` returns a `Generator`
        object, which is `final` and `implements Iterator`. Values are produced on demand, and
        the manual is explicit that generators "are forward-only iterators, and cannot be
        rewound once iteration has started".

        **B** is the exact opposite of the memory benefit generators exist for. **C** is wrong:
        `rewind()` after the generator has advanced throws *Cannot rewind a generator that was
        already run*; `rewind()` is only tolerated before the first advance, where it merely
        primes the generator. **D** invents an interface — random access is impossible by
        construction, since the values do not exist until you ask for them.

        **Official reference:** https://www.php.net/manual/en/language.generators.comparison.php

??? question "Question 11 · Trap"
    ```php
    function items(): Generator { yield 1; yield 2; }

    $g = items();
    foreach ($g as $v) { /* consumes it */ }
    foreach ($g as $v) { echo $v; }   // second loop
    ```
    What does the **second** loop do?

    - A. Nothing — it simply iterates zero times.
    - B. It restarts from the first value.
    - C. It throws `Exception: Cannot traverse an already closed generator`.
    - D. It throws a `TypeError`.

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** a consumed generator is *closed*, not merely exhausted. `foreach`
        calls `rewind()` on it, and the engine refuses with an `Exception` whose message is
        *Cannot traverse an already closed generator*. The failure is loud, and that is good:
        silent emptiness would be far harder to debug.

        **A** is the most popular wrong answer, and it is what people expect from an exhausted
        array cursor. **B** would require rewinding, which generators cannot do. **D** picks
        the wrong throwable class — nothing here violates a type. The fix is to re-create the
        generator (call `items()` again) or to wrap the factory in an `IteratorAggregate`, the
        pattern Symfony ships as `RewindableGenerator`.

        **Official reference:** https://www.php.net/manual/en/language.generators.comparison.php

??? question "Question 12 · Code analysis"
    ```php
    function inner(): Generator { yield 1; yield 2; return 'END'; }
    function outer(): Generator { yield 0; $r = yield from inner(); yield $r; }

    var_dump(count(iterator_to_array(outer())));
    var_dump(count(iterator_to_array(outer(), false)));
    ```
    Which pair of numbers is printed?

    - A. `4` then `4`
    - B. `2` then `4`
    - C. `4` then `2`
    - D. `3` then `3`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `yield from` **does not renumber keys**. `outer()` yields key `0`,
        the delegated `inner()` yields its own keys `0` and `1`, then `yield $r` continues the
        outer counter at `1`. The key sequence is therefore `0, 0, 1, 1` for four values.
        `iterator_to_array()` preserves keys by default, so the two duplicates overwrite the
        two earlier values and only **2** elements survive. Passing `preserve_keys: false`
        renumbers on insertion and keeps all **4**.

        **A** assumes `yield from` renumbers — the manual's explicit caution says it does not.
        **C** inverts the two calls. **D** would require a value to disappear entirely, which
        never happens: overwriting is by key, and there are exactly two colliding keys.

        **Official reference:** https://www.php.net/manual/en/language.generators.syntax.php

??? question "Question 13"
    What is the default value of the second parameter of `iterator_to_array()`?

    - A. `preserve_keys: true`
    - B. `preserve_keys: false`
    - C. There is no second parameter.
    - D. It defaults to `true` for iterators and `false` for generators.

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the signature is
        `iterator_to_array(Traversable|array $iterator, bool $preserve_keys = true): array`.
        Because the default keeps keys, duplicate keys overwrite each other and "my array is
        shorter than my iterator" becomes a classic bug. (Since PHP 8.2 the first parameter
        also accepts a plain `array`.)

        **B** inverts the default. **C** is wrong — the parameter has existed since the
        function was introduced. **D** invents a per-type rule; the engine has no such
        special case, and a generator is just another `Traversable` here.

        **Official reference:** https://www.php.net/manual/en/function.iterator-to-array.php

??? question "Question 14 · Multiple answers"
    Which statements about `Generator::send()` and `Generator::getReturn()` are correct?
    (Choose all that apply.)

    - A. `send()` supplies the result of the currently paused `yield` expression and resumes the generator.
    - B. `send()` returns the next value the generator yields.
    - C. Calling `getReturn()` before the generator has finished throws an `Exception`.
    - D. You must call `next()` once to "prime" a generator before the first `send()`.

    ??? success "Show answer"
        **Correct answer:** A, B and C

        **Explanation:** **A** and **B** are the documented contract — `send()` "sends the
        given value to the generator as the result of the current `yield` expression and
        resumes execution", and it "returns the yielded value", i.e. the *next* one. **C** is
        the trap most people meet once: `getReturn()` on an unfinished generator throws
        *Cannot get return value of a generator that hasn't returned*.

        **D** is false and the manual calls it out by name: if the generator has not started,
        `send()` advances it to the first `yield` itself, so priming "like it is done in
        Python" is unnecessary.

        **Official reference:** https://www.php.net/manual/en/generator.send.php

## SPL data structures

??? question "Question 15"
    Which SPL structure maps arbitrary data keyed by an **object instance**?

    - A. `SplObjectStorage`
    - B. `SplStack`
    - C. `SplFixedArray`
    - D. `SplQueue`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `SplObjectStorage` "provides a map from objects to data or, by
        ignoring data, an object set". The key is object identity — the same handle
        `spl_object_id()` reports — so two structurally identical but distinct objects are two
        different keys. A plain PHP array cannot do this at all: array keys are `int|string`
        only.

        **B** and **D** are ordered lists (LIFO/FIFO) built on `SplDoublyLinkedList`; their
        keys are positional integers. **C** is an integer-indexed fixed-size vector that
        throws a `TypeError` on any non-integer offset. None of the three can key by identity.

        **Official reference:** https://www.php.net/manual/en/class.splobjectstorage.php

??? question "Question 16 · Multiple answers"
    Which statements about `SplObjectStorage` are correct? (Choose all that apply.)

    - A. `attach($o, $data)` and `$storage[$o] = $data` are the same operation.
    - B. Attaching an object that is already present replaces its data and leaves `count()` unchanged.
    - C. During `foreach`, `current()` yields the object and `getInfo()` returns its attached data.
    - D. Attaching the same object twice makes `count()` return 2.

    ??? success "Show answer"
        **Correct answer:** A, B and C

        **Explanation:** **A** — the manual states `attach()` "is an alias of
        `SplObjectStorage::offsetSet`". **B** follows directly: a set stores each identity
        once, so re-attaching overwrites the associated data without growing the container.
        **C** is the iteration protocol people get wrong: the loop variable is the *object*
        (keys are sequential integers), and the payload is read through `getInfo()` — or
        equivalently `$storage[$object]`.

        **D** contradicts the "set" half of the class. The whole reason `SplObjectStorage`
        answers "have I already visited this instance?" is that duplicates cannot exist.

        Worth knowing for future-proofing: the PHP manual documents `attach()`, `detach()` and
        `contains()` as deprecated from PHP **8.5** in favour of `offsetSet()`, `offsetUnset()`
        and `offsetExists()`. On the PHP 8.4 baseline of Symfony 8 both spellings are valid.

        **Official reference:** https://www.php.net/manual/en/splobjectstorage.attach.php

??? question "Question 17"
    With `SplPriorityQueue`, the relative order of elements inserted with **identical**
    priorities is…

    - A. Guaranteed FIFO (insertion order).
    - B. Undefined — it may differ from insertion order.
    - C. Always LIFO.
    - D. Alphabetical on the data.

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the class is implemented as a max heap, and the manual states that
        "the order of elements with identical priority is **undefined**. It may differ from
        the order in which they have been inserted". Inserting `a, b, c, d` all at priority 1
        really can extract as `a, d, c, b`. When you need a stable tie-break, make the
        priority a composite — for example `[$priority, $decreasingSerial]`, which compares
        the second element only when the first ties.

        **A** is the assumption that breaks schedulers in production. **C** and **D** invent
        rules the heap never applies: the sift-up path depends on the internal tree shape, not
        on insertion recency or on the payload's value.

        **Official reference:** https://www.php.net/manual/en/class.splpriorityqueue.php

??? question "Question 18 · Configuration consequence"
    ```php
    $q = new SplPriorityQueue();
    $q->setExtractFlags(SplPriorityQueue::EXTR_BOTH);
    $q->insert('deploy', 7);
    var_dump($q->extract());
    ```
    What does `extract()` return?

    - A. `string(6) "deploy"`
    - B. `int(7)`
    - C. `array(2) { ["data"]=> string(6) "deploy" ["priority"]=> int(7) }`
    - D. `array(2) { [0]=> string(6) "deploy" [1]=> int(7) }`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** `setExtractFlags()` decides what `current()`, `top()` and `extract()`
        hand back. `EXTR_BOTH` returns an **associative** array with the keys `data` and
        `priority`.

        **A** is the default (`EXTR_DATA`) — the mode you get without calling
        `setExtractFlags()` at all. **B** is `EXTR_PRIORITY`. **D** is the right idea with the
        wrong shape: the array is keyed by name, not positionally, so `[0]`/`[1]` would be
        undefined-key warnings in the calling code.

        **Official reference:** https://www.php.net/manual/en/splpriorityqueue.setextractflags.php

??? question "Question 19 · Code analysis"
    ```php
    $stack = new SplStack();
    $stack->push('a'); $stack->push('b'); $stack->push('c');
    foreach ($stack as $v) { echo $v; }
    echo '|', count($stack);

    $heap = new SplMinHeap();
    $heap->insert(5); $heap->insert(1); $heap->insert(9);
    foreach ($heap as $v) { echo $v; }
    echo '|', count($heap);
    ```
    What is printed?

    - A. `abc|3` then `159|3`
    - B. `cba|3` then `159|0`
    - C. `cba|0` then `951|0`
    - D. `abc|0` then `159|3`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** two different disciplines in one snippet. `SplStack` is an
        `SplDoublyLinkedList` whose iterator mode is `IT_MODE_LIFO`, so it walks `c`, `b`, `a`
        — and its default behaviour flag is `IT_MODE_KEEP`, so the three elements are still
        there afterwards. An `SplHeap` iterates by **extracting**: it yields the smallest
        first (`1`, `5`, `9` for a min-heap) and is **empty** when the loop ends.

        **A** iterates the stack FIFO, which is what `SplQueue` does. **C** empties the stack
        and reverses the heap. **D** mixes both errors. The one-line takeaway: *a heap is
        consumed by `foreach`; a stack or queue is not.*

        **Official reference:** https://www.php.net/manual/en/class.spldoublylinkedlist.php

??? question "Question 20 · Expert"
    You extend `SplHeap` and implement `compare($value1, $value2)` returning
    `$value1 <=> $value2`. What ordering does `extract()` produce?

    - A. Largest value first (max-heap).
    - B. Smallest value first (min-heap).
    - C. Insertion order.
    - D. It throws, because `compare()` must return a `bool`.

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `SplHeap::compare()` must return "positive integer if `value1` is
        greater than `value2`, 0 if they are equal, negative integer otherwise", and the
        element that compares *greatest* sifts to the root. So `$value1 <=> $value2` is the
        max-heap; `SplMinHeap` is the same class with the comparison flipped
        (`$value2 <=> $value1`).

        **B** is what you get from the inverted body — a very common one-character bug. **C**
        ignores the heap invariant entirely. **D** is wrong about the signature: `compare()` is
        `protected` and returns `int`. Two more facts worth carrying: throwing from
        `compare()` can corrupt the heap (recoverable only via `recoverFromCorruption()`), and
        equal elements "end up in an arbitrary relative position", so heaps are unstable for
        ties just like `SplPriorityQueue`.

        **Official reference:** https://www.php.net/manual/en/splheap.compare.php

??? question "Question 21 · Edge case"
    On PHP 8.4, which statements about `SplFixedArray` are correct? (Choose all that apply.)

    - A. Reading or writing an index outside the size throws `OutOfBoundsException`.
    - B. Using a string offset throws a `TypeError`.
    - C. It implements `IteratorAggregate`, not `Iterator`.
    - D. `setSize()` can grow the array, filling new slots with `null`.

    ??? success "Show answer"
        **Correct answer:** A, B, C and D

        **Explanation:** all four are true on the 8.4 baseline. **A** — since PHP 8.4 out-of-
        bounds access throws `OutOfBoundsException` (previously `RuntimeException`; since
        `OutOfBoundsException` extends `RuntimeException`, existing `catch` blocks keep
        working). **B** — since PHP 8.1 a non-integer key is a `TypeError`, not a
        `RuntimeException`. **C** — since PHP 8.0 the class implements `IteratorAggregate`;
        it implemented `Iterator` before that, and code doing `$fixed->rewind()` broke on the
        upgrade. **D** — `setSize()` resizes in place; growing pads with `null`, shrinking
        discards the tail.

        Because every option is correct, the exam value of this question is the version
        table itself: 8.0 changed the iteration interface, 8.1 changed the key error and added
        `JsonSerializable`, 8.4 changed the bounds exception.

        **Official reference:** https://www.php.net/manual/en/class.splfixedarray.php

## SPL iterators

??? question "Question 22 · Code analysis"
    ```php
    function naturals(): Generator { $i = 0; while (true) { yield $i++; } }

    foreach (new LimitIterator(naturals(), 2, 3) as $k => $v) { echo "$k:$v "; }
    ```
    What is printed?

    - A. `0:2 1:3 2:4`
    - B. `2:2 3:3 4:4`
    - C. `0:0 1:1 2:2`
    - D. A `TypeError` — `LimitIterator` needs an `Iterator`, and a generator is not one.

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `LimitIterator::__construct(Iterator $iterator, int $offset = 0,
        int $limit = -1)` skips `offset` elements and then yields at most `limit` of them.
        It is a decorator: it forwards the **inner** keys untouched, so you see the
        generator's own auto-keys `2`, `3`, `4`. The infinite generator is never a problem —
        laziness means only five values are ever produced.

        **A** assumes the decorator renumbers keys; it does not. **C** ignores the offset.
        **D** is the tempting trap: a `Generator` *is* an `Iterator` (the class is declared
        `final class Generator implements Iterator`), so it is accepted directly. What you
        cannot pass directly is an `IteratorAggregate` — that one needs an `IteratorIterator`
        wrapper first.

        **Official reference:** https://www.php.net/manual/en/limititerator.construct.php

??? question "Question 23"
    What are the three arguments a `CallbackFilterIterator` callback receives, and what must
    it return?

    - A. `($current, $key, $iterator)`, returning `true` to keep the element.
    - B. `($key, $current, $iterator)`, returning `true` to drop the element.
    - C. `($current, $iterator)`, returning the transformed value.
    - D. `($current)` only, returning `true` to keep the element.

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual documents the callback as accepting "up to three
        arguments: the current item, the current key and the iterator, respectively", and
        returning `true` to accept the current item. "Up to" matters: a one-argument closure
        is perfectly valid, which is why **D** looks right — but the question asks for the
        full signature, and only A states both the order and the polarity correctly.

        **B** swaps value and key *and* inverts the meaning of the return value — a filter
        that keeps exactly what you meant to remove. **C** describes a *mapping* decorator;
        `CallbackFilterIterator` extends `FilterIterator` and only decides accept/reject, it
        never rewrites values. Note also that it **preserves the inner keys**, so
        `iterator_to_array()` on a filtered iterator returns a sparse key set.

        **Official reference:** https://www.php.net/manual/en/callbackfilteriterator.construct.php

??? question "Question 24 · Execution order"
    A `RecursiveIteratorIterator` is built over a nested structure with no explicit mode
    argument. Which elements does `foreach` produce?

    - A. Only the leaves — `LEAVES_ONLY` is the default.
    - B. Parents first, then their children (`SELF_FIRST`).
    - C. Children first, then their parent (`CHILD_FIRST`).
    - D. Nothing, because a mode argument is mandatory.

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the constructor is
        `__construct(Traversable $iterator, int $mode = RecursiveIteratorIterator::LEAVES_ONLY,
        int $flags = 0)`, and `LEAVES_ONLY` "lists only leaves in iteration" — nested
        containers are traversed but never emitted themselves.

        **B** and **C** are the two opt-in modes: `SELF_FIRST` emits a parent before its
        children (what Symfony's Finder uses, so that directories can be filtered before being
        descended into), `CHILD_FIRST` emits children before the parent (the order you want
        for recursive deletion). **D** is wrong — the mode is optional, and forgetting that
        the default hides directories is the number-one surprise of this class.

        **Official reference:** https://www.php.net/manual/en/recursiveiteratoriterator.construct.php

??? question "Question 25 · Debugging"
    ```php
    $all = new AppendIterator();
    $all->append(new ArrayIterator(['a', 'b']));
    $all->append(new ArrayIterator(['c']));

    print_r(iterator_to_array($all));
    ```
    The developer expected three elements but got two. Why?

    - A. `AppendIterator` stops at the first exhausted inner iterator.
    - B. Both inner iterators emit keys `0`/`1`, and `iterator_to_array()` preserves keys, so `'c'` overwrites `'a'`.
    - C. `AppendIterator` requires `IteratorAggregate` inputs.
    - D. `ArrayIterator` cannot be appended twice.

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `AppendIterator` iterates its inner iterators one after another but
        **does not renumber their keys**. The first emits `0 => 'a'`, `1 => 'b'`; the second
        emits `0 => 'c'`. With key preservation on (the default) the second `0` overwrites the
        first, leaving `[0 => 'c', 1 => 'b']`. Passing `preserve_keys: false` gives the
        expected three elements — and a plain `foreach` over `$all` was never lossy in the
        first place; only the *array conversion* is.

        **A** is wrong: appending exists precisely to continue past exhaustion. **C** is
        wrong: `append()` takes an `Iterator`. **D** invents a restriction. This is the same
        root cause as the `yield from` trap: key collision at array-conversion time.

        **Official reference:** https://www.php.net/manual/en/class.appenditerator.php

??? question "Question 26 · Scenario"
    You need to loop over an `IteratorAggregate` **and** apply a `LimitIterator`, which
    requires an `Iterator`. Which decorator bridges the two?

    - A. `IteratorIterator`
    - B. `CachingIterator`
    - C. `MultipleIterator`
    - D. `ArrayIterator`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `IteratorIterator` is documented as the wrapper that "allows the
        conversion of anything that is `Traversable` into an `Iterator`". Symfony's `Finder`
        uses exactly this pattern — `new \IteratorIterator(new LazyIterator(...))` — before
        appending to an `AppendIterator`.

        **B** caches one element ahead so you can ask `hasNext()`; it happens to extend
        `IteratorIterator`, but that is not what it is *for*. **C** iterates several iterators
        **in parallel**, emitting one tuple per step. **D** wraps an **array**, not a
        `Traversable`; converting an aggregate through `iterator_to_array()` and then into an
        `ArrayIterator` would materialise everything in memory and throw away the laziness you
        wanted.

        **Official reference:** https://www.php.net/manual/en/class.iteratoriterator.php

## SPL in Symfony 8.0

??? question "Question 27 · Scenario"
    `Symfony\Component\DependencyInjection\Argument\RewindableGenerator` implements
    `\IteratorAggregate` and `\Countable`, and its `getIterator()` calls a stored closure that
    returns a fresh generator. What problem does that design solve?

    - A. It lets an injected tagged-service iterator be looped more than once, which a raw generator forbids.
    - B. It makes generators rewindable at the engine level.
    - C. It converts the generator to an array so services are instantiated eagerly.
    - D. It is only there to satisfy the `iterable` type declaration.

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** a `Generator` is single-use, so injecting one directly would break any
        service that iterates its handlers twice. Wrapping the *factory* in an
        `IteratorAggregate` means each `foreach` calls `getIterator()`, which calls the closure,
        which produces a **new** generator — re-iterable without losing laziness. `Countable`
        is there so `count($handlers)` does not have to consume the iterator.

        **B** overstates it: nothing about the `Generator` class changes; the aggregate simply
        makes a new one. **C** is the opposite of the intent — services stay lazily
        instantiated. **D** is wrong: a bare generator already satisfies `iterable`, so the
        wrapper would be pointless if that were the goal.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/Argument/RewindableGenerator.php

??? question "Question 28 · Multiple answers"
    Which of these are true of Symfony 8.0's `Finder` component? (Choose all that apply.)

    - A. `Finder` implements `\IteratorAggregate` and `\Countable`.
    - B. `Finder::count()` is implemented with `iterator_count()`.
    - C. Its directory walk uses `\RecursiveIteratorIterator` in `SELF_FIRST` mode.
    - D. `Finder::getIterator()` returns an array of `SplFileInfo` objects.

    ??? success "Show answer"
        **Correct answer:** A, B and C

        **Explanation:** **A** — the class is declared
        `class Finder implements \IteratorAggregate, \Countable`, which is why `foreach
        ($finder as $file)` and `count($finder)` both work. **B** — `count()` is literally
        `return iterator_count($this->getIterator());`, so counting walks the filesystem.
        **C** — `searchInDirectory()` builds
        `new \RecursiveIteratorIterator($iterator, \RecursiveIteratorIterator::SELF_FIRST)`,
        because directories must be visible to the exclude/depth filters before being
        descended into.

        **D** is wrong on the return type: `getIterator()` is declared `: \Iterator` and
        returns a lazy iterator chain (`AppendIterator`, `IteratorIterator`, `LazyIterator`,
        `SortableIterator`), never a materialised array. That laziness is the reason a Finder
        over a huge tree does not exhaust memory.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Finder/Finder.php

??? question "Question 29 · Expert trap"
    `Symfony\Component\Finder\Iterator\LazyIterator` implements `\IteratorAggregate` and its
    `getIterator()` body is `yield from ($this->iteratorFactory)();`. Why is `getIterator()`
    itself a generator here rather than `return ($this->iteratorFactory)();`?

    - A. Because `yield from` renumbers the keys of the inner iterator.
    - B. Because the factory must not run until iteration actually starts.
    - C. Because `getIterator()` cannot return an object.
    - D. Because `yield from` makes the result rewindable.

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** a function containing `yield` does **not** execute any of its body
        when called — it immediately returns a `Generator` and runs only on the first advance.
        So `getIterator()` hands back a generator without touching the filesystem; the
        expensive `searchInDirectory()` call happens when (and only when) the consumer starts
        looping. That is the whole point of a class named `LazyIterator`.

        **A** is the opposite of the documented behaviour: `yield from` **preserves** inner
        keys, which here keeps the pathname keys `Finder` relies on. **C** is false —
        returning an `Iterator` object is the normal case. **D** is false: the generator
        produced is still single-use; re-iterability comes from `getIterator()` being called
        again by each `foreach`, not from `yield from`.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Finder/Iterator/LazyIterator.php

??? question "Question 30 · True or false"
    In Symfony 8.0, `Symfony\Component\Messenger\Bridge\Amqp\Transport\AmqpReceiver::get()`
    is declared `: iterable` and delegates with `yield from`, so no envelope is fetched until
    the worker actually iterates the result.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** A — true

        **Explanation:** the method body is `yield from $this->getFromQueues(
        $this->connection->getQueueNames());`, and the chain continues with another
        `yield from` down to a `yield $envelope->with(...)`. Because the outermost method
        contains `yield`, calling it only creates a `Generator`; the AMQP round-trip happens on
        the first advance. Declaring the return type as `iterable` rather than `Generator`
        keeps the door open for a transport that returns a plain array instead.

        **B** would be right only if the method built and returned a collection eagerly. The
        certification-level point: adding a single `yield` anywhere in a function changes its
        call semantics for every caller — the body no longer runs at call time.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Messenger/Bridge/Amqp/Transport/AmqpReceiver.php

---

<small>Back to the lesson: [SPL — Standard PHP Library](spl.md) · [Guided exercises](spl-exercises.md) · [Review flashcards](spl-flashcards.md)</small>

# Guided Exercises — SPL, Iteration & Generators

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    a prediction before revealing the hint, and to a full attempt before revealing the
    solution — an iteration order you predicted wrongly and then corrected sticks far better
    than one you read.

    Theory: **[SPL — Standard PHP Library](spl.md)** · Then: **[Topic exam](spl-exam.md)**

    All code targets **PHP 8.4**. Every snippet runs in one file: save it and execute
    `php file.php`. Where an error is expected, that error **is** the observation.

## Exercise 1 · Watch `foreach` drive an iterator, call by call

**Objective:** Establish by experiment the exact order in which `foreach` calls the five
`Iterator` methods, and how that differs from `IteratorAggregate`.

**Context:** You are about to hand-write an iterator for an audit-log collection. Before
writing one, find out what the engine actually asks for, and when.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class Spy implements Iterator
{
    private int $i = 0;
    /** @var list<string> */
    private array $rows = ['login', 'update', 'logout'];

    public function rewind(): void { echo "rewind\n"; $this->i = 0; }
    public function valid(): bool { echo "valid\n"; return isset($this->rows[$this->i]); }
    public function current(): mixed { echo "current\n"; return $this->rows[$this->i]; }
    public function key(): mixed { echo "key\n"; return $this->i; }
    public function next(): void { echo "next\n"; ++$this->i; }
}

foreach (new Spy() as $k => $v) {
    echo "-> $k=$v\n";
}
```

**Task:** Write down the first five lines of output **before** running the file. Then run it
and check. Then answer: how many times is `valid()` called for three rows, and why?

**Expected observation:** the run opens with `rewind`, `valid`, `current`, `key`, then the
body. `valid()` is called four times for three rows — once per element plus one final call
that returns `false` and ends the loop.

??? tip "Show a hint"
    Ask what the engine must know before it dares read anything. It cannot call `current()`
    on an unpositioned cursor, and it cannot trust that the collection is non-empty. Also
    note that `key()` is only useful once `current()` has been read — the order between those
    two is fixed, not arbitrary.

??? success "Show the solution"
    ```
    rewind
    valid
    current
    key
    -> 0=login
    next
    valid
    current
    key
    -> 1=update
    next
    valid
    current
    key
    -> 2=logout
    next
    valid
    ```

    The loop is: `rewind()` once, then repeat `valid()` → `current()` → `key()` → body →
    `next()` until `valid()` returns `false`.

    Now replace the class with the aggregate form and run it twice in a row:

    ```php
    <?php
    declare(strict_types=1);

    final class Log implements IteratorAggregate
    {
        public function getIterator(): Traversable
        {
            echo "getIterator\n";

            yield from ['login', 'update', 'logout'];
        }
    }

    $log = new Log();
    foreach ($log as $v) { echo "-> $v\n"; }
    foreach ($log as $v) { echo "again $v\n"; }
    ```

    `getIterator` is printed **once per loop**, and the second loop works — because each
    `foreach` asks for a brand-new iterator.

    **Why it works:** `foreach` over an object first looks for `Traversable`. If the object is
    an `Iterator` it drives the object itself with the five methods. If it is an
    `IteratorAggregate` it calls `getIterator()` and drives the returned `Traversable`
    instead. A method containing `yield` returns a fresh `Generator` on every call, so the
    aggregate is re-iterable while the generator alone would not be.

    **Certification takeaway:** the examinable sentence is "`rewind`, then `valid`, `current`,
    `key`, then per step `next`, `valid`, `current`, `key`". Any option starting with
    `current` or omitting the leading `valid` is wrong.

    **Official reference:** https://www.php.net/manual/en/class.iterator.php

## Exercise 2 · Make one class behave like an array, a counter and a loop

**Objective:** Implement `IteratorAggregate`, `Countable` and `ArrayAccess` on a single
domain object, and prove each interface unlocks exactly one syntax.

**Context:** A `TagCollection` used by an article entity. Controllers want `foreach`,
templates want `count()`, and legacy code wants `$tags[0]`.

**Starting point:**

```php
<?php
declare(strict_types=1);

final class TagCollection
{
    /** @var array<int|string, string> */
    private array $tags = [];
}

$tags = new TagCollection();
$tags[] = 'php';
$tags['primary'] = 'symfony';

echo count($tags), "\n";
var_dump(isset($tags['primary']), $tags['missing'] ?? 'none');

foreach ($tags as $key => $tag) {
    echo "$key => $tag\n";
}
```

**Task:** Run the file first and read the error. Then add the three interfaces so that every
line works. Implement `getIterator()` with a single `yield from`. Do not add a `getTags()`
accessor — the point is to make the native syntax work.

**Expected observation:** before the fix, `Cannot use object of type TagCollection as array`.
After the fix: `2`, `bool(true)`, `string(4) "none"`, then the two `key => tag` lines with
keys `0` and `primary`.

??? tip "Show a hint"
    Four `offset*` methods, one `count()`, one `getIterator()` — six methods total. The
    append form `$tags[] = 'php'` arrives in `offsetSet()` with `$offset === null`; that
    `null` is the signal to push instead of assign.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    /**
     * @implements IteratorAggregate<int|string, string>
     * @implements ArrayAccess<int|string, string>
     */
    final class TagCollection implements IteratorAggregate, Countable, ArrayAccess
    {
        /** @var array<int|string, string> */
        private array $tags = [];

        public function getIterator(): Traversable
        {
            yield from $this->tags;
        }

        public function count(): int
        {
            return \count($this->tags);
        }

        public function offsetExists(mixed $offset): bool
        {
            return \array_key_exists($offset, $this->tags);
        }

        public function offsetGet(mixed $offset): mixed
        {
            return $this->tags[$offset] ?? null;
        }

        public function offsetSet(mixed $offset, mixed $value): void
        {
            if (null === $offset) {
                $this->tags[] = $value;

                return;
            }

            $this->tags[$offset] = $value;
        }

        public function offsetUnset(mixed $offset): void
        {
            unset($this->tags[$offset]);
        }
    }
    ```

    **Why it works:** each interface is a contract between your object and one piece of
    engine syntax. `ArrayAccess` routes `[]` to the four `offset*` methods, `Countable` routes
    `count()` to `count()`, and `IteratorAggregate` routes `foreach` to `getIterator()`. The
    generator inside `getIterator()` satisfies the `Traversable` return type because
    `Generator` is declared `final class Generator implements Iterator`.

    **Certification takeaway:** `IteratorAggregate` costs one method, `Iterator` costs five.
    Unless you genuinely need to control the cursor from outside, the aggregate is the
    correct choice — and it is what Symfony uses for `Finder`, `ParameterBag` and form
    objects.

    **Official reference:** https://www.php.net/manual/en/class.arrayaccess.php

## Exercise 3 · Inspect what `iterator_to_array()` really returns

**Objective:** Observe that `yield from` preserves inner keys, and that array conversion
silently loses values when keys collide.

**Context:** You are merging a "recent" feed into a "pinned" feed with `yield from`, then
dumping the result for a test assertion.

**Starting point:**

```php
<?php
declare(strict_types=1);

function pinned(): Generator
{
    yield 'welcome';
    yield 'changelog';
}

function feed(): Generator
{
    yield 'breaking-news';
    yield from pinned();
    yield 'footer';
}

foreach (feed() as $k => $v) {
    echo "$k => $v\n";
}

var_dump(count(iterator_to_array(feed())));
var_dump(count(iterator_to_array(feed(), false)));
```

**Task:** Predict the four key/value pairs and the two counts before running. Then run it and
explain, key by key, which value overwrote which.

**Expected observation:** keys `0, 0, 1, 1` for four values; then `int(2)` and `int(4)`.

??? tip "Show a hint"
    `yield from` does not restart the outer key counter and does not renumber the inner one.
    Write the four keys down in order — the collision becomes obvious before you even think
    about `iterator_to_array()`.

??? success "Show the solution"
    ```
    0 => breaking-news
    0 => welcome
    1 => changelog
    1 => footer
    int(2)
    int(4)
    ```

    `feed()` emits key `0`, then `pinned()` emits its own keys `0` and `1`, then the outer
    generator continues its own counter at `1`. With `preserve_keys` at its default `true`,
    `'welcome'` overwrites `'breaking-news'` at key `0` and `'footer'` overwrites
    `'changelog'` at key `1` — two elements survive. With `preserve_keys: false` the values
    are appended in order and all four survive.

    **Why it works:** the manual's caution on `yield from` says it plainly — delegation
    "does not reset the keys. It preserves the keys returned by the `Traversable` object, or
    `array`", and warns that `iterator_to_array()` returning a keyed array by default is
    exactly where this bites. A plain `foreach` never loses anything, because nothing is
    being inserted into an array.

    **Certification takeaway:** two facts, always asked together: `iterator_to_array()`
    defaults to `preserve_keys: true`, and `yield from` preserves inner keys. The observable
    consequence is a **shorter array than the iterator**, never a wrong order.

    **Official reference:** https://www.php.net/manual/en/language.generators.syntax.php

## Exercise 4 · Change one structure and watch the discipline change

**Objective:** Compare `SplQueue`, `SplStack`, `SplMinHeap` and `SplMaxHeap` on identical
input, and discover which of them `foreach` consumes.

**Context:** A deployment runner processes task names. You are choosing the container.

**Starting point:**

```php
<?php
declare(strict_types=1);

$items = ['migrate', 'warmup', 'notify'];

$queue = new SplQueue();
foreach ($items as $i) {
    $queue->enqueue($i);
}

$stack = new SplStack();
foreach ($items as $i) {
    $stack->push($i);
}

foreach ($queue as $v) { echo $v, ' '; }
echo '| left: ', count($queue), "\n";

foreach ($stack as $v) { echo $v, ' '; }
echo '| left: ', count($stack), "\n";
```

**Task:** Run it, then add an `SplMinHeap` and an `SplMaxHeap` fed with `[5, 1, 9]` and repeat
the same "iterate, then count what is left" measurement. Explain the difference between the
two families in one sentence.

**Expected observation:** queue and stack keep their three elements; both heaps end up
**empty**, because iterating a heap extracts from it.

??? tip "Show a hint"
    `SplStack` and `SplQueue` are the same class underneath, differing only by iterator mode
    (`IT_MODE_LIFO` vs `IT_MODE_FIFO`), and their default behaviour flag is `IT_MODE_KEEP`.
    A heap has no such flag — think about what `top()` plus "move to the next element" can
    possibly mean for a tree that only knows its root.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    $min = new SplMinHeap();
    $max = new SplMaxHeap();
    foreach ([5, 1, 9] as $n) {
        $min->insert($n);
        $max->insert($n);
    }

    echo 'min top: ', $min->top(), ' | max top: ', $max->top(), "\n";

    foreach ($min as $v) { echo $v, ' '; }
    echo '| left: ', count($min), "\n";

    foreach ($max as $v) { echo $v, ' '; }
    echo '| left: ', count($max), "\n";
    ```

    ```
    migrate warmup notify | left: 3
    notify warmup migrate | left: 3
    min top: 1 | max top: 9
    1 5 9 | left: 0
    9 5 1 | left: 0
    ```

    **Why it works:** `SplStack` and `SplQueue` both extend `SplDoublyLinkedList`; the only
    difference is the iteration direction constant they set, and iteration is non-destructive
    by default. `SplHeap` (and its `SplMinHeap`/`SplMaxHeap` subclasses) implements `Iterator`
    by repeatedly extracting the root, so the container is empty once the loop finishes.

    **Certification takeaway:** "iterating a heap empties it, iterating a linked list does
    not" is the discriminating fact. If you need the heap contents twice, `clone` it before
    iterating — the clone is a separate heap.

    **Official reference:** https://www.php.net/manual/en/class.spldoublylinkedlist.php

## Exercise 5 · Diagnose "my generator produced nothing the second time"

**Objective:** Reproduce the closed-generator failure, read the real exception message, and
fix it with the pattern Symfony itself ships.

**Context:** A service receives an `iterable` of handlers and loops over it twice: once to
count them for a log line, once to run them.

**Starting point:**

```php
<?php
declare(strict_types=1);

function handlers(): Generator
{
    yield 'validate';
    yield 'persist';
    yield 'notify';
}

$handlers = handlers();

$n = 0;
foreach ($handlers as $h) {
    ++$n;
}
echo "found $n handlers\n";

foreach ($handlers as $h) {
    echo "running $h\n";
}
```

**Task:** Predict what the second loop prints, then run it. Read the exception class and the
exact message. Then fix the code **without** materialising the handlers into an array, so
that both loops work and the values are still produced lazily.

**Expected observation:** `found 3 handlers`, then an uncaught
`Exception: Cannot traverse an already closed generator`.

??? tip "Show a hint"
    The generator object is not the collection — it is one *pass* over the collection. What
    you want to inject is something that can hand out a new pass on demand. Which interface
    is asked for a fresh iterator on every single `foreach`?

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    /** @implements IteratorAggregate<int, string> */
    final class HandlerList implements IteratorAggregate, Countable
    {
        /** @var Closure(): Generator<int, string> */
        private Closure $factory;

        public function __construct(callable $factory, private readonly int $size)
        {
            $this->factory = $factory(...);
        }

        public function getIterator(): Traversable
        {
            return ($this->factory)();
        }

        public function count(): int
        {
            return $this->size;
        }
    }

    $handlers = new HandlerList(handlers(...), 3);

    echo 'found ', count($handlers), " handlers\n";

    foreach ($handlers as $h) { echo "running $h\n"; }
    foreach ($handlers as $h) { echo "again $h\n"; }
    ```

    **Why it works:** every `foreach` over an `IteratorAggregate` calls `getIterator()`, which
    calls the factory, which returns a **new** `Generator`. Nothing is buffered, so laziness
    survives; and `count()` answers without consuming anything. This is precisely
    `Symfony\Component\DependencyInjection\Argument\RewindableGenerator`, the object injected
    when you use a tagged iterator — it implements `\IteratorAggregate` and `\Countable` and
    stores the generator factory as a `Closure`.

    **Certification takeaway:** the second pass over a consumed generator does **not** yield
    nothing — it throws `Exception: Cannot traverse an already closed generator`. Distinguish
    it from `Exception: Cannot rewind a generator that was already run`, which is what you get
    from an explicit `rewind()` after advancing.

    **Official reference:** https://www.php.net/manual/en/language.generators.comparison.php

## Exercise 6 · Handle the equal-priority edge case

**Objective:** Prove that `SplPriorityQueue` is unstable for equal priorities, and build a
tie-break that makes the order deterministic.

**Context:** A job scheduler where most jobs share the default priority `1`, and the business
rule is "same priority ⇒ first submitted runs first".

**Starting point:**

```php
<?php
declare(strict_types=1);

$queue = new SplPriorityQueue();
foreach (['alpha', 'bravo', 'charlie', 'delta'] as $job) {
    $queue->insert($job, 1);
}

$order = [];
while (!$queue->isEmpty()) {
    $order[] = $queue->extract();
}

echo implode(', ', $order), "\n";
```

**Task:** Run it. Is the output insertion order? Then make it deterministic **without**
changing the business priorities: keep priority `1` for every job, and still extract
`alpha, bravo, charlie, delta`.

**Expected observation:** the naive run prints something like `alpha, delta, charlie, bravo`
— not insertion order. After the fix, insertion order is restored.

??? tip "Show a hint"
    A priority may be any comparable value, not just an `int`. PHP compares arrays element by
    element, so a two-element priority compares the second element only when the first ties.
    You need a counter that *decreases* with each insertion, because the queue extracts the
    greatest priority first.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    $queue = new SplPriorityQueue();
    $serial = PHP_INT_MAX;

    foreach (['alpha', 'bravo', 'charlie', 'delta'] as $job) {
        $queue->insert($job, [1, $serial--]);
    }

    $order = [];
    while (!$queue->isEmpty()) {
        $order[] = $queue->extract();
    }

    echo implode(', ', $order), "\n";   // alpha, bravo, charlie, delta
    ```

    Add `$queue->setExtractFlags(SplPriorityQueue::EXTR_BOTH);` before extracting and each
    `extract()` returns `['data' => 'alpha', 'priority' => [1, ...]]` instead of the bare
    payload — useful when debugging the tie-break itself.

    **Why it works:** `SplPriorityQueue` is a max heap, and the manual states that the order
    of elements with identical priority is undefined and may differ from insertion order. The
    composite priority `[businessPriority, decreasingSerial]` never ties, so the heap has a
    total order and behaves stably. The same trick works for `SplHeap`, whose documentation
    also warns that equal elements "end up in an arbitrary relative position".

    **Certification takeaway:** "not stable for equal priorities" is a documented property,
    not an implementation accident — never answer "FIFO among equals". And the fix is a
    composite priority, not a second queue.

    **Official reference:** https://www.php.net/manual/en/class.splpriorityqueue.php

## Exercise 7 · Expert challenge — build a lazy file pipeline and a cycle-safe walker

**Objective:** Compose SPL iterators into a memory-flat pipeline the way `Finder` does, then
use `SplObjectStorage` to walk an object graph that contains a cycle.

**Context:** You must list the first three `.md` files of a documentation tree, and
separately serialise an entity graph whose objects reference each other.

**Starting point:**

```php
<?php
declare(strict_types=1);

$root = sys_get_temp_dir() . '/spl-lab';
@mkdir($root . '/sub', 0o777, true);
file_put_contents($root . '/a.md', "a\n");
file_put_contents($root . '/b.txt', "b\n");
file_put_contents($root . '/sub/c.md', "c\n");
file_put_contents($root . '/sub/d.md', "d\n");
```

**Task:**

1. Walk `$root` recursively and emit only files whose extension is `md`, limited to the first
   three results, without ever building an intermediate array. Then count the matches with
   `iterator_count()` on a fresh pipeline and explain why you cannot reuse the first one.
2. Build two objects that reference each other, then write a `walk()` function that visits
   every reachable object exactly once using `SplObjectStorage`, and prove it terminates.

**Expected observation:** the three `.md` paths and never `b.txt` (the exact order follows the
filesystem, not the alphabet), then a walk that prints each node once instead of recursing
forever.

??? tip "Show a hint"
    For part 1: `RecursiveDirectoryIterator` produces the tree, `RecursiveIteratorIterator`
    flattens it, `CallbackFilterIterator` decides what survives, `LimitIterator` stops early.
    Use `RecursiveDirectoryIterator::SKIP_DOTS` or your filter will trip over `.` and `..`.

    For part 2: an array cannot be keyed by an object, but `SplObjectStorage` can — and
    `contains()` (alias of `offsetExists()`) answers "seen already?" in constant time.

??? success "Show the solution"
    ```php
    <?php
    declare(strict_types=1);

    $root = sys_get_temp_dir() . '/spl-lab';

    function markdownFiles(string $root): Iterator
    {
        $tree = new RecursiveDirectoryIterator($root, FilesystemIterator::SKIP_DOTS);
        $flat = new RecursiveIteratorIterator($tree, RecursiveIteratorIterator::LEAVES_ONLY);

        return new CallbackFilterIterator(
            $flat,
            static fn (SplFileInfo $file): bool => $file->isFile() && 'md' === $file->getExtension(),
        );
    }

    foreach (new LimitIterator(markdownFiles($root), 0, 3) as $file) {
        echo $file->getPathname(), "\n";
    }

    echo 'total: ', iterator_count(markdownFiles($root)), "\n";
    ```

    ```php
    <?php
    declare(strict_types=1);

    final class Node
    {
        /** @var list<Node> */
        public array $links = [];

        public function __construct(public readonly string $name) {}
    }

    $a = new Node('a');
    $b = new Node('b');
    $a->links[] = $b;
    $b->links[] = $a;          // cycle

    function walk(Node $node, SplObjectStorage $seen): void
    {
        if ($seen->contains($node)) {
            return;
        }

        $seen->attach($node, ['visitedAt' => microtime(true)]);
        echo $node->name, "\n";

        foreach ($node->links as $child) {
            walk($child, $seen);
        }
    }

    $seen = new SplObjectStorage();
    walk($a, $seen);
    echo 'visited: ', count($seen), "\n";
    ```

    **Why it works:** each decorator in the file pipeline pulls exactly one element from the
    one below it, so peak memory is a handful of `SplFileInfo` objects regardless of tree
    size. `LimitIterator` stops asking after three, so the fourth file is never even
    `stat()`ed. The pipeline is single-use — `iterator_count()` would consume it — which is
    why the code calls the factory a second time rather than reusing the object; Symfony
    solves the same problem in `Finder::count()`, which calls `iterator_count($this->getIterator())`
    on a freshly built chain.

    For the graph, `SplObjectStorage` keys by object **identity**, the same identity
    `spl_object_id()` exposes. `contains()` turns "have I been here?" into an O(1) question
    without adding a `visited` flag to the domain object, and the optional second argument of
    `attach()` lets you record metadata about the visit at the same time.

    **Certification takeaway:** the SPL iterators compose because each one *is* an `Iterator`
    and *takes* an `Iterator`. Remember the three roles: `RecursiveIteratorIterator` flattens,
    `FilterIterator` (and its `CallbackFilterIterator` subclass) selects,
    `LimitIterator` slices. And `SplObjectStorage` is the answer whenever a question says
    "keyed by object".

    **Official reference:** https://www.php.net/manual/en/class.recursiveiteratoriterator.php

---

<small>Back to the lesson: [SPL — Standard PHP Library](spl.md) · Next: [Take the topic exam](spl-exam.md)</small>

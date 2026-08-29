# Guided Exercises — PHP Extensions

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    an answer before revealing a hint, and to a full attempt before revealing the solution —
    an extension behaviour you predicted wrongly and then corrected sticks far better than
    one you read.

    Theory: **[PHP Extensions](extensions.md)** · Then:
    **[Topic exam](extensions-exam.md)**

    All code targets **PHP 8.4** and **Symfony 8.0**. Exercises 1 to 6 run with a bare
    `php file.php`; exercise 7 assumes a Composer-managed project.

## Exercise 1 · Inventory the build you are actually running on

**Objective:** Stop guessing what your PHP has, and learn the three introspection calls plus
the one module name that never matches its INI prefix.

**Context:** Every deployment bug in this chapter starts the same way — someone assumed an
extension was there. Before writing any guard, look.

**Starting point:** A terminal with `php` on the path.

**Task:**

1. Run `php -m` and read the output *including the section headers at the bottom*.
2. Then run this script and explain every line of its output:

```php
<?php
declare(strict_types=1);

var_dump(\extension_loaded('intl'));
var_dump(\extension_loaded('INTL'));
var_dump(\extension_loaded('opcache'));
var_dump(\extension_loaded('Zend OPcache'));
var_dump(\count(\get_loaded_extensions()));
var_dump(\get_loaded_extensions(true));
```

**Expected observation:** the first two agree, the third and fourth **disagree**, and
`get_loaded_extensions(true)` returns a very short list. If your build has no OPcache at all,
lines 3 and 4 both print `false` — install or enable it, or read the solution for what you
would have seen.

??? tip "Show a hint"
    `php -m` prints two sections, not one. Read the second header carefully and then look for
    the same string in the first section. The name PHP registers is not always the name you
    type in `php.ini` — `opcache.enable` is an INI *prefix*, not a module name.

??? success "Show the solution"
    `php -m` prints something like:

    ```text
    [PHP Modules]
    ...
    Zend OPcache
    ...
    [Zend Modules]
    Zend OPcache
    ```

    And the script prints:

    ```text
    bool(true)     // intl is loaded
    bool(true)     // extension_loaded() is case-insensitive
    bool(false)    // there is no module called "opcache"
    bool(true)     // the module is registered as "Zend OPcache"
    int(60)        // however many modules this build has
    array(1) { [0]=> string(12) "Zend OPcache" }
    ```

    **Why it works:** `extension_loaded()` matches a registered **module name**,
    case-insensitively, and OPcache registers itself as `Zend OPcache`. It appears in *both*
    `php -m` sections, and in both `get_loaded_extensions()` and `get_loaded_extensions(true)`,
    because it registers a normal module entry *and* hooks the compiler as a Zend extension.
    `get_loaded_extensions(bool $zend_extensions = false)` filters to Zend extensions when you
    pass `true`.

    **Certification takeaway:** `extension_loaded('opcache')` is `false` on a server where
    OPcache is running. Symfony's own `about` command uses
    `\extension_loaded('Zend OPcache')` — when in doubt, check what the framework checks.

    **Official reference:** https://www.php.net/manual/en/function.get-loaded-extensions.php

## Exercise 2 · Write a preflight guard that names everything that is missing

**Objective:** Turn detection into a single, actionable error instead of a runtime surprise
twenty files later.

**Context:** A console entry point that must not start unless `mbstring`, `intl` and a usable
PDO driver are present.

**Starting point:**

```php
<?php
declare(strict_types=1);

if (!\extension_loaded('mbstring')) {
    throw new \RuntimeException('mbstring missing');
}
// ... and then someone adds a second copy of this block for intl, and a third for pdo
```

**Task:** Replace the stack of `if` blocks with one guard that

1. reports **all** missing extensions in a single message rather than the first one,
2. reports the version of each extension it did find,
3. also fails when `pdo` is loaded but has **no drivers** at all.

**Expected observation:** on a complete host the script prints a summary and exits 0. Remove
one requirement name from the list to a deliberately bogus value (say `'intlx'`) and the
message must name exactly that one.

??? tip "Show a hint"
    `array_filter()` with `extension_loaded` as the predicate gives you the missing set in one
    pass. For versions, remember there is a call that returns a version string *or* `false`
    when the extension is absent — you do not need two calls per extension. For the driver
    check, PDO exposes a static method that lists what is actually loaded.

??? success "Show the solution"

    ```php
    <?php
    declare(strict_types=1);

    $required = ['mbstring', 'intl', 'pdo'];

    $missing = array_values(array_filter(
        $required,
        static fn (string $name): bool => !\extension_loaded($name),
    ));

    if ([] !== $missing) {
        throw new \RuntimeException(
            'Missing PHP extensions: '.implode(', ', $missing)
            .'. Install them before running this application.'
        );
    }

    if ([] === \PDO::getAvailableDrivers()) {
        throw new \RuntimeException('ext-pdo is loaded but no PDO driver is available.');
    }

    foreach ($required as $name) {
        printf("%-10s %s\n", $name, \phpversion($name) ?: '(no version reported)');
    }
    printf("%-10s %s\n", 'pdo drivers', implode(', ', \PDO::getAvailableDrivers()));
    ```

    Typical output:

    ```text
    mbstring   8.4.19
    intl       8.4.19
    pdo        8.4.19
    pdo drivers mysql, pgsql, sqlite
    ```

    **Why it works:** `extension_loaded()` answers presence; `phpversion($ext)` answers
    presence *and* version in one call, returning `false` when the extension is missing or
    reports no version — which is why the `?:` fallback is there rather than a second guard.
    `PDO::getAvailableDrivers()` returns the drivers "which can be used in the DSN parameter of
    `PDO::__construct`", and an **empty array** when none are available: `ext-pdo` on its own
    connects to nothing.

    **Certification takeaway:** `pdo` and `pdo_mysql` are two different extensions. A host can
    pass an `ext-pdo` check and still fail every connection with "could not find driver".

    **Official reference:** https://www.php.net/manual/en/pdo.getavailabledrivers.php

## Exercise 3 · Measure the same string three ways

**Objective:** See, on one line of text, that "length" is not one number but three — bytes,
code points and grapheme clusters.

**Context:** A form says "max 20 characters". Your validator uses `strlen()`. A user types an
emoji.

**Starting point:**

```php
<?php
declare(strict_types=1);

$samples = ['hello', 'café', 'ñ', "n\u{0303}"];
```

**Task:** For each sample print `strlen()`, `mb_strlen($s, 'UTF-8')` and `grapheme_strlen($s)`
side by side. Then add the family emoji `"\u{1F468}\u{200D}\u{1F469}\u{200D}\u{1F467}"` as a
fifth sample. Before running, predict the three numbers for **each** row.

**Expected observation:** `hello` agrees everywhere. `café` splits bytes from the other two.
`ñ` written as one code point and `n` + combining tilde written as two code points look
identical on screen but disagree on `mb_strlen`. The emoji disagrees on all three.

??? tip "Show a hint"
    `grapheme_strlen()` comes from `intl`, not from `mbstring`. If it is undefined on your
    build, that is itself the lesson: the "how many characters does a human see?" question is
    an ICU question. A combining mark is a separate code point that renders on top of the
    previous one.

??? success "Show the solution"

    ```php
    <?php
    declare(strict_types=1);

    $samples = [
        'hello'            => 'hello',
        'cafe-accented'    => 'café',
        'n-tilde-single'   => "\u{00F1}",
        'n-tilde-combined' => "n\u{0303}",
        'family-emoji'     => "\u{1F468}\u{200D}\u{1F469}\u{200D}\u{1F467}",
    ];

    printf("%-18s %6s %6s %9s\n", 'sample', 'bytes', 'points', 'graphemes');
    foreach ($samples as $label => $s) {
        printf(
            "%-18s %6d %6d %9d\n",
            $label,
            \strlen($s),
            \mb_strlen($s, 'UTF-8'),
            \grapheme_strlen($s),
        );
    }
    ```

    ```text
    sample              bytes points graphemes
    hello                   5      5         5
    cafe-accented           5      4         4
    n-tilde-single          2      1         1
    n-tilde-combined        3      2         1
    family-emoji           18      5         1
    ```

    **Why it works:** bytes are storage; code points are the atomic units Unicode defines;
    grapheme clusters are "one or more code points which are displayed as a single graphical
    unit". `n` + `U+0303` (combining tilde) is two code points rendering as one `ñ` — the
    Symfony String documentation uses this exact pair as its example. The family emoji is three
    emoji joined by two zero-width joiners: 5 code points, 18 bytes, 1 grapheme.

    **Certification takeaway:** Symfony's String component names the three levels explicitly —
    `ByteString`, `CodePointString`, `UnicodeString` — and `UnicodeString` is the grapheme-aware
    one. When a question says "characters", decide which of the three it means before answering.

    **Official reference:** https://symfony.com/doc/8.0/string.html

## Exercise 4 · Change one call at a time and watch the corruption appear

**Objective:** Reproduce the classic UTF-8 truncation bug on purpose, then fix it by changing
exactly one function name.

**Context:** A "preview" feature cuts a description to 4 characters. It works in English and
produces black diamonds in French.

**Starting point:**

```php
<?php
declare(strict_types=1);

$s = 'café';

var_dump(\substr($s, 0, 4));
var_dump(\strtoupper($s));
var_dump(\strrev($s));
var_dump(\str_pad($s, 6, '*'));
```

**Task:** Run it, then inspect the raw bytes with `bin2hex()` on each result. Now replace each
call with its `mb_` counterpart where one exists (`mb_substr`, `mb_strtoupper`, `mb_str_pad`)
and compare. Note which line has **no** `mb_` counterpart and think about why.

**Expected observation:** the byte functions all produce something wrong on `é`, in four
different ways: a truncated lead byte, an unchanged accent, reversed garbage, and padding that
is one star short.

??? tip "Show a hint"
    Count the bytes before you run anything: `café` is `63 61 66 c3 a9`. Now ask each function
    what it does with a *byte* budget of 4, or 6. For `strrev`, ask what happens when you
    reverse `c3 a9` into `a9 c3`.

??? success "Show the solution"

    ```php
    <?php
    declare(strict_types=1);

    $s = 'café';

    printf("bytes         %s\n", \bin2hex($s));
    printf("substr        %s -> %s\n", \substr($s, 0, 4), \bin2hex(\substr($s, 0, 4)));
    printf("mb_substr     %s -> %s\n", \mb_substr($s, 0, 4, 'UTF-8'), \bin2hex(\mb_substr($s, 0, 4, 'UTF-8')));
    printf("strtoupper    %s\n", \strtoupper($s));
    printf("mb_strtoupper %s\n", \mb_strtoupper($s, 'UTF-8'));
    printf("strrev        %s\n", \bin2hex(\strrev($s)));
    printf("str_pad       %s\n", \str_pad($s, 6, '*'));
    printf("mb_str_pad    %s\n", \mb_str_pad($s, 6, '*'));
    printf("valid?        substr=%s\n", \var_export(\mb_check_encoding(\substr($s, 0, 4), 'UTF-8'), true));
    ```

    ```text
    bytes         636166c3a9
    substr        caf? -> 636166c3
    mb_substr     café -> 636166c3a9
    strtoupper    CAFé
    mb_strtoupper CAFÉ
    strrev        a9c3666163
    str_pad       café*
    mb_str_pad    café**
    valid?        substr=false
    ```

    (The `?` on the `substr` line is the terminal rendering the orphaned `0xC3` lead byte; the
    hex column is the ground truth.)

    Line by line: `substr($s, 0, 4)` keeps `63 61 66 c3` — the lead byte of `é` without its
    continuation byte, which is why `mb_check_encoding()` on the result returns `false`.
    `strtoupper()` uppercases ASCII only, leaving `é` untouched. `strrev()` reverses *bytes*,
    turning `c3 a9` into `a9 c3`, which is not valid UTF-8 in either order. `str_pad()` counts
    bytes, so it thinks `café` is already 5 long and adds one star instead of two.

    There is no `mb_strrev()`. Reversing text is not a well-defined operation on Unicode —
    combining marks and grapheme clusters would have to move together — so mbstring does not
    pretend to offer it. Use `implode('', array_reverse(mb_str_split($s)))` if you accept
    code-point semantics, or the String component's `reverse()` for grapheme semantics.

    **Why it works:** every plain string function in PHP operates on bytes and has no notion of
    an encoding. `mb_*` functions take an `encoding` argument that defaults to the internal
    encoding, and count characters instead.

    **Certification takeaway:** the trap is not that `strlen()` is "wrong" — it is that it
    answers a different question. Byte length is the right answer for `Content-Length`; character
    length is the right answer for a validation message.

    **Official reference:** https://www.php.net/manual/en/function.mb-substr.php

## Exercise 5 · Diagnose a validator that lets bad input through

**Objective:** Meet the two `ctype` surprises in the context where they actually cause damage.

**Context:** A legacy `isPositiveIntegerLike()` helper guards a database lookup. QA reports
that it rejects a value the form definitely sent, and accepts an empty one somewhere else.

**Starting point:**

```php
<?php
declare(strict_types=1);

function isPositiveIntegerLike(mixed $v): bool
{
    return \ctype_digit($v);
}

var_dump(isPositiveIntegerLike('123'));
var_dump(isPositiveIntegerLike(''));
var_dump(isPositiveIntegerLike(123));
var_dump(isPositiveIntegerLike(1234));
```

**Task:** Predict all four results before running. Then run with
`error_reporting(E_ALL)` so deprecations are visible, explain why two of the four surprise
you, and rewrite the helper so it is correct for `int` and `string` input alike.

**Expected observation:** `'123'` is `true`. `''` is `false`. `123` is `false` **and emits a
deprecation notice**. `1234` is `true`. The failure is that the third and fourth lines behave
*differently from each other* while both are integers.

??? tip "Show a hint"
    Read the manual's parameter note for `ctype_digit`, not just its description. There is a
    numeric window in which an integer means something entirely different from what you typed.
    Ask yourself: what character has ASCII code 123?

??? success "Show the solution"

    ```php
    <?php
    declare(strict_types=1);

    error_reporting(\E_ALL);

    function isPositiveIntegerLike(int|string $v): bool
    {
        // Always hand ctype_* a string: an int is a codepoint, not its digits.
        return \ctype_digit((string) $v);
    }

    var_dump(isPositiveIntegerLike('123'));  // true
    var_dump(isPositiveIntegerLike(''));     // false — empty is always false
    var_dump(isPositiveIntegerLike(123));    // true, now that we cast
    var_dump(isPositiveIntegerLike(1234));   // true
    ```

    With the original helper you would have seen:

    ```text
    bool(true)
    bool(false)
    Deprecated: ctype_digit(): Argument of type int will be interpreted as string in the future
    bool(false)
    Deprecated: ctype_digit(): Argument of type int will be interpreted as string in the future
    bool(true)
    ```

    **Why it works:** the manual states that an `int` between **-128 and 255 inclusive** is
    interpreted as the ASCII value of a single character, and that any other integer is
    interpreted as a string containing its decimal digits. `123` is inside the window and means
    `{`, which is not a digit; `1234` is outside it and is stringified to `"1234"`, which is.
    Separately, the manual notes that "when called with an empty string the result will always
    be `false`" — that is by design for a validator, but it means `ctype_digit()` alone never
    doubles as a "not empty" check. Finally, since **PHP 8.1.0** passing a non-string argument
    is deprecated, and PHP announces that the argument will be interpreted as a string in the
    future — so the `123` behaviour is transitional and must not be relied on.

    **Certification takeaway:** `ctype_digit('123') === true`, `ctype_digit(123) === false`,
    `ctype_digit(1234) === true`, `ctype_digit('') === false`. Cast to `string` and the whole
    family of surprises disappears.

    **Official reference:** https://www.php.net/manual/en/function.ctype-digit.php

## Exercise 6 · Handle the edge case: converting text that will not fit

**Objective:** Choose deliberately between approximating, dropping and failing when a character
has no representation in the target charset — and see why the answer is host-dependent.

**Context:** You must produce an ASCII-only filename from a user-supplied title that contains
`€` and accents.

**Starting point:**

```php
<?php
declare(strict_types=1);

$title = "Facture 5€ — café";

var_dump(\iconv('UTF-8', 'ASCII', $title));
```

**Task:** Run it as-is and note both the return value and the diagnostic. Then try
`'ASCII//TRANSLIT'` and `'ASCII//IGNORE'` and describe, in one sentence each, what you would
lose. Finally, compare the results with Symfony's
`(new \Symfony\Component\String\UnicodeString($title))->ascii()` if you have the String
component available.

**Expected observation:** the plain conversion fails; `//IGNORE` returns a string with holes in
it; `//TRANSLIT` returns a readable approximation — *on your machine*. On a musl-based image
such as Alpine, `//TRANSLIT` may quietly do nothing.

??? tip "Show a hint"
    The suffix goes on the **target** encoding, not the source, and there are exactly two
    documented suffixes. For the failure mode of the plain call, look at what PHP emits as well
    as what the function returns — one of the two is easy to miss under a `@`.

??? success "Show the solution"

    ```php
    <?php
    declare(strict_types=1);

    $title = "Facture 5€ — café";

    foreach (['ASCII', 'ASCII//TRANSLIT', 'ASCII//IGNORE'] as $target) {
        $out = @\iconv('UTF-8', $target, $title);
        printf("%-16s %s\n", $target, false === $out ? '(false)' : $out);
    }
    ```

    ```text
    ASCII            (false)
    ASCII//TRANSLIT  Facture 5EUR -- cafe
    ASCII//IGNORE    Facture 5  caf
    ```

    - **Plain `ASCII`** — an `E_NOTICE` is generated and the function returns `false`. Loud, and
      safe: you cannot ship corrupted output by accident, but you must handle `false`.
    - **`//IGNORE`** — unrepresentable characters "are silently discarded". You keep a string,
      but `5€` becomes `5 ` and `café` becomes `caf`: a data-integrity bug in an invoice, and a
      word that is no longer the word the user typed.
    - **`//TRANSLIT`** — the character "may be approximated through one or several similarly
      looking characters". The manual warns that how it works "depends on the system's iconv
      implementation" and that "some implementations are known to ignore `//TRANSLIT`".

    Symfony hits this exact wall. `AbstractUnicodeString::ascii()` uses ICU transliteration when
    `transliterator_transliterate()` exists, and otherwise falls back to iconv — where it probes
    the implementation and throws a `LogicException` telling you to install `gnu-libiconv` if
    you are on Alpine Linux. Without either, non-ASCII characters degrade to `?`.

    **Why it works:** iconv exposes the system's conversion facility, so its capabilities are a
    property of the host, not of PHP. That is the structural difference from mbstring, which
    ships its own conversion tables and therefore behaves identically everywhere.

    **Certification takeaway:** mbstring is portable and self-contained; iconv is a thin binding
    to the platform. When a question asks which one gives you `//TRANSLIT`, the answer is iconv —
    and the follow-up is "with no guarantee".

    **Official reference:** https://www.php.net/manual/en/function.iconv.php

## Exercise 7 · Expert challenge — make the platform contract actually true

**Objective:** Discover that `"ext-mbstring": "*"` does not prove the module is installed, then
build a check that cannot be fooled, and finish with the OPcache deployment rule that turns a
green deploy into stale code.

**Context:** A production incident. `composer install` was green, `composer.json` requires
`ext-mbstring` and `ext-intl`, yet dates render in English and a slug endpoint returns
question marks.

**Starting point:** a project whose `composer.json` contains:

```json
{
    "require": {
        "php": ">=8.4",
        "ext-mbstring": "*",
        "symfony/string": "^8.0"
    }
}
```

**Task:**

1. Explain how `composer install` can succeed on a host with **no** `mbstring` module.
2. Give the command that would have caught it, and say what makes that command different from
   `composer install`.
3. Then explain why, after you fix the extensions and redeploy, the site may *still* serve the
   old behaviour, and list the three documented ways out.

**Expected observation:** the dependency graph, not the host, satisfied the requirement — and a
second, unrelated cache is holding the old bytecode.

??? tip "Show a hint"
    Open `vendor/symfony/polyfill-mbstring/composer.json` and read the key that is neither
    `require` nor `suggest`. For step 2, one Composer subcommand is documented as ignoring
    `config.platform` on purpose. For step 3, remember that the CLI process and the web process
    do not share anything.

??? success "Show the solution"

    **1. Why the install succeeded.** `symfony/polyfill-mbstring` declares:

    ```json
    {
        "require": { "php": ">=7.2", "ext-iconv": "*" },
        "provide": { "ext-mbstring": "*" },
        "suggest": { "ext-mbstring": "For best performance" }
    }
    ```

    `provide` tells Composer "this package supplies that package name". `symfony/string` depends
    on the polyfill, so the polyfill enters the graph, and the virtual `ext-mbstring` platform
    package is satisfied by it rather than by the real module. The install is green and every
    `mb_*` call is served by userland PHP — correct, but slower, and the `suggest` line is the
    only hint you get. Note that the polyfill itself requires `ext-iconv`, which is one reason
    `iconv` appears in Symfony's documented technical requirements while `mbstring` does not.

    **2. The command that catches it.**

    ```console
    $ composer check-platform-reqs
    ```

    Composer documents it as checking "that your PHP and extensions versions match the platform
    requirements of the installed packages", and — the decisive part — "unlike update/install,
    this command will ignore `config.platform` settings and check the real platform packages".
    It inspects the machine you run it on, which is why it belongs in the deploy pipeline on the
    **target** host, not on the build agent. Add `--no-dev` there so dev-only requirements do not
    fail a production check.

    **3. Why the fix does not appear.** If the server runs `opcache.validate_timestamps=0` —
    which Symfony's performance page recommends for production — OPcache never stats source
    files again, so new code is invisible until the cache is reset. `opcache.revalidate_freq`
    does not help: it is explicitly ignored when `validate_timestamps` is disabled. The
    documented ways to clear it are:

    1. restart the web server (or the PHP-FPM pool);
    2. call `opcache_reset()` **through the web server**, since CLI and web processes do not
       share an OPcache;
    3. use an external tool such as `cachetool` to talk to the FPM socket from the CLI.

    A robust deploy therefore ends with an explicit OPcache reset, and — if you use
    `opcache.preload` pointing at `config/preload.php` — a full PHP process restart, because
    preloaded scripts can only be cleared by restarting the process.

    **Why it works:** each layer is a *contract about the environment*, and each one can be
    satisfied in a way you did not intend. Composer's contract is about the dependency graph;
    `check-platform-reqs` re-asks the question against reality; OPcache's contract is about file
    timestamps, and you opted out of it for speed.

    **Certification takeaway:** `ext-*` in `require` gates resolution, not reality. A `provide`
    can satisfy it, `--ignore-platform-req` can bypass it, and `config.platform` can fake it.
    Only `composer check-platform-reqs` — plus `extension_loaded()` at runtime — tells you what
    the host really has.

    **Official reference:** https://getcomposer.org/doc/03-cli.md#check-platform-reqs

---

<small>Back to the lesson: [PHP Extensions](extensions.md) ·
[Take the topic exam](extensions-exam.md)</small>

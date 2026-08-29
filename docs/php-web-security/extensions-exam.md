# Topic Exam — PHP Extensions

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because extension questions
    are built on near-misses: one wrong module name, one integer instead of a string, one
    inverted argument order, and the answer flips.

    Theory: **[PHP Extensions](extensions.md)** ·
    Practice: **[Guided exercises](extensions-exercises.md)** ·
    Recall: **[Flashcards](extensions-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4** and **Symfony 8.0**.

## Detecting and requiring extensions

??? question "Question 1 · Detection API"
    Which call reliably reports whether an extension is loaded?

    - A. `extension_loaded('intl')`
    - B. `include 'intl'`
    - C. `require_extension('intl')`
    - D. `ini_get('intl')`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `extension_loaded()` takes a module name and returns a `bool`
        saying whether that module is loaded. The parameter is case-insensitive, so
        `extension_loaded('INTL')` works too.

        **B** is wrong because `include` expects a *file path*: it would look for a file
        literally named `intl` on the include path, emit a warning, and return `false` —
        nothing to do with modules. **C** invents a function; `require_extension()` does not
        exist in PHP and calling it raises `Error: Call to undefined function`. **D** is
        wrong because `ini_get()` reads an **INI directive**, not a module: there is no INI
        setting called `intl`, so it returns `false` whether or not the extension is present
        — a silent false negative.

        **Official reference:** https://www.php.net/manual/en/function.extension-loaded.php

??? question "Question 2 · Composer platform requirement"
    How do you make `composer install` fail on a host lacking the `intl` extension?

    - A. Add `"ext-intl": "*"` to the `require` section of `composer.json`
    - B. Add it to the `autoload` section
    - C. Set an environment variable such as `PHP_EXT_INTL=1`
    - D. Nothing — Composer detects the extensions your code uses automatically

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** Composer exposes the environment as **virtual platform packages**
        (`php`, `ext-*`, `lib-*`, `composer-*`). Requiring `ext-intl` makes the solver check
        the real environment at install/update time and abort when the module is absent. No
        code is downloaded: a platform package only gates.

        **B** is wrong: `autoload` configures class-to-file mapping (PSR-4, classmap, files)
        and is never consulted for platform checks. **C** is wrong: Composer reads
        `composer.json` and the actual PHP runtime, not ad-hoc environment variables; the
        only env knobs are things like `COMPOSER_*` flags, and none of them add a
        requirement. **D** is wrong: Composer performs no static analysis of your source, so
        an undeclared `ext-*` is simply never checked.

        **Official reference:** https://getcomposer.org/doc/articles/composer-platform-dependencies.md

??? question "Question 3 · Symfony 8 documented requirements · Multiple answers"
    According to the Symfony 8.0 "Technical Requirements", which PHP extensions must be
    installed before creating a Symfony application? (Choose all that apply.)

    - A. `Ctype`
    - B. `iconv`
    - C. `mbstring`
    - D. `Tokenizer`

    ??? success "Show answer"
        **Correct answers:** A, B and D

        **Explanation:** the Symfony 8.0 setup page lists exactly six extensions beside
        PHP 8.4+: **Ctype, iconv, PCRE, Session, SimpleXML and Tokenizer** — noting that they
        are installed and enabled by default in most PHP 8 installations. `Ctype`, `iconv`
        and `Tokenizer` are three of those six.

        **C** is the trap. `mbstring` is *not* in the documented requirement list, because
        Symfony ships `symfony/polyfill-mbstring` as a hard Composer dependency: a userland
        implementation is always available, so the native module is a performance choice, not
        a prerequisite. (The polyfill itself requires `ext-iconv`, which is one reason
        `iconv` *is* on the list.) Do not confuse "Symfony works better with it" with
        "Symfony requires it".

        **Official reference:** https://symfony.com/doc/8.0/setup.html#symfony-tech-requirements

??? question "Question 4 · Debugging a false sense of safety"
    A project's `composer.json` contains `"ext-mbstring": "*"`. `composer install` succeeds
    on a server, yet a colleague insists that server has no `mbstring` module compiled in.
    What is the most likely explanation?

    - A. Composer downloaded and compiled `mbstring` during install
    - B. `symfony/polyfill-mbstring` is installed and declares `"provide": {"ext-mbstring": "*"}`, which satisfies the requirement
    - C. Composer only checks `ext-*` requirements on `composer update`, never on `install`
    - D. `ext-*` entries are advisory comments and are never enforced

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `symfony/polyfill-mbstring` lists `ext-mbstring` in its `provide`
        block. `provide` tells the solver "this package supplies that package name", so once
        the polyfill is in the dependency graph the virtual `ext-mbstring` requirement is
        satisfied by the polyfill instead of by the real module — and the install succeeds on
        a host without it. That is exactly the portability the polyfill exists for, and
        exactly why `ext-*` alone is not proof that a native extension is present. Verify the
        real platform with `composer check-platform-reqs`, which ignores such substitutions
        for `config.platform` and inspects the actual runtime.

        **A** is impossible: platform packages install no code, and Composer cannot build C
        extensions. **C** is wrong: platform requirements are verified on `install` as well as
        `update` (`install` re-checks the locked requirements against the current platform).
        **D** is wrong: `ext-*` requirements are genuinely enforced — the only ways around them
        are `--ignore-platform-req(s)`, the `config.platform` override, or a `provide` as
        described here.

        **Official reference:** https://getcomposer.org/doc/04-schema.md#provide

??? question "Question 5 · Verifying the real platform"
    Which statement about `composer check-platform-reqs` is correct?

    - A. It is a synonym for `composer validate`
    - B. It checks that your PHP and extension versions match the platform requirements of the installed packages, and ignores `config.platform` so it sees the real machine
    - C. It installs any missing PHP extensions
    - D. It only inspects `composer.json`, never the installed packages

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the command exists precisely to answer "will this production server
        actually run what I installed?". Composer's own documentation states that, unlike
        `install`/`update`, it **ignores `config.platform` settings and checks the real
        platform packages**, so a fake platform pinned for reproducible resolution cannot hide
        a missing module.

        **A** is wrong: `composer validate` lints the *schema and semantics of `composer.json`
        itself* (required fields, version constraints, license), not the host. **C** is wrong:
        no Composer command compiles or installs a C extension; that is the job of your OS
        package manager, `pecl`, or your Docker image. **D** is wrong: it walks the
        requirements of the **installed** packages (or, with `--lock`, those in the lock file)
        — that is what makes it useful on a deployment target.

        **Official reference:** https://getcomposer.org/doc/03-cli.md#check-platform-reqs

## Bytes versus characters — mbstring

??? question "Question 6 · Byte semantics"
    For a UTF-8 encoded string, `strlen('é')` returns…

    - A. 1
    - B. 2
    - C. 0
    - D. 4

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `strlen()` counts **bytes**, and `é` (U+00E9) is encoded as two bytes
        (`0xC3 0xA9`) in UTF-8. The character count is what `mb_strlen($s, 'UTF-8')` returns,
        and that is `1`.

        **A** is the character count, which requires `mb_strlen()` — that is the whole point of
        the question. **C** would only be true for the empty string; `strlen()` never returns 0
        for a non-empty string. **D** would be the byte length in UTF-32, which PHP does not use
        for its native string type.

        **Official reference:** https://www.php.net/manual/en/function.strlen.php

??? question "Question 7 · Code analysis"
    What do the two lines print?

    ```php
    <?php
    echo strlen('café'), "\n";
    echo mb_strlen('café', 'UTF-8'), "\n";
    ```

    - A. `4` then `4`
    - B. `4` then `5`
    - C. `5` then `4`
    - D. `5` then `5`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** `café` is `c`, `a`, `f` (one byte each) plus `é` (two bytes) = **5
        bytes**, so `strlen()` prints `5`. `mb_strlen()` counts characters and prints **4**:
        the manual states that a multi-byte character is counted as 1.

        **A** assumes `strlen()` is character-aware; it is not — it is a pure byte count and has
        no notion of encoding. **B** inverts the two, which would require `strlen()` to be
        multibyte-aware and `mb_strlen()` to be byte-based — the exact opposite of reality.
        **D** assumes `mb_strlen()` counts bytes, which would make the function pointless.

        **Official reference:** https://www.php.net/manual/en/function.mb-strlen.php

??? question "Question 8 · Edge case"
    Given `$s = 'café';` (UTF-8), what is the result of `substr($s, 0, 4)`?

    - A. `'café'`
    - B. `'caf'`
    - C. Four bytes: `caf` plus the first byte of `é`, i.e. an invalid UTF-8 sequence
    - D. A `ValueError`, because the offset splits a character

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** `substr()` slices **bytes**. Asking for four bytes yields `0x63 0x61
        0x66 0xC3` — the three ASCII letters plus the *lead byte* of the two-byte `é`. The
        result is a broken UTF-8 string that most terminals and browsers render as a
        replacement character, and that will make `mb_check_encoding($result, 'UTF-8')` return
        `false`. `mb_substr($s, 0, 4, 'UTF-8')` returns the whole `'café'` because it counts
        characters.

        **A** would require `substr()` to be multibyte-aware. **B** describes a three-byte
        slice, i.e. `substr($s, 0, 3)`. **D** is wrong and dangerous to believe: PHP does not
        validate encodings in byte functions, so nothing is thrown — the corruption is
        **silent**, which is why it usually surfaces much later as mojibake in a database or a
        broken JSON response.

        **Official reference:** https://www.php.net/manual/en/function.mb-substr.php

??? question "Question 9 · Argument order · Code analysis"
    Which call correctly converts `$s` from `ISO-8859-1` to `UTF-8`?

    - A. `iconv('UTF-8', 'ISO-8859-1', $s)`
    - B. `iconv('ISO-8859-1', 'UTF-8', $s)`
    - C. `mb_convert_encoding($s, 'ISO-8859-1', 'UTF-8')`
    - D. `mb_convert_encoding('ISO-8859-1', 'UTF-8', $s)`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the two functions take their arguments in **different orders**, and
        that is the entire trap. `iconv(string $from_encoding, string $to_encoding, string
        $string)` puts the string **last**; `mb_convert_encoding(array|string $string, string
        $to_encoding, array|string|null $from_encoding = null)` puts it **first** and the
        *source* encoding last. So B is right, and the mbstring equivalent would be
        `mb_convert_encoding($s, 'UTF-8', 'ISO-8859-1')`.

        **A** converts in the wrong direction: it declares the input to be UTF-8 and asks for
        Latin-1 output. **C** has the mbstring order right but the encodings swapped — it
        produces Latin-1 from a string it assumes is UTF-8. **D** mixes both mistakes: it
        passes encodings where the string belongs, so mbstring would try to convert the literal
        text `"ISO-8859-1"`.

        **Official reference:** https://www.php.net/manual/en/function.mb-convert-encoding.php

??? question "Question 10 · iconv conversion modes"
    `iconv('UTF-8', $target, "This costs 5€")` is called with three different targets. Match
    the behaviour: which statement is correct?

    - A. `'ASCII//TRANSLIT'` approximates `€` with similar characters; `'ASCII//IGNORE'` silently drops it; plain `'ASCII'` emits an `E_NOTICE` and returns `false`
    - B. `'ASCII//TRANSLIT'` drops `€`; `'ASCII//IGNORE'` approximates it; plain `'ASCII'` returns the string unchanged
    - C. All three return the same string, because iconv always transliterates
    - D. `'ASCII//IGNORE'` throws an `Exception` when a character cannot be represented

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual documents the three modes exactly: appending `//TRANSLIT`
        activates transliteration so an unrepresentable character "may be approximated through
        one or several similarly looking characters"; appending `//IGNORE` silently discards
        such characters; with neither suffix an `E_NOTICE` is generated and the function
        returns `false`. Note the caveat that `//TRANSLIT`'s exact behaviour depends on the
        system's iconv implementation — musl-based images such as Alpine are known to ignore
        it.

        **B** swaps `//TRANSLIT` and `//IGNORE` and invents a pass-through for plain `ASCII`.
        **C** is wrong: transliteration is opt-in via the suffix, never the default. **D** is
        wrong: `//IGNORE` is the *silent* mode; iconv signals failure with a notice and `false`,
        not with an exception.

        **Official reference:** https://www.php.net/manual/en/function.iconv.php

??? question "Question 11 · Invalid encoding · True/False"
    True or false: on PHP 8.4, `mb_strlen('abc', 'NOT-A-CHARSET')` emits a warning and returns
    `false`.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B (False)

        **Explanation:** as of **PHP 8.0.0**, mbstring functions throw a `ValueError` when the
        `encoding` argument names an invalid encoding. The warning-plus-`false` behaviour the
        statement describes is the **pre-8.0** behaviour, and code that still writes
        `if (false === mb_strlen(...))` is checking for something that can no longer happen —
        the uncaught `ValueError` becomes a fatal error instead.

        **A** is wrong for the reason above. This matters in practice because encoding names
        often arrive from configuration or user input; validate them, or catch `ValueError`.

        **Official reference:** https://www.php.net/manual/en/function.mb-strlen.php

??? question "Question 12 · Counting units · Expert trap"
    For the family emoji `👨‍👩‍👧` (three emoji joined by zero-width joiners) on a UTF-8 system,
    which set of results is correct?

    - A. `strlen()` = 18, `mb_strlen()` = 5, `grapheme_strlen()` = 1
    - B. `strlen()` = 1, `mb_strlen()` = 1, `grapheme_strlen()` = 1
    - C. `strlen()` = 3, `mb_strlen()` = 3, `grapheme_strlen()` = 3
    - D. `strlen()` = 5, `mb_strlen()` = 18, `grapheme_strlen()` = 5

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** there are three *counting units*, and they disagree. Bytes: each of
        the three emoji takes 4 bytes in UTF-8 and each of the two zero-width joiners takes 3,
        giving 18. Code points: 3 emoji + 2 joiners = 5, which is what `mb_strlen()` returns.
        Grapheme clusters — what a human calls "one character on screen" — is 1, which only
        `grapheme_strlen()` (from `intl`) reports.

        **B** would be true only if PHP strings stored graphemes, which they do not. **C**
        confuses the number of emoji with any of the three measures and forgets the joiners.
        **D** inverts bytes and code points. Symfony's String component exposes the same three
        levels as `ByteString`, `CodePointString` and `UnicodeString`, so knowing which unit
        you are counting is a Symfony question as much as a PHP one.

        **Official reference:** https://www.php.net/manual/en/function.grapheme-strlen.php

## ctype

??? question "Question 13 · The integer trap"
    What is the classic gotcha with `ctype_digit(123)` (an **integer** argument)?

    - A. Integers between -128 and 255 are interpreted as an ASCII character code, not as their digits — so `ctype_digit(123)` tests the character `{` and returns `false`
    - B. It always returns `true` for any integer
    - C. It throws a `TypeError` for non-string arguments
    - D. The integer is cast to a string first, so it behaves exactly like `ctype_digit('123')`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual is explicit: "If an `int` between -128 and 255 inclusive is
        provided, it is interpreted as the ASCII value of a single character… Any other
        integer is interpreted as a string containing the decimal digits of the integer."
        `123` falls inside that window, so the check runs against character code 123, which is
        `{` — not a digit — and the result is `false`. Sadistically, `ctype_digit(1234)` **is**
        `true`, because 1234 is outside the window and gets stringified.

        **B** is wrong, as the `123` case demonstrates. **C** is wrong: nothing is thrown — but
        note that as of PHP 8.1.0 passing a non-string argument is **deprecated**, so you get a
        deprecation notice, not a `TypeError`. **D** describes the intuition everyone has and
        the reason this trap works; stringification happens only *outside* the -128..255 range.

        **Official reference:** https://www.php.net/manual/en/function.ctype-digit.php

??? question "Question 14 · Empty string edge case"
    What does `ctype_digit('')` return?

    - A. `true`, because there is no non-digit character in the string
    - B. `false`
    - C. `null`
    - D. It throws a `ValueError`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual states the rule for the whole `ctype_*` family: "When
        called with an empty string the result will always be `false`." That is deliberate,
        because these functions are used as validators and an empty value should not pass a
        "consists only of digits" test.

        **A** is the vacuous-truth reading a mathematician would expect, and it is precisely
        what PHP does *not* do here. **C** is wrong: the return type is `bool`, never `null`.
        **D** is wrong: an empty string is a perfectly valid argument, so nothing is thrown —
        which is why the surprising `false` is easy to miss in a validation chain.

        **Official reference:** https://www.php.net/manual/en/function.ctype-digit.php

??? question "Question 15 · Deprecation · True/False"
    True or false: as of PHP 8.1.0, passing a non-string argument to a `ctype_*` function is
    deprecated.

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** A (True)

        **Explanation:** the manual carries a warning on every `ctype_*` page: "As of PHP
        8.1.0, passing a non-string argument is deprecated. In the future, the argument will be
        interpreted as a string instead of an ASCII codepoint." The documented fix is to cast
        explicitly to `string`, or to call `chr()` when you really did mean a codepoint.

        **B** is wrong. The practical consequence is that the ASCII-codepoint behaviour is a
        **transitional** rule: code that relies on `ctype_digit($int)` returning `false` for a
        small integer is depending on behaviour PHP has announced it will change, which is one
        more reason to always pass strings.

        **Official reference:** https://www.php.net/manual/en/function.ctype-digit.php

## intl

??? question "Question 16 · Locale-aware sorting"
    German words `['Zebra', 'Äpfel', 'Apfel', 'Öl']` are sorted twice: once with PHP's `sort()`
    and once with `usort()` using `(new Collator('de_DE'))->compare(...)`. What differs?

    - A. Nothing — both produce the same order
    - B. `sort()` orders by byte value, so `Äpfel` and `Öl` land after `Zebra`; the `Collator` applies German collation rules and places `Apfel`, `Äpfel`, `Öl`, `Zebra`
    - C. `sort()` is locale-aware since PHP 8.0 and matches the `Collator`
    - D. `Collator::compare()` sorts by string length

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `sort()` falls back to a byte-wise comparison. In UTF-8, `Ä` starts
        with byte `0xC3`, which is numerically greater than `Z` (`0x5A`), so every accented
        word is exiled to the end of the list — the classic "why is Äpfel after Zebra?" bug.
        `Collator` implements the Unicode Collation Algorithm through ICU with locale-specific
        tailoring, producing the order a German reader expects.

        **A** is wrong, as the byte values show. **C** invents a change: PHP's `sort()` has no
        locale awareness, and no PHP 8 release added any. **D** is wrong: `Collator::compare()`
        is a lexicographic comparison under collation rules; length plays no special role.

        **Official reference:** https://www.php.net/manual/en/class.collator.php

??? question "Question 17 · Symfony without ext-intl · Multiple answers"
    Which statements about running a Symfony 8 application **without** the native `intl`
    extension are correct? (Choose all that apply.)

    - A. `symfony/polyfill-intl-icu` supplies `Collator`, `NumberFormatter`, `Locale`, `IntlDateFormatter` and `IntlListFormatter`, but is limited to the `en` locale
    - B. The application refuses to boot with a fatal error
    - C. The Symfony documentation states you must install the PHP `intl` extension when translating into locales other than English
    - D. `Symfony\Component\String\AbstractUnicodeString::ascii()` degrades rather than crashing, because it only adds the `any-latin/bgn` transliteration rule when `transliterator_transliterate()` exists

    ??? success "Show answer"
        **Correct answers:** A, C and D

        **Explanation:** the whole design is graceful degradation. The ICU polyfill's own
        README states the class list and the "limited to the `en` locale" restriction (A). The
        Symfony 8.0 translation page says the polyfills "only support English translations, so
        you must install the PHP `intl` extension when translating into other languages" (C).
        And the String component guards the ICU-only rule behind a `function_exists()` check,
        falling back to an iconv-based transliteration and finally to replacing non-ASCII
        characters with `?` (D).

        **B** is the trap: nothing fatals. That is *worse* than a crash for a certification
        candidate to forget, because the failure mode in production is silently wrong output —
        English month names on a French page, unsorted accented names — rather than an
        exception in the log.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/String/AbstractUnicodeString.php

??? question "Question 18 · Which constraint needs what"
    Symfony's `Locale`, `Country` and `Currency` validation constraints check their value
    against…

    - A. The native `intl` extension, which is therefore mandatory for them
    - B. The ICU data bundled in the `symfony/intl` **Composer package** (`Locales::exists()`, `Countries::exists()`, `Currencies::exists()`)
    - C. A hard-coded list inside the Validator component
    - D. A remote call to the Unicode CLDR service

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `LocaleValidator` calls `Symfony\Component\Intl\Locales::exists()`,
        `CountryValidator` calls `Countries::exists()` (or `alpha3CodeExists()`), and
        `CurrencyValidator` calls `Currencies::exists()`. Those classes read the ICU data files
        shipped inside the `symfony/intl` package, which is a `require-dev` of the Validator
        component and requires only `php >= 8.4` — no native extension.

        **A** confuses the *component* `symfony/intl` with the *extension* `ext-intl`; they are
        different things with confusingly similar names, and this is the single most common
        mix-up on the topic. **C** is wrong: hard-coded lists would rot with every CLDR release,
        which is exactly why the data lives in a versioned package. **D** is wrong and would be
        an unacceptable dependency: validation is offline and deterministic.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Validator/Constraints/LocaleValidator.php

## OPcache

??? question "Question 19 · What is cached"
    What does the OPcache extension cache?

    - A. Compiled PHP bytecode in shared memory
    - B. Database query results
    - C. HTTP responses
    - D. Rendered Twig templates

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** OPcache stores the **opcodes** produced by compiling a PHP script into
        shared memory, so subsequent requests skip lexing, parsing and compiling. The Symfony
        performance page describes it in the same terms: it "caches the compiled bytecode of
        PHP scripts to avoid recompiling them on each request".

        **B** is a job for a data cache — APCu, Redis, Doctrine's result cache, or the Symfony
        Cache component. **C** is HTTP caching: a reverse proxy, or Symfony's own
        `HttpCache`/`Cache-Control` handling. **D** is Twig's own compilation cache, which
        writes PHP classes to `var/cache/`; OPcache then caches *those generated PHP files* as
        bytecode, which is a different layer. Conflating the bytecode cache with a key/value
        data cache is the classic misconception here.

        **Official reference:** https://symfony.com/doc/8.0/performance.html#performance-use-opcache

??? question "Question 20 · Module name · Expert trap"
    On a server where OPcache is active, what does `var_dump(extension_loaded('opcache'));`
    print, and why?

    - A. `bool(true)` — `opcache` is the module name
    - B. `bool(false)` — the module registers under the name `Zend OPcache`, so you must test `extension_loaded('Zend OPcache')`
    - C. `bool(false)` — `extension_loaded()` cannot see Zend extensions at all
    - D. It throws, because `opcache` is not a valid extension name

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** OPcache registers its module entry as **`Zend OPcache`**, which is the
        name `php -m` prints (in both the `[PHP Modules]` and `[Zend Modules]` sections) and the
        name `php --ri "Zend OPcache"` expects. Since `extension_loaded()` is case-insensitive
        but not fuzzy, `'opcache'` simply does not match. Symfony's own `about` command settles
        the argument: it reports the OPcache row using `\extension_loaded('Zend OPcache')`.

        **A** is the intuitive guess that fails, and it is why so many "is OPcache on?" health
        checks report a false negative. **C** is wrong: the module shows up in
        `get_loaded_extensions()` as well as in `get_loaded_extensions(true)`. **D** is wrong:
        `extension_loaded()` never throws for an unknown name — it just returns `false`, which
        is what makes the mistake silent.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Command/AboutCommand.php

??? question "Question 21 · How OPcache is loaded"
    Which php.ini line loads OPcache?

    - A. `extension=opcache`
    - B. `zend_extension=opcache`
    - C. `opcache.load=1`
    - D. `auto_prepend_file=opcache.php`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** OPcache is a **Zend extension**: it hooks the compiler itself, so it is
        loaded with the `zend_extension` directive — `zend_extension=/full/path/to/opcache.so`
        on Unix-like systems, `zend_extension=C:\path\to\php_opcache.dll` on Windows. The manual
        also warns that if you use Xdebug too, OPcache must be loaded first.

        **A** is the ordinary-extension directive and will not load OPcache. **C** invents a
        directive; the real switch is `opcache.enable`, which defaults to `1` — but a default of
        `1` is meaningless until the extension has been loaded, which is why "`opcache.enable=1`
        is set yet OPcache is off" is such a common support ticket. **D** is a completely
        unrelated INI setting that prepends a PHP file to every script.

        **Official reference:** https://www.php.net/manual/en/opcache.installation.php

??? question "Question 22 · Configuration consequence"
    You deploy new code to a server running `opcache.validate_timestamps=0` and forget to reset
    OPcache. What do requests serve?

    - A. The stale, previously cached bytecode — OPcache never notices the file changed
    - B. The new code, because PHP still compares mtimes on every request
    - C. A fatal error, because the cached bytecode no longer matches the file hash
    - D. The new code, but only after `opcache.revalidate_freq` seconds elapse

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** with `opcache.validate_timestamps=0` OPcache trusts its cache
        unconditionally and stops stat-ing source files — that removed syscall *is* the
        performance win. The manual states that when the directive is disabled "you must reset
        OPcache manually via `opcache_reset()`, `opcache_invalidate()` or by restarting the Web
        server for changes to the filesystem to take effect". Symfony's performance page adds
        the operational catch: CLI and web processes do not share an OPcache, so running a
        command in your terminal cannot clear the web server's cache.

        **B** contradicts the directive's entire purpose. **C** invents a hash check; OPcache
        keys on the file path, not on content, and no integrity error is raised. **D** is the
        subtlest distractor: `opcache.revalidate_freq` is **ignored** when
        `opcache.validate_timestamps` is disabled, so waiting changes nothing — ever.

        **Official reference:** https://www.php.net/manual/en/opcache.configuration.php#ini.opcache.validate-timestamps

??? question "Question 23 · Preloading semantics · Multiple answers"
    Which statements about OPcache preloading (`opcache.preload`) are correct? (Choose all that
    apply.)

    - A. Functions, classes, interfaces and traits declared by the preloaded files become available to every request without being included
    - B. Constants defined in preloaded files are preloaded in the same way
    - C. Clearing preloaded scripts requires restarting the PHP process
    - D. Preloading is not supported on Windows

    ??? success "Show answer"
        **Correct answers:** A, C and D

        **Explanation:** the manual's preloading page states all three: preloading makes "any
        functions, classes, interfaces, or traits (but not constants) in those files… globally
        available for all requests"; it "requires restarting the PHP process to clear pre-loaded
        scripts, meaning this feature is only practical to use in production"; and a note adds
        that "preloading is not supported on Windows".

        **B** is the exception the manual calls out explicitly, and it is the detail examiners
        like: constants are **not** handled by preloading, which is why a later `include` of an
        already-preloaded file may still be needed to obtain its global constants. In Symfony,
        `opcache.preload` points at `config/preload.php`, and the `container.preload` /
        `container.no_preload` service tags let you choose what goes in.

        **Official reference:** https://www.php.net/manual/en/opcache.preloading.php

??? question "Question 24 · Symfony's recommended OPcache tuning"
    The Symfony 8.0 performance page recommends raising `opcache.interned_strings_buffer` well
    above its default. Why?

    - A. Because Symfony applications use a very large number of fully-qualified class names, and the default 8 MB buffer is too low
    - B. Because interned strings store the HTTP response body
    - C. Because it controls how many files OPcache may cache
    - D. Because Symfony stores its service container in that buffer

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the documentation's own comment next to `opcache.interned_strings_buffer=32`
        reads: "memory (in MB) for interned strings; the default value (8 MB) is too low for
        Symfony applications, which use many fully-qualified class names". String interning
        stores one shared copy of each repeated string; FQCNs are long and repeat constantly in a
        compiled container, so the buffer fills quickly.

        **B** is wrong: response bodies are ordinary request-scoped strings, not interned
        constants. **C** describes `opcache.max_accelerated_files` (default 10000; Symfony
        suggests 32531). **D** is wrong: the compiled container is dumped to PHP files in
        `var/cache/` and is then cached as *bytecode* like any other file.

        **Official reference:** https://symfony.com/doc/8.0/performance.html#performance-configure-opcache

## PDO and the extension catalogue

??? question "Question 25 · PDO and its drivers"
    Which statement about PDO is correct?

    - A. `ext-pdo` alone is enough to connect to MySQL, because PDO speaks every protocol itself
    - B. PDO is a common interface, and each database needs its own driver extension (`pdo_mysql`, `pdo_pgsql`, `pdo_sqlite`, …); `PDO::getAvailableDrivers()` lists the ones present
    - C. Drivers must be loaded *before* `pdo` in php.ini
    - D. `PDO::getAvailableDrivers()` returns every driver PHP could theoretically support, whether installed or not

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** PDO defines the API; the database-specific extensions implement it.
        `PDO::getAvailableDrivers()` (aliased as `pdo_drivers()`) "returns all currently
        available PDO drivers which can be used in the DSN parameter of `PDO::__construct`", and
        returns an empty array when none are available.

        **A** is wrong: without `pdo_mysql`, `new PDO('mysql:...')` fails with "could not find
        driver". **C** inverts the documented order — the manual says drivers "must be loaded
        after PDO itself", because PDO has to be initialised first. **D** is wrong: the list
        reflects what is loaded right now, which is exactly what makes it useful as a runtime
        check.

        **Official reference:** https://www.php.net/manual/en/pdo.getavailabledrivers.php

??? question "Question 26 · Core versus bundled · Expert trap"
    Which statement matches the PHP manual's extension categorisation?

    - A. `json` is a **core** extension that is always enabled; before PHP 8.0.0 it was bundled and could be disabled with `--disable-json`
    - B. `mbstring` is enabled by default and must be switched off with `--disable-mbstring`
    - C. `intl` needs no external library
    - D. PECL extensions ship inside the PHP source distribution

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** the manual's JSON installation page says precisely this: "The JSON
        extension is a core PHP extension, so it is always enabled. Prior to PHP 8.0.0, the JSON
        extension was bundled and compiled into PHP by default, but could be explicitly disabled
        using `--disable-json`." That single sentence illustrates the difference between *core*
        (cannot be removed) and *bundled* (ships with PHP, still optional).

        **B** is backwards: mbstring is documented as "a non-default extension… not enabled by
        default", requiring `--enable-mbstring`. Compare `ctype` (`--disable-ctype`) and `iconv`
        (`--without-iconv`), which really are on by default. **C** is wrong: `intl` is a wrapper
        around the **ICU** library and cannot be built without it. **D** is wrong by definition:
        PECL extensions are distributed separately from the PHP source and installed on their
        own, which is why they never appear in a stock build.

        **Official reference:** https://www.php.net/manual/en/extensions.membership.php

??? question "Question 27 · Choosing the right introspection call"
    You need the *version string* of the loaded `intl` extension, or a clear signal that it is
    absent. Which call is designed for that?

    - A. `extension_loaded('intl')`
    - B. `phpversion('intl')`
    - C. `get_extension_funcs('intl')`
    - D. `ini_get('intl.version')`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `phpversion(?string $extension = null)` returns the version of the named
        extension, or `false` "if there is no version information associated or the extension
        isn't enabled". That single call gives you both the version and the presence signal.

        **A** returns only a `bool` — correct for presence, useless for a version constraint.
        **C** returns the *function names* the module defines (or `false` for an unknown module);
        the manual notes the parameter must be given in lowercase. It is the right tool for "does
        this build expose `mb_str_pad()`?", not for a version. **D** invents an INI directive;
        extension versions are not exposed through the INI system.

        **Official reference:** https://www.php.net/manual/en/function.phpversion.php

---

<small>Back to the lesson: [PHP Extensions](extensions.md) ·
[Guided exercises](extensions-exercises.md) · [Review flashcards](extensions-flashcards.md)</small>

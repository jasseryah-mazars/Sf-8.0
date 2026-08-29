# Flashcards — PHP Extensions

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[PHP Extensions](extensions.md)** ·
    Practice: **[Guided exercises](extensions-exercises.md)** ·
    Test: **[Topic exam](extensions-exam.md)**

## What an extension is

??? question "What is a PHP extension, in one sentence?"
    Think before revealing the answer.

    ??? success "Show answer"
        A compiled module — usually written in C — that registers additional functions,
        classes, constants and INI directives into the PHP engine at startup. PHP's own core is
        small; almost everything you think of as "PHP" arrives through an extension.

        **Why it matters:** it explains why a function can be undefined on one server and
        present on another with the *same PHP version*: the language did not change, the build
        did.

        **Official reference:** https://www.php.net/manual/en/extensions.php

??? question "Name the four membership categories the manual uses to classify extensions."
    Think before revealing the answer.

    ??? success "Show answer"
        **Core**, **bundled**, **external** and **PECL** — the four sections of the manual's
        "Extension Categorization" appendix.

        **Why it matters:** it is the vocabulary behind "is it available by default?".
        Core extensions cannot be removed, bundled ones ship with PHP but are optional, and
        PECL ones are distributed separately and must be installed on their own.

        **Official reference:** https://www.php.net/manual/en/extensions.membership.php

??? question "Give the textbook example of the difference between a *core* and a *bundled* extension."
    Think before revealing the answer.

    ??? success "Show answer"
        `json`. The manual states it is a **core** PHP extension and therefore always enabled —
        but that *prior to PHP 8.0.0* it was **bundled**, compiled in by default yet removable
        with `--disable-json`.

        **Why it matters:** the same extension changed category between versions, which proves
        the categories are about *build guarantees*, not about how useful the extension is.

        **Official reference:** https://www.php.net/manual/en/json.installation.php

??? question "Which of `mbstring`, `ctype` and `iconv` is **not** enabled by default in a stock PHP build?"
    Think before revealing the answer.

    ??? success "Show answer"
        `mbstring`. The manual calls it "a non-default extension… not enabled by default" and
        requires `--enable-mbstring`. `ctype` is on by default (`--disable-ctype` turns it off)
        and `iconv` is on by default (`--without-iconv` turns it off).

        **Why it matters:** it is the reason Symfony ships a `mbstring` polyfill but not a
        `ctype`-only stack — and the reason `mbstring` is the extension most likely to be
        missing on an unusual host.

        **Official reference:** https://www.php.net/manual/en/mbstring.installation.php

## Detecting an extension

??? question "Which function answers 'is this module loaded?', and is it case-sensitive?"
    Think before revealing the answer.

    ??? success "Show answer"
        `extension_loaded(string $extension): bool`. The manual states the parameter is
        **case-insensitive**, so `extension_loaded('INTL')` and `extension_loaded('intl')` agree.

        **Why it matters:** it is the canonical runtime guard. `function_exists()` and
        `class_exists()` test a *symbol*, which is a different question — and the wrong one when
        a polyfill has defined the symbol without the module being present.

        **Official reference:** https://www.php.net/manual/en/function.extension-loaded.php

??? question "Under what name is OPcache registered, and what does `extension_loaded('opcache')` return?"
    Think before revealing the answer.

    ??? success "Show answer"
        It registers as **`Zend OPcache`**. `extension_loaded('opcache')` returns **`false`**
        even when OPcache is running; you must write `extension_loaded('Zend OPcache')`.

        **Why it matters:** this single mismatch produces silent false negatives in health
        checks. Symfony's `about` command uses `\extension_loaded('Zend OPcache')` for exactly
        this reason.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Command/AboutCommand.php

??? question "What does `get_loaded_extensions(true)` return that `get_loaded_extensions()` does not?"
    Think before revealing the answer.

    ??? success "Show answer"
        Passing `true` restricts the list to **Zend extensions** (engine-level hooks such as
        OPcache and Xdebug) instead of regular modules. The signature is
        `get_loaded_extensions(bool $zend_extensions = false): array`.

        **Why it matters:** it mirrors the two sections `php -m` prints, `[PHP Modules]` and
        `[Zend Modules]`, and explains why OPcache appears in both.

        **Official reference:** https://www.php.net/manual/en/function.get-loaded-extensions.php

??? question "Which call gives you an extension's version *and* a presence signal at once?"
    Think before revealing the answer.

    ??? success "Show answer"
        `phpversion(?string $extension = null)`. With an extension name it returns that
        extension's version string, or **`false`** "if there is no version information
        associated or the extension isn't enabled".

        **Why it matters:** one call replaces `extension_loaded()` plus a version lookup when
        your requirement is "at least version X of this module".

        **Official reference:** https://www.php.net/manual/en/function.phpversion.php

??? question "What does `get_extension_funcs()` return, and what does the manual say about its argument?"
    Think before revealing the answer.

    ??? success "Show answer"
        An array of the function names defined by the named module, or `false` if it is not a
        valid extension. The manual states the parameter "must be in lowercase".

        **Why it matters:** it answers a question `extension_loaded()` cannot — "does *this
        build* of the module expose the function I need?" — which matters for functions added in
        a later PHP version.

        **Official reference:** https://www.php.net/manual/en/function.get-extension-funcs.php

??? question "Which two console commands inventory a host's extensions and one extension's configuration?"
    Think before revealing the answer.

    ??? success "Show answer"
        `php -m` lists loaded modules (in `[PHP Modules]` and `[Zend Modules]` sections);
        `php --ri <name>` prints one extension's runtime information and INI values, e.g.
        `php --ri "Zend OPcache"`.

        **Why it matters:** `-m` is the fastest way to settle a "the extension is installed"
        argument, and `--ri` is the fastest way to settle "…but is it configured the way you
        think?".

        **Official reference:** https://www.php.net/manual/en/function.extension-loaded.php

## Composer and the platform

??? question "What is a Composer 'platform package', and what gets installed when you require one?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **virtual** package representing the environment: `php`, `php-64bit`, `ext-*`,
        `lib-*`, `composer-*`. Requiring one installs **no code**; its version is derived from
        the environment Composer runs in and cannot be updated or removed.

        **Why it matters:** it reframes `"ext-intl": "*"` correctly — it is a *gate*, never a
        way to obtain the extension.

        **Official reference:** https://getcomposer.org/doc/articles/composer-platform-dependencies.md

??? question "Which command lists every platform package available in your environment?"
    Think before revealing the answer.

    ??? success "Show answer"
        `composer show --platform` (short form `composer show -p`).

        **Why it matters:** it is the bridge between `php -m` and `composer.json` — it shows you
        the exact `ext-*` names Composer will match against, versions included.

        **Official reference:** https://getcomposer.org/doc/articles/composer-platform-dependencies.md

??? question "Three ways an `ext-*` requirement can be satisfied without the extension being installed."
    Think before revealing the answer.

    ??? success "Show answer"
        1. Another package **provides** it — `symfony/polyfill-mbstring` declares
           `"provide": {"ext-mbstring": "*"}`.
        2. `--ignore-platform-req=ext-mbstring` (or `--ignore-platform-reqs`) on the command
           line.
        3. A `config.platform` entry in `composer.json` faking the environment for resolution.

        **Why it matters:** all three make `composer install` green on a host that cannot run
        the code. This is the difference between a resolution contract and reality.

        **Official reference:** https://getcomposer.org/doc/04-schema.md#provide

??? question "Which Composer command verifies the **real** platform rather than the resolved one?"
    Think before revealing the answer.

    ??? success "Show answer"
        `composer check-platform-reqs`. Composer documents that, unlike `install`/`update`, it
        **ignores `config.platform` settings and checks the real platform packages**. `--lock`
        checks the lock file instead of installed packages; `--no-dev` skips `require-dev`.

        **Why it matters:** it is the one command that belongs in the deploy step on the target
        host, and the one that would have caught a polyfill silently standing in for a native
        module.

        **Official reference:** https://getcomposer.org/doc/03-cli.md#check-platform-reqs

## mbstring

??? question "`strlen()` versus `mb_strlen()` — what does each one count?"
    Think before revealing the answer.

    ??? success "Show answer"
        `strlen()` counts **bytes**. `mb_strlen($s, $encoding)` counts **characters**: the
        manual says a multi-byte character is counted as 1. For UTF-8 `'café'`: `5` versus `4`.

        **Why it matters:** it is the single most examined fact of this chapter, and the root of
        every "max length" validation bug on non-ASCII input.

        **Official reference:** https://www.php.net/manual/en/function.mb-strlen.php

??? question "Why does `substr($utf8, 0, 4)` sometimes produce an invalid string?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because it slices **bytes**. Cutting `'café'` at byte 4 keeps `0x63 0x61 0x66 0xC3` —
        the lead byte of `é` without its continuation byte. Nothing is thrown; the corruption is
        silent, and `mb_check_encoding($result, 'UTF-8')` returns `false`.

        **Why it matters:** the bug surfaces far from its cause — as mojibake in a database, a
        broken JSON response, or a mail header. `mb_substr()` is the fix.

        **Official reference:** https://www.php.net/manual/en/function.mb-substr.php

??? question "What happens when you pass an invalid encoding name to an `mb_*` function on PHP 8.4?"
    Think before revealing the answer.

    ??? success "Show answer"
        A **`ValueError`** is thrown. As of PHP 8.0.0 that replaced the old behaviour of
        emitting an `E_WARNING` and returning `false`.

        **Why it matters:** legacy code that tests `if (false === mb_strlen(...))` is guarding
        against something that can no longer happen — and the uncaught `ValueError` becomes a
        fatal error instead.

        **Official reference:** https://www.php.net/manual/en/function.mb-strlen.php

??? question "If the `encoding` argument of an `mb_*` function is omitted or `null`, what is used?"
    Think before revealing the answer.

    ??? success "Show answer"
        The **internal character encoding** — readable and settable with
        `mb_internal_encoding()`. For `mb_convert_encoding()`'s `from_encoding`, the manual is
        more precise: the `mbstring.internal_encoding` setting if set, otherwise
        `default_charset`.

        **Why it matters:** omitting the argument makes your code depend on server INI. Passing
        `'UTF-8'` explicitly makes it depend on nothing, which is why every example in this
        chapter does.

        **Official reference:** https://www.php.net/manual/en/function.mb-internal-encoding.php

??? question "Which mbstring function detects an 'Invalid Encoding Attack' payload?"
    Think before revealing the answer.

    ??? success "Show answer"
        `mb_check_encoding(array|string|null $value, ?string $encoding)` — the manual says
        explicitly that it "is useful to prevent so-called *Invalid Encoding Attack*". Since
        PHP 8.1.0, omitting the value or passing `null` is deprecated.

        **Why it matters:** malformed byte sequences can survive one sanitiser and become
        meaningful in another layer. Validating the encoding at the boundary closes that class
        of bug before escaping is even discussed.

        **Official reference:** https://www.php.net/manual/en/function.mb-check-encoding.php

??? question "Why is there no `mb_strrev()`?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because reversing text is not well defined on Unicode: combining marks and grapheme
        clusters must move together with their base characters, and mbstring works at the
        code-point level. `strrev('café')` reverses *bytes*, turning `c3 a9` into `a9 c3` —
        invalid UTF-8.

        **Why it matters:** the absence of a function is evidence about the model. When a
        multibyte counterpart does not exist, ask what the operation would even mean.

        **Official reference:** https://www.php.net/manual/en/book.mbstring.php

## intl

??? question "What is the `intl` extension a wrapper for, and what does that imply for building it?"
    Think before revealing the answer.

    ??? success "Show answer"
        It wraps the **ICU** library. Building it requires ICU to be installed
        (`--enable-intl`), and the manual records that ICU 50.1 or newer is required as of
        PHP 7.4.0.

        **Why it matters:** the locale data is ICU's, not PHP's — which is why output can differ
        between two servers running the same PHP version but different ICU releases.

        **Official reference:** https://www.php.net/manual/en/intl.installation.php

??? question "Name the intl classes you are most likely to meet in a Symfony application."
    Think before revealing the answer.

    ??? success "Show answer"
        `Collator` (locale-sensitive string comparison), `NumberFormatter` (numbers, currencies,
        percentages, spell-out rules), `IntlDateFormatter` (localised dates/times),
        `MessageFormatter` (ICU MessageFormat), `Locale`, `Normalizer` and `Transliterator`.

        **Why it matters:** these are the concrete deliverables of "the intl extension". Naming
        them turns an abstract requirement into a checklist of features you lose without it.

        **Official reference:** https://www.php.net/manual/en/book.intl.php

??? question "What does `Collator` do that PHP's `sort()` cannot?"
    Think before revealing the answer.

    ??? success "Show answer"
        It sorts by **locale-aware collation rules** (the Unicode Collation Algorithm with ICU
        tailoring) instead of byte value. In German, `sort()` pushes `Äpfel` and `Öl` after
        `Zebra` because `0xC3` > `0x5A`; a `Collator('de_DE')` yields `Apfel, Äpfel, Öl, Zebra`.

        **Why it matters:** "why is Äpfel after Zebra?" is the fastest recognisable symptom of a
        missing collator, in any language with accents.

        **Official reference:** https://www.php.net/manual/en/class.collator.php

??? question "Distinguish the `intl` **extension** from the `symfony/intl` **component**."
    Think before revealing the answer.

    ??? success "Show answer"
        The **extension** is a compiled PHP module wrapping ICU and providing `Collator`,
        `NumberFormatter`, `IntlDateFormatter`, … The **component** is a Composer package
        (`php >= 8.4`, no `ext-*` requirement) that ships ICU **data** — `Languages`,
        `Countries`, `Locales`, `Currencies`, `Timezones` — as PHP arrays.

        **Why it matters:** they have near-identical names and completely different jobs.
        Symfony's `Locale`, `Country` and `Currency` validators need the **component**, not the
        extension.

        **Official reference:** https://symfony.com/doc/8.0/components/intl.html

??? question "Three units of string length, and which function reports each."
    Think before revealing the answer.

    ??? success "Show answer"
        **Bytes** → `strlen()`. **Code points** → `mb_strlen()`. **Grapheme clusters** (what a
        human sees as one character) → `grapheme_strlen()`, which comes from `intl`. A family
        emoji joined by zero-width joiners is 18 bytes, 5 code points, 1 grapheme.

        **Why it matters:** Symfony's String component exposes exactly these three levels as
        `ByteString`, `CodePointString` and `UnicodeString`, so the distinction is a Symfony API
        design question as much as a PHP one.

        **Official reference:** https://www.php.net/manual/en/function.grapheme-strlen.php

## ctype

??? question "What does `ctype_digit('')` return, and why?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`false`**. The manual states the rule for the whole family: "When called with an empty
        string the result will always be `false`."

        **Why it matters:** it defeats the vacuous-truth intuition ("no non-digit, so true") and
        means `ctype_digit()` alone is not a "not empty" test — nor an excuse to skip one.

        **Official reference:** https://www.php.net/manual/en/function.ctype-digit.php

??? question "Why is `ctype_digit(123)` false while `ctype_digit(1234)` is true?"
    Think before revealing the answer.

    ??? success "Show answer"
        An `int` between **-128 and 255 inclusive** is interpreted as an **ASCII character
        code**; any other integer is interpreted as a string containing its decimal digits.
        `123` is inside the window and means `{`; `1234` is outside it and becomes `"1234"`.

        **Why it matters:** two integers, two different rules, no error — the most reliably
        surprising behaviour in the chapter. Casting to `string` removes it entirely.

        **Official reference:** https://www.php.net/manual/en/function.ctype-digit.php

??? question "What changed for `ctype_*` arguments in PHP 8.1.0?"
    Think before revealing the answer.

    ??? success "Show answer"
        Passing a **non-string** argument became **deprecated**. The manual adds that in the
        future the argument will be interpreted as a string rather than an ASCII codepoint, and
        recommends casting to `string` or calling `chr()` when a codepoint really was intended.

        **Why it matters:** the ASCII-codepoint behaviour is explicitly transitional, so code
        relying on it is code with a scheduled expiry date.

        **Official reference:** https://www.php.net/manual/en/function.ctype-digit.php

## iconv, PDO, OPcache

??? question "Compare the argument order of `iconv()` and `mb_convert_encoding()`."
    Think before revealing the answer.

    ??? success "Show answer"
        `iconv(string $from_encoding, string $to_encoding, string $string)` — the string is
        **last**. `mb_convert_encoding(array|string $string, string $to_encoding,
        array|string|null $from_encoding = null)` — the string is **first** and the source
        encoding is optional and last.

        **Why it matters:** identical purpose, mirrored signatures. Memorising which one takes
        the haystack first is worth a whole exam question.

        **Official reference:** https://www.php.net/manual/en/function.mb-convert-encoding.php

??? question "What do `//TRANSLIT` and `//IGNORE` do in an iconv target encoding, and what happens without them?"
    Think before revealing the answer.

    ??? success "Show answer"
        `//TRANSLIT` approximates an unrepresentable character with similar-looking ones;
        `//IGNORE` silently discards it; with neither, an `E_NOTICE` is generated and `iconv()`
        returns **`false`**. The manual warns that `//TRANSLIT`'s behaviour depends on the
        system's iconv implementation and that some implementations ignore it.

        **Why it matters:** it is the structural difference from mbstring — iconv is a binding to
        the host's conversion facility, so the same code can behave differently on Alpine and on
        Debian.

        **Official reference:** https://www.php.net/manual/en/function.iconv.php

??? question "Why does `ext-pdo` alone not let you connect to MySQL?"
    Think before revealing the answer.

    ??? success "Show answer"
        PDO is only the common interface; each database needs its own **driver** extension
        (`pdo_mysql`, `pdo_pgsql`, `pdo_sqlite`, …). `PDO::getAvailableDrivers()` (alias
        `pdo_drivers()`) lists the drivers currently usable in a DSN and returns an empty array
        when there are none. The manual also notes drivers must be loaded **after** PDO itself.

        **Why it matters:** "could not find driver" is a driver problem, never a PDO problem, and
        a preflight check that only tests `ext-pdo` will miss it.

        **Official reference:** https://www.php.net/manual/en/pdo.getavailabledrivers.php

??? question "Which INI directive loads OPcache, and why is it not `extension=`?"
    Think before revealing the answer.

    ??? success "Show answer"
        `zend_extension=` — `zend_extension=/full/path/to/opcache.so` on Unix-like systems,
        `zend_extension=C:\path\to\php_opcache.dll` on Windows. OPcache hooks the **compiler**
        itself, which is what a Zend extension is. The manual also notes that when Xdebug is
        used, OPcache must be loaded first.

        **Why it matters:** `opcache.enable` defaults to `1`, so "enable is on but OPcache is
        off" nearly always means the module was never loaded.

        **Official reference:** https://www.php.net/manual/en/opcache.installation.php

??? question "What exactly does OPcache cache — and what does it *not* cache?"
    Think before revealing the answer.

    ??? success "Show answer"
        It caches **compiled bytecode (opcodes) in shared memory**, so requests skip lexing,
        parsing and compiling. It does **not** cache query results, HTTP responses, or your
        application's data — those belong to APCu/Redis, a reverse proxy, and the Symfony Cache
        component respectively.

        **Why it matters:** "it's a cache" is where the confusion starts. Naming the layer
        prevents the classic wrong answer on both the exam and in production tuning.

        **Official reference:** https://symfony.com/doc/8.0/performance.html#performance-use-opcache

??? question "What are the defaults of `opcache.validate_timestamps` and `opcache.revalidate_freq`, and how do they interact?"
    Think before revealing the answer.

    ??? success "Show answer"
        `opcache.validate_timestamps=1` and `opcache.revalidate_freq=2` (seconds) by default,
        both `INI_ALL`. When `validate_timestamps` is **disabled**, `revalidate_freq` is
        **ignored** entirely and OPcache must be reset manually via `opcache_reset()`,
        `opcache_invalidate()` or a web server restart.

        **Why it matters:** the interaction is the exam-grade detail. "Wait a couple of seconds
        and it picks up the change" is true only while `validate_timestamps` is on.

        **Official reference:** https://www.php.net/manual/en/opcache.configuration.php#ini.opcache.validate-timestamps

??? question "Why can't you clear the web server's OPcache from your terminal?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because the CLI and the web (PHP-FPM/mod_php) processes do not share an OPcache — the
        Symfony performance page says so explicitly. The documented options are: restart the web
        server, call `opcache_reset()` *through* the web server, or use a tool such as
        `cachetool` that talks to the FPM socket.

        **Why it matters:** it is the operational half of `validate_timestamps=0`. Choosing that
        setting without automating the reset is how a green deploy serves week-old code.

        **Official reference:** https://symfony.com/doc/8.0/performance.html#performance-dont-check-timestamps

??? question "What does OPcache preloading make globally available — and what does it deliberately skip?"
    Think before revealing the answer.

    ??? success "Show answer"
        Functions, classes, interfaces and traits declared by the preloaded files become
        available to every request without being included — but **not constants**. Preloaded
        scripts can only be cleared by restarting the PHP process, and preloading is **not
        supported on Windows**.

        **Why it matters:** the "not constants" exception is exactly the kind of detail a trap
        question is built on, and the restart requirement is why preloading is a production-only
        feature.

        **Official reference:** https://www.php.net/manual/en/opcache.preloading.php

??? question "In a Symfony 8 project, which file does `opcache.preload` point at, and which tags control its contents?"
    Think before revealing the answer.

    ??? success "Show answer"
        `config/preload.php`, created by the Symfony Flex recipe for
        `symfony/framework-bundle`. The `container.preload` and `container.no_preload` service
        tags decide which classes are included.

        **Why it matters:** it turns a PHP engine feature into a Symfony configuration question,
        which is exactly how the certification likes to frame it.

        **Official reference:** https://symfony.com/doc/8.0/performance.html#performance-use-preloading

??? question "Why does Symfony recommend raising `opcache.interned_strings_buffer`?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because Symfony applications use a very large number of fully-qualified class names, and
        the default of 8 MB is too low; the documentation recommends `32`. It also recommends
        `opcache.memory_consumption=256` and `opcache.max_accelerated_files=32531` (the PHP
        default for the latter is 10000).

        **Why it matters:** it is the only OPcache setting whose recommended value is justified
        by a *framework* characteristic rather than a generic one — FQCNs are long and repeat
        endlessly in a compiled container.

        **Official reference:** https://symfony.com/doc/8.0/performance.html#performance-configure-opcache

## Symfony, polyfills and requirements

??? question "Which extensions does the Symfony 8.0 documentation list as technical requirements?"
    Think before revealing the answer.

    ??? success "Show answer"
        PHP 8.4 or higher plus **Ctype, iconv, PCRE, Session, SimpleXML and Tokenizer** — noted
        as installed and enabled by default in most PHP 8 installations. `symfony
        check:requirements` verifies them.

        **Why it matters:** neither `mbstring` nor `intl` is on that list, which contradicts the
        common assumption. They are strongly recommended, not required, because polyfills cover
        the gap.

        **Official reference:** https://symfony.com/doc/8.0/setup.html#symfony-tech-requirements

??? question "Which `ext-*` requirement does the `symfony/symfony` monorepo actually declare?"
    Think before revealing the answer.

    ??? success "Show answer"
        Only **`ext-xml`**. Everything else in the multibyte/locale space is covered by
        dependencies on `symfony/polyfill-ctype`, `symfony/polyfill-mbstring`,
        `symfony/polyfill-intl-icu`, `-intl-grapheme`, `-intl-idn` and `-intl-normalizer`.

        **Why it matters:** it is the concrete proof that Symfony's strategy is *polyfill first,
        extension for performance* — not *hard platform requirement*.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/composer.json

??? question "What does `symfony/polyfill-intl-icu` provide, and what is its hard limitation?"
    Think before revealing the answer.

    ??? success "Show answer"
        Fallback implementations of `Collator`, `NumberFormatter`, `Locale`, `IntlDateFormatter`,
        `IntlListFormatter` and the `intl_*` error functions — **limited to the `en` locale**.

        **Why it matters:** it is the exact boundary between "works" and "works correctly". The
        Symfony translation page states you must install the native `intl` extension when
        translating into locales other than English.

        **Official reference:** https://symfony.com/doc/8.0/translation.html

??? question "Which extension does `symfony/polyfill-mbstring` itself require?"
    Think before revealing the answer.

    ??? success "Show answer"
        **`ext-iconv`**. Its `composer.json` requires `php >= 7.2` and `ext-iconv`, provides
        `ext-mbstring`, and *suggests* `ext-mbstring` "For best performance".

        **Why it matters:** it explains an otherwise odd asymmetry — `iconv` is on Symfony's
        required list while `mbstring` is not, because the mbstring fallback is built on iconv.

        **Official reference:** https://symfony.com/doc/8.0/setup.html#symfony-tech-requirements

??? question "Without `ext-intl`, what does `Symfony\Component\String\AbstractUnicodeString::ascii()` do?"
    Think before revealing the answer.

    ??? success "Show answer"
        It degrades instead of crashing. It only appends the ICU `any-latin/bgn` rule when
        `function_exists('transliterator_transliterate')`, then falls back to
        `iconv('UTF-8', 'ASCII//TRANSLIT', …)` per character — throwing a `LogicException` that
        recommends installing `gnu-libiconv` on Alpine — and finally replaces remaining
        non-ASCII characters with `?`.

        **Why it matters:** it is the canonical example of "missing extension ⇒ degraded output,
        not an exception", which is the harder failure mode to notice in production.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/String/AbstractUnicodeString.php

??? question "Which Symfony console command reports OPcache status, the Intl locale and the PHP version?"
    Think before revealing the answer.

    ??? success "Show answer"
        `php bin/console about`. Its PHP section prints Version, Architecture, Intl locale
        (guarded by `class_exists(\Locale::class, false)`), Timezone, OPcache (via
        `extension_loaded('Zend OPcache')` plus `ini_get('opcache.enable')`) and APCu.

        **Why it matters:** it is a first-party, always-available diagnostic — and its source is
        the definitive answer to "what name does Symfony use to detect OPcache?".

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Command/AboutCommand.php

## Memory hooks

??? question "One sentence to remember `strlen` versus `mb_strlen`."
    Think before revealing the answer.

    ??? success "Show answer"
        **`mb` means "multi-byte aware"; the plain function is not.** `strlen` measures the
        *box*, `mb_strlen` counts the *letters*.

        **Why it matters:** it compresses the most examined fact of the chapter into one image,
        and it generalises: every `mb_` twin counts characters where its plain sibling counts
        bytes.

        **Official reference:** https://www.php.net/manual/en/book.mbstring.php

??? question "One sentence to remember what `ext-*` in `composer.json` really guarantees."
    Think before revealing the answer.

    ??? success "Show answer"
        **`ext-*` is a bouncer, not a supplier — and the bouncer can be talked round.** It
        blocks the install, it never installs anything, and `provide`, `--ignore-platform-req`
        or `config.platform` will each get you past it.

        **Why it matters:** it settles, in one image, both halves of the Composer questions: what
        the requirement does, and why a green install is not proof.

        **Official reference:** https://getcomposer.org/doc/articles/composer-platform-dependencies.md

??? question "One sentence to remember the OPcache deployment rule."
    Think before revealing the answer.

    ??? success "Show answer"
        **Turn off the stat, take over the reset.** `opcache.validate_timestamps=0` buys speed by
        making OPcache stop looking at your files, so every deploy must end with an explicit
        reset — and a process restart if you preload.

        **Why it matters:** it links the setting to the operational duty it creates, which is
        exactly the pairing a scenario question tests.

        **Official reference:** https://symfony.com/doc/8.0/performance.html#performance-dont-check-timestamps

---

<small>Back to the lesson: [PHP Extensions](extensions.md) ·
[Retake the topic exam](extensions-exam.md) · Continue to the next topic: [SPL](spl.md)</small>

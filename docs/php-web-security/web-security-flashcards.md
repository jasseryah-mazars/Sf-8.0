# Flashcards — Web Security Fundamentals

!!! abstract "How to use this page"
    One idea per card. Read the prompt, answer it **out loud or in your head**, then reveal.
    Revealing before committing to an answer turns active recall into passive reading and
    costs you most of the benefit. Mark what you miss and cycle those cards again tomorrow.

    Theory: **[Web Security Fundamentals](web-security.md)** ·
    Practice: **[Guided exercises](web-security-exercises.md)** ·
    Test: **[Topic exam](web-security-exam.md)**

## The threat-to-defence map

??? question "State the six core threat/defence pairs of this chapter in one line each."
    Think before revealing the answer.

    ??? success "Show answer"
        XSS → context-aware output escaping (Twig autoescaping).
        CSRF → unpredictable token validated server-side, plus `SameSite`.
        SQL injection → prepared statements with bound parameters.
        Session fixation → new session id at authentication.
        Session hijacking → `HttpOnly`, `Secure`, HTTPS.
        Clickjacking → CSP `frame-ancestors` / `X-Frame-Options`.

        **Why it matters:** the exam asks "which mechanism defends against X". Every
        question in this topic is a lookup in this table plus one detail. Learn the table
        first and the details attach to something.

        **Official reference:** https://symfony.com/doc/8.0/security.html

??? question "Which of this chapter's defences are on by default in a Symfony 8.0 app, and which are not?"
    Think before revealing the answer.

    ??? success "Show answer"
        **On by default:** Twig output escaping, CSRF tokens in Form-component forms,
        prepared statements through Doctrine/DBAL, session-id migration on login
        (`session_fixation_strategy: MIGRATE`), `cookie_httponly: true`,
        `cookie_samesite: 'lax'`, `session.use_strict_mode = 1`, `allow_extra_fields: false`.

        **Not on by default:** every security header (CSP, HSTS, `X-Frame-Options`,
        `nosniff`, `Referrer-Policy`, `Permissions-Policy`), HTTPS enforcement,
        redirect-target validation, timing-safe comparison in your own code, upload storage
        outside the web root.

        **Why it matters:** this split is the highest-yield fact in the chapter. Most
        "which of these does Symfony do for you" questions are answered by it.

        **Official reference:** https://symfony.com/doc/8.0/security.html

## XSS and escaping

??? question "Name the three XSS variants and what distinguishes them."
    Think before revealing the answer.

    ??? success "Show answer"
        **Reflected:** the payload arrives in the request and is echoed back in that same
        response. **Stored:** the payload is persisted (comment, profile, filename) and
        served to every later visitor. **DOM-based:** the payload never has to reach the
        server — client-side JavaScript reads it from `location`, `document.referrer` or
        similar and writes it into a dangerous sink.

        **Why it matters:** only the first two are fixed by server-side output escaping. A
        DOM XSS lives entirely in the browser, so a perfectly escaped Twig template does not
        protect you if your JavaScript assigns to `innerHTML`.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html

??? question "How does Twig decide which escaping strategy to use in a Symfony app?"
    Think before revealing the answer.

    ??? success "Show answer"
        TwigBundle sets `autoescape` to the `'name'` strategy, which calls
        `Twig\FileExtensionEscapingStrategy::guess()` on the template name **at compile
        time**: `js` for `.js.twig` and `.json.twig`, `css` for `.css.twig`, **`false`
        (no escaping) for `.txt.twig`**, and `html` for everything else.

        **Why it matters:** it is per *template*, not per element — Twig never parses your
        HTML. And it explains the `.txt.twig` blind spot, which is a real source of stored
        XSS when a plain-text template is reused in an HTML context.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/twig.html#config-twig-autoescape

??? question "List the escaping strategies Twig's `escape` filter supports for HTML documents, and the context each targets."
    Think before revealing the answer.

    ??? success "Show answer"
        `html` — the HTML body, or attribute values **inside quotes**.
        `js` — JavaScript and JSON strings, using backslash escape sequences.
        `css` — any string inserted into CSS; escapes everything except alphanumerics.
        `url` — a URI **subcomponent**, never a whole URI.
        `html_attr` — an attribute **name**, or an attribute value **without quotes**.
        `html_attr_relaxed` — as `html_attr`, but leaves `@`, `:`, `[`, `]` alone for
        front-end frameworks.

        **Why it matters:** this is the documented list, and "which strategy for which
        context" is directly examinable. The recommended pattern is to quote your attributes
        and use `html`, because `html_attr` is documented as less performant.

        **Official reference:** https://twig.symfony.com/doc/3.x/filters/escape.html

??? question "What exactly does `|raw` do, and what does it *not* do?"
    Think before revealing the answer.

    ??? success "Show answer"
        It **disables** output escaping for that one expression. It performs **no**
        sanitising, filtering or tag-stripping of any kind — it is the absence of a
        transformation.

        **Why it matters:** "`raw` cleans the value" is the belief that turns a template
        into an XSS. `raw` is only correct on markup your own code produced or that a real
        HTML sanitiser has already vetted.

        **Official reference:** https://symfony.com/doc/8.0/templates.html#output-escaping

??? question "Which five characters does Twig's `html` strategy transform?"
    Think before revealing the answer.

    ??? success "Show answer"
        `<`, `>`, `&`, `"` and `'` — that is it. The strategy is one
        `htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, $charset)` call. Backslash,
        slash, space, parentheses, semicolon, equals and backtick all pass through
        untouched.

        **Why it matters:** it makes "HTML escaping is not JavaScript escaping" concrete
        rather than a slogan. Those seven surviving characters are precisely the ones a
        JavaScript or CSS parser cares about.

        **Official reference:** https://www.php.net/manual/en/function.htmlspecialchars.php

??? question "Why is HTML escaping insufficient inside `onclick=\"doIt('{{ x }}')\"`?"
    Think before revealing the answer.

    ??? success "Show answer"
        Two parsers run in sequence. The HTML parser decodes entities in the attribute value
        **first**, so the `&#039;` produced by `html` escaping becomes a live `'` before the
        JavaScript parser ever sees it, and the payload closes the string. `js` escaping
        survives because it emits backslash escapes, not entities.

        **Why it matters:** OWASP lists this exact shape as an unsafe quoted JavaScript data
        value. The durable fix is to stop nesting contexts: put the value in a `data-`
        attribute and read it from a real `.js` file.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

??? question "Why is escaping on the way *into* the database an anti-pattern?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because the correct transformation depends on the *destination* language, which is
        unknown at write time. A value HTML-escaped at insert arrives double-escaped in the
        next HTML render, corrupted in a JSON API, a CSV export or an e-mail — and is still
        unsafe inside a `<script>`, a URL or a CSS property.

        **Why it matters:** it separates two controls that get conflated. Validation decides
        whether a value is *acceptable*; escaping decides how it is *represented* in one
        output language, at the moment of output.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

## SQL injection

??? question "Why does binding a parameter stop injection when escaping quotes does not?"
    Think before revealing the answer.

    ??? success "Show answer"
        `prepare()` sends the statement text to the driver to be parsed **before** any value
        is attached, so the parse tree is fixed. A bound value can only occupy the leaf its
        placeholder marked; it can never add a node. Escaping is a blocklist that must be
        right about the character set, about numeric contexts where no quotes exist at all,
        and about identifiers that cannot be quoted.

        **Why it matters:** it turns "use prepared statements" from a rule you memorised
        into a mechanism you can explain, which is what the code-analysis questions require.

        **Official reference:** https://www.php.net/manual/en/pdo.prepare.php

??? question "Is Doctrine DQL automatically safe from injection?"
    Think before revealing the answer.

    ??? success "Show answer"
        No. DQL is safe when values arrive through `setParameter()`; it is injectable when
        you concatenate them into the DQL string, because DQL is *parsed* as a string before
        being compiled to SQL. `->where("p.name = '".$name."'")` is a classic injection with
        extra steps.

        **Why it matters:** "it is an ORM, therefore it is safe" is the exam's favourite
        false premise. The safety comes from parameter binding, not from the query language.

        **Official reference:** https://symfony.com/doc/8.0/doctrine.html#doctrine-queries

??? question "What can never be bound as a parameter, and what do you do instead?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Identifiers** — table names, column names, sort columns, `ASC`/`DESC` — cannot be
        parameterised, because they are part of the statement's structure rather than its
        data. The only safe source for them is a hard-coded allow-list in your own code,
        keyed by the request value.

        **Why it matters:** it is the one place where "just bind it" does not apply, and it
        is where dynamic-sorting features quietly reintroduce injection.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

## CSRF

??? question "In one sentence: what is CSRF, and what does the attacker exploit?"
    Think before revealing the answer.

    ??? success "Show answer"
        A malicious site causes the victim's browser to issue a state-changing request to
        your application; the attack "is based on the trust that a web application has in a
        user's browser (e.g. on session cookies)". The attacker never reads the response —
        they only need the side effect.

        **Why it matters:** it explains why a token works. The attacker can make the browser
        *send* a request with its cookies, but cannot *read* a value out of your pages to
        put in it.

        **Official reference:** https://symfony.com/doc/8.0/security/csrf.html

??? question "Stateful vs stateless CSRF tokens in Symfony 8.0 — how does each one validate?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Stateful** (the default): the secret lives in the session's token storage and the
        submitted value is compared against it. **Stateless**: no session; Symfony checks
        the request's `Origin` and `Referer` headers against the application's own origin,
        with an optional cookie/header "double-submit" as defence in depth.

        **Why it matters:** stateful tokens force a session to start as soon as a protected
        form renders, which blocks full-page HTTP caching. Stateless tokens exist precisely
        to lift that constraint, and are enabled by default in Flex applications for the
        `submit`, `authenticate` and `logout` IDs.

        **Official reference:** https://symfony.com/doc/8.0/security/csrf.html#csrf-stateless-tokens

??? question "Why does the rendered CSRF token value change on every render?"
    Think before revealing the answer.

    ??? success "Show answer"
        `CsrfTokenManager::getToken()` XOR-masks the stable stored secret with 32 fresh
        random bytes and emits `prefix.key.maskedValue`; `isTokenValid()` de-randomises and
        compares with `hash_equals()`. The documented reason is BREACH and CRIME —
        compression side-channel attacks that need repeated ciphertext to work.

        **Why it matters:** it is the answer to "Symfony regenerates my token, is that a
        bug?" (no) and to "can I assert on the token string in a test?" (no — you would be
        asserting on the mask).

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Csrf/CsrfTokenManager.php

??? question "Why is `SameSite=Lax` alone not enough against CSRF?"
    Think before revealing the answer.

    ??? success "Show answer"
        `lax` still sends the cookie when "the user consciously made the request (by
        clicking a link or submitting a form with the `GET` method)". Any state-changing
        `GET` endpoint therefore stays exploitable. `SameSite` is also enforced by the
        browser, so it is a hardening layer rather than a server-side guarantee.

        **Why it matters:** the two mitigations are complementary and the exam tests whether
        you treat them as interchangeable. Tokens are the control; `SameSite` narrows the
        window.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#config-framework-session

??? question "Do Symfony forms need any code to be CSRF-protected? And hand-written HTML forms?"
    Think before revealing the answer.

    ??? success "Show answer"
        Form-component forms: **no code at all** — "Symfony Forms include CSRF tokens by
        default and Symfony also checks them automatically for you", in a hidden field named
        `_token`. Hand-written forms: yes — render `{{ csrf_token('some-id') }}` and verify
        with `isCsrfTokenValid('some-id', $submitted)` or the `#[IsCsrfTokenValid]`
        attribute.

        **Why it matters:** the two halves are examined separately, and the manual API is
        also what the login and logout flows use (`enable_csrf: true`, field `_csrf_token`,
        token ID `authenticate`).

        **Official reference:** https://symfony.com/doc/8.0/security/csrf.html#csrf-protection-forms

??? question "What does the `methods` parameter of `#[IsCsrfTokenValid]` do when the request uses another method?"
    Think before revealing the answer.

    ??? success "Show answer"
        The attribute is **ignored** — no CSRF validation occurs and the action runs
        normally. It is a filter on when to check, never a restriction on which methods are
        allowed.

        **Why it matters:** it looks like a guard and behaves like an opt-out. Pair it with
        a route that already restricts the method, or you have written a check that a `POST`
        simply walks past.

        **Official reference:** https://symfony.com/doc/8.0/security/csrf.html#csrf-controller-attributes

??? question "Why must CSRF protection never rely on the `Referer` header or a hidden non-random field?"
    Think before revealing the answer.

    ??? success "Show answer"
        `Referer` is frequently absent (privacy settings, `Referrer-Policy`, HTTPS→HTTP
        transitions), so a check that has to accept the empty case is trivially bypassed. A
        hidden field whose value the attacker can predict or read is not a secret at all —
        the whole point of a token is unpredictability held server-side.

        **Why it matters:** it is the classic "we already have protection" answer. Note that
        Symfony's *stateless* CSRF does use `Origin`/`Referer` — but as a same-origin proof
        combined with a token, not as a standalone defence.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html

## Sessions

??? question "Session fixation vs session hijacking — what is the difference?"
    Think before revealing the answer.

    ??? success "Show answer"
        **Fixation:** the attacker makes the victim use an id the attacker already knows,
        *before* login. **Hijacking:** the attacker obtains an id the victim already has,
        *after* login. Fixation is defeated by regenerating the id at authentication;
        hijacking by keeping the cookie unreadable (`HttpOnly`) and unsniffable
        (`Secure` + HTTPS).

        **Why it matters:** two attacks with the same symptom and completely different
        countermeasures. Questions test whether you can pick the right one.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

??? question "What is the default `session_fixation_strategy`, and what are the three values?"
    Think before revealing the answer.

    ??? success "Show answer"
        Default: `SessionAuthenticationStrategy::MIGRATE`. The three values are `NONE` (no
        change — documented as "not recommended"), `MIGRATE` (new id, attributes kept) and
        `INVALIDATE` (new id, all attributes lost).

        **Why it matters:** it is the reason a Symfony app resists fixation with zero
        configuration, and the default value is a straight recall question.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/security.html#session-fixation-strategy

??? question "What does `SessionAuthenticationStrategy::MIGRATE` do beyond changing the id?"
    Think before revealing the answer.

    ??? success "Show answer"
        It calls `$request->getSession()->migrate(true)` — the `true` **destroys** the old
        server-side record rather than orphaning it — and then clears the CSRF token storage
        when one is available, so tokens minted before login cannot be replayed after it.

        **Why it matters:** the `true` is the difference between closing the fixation window
        and leaving a valid stale record on disk for `gc_maxlifetime` seconds.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Session/SessionAuthenticationStrategy.php

??? question "`migrate()` vs `migrate(true)` vs `invalidate()` — what is the difference?"
    Think before revealing the answer.

    ??? success "Show answer"
        `migrate()` — new id, attributes kept, **old record left on disk**.
        `migrate(true)` — new id, attributes kept, old record deleted.
        `invalidate()` — literally `clear()` followed by `migrate(true)`: new id, attributes
        gone, old record deleted.

        **Why it matters:** three near-identical calls with materially different security
        outcomes, all reachable from your own code. The default argument is the unsafe one.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Session/Session.php

??? question "What are the documented defaults for `cookie_httponly`, `cookie_samesite` and `cookie_secure`?"
    Think before revealing the answer.

    ??? success "Show answer"
        `cookie_httponly`: **`true`**. `cookie_samesite`: **`'lax'`**. `cookie_secure`: **no
        default** — type "boolean or `'auto'`"; if unset, PHP's `session.cookie_secure`
        applies. `'auto'` means `true` for HTTPS requests and `false` for HTTP ones.

        **Why it matters:** the odd one out is `cookie_secure`, and assuming it defaults to
        `true` is exactly the mistake that ships a session cookie over plain HTTP.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#config-framework-session

??? question "`session.use_strict_mode`: PHP's default, Symfony's value, and what it prevents."
    Think before revealing the answer.

    ??? success "Show answer"
        PHP defaults it to **`0`** and the manual calls enabling it "mandatory for general
        session security". `NativeSessionStorage` merges `'use_strict_mode' => 1` into its
        options, so a standard Symfony app runs with it **on**. With it on, PHP refuses an
        uninitialised session id and issues a new one instead of *adopting* the id the
        browser sent — the session-adoption flavour of fixation.

        **Why it matters:** a two-value question where the framework and the language
        disagree, which is precisely the shape the exam likes. Caveat: a custom save handler
        that does not implement `validateId()` disables strict mode in practice.

        **Official reference:** https://www.php.net/manual/en/session.configuration.php#ini.session.use-strict-mode

??? question "`HttpOnly` vs `Secure` — which threat does each address?"
    Think before revealing the answer.

    ??? success "Show answer"
        `HttpOnly` hides the cookie from `document.cookie`, so an XSS payload cannot read
        and exfiltrate it. `Secure` tells the browser to send the cookie only over TLS, so a
        network attacker cannot capture it in transit. Different adversaries, different
        channels.

        **Why it matters:** swapping the two is the single most common mistake on this
        topic, and both appear in almost every session-security question.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#config-framework-session

## Headers, HTTPS and clickjacking

??? question "Which two headers stop clickjacking, and which one should you prefer?"
    Think before revealing the answer.

    ??? success "Show answer"
        `Content-Security-Policy: frame-ancestors …` and `X-Frame-Options`. Prefer
        `frame-ancestors`: OWASP states that CSP `frame-ancestors` "obsoletes
        X-Frame-Options for supporting browsers", and it can list several allowed origins,
        which `X-Frame-Options` cannot.

        **Why it matters:** `X-Frame-Options: ALLOW-FROM` is "an obsolete directive that no
        longer works in modern browsers" — relying on it can leave you with no clickjacking
        defence at all. Neither control works from a `<meta>` tag.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html

??? question "What does `X-Content-Type-Options: nosniff` actually prevent?"
    Think before revealing the answer.

    ??? success "Show answer"
        It tells the browser to obey the declared `Content-Type` instead of guessing from
        the bytes. That blocks MIME sniffing, "which can transform non-executable MIME types
        into executable MIME types" — a user-uploaded file served with the wrong
        `Content-Type` being run as a script.

        **Why it matters:** it is the header people misfile under "XSS protection" or
        "clickjacking". It pairs with uploads: `nosniff` plus a correct `Content-Type` plus
        storage outside the web root.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html

??? question "What does `Referrer-Policy` control, and what is OWASP's recommended value?"
    Think before revealing the answer.

    ??? success "Show answer"
        How much of the current URL is placed in the `Referer` header of outgoing requests.
        The recommended value is `strict-origin-when-cross-origin`: full URL to the same
        origin, origin only to other origins, and nothing at all when downgrading to HTTP.

        **Why it matters:** URLs leak — password-reset tokens, search terms, internal IDs —
        to every third-party image, font and analytics endpoint on the page. It is also the
        reason a `Referer`-based CSRF check is unreliable.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html

??? question "What is `Permissions-Policy` for?"
    Think before revealing the answer.

    ??? success "Show answer"
        It controls which origins may use which browser features, in the top-level page and
        in embedded frames — for example `Permissions-Policy: geolocation=(), camera=(),
        microphone=()`. OWASP frames it as limiting the blast radius of an injection: "this
        prevents that an injection, for example an XSS, enables the camera, the microphone,
        or other browser feature".

        **Why it matters:** it is the defence-in-depth header people forget exists, and its
        job — capability reduction, not injection prevention — is what makes it a clean
        distractor in header questions.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html

??? question "Why can HSTS not protect the first request to a domain?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because it is a *response* header: the policy only applies "once a supported browser
        receives this header". Before that first successful response there is nothing to
        enforce. The documented remedy is the HSTS preload list, which ships the policy
        inside the browser.

        **Why it matters:** it is the standard true/false trap. Two companions: omitting
        `includeSubDomains` "permits a broad range of cookie-related attacks", and sending
        `preload` "can have PERMANENT CONSEQUENCES".

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html

??? question "Which Symfony option redirects an `http` request to `https`, and what does it need to work behind a proxy?"
    Think before revealing the answer.

    ??? success "Show answer"
        `requires_channel: https` on a matching `access_control` entry: "if the incoming
        request's channel (e.g. `http`) does not match this value (e.g. `https`), the user
        will be redirected". Behind a TLS-terminating proxy it needs `trusted_proxies`
        configured, otherwise `Request::isSecure()` reports every request as plain HTTP.

        **Why it matters:** the two halves are usually examined separately, and the proxy
        half also decides whether `cookie_secure: auto` sets the `Secure` flag at all.

        **Official reference:** https://symfony.com/doc/8.0/security/access_control.html#forcing-a-channel-http-https

## Passwords

??? question "What does `password_hash()` embed in its output, and what follows from that?"
    Think before revealing the answer.

    ??? success "Show answer"
        "The used algorithm, cost and salt are returned as part of the hash", so
        `password_verify()` needs no separate storage for any of them. You never generate,
        store or supply a salt yourself.

        **Why it matters:** it kills the "where do I store the salt?" question and explains
        why one column holds everything. It is also why `password_needs_rehash()` can decide
        anything at all — it reads the parameters back out of the hash.

        **Official reference:** https://www.php.net/manual/en/function.password-hash.php

??? question "What happens to the `salt` option of `password_hash()` on PHP 8.4?"
    Think before revealing the answer.

    ??? success "Show answer"
        It is **ignored**. The option is deprecated and, "as of PHP 8.0.0, an explicitly
        given salt is ignored". A random salt is always generated per call.

        **Why it matters:** legacy code that passes a salt is not merely unnecessary, it is
        inert — and reading it can convince a reviewer that a custom salt is still in play
        when it is not.

        **Official reference:** https://www.php.net/manual/en/function.password-hash.php

??? question "Three numbers: bcrypt's input limit, PHP 8.4's default bcrypt cost, Symfony's default cost."
    Think before revealing the answer.

    ??? success "Show answer"
        **72 bytes** — bcrypt truncates the password there.
        **12** — PHP 8.4 raised `PASSWORD_BCRYPT`'s default cost from 10 to 12.
        **13** — `NativePasswordHasher`'s own default cost.

        Add a fourth if you can: **4096 bytes**, `PasswordHasherInterface::MAX_PASSWORD_LENGTH`.

        **Why it matters:** each increment of the cost doubles the hashing time, the valid
        range is 4–31, and 4 is the documented value for the `test` environment.

        **Official reference:** https://symfony.com/doc/8.0/security/passwords.html#reference-security-encoder-bcrypt

??? question "How does Symfony stop bcrypt from silently ignoring bytes 73 and beyond?"
    Think before revealing the answer.

    ??? success "Show answer"
        `NativePasswordHasher::hash()` detects a bcrypt algorithm with an input longer than
        72 bytes (or containing a NUL) and replaces it with
        `base64_encode(hash('sha512', $plainPassword, true))` before calling
        `password_hash()`. `verify()` applies the same transformation, so every byte of a
        long passphrase contributes entropy.

        **Why it matters:** without it, two passphrases that share their first 72 bytes are
        interchangeable — demonstrable in three lines of PHP, and a real risk now that
        passphrase managers are common.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/PasswordHasher/Hasher/NativePasswordHasher.php

??? question "What does `algorithm: 'auto'` actually build, and which hasher writes new hashes?"
    Think before revealing the answer.

    ??? success "Show answer"
        `PasswordHasherFactory` builds a `MigratingPasswordHasher` over the chain
        `['native', 'sodium', 'pbkdf2']` (or `['native', 'pbkdf2']` without libsodium).
        `MigratingPasswordHasher::hash()` delegates to the **first** hasher only, so new
        hashes are written by `NativePasswordHasher` — bcrypt. The reference confirms it:
        "auto" "automatically selects the best available hasher (currently Bcrypt)".

        **Why it matters:** "auto means argon2id" is the plausible wrong answer. The other
        hashers in the chain exist for verification and migration, and the selection may
        legitimately change in a future release — which is why `needsRehash()` exists.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/PasswordHasher/Hasher/PasswordHasherFactory.php

??? question "Where does a rehash happen, and which interface stores the result?"
    Think before revealing the answer.

    ??? success "Show answer"
        "Upon successful login, the Security system checks whether a better algorithm is
        available"; if so it rehashes the plaintext it has just verified and hands the
        result to your implementation of
        `Symfony\Component\Security\Core\User\PasswordUpgraderInterface::upgradePassword()`
        — on the `UserRepository` for the entity provider, or on a custom user provider.

        **Why it matters:** login is the only moment the plaintext exists, so migration is
        necessarily gradual. Skip the interface and the check still runs, the new hash is
        computed, and it is thrown away — a migration that never completes and never warns.

        **Official reference:** https://symfony.com/doc/8.0/security/passwords.html#security-password-migration

??? question "What is `migrate_from` for, and which hashers enable migration automatically?"
    Think before revealing the answer.

    ??? success "Show answer"
        It lists legacy hasher configurations the new hasher must still be able to *verify*,
        so existing users can log in while their hashes are upgraded. The docs note that the
        `auto`, `native`, `bcrypt` and `argon` hashers already enable migration from PBKDF2
        and message-digest hashes automatically.

        **Why it matters:** the rename-then-add pattern (keep the old hasher, rename it,
        point `migrate_from` at it) is the examinable shape, and dropping the old hasher
        instead locks out every account that has not logged in yet.

        **Official reference:** https://symfony.com/doc/8.0/security/passwords.html#security-password-migration

## Redirects, uploads, mass assignment, timing

??? question "What makes a redirect an *open* redirect, and what is the robust fix?"
    Think before revealing the answer.

    ??? success "Show answer"
        Redirecting to a URL taken from untrusted input. "Because the server name in the
        modified link is identical to the original site, phishing attempts may have a more
        trustworthy appearance." The robust fix is never to accept a URL: take a route name
        or a bare path and build the URL yourself with `redirectToRoute()`/`generateUrl()`,
        or validate the host against an allow-list.

        **Why it matters:** it is the threat with no framework default. `redirect()` sends
        whatever string it is given.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html

??? question "Which two redirect targets look local but are not?"
    Think before revealing the answer.

    ??? success "Show answer"
        `//evil.example` — a protocol-relative URL: the browser keeps your scheme and
        changes the host. And `/\evil.example` — some browsers normalise the backslash into
        a slash, producing the same thing. Both begin with `/`, so a naive
        `str_starts_with($target, '/')` check accepts them.

        **Why it matters:** it is the concrete failure of the most common home-made guard.
        Reject a second leading slash, any backslash and any `:`.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html

??? question "What is mass assignment, and what does Symfony's Form component do about it?"
    Think before revealing the answer.

    ??? success "Show answer"
        Mass assignment is binding request fields the developer never meant to expose — the
        classic `roles[]=ROLE_ADMIN` appended to a profile form. `FormType`'s
        `allow_extra_fields` defaults to **`false`**, so a submitted field the form does not
        declare raises "This form should not contain extra fields."

        **Why it matters:** the protection is a default you can switch off, and switching it
        off is the whole vulnerability. The residual risk is a field you *did* declare —
        keep sensitive properties out of the form type, or mark them `mapped: false`.

        **Official reference:** https://symfony.com/doc/8.0/reference/forms/types/form.html#form-option-allow-extra-fields

??? question "Which pieces of an uploaded file must you never trust, and what do you use instead?"
    Think before revealing the answer.

    ??? success "Show answer"
        The client-supplied name, path, extension and size — `getClientOriginalName()`,
        `getClientOriginalPath()`, `getClientOriginalExtension()`, `getSize()` — are
        documented as "not safe because a malicious user could tamper with that
        information". Generate a new name (slug plus a unique suffix) and derive the
        extension from the detected media type with `guessExtension()`.

        **Why it matters:** the name is the attack. It carries the executable extension and
        any `../` traversal. Complete the defence by storing outside the web root and
        validating with the `File` constraint.

        **Official reference:** https://symfony.com/doc/8.0/controller/upload_file.html

??? question "Why does the `File` constraint's documentation prefer `extensions` over `mimeTypes`?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because `extensions` checks the extension **and** the associated media type
        together. Using `mimeTypes` alone means you are not verifying "that the extension of
        the file is consistent with its content (this can be a security issue)".

        **Why it matters:** it is the difference between "this file claims to be a PDF" and
        "this file is a PDF and is named like one" — which is exactly the gap a
        `invoice.pdf.php` upload exploits.

        **Official reference:** https://symfony.com/doc/8.0/reference/constraints/File.html#reference-constraints-file-mime-types

??? question "What is a timing attack, and what is the correct argument order for `hash_equals()`?"
    Think before revealing the answer.

    ??? success "Show answer"
        A regular `===` comparison "will take more or less time to execute depending on
        whether the two values are different or not and at which position the first
        difference can be found, thus leaking information about the contents of the secret".
        The signature is `hash_equals($known_string, $user_string)` — the manual insists on
        providing "the user-supplied string as the **second** parameter, rather than the
        first".

        **Why it matters:** the argument order is examinable and easy to get backwards.
        Symfony follows the same rule in `CsrfTokenManager::isTokenValid()`.

        **Official reference:** https://www.php.net/manual/en/function.hash-equals.php

??? question "Why is `password_verify()` already timing-safe, unlike a manual hash comparison?"
    Think before revealing the answer.

    ??? success "Show answer"
        Because it performs the comparison internally in constant time rather than returning
        a hash for you to compare with `===`. If you ever find yourself writing
        `if ($storedHash === hash('sha256', $input))`, you have rebuilt both the fast-hash
        problem and the timing problem in one line.

        **Why it matters:** it is why the correct answer to "how do I check a password" is
        always a verify function, never a comparison operator.

        **Official reference:** https://www.php.net/manual/en/function.password-verify.php

## Memory hooks

??? question "One sentence that encodes the whole chapter."
    Think before revealing the answer.

    ??? success "Show answer"
        **"Escape at the output, bind at the query, regenerate at the login, hash at the
        password — and set the headers yourself."** The first four are Symfony defaults; the
        fifth never is.

        **Why it matters:** four defences and one gap, in the order they occur in a request.
        It reconstructs both the threat/defence table and the "what does the framework not
        do for me" question.

        **Official reference:** https://symfony.com/doc/8.0/security.html

??? question "A mnemonic for the session cookie flags."
    Think before revealing the answer.

    ??? success "Show answer"
        **"HttpOnly hides it from scripts, Secure hides it from the wire, SameSite hides it
        from other sites."** Three verbs, three adversaries: XSS, network, cross-site
        request.

        **Why it matters:** it makes the three flags impossible to swap, which is what the
        distractors in this area are built on.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#config-framework-session

---

<small>Back to the lesson: [Web Security Fundamentals](web-security.md) · [Retake the topic exam](web-security-exam.md) · Continue to the next stage: [HTTP](../http/index.md)</small>

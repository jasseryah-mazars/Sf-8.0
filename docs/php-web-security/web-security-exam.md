# Topic Exam — Web Security Fundamentals

!!! abstract "How to use this page"
    Answer each question **before** revealing the key. Every explanation states why the
    correct option is right *and* why each distractor is wrong, because the exam is built on
    near-misses rather than definitions.

    Theory: **[Web Security Fundamentals](web-security.md)** ·
    Practice: **[Guided exercises](web-security-exercises.md)** ·
    Recall: **[Flashcards](web-security-flashcards.md)**

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and
    aligned with the syllabus — it is not sourced from, or reviewed by, the official
    Symfony 8 certification.

All questions target **PHP 8.4** and **Symfony 8.0**.

## XSS and output escaping

??? question "Question 1"
    Twig's default protection against XSS in a Symfony application is…

    - A. Context auto-escaping of printed variables
    - B. Stripping every HTML tag from the output
    - C. A `Content-Security-Policy` response header added by TwigBundle
    - D. Encrypting the rendered output

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** Symfony applications are "safe by default because they perform
        automatic output escaping". Every `{{ … }}` printed value is escaped with the
        strategy chosen for the template, so `<script>alert('hello!')</script>` renders as
        `&lt;script&gt;alert(&#39;hello!&#39;)&lt;/script&gt;` — visible text, never executed
        markup.

        **B** is wrong because nothing is removed: escaping *transforms* the characters that
        have meaning in the output language, so the user still sees exactly what they typed.
        A tag-stripping sanitiser is a different, lossy tool. **C** is wrong because
        TwigBundle sends no CSP header; CSP is a defence-in-depth layer you configure
        yourself, and it does not replace escaping. **D** is wrong because escaping is not
        encryption — the output stays fully readable, it is only made inert.

        **Official reference:** https://symfony.com/doc/8.0/templates.html#output-escaping

??? question "Question 2 · Code analysis"
    A project has `templates/mail/welcome.txt.twig` containing `Hello {{ name }}` and
    `templates/mail/welcome.html.twig` containing `Hello {{ name }}`. `name` is
    `<b>Ada</b>`. What does each template output?

    - A. Both output `&lt;b&gt;Ada&lt;/b&gt;`
    - B. Both output `<b>Ada</b>`
    - C. The `.txt.twig` outputs `<b>Ada</b>`, the `.html.twig` outputs `&lt;b&gt;Ada&lt;/b&gt;`
    - D. The `.txt.twig` outputs `&lt;b&gt;Ada&lt;/b&gt;`, the `.html.twig` outputs `<b>Ada</b>`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** TwigBundle configures Twig's autoescaping with the `name` strategy,
        which delegates to `Twig\FileExtensionEscapingStrategy::guess()`. That method strips
        the trailing `.twig`, looks at the remaining extension and returns `js` for
        `js`/`json`, `css` for `css`, **`false` for `txt`** and `html` for everything else.
        `false` means autoescaping is *disabled* for that template, so the `.txt.twig`
        prints the raw string.

        **A** assumes the strategy is global; it is per-template and decided at compile
        time. **B** would only happen if autoescaping were switched off everywhere. **D**
        inverts the mapping — plain-text templates are the ones with no escaper, because
        there is no markup language to break in a `.txt` body.

        This is why an HTML e-mail rendered from a `.txt.twig` template, or user data piped
        into a `.txt.twig` and then embedded in HTML, is a classic stored-XSS hole.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/twig.html#config-twig-autoescape

??? question "Question 3 · Expert trap"
    Inside `profile.html.twig` you write:

    ```twig
    <div onmouseover="showTip('{{ tip }}')">…</div>
    ```

    Why is this **not** safe even though autoescaping is on?

    - A. Because autoescaping never applies inside an event-handler attribute
    - B. Because the template's strategy is `html` (chosen from the file name) and the browser HTML-decodes the attribute value *before* the JavaScript parser sees it, so `&#039;` turns back into a live `'` and closes the string
    - C. Because Twig escapes attributes with `css` instead of `js`
    - D. Because `{{ }}` is disabled inside attributes and only `{% %}` works

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the escaping strategy is picked **once per template, at compile
        time, from the file name** — not per element. A `.html.twig` file is compiled with
        the `html` strategy everywhere. That is correct for one context, and this attribute
        is *two* nested contexts: HTML attribute, then JavaScript. The HTML parser decodes
        entities in the attribute value first, so an escaped `&#039;` becomes a real quote
        by the time the JS parser runs, and `');alert(1);//` escapes the call. OWASP lists
        `<div onmouseover="'$varUnsafe'">` as exactly this trap and requires JavaScript
        encoding for it.

        **A** is wrong in the opposite direction: escaping *is* applied, it is simply the
        wrong escaper for the inner context. **C** invents a behaviour — `css` is only
        chosen for `.css.twig` files. **D** is wrong because `{{ }}` works everywhere in a
        Twig template; Twig does not parse HTML at all, it treats the file as text.

        The robust fix is not to nest contexts: put the value in a plain `data-` attribute
        and read it from an event listener in a real `.js` file.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

??? question "Question 4 · Multiple answer"
    Which statements about `{{ value|raw }}` are correct? (select all that apply)

    - A. It disables output escaping for that one printed expression
    - B. It sanitises the value by removing dangerous tags before printing
    - C. It is safe when the value was produced by your own code and already sanitised
    - D. It changes the escaping strategy of the whole template
    - E. Applying it to user-supplied input reintroduces XSS

    ??? success "Show answer"
        **Correct answer:** A, C and E

        **Explanation:** `raw` is documented as the filter to "disable the output escaping
        for that variable" when "you are rendering a variable that is trusted and contains
        HTML contents". It is a local opt-out (**A**), legitimate for trusted, already-safe
        markup (**C**), and a direct XSS vector on anything an attacker can influence
        (**E**).

        **B** is the single most damaging misconception: `raw` performs **no** sanitising
        whatsoever. It is the absence of a transformation, not a different transformation.
        **D** is wrong because the filter applies to one expression; changing the template's
        strategy needs `{% autoescape %}` or a different file extension.

        **Official reference:** https://symfony.com/doc/8.0/templates.html#output-escaping

??? question "Question 5 · Edge case"
    Which Twig escaping strategy is designed for a value injected into an **unquoted** HTML
    attribute, e.g. `<p data-x={{ v }}>`?

    - A. `html`
    - B. `url`
    - C. `html_attr`
    - D. `css`

    ??? success "Show answer"
        **Correct answer:** C

        **Explanation:** the Twig documentation defines `html_attr` as the strategy for a
        string "used as an HTML attribute name, and also when used as the value of an HTML
        attribute **without quotes**". Without quotes, a space or `/` in the value is enough
        to start a new attribute (`onmouseover=…`), which `html` escaping does not prevent.

        **A** `html` covers "the HTML body context, or for HTML attribute values **inside
        quotes**" — the documented, and more performant, recommendation is to quote the
        attribute and use `html`. **B** `url` is for "the URI or parameter contexts", and
        the docs warn it "should not be used to escape an entire URI; only a subcomponent".
        **D** `css` escapes everything except alphanumerics for stylesheet contexts.

        **Official reference:** https://twig.symfony.com/doc/3.x/filters/escape.html

## SQL injection

??? question "Question 6"
    Which technique best prevents SQL injection?

    - A. Prepared statements with bound parameters
    - B. Escaping quotes in the input with `addslashes()`
    - C. Putting a web application firewall in front of the app
    - D. HTML-escaping the input before building the query

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** with `PDO::prepare()` the SQL text and the data travel separately.
        The statement's structure is fixed before any user value is attached, so a bound
        value can only ever be read as a literal — it can never become a new clause.

        **B** is a blocklist that has been broken repeatedly (multi-byte charset tricks,
        numeric contexts with no quotes at all, identifiers that cannot be quoted). **C** is
        a mitigation layer, not a fix: a WAF guesses at payloads and is bypassed by
        encoding, while a prepared statement removes the ambiguity entirely. **D** confuses
        two output contexts — HTML entities mean nothing to a SQL parser, and `&lt;` inside
        a query is just a weird string.

        **Official reference:** https://www.php.net/manual/en/pdo.prepare.php

??? question "Question 7 · Code analysis"
    Which of these Doctrine snippets is injectable?

    ```php
    // (1)
    $qb->where('p.name = :name')->setParameter('name', $name);

    // (2)
    $qb->where("p.name = '".$name."'");

    // (3)
    $em->createQuery('SELECT p FROM App\Entity\Product p WHERE p.price > :price')
       ->setParameter('price', $price);
    ```

    - A. Only (2)
    - B. Only (2) and (3)
    - C. All three, because DQL is compiled to SQL
    - D. None, because DQL is not SQL

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** DQL is compiled into SQL, and the compiled SQL is executed as a
        prepared statement with the values supplied through `setParameter()`. (1) and (3)
        follow the documented pattern and are safe. (2) concatenates the value into the DQL
        string *before* parsing, so the attacker controls the query text — exactly the same
        hole as string-built SQL.

        **B** wrongly condemns (3): a named placeholder plus `setParameter()` is the
        documented safe form. **C** is the mirror mistake — compilation to SQL is irrelevant
        once the value is bound rather than interpolated. **D** is the dangerous myth that a
        different query language is automatically immune; DQL parsing is just as
        manipulable when you build the string by concatenation.

        **Official reference:** https://symfony.com/doc/8.0/doctrine.html#doctrine-queries

## CSRF

??? question "Question 8"
    Why is `SameSite=Lax` on the session cookie **not** a complete CSRF defence on its own?

    - A. Because browsers ignore `SameSite` on POST requests
    - B. Because `Lax` still sends the cookie on top-level cross-site `GET` navigations, so any state-changing `GET` endpoint stays exploitable, and older or non-conforming clients may not enforce it at all
    - C. Because `SameSite` only applies to cookies set by JavaScript
    - D. Because Symfony strips the `SameSite` attribute when a firewall is active

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the reference describes `lax` as "allow sending cookies when the
        request originated from a different domain, but only when the user consciously made
        the request (by clicking a link or submitting a form with the `GET` method)". So a
        cross-site top-level `GET` still carries the session. If any endpoint changes state
        on `GET`, `Lax` does not protect it — which is exactly why OWASP requires CSRF
        protection on state-changing operations and forbids performing them with `GET`.
        `SameSite` is also a browser-side control: you cannot rely on every client
        enforcing it.

        **A** is false — `Lax` is precisely the value that *does* withhold the cookie on
        cross-site POST. **C** is false: `SameSite` is an attribute of the `Set-Cookie`
        header regardless of who set it. **D** is invented; Symfony sets `cookie_samesite`
        to `lax` by default and a firewall does not remove it.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#config-framework-session

??? question "Question 9 · Expert trap"
    You render the same form twice and notice the value of the hidden `_token` field is
    different each time, even though you never called `refreshToken()`. What happened?

    - A. The token is regenerated in the session on every render, so only the last form can be submitted
    - B. The stored token is unchanged; `CsrfTokenManager::getToken()` returns the stored value XOR-masked with fresh random bytes on every call, and validation de-randomises before comparing
    - C. The form component appends a timestamp to the token
    - D. CSRF protection is misconfigured — a stable token is expected

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `CsrfTokenManager::getToken()` reads (or creates) the secret in the
        token storage and then returns `$this->randomize($value)` — the secret XORed with 32
        fresh random bytes, emitted as `hash.key.value`. `isTokenValid()` calls
        `derandomize()` and compares with `hash_equals()`. The documentation explains the
        purpose: BREACH and CRIME are compression side-channel attacks, and "a random mask
        is prepended to the token and used to scramble it" so the ciphertext of the response
        never repeats.

        **A** is wrong and would be a real bug: the *stored* secret is stable, so both
        rendered forms validate. **C** invents a mechanism; there is no timestamp. **D**
        inverts the expectation — a byte-identical token on every render is the pattern the
        masking exists to avoid.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Csrf/CsrfTokenManager.php

??? question "Question 10 · Configuration consequence"
    Your pages cannot be HTTP-cached because rendering a CSRF-protected form starts a
    session. Which Symfony 8.0 feature removes that constraint while keeping CSRF
    protection?

    - A. Setting `framework.csrf_protection: false`
    - B. Listing the token IDs in `framework.csrf_protection.stateless_token_ids`
    - C. Setting `framework.session.enabled: false`
    - D. Moving the token into a `GET` query parameter

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "By default, the tokens used for CSRF protection are stored in the
        session. That's why a session is started automatically as soon as you render a form
        with CSRF protection." Token IDs listed under `stateless_token_ids` switch to
        stateless CSRF, which "provide protection without relying on the session" and
        "allows you to fully cache pages while still protecting against CSRF attacks".

        **A** removes the protection instead of the session dependency. **C** breaks
        authentication and does not make stateful tokens work — they need the session they
        no longer have. **D** is explicitly discouraged: including CSRF tokens in `GET`
        parameters "can cause them to leak through browser history, log files, network
        utilities, and Referer headers".

        **Official reference:** https://symfony.com/doc/8.0/security/csrf.html#csrf-stateless-tokens

??? question "Question 11 · Execution flow"
    When Symfony validates a **stateless** CSRF token, what is checked first, before any
    optional cookie/header comparison?

    - A. The token value stored in the session
    - B. The `Origin` and `Referer` headers of the request against the application's own origin
    - C. The `User-Agent` string
    - D. A signature computed from `kernel.secret`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "When validating a stateless CSRF token, Symfony checks the
        `Origin` and `Referer` headers of the incoming HTTP request. If either header
        matches the application's target origin (i.e. its domain), the token is considered
        valid." The cookie/header "double-submit" comparison is described as an *additional*
        defence-in-depth layer that needs JavaScript and is applied opportunistically.

        **A** is the stateful mechanism, which stateless tokens exist to avoid. **C** is
        never a security control — it is fully attacker-controlled. **D** describes a signed
        token scheme Symfony does not use here.

        Because this relies on the app knowing its own origin, a misconfigured reverse
        proxy breaks it — hence the pointer to trusted-proxy configuration.

        **Official reference:** https://symfony.com/doc/8.0/security/csrf.html#csrf-stateless-tokens

??? question "Question 12 · Code analysis"
    ```php
    #[IsCsrfTokenValid('delete-item', tokenKey: 'token', methods: ['DELETE'])]
    public function delete(Post $post): Response
    {
        // ... delete the object
    }
    ```

    A `POST` request reaches this action with no `token` value at all. What happens?

    - A. A 403 is returned because the token is missing
    - B. The attribute is ignored, no CSRF validation happens, and the action runs
    - C. Symfony throws a `LogicException` because the method is not allowed
    - D. The request is rewritten to `DELETE` and validated

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the documentation is explicit: "If the request uses a method not
        listed in the `methods` array, the attribute is ignored for that request, and no
        CSRF validation occurs." Restricting `methods` narrows *when* the check applies; it
        never rejects other methods.

        **A** is the intuitive but wrong reading — no check runs, so nothing can fail.
        **C** invents an exception; `methods` is a filter, not a route requirement. **D**
        invents method overriding. The practical lesson: `methods` is a foot-gun unless the
        route itself is already restricted to the same methods.

        **Official reference:** https://symfony.com/doc/8.0/security/csrf.html#csrf-controller-attributes

??? question "Question 13 · True/False"
    "Symfony Forms include CSRF tokens by default and check them automatically, so a form
    built with the Form component needs no extra CSRF code."

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** A — True

        **Explanation:** "Symfony Forms include CSRF tokens by default and Symfony also
        checks them automatically for you. So, when using Symfony Forms, you don't have to
        do anything to be protected against CSRF attacks." The token lands in a hidden field
        named `_token` unless `csrf_field_name` changes it.

        **B** is the trap for people who remember `csrf_token()` and `isCsrfTokenValid()`.
        Those exist for **hand-written HTML forms not managed by the Form component**, and
        for the login and logout flows, which are handled by the Security component rather
        than the Form component.

        **Official reference:** https://symfony.com/doc/8.0/security/csrf.html#csrf-protection-forms

## Session security

??? question "Question 14"
    Session fixation is mitigated primarily by…

    - A. Regenerating the session id when the user authenticates
    - B. Using longer session ids
    - C. Deleting cookies on logout only
    - D. Base64-encoding the session id before sending it

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** in a fixation attack the attacker plants a session id they already
        know and waits for the victim to authenticate on it. "Applications that don't assign
        new session IDs when authenticating users are vulnerable to this attack." Assigning
        a fresh id at the privilege change makes the planted id worthless.

        **B** raises the cost of *guessing* an id, which is a different attack; a fixed id
        is known, not guessed. **C** happens far too late — the attacker rides the session
        while the victim is logged in. **D** is encoding, not a security property: the id is
        just as reusable after a round trip through base64.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/security.html#session-fixation-strategy

??? question "Question 15 · Expert"
    What is the default value of `security.firewalls.<name>.session_fixation_strategy`, and
    what exactly does it do?

    - A. `NONE` — the session is untouched
    - B. `MIGRATE` — the session id is updated and the session attributes are kept
    - C. `INVALIDATE` — the id is updated and every attribute is discarded
    - D. There is no default; the option is mandatory

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the reference gives the default as
        `SessionAuthenticationStrategy::MIGRATE`, described as "the session ID is updated,
        but the rest of the session attributes are kept". In the source,
        `SessionAuthenticationStrategy::onAuthentication()` calls
        `$request->getSession()->migrate(true)` for that strategy — and, when a CSRF token
        storage is available, also clears it so pre-login tokens cannot be replayed.

        **A** is offered by the option but the docs mark it "**not recommended**" — it is
        the vulnerable configuration. **C** is a valid, stricter choice, but it is not the
        default and it costs you the flash bag, the cart, the locale and everything else
        stored before login. **D** is wrong: the option has a documented default, which is
        why Symfony apps are protected without configuration.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Session/SessionAuthenticationStrategy.php

??? question "Question 16 · Code analysis"
    ```php
    $session->migrate();          // (1)
    $session->migrate(true);      // (2)
    $session->invalidate();       // (3)
    ```

    Which statement is correct?

    - A. (1) and (2) are identical; (3) additionally logs the user out
    - B. (1) creates a new id and leaves the old session data in storage; (2) creates a new id and destroys the old record; (3) clears the attributes and then does (2)
    - C. All three destroy the old session record
    - D. (3) only deletes the cookie; the server-side record survives

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `Session::migrate(bool $destroy = false, ?int $lifetime = null)`
        forwards to `NativeSessionStorage::regenerate()`, which ends in
        `session_regenerate_id($destroy)`. With `$destroy = false` the old server-side record
        is left behind; with `true` it is deleted. `Session::invalidate()` is literally
        `$this->storage->clear(); return $this->migrate(true, $lifetime);`.

        **A** ignores the `$destroy` argument, which is the entire point of the signature.
        **C** is wrong for the default call — an orphan session record that still holds the
        pre-migration data is exactly what an attacker wants. **D** inverts the model: the
        authoritative state is server-side, and `invalidate()` clears it.

        **Official reference:** https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Session/Session.php

??? question "Question 17 · Multiple answer"
    Which of these are the **documented defaults** for `framework.session` in Symfony 8.0?
    (select all that apply)

    - A. `cookie_httponly: true`
    - B. `cookie_samesite: 'lax'`
    - C. `cookie_secure: true`
    - D. `save_path: %kernel.cache_dir%/sessions`
    - E. `enabled: true`

    ??? success "Show answer"
        **Correct answer:** A, B, D and E

        **Explanation:** the framework reference lists `cookie_httponly` **type** boolean
        **default** `true`, `cookie_samesite` **default** `'lax'`, `save_path` **default**
        `%kernel.cache_dir%/sessions` and `enabled` **default** `true`.

        **C** is the odd one out: `cookie_secure` is documented as "**type**: boolean or
        `'auto'`" with **no** default — "if not set, `php.ini`'s `session.cookie_secure`
        directive will be relied on". The recommended value is `'auto'`, which "means `true`
        for HTTPS requests and `false` for HTTP requests" so local HTTP development keeps
        working. Assuming a hard `true` default is a common and dangerous mistake, because
        it makes people believe the flag is already on.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#config-framework-session

??? question "Question 18 · Expert trap"
    `session.use_strict_mode` is `0` by default in PHP. What is it in a standard Symfony 8.0
    application, and why does that matter?

    - A. Still `0` — Symfony never touches PHP session ini settings
    - B. `1` — `NativeSessionStorage` defaults the option to `1`, so PHP refuses uninitialised session ids and issues a new one instead of adopting the attacker's
    - C. `1`, but only when `framework.session.cookie_secure` is `true`
    - D. It is irrelevant because Symfony does not use PHP's native session handling

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the PHP manual documents the directive's default as `0` and states
        that "enabling `session.use_strict_mode` is mandatory for general session security".
        `NativeSessionStorage::__construct()` merges `'use_strict_mode' => 1` into the
        options and `setOptions()` applies it with `ini_set('session.use_strict_mode', 1)`.
        Without it, PHP *adopts* any id the browser sends — the session-adoption flavour of
        fixation.

        **A** is contradicted by the constructor. **C** invents a dependency; the two
        options are unrelated. **D** is wrong: the default storage is precisely PHP's native
        session. Note the manual's caveat — a custom save handler that does not implement
        `validateId()` disables strict mode in practice regardless of the directive.

        **Official reference:** https://www.php.net/manual/en/session.configuration.php#ini.session.use-strict-mode

??? question "Question 19 · Debugging"
    An audit reports that a stolen session cookie let an attacker impersonate a user. Which
    two cookie flags address *different* halves of that problem, and how?

    - A. `HttpOnly` hides the cookie from JavaScript (so an XSS cannot read it); `Secure` prevents it being sent over plain HTTP (so a network attacker cannot capture it)
    - B. `HttpOnly` forces HTTPS; `Secure` hides the cookie from JavaScript
    - C. Both do the same thing with different names
    - D. Neither matters once `SameSite=Strict` is set

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `cookie_httponly` "determines whether cookies should only be
        accessible through the HTTP protocol… the cookie won't be accessible by scripting
        languages, such as JavaScript", and the reference explicitly ties it to reducing
        "identity theft through XSS attacks". `cookie_secure` "determines whether cookies
        should only be sent over secure connections". Two theft channels, two flags.

        **B** swaps the two — the single most common mix-up on this topic. **C** is wrong
        because an XSS payload and a passive network sniffer are entirely different
        adversaries. **D** confuses theft with forgery: `SameSite` governs when the browser
        *attaches* a cookie to a cross-site request, and does nothing once the value itself
        has leaked.

        **Official reference:** https://symfony.com/doc/8.0/reference/configuration/framework.html#config-framework-session

## Clickjacking, HTTPS and security headers

??? question "Question 20"
    Which response header defends against clickjacking?

    - A. `X-Frame-Options: DENY` (or CSP `frame-ancestors 'none'`)
    - B. `X-Content-Type-Options: nosniff`
    - C. `Referrer-Policy: no-referrer`
    - D. `Accept-Language`

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** clickjacking loads your page in a transparent frame over bait UI so
        the victim's clicks land on your controls. Forbidding framing is the fix, and OWASP
        recommends `Content-Security-Policy: frame-ancestors 'none'` with `X-Frame-Options`
        as the legacy fallback.

        **B** stops MIME sniffing — it prevents a text upload being executed as a script,
        not framing. **C** limits how much URL information leaks in the `Referer` header.
        **D** is a *request* header sent by the browser for content negotiation and is not a
        security control at all.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html

??? question "Question 21 · Multiple answer"
    Which statements about `X-Frame-Options` and CSP `frame-ancestors` are correct? (select
    all that apply)

    - A. `frame-ancestors` supersedes `X-Frame-Options` in browsers that support CSP
    - B. `X-Frame-Options` has a well-supported `ALLOW-FROM` value for a single origin
    - C. `frame-ancestors` can list several allowed origins
    - D. Sending both is a reasonable strategy while legacy clients exist

    ??? success "Show answer"
        **Correct answer:** A, C and D

        **Explanation:** OWASP quotes the CSP specification: "If a resource is delivered
        with a policy that includes a directive named `frame-ancestors` and whose
        disposition is 'enforce', then the `X-Frame-Options` header MUST be ignored" — with
        the caveat that some old browser versions did the opposite. `frame-ancestors`
        "allows a site to authorize multiple domains using the normal Content Security
        Policy semantics", e.g.
        `frame-ancestors 'self' *.somesite.com https://myfriend.site.com`. Keeping both
        headers is the documented belt-and-braces approach.

        **B** is the trap: `ALLOW-FROM` is described as "an obsolete directive that no
        longer works in modern browsers", and OWASP warns that depending on it can leave you
        with "NO clickjacking defense in place". Allow-listing a specific parent origin is
        precisely what you must express with `frame-ancestors`. A second detail worth
        remembering: neither control works from a `<meta http-equiv>` tag — both must be
        real HTTP response headers.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html

??? question "Question 22 · True/False"
    "`Strict-Transport-Security` protects the very first request a browser ever makes to
    your domain."

    - A. True
    - B. False

    ??? success "Show answer"
        **Correct answer:** B — False

        **Explanation:** OWASP describes HSTS as "an opt-in security enhancement…
        specified by a web application through the use of a special response header. **Once
        a supported browser receives this header**, that browser will prevent any
        communications from being sent over HTTP to the specified domain." The policy is
        therefore learned only after a first successful visit; that first plain-HTTP request
        remains exposed. The documented remedy is submitting the domain to the HSTS preload
        list, which ships the policy inside the browser.

        **A** is the intuitive reading and the classic exam trap. Two facts worth pairing
        with it: omitting `includeSubDomains` "permits a broad range of cookie-related
        attacks that HSTS would otherwise prevent", and sending `preload` "can have
        PERMANENT CONSEQUENCES" if you ever need to move a subdomain back to HTTP.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html

??? question "Question 23 · Configuration consequence"
    Which Symfony security configuration forces a request that arrives over `http` to be
    redirected to `https`?

    - A. `framework.session.cookie_secure: true`
    - B. An `access_control` entry with `requires_channel: https`
    - C. `framework.trusted_proxies: private_ranges`
    - D. `security.firewalls.main.stateless: true`

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** "`requires_channel` If the incoming request's channel (e.g. `http`)
        does not match this value (e.g. `https`), the user will be redirected". A matching
        `access_control` entry with `requires_channel: https` therefore performs the
        redirect.

        **A** only controls the `Secure` attribute of the session cookie — with no
        redirection, a plain-HTTP page simply loses its session. **C** tells Symfony which
        `X-Forwarded-*` headers to trust so that `Request::isSecure()` is accurate behind a
        load balancer; it is a *prerequisite* for `requires_channel` to see the real scheme,
        not the redirect itself. **D** disables the session for that firewall and has
        nothing to do with the transport.

        **Official reference:** https://symfony.com/doc/8.0/security/access_control.html#forcing-a-channel-http-https

## Password storage

??? question "Question 24"
    The correct way to store user passwords is…

    - A. `password_hash()` with bcrypt or argon2id
    - B. SHA-256 with one static application-wide salt
    - C. MD5
    - D. Reversible encryption, so support can recover them

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** `password_hash()` "creates a new password hash using a strong
        one-way hashing algorithm", generates a random salt per password, and embeds the
        algorithm, cost and salt in the result so `password_verify()` needs no separate
        storage.

        **B** fails twice: SHA-256 is fast (billions of guesses per second on a GPU) and a
        static salt lets one rainbow table cover every account. **C** is the same problem,
        worse, on a broken hash. **D** is a design error, not a weak choice: any key that
        can decrypt is a key an attacker can steal, and a support agent should never be able
        to read a password.

        **Official reference:** https://www.php.net/manual/en/function.password-hash.php

??? question "Question 25 · Expert trap"
    In Symfony 8.0, `algorithm: 'auto'` is configured for `App\Entity\User`. Which algorithm
    actually **hashes** a newly registered user's password on a server where libsodium is
    available?

    - A. Argon2id, because it is the strongest available
    - B. Bcrypt, via `NativePasswordHasher`, which is the first hasher of the migrating chain
    - C. PBKDF2, for portability
    - D. It is random per request

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the reference for the "auto" hasher says it "automatically selects
        the best available hasher (**currently Bcrypt**)". `PasswordHasherFactory` builds a
        `MigratingPasswordHasher` from the chain `['native', 'sodium', 'pbkdf2']`, and
        `MigratingPasswordHasher::hash()` delegates to the **first** hasher only.
        `NativePasswordHasher`'s `$algorithm` property is initialised to `PASSWORD_BCRYPT`.

        **A** is the reasonable-sounding answer that Symfony 8.0's own reference contradicts;
        `sodium` sits in the chain for *verification and migration*, not for hashing new
        passwords. **C** is last in the chain, kept only to verify legacy hashes. **D**
        would make verification impossible.

        The point of `auto` is that this answer may legitimately change in a future release
        — which is the whole reason `needsRehash()` exists.

        **Official reference:** https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/PasswordHasher/Hasher/PasswordHasherFactory.php

??? question "Question 26 · Execution order"
    Passwords must be rehashed after a hasher upgrade. Put the steps in the order Symfony
    performs them.

    1. The repository persists the new hash
    2. The user submits valid credentials
    3. Symfony checks whether a better algorithm is available for the stored hash
    4. `PasswordUpgraderInterface::upgradePassword()` is called with the freshly hashed password

    - A. 2 → 3 → 4 → 1
    - B. 3 → 2 → 4 → 1
    - C. 2 → 4 → 3 → 1
    - D. 1 → 2 → 3 → 4

    ??? success "Show answer"
        **Correct answer:** A

        **Explanation:** "Upon **successful login**, the Security system checks whether a
        better algorithm is available to hash the user's password. If it is, it'll hash the
        correct password using the new hash." Storage then happens in your implementation of
        `PasswordUpgraderInterface::upgradePassword()`, typically on the `UserRepository`,
        which sets the password and flushes.

        **B** is impossible: the plaintext is only available once the user submits it, and
        rehashing requires the plaintext. **C** puts persistence before the decision to
        rehash. **D** starts with a write that has no value to write yet.

        The failure mode to remember: if you never implement `PasswordUpgraderInterface`,
        `migrate_from` still lets old hashes authenticate but nothing is ever upgraded, and
        the migration silently never completes.

        **Official reference:** https://symfony.com/doc/8.0/security/passwords.html#security-password-migration

??? question "Question 27 · Edge case"
    ```php
    $hash = password_hash($plain, PASSWORD_BCRYPT, ['salt' => $mySalt, 'cost' => 12]);
    ```

    On PHP 8.4, what happens to `$mySalt`?

    - A. It is used as the salt
    - B. It is ignored; an explicitly given salt has been ignored since PHP 8.0.0
    - C. A `ValueError` is thrown
    - D. It is appended to the password before hashing

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual's changelog and the option description are explicit: the
        `salt` option is deprecated and "as of PHP 8.0.0, an explicitly given salt is
        ignored". `password_hash()` always generates a cryptographically random salt per
        call and embeds it in the output.

        **A** describes pre-8.0 behaviour. **C** is wrong — a `ValueError` is thrown for an
        *invalid algorithm*, not for a stray option. **D** invents peppering; a pepper is a
        separate design that lives outside the hash function.

        The related PHP 8.4 change worth memorising: the default `cost` for
        `PASSWORD_BCRYPT` was raised from **10 to 12**. Symfony's `NativePasswordHasher`
        overrides it with its own default of **13**.

        **Official reference:** https://www.php.net/manual/en/function.password-hash.php

??? question "Question 28 · Expert"
    Why does `NativePasswordHasher` pre-hash long passwords with `sha512` and base64 before
    calling `password_hash()`?

    - A. To make hashing faster
    - B. Because bcrypt truncates the input at 72 bytes, so without pre-hashing everything after byte 72 would be silently ignored
    - C. Because `password_hash()` rejects strings longer than 72 bytes
    - D. To add a pepper

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual states that using `PASSWORD_BCRYPT` "will result in the
        password parameter being truncated to a maximum length of 72 bytes". The source
        guards exactly that case: when the algorithm is bcrypt and the password exceeds 72
        bytes (or contains a NUL), it hashes with `sha512` and base64-encodes before
        delegating — so the whole passphrase contributes entropy.

        **A** is backwards: hashing is deliberately slow, and the extra sha512 is
        negligible. **C** is wrong — PHP truncates silently rather than erroring, which is
        what makes the bug so hard to notice. **D** is a different concept; no secret key is
        involved. Symfony's independent 4096-byte guard
        (`PasswordHasherInterface::MAX_PASSWORD_LENGTH`) is a DoS protection against
        multi-megabyte "passwords", not a bcrypt concern.

        **Official reference:** https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/PasswordHasher/Hasher/NativePasswordHasher.php

## Timing, redirects, mass assignment and uploads

??? question "Question 29 · Debugging"
    ```php
    if ($submittedSignature === $expectedSignature) { /* accept */ }
    ```

    What is wrong, and what is the correct replacement?

    - A. Nothing is wrong; `===` is a strict comparison
    - B. `===` on strings short-circuits at the first differing byte, leaking the position of the mismatch through timing; use `hash_equals($expectedSignature, $submittedSignature)`
    - C. Use `==` instead, which is constant-time
    - D. Use `strcmp()`, which is constant-time

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the manual for `hash_equals()` says a "regular comparison with
        `===` will take more or less time to execute depending on whether the two values are
        different or not and at which position the first difference can be found, thus
        leaking information about the contents of the secret". It also insists on the
        argument order: "It is important to provide the user-supplied string as the
        **second** parameter, rather than the first."

        **A** confuses type strictness with timing safety — they are unrelated properties.
        **C** is worse: `==` adds PHP's loose comparison rules on top and is still not
        constant-time. **D** is wrong — `strcmp()` also returns as soon as it finds a
        difference. This is exactly why `CsrfTokenManager::isTokenValid()` uses
        `hash_equals()`.

        **Official reference:** https://www.php.net/manual/en/function.hash-equals.php

??? question "Question 30 · Scenario"
    A controller does `return $this->redirect($request->query->get('next'));` after login.
    What is the vulnerability and the correct fix?

    - A. None; the value comes from the same site
    - B. An open redirect: an attacker sends `?next=https://evil.example/login` to make a phishing page look like it was reached from your domain. Fix by allow-listing, or by treating the parameter as a **route name**/relative path and generating the URL yourself
    - C. It is an XSS; escape the value with `|e('url')`
    - D. It is a CSRF; add a token to the link

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** `redirect()` sends whatever URL it is given; the framework performs
        no origin validation. An externally supplied absolute URL therefore turns your
        trusted domain into a redirector, which is the classic phishing amplifier OWASP
        documents under unvalidated redirects and forwards. The robust fixes are to never
        accept a full URL from the client — accept a route name or a bare path and build the
        URL with `generateUrl()`/`redirectToRoute()` — or to validate the host against an
        allow-list.

        **A** is wrong because a query parameter is attacker-controlled by definition; it
        arrives in a link the attacker wrote. **C** solves an output-encoding problem that
        is not the issue here — a perfectly escaped URL still redirects. **D** is the wrong
        threat: nothing about the victim's own state is being forged; they are simply sent
        somewhere else.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html

??? question "Question 31 · Configuration consequence"
    What is the default value of the `allow_extra_fields` option on Symfony's `FormType`,
    and what does it protect against?

    - A. `true` — extra fields are silently mapped onto the entity
    - B. `false` — submitting a field the form does not declare produces a validation error, which blocks mass assignment through the form layer
    - C. `null` — the behaviour depends on `data_class`
    - D. `false` — but it only affects rendering, not submission

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the `FormType` reference documents `allow_extra_fields` as
        **type** boolean **default** `false`: "if you submit extra fields that aren't
        configured in your form, you'll get a 'This form should not contain extra fields.'
        validation error". So a request that adds `roles[]=ROLE_ADMIN` to a profile form is
        rejected rather than mapped.

        **A** inverts the default and describes the classic mass-assignment hole. **C**
        invents a dependency on `data_class`. **D** is wrong because the option is precisely
        about **submitted** data — the form never renders fields it does not declare.

        The remaining risk is a field you *did* declare and did not intend to expose, which
        is why sensitive properties belong outside the form type or behind `mapped: false`.

        **Official reference:** https://symfony.com/doc/8.0/reference/forms/types/form.html#form-option-allow-extra-fields

??? question "Question 32 · Edge case"
    A user uploads `invoice.pdf.php` with a PDF magic header. Which combination best
    protects the application?

    - A. Trust `UploadedFile::getClientOriginalName()` and keep the name as sent
    - B. Generate a new file name, derive the extension from the detected media type with `guessExtension()`, validate with the `File` constraint's `extensions` option, and store outside the web root
    - C. Check only `$_FILES['file']['type']`
    - D. Rely on `X-Content-Type-Options: nosniff` alone

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** the upload documentation calls the client-supplied name, path,
        extension and size "**not safe** because a malicious user could tamper with that
        information", and recommends generating a unique name plus `guessExtension()`, which
        derives the extension from the detected MIME type. The `File` constraint's
        `extensions` option checks the extension **and** the media type together — the
        reference warns you to prefer it over `mimeTypes`, because checking the media type
        without checking that the extension is consistent with the content "can be a
        security issue". Storing outside the document root removes the possibility of the
        server executing the file at all.

        **A** is the vulnerability itself: a name the attacker chose, including its
        extension and any `../` it contains. **C** is worse — `$_FILES[...]['type']` is
        copied straight from the request and never verified by PHP. **D** stops MIME
        sniffing in the *browser*; it does nothing about the web server deciding to run a
        `.php` file.

        **Official reference:** https://symfony.com/doc/8.0/controller/upload_file.html

??? question "Question 33 · Expert trap"
    Which single statement is true?

    - A. Escaping input on the way *into* the database is equivalent to escaping output on the way out
    - B. Output escaping is context-dependent, so it must happen where the value is used — the same stored string needs `html`, `js`, `url` or `css` escaping depending on where it lands
    - C. Validation replaces escaping
    - D. `htmlspecialchars()` at insert time makes a value safe for every later context

    ??? success "Show answer"
        **Correct answer:** B

        **Explanation:** a stored value has no single "safe" form. The correct
        transformation depends on the grammar of the destination — HTML body, JavaScript
        string, URL component, CSS — which is exactly why Twig exposes `html`, `js`, `url`,
        `css` and `html_attr` strategies rather than one escaper.

        **A** and **D** describe input-escaping, the historical anti-pattern: values get
        double-escaped when re-rendered, arrive corrupted in JSON APIs and CSV exports, and
        are still unsafe inside a `<script>` or a URL. **C** confuses two complementary
        controls: validation decides whether a value is *acceptable* ("is this a valid
        e-mail?"), escaping decides how it is *represented* in one output language. A
        perfectly valid name may still contain `<`.

        **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

---

<small>Back to the lesson: [Web Security Fundamentals](web-security.md) · [Guided exercises](web-security-exercises.md) · [Review flashcards](web-security-flashcards.md)</small>

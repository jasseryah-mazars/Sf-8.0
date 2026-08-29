# Guided Exercises — Web Security Fundamentals

!!! abstract "How to use this page"
    Work top to bottom: each exercise changes **one** thing from the previous one. Commit to
    an answer before revealing a hint, and to a full attempt before revealing the solution.

    Theory: **[Web Security Fundamentals](web-security.md)** · Then:
    **[Topic exam](web-security-exam.md)**

    Every snippet below runs as a standalone file with `php file.php` on **PHP 8.4** — no
    framework, no database server, no network. That is deliberate: the point of this chapter
    is that you can *watch* an escaper miss a character and *watch* a login be bypassed,
    instead of taking either on faith. Where a snippet reproduces Symfony or Twig behaviour,
    the reproduction is labelled as such and the real implementation is linked.

## Exercise 1 · Find out what HTML escaping actually does

**Objective:** Replace "Twig escapes, so I am safe" with a precise list of the characters
each strategy touches.

**Context:** Twig's `html` strategy is one `htmlspecialchars()` call; its `js` strategy
escapes almost everything. Seeing the two side by side is what makes "context-aware
escaping" stop being a slogan.

**Starting point:**

```php
<?php
declare(strict_types=1);

// Twig's 'html' strategy is exactly this call.
$html = static fn (string $s): string => htmlspecialchars(
    $s,
    ENT_QUOTES | ENT_SUBSTITUTE,
    'UTF-8',
);

// Twig's 'js' strategy escapes every character outside [a-zA-Z0-9,._].
// (Simplified: real Twig emits short forms such as \\ and \/ for a few chars.)
$js = static fn (string $s): string => preg_replace_callback(
    '#[^a-zA-Z0-9,\._]#Su',
    static fn (array $m): string => sprintf('\u%04X', mb_ord($m[0], 'UTF-8')),
    $s,
);

$chars = ['<', '>', '&', '"', "'", '\\', '/', ' ', '(', ';', '=', '`'];

printf("%-6s | %-8s | %s\n", 'char', 'html', 'js');
printf("%s\n", str_repeat('-', 32));
foreach ($chars as $c) {
    printf("%-6s | %-8s | %s\n", $c, $html($c), $js($c));
}
```

**Task:** Before running, predict which of the twelve characters the `html` column leaves
untouched. Then run the file.

**Expected observation:** `html` transforms exactly five characters and passes the other
seven through unchanged.

??? tip "Show a hint"
    The name of the function is the answer: `htmlspecialchars` escapes the characters that
    are *special in HTML*. Ask yourself which of `\`, `/`, `(`, `;`, `=` and `` ` `` change
    the meaning of an HTML document. Then ask the same question about a JavaScript program.

??? success "Show the solution"
    ```
    char   | html     | js
    --------------------------------
    <      | &lt;     | \u003C
    >      | &gt;     | \u003E
    &      | &amp;    | \u0026
    "      | &quot;   | \u0022
    '      | &#039;   | \u0027
    \      | \        | \u005C
    /      | /        | \u002F
           |          | \u0020
    (      | (        | \u0028
    ;      | ;        | \u003B
    =      | =        | \u003D
    `      | `        | \u0060
    ```

    `html` touches `<`, `>`, `&`, `"` and `'` — and nothing else. `js` escapes all twelve,
    including the space, because it keeps only `[a-zA-Z0-9,._]`.

    `ENT_QUOTES` is what adds the two quote characters to the HTML set; without it, single
    quotes would survive and every single-quoted HTML attribute would be injectable.
    `ENT_SUBSTITUTE` replaces invalid UTF-8 byte sequences with U+FFFD instead of returning
    an empty string, so a deliberately mangled payload cannot blank the value out.

    **Why it works:** escaping is a *translation into one output language*. HTML's grammar
    only reacts to those five characters, so a correct HTML escaper has no reason to touch
    the others. A JavaScript program reacts to almost everything, so the `js` strategy
    inverts the logic: keep the alphanumerics, escape the rest.

    **Certification takeaway:** "escaped" is meaningless without "escaped for *what*". A
    value that is perfectly HTML-escaped is still raw input as far as a JavaScript parser,
    a URL parser or a CSS parser is concerned.

    **Official reference:** https://twig.symfony.com/doc/3.x/filters/escape.html

## Exercise 2 · Fix a nested-context XSS with the right escaper

**Objective:** Write the minimal correct fix for a value that lands inside an HTML attribute
*and* inside a JavaScript string.

**Context:** A template renders `<div onmouseover="showTip('{{ tip }}')">`. The template is
`tip.html.twig`, so Twig compiles it with the `html` strategy.

**Starting point:**

```php
<?php
declare(strict_types=1);

$html = static fn (string $s): string => htmlspecialchars(
    $s,
    ENT_QUOTES | ENT_SUBSTITUTE,
    'UTF-8',
);

$payload = "');alert(1);//";

// What the browser receives:
$attribute = sprintf('<div onmouseover="showTip(\'%s\')">', $html($payload));
echo $attribute, "\n";

// What the HTML parser hands to the JavaScript parser
// (entities inside an attribute value are decoded first):
echo html_entity_decode($attribute, ENT_QUOTES, 'UTF-8'), "\n";
```

**Task:** Run the file. Read the second line and decide whether `showTip()`'s argument is
still a single string. Then write the Twig expression that fixes it, and the template change
that removes the problem entirely.

**Expected observation:** The escaped output *looks* safe, but after HTML-entity decoding
the payload's `'` is a live quote again and `alert(1)` is a separate statement.

??? tip "Show a hint"
    There are two parsers in a row here: HTML first, JavaScript second. Anything you encode
    as an HTML entity is *decoded again* by the first parser before the second one starts,
    so it protects nothing at the inner layer. Which escaping strategy produces output that
    contains no HTML entities at all?

??? success "Show the solution"
    The second line prints:

    ```
    <div onmouseover="showTip('');alert(1);//')">
    ```

    The `&#039;` produced by `html` escaping is decoded back into `'` by the HTML parser
    before the JavaScript ever runs, so the string closes and `alert(1)` executes.

    The minimal fix is to escape for the *inner* context, whose output contains no HTML
    entities to decode:

    ```twig
    <div onmouseover="showTip('{{ tip|e('js') }}')">…</div>
    ```

    `js` renders `'` as the backslash escape `'`, which contains no HTML entity, so
    HTML decoding leaves it exactly as it is. The JavaScript parser then reads it as an
    escape sequence *inside* the string literal — a character, not a terminator.

    The better fix removes the nesting altogether:

    ```twig
    <div data-tip="{{ tip }}" data-controller="tip">…</div>
    ```

    Now there is exactly one context — an HTML attribute value inside quotes — which is
    precisely what the `html` strategy is documented to handle, and the JavaScript reads the
    value with `element.dataset.tip` in a real `.js` file.

    **Why it works:** OWASP lists `<div onmouseover="'$varUnsafe'">` as a quoted JavaScript
    data value and requires JavaScript encoding for it. The general rule is that each nested
    context needs the escaper of the *innermost* language, applied so that no outer parser
    can undo it — and that the reliable way to get this right is to stop nesting.

    **Certification takeaway:** the escaping strategy is decided **once per template, at
    compile time, from the file name**. Twig does not parse your HTML and will not notice
    that a particular `{{ }}` sits inside an event handler. Nested contexts are always a
    manual decision.

    **Official reference:** https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

## Exercise 3 · Inspect a CSRF token and explain why it changes

**Objective:** Observe that the rendered CSRF token differs on every render while the stored
secret does not, and understand the mechanism.

**Context:** People routinely report "Symfony regenerates my CSRF token on every render" as
a bug. It is not — it is a deliberate mitigation against the BREACH and CRIME compression
side-channel attacks, which need the same ciphertext to repeat.

**Starting point:**

```php
<?php
declare(strict_types=1);

// Reproduction of CsrfTokenManager::randomize()/derandomize().
function randomize(string $value): string
{
    $key = random_bytes(32);
    $masked = $value ^ str_pad('', strlen($value), $key);

    return sprintf(
        '%s.%s.%s',
        substr(hash('xxh128', $key), 0, 1 + (ord($key[0]) % 32)),
        rtrim(strtr(base64_encode($key), '+/', '-_'), '='),
        rtrim(strtr(base64_encode($masked), '+/', '-_'), '='),
    );
}

function derandomize(string $value): string
{
    [, $k, $v] = explode('.', $value);
    $key = base64_decode(strtr($k, '-_', '+/'));
    $masked = base64_decode(strtr($v, '-_', '+/'));

    return $masked ^ str_pad('', strlen($masked), $key);
}

// The stable secret held in the session's token storage.
$stored = 'the-stable-secret-value';

foreach ([1, 2] as $render) {
    $emitted = randomize($stored);
    printf("render %d -> %s\n", $render, $emitted);
    printf("  derandomized: %s (hash_equals: %s)\n\n",
        derandomize($emitted),
        var_export(hash_equals($stored, derandomize($emitted)), true),
    );
}
```

**Task:** Run it twice. Compare the two emitted values, then compare the two de-randomised
values. Explain why submitting either rendered form validates.

**Expected observation:** the emitted strings differ completely — even their first segment
differs in length — yet both de-randomise to the identical stored secret and both pass
`hash_equals()`.

??? tip "Show a hint"
    Look at the three dot-separated segments. One of them is the random key itself, in
    URL-safe base64. If you have the key and the masked value, XOR is its own inverse.

??? success "Show the solution"
    Sample output (yours will differ, that is the point):

    ```
    render 1 -> f.AGte2hjCck-WfC9hxBSYoW7fHFK_MJlHmg03xF2ewUI.dAM792u2Ey36GQISoXfqxBryajPTRfw
      derandomized: the-stable-secret-value (hash_equals: true)

    render 2 -> 4fbd2c84ca360e.rcX28FR1-M-YZ-2978QPvY8TelWAfbyRFnbAjIUULAI.2a2T3ScBma30AsDOiqd92Ps-DDTsCNk
      derandomized: the-stable-secret-value (hash_equals: true)
    ```

    The three segments are `prefix.key.maskedValue`. `getToken()` reads the stable secret
    from the token storage (the session, for stateful tokens), XORs it with 32 fresh random
    bytes and emits the result together with the key. `isTokenValid()` reverses the mask and
    compares with `hash_equals()` — never with `===`.

    Even the *length* of the first segment varies, because it is
    `substr(hash('xxh128', $key), 0, 1 + (ord($key[0]) % 32))` — a random amount of padding
    so that the compressed response size carries no information either.

    **Why it works:** BREACH and CRIME recover secrets by observing how well a response
    compresses when the attacker varies part of it. A secret that is byte-identical in every
    response compresses identically and leaks; a freshly masked one does not. The
    documentation states it directly: "a random mask is prepended to the token and used to
    scramble it".

    **Certification takeaway:** the *stored* token is stable per token ID, the *rendered*
    token is not. Two forms rendered in the same session both validate. An assertion in a
    functional test that compares two rendered token strings is testing the mask, not the
    protection.

    **Official reference:** https://symfony.com/doc/8.0/security/csrf.html

## Exercise 4 · Change one flag and watch a session record survive

**Objective:** See the difference between `Session::migrate()` and `Session::migrate(true)`
on disk, and connect it to `session_fixation_strategy`.

**Context:** Symfony's `MIGRATE` strategy calls `$request->getSession()->migrate(true)` on
authentication. The `true` is not decoration — it decides whether the pre-login session
record is deleted or left lying around with its old id still valid.

**Starting point:**

```php
<?php
declare(strict_types=1);

$dir = __DIR__.'/sess';
@mkdir($dir);
ini_set('session.save_path', $dir);
ini_set('session.use_strict_mode', '1');

$destroyOld = (bool) ($argv[1] ?? false);

session_start();
$_SESSION['user'] = 'ada';
$before = session_id();

// This is what Session::migrate($destroy) ends up calling.
session_regenerate_id($destroyOld);
$after = session_id();

printf("destroy old record : %s\n", var_export($destroyOld, true));
printf("id before          : %s\n", $before);
printf("id after           : %s\n", $after);
printf("attributes kept    : %s\n", var_export($_SESSION['user'] ?? null, true));
session_write_close();

printf("files on disk      : %s\n", implode(', ', array_map(
    'basename',
    glob($dir.'/sess_*') ?: [],
)));
```

**Task:** Run `php file.php` (no argument), note the files listed. Delete the `sess/`
directory, then run `php file.php 1` — the single changed variable. Compare.

**Expected observation:** without the flag, **two** session files exist afterwards; with it,
only **one**.

??? tip "Show a hint"
    A new session id is only half of the defence. Ask what an attacker who already knows the
    *old* id can still do with it while that old record is alive on the server.

??? success "Show the solution"
    ```
    destroy old record : false
    id before          : 2c2430c570db9e7f26954cb2404877a7
    id after           : 9282ae885422f14ae6b56cb6b626d515
    attributes kept    : 'ada'
    files on disk      : sess_2c2430c570db9e7f26954cb2404877a7,
                         sess_9282ae885422f14ae6b56cb6b626d515
    ```

    With `1`:

    ```
    destroy old record : true
    files on disk      : sess_630096bb4f7257f21f21aaa965e90f44
    ```

    In both runs the id changes and `$_SESSION` survives — regeneration keeps the
    attributes. The difference is the orphan record. Left alive, the attacker's planted id
    still resolves to a valid, though now stale, session, and every save handler that
    garbage-collects lazily keeps it for `gc_maxlifetime` seconds.

    Symfony closes that window by default:
    `SessionAuthenticationStrategy::onAuthentication()` calls `migrate(true)` for the
    `MIGRATE` strategy, and additionally clears the CSRF token storage so tokens minted
    before login cannot be replayed after it. The `INVALIDATE` strategy goes further —
    `Session::invalidate()` is literally `clear()` followed by `migrate(true)` — at the cost
    of losing the cart, the locale and the flash bag.

    **Why it works:** fixation is only defeated when the attacker-known id stops being
    usable. A new id plus a surviving old record leaves the attack half-open.

    **Certification takeaway:** three values, one default. `session_fixation_strategy`
    defaults to `MIGRATE` (new id, attributes kept); `INVALIDATE` also drops the attributes;
    `NONE` is documented as "not recommended" and is the vulnerable setting.

    **Official reference:** https://symfony.com/doc/8.0/reference/configuration/security.html#session-fixation-strategy

## Exercise 5 · Diagnose a login bypass, then close it

**Objective:** Watch string concatenation turn a lookup into an authentication bypass, and
verify that binding — not escaping — is what stops it.

**Context:** An in-memory SQLite database with two users. The lookup builds its SQL by
interpolation, which is the single most common way this bug reaches production.

**Starting point:**

```php
<?php
declare(strict_types=1);

$pdo = new PDO('sqlite::memory:', options: [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
]);
$pdo->exec('CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, is_admin INTEGER)');
$pdo->exec("INSERT INTO users (email, is_admin)
            VALUES ('ada@example.com', 0), ('root@example.com', 1)");

function vulnerable(PDO $pdo, string $email): array
{
    $sql = "SELECT id, email, is_admin FROM users WHERE email = '$email'";
    echo "SQL: $sql\n";

    return $pdo->query($sql)->fetchAll(PDO::FETCH_ASSOC);
}

foreach (['ada@example.com', "nobody' OR is_admin = 1 --"] as $input) {
    $rows = vulnerable($pdo, $input);
    echo 'rows: ', count($rows), ' -> ',
        json_encode(array_column($rows, 'email')), "\n\n";
}
```

**Task:** Run it. Read the printed SQL for the second input and say exactly which token the
attacker took control of. Then rewrite `vulnerable()` as `safe()` using a prepared statement
and confirm the second input now returns zero rows.

**Expected observation:** the second input returns the **admin** row even though no such
e-mail exists.

??? tip "Show a hint"
    Look at where the attacker's `'` lands relative to the quotes the code wrote. Once the
    string literal is closed early, everything after it is *query text*, not data — and `--`
    comments out the quote the code was going to append.

??? success "Show the solution"
    ```
    SQL: SELECT id, email, is_admin FROM users WHERE email = 'ada@example.com'
    rows: 1 -> ["ada@example.com"]

    SQL: SELECT id, email, is_admin FROM users WHERE email = 'nobody' OR is_admin = 1 --'
    rows: 1 -> ["root@example.com"]
    ```

    The payload's `'` closes the literal the code opened; `OR is_admin = 1` becomes a new
    boolean term in the `WHERE` clause; `--` turns the trailing `'` into a comment so the
    statement still parses. The attacker did not smuggle *data* — they wrote *syntax*.

    The fix:

    ```php
    <?php
    declare(strict_types=1);

    function safe(PDO $pdo, string $email): array
    {
        $stmt = $pdo->prepare(
            'SELECT id, email, is_admin FROM users WHERE email = :email'
        );
        $stmt->execute(['email' => $email]);

        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
    ```

    ```
    input: ada@example.com                rows: 1
    input: nobody' OR is_admin = 1 --     rows: 0
    ```

    The malicious string is now looked up as a literal e-mail address, which simply does not
    exist.

    **Why it works:** `prepare()` sends the statement text to be parsed *before* any value
    is attached. The parse tree is fixed at that moment, so a bound value can only occupy
    the leaf where its placeholder was. No amount of quoting inside the value can add a node
    to a tree that is already built.

    Note what the fix is **not**: it is not escaping the quote. Escaping is a blocklist that
    has to be right about the character set, the numeric contexts where no quotes exist at
    all, and the identifiers that cannot be parameterised. Binding sidesteps all three.

    The same rule applies one level up in Doctrine: `->where('p.name = :name')` with
    `->setParameter(...)` is safe, and `->where("p.name = '".$name."'")` is this exercise
    again with extra steps — DQL is parsed as a string before it is ever compiled to SQL.

    **Certification takeaway:** the only structural defence is separating query text from
    data. Identifiers (table and column names, `ORDER BY` directions) cannot be bound, so
    they must come from a hard-coded allow-list, never from the request.

    **Official reference:** https://symfony.com/doc/8.0/doctrine.html#doctrine-queries

## Exercise 6 · Meet bcrypt's 72-byte edge and the rehash signal

**Objective:** Reproduce the truncation that lets a *different* passphrase authenticate, and
see the mechanism Symfony uses to detect an out-of-date hash.

**Context:** bcrypt ignores everything after byte 72. With passphrase managers in common
use, that is no longer a theoretical length.

**Starting point:**

```php
<?php
declare(strict_types=1);

$base = str_repeat('a', 72);
$long1 = $base.'ONE';
$long2 = $base.'TWO';

$hash = password_hash($long1, PASSWORD_BCRYPT);

echo 'different passphrase verifies: ',
    var_export(password_verify($long2, $hash), true), "\n";
echo 'hash length                  : ', strlen($hash), "\n";
echo 'hash info                    : ',
    json_encode(password_get_info($hash)), "\n";
echo 'PASSWORD_BCRYPT_DEFAULT_COST : ', PASSWORD_BCRYPT_DEFAULT_COST, "\n";
echo 'needs rehash at cost 13      : ',
    var_export(password_needs_rehash($hash, PASSWORD_BCRYPT, ['cost' => 13]), true),
    "\n";
```

**Task:** Predict the first line, then run the file. Afterwards, explain what
`NativePasswordHasher` does that this raw call does not, and what the last line has to do
with `PasswordUpgraderInterface`.

**Expected observation:** two different passphrases verify against the same hash, and the
default cost is **12** on PHP 8.4.

??? tip "Show a hint"
    Count the bytes the two passphrases share. Then ask how many of them bcrypt actually
    reads. For the last line, ask what would have to happen in your database if the answer
    is `true` for every stored hash.

??? success "Show the solution"
    ```
    different passphrase verifies: true
    hash length                  : 60
    hash info                    : {"algo":"2y","algoName":"bcrypt","options":{"cost":12}}
    PASSWORD_BCRYPT_DEFAULT_COST : 12
    needs rehash at cost 13      : true
    ```

    `password_hash()` with `PASSWORD_BCRYPT` truncates its input at 72 bytes, so `…aaaONE`
    and `…aaaTWO` are the same secret as far as the algorithm is concerned. The hash is 60
    characters and carries the algorithm (`$2y$`), the cost and the salt, which is why
    verification needs no extra storage.

    Symfony does not leave this to chance. `NativePasswordHasher::hash()` contains:

    ```php
    if (\PASSWORD_BCRYPT === $this->algorithm
        && (72 < \strlen($plainPassword)
            || str_contains($plainPassword, "\0"))) {
        $plainPassword = base64_encode(hash('sha512', $plainPassword, true));
    }
    ```

    Every byte of the passphrase now contributes entropy, because the sha512 digest is a
    fixed 88-character base64 string that fits inside the 72-byte window. `verify()` applies
    the same transformation, so old and new hashes both keep working. A second, independent
    guard rejects anything over `PasswordHasherInterface::MAX_PASSWORD_LENGTH` (4096 bytes)
    to stop a multi-megabyte "password" from becoming a CPU denial of service.

    The last line is the migration signal. `password_needs_rehash()` returns `true` whenever
    the stored hash was produced with a different algorithm or weaker options than the ones
    you now want — here, cost 12 versus the cost 13 that `NativePasswordHasher` defaults to.
    Symfony calls the equivalent (`PasswordHasherInterface::needsRehash()`) on every
    successful login and, if it is `true`, rehashes the plaintext it has just verified and
    hands the result to your `PasswordUpgraderInterface::upgradePassword()` implementation.
    Without that implementation, the check still runs and the new hash is simply thrown
    away.

    **Why it works:** the plaintext exists exactly once in the request lifecycle — at
    login — so login is the only moment a rehash is possible. That is why migration is
    gradual and why `migrate_from` must keep verifying old hashes for as long as inactive
    accounts exist.

    **Certification takeaway:** three numbers to keep straight. bcrypt truncates at **72
    bytes**; PHP 8.4 raised the default bcrypt cost to **12**; Symfony's
    `NativePasswordHasher` uses its own default of **13** and rejects passwords longer than
    **4096** bytes.

    **Official reference:** https://www.php.net/manual/en/function.password-hash.php

## Exercise 7 · Expert challenge — build the outbound defences

**Objective:** Assemble the three controls that live at the edge of a response: a
security-header listener, an allow-listed redirect, and a constant-time signature check.

**Context:** Escaping, binding and hashing protect what happens *inside* the app. These three
protect what the browser is told to do afterwards. None of them is enabled by default in
Symfony, which is exactly why they are examinable.

**Starting point:** Write the redirect guard first — it is the only one you can run offline.

```php
<?php
declare(strict_types=1);

function safeRedirectTarget(?string $candidate, string $fallback = '/'): string
{
    // Your implementation here.
    return $fallback;
}

$cases = [
    '/dashboard',
    'https://evil.example/login',
    '//evil.example',
    '/\\evil.example',
    'javascript:alert(1)',
    null,
];

foreach ($cases as $c) {
    printf("%-30s -> %s\n", var_export($c, true), safeRedirectTarget($c));
}
```

**Task:**

1. Implement `safeRedirectTarget()` so that only `/dashboard` survives and every other case
   falls back to `/`.
2. Write a `kernel.response` listener that adds `X-Frame-Options`,
   `X-Content-Type-Options`, `Referrer-Policy`, `Strict-Transport-Security` and a
   `Content-Security-Policy`, and explain why HSTS must be conditional.
3. Replace a `===` signature comparison with a timing-safe one, with the arguments in the
   documented order.

**Expected observation:** `//evil.example` and `/\evil.example` are the two that catch people
out — both start with a slash and both are *protocol-relative* references to another host.

??? tip "Show a hint"
    For (1), think in terms of an allow-list of *shapes*, not a blocklist of bad strings: a
    local path starts with exactly one `/`, contains no `:` that could introduce a scheme,
    and contains no backslash (some browsers normalise `\` to `/` in the authority). For
    (2), ask what `Strict-Transport-Security` on a plain-HTTP development response would do
    to your laptop. For (3), re-read which argument of `hash_equals()` is the secret.

??? success "Show the solution"
    **1. The redirect guard**

    ```php
    <?php
    declare(strict_types=1);

    function safeRedirectTarget(?string $candidate, string $fallback = '/'): string
    {
        if (null === $candidate || '' === $candidate) {
            return $fallback;
        }
        // A local path starts with exactly one slash.
        if (!str_starts_with($candidate, '/')
            || str_starts_with($candidate, '//')) {
            return $fallback;
        }
        // No scheme, and no backslash-based authority.
        if (str_contains($candidate, '\\') || str_contains($candidate, ':')) {
            return $fallback;
        }

        return $candidate;
    }
    ```

    ```
    '/dashboard'                   -> /dashboard
    'https://evil.example/login'   -> /
    '//evil.example'               -> /
    '/\\evil.example'              -> /
    'javascript:alert(1)'          -> /
    NULL                           -> /
    ```

    In a real controller the stronger version never accepts a URL at all: accept a **route
    name** from a hard-coded map and build the URL with `redirectToRoute()`. Then there is
    no string for an attacker to shape.

    **2. The response listener**

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventListener;

    use Symfony\Component\EventDispatcher\Attribute\AsEventListener;
    use Symfony\Component\HttpKernel\Event\ResponseEvent;
    use Symfony\Component\HttpKernel\KernelEvents;

    #[AsEventListener(event: KernelEvents::RESPONSE)]
    final class SecurityHeadersListener
    {
        public function __invoke(ResponseEvent $event): void
        {
            if (!$event->isMainRequest()) {
                return;
            }

            $headers = $event->getResponse()->headers;
            $headers->set('X-Frame-Options', 'DENY');
            $headers->set('X-Content-Type-Options', 'nosniff');
            $headers->set('Referrer-Policy', 'same-origin');
            $headers->set(
                'Content-Security-Policy',
                "default-src 'self'; frame-ancestors 'none'",
            );

            // HSTS is meaningful only on a response the browser
            // received over TLS; sending it over plain HTTP would
            // pin a development host to HTTPS it cannot serve.
            if ($event->getRequest()->isSecure()) {
                $headers->set(
                    'Strict-Transport-Security',
                    'max-age=31536000; includeSubDomains',
                );
            }
        }
    }
    ```

    Two details worth defending in an interview. `isMainRequest()` keeps the headers off
    sub-requests, whose responses are merged into the main one anyway. And `frame-ancestors`
    is what modern browsers honour — the CSP specification says `X-Frame-Options` "MUST be
    ignored" when an enforced `frame-ancestors` is present — so `X-Frame-Options` is kept
    only for old clients, and `ALLOW-FROM` is never an option because it is obsolete.

    `Request::isSecure()` is only trustworthy behind a proxy once `trusted_proxies` is
    configured; otherwise every TLS-terminated request looks like plain HTTP and the HSTS
    header is never sent.

    **3. The signature check**

    ```php
    <?php
    declare(strict_types=1);

    $expected = hash_hmac('sha256', $payload, $secretKey);

    // Wrong: returns as soon as two bytes differ, so the time taken
    // reveals how many leading bytes the guess got right.
    // if ($submitted === $expected) { /* accept */ }

    if (hash_equals($expected, $submitted)) {
        // accept
    }
    ```

    The argument order is part of the contract: the manual states "it is important to
    provide the user-supplied string as the **second** parameter, rather than the first".
    Symfony follows the same rule —
    `CsrfTokenManager::isTokenValid()` calls
    `hash_equals($this->storage->getToken($id), $this->derandomize($token->getValue()))`.

    **Why it works:** each of the three controls removes an assumption the browser would
    otherwise make on your behalf — that any URL you emit is one you meant, that any page
    may be framed, and that a comparison's duration carries no information.

    **Certification takeaway:** Symfony ships XSS, CSRF, SQL-injection and session-fixation
    defences on by default. It ships **no** security headers, **no** redirect validation and
    **no** timing-safe comparison in your own code. Knowing which half of the list is
    automatic is the difference between a correct answer and a plausible one.

    **Official reference:** https://www.php.net/manual/en/function.hash-equals.php

---

<small>Back to the lesson: [Web Security Fundamentals](web-security.md) · Next: [Topic exam](web-security-exam.md)</small>

# Authenticators, Passports & Badges

!!! tip "In a nutshell"
    An authenticator turns a request into a token by building a **Passport** of
    **badges**; it never verifies credentials itself — that happens on
    `CheckPassportEvent`.
    Exam hook: credentials (`PasswordCredentials`) live in `Passport\Credentials`,
    while `UserBadge`/`CsrfTokenBadge`/`RememberMeBadge` live in `Passport\Badge`.

!!! example "Real-world analogy"
    An authenticator is the clerk who assembles your file at the counter. They
    gather your documents into one folder — the **Passport** of **badges** (ID,
    proof of address, a signature) — but verify nothing themselves. A back office
    (`CheckPassportEvent` listeners) checks each document before your pass is
    issued.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Write a custom authenticator implementing the full contract.
    - [ ] Build a `Passport` with the right badges and credentials.
    - [ ] Choose between form/JSON/access-token authenticators.

    **Syllabus:** `Security → Authenticators` ·
    **Level:** Expert ·
    **Est. time:** 40 min ·
    **Prerequisites:** [Authentication](authentication.md) · [Users](users.md) ·
    [Password Hashers](password-hashers.md)

---

## Theory

An **authenticator** turns a request into an authenticated token. In Symfony 8
every authenticator implements
`Symfony\Component\Security\Http\Authenticator\AuthenticatorInterface`:

```php
public function supports(Request $request): ?bool;
public function authenticate(Request $request): Passport;
public function createToken(Passport $passport, string $firewallName): TokenInterface;
public function onAuthenticationSuccess(Request $r, TokenInterface $t, string $fw): ?Response;
public function onAuthenticationFailure(Request $r, AuthenticationException $e): ?Response;
```

`authenticate()` returns a **Passport** — a container of **badges** describing
who the user is and what must be verified. It does **not** verify anything
itself; badge resolution happens on `CheckPassportEvent`.

!!! question "Predict first"
    Your authenticator builds a `Passport` with a `UserBadge` but you forget to
    add the `CsrfTokenBadge` on a form login. What happens on submit?

??? note "Reveal"
    Login *succeeds* with no CSRF protection. Badges are only checked if present —
    there is no implicit CSRF for custom authenticators. The missing
    `CsrfProtectionListener` check means a forged cross-site POST would log the
    victim in. Always add the `CsrfTokenBadge` to state-changing logins.

## Deep Dive — how it works internally

### Passport and badges

A `Symfony\Component\Security\Http\Authenticator\Passport\Passport` bundles:

- a **`UserBadge`** — the identifier + an optional user loader;
- **credentials** — usually `PasswordCredentials` (plaintext to verify) or
  `CustomCredentials` (your own callback);
- optional badges: `CsrfTokenBadge`, `RememberMeBadge`, `PasswordUpgradeBadge`,
  `PreAuthenticatedUserBadge`.

Use `SelfValidatingPassport` when there are **no credentials to check** (e.g. a
valid API token already identifies the user) — it needs only a `UserBadge`.

| Badge (FQCN suffix) | Resolved by | Purpose |
|---|---|---|
| `Badge\UserBadge` | `UserProviderListener` / `CheckCredentialsListener` | Load the user |
| `Credentials\PasswordCredentials` | `CheckCredentialsListener` | Verify password |
| `Credentials\CustomCredentials` | `CheckCredentialsListener` | Verify via callback |
| `Badge\CsrfTokenBadge` | `CsrfProtectionListener` | Validate CSRF token |
| `Badge\RememberMeBadge` | `RememberMeListener` | Enable remember-me cookie |
| `Badge\PasswordUpgradeBadge` | `PasswordMigratingListener` | Rehash on login |

A `Passport` is a **composition** of badges; on `CheckPassportEvent` a dedicated
listener resolves each one before the passport is accepted:

```mermaid
flowchart TD
    P["Passport"] --> UB["UserBadge"]
    P --> CR["PasswordCredentials /<br/>CustomCredentials"]
    P --> CB["CsrfTokenBadge"]
    P --> RB["RememberMeBadge"]
    UB -.resolved by.-> L1["UserProviderListener"]
    CR -.-> L2["CheckCredentialsListener"]
    CB -.-> L3["CsrfProtectionListener"]
    RB -.-> L4["RememberMeListener"]
    L1 & L2 & L3 & L4 --> CPE["CheckPassportEvent:<br/>all resolved → createToken()"]
```

!!! note "Source reference"
    `Symfony\Component\Security\Http\Authenticator\AbstractLoginFormAuthenticator`
    and `Passport` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authenticator/AbstractLoginFormAuthenticator.php).

### The event flow

```mermaid
sequenceDiagram
    participant A as Authenticator
    participant M as AuthenticatorManager
    participant CP as CheckPassportEvent listeners
    A->>M: authenticate() → Passport(badges)
    M->>CP: dispatch CheckPassportEvent
    CP-->>M: badges resolved (user, credentials, csrf…)
    M->>A: createToken(Passport, firewall)
    M->>M: AuthenticationTokenCreatedEvent
    M->>M: LoginSuccessEvent → onAuthenticationSuccess()
    Note over M: on error → LoginFailureEvent → onAuthenticationFailure()
```

An **unresolved** badge is a bug: `Passport::checkIfCompletelyResolved()` throws
if any badge was never marked resolved, ensuring you cannot forget to validate a
credential.

### Built-in authenticators

You rarely write these from scratch — configure them in `security.yaml`:

- **`form_login`** → `FormLoginAuthenticator` (session, CSRF, redirect).
  Subclass `AbstractLoginFormAuthenticator` for a custom form flow; it also
  implements the entry point (redirect to `getLoginUrl()`).
- **`json_login`** → `JsonLoginAuthenticator` (credentials in a JSON body).
- **`access_token`** → `AccessTokenAuthenticator` (bearer token + a
  `token_handler` returning a `UserBadge`; typically a `SelfValidatingPassport`).
- **`http_basic`**, **`login_link`**, **`remember_me`** — configured, not coded.

### `AbstractAuthenticator` and `AbstractLoginFormAuthenticator`

`AbstractAuthenticator` provides a single default: `createToken()` returning a
`PostAuthenticationToken` (subclasses such as `FormLoginAuthenticator` override
it to return a `UsernamePasswordToken`); it does **not** implement
`onAuthenticationFailure()`. `AbstractLoginFormAuthenticator` adds `supports()`
(POST to the check path), the entry point (`start()`) via the abstract
`getLoginUrl()`, and a default `onAuthenticationFailure()` that redirects back to
the login page — you implement `authenticate()`, `getLoginUrl()` and
`onAuthenticationSuccess()`.

### Null behavior

A `UserBadge` can be built with **no user loader** — just the identifier. That
`null` loader is deliberate: it tells the `UserProviderListener` to fall back to
the firewall's configured provider. If you *do* pass a loader and it returns
`null`, the badge stays **unresolved** and `Passport::checkIfCompletelyResolved()`
throws — a missing user surfaces as an `AuthenticationException`, never a silent
`null` user on the token.

```php
new UserBadge($email);                                            // null loader → use the provider
new UserBadge($email, fn (string $id): ?UserInterface => $repo->find($id)); // may be null → error
```

So there is no such thing as a token holding a `null` user coming out of a
successful passport: either the user resolves, or authentication fails.

!!! note "Null in real life"
    A badge with a `null` loader is an application form with only your name on it —
    the clerk looks you up in the directory. If the lookup finds nobody, the
    application is rejected, not stamped blank.

!!! info "Expert note"
    `Passport::checkIfCompletelyResolved()` is your safety net: every badge must
    be marked resolved by *some* `CheckPassportEvent` listener or the passport is
    rejected. That is why adding a badge with no matching listener (e.g. a custom
    badge you never wrote a listener for) fails authentication — silence is not
    success.

??? example "Debugging story"
    **Symptom:** a bespoke SSO authenticator "logged in" but `getUser()` was the
    wrong account under load. **Diagnosis:** `authenticate()` called the identity
    provider *and* resolved the `UserBadge` with a closure that captured a shared
    request-scoped variable, so concurrent requests crossed users. **Fix:** build
    `new UserBadge($identifier)` with a *pure* loader (no captured mutable state),
    letting `UserProviderListener` resolve it on `CheckPassportEvent`. **Avoid:**
    never do identity resolution with shared state inside `authenticate()` — build
    a passport, let the listeners resolve it.

??? abstract "Source-code tour"
    - `Symfony\Component\Security\Http\Authenticator\AuthenticatorInterface` — the
      five-method contract (`supports`/`authenticate`/`createToken`/success/failure).
    - `...\Authenticator\AbstractLoginFormAuthenticator` — adds `supports()`, the
      entry point (`start()`) and a default failure redirect.
    - `...\Authenticator\Passport\Passport` and `SelfValidatingPassport` — badge
      containers; the latter carries only a `UserBadge`.
    - `...\Authenticator\Passport\Badge\UserBadge` +
      `...\EventListener\UserProviderListener` — how the identifier becomes a user.
    - `...\Authenticator\Passport\Credentials\PasswordCredentials` +
      `CheckCredentialsListener` — where the password is actually verified.

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Security;

    use Symfony\Component\HttpFoundation\RedirectResponse;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Generator\UrlGeneratorInterface;
    use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
    use Symfony\Component\Security\Http\Authenticator\AbstractLoginFormAuthenticator;
    use Symfony\Component\Security\Http\Authenticator\Passport\Badge\CsrfTokenBadge;
    use Symfony\Component\Security\Http\Authenticator\Passport\Badge\RememberMeBadge;
    use Symfony\Component\Security\Http\Authenticator\Passport\Badge\UserBadge;
    use Symfony\Component\Security\Http\Authenticator\Passport\Credentials\PasswordCredentials;
    use Symfony\Component\Security\Http\Authenticator\Passport\Passport;

    final class LoginFormAuthenticator extends AbstractLoginFormAuthenticator
    {
        public function __construct(private readonly UrlGeneratorInterface $urls) {}

        public function authenticate(Request $request): Passport
        {
            $email = (string) $request->request->get('email', '');

            return new Passport(
                new UserBadge($email),                                   // load the user
                new PasswordCredentials((string) $request->request->get('password', '')),
                [
                    new CsrfTokenBadge('authenticate', (string) $request->request->get('_csrf_token')),
                    new RememberMeBadge(),
                ],
            );
        }

        protected function getLoginUrl(Request $request): string
        {
            return $this->urls->generate('app_login');
        }

        public function onAuthenticationSuccess(Request $r, TokenInterface $t, string $fw): ?Response
        {
            return new RedirectResponse($this->urls->generate('dashboard'));
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/packages/security.yaml
    security:
        firewalls:
            main:
                lazy: true
                provider: app_users
                custom_authenticators:
                    - App\Security\LoginFormAuthenticator
                remember_me:
                    secret: '%kernel.secret%'
                    lifetime: 604800
            api:
                pattern: ^/api
                stateless: true
                access_token:
                    token_handler: App\Security\AccessTokenHandler
    ```

=== "Access token handler"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Security;

    use Symfony\Component\Security\Core\Exception\BadCredentialsException;
    use Symfony\Component\Security\Http\AccessToken\AccessTokenHandlerInterface;
    use Symfony\Component\Security\Http\Authenticator\Passport\Badge\UserBadge;

    final class AccessTokenHandler implements AccessTokenHandlerInterface
    {
        public function __construct(private readonly TokenRepository $tokens) {}

        public function getUserBadgeFrom(string $accessToken): UserBadge
        {
            $token = $this->tokens->findValid($accessToken)
                ?? throw new BadCredentialsException('Invalid token.');

            return new UserBadge($token->getUserIdentifier());
        }
    }
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Add `PasswordCredentials`, let the listener verify | Calling `verify()` in `authenticate()` |
| `SelfValidatingPassport` for token APIs | Adding empty `PasswordCredentials` |
| Subclass `AbstractLoginFormAuthenticator` | Reimplementing form login by hand |
| Add `CsrfTokenBadge` to form logins | Skipping CSRF on state-changing logins |

## When (not) to use it / alternatives

Prefer built-in `form_login`/`json_login`/`access_token` — write a custom
authenticator only for a genuinely custom flow (e.g. a bespoke SSO handshake).
For stateless APIs, `access_token` + a `token_handler` covers most needs without
a full authenticator.

!!! danger "Certification traps"
    - `authenticate()` **builds** the Passport; it never verifies credentials —
      that is `CheckPassportEvent`.
    - `PasswordCredentials` lives in the **`Credentials`** namespace;
      `CsrfTokenBadge`/`RememberMeBadge`/`UserBadge` live in **`Badge`**.
    - Use **`SelfValidatingPassport`** when there is no password to check;
      a plain `Passport` requires credentials.
    - An unresolved badge causes a **failure** — the passport must be fully
      resolved.
    - Two entry-point authenticators need an explicit `entry_point:`.

!!! warning "Common mistakes"
    - Returning `true` from `supports()` for every request, hijacking unrelated
      routes.
    - Forgetting the `CsrfTokenBadge` on a form login, then wondering why CSRF is
      not enforced.

## Exercises

1. **(Advanced)** Build a `Passport` for a login form with CSRF and remember-me.
2. **(Expert)** Explain why an access-token flow uses `SelfValidatingPassport`.

??? success "Solutions"

    **1.** See `LoginFormAuthenticator::authenticate()` above — `UserBadge` +
    `PasswordCredentials` + `[CsrfTokenBadge, RememberMeBadge]`.

    **2.** A valid bearer token already proves identity; there is no password to
    verify. `SelfValidatingPassport` carries only the `UserBadge`, so the
    `CheckCredentialsListener` has nothing to check and the passport resolves
    with just user loading.

## Certification questions

??? question "Q1. What does `authenticate()` return?"
    - [ ] A. A `TokenInterface`
    - [x] B. A `Passport` ✅
    - [ ] C. A `Response`
    - [ ] D. A `UserInterface`

    **Why:** `authenticate()` builds a Passport; the token is produced later by
    `createToken()`.
    **Ref:** [Custom authenticator](https://symfony.com/doc/current/security/custom_authenticator.html).

??? question "Q2. Which passport suits a valid-API-token flow with no password?"
    - [ ] A. `Passport` with empty `PasswordCredentials`
    - [x] B. `SelfValidatingPassport` with a `UserBadge` ✅
    - [ ] C. `PreAuthenticatedToken`
    - [ ] D. `UsernamePasswordToken`

    **Why:** No credential to verify ⇒ self-validating passport carrying only the
    user badge.
    **Ref:** [Passport](https://symfony.com/doc/current/security/custom_authenticator.html#the-passport).

??? question "Q3. In which namespace is `PasswordCredentials`?"
    - [ ] A. `…\Passport\Badge`
    - [x] B. `…\Passport\Credentials` ✅
    - [ ] C. `…\Token`
    - [ ] D. `…\EntryPoint`

    **Why:** Credentials (`PasswordCredentials`, `CustomCredentials`) live under
    `Passport\Credentials`; other badges under `Passport\Badge`.
    **Ref:** [Security source](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport).

## Key takeaways

- Contract: `supports` / `authenticate` (Passport) / `createToken` /
  `onAuthenticationSuccess` / `onAuthenticationFailure`.
- Passport = `UserBadge` + credentials + optional badges; validated on `CheckPassportEvent`.
- `SelfValidatingPassport` for credential-less flows (API tokens).
- Prefer built-in `form_login`/`json_login`/`access_token`; subclass
  `AbstractLoginFormAuthenticator` for custom forms.

## Last-minute revision

!!! tip "Cheat sheet"
    - Badges: `UserBadge`, `CsrfTokenBadge`, `RememberMeBadge`,
      `PasswordUpgradeBadge`, `PreAuthenticatedUserBadge` (in `Badge`).
    - Credentials: `PasswordCredentials`, `CustomCredentials` (in `Credentials`).
    - `authenticate()` builds; `CheckPassportEvent` verifies.
    - `access_token` needs a `token_handler` → `UserBadge`.

## Connections

- **Depends on:** [Authentication](authentication.md) — the `AuthenticatorManager`
  flow that invokes this contract.
- **Depends on:** [Event Dispatcher](../architecture/events.md) — badges are
  resolved by listeners on `CheckPassportEvent`.
- **Reused in:** [Password Hashers](password-hashers.md) — the `PasswordCredentials`
  badge is verified with the configured hasher.
- **Confused with:** [Providers](providers.md) — the authenticator *builds* the
  passport; the provider only *loads* the user behind the `UserBadge`.

## Official References
- [Symfony docs — Custom authenticator](https://symfony.com/doc/current/security/custom_authenticator.html)
- [Symfony docs — Access token authentication](https://symfony.com/doc/current/security/access_token.html)
- [Symfony source — Passport](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony security" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/security/custom_authenticator.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** `authenticate()` only builds a Passport and verifies nothing
- [ ] implement a custom authenticator with the right badges in Symfony 8
- [ ] debug an "unresolved badge" / missing-CSRF failure
- [ ] spot when `SelfValidatingPassport` is correct vs a plain `Passport`
- [ ] name which listener resolves each badge on `CheckPassportEvent`

---

<small>Related: [Authentication](authentication.md) · [Users](users.md) ·
[Password Hashers](password-hashers.md) · [Firewalls](firewalls.md)</small>

# Password Hashers

!!! tip "In a nutshell"
    Passwords are stored as slow, salted one-way hashes; you configure hashers per
    user class and never verify them by hand.
    Exam hook: use `auto` (currently bcrypt) as the default, and transparent rehash
    needs **both** `migrate_from` *and* a `PasswordUpgraderInterface` provider.

!!! example "Real-world analogy"
    A password hasher is a one-way shredder. You never keep the original slip —
    only its unique shredded pattern. When someone claims a password, you shred
    their attempt the same way and compare patterns (`verify()`). A better
    shredder arrives? `needsRehash()` re-shreds the slip next time they sign in.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Configure `auto`/`bcrypt`/`sodium` hashers and explain the defaults.
    - [ ] Implement transparent rehash via `migrate_from` + `needsRehash()`.
    - [ ] Use `PasswordHasherFactory`/`UserPasswordHasherInterface` correctly.

    **Syllabus:** `Security → Password hashers` ·
    **Level:** Expert ·
    **Est. time:** 30 min ·
    **Prerequisites:** [Users](users.md) · [Configuration](configuration.md)

---

## Theory

Passwords are never stored in plaintext — they are **hashed** with a slow,
salted, one-way function. Symfony's PasswordHasher component wraps PHP's
`password_hash()` and libsodium behind
`Symfony\Component\PasswordHasher\PasswordHasherInterface`
(`hash()`, `verify()`, `needsRehash()`).

```php
// PasswordHasherInterface — wraps password_hash() / libsodium
$hash = $hasher->hash('S3cr3t!');    // hash(): slow, salted, one-way
$hasher->verify($hash, 'S3cr3t!');   // verify(): true on match
$hasher->needsRehash($hash);         // needsRehash(): true after an algo/cost bump
```

| Algorithm | Backed by | Note |
|---|---|---|
| `auto` | best available | **Default & recommended**; currently bcrypt |
| `bcrypt` | `password_hash(PASSWORD_BCRYPT)` | `cost` 4–31; 72-byte input limit |
| `sodium` | libsodium Argon2id | memory-hard; `memory_cost`/`time_cost` |
| `pbkdf2` | `hash_pbkdf2` | legacy interop |
| `plaintext` | none | **tests only — never production** |

!!! question "Predict first"
    You set `migrate_from: ['bcrypt']` but your provider does not implement
    `PasswordUpgraderInterface`. Do legacy hashes get upgraded on login?

??? note "Reveal"
    No. The new hash is *computed* (because `needsRehash()` is true) but there is
    nowhere to persist it — transparent rehash needs **both** `migrate_from` *and*
    a `PasswordUpgraderInterface` provider that the `PasswordMigratingListener`
    calls.

## Deep Dive — how it works internally

### Factory and per-class hashers

`security.yaml`'s `password_hashers` map compiles into a
`Symfony\Component\PasswordHasher\Hasher\PasswordHasherFactory`. Keyed by
**user class/interface**, it returns the right `PasswordHasherInterface` for a
given user. Controllers use the higher-level
`Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface`
(`hashPassword(user, plain)`, `isPasswordValid(user, plain)`,
`needsRehash(user)`), which asks the factory for the user's hasher.

```mermaid
flowchart LR
    C[Controller] --> UPH[UserPasswordHasherInterface]
    UPH --> F[PasswordHasherFactory]
    F -->|by user class| H[PasswordHasherInterface: bcrypt/sodium]
```

!!! note "Source reference"
    `Symfony\Component\PasswordHasher\Hasher\PasswordHasherFactory` and
    `UserPasswordHasher` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/PasswordHasher/Hasher/PasswordHasherFactory.php).

### Verification during login

You do **not** verify passwords by hand. The authenticator adds a
`PasswordCredentials` badge (the plaintext); on `CheckPassportEvent` the
`CheckCredentialsListener` calls the hasher's `verify($hash, $plain)`. See
[Authenticators, Passports & Badges](authenticators.md).

```php
// Authenticator: hand over the plaintext via a badge — never verify it yourself
return new Passport(
    new UserBadge($email),
    new PasswordCredentials($plaintextPassword)
);
// Then, on CheckPassportEvent, CheckCredentialsListener runs:
// $hasher->verify($user->getPassword(), $plaintextPassword)
```

### Migration & rehash (`needsRehash`)

Algorithms and costs improve over time. `migrate_from` lets you accept old
hashes while upgrading them on the next successful login:

1. Configure the new algorithm with `migrate_from: [old_algo]`.
2. On login, if `PasswordHasherInterface::needsRehash()` returns `true`, the
   `PasswordMigratingListener` (triggered by the **`PasswordUpgradeBadge`**)
   rehashes the plaintext and calls
   `PasswordUpgraderInterface::upgradePassword()` on the provider to persist it.

```php
// security.yaml: App\Security\AppUser: { algorithm: sodium, migrate_from: ['bcrypt'] }
final class UserRepository implements PasswordUpgraderInterface
{
    // Called by PasswordMigratingListener (via the PasswordUpgradeBadge)
    // when needsRehash() returned true for the legacy hash
    public function upgradePassword(PasswordAuthenticatedUserInterface $user, string $newHashedPassword): void
    {
        $user->setPassword($newHashedPassword); // persist the new sodium hash
    }
}
```

This is transparent to the user — no password reset needed.

### Null behavior

`PasswordAuthenticatedUserInterface::getPassword()` is typed **`?string`**, so a
user may legitimately have **`null`** as their stored hash (passwordless / SSO /
token-only accounts). The `CheckCredentialsListener` guards for this: a `null`
hash means "no password on file", so verification **fails cleanly** instead of
calling `verify()` against nothing, and `needsRehash()` short-circuits when there
is no hash to inspect.

```php
// PasswordAuthenticatedUserInterface::getPassword() is typed ?string
public function getPassword(): ?string
{
    return $this->passwordHash; // null = passwordless / SSO / token-only account
}
// CheckCredentialsListener: a null hash fails cleanly — verify() is never
// called against nothing, and needsRehash() is skipped
```

Never feed a `null` (or empty) plaintext into `hashPassword()` expecting a
"blank" account — hash a real secret, or leave the field `null` and let the login
fail. Treat `getPassword()` as `?string` at every call site.

!!! note "Null in real life"
    A `null` hash is a lock with no key cut for it yet: you cannot test a key
    against it, so that door just will not open by key.

## Configuration & code

=== "YAML"

    ```yaml
    # config/packages/security.yaml
    security:
        password_hashers:
            # Recommended: let Symfony pick + auto-rehash on cost bumps.
            Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface: 'auto'

            # Explicit example with migration from a legacy algo.
            App\Security\AppUser:
                algorithm: sodium
                migrate_from: ['bcrypt']
    ```

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use App\Security\AppUser;
    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
    use Symfony\Component\Routing\Attribute\Route;

    final class RegistrationController extends AbstractController
    {
        #[Route('/register', name: 'register', methods: ['POST'])]
        public function register(UserPasswordHasherInterface $hasher): Response
        {
            $user = new AppUser('jane@example.com', '');
            $hashed = $hasher->hashPassword($user, 'plaintext-from-form');
            // persist $hashed via your store (Doctrine is out of scope here)

            return new Response('created', Response::HTTP_CREATED);
        }
    }
    ```

=== "Console"

    ```console
    $ php bin/console security:hash-password
     Type in your password to be hashed: ******
     $2y$13$Q0m...   # bcrypt hash for security.yaml / fixtures
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Use `auto` in production | Hard-coding a fixed cost with no `migrate_from` |
| `migrate_from` to upgrade legacy hashes | Forcing mass password resets |
| `plaintext` only in test env config | `plaintext` anywhere near production |
| Let `CheckCredentialsListener` verify | Calling `password_verify()` manually |

## When (not) to use it / alternatives

Always hash. Use `auto` unless a compliance rule mandates a specific algorithm;
use `sodium` (Argon2id) when you want memory-hard hashing. `plaintext` exists to
keep test fixtures fast — never ship it. For tokens/API keys, hash them too, but
verification usually lives in a `token_handler`, not the password hasher.

!!! danger "Certification traps"
    - `auto` is the **default and recommended** algorithm; it currently maps to
      bcrypt but may change — that is the point.
    - Rehash needs **both** `migrate_from` *and* a provider implementing
      `PasswordUpgraderInterface`; the `PasswordUpgradeBadge` triggers it.
    - `plaintext` is **test-only**; the exam flags it as a production anti-pattern.
    - bcrypt truncates input at **72 bytes** — very long passphrases lose entropy
      (sodium does not).

!!! warning "Common mistakes"
    - Verifying passwords manually in the authenticator instead of adding a
      `PasswordCredentials` badge.
    - Expecting rehash to work without a `PasswordUpgraderInterface` provider —
      the new hash is computed but never persisted.

## Exercises

1. **(Advanced)** Configure `sodium` for `AppUser` while still accepting existing
   `bcrypt` hashes.
2. **(Expert)** Describe the exact chain that rehashes a legacy password on login.

??? success "Solutions"

    **1.** See the `App\Security\AppUser` block:
    `algorithm: sodium`, `migrate_from: ['bcrypt']`.

    **2.** Authenticator adds `PasswordCredentials` + `PasswordUpgradeBadge` →
    `CheckCredentialsListener` verifies against the old bcrypt hash → since the
    configured algo is sodium, `needsRehash()` is `true` →
    `PasswordMigratingListener` rehashes the plaintext with sodium and calls the
    provider's `upgradePassword()` to persist it.

## Certification questions

??? question "Q1. Which algorithm is the recommended default?"
    - [x] A. `auto` ✅
    - [ ] B. `plaintext`
    - [ ] C. `md5`
    - [ ] D. `pbkdf2`

    **Why:** `auto` selects the best available algorithm and adapts over time.
    **Ref:** [Passwords](https://symfony.com/doc/8.0/security/passwords.html).

??? question "Q2. Transparent rehash on login requires…"
    - [ ] A. Only `migrate_from`
    - [ ] B. Only a `PasswordUpgraderInterface` provider
    - [x] C. Both `migrate_from` and a `PasswordUpgraderInterface` provider ✅
    - [ ] D. Calling `password_hash()` yourself

    **Why:** `migrate_from` detects the old hash; the upgrader persists the new
    one via the `PasswordUpgradeBadge` flow.
    **Ref:** [Password migration](https://symfony.com/doc/8.0/security/passwords.html#password-migration).

??? question "Q3. Where is a login password actually verified?"
    - [ ] A. In `getPassword()`
    - [ ] B. In the user provider
    - [x] C. In `CheckCredentialsListener` on `CheckPassportEvent` ✅
    - [ ] D. In the controller

    **Why:** The `PasswordCredentials` badge is checked by the listener using the
    hasher's `verify()`.
    **Ref:** [Custom authenticator](https://symfony.com/doc/8.0/security/custom_authenticator.html).

## Key takeaways

- `auto` (recommended), `bcrypt`, `sodium`; `plaintext` for tests only.
- `PasswordHasherFactory` picks the hasher per user class;
  `UserPasswordHasherInterface` is the app-facing API.
- Rehash = `migrate_from` + `PasswordUpgraderInterface` + `PasswordUpgradeBadge`.
- Never verify passwords manually — use the `PasswordCredentials` badge.

## Last-minute revision

!!! tip "Cheat sheet"
    - `password_hashers: PasswordAuthenticatedUserInterface: 'auto'`.
    - `hashPassword()` / `isPasswordValid()` / `needsRehash()`.
    - Rehash triggered by `PasswordUpgradeBadge` → `PasswordMigratingListener`.
    - bcrypt: 72-byte limit; sodium: Argon2id, memory-hard.

## Connections

- **Depends on:** [Users](users.md) — hashers key off the user class and its
  `getPassword(): ?string`.
- **Reused in:** [Authenticators](authenticators.md) — the `PasswordCredentials`
  badge is verified with the configured hasher.
- **Reused in:** [Providers](providers.md) — a `PasswordUpgraderInterface`
  provider persists rehashed passwords.
- **Confused with:** [Configuration](configuration.md) — `password_hashers` is
  keyed by user class, not by provider or firewall name.

## Official References
- [Symfony docs — Passwords](https://symfony.com/doc/8.0/security/passwords.html)
- [Symfony source — PasswordHasherFactory](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/PasswordHasher/Hasher/PasswordHasherFactory.php)
- [Symfony source — UserPasswordHasher](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/PasswordHasher/Hasher/UserPasswordHasher.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony security" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/security/passwords.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** passwords are slow, salted, one-way hashes
- [ ] configure `auto`/`sodium` with `migrate_from` in Symfony 8
- [ ] debug rehash that computes but never persists (missing upgrader)
- [ ] spot that `plaintext` is a production anti-pattern and bcrypt's 72-byte limit
- [ ] trace verification to `CheckCredentialsListener` on `CheckPassportEvent`

---

<small>Related: [Users](users.md) · [Providers](providers.md) ·
[Authenticators, Passports & Badges](authenticators.md) · [Configuration](configuration.md)</small>

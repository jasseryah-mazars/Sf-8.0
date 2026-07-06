# Revision Sheet — Security

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Security](../../security/index.md).

## Access Control Rules
- `access_control` = URL-based authorization, first match wins.
- Matchers: path/host/port/ip(s)/methods; requirements: roles/allow_if/requires_channel.
- It runs through the same `AccessDecisionManager`/voters as `isGranted()`.
- No subject support and no match ⇒ allowed; use voters for per-object rules.

**Cheat:** First match wins → specific first, `^/` catch-all last. Roles in a rule = OR; `roles` + `allow_if` = AND. `requires_channel: https` = pre-auth redirect. `ips` + `PUBLIC_ACCESS` = LAN allowlist; no match = allowed.

## Authentication
- Symfony 8 has one auth system: authenticators + passports + badges + token.
- Flow: `supports` → `authenticate` (Passport) → `CheckPassportEvent` →
  `createToken` → `AuthenticationTokenCreatedEvent` → store → `LoginSuccessEvent`.
- Stateful = session-backed token restored via `ContextListener`; stateless =
  re-auth per request.
- The entry point decides how to *start* auth for anonymous users.

**Cheat:** Firewall = `kernel.request` listener → `AuthenticatorManager`. Events: `CheckPassportEvent`, `AuthenticationTokenCreatedEvent`, `LoginSuccessEvent`, `LoginFailureEvent`. `TokenInterface` in `TokenStorageInterface` = "logged in". `stateless: true` ⇒ no `ContextListener`, no session token.

## Authenticators, Passports & Badges
- Contract: `supports` / `authenticate` (Passport) / `createToken` /
  `onAuthenticationSuccess` / `onAuthenticationFailure`.
- Passport = `UserBadge` + credentials + optional badges; validated on `CheckPassportEvent`.
- `SelfValidatingPassport` for credential-less flows (API tokens).
- Prefer built-in `form_login`/`json_login`/`access_token`; subclass
  `AbstractLoginFormAuthenticator` for custom forms.

**Cheat:** Badges: `UserBadge`, `CsrfTokenBadge`, `RememberMeBadge`, `PasswordUpgradeBadge`, `PreAuthenticatedUserBadge` (in `Badge`). Credentials: `PasswordCredentials`, `CustomCredentials` (in `Credentials`). `authenticate()` builds; `CheckPassportEvent` verifies. `access_token` needs a `token_handler` → `UserBadge`.

## Authorization
- Authorization = "is this token granted attribute A on subject S?".
- Path: `isGranted()` → `AuthorizationChecker` → `AccessDecisionManager` → voters.
- Enforce via `#[IsGranted]`, `denyAccessUnlessGranted()`, or `access_control`.
- Only the imperative/attribute path carries a subject; use voters for per-object rules.

**Cheat:** `#[IsGranted('ROLE_X')]` / `#[IsGranted('PERM', subject: 'x')]`. `denyAccessUnlessGranted($attr, $subject)` → `AccessDeniedException` → 403. Twig: `is_granted(attr, subject)`. Voter votes: GRANTED 1 / ABSTAIN 0 / DENIED -1.

## Configuration (security.yaml)
- Five keys: `providers`, `firewalls`, `access_control`, `password_hashers`,
  `role_hierarchy`.
- `SecurityExtension` compiles the config into a `FirewallMap` + per-firewall services.
- Firewalls and `access_control` are first-match, top-to-bottom.
- Symfony 8 removed `enable_authenticator_manager` and legacy auth keys.

**Cheat:** `dev` firewall (`security: false`) first; catch-all `main` last. `password_hashers: PasswordAuthenticatedUserInterface: 'auto'`. Multiple providers ⇒ each firewall needs `provider:`. `debug:config security`, `debug:firewall`, `security:hash-password`.

## Firewalls
- One firewall per request: first matcher wins (order specific → general).
- Match on `pattern`/`host`/`methods`/`request_matcher`.
- `dev` firewall + `security: false` first; protects the profiler/assets.
- `lazy` defers auth; `stateless` skips the session; `context` shares tokens.

**Cheat:** Firewall = authentication zone; `access_control` = authorization. First match wins — `dev`/`security: false` first, catch-all last. `lazy: true` = auth on token read; `stateless: true` = no session token. Same `context:` ⇒ shared login.

## Password Hashers
- `auto` (recommended), `bcrypt`, `sodium`; `plaintext` for tests only.
- `PasswordHasherFactory` picks the hasher per user class;
  `UserPasswordHasherInterface` is the app-facing API.
- Rehash = `migrate_from` + `PasswordUpgraderInterface` + `PasswordUpgradeBadge`.
- Never verify passwords manually — use the `PasswordCredentials` badge.

**Cheat:** `password_hashers: PasswordAuthenticatedUserInterface: 'auto'`. `hashPassword()` / `isPasswordValid()` / `needsRehash()`. Rehash triggered by `PasswordUpgradeBadge` → `PasswordMigratingListener`. bcrypt: 72-byte limit; sodium: Argon2id, memory-hard.

## User Providers
- A provider **loads and refreshes** users; it never authenticates them.
- `loadUserByIdentifier()`, `refreshUser()`, `supportsClass()` are the contract.
- `refreshUser()` runs every stateful request; keep it cheap and current.
- Memory/chain/custom providers cover non-Doctrine needs (entity is out of scope).

**Cheat:** Contract: `loadUserByIdentifier` / `refreshUser` / `supportsClass`. Add `PasswordUpgraderInterface` for transparent rehash. `memory` for tests; `chain` tries providers in order. Stateless firewall ⇒ no `refreshUser()`.

## Roles
- Roles are `ROLE_`-prefixed strings from `getRoles()`, expanded by the hierarchy.
- `RoleHierarchyVoter` expands reachable roles before checking membership.
- `IS_AUTHENTICATED_*`/`PUBLIC_ACCESS` are `AuthenticatedVoter` attributes, not roles.
- `_REMEMBERED` ⊇ `_FULLY`; no more `ANONYMOUSLY` in Symfony 8.

**Cheat:** `ROLE_` prefix required for `RoleVoter`. Hierarchy is downward: `ROLE_ADMIN: [ROLE_USER]`. `PUBLIC_ACCESS` = everyone; `IS_AUTHENTICATED_FULLY` = strict; `_REMEMBERED` = looser. `IS_IMPERSONATOR` on a `SwitchUserToken`.

## Users
- `UserInterface` in 8.0 = `getRoles()` + `getUserIdentifier()` only.
- `getUserIdentifier()` must be stable and unique; it drives `refreshUser()`.
- `eraseCredentials()` removed — strip secrets in `__serialize()`.
- `EquatableInterface::isEqualTo()` can force re-login on identity change.

**Cheat:** Two methods: `getRoles()`, `getUserIdentifier()`. Password ⇒ `PasswordAuthenticatedUserInterface::getPassword()`. No `eraseCredentials()` in 8.0 → use `__serialize()`. `isEqualTo() === false` on refresh ⇒ logout.

## Voters & Voting Strategies
- A voter votes GRANTED/DENIED/ABSTAIN on an attribute + optional subject.
- Extend `Voter`; `supports()` filters, `voteOnAttribute()` decides.
- Strategies: affirmative (default), consensus, unanimous, priority.
- Abstain ≠ deny; all-abstain denies unless `allow_if_all_abstain: true`.

**Cheat:** Constants: GRANTED 1 / ABSTAIN 0 / DENIED -1. `supports()` false ⇒ abstain. Strategy config: `security.access_decision_manager.strategy`. Voters autoconfigured via `security.voter` tag.

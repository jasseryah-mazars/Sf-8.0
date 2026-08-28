# Revision Sheet — Security

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Security](../../security/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Une **fiche imprimable, tenant sur une page**, qui résume chaque sous-chapitre de Security en quelques puces "à retenir" suivies d'une ligne "Cheat" très dense.

**Pourquoi ça existe ?** Dans les derniers jours avant l'examen, on veut un support papier ou PDF unique par domaine — pas 10 onglets de navigateur ouverts. Cette fiche condense un domaine entier sur une seule page imprimable.

**🏠 Analogie de la vraie vie :** C'est la **fiche de révision recto-verso** qu'un étudiant prépare avant un examen universitaire : tout le cours du semestre réduit à une page, à relire dans le métro le matin de l'épreuve.

**Symfony dans la vraie vie :** Chaque puce "à retenir" → une règle déjà apprise en détail dans le chapitre / La ligne "Cheat:" → la version ultra-compacte, presque un aide-mémoire de syntaxe / Lien "Full detail" → retour au chapitre complet si un point ne "sonne" plus familier.

**⚠️ Erreur fréquente :** Imprimer cette fiche *avant* d'avoir étudié Security en détail, en espérant apprendre directement dessus — le format est trop dense pour un premier apprentissage, il ne fonctionne qu'en rappel.

**🧠 Comment le mémoriser :** *« Une page, un domaine, la veille de l'examen »* — cette fiche est le tout dernier support à consulter, pas le premier.

## Access Control Rules
- `access_control` = URL-based authorization, first match wins.
- Matchers: path/host/port/ip(s)/methods; requirements: roles/allow_if/requires_channel.
- It runs through the same `AccessDecisionManager`/voters as `isGranted()`.
- No subject support and no match ⇒ allowed; use voters for per-object rules.

**Cheat:** First match wins → specific first, `^/` catch-all last. Roles in a rule = OR; `roles` + `allow_if` = AND. `requires_channel: https` = pre-auth redirect. `ips` + `PUBLIC_ACCESS` = LAN allowlist; no match = allowed.

## Access Decision Strategies
- Four strategies: affirmative (default, one grant wins), consensus
  (majority + tie flag), unanimous (any deny vetoes), priority (first
  non-abstain decides).
- Abstain is neutral in every strategy; all-abstain denies unless
  `allow_if_all_abstain: true`.
- Consensus ties default to **granted** (`allow_if_equal_granted_denied: true`).
- Configure globally at `security.access_decision_manager`; custom logic via
  `strategy_service` implementing `AccessDecisionStrategyInterface`.
- Votes are `VoterInterface::ACCESS_GRANTED/ABSTAIN/DENIED` = 1 / 0 / -1.

**Cheat:** affirmative: ∃ grant ⇒ ✔ · consensus: grants > denies (tie ⇒ flag, default ✔) unanimous: no deny ∧ ≥1 grant ⇒ ✔ · priority: first non-abstain decides all abstain ⇒ `allow_if_all_abstain` (default ✘) Config: `security.access_decision_manager.{strategy, strategy_service, service}`

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

## User Impersonation (switch_user)
- `switch_user` is per-firewall; defaults: role `ROLE_ALLOWED_TO_SWITCH`,
  parameter `_switch_user`, exit value `_exit`.
- The active token becomes a `SwitchUserToken` carrying the target user **and**
  the original token.
- Detect impersonation with `IS_IMPERSONATOR` (not the legacy
  `ROLE_PREVIOUS_ADMIN`).
- `SwitchUserEvent` fires on switch *and* exit — the hook for auditing, vetoing
  and custom target resolution.
- All authorization while switched uses the **target** user's roles.

**Cheat:** Enable: `switch_user: true` (or `{ role: ..., parameter: ... }`). Switch: `?_switch_user=identifier` · Exit: `?_switch_user=_exit`. Check: `is_granted('IS_IMPERSONATOR')`. Internals: `SwitchUserListener` → `SwitchUserToken(originalToken)`. Event: `SwitchUserEvent` (audit / restrict / custom lookup).

## Login Throttling & Rate Limiting
- `login_throttling: { max_attempts, interval }` on the firewall; requires
  **symfony/rate-limiter**.
- Defaults: `max_attempts: 5`, interval `'1 minute'`; counters are
  username+IP **and** IP alone at 5×.
- Implemented by `LoginThrottlingListener` on `CheckPassportEvent`; success
  resets the counter.
- Custom behaviour = a `RequestRateLimiterInterface` service via the `limiter`
  option (extend `AbstractRequestRateLimiter`).
- RateLimiter policies (fixed/sliding window, token bucket) power any custom
  limiter you define under `framework.rate_limiter`.

**Cheat:** Config: `login_throttling: { max_attempts: N, interval: '15 minutes' }`. Dual default limits: user+IP = N · IP alone = 5N. Hook: `CheckPassportEvent` (blocks **before** credential checks). Custom: `limiter:` → `RequestRateLimiterInterface` service. Needs: `composer require symfony/rate-limiter`.

## Password Hashers
- `auto` (recommended), `bcrypt`, `sodium`; `plaintext` for tests only.
- `PasswordHasherFactory` picks the hasher per user class;
  `UserPasswordHasherInterface` is the app-facing API.
- Rehash = `migrate_from` + `PasswordUpgraderInterface` + `PasswordUpgradeBadge`.
- Never verify passwords manually — use the `PasswordCredentials` badge.

**Cheat:** `password_hashers: PasswordAuthenticatedUserInterface: 'auto'`. `hashPassword()` / `isPasswordValid()` / `needsRehash()`. Rehash triggered by `PasswordUpgradeBadge` → `PasswordMigratingListener`. bcrypt: 72-byte limit; sodium: Argon2id, memory-hard.

## Programmatic Login & Logout
- `Security::login($user, ?$authenticatorName, ?$firewallName, $badges)` —
  programmatic authentication through the real pipeline.
- Authenticator name required with multiple authenticators; firewall name when
  targeting a firewall other than the current one.
- Badges (e.g. `RememberMeBadge`) make the login behave like its interactive
  twin; the same events are dispatched.
- `logout($validateCsrf = true)` dispatches `LogoutEvent`; disable CSRF checks
  only for non-form flows.
- Tests use `KernelBrowser::loginUser()` instead — different tool, different
  layer.

**Cheat:** Service: `Symfony\Bundle\SecurityBundle\Security`. `login(user, 'form_login', 'main', [new RememberMeBadge()])` → `?Response`. Multiple authenticators ⇒ name one; built-ins by config key. `logout(false)` ⇒ skip CSRF validation. Same events as interactive login · tests ⇒ `loginUser()`.

## User Providers
- A provider **loads and refreshes** users; it never authenticates them.
- `loadUserByIdentifier()`, `refreshUser()`, `supportsClass()` are the contract.
- `refreshUser()` runs every stateful request; keep it cheap and current.
- Memory/chain/custom providers cover non-Doctrine needs (entity is out of scope).

**Cheat:** Contract: `loadUserByIdentifier` / `refreshUser` / `supportsClass`. Add `PasswordUpgraderInterface` for transparent rehash. `memory` for tests; `chain` tries providers in order. Stateless firewall ⇒ no `refreshUser()`.

## Role Hierarchy
- `security.role_hierarchy` declares role implications, resolved transitively.
- The hierarchy applies in `isGranted()`, `#[IsGranted]`, Twig and
  `access_control` — never in `$user->getRoles()`/`$token->getRoleNames()`.
- `RoleHierarchyInterface::getReachableRoleNames()` is the expansion API for
  your own services and voters.
- Under the hood: `RoleHierarchyVoter` (subclass of `RoleVoter`) expands roles
  before matching the attribute.
- Store minimal roles; derive the rest — the map is config, not data.

**Cheat:** Config: `security.role_hierarchy: { ROLE_ADMIN: ROLE_USER, ... }`. Transitive: A→B→C ⇒ A reaches C. `isGranted()` expands · `getRoles()` does **not**. Manual expansion: `RoleHierarchyInterface->getReachableRoleNames()`. Voter swap: `RoleVoter` → `RoleHierarchyVoter`.

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

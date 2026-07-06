# Security

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[Voter](../labs/security.md)** — a step-by-step TD with test-first guidance and a reference solution.

Symfony Security is two cooperating subsystems: **authentication** (who are
you?) driven by the authenticator manager, firewalls and passports, and
**authorization** (are you allowed?) driven by the access-decision manager and
voters. In Symfony 8 there is only the **authenticator-based** system — the
legacy `Guard` and the old authentication providers are gone, and
`enable_authenticator_manager` no longer exists.

!!! abstract "Stage at a glance"
    - **Prerequisites:** [Symfony Architecture](../architecture/index.md)
      (kernel events), [Dependency Injection](../dependency-injection/index.md),
      [HTTP](../http/index.md) (requests, cookies, sessions)
    - **Level:** Advanced → Expert
    - **Difficulty:** ★★★
    - **Est. time:** 6–8 h
    - **Dependencies:** builds on the [event dispatcher](../architecture/events.md)
      and the [service container](../dependency-injection/index.md); the
      firewall is a `kernel.request` listener
    - **Revision priority:** **Critical** — one of the most heavily tested
      stages. `access_control` first-match, voter strategies, passport badges and
      the `IS_AUTHENTICATED_*` attributes are prime traps.

## Why this stage is Critical

Security is where the most subtle exam questions live because so much happens
implicitly: a single `kernel.request` listener (`Firewall`) selects a firewall,
an authenticator turns the request into a **Passport**, listeners validate its
**badges** on `CheckPassportEvent`, a **token** is created and stored, and later
the **access-decision manager** polls **voters** to grant or deny. Knowing the
exact classes, event order and first-match rules is the difference between
guessing and scoring.

## Chapters

- [Authentication](authentication.md) — the firewall/authenticator flow: how a
  request becomes an authenticated token, stateless vs stateful, entry points.
- [Authorization](authorization.md) — roles, access decisions, `isGranted()`,
  `denyAccessUnlessGranted()`, `#[IsGranted]`, attributes vs roles.
- [Configuration](configuration.md) — `security.yaml` anatomy: providers,
  firewalls, `access_control`, `password_hashers`, `role_hierarchy`.
- [Providers](providers.md) — user providers: memory, custom
  `UserProviderInterface`, chain provider, `refreshUser()` (entity is out of scope).
- [Firewalls](firewalls.md) — matching, the `dev` firewall, `security: false`,
  first-match order, lazy firewalls, context sharing.
- [Users](users.md) — `UserInterface`, `PasswordAuthenticatedUserInterface`,
  `getUserIdentifier()`, `EquatableInterface`, the user lifecycle.
- [Password Hashers](password-hashers.md) — `auto`/`bcrypt`/`sodium`, migration
  and rehash (`needsRehash`), `PasswordHasherFactory`, plaintext for tests only.
- [Roles](roles.md) — `ROLE_` conventions, role hierarchy, the
  `IS_AUTHENTICATED_*` special attributes, `PUBLIC_ACCESS`.
- [Access Control Rules](access-control.md) — `access_control` matching,
  `allow_if` expressions, `requires_channel`, first-match semantics.
- [Authenticators, Passports & Badges](authenticators.md) — custom
  authenticators, the Passport + badges model, form/JSON/access-token login.
- [Voters & Voting Strategies](voters.md) — the `Voter` base class,
  grant/deny/abstain, affirmative/consensus/unanimous/priority strategies.

## Suggested reading order

Read [Authentication](authentication.md) and [Authorization](authorization.md)
first for the mental model, then [Configuration](configuration.md) to see it in
`security.yaml`. Cover the building blocks — [Users](users.md),
[Providers](providers.md), [Password Hashers](password-hashers.md),
[Firewalls](firewalls.md) — then the two deep systems:
[Authenticators, Passports & Badges](authenticators.md) and
[Voters](voters.md). Finish with [Roles](roles.md) and
[Access Control Rules](access-control.md), which are dense with exam traps.
</content>
</invoke>

## Official References

- [Symfony documentation — Security](https://symfony.com/doc/current/security.html)
- [Symfony documentation home](https://symfony.com/doc/current/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)

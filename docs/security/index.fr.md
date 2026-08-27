# Security

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Voter](../labs/security.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Symfony Security se compose de deux sous-systèmes qui coopèrent :
l'**authentication** (qui êtes-vous ?), pilotée par l'authenticator manager, les
firewalls et les passports, et l'**authorization** (en avez-vous le droit ?),
pilotée par l'access-decision manager et les voters. Dans Symfony 8, il n'existe
plus que le système **basé sur les authenticators** — le `Guard` historique et
les anciens authentication providers ont disparu, et
`enable_authenticator_manager` n'existe plus.

!!! abstract "Stage at a glance"
    - **Prerequisites:** [Symfony Architecture](../architecture/index.md)
      (kernel events), [Dependency Injection](../dependency-injection/index.md),
      [HTTP](../http/index.md) (requests, cookies, sessions)
    - **Level:** Advanced → Expert
    - **Difficulty:** ★★★
    - **Est. time:** 6–8 h
    - **Dependencies:** s'appuie sur l'[event dispatcher](../architecture/events.md)
      et le [service container](../dependency-injection/index.md) ; le
      firewall est un listener `kernel.request`
    - **Revision priority:** **Critical** — l'un des stages les plus testés à
      l'examen. Le first-match de `access_control`, les stratégies de voters, les
      badges du passport et les attributs `IS_AUTHENTICATED_*` sont des pièges de
      premier ordre.

## Why this stage is Critical

La sécurité concentre les questions d'examen les plus subtiles, car énormément
de choses se passent implicitement : un unique listener `kernel.request`
(`Firewall`) sélectionne un firewall, un authenticator transforme la request en
**Passport**, des listeners valident ses **badges** sur `CheckPassportEvent`, un
**token** est créé et stocké, puis l'**access-decision manager** interroge les
**voters** pour accorder ou refuser l'accès. Connaître les classes exactes,
l'ordre des events et les règles de first-match fait la différence entre deviner
et marquer des points.

## Chapters

- [Authentication](authentication.md) — le flux firewall/authenticator : comment
  une request devient un token authentifié, stateless vs stateful, les entry
  points.
- [Authorization](authorization.md) — les rôles, les décisions d'accès,
  `isGranted()`, `denyAccessUnlessGranted()`, `#[IsGranted]`, attributs vs rôles.
- [Configuration](configuration.md) — l'anatomie de `security.yaml` : providers,
  firewalls, `access_control`, `password_hashers`, `role_hierarchy`.
- [Providers](providers.md) — les user providers : memory, un
  `UserProviderInterface` personnalisé, le chain provider, `refreshUser()`
  (entity est hors programme).
- [Firewalls](firewalls.md) — le matching, le firewall `dev`, `security: false`,
  l'ordre first-match, les firewalls lazy, le partage de contexte.
- [Users](users.md) — `UserInterface`, `PasswordAuthenticatedUserInterface`,
  `getUserIdentifier()`, `EquatableInterface`, le cycle de vie de l'utilisateur.
- [Password Hashers](password-hashers.md) — `auto`/`bcrypt`/`sodium`, la
  migration et le rehash (`needsRehash`), `PasswordHasherFactory`, le plaintext
  réservé aux tests.
- [Roles](roles.md) — les conventions `ROLE_`, la hiérarchie de rôles, les
  attributs spéciaux `IS_AUTHENTICATED_*`, `PUBLIC_ACCESS`.
- [Access Control Rules](access-control.md) — le matching de `access_control`,
  les expressions `allow_if`, `requires_channel`, la sémantique first-match.
- [Authenticators, Passports & Badges](authenticators.md) — les authenticators
  personnalisés, le modèle Passport + badges, le login form/JSON/access-token.
- [Voters & Voting Strategies](voters.md) — la classe de base `Voter`,
  grant/deny/abstain, les stratégies affirmative/consensus/unanimous/priority.

## Suggested reading order

Lisez d'abord [Authentication](authentication.md) et
[Authorization](authorization.md) pour acquérir le modèle mental, puis
[Configuration](configuration.md) pour le voir concrètement dans
`security.yaml`. Couvrez ensuite les briques de base — [Users](users.md),
[Providers](providers.md), [Password Hashers](password-hashers.md),
[Firewalls](firewalls.md) — puis les deux systèmes en profondeur :
[Authenticators, Passports & Badges](authenticators.md) et
[Voters](voters.md). Terminez par [Roles](roles.md) et
[Access Control Rules](access-control.md), très denses en pièges d'examen.

## Official References

- [Symfony documentation — Security](https://symfony.com/doc/8.0/security.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)

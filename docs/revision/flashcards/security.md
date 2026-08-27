# Flashcards — Security

78 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

??? question "1. In Symfony 8, where are a Passport's badges validated?"
    **✅ By listeners on the CheckPassportEvent**

    authenticate() only builds the Passport. Badge resolution and credential verification happen on CheckPassportEvent (UserProviderListener, CheckCredentialsListener, CsrfProtectionListener…).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html)

??? question "2. What is the status of enable_authenticator_manager in Symfony 8?"
    **✅ Removed — the authenticator system is the only one**

    The key existed and was deprecated in 7.x; Symfony 8 removed it entirely because the legacy authentication system is gone.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "3. A stateless firewall (stateless: true) does NOT do which of these?"
    **✅ Persist the token in the session via ContextListener**

    Stateless firewalls skip the ContextListener, so nothing is stored or restored between requests; each request re-authenticates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "4. An authenticator's supports() returns null. What does that mean?"
    **✅ Authenticate lazily when the token is needed**

    null means 'unsure — call me lazily'. Many stateless authenticators use it so authentication is deferred until required.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authenticator/AuthenticatorInterface.php)

??? question "5. During a successful login, in which order does the AuthenticatorManager dispatch these events?"
    **✅ CheckPassportEvent → AuthenticationTokenCreatedEvent → LoginSuccessEvent**

    authenticate() builds the Passport; CheckPassportEvent listeners then resolve the badges; createToken() runs; AuthenticationTokenCreatedEvent is the last chance to swap/decorate the token; the token is stored; finally LoginSuccessEvent fires (invoking onAuthenticationSuccess()). On error a LoginFailureEvent is dispatched instead. Any ordering that runs LoginSuccessEvent before the passport is checked, or creates the token before CheckPassportEvent, contradicts the manager's pipeline.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authentication/AuthenticatorManager.php)

??? question "6. A controller runs $security->getUser()->getUserIdentifier() and fatals on some requests. What is the cause?"
    **✅ On an anonymous request getUser() returns null, so calling a method on null fatals; guard with ?->, ?? or an IsGranted check**

    Security::getUser() returns ?UserInterface — it is null whenever no token holds a user (a truly anonymous request, or a lazy firewall whose token was never read). Dereferencing null is a fatal error. Guard with $user?->…, a ?? fallback, or an earlier #[IsGranted('IS_AUTHENTICATED_FULLY')] / denyAccessUnlessGranted() so $user is guaranteed non-null past that point. getUserIdentifier() is very much part of the 8.0 interface, and getUser() never throws for guests — it simply returns null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "7. True or False: a firewall with stateless: true restores the authenticated token from the session on the next request."
    **✅ False**

    False. stateless: true means the ContextListener is not registered, so no token is written to or restored from the session. Each request starts with empty token storage and must re-authenticate (e.g. re-read the bearer token). Session-backed restore is a property of stateful firewalls only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "8. Which check can pass a subject to voters?"
    **✅ isGranted('EDIT', $post)**

    Only the isGranted()/#[IsGranted]/denyAccessUnlessGranted() path carries a subject. access_control is URL-based and cannot pass a subject.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

??? question "9. A #[IsGranted] check fails for an unauthenticated user. What happens?"
    **✅ The entry point starts authentication (e.g. login redirect)**

    An AccessDeniedException for an unauthenticated user is converted to the entry point response; an authenticated-but-unauthorized user gets a 403.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#access-control)

??? question "10. isGranted() ultimately delegates the decision to which interface?"
    **✅ AccessDecisionManagerInterface**

    AuthorizationChecker reads the current token from TokenStorage, then calls AccessDecisionManager::decide().

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/AccessDecisionManager.php)

??? question "11. On a logged-out request, what does isGranted('ROLE_ADMIN') do internally?"
    **✅ The AuthorizationChecker substitutes a NullToken and voters run; RoleVoter finds no matching role and it returns a clean false**

    When TokenStorage holds no token, AuthorizationChecker substitutes a NullToken rather than crashing, and voting proceeds normally. RoleVoter finds ROLE_ADMIN is not present, so the decision is false — not an exception. (AuthenticatedVoter denies the IS_AUTHENTICATED_* attributes for a NullToken, while PUBLIC_ACCESS still grants.) Authorization never starts authentication by itself; only an AccessDeniedException handled by the firewall triggers the entry point.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authentication/Token/NullToken.php)

??? question "12. In #[IsGranted('EDIT', subject: 'post')], what does subject: 'post' do?"
    **✅ Passes the controller argument named $post to the voters as the subject of the EDIT decision**

    The subject option references a controller argument by name; Symfony resolves $post and passes it to AccessDecisionManager::decide() as the subject, so a voter's voteOnAttribute() receives the actual Post instance and can apply per-object rules (ownership, state). It is not a voter name, a route requirement, or a role suffix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#access-controllers)

??? question "13. Which statement about access_control vs isGranted() is correct?"
    **✅ access_control is URL-based and cannot pass a subject; only isGranted()/#[IsGranted] can**

    access_control runs through the same AccessDecisionManager and voters as isGranted(), but it only supplies the rule's roles/allow_if — there is no subject, because it matches on the URL, not on a domain object. Per-object decisions ("can edit THIS post?") must use #[IsGranted]/denyAccessUnlessGranted() with a subject. Both do reach voters, so the "neither" option is wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

??? question "14. Which of these funnel through AuthorizationCheckerInterface::isGranted()? (choose 3)"
    **✅ The #[IsGranted] attribute ; denyAccessUnlessGranted() in a controller ; Twig's is_granted() function**

    #[IsGranted], denyAccessUnlessGranted() and Twig's is_granted() are all thin wrappers over AuthorizationCheckerInterface::isGranted(), which delegates to the AccessDecisionManager and voters. loadUserByIdentifier() belongs to the authentication/provider layer (loading users), not authorization, so it does not go through isGranted().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#access-control-authorization)

??? question "15. The password_hashers map in security.yaml is keyed by…"
    **✅ A user class or interface name**

    You map a user class (commonly PasswordAuthenticatedUserInterface) to an algorithm such as 'auto'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html)

??? question "16. Two providers are defined and a firewall omits the provider key. Result?"
    **✅ Configuration error — the provider is ambiguous**

    With multiple providers there is no implicit default; each firewall must name its provider explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html)

??? question "17. Why must the dev firewall (security: false) be listed first?"
    **✅ Firewalls are first-match, so it must precede protecting firewalls**

    Firewall matching is top-to-bottom, first match wins. Listing the dev firewall first stops the profiler/assets being intercepted by login.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-firewall)

??? question "18. For each firewall, what does SecurityExtension compile at container build time?"
    **✅ A FirewallContext bundling its listeners, the authenticator list, an AuthenticatorManager, and (unless stateless) a ContextListener — all indexed in a FirewallMap**

    SecurityExtension reads the security.yaml tree and, per firewall, compiles a dedicated FirewallContext (its listeners, the list of authenticators, an AuthenticatorManager, an exception listener, and a ContextListener unless the firewall is stateless). All contexts are registered in the FirewallMap; at runtime the single Firewall listener asks the map which context matches. The work happens at compile time, not lazily per request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/SecurityBundle/DependencyInjection/SecurityExtension.php)

??? question "19. Requests under /api are being handled by the session-based main firewall instead of the stateless api firewall. What is wrong?"
    **✅ The catch-all main firewall is listed before api; firewalls are first-match, so api must come first**

    Firewalls match top-to-bottom, first match wins. A catch-all main firewall (no pattern) placed before api matches every request, so /api never reaches the stateless firewall. Move the specific ^/api firewall above main. enable_authenticator_manager no longer exists in Symfony 8, stateless does not affect matching, and multiple providers do not skip a firewall.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-firewall)

??? question "20. Which of these are valid top-level keys under security: in Symfony 8? (choose 4)"
    **✅ providers ; firewalls ; access_control ; role_hierarchy**

    providers, firewalls, access_control, password_hashers and role_hierarchy are the core keys of security.yaml. enable_authenticator_manager was removed in Symfony 8 — the authenticator system is the only one — so it is not a valid key anymore.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/configuration/security.html)

??? question "21. How do you configure eraseCredentials behaviour in security.yaml in Symfony 8?"
    **✅ You don't — eraseCredentials() was removed in 8.0; strip secrets in the user's __serialize()**

    There is no eraseCredentials configuration key, and there never was — it was a UserInterface method. In Symfony 8 both UserInterface::eraseCredentials() and TokenInterface::eraseCredentials() were removed; the documented replacement is to strip sensitive data (the password) in your user's __serialize() method, which is what runs when the token/user is stored in the session.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/UPGRADE-8.0.md)

??? question "22. Which method loads a user by identifier in Symfony 8?"
    **✅ loadUserByIdentifier()**

    loadUserByUsername() was removed; the UserProviderInterface loader is loadUserByIdentifier().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html)

??? question "23. When is refreshUser() called?"
    **✅ On every stateful request, to re-sync the session user**

    The ContextListener refreshes the stored user on each request of a stateful firewall; a stateless firewall never calls it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall/ContextListener.php)

??? question "24. Does a user provider verify the user's password?"
    **✅ No — credentials are checked on CheckPassportEvent**

    Providers only load and refresh users. CheckCredentialsListener verifies the PasswordCredentials badge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html)

??? question "25. A custom provider does `return $repo->find($id);` in loadUserByIdentifier() and sometimes throws a TypeError. What is the fix?"
    **✅ find() can return null but the return type is a non-nullable UserInterface; throw UserNotFoundException when no user matches**

    loadUserByIdentifier(): UserInterface has a non-nullable return type. Returning null (as find() may) is a contract violation and causes a TypeError. When no user matches you must throw UserNotFoundException, which Symfony normalises to a generic BadCredentialsException so an attacker cannot distinguish "unknown user" from "wrong password". You never return null or false, and the method returns a single UserInterface, not an array.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html)

??? question "26. An admin deletes a user's account while that user is browsing under a stateful firewall. What happens on the user's next request?"
    **✅ refreshUser() can no longer load them and throws; the ContextListener discards the token, effectively logging them out**

    On each stateful request the ContextListener calls refreshUser() to re-sync the session user. A now-missing account makes refreshUser() throw (UserNotFoundException / UnsupportedUserException), so the ContextListener treats the user as unloadable, discards the token and clears storage — an immediate, clean logout. It is not a fatal error, and access does not persist until the cookie expires precisely because the user is re-checked every request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall/ContextListener.php)

??? question "27. A provider is configured as `all_users: { chain: { providers: [in_memory, api_users] } }`. What does it do?"
    **✅ Tries each listed provider in order; the first that supports/loads the user wins**

    A chain provider delegates to its sub-providers in the declared order and returns the first successful match; if none support/find the user it throws. It does not merge users, require presence in all providers, or choose randomly. Correct supportsClass()/UnsupportedUserException handling in each sub-provider is what lets the chain fall through cleanly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html#chaining-user-providers)

??? question "28. True or False: a firewall with stateless: true still calls refreshUser() on every request."
    **✅ False**

    False. refreshUser() is invoked by the ContextListener, which only exists on stateful firewalls. A stateless firewall stores no token in the session, so there is nothing to refresh — the user is re-loaded from scratch by the authenticator on each request instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html)

??? question "29. How many firewalls are active for a given request?"
    **✅ Exactly one — the first whose matcher matches**

    The FirewallMap returns the first matching FirewallContext; matching stops there.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-firewall)

??? question "30. What does security: false on a firewall do?"
    **✅ Disables the security layer for that zone (and still counts as the match)**

    It turns off all security listeners for matching requests (used for the profiler and dev assets) and, being first-match, prevents later firewalls from matching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "31. Two firewalls should share a logged-in session. What do you configure?"
    **✅ The same context: name on both firewalls**

    Token sharing between firewalls requires an explicit matching context key; otherwise each firewall keeps its own token.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "32. What does lazy: true achieve on a firewall?"
    **✅ Authentication is deferred until the token is actually read**

    A lazy firewall only authenticates when the token is accessed (e.g. is_granted/getUser), so fully public pages skip auth and session loading.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "33. A firewall configured with `pattern: /api` unexpectedly also intercepts /my-api-docs. Why?"
    **✅ pattern is a regex; without a leading ^ it matches anywhere in the path. Anchor it as ^/api**

    Firewall pattern is an unanchored regular expression, so /api matches any path containing that sequence — including /my-api-docs. Anchoring with ^ (^/api) fixes it to the start of the path. Patterns are regexes (anchorable), the doc route is unrelated to physical location, and methods: narrows HTTP verbs, not path matching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-firewall)

??? question "34. Given firewalls declared as main (no pattern) then api (pattern: ^/api), what happens to /api requests?"
    **✅ main (the catch-all) matches first, so /api never reaches the api firewall; list api first**

    Firewall selection is first-match, top-to-bottom — not most-specific-wins. A patternless main firewall matches everything, so it swallows /api before the api firewall is considered. The fix is ordering: specific firewalls (^/api) before the catch-all. Symfony does not run multiple firewalls per request, nor does it error on overlap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-firewall)

??? question "35. When does the Firewall listener run in the kernel lifecycle?"
    **✅ On kernel.request at priority 8 (after routing), it asks the FirewallMap for the first matching FirewallContext**

    The Firewall listener subscribes to kernel.request at priority 8, which runs after the RouterListener (routing), then queries the FirewallMap for the matching FirewallContext and runs its listeners. It is a request-phase concern, not controller/response/terminate, and it deliberately runs after routing so route attributes are available.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall.php)

??? question "36. Which methods does UserInterface declare in Symfony 8?"
    **✅ getRoles() and getUserIdentifier()**

    Symfony 8 trimmed UserInterface to two methods; eraseCredentials() and getUsername() were removed.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/UserInterface.php)

??? question "37. How do you keep a user's password out of the session in Symfony 8?"
    **✅ Override __serialize() and unset the password field**

    eraseCredentials() was removed in 8.0; the documented replacement is to strip sensitive data in __serialize().

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/UPGRADE-8.0.md)

??? question "38. isEqualTo() returns false when a stored user is refreshed. Effect?"
    **✅ The token is invalidated — the user is logged out**

    A negative EquatableInterface comparison on refresh tells the framework the stored identity is stale, so the token is dropped.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/EquatableInterface.php)

??? question "39. Which interface declares getPassword()?"
    **✅ PasswordAuthenticatedUserInterface**

    getPassword(): ?string is declared by PasswordAuthenticatedUserInterface, an opt-in interface — not by UserInterface (which only has getRoles() and getUserIdentifier() in 8.0). EquatableInterface adds isEqualTo(); PasswordUpgraderInterface (a provider concern) adds upgradePassword(). A token-only/SSO user may skip PasswordAuthenticatedUserInterface entirely.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/PasswordAuthenticatedUserInterface.php)

??? question "40. A token-only API user declares getPassword(): string. Login works, but the security layer throws a TypeError when serialising the user. Why?"
    **✅ Such a user has no local password, so the stored hash is null; getPassword() must be typed ?string**

    PasswordAuthenticatedUserInterface::getPassword() is typed ?string precisely because passwordless accounts (OAuth/LDAP/token-only) legitimately have a null hash. Declaring a non-nullable string return type makes PHP throw a TypeError the moment null is returned during verification or serialization. The CheckCredentialsListener treats a null hash as non-verifiable. The method name and return type are fixed by the interface, and eraseCredentials() no longer exists.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-user)

??? question "41. You need a user's role change to immediately end their existing sessions. What do you implement?"
    **✅ EquatableInterface::isEqualTo() comparing roles; returning false on refresh invalidates the token**

    When a user implements EquatableInterface, the ContextListener compares the session copy with the freshly refreshed user on each request via isEqualTo(). Including getRoles() in that comparison means a role change yields false, which invalidates the token and logs the user out immediately. eraseCredentials() no longer exists; a manual logout-everywhere listener is crude; and stateless would drop sessions entirely rather than invalidate on change.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/EquatableInterface.php)

??? question "42. True or False: UserInterface::getUsername() still exists in Symfony 8."
    **✅ False**

    False. getUsername() was replaced by getUserIdentifier() (mandatory since 6.0) and no longer exists on UserInterface in Symfony 8. Use getUserIdentifier() for the login identifier the session stores and refreshUser() reloads from.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/UserInterface.php)

??? question "43. Which password algorithm is the recommended default?"
    **✅ auto**

    'auto' selects the best available algorithm (currently bcrypt) and can adapt over time; it also enables automatic rehash on cost changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html)

??? question "44. Transparent password rehash on login requires…"
    **✅ Both migrate_from and a provider implementing PasswordUpgraderInterface**

    migrate_from lets needsRehash() detect the old hash; the PasswordUpgradeBadge triggers PasswordMigratingListener, which persists the new hash via upgradePassword().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html#password-migration)

??? question "45. Where is a login password actually verified?"
    **✅ In CheckCredentialsListener on CheckPassportEvent**

    The authenticator adds a PasswordCredentials badge; the listener verifies it against the hash using the configured hasher.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html)

??? question "46. Which statement about the plaintext hasher is correct?"
    **✅ It is intended for tests only and must never be used in production**

    plaintext stores passwords unhashed; it exists to speed up test fixtures and is a production anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html)

??? question "47. A hasher entry is `algorithm: sodium, migrate_from: ['bcrypt']`. What does it mean?"
    **✅ Hash new passwords with sodium, but still accept existing bcrypt hashes and upgrade them on the next successful login**

    The primary algorithm (sodium/Argon2id) is used to hash new passwords, while migrate_from lists legacy algorithms whose hashes are still verifiable. On a valid login against an old bcrypt hash, needsRehash() returns true and the PasswordUpgradeBadge flow rehashes with sodium and persists it — transparent, no reset. It does not reject bcrypt, swap hashing/verifying roles, or double-hash.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html#password-migration)

??? question "48. A user with a very long passphrase can change the trailing characters and still log in. Which hasher is in use and why?"
    **✅ bcrypt — it truncates input at 72 bytes, so bytes beyond that are ignored**

    bcrypt has a hard 72-byte input limit; any bytes past 72 are silently ignored, so two passphrases sharing the first 72 bytes verify identically. Very long passphrases therefore lose entropy under bcrypt. sodium (Argon2id) has no such truncation, which is one reason to prefer it for long secrets. The other options invent behaviour that does not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html)

??? question "49. You set migrate_from and needsRehash() returns true, yet stored hashes are never upgraded. What is missing?"
    **✅ The user provider does not implement PasswordUpgraderInterface, so upgradePassword() is never called to persist the new hash**

    migrate_from + needsRehash() computes a fresh hash, but persisting it is the provider's job: only a provider implementing PasswordUpgraderInterface's upgradePassword() actually stores it (triggered by the PasswordUpgradeBadge / PasswordMigratingListener). Without it, the rehash is computed and discarded every login. migrate_from is not plaintext-only, you must not hash manually, and needsRehash() is fully supported.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html#password-migration)

??? question "50. Which special attribute is broader?"
    **✅ IS_AUTHENTICATED_REMEMBERED (fully-authenticated users also satisfy it)**

    Fully-authenticated users satisfy IS_AUTHENTICATED_REMEMBERED, but remember-me users do NOT satisfy IS_AUTHENTICATED_FULLY.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#security-authorization-access-decision)

??? question "51. In Symfony 8, how do you allow everyone (including not-logged-in) on a path?"
    **✅ PUBLIC_ACCESS**

    Anonymous tokens were removed; PUBLIC_ACCESS is the attribute that opts a path out of authentication.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "52. An attribute 'EDITOR' (no ROLE_ prefix) is checked. How does RoleVoter treat it?"
    **✅ It is ignored — RoleVoter only handles ROLE_-prefixed attributes**

    RoleVoter supports only ROLE_* attributes; unprefixed strings abstain there (a custom voter could still handle them).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#roles)

??? question "53. Given role_hierarchy ROLE_ADMIN: [ROLE_USER], a user with ROLE_ADMIN…"
    **✅ Is also granted ROLE_USER (reachable roles are expanded)**

    RoleHierarchyVoter expands reachable roles, so ROLE_ADMIN transitively includes ROLE_USER. Hierarchy flows downward.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#hierarchical-roles)

??? question "54. With role_hierarchy ROLE_ADMIN: [ROLE_USER] and ROLE_SUPER_ADMIN: [ROLE_ADMIN], which roles does a ROLE_SUPER_ADMIN user satisfy?"
    **✅ ROLE_SUPER_ADMIN, ROLE_ADMIN and ROLE_USER (transitively reachable)**

    RoleHierarchy::getReachableRoleNames() expands roles transitively: ROLE_SUPER_ADMIN reaches ROLE_ADMIN, which reaches ROLE_USER, so the user satisfies all three. Inheritance flows downward and is transitive (not just one level), but it does not grant unrelated roles that are not on the reachable path.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Role/RoleHierarchy.php)

??? question "55. Which attribute protects a 'change email' action so that a remember-me cookie is not sufficient?"
    **✅ IS_AUTHENTICATED_FULLY**

    IS_AUTHENTICATED_FULLY is granted only to users who authenticated fresh in the current session — not via a remember-me cookie. A stolen remember-me cookie satisfies IS_AUTHENTICATED_REMEMBERED and IS_AUTHENTICATED, so those would wrongly permit a sensitive identity change; PUBLIC_ACCESS allows everyone. Use _FULLY to force a fresh login for payments/identity changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#security-authorization-access-decision)

??? question "56. True or False: IS_AUTHENTICATED_ANONYMOUSLY is still a valid access attribute in Symfony 8."
    **✅ False**

    False. Symfony 8 has no anonymous tokens, so IS_AUTHENTICATED_ANONYMOUSLY no longer exists. To open a path to everyone (including not-logged-in visitors) use PUBLIC_ACCESS instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "57. How many access_control rules apply to a request?"
    **✅ Only the first matching rule**

    AccessMap returns the first match and evaluation stops. Order rules from specific to general.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#securing-url-patterns-access-control)

??? question "58. A rule has roles: [ROLE_A, ROLE_B]. Access is granted when the user has…"
    **✅ Either ROLE_A or ROLE_B**

    Multiple roles within a single access_control rule are OR-combined.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#securing-url-patterns-access-control)

??? question "59. No access_control rule matches the request. What happens?"
    **✅ Access is allowed (deferred to controller-level guards)**

    access_control only restricts on a matching rule; with no match there is no URL-level restriction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "60. What does requires_channel: https do, and when?"
    **✅ Redirects matching paths to HTTPS before authentication runs**

    The ChannelListener enforces requires_channel before authentication, so even the login page is redirected to HTTPS.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "61. After adding { path: ^/, roles: PUBLIC_ACCESS } at the top of access_control, the ^/admin rule below stops protecting admin. Why?"
    **✅ First match wins; ^/ matches every path including /admin, so the catch-all is enforced and the admin rule is never reached**

    access_control is first-match, top-to-bottom. ^/ matches all paths, so placing it first means /admin hits the PUBLIC_ACCESS rule and the ^/admin rule underneath is never evaluated — admin becomes public. Order specific rules before the ^/ catch-all. PUBLIC_ACCESS is a normal attribute (it does not disable other rules), and the roles syntax/requires_channel are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#securing-url-patterns-access-control)

??? question "62. Can an access_control rule pass the matched entity to a voter as the subject?"
    **✅ No — access_control has no subject; it calls AccessDecisionManager with only roles/allow_if. Use #[IsGranted] with a subject for per-object rules**

    access_control routes through the same AccessDecisionManager and voters as isGranted(), but it is purely URL-driven: the AccessListener calls decide() with the rule's roles/expression and no subject. There is no subject: key and path parameters are not passed as subjects. Per-object decisions require #[IsGranted]/denyAccessUnlessGranted() with an explicit subject.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

??? question "63. A rule sets both roles: ROLE_USER and an allow_if expression. When is access granted?"
    **✅ Only when BOTH the role check and the expression pass (AND)**

    Within one rule, multiple roles are OR-combined, but when roles and allow_if are both present they must BOTH pass — it is an AND. (allow_if runs the expression through the ExpressionVoter.) Neither key is ignored, and combining them does not turn the rule into an OR.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/expressions.html)

??? question "64. What does an authenticator's authenticate() method return?"
    **✅ A Passport**

    authenticate() builds a Passport of badges; the token is produced later by createToken() after CheckPassportEvent resolves the badges.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html)

??? question "65. Which passport type suits a valid-API-token flow with no password to verify?"
    **✅ SelfValidatingPassport with a UserBadge**

    When the credential itself proves identity, use SelfValidatingPassport, which carries only a UserBadge — there is nothing further to check.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html#the-passport)

??? question "66. In which namespace does PasswordCredentials live?"
    **✅ Symfony\Component\Security\Http\Authenticator\Passport\Credentials**

    PasswordCredentials and CustomCredentials live under Passport\\Credentials; UserBadge, CsrfTokenBadge, RememberMeBadge, PasswordUpgradeBadge and PreAuthenticatedUserBadge live under Passport\\Badge.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport)

??? question "67. Which built-in authenticator uses a token_handler returning a UserBadge?"
    **✅ access_token**

    The access_token authenticator delegates to an AccessTokenHandlerInterface whose getUserBadgeFrom() validates the bearer token and returns a UserBadge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/access_token.html)

??? question "68. An authenticator adds a badge that no CheckPassportEvent listener resolves. What happens?"
    **✅ Passport::checkIfCompletelyResolved() throws, so authentication fails — you cannot forget to validate a badge**

    After CheckPassportEvent, the manager calls Passport::checkIfCompletelyResolved(), which throws if any badge was never marked resolved. This is a deliberate safety net: an unregistered/forgotten badge (e.g. a CsrfTokenBadge with no listener) fails authentication as an AuthenticationException rather than letting an unverified credential slip through. It is neither ignored nor attached to a successful token.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport)

??? question "69. Which of these live in Passport\Badge (i.e. are badges, not credentials)? (choose 3)"
    **✅ UserBadge ; CsrfTokenBadge ; RememberMeBadge**

    UserBadge, CsrfTokenBadge, RememberMeBadge (plus PasswordUpgradeBadge and PreAuthenticatedUserBadge) live under Passport\\Badge. PasswordCredentials — like CustomCredentials — lives under Passport\\Credentials, not Badge. This namespace split is a classic exam distinction.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport)

??? question "70. What does AbstractLoginFormAuthenticator provide that AbstractAuthenticator does not?"
    **✅ supports() (POST to the check path), the entry point via getLoginUrl(), and a default onAuthenticationFailure() that redirects back to the login page**

    AbstractLoginFormAuthenticator adds form-login plumbing on top of AbstractAuthenticator: supports() (POST to the check path), the entry point start() built from the abstract getLoginUrl(), and a default onAuthenticationFailure() redirecting to the login page — leaving you to write authenticate(), getLoginUrl() and onAuthenticationSuccess(). It does not verify passwords (that is CheckCredentialsListener), does not own the event listeners or the provider; and returning a PostAuthenticationToken is AbstractAuthenticator's default, which FormLoginAuthenticator overrides to a UsernamePasswordToken.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authenticator/AbstractLoginFormAuthenticator.php)

??? question "71. What is the default AccessDecisionManager strategy?"
    **✅ affirmative**

    Affirmative is the default: access is granted if at least one voter returns ACCESS_GRANTED.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html#changing-the-access-decision-strategy)

??? question "72. The base Voter's supports() returns false. What is the resulting vote?"
    **✅ ACCESS_ABSTAIN**

    The abstract Voter abstains for unsupported attributes/subjects; it never calls voteOnAttribute() in that case.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/Voter.php)

??? question "73. All voters abstain and allow_if_all_abstain keeps its default. Result?"
    **✅ Access is denied**

    allow_if_all_abstain defaults to false, so if every voter abstains and no one grants, access is denied.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

??? question "74. What are the integer values of the voter constants?"
    **✅ ACCESS_GRANTED = 1, ACCESS_ABSTAIN = 0, ACCESS_DENIED = -1**

    These integer constants drive the strategy arithmetic in the AccessDecisionManager.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/VoterInterface.php)

??? question "75. Under the unanimous strategy, one voter denies while another grants. Outcome?"
    **✅ Access is denied — unanimous grants only if no voter denies**

    unanimous requires that no voter denies. A single ACCESS_DENIED blocks access regardless of grants (unlike affirmative).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

??? question "76. In a Voter, voteOnAttribute() starts with `if (!$user instanceof AppUser) { return false; }`. Why return false rather than abstain?"
    **✅ supports() already accepted the attribute, so this voter owns the decision; with no valid user it must deny — abstaining would wrongly delegate an attribute it claimed**

    By the time voteOnAttribute() runs, supports() has already said "this attribute/subject is mine", so the voter must return a real yes/no. An unauthenticated request carries a NullToken whose getUser() is null (or a user of the wrong class), so there is nobody to authorize — deny (return false). Abstaining would contradict supports(); getUser() genuinely can be null; and voters signal decisions via return values, not by throwing.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

??? question "77. Under the unanimous strategy, a voter returns false from voteOnAttribute() for an attribute it does not actually care about. Effect?"
    **✅ false is ACCESS_DENIED, which blocks access under unanimous; unrelated attributes must be filtered out in supports() so the voter abstains**

    Returning false from voteOnAttribute() maps to ACCESS_DENIED, not abstain. Under unanimous a single deny blocks access, so a voter that "says no to what isn't mine" silently breaks authorization. The correct pattern is to reject unrelated attributes/subjects in supports(), which makes the base Voter abstain (ACCESS_ABSTAIN, no effect). abstain and deny are distinct, and an unsupported attribute does not throw.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/Voter.php)

??? question "78. With access_decision_manager.strategy set to priority, how is the decision made?"
    **✅ The first voter that does not abstain decides the outcome**

    The priority strategy takes the vote of the first (highest-priority) non-abstaining voter as final, letting a high-priority voter short-circuit (e.g. a global "banned user" voter denying before feature voters run). "All must agree" describes unanimous, "majority" describes consensus, and "one grant is enough" describes affirmative.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html#changing-the-access-decision-strategy)

---

<small>Back to [Flashcards](index.md) · [Security](../../security/index.md)</small>

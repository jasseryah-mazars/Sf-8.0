# Flashcards — Security

41 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

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

??? question "5. Which check can pass a subject to voters?"
    **✅ isGranted('EDIT', $post)**

    Only the isGranted()/#[IsGranted]/denyAccessUnlessGranted() path carries a subject. access_control is URL-based and cannot pass a subject.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

??? question "6. A #[IsGranted] check fails for an unauthenticated user. What happens?"
    **✅ The entry point starts authentication (e.g. login redirect)**

    An AccessDeniedException for an unauthenticated user is converted to the entry point response; an authenticated-but-unauthorized user gets a 403.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#access-control)

??? question "7. isGranted() ultimately delegates the decision to which interface?"
    **✅ AccessDecisionManagerInterface**

    AuthorizationChecker reads the current token from TokenStorage, then calls AccessDecisionManager::decide().

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/AccessDecisionManager.php)

??? question "8. The password_hashers map in security.yaml is keyed by…"
    **✅ A user class or interface name**

    You map a user class (commonly PasswordAuthenticatedUserInterface) to an algorithm such as 'auto'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html)

??? question "9. Two providers are defined and a firewall omits the provider key. Result?"
    **✅ Configuration error — the provider is ambiguous**

    With multiple providers there is no implicit default; each firewall must name its provider explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html)

??? question "10. Why must the dev firewall (security: false) be listed first?"
    **✅ Firewalls are first-match, so it must precede protecting firewalls**

    Firewall matching is top-to-bottom, first match wins. Listing the dev firewall first stops the profiler/assets being intercepted by login.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-firewall)

??? question "11. Which method loads a user by identifier in Symfony 8?"
    **✅ loadUserByIdentifier()**

    loadUserByUsername() was removed; the UserProviderInterface loader is loadUserByIdentifier().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html)

??? question "12. When is refreshUser() called?"
    **✅ On every stateful request, to re-sync the session user**

    The ContextListener refreshes the stored user on each request of a stateful firewall; a stateless firewall never calls it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall/ContextListener.php)

??? question "13. Does a user provider verify the user's password?"
    **✅ No — credentials are checked on CheckPassportEvent**

    Providers only load and refresh users. CheckCredentialsListener verifies the PasswordCredentials badge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html)

??? question "14. How many firewalls are active for a given request?"
    **✅ Exactly one — the first whose matcher matches**

    The FirewallMap returns the first matching FirewallContext; matching stops there.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-firewall)

??? question "15. What does security: false on a firewall do?"
    **✅ Disables the security layer for that zone (and still counts as the match)**

    It turns off all security listeners for matching requests (used for the profiler and dev assets) and, being first-match, prevents later firewalls from matching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "16. Two firewalls should share a logged-in session. What do you configure?"
    **✅ The same context: name on both firewalls**

    Token sharing between firewalls requires an explicit matching context key; otherwise each firewall keeps its own token.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "17. What does lazy: true achieve on a firewall?"
    **✅ Authentication is deferred until the token is actually read**

    A lazy firewall only authenticates when the token is accessed (e.g. is_granted/getUser), so fully public pages skip auth and session loading.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "18. Which methods does UserInterface declare in Symfony 8?"
    **✅ getRoles() and getUserIdentifier()**

    Symfony 8 trimmed UserInterface to two methods; eraseCredentials() and getUsername() were removed.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/UserInterface.php)

??? question "19. How do you keep a user's password out of the session in Symfony 8?"
    **✅ Override __serialize() and unset the password field**

    eraseCredentials() was removed in 8.0; the documented replacement is to strip sensitive data in __serialize().

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/UPGRADE-8.0.md)

??? question "20. isEqualTo() returns false when a stored user is refreshed. Effect?"
    **✅ The token is invalidated — the user is logged out**

    A negative EquatableInterface comparison on refresh tells the framework the stored identity is stale, so the token is dropped.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/EquatableInterface.php)

??? question "21. Which password algorithm is the recommended default?"
    **✅ auto**

    'auto' selects the best available algorithm (currently bcrypt) and can adapt over time; it also enables automatic rehash on cost changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html)

??? question "22. Transparent password rehash on login requires…"
    **✅ Both migrate_from and a provider implementing PasswordUpgraderInterface**

    migrate_from lets needsRehash() detect the old hash; the PasswordUpgradeBadge triggers PasswordMigratingListener, which persists the new hash via upgradePassword().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html#password-migration)

??? question "23. Where is a login password actually verified?"
    **✅ In CheckCredentialsListener on CheckPassportEvent**

    The authenticator adds a PasswordCredentials badge; the listener verifies it against the hash using the configured hasher.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html)

??? question "24. Which statement about the plaintext hasher is correct?"
    **✅ It is intended for tests only and must never be used in production**

    plaintext stores passwords unhashed; it exists to speed up test fixtures and is a production anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html)

??? question "25. Which special attribute is broader?"
    **✅ IS_AUTHENTICATED_REMEMBERED (fully-authenticated users also satisfy it)**

    Fully-authenticated users satisfy IS_AUTHENTICATED_REMEMBERED, but remember-me users do NOT satisfy IS_AUTHENTICATED_FULLY.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#security-authorization-access-decision)

??? question "26. In Symfony 8, how do you allow everyone (including not-logged-in) on a path?"
    **✅ PUBLIC_ACCESS**

    Anonymous tokens were removed; PUBLIC_ACCESS is the attribute that opts a path out of authentication.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "27. An attribute 'EDITOR' (no ROLE_ prefix) is checked. How does RoleVoter treat it?"
    **✅ It is ignored — RoleVoter only handles ROLE_-prefixed attributes**

    RoleVoter supports only ROLE_* attributes; unprefixed strings abstain there (a custom voter could still handle them).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#roles)

??? question "28. Given role_hierarchy ROLE_ADMIN: [ROLE_USER], a user with ROLE_ADMIN…"
    **✅ Is also granted ROLE_USER (reachable roles are expanded)**

    RoleHierarchyVoter expands reachable roles, so ROLE_ADMIN transitively includes ROLE_USER. Hierarchy flows downward.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#hierarchical-roles)

??? question "29. How many access_control rules apply to a request?"
    **✅ Only the first matching rule**

    AccessMap returns the first match and evaluation stops. Order rules from specific to general.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#securing-url-patterns-access-control)

??? question "30. A rule has roles: [ROLE_A, ROLE_B]. Access is granted when the user has…"
    **✅ Either ROLE_A or ROLE_B**

    Multiple roles within a single access_control rule are OR-combined.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#securing-url-patterns-access-control)

??? question "31. No access_control rule matches the request. What happens?"
    **✅ Access is allowed (deferred to controller-level guards)**

    access_control only restricts on a matching rule; with no match there is no URL-level restriction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "32. What does requires_channel: https do, and when?"
    **✅ Redirects matching paths to HTTPS before authentication runs**

    The ChannelListener enforces requires_channel before authentication, so even the login page is redirected to HTTPS.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

??? question "33. What does an authenticator's authenticate() method return?"
    **✅ A Passport**

    authenticate() builds a Passport of badges; the token is produced later by createToken() after CheckPassportEvent resolves the badges.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html)

??? question "34. Which passport type suits a valid-API-token flow with no password to verify?"
    **✅ SelfValidatingPassport with a UserBadge**

    When the credential itself proves identity, use SelfValidatingPassport, which carries only a UserBadge — there is nothing further to check.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html#the-passport)

??? question "35. In which namespace does PasswordCredentials live?"
    **✅ Symfony\Component\Security\Http\Authenticator\Passport\Credentials**

    PasswordCredentials and CustomCredentials live under Passport\\Credentials; UserBadge, CsrfTokenBadge, RememberMeBadge, PasswordUpgradeBadge and PreAuthenticatedUserBadge live under Passport\\Badge.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport)

??? question "36. Which built-in authenticator uses a token_handler returning a UserBadge?"
    **✅ access_token**

    The access_token authenticator delegates to an AccessTokenHandlerInterface whose getUserBadgeFrom() validates the bearer token and returns a UserBadge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/access_token.html)

??? question "37. What is the default AccessDecisionManager strategy?"
    **✅ affirmative**

    Affirmative is the default: access is granted if at least one voter returns ACCESS_GRANTED.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html#changing-the-access-decision-strategy)

??? question "38. The base Voter's supports() returns false. What is the resulting vote?"
    **✅ ACCESS_ABSTAIN**

    The abstract Voter abstains for unsupported attributes/subjects; it never calls voteOnAttribute() in that case.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/Voter.php)

??? question "39. All voters abstain and allow_if_all_abstain keeps its default. Result?"
    **✅ Access is denied**

    allow_if_all_abstain defaults to false, so if every voter abstains and no one grants, access is denied.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

??? question "40. What are the integer values of the voter constants?"
    **✅ ACCESS_GRANTED = 1, ACCESS_ABSTAIN = 0, ACCESS_DENIED = -1**

    These integer constants drive the strategy arithmetic in the AccessDecisionManager.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/VoterInterface.php)

??? question "41. Under the unanimous strategy, one voter denies while another grants. Outcome?"
    **✅ Access is denied — unanimous grants only if no voter denies**

    unanimous requires that no voter denies. A single ACCESS_DENIED blocks access regardless of grants (unlike affirmative).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

---

<small>Back to [Flashcards](index.md) · [Security](../../security/index.md)</small>

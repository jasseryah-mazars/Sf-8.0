# Chapter Exam — Security

!!! abstract "How to use"
    78 questions spanning every subchapter of **Security**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Security](../security/index.md).

---

**Q1.** What is the status of enable_authenticator_manager in Symfony 8?  <small>_(easy · trap)_</small>

- A. Removed — the authenticator system is the only one
- B. Required and must be set to true
- C. Optional, defaults to false
- D. Renamed to authenticator_manager: true

??? success "Answer Q1"
    **A**

    The key existed and was deprecated in 7.x; Symfony 8 removed it entirely because the legacy authentication system is gone.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q2.** True or False: a firewall with stateless: true restores the authenticated token from the session on the next request.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q2"
    **B**

    False. stateless: true means the ContextListener is not registered, so no token is written to or restored from the session. Each request starts with empty token storage and must re-authenticate (e.g. re-read the bearer token). Session-backed restore is a property of stateful firewalls only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q3.** Which check can pass a subject to voters?  <small>_(easy · single)_</small>

- A. isGranted('EDIT', $post)
- B. An access_control rule
- C. role_hierarchy configuration
- D. The firewall pattern

??? success "Answer Q3"
    **A**

    Only the isGranted()/#[IsGranted]/denyAccessUnlessGranted() path carries a subject. access_control is URL-based and cannot pass a subject.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html)

**Q4.** isGranted() ultimately delegates the decision to which interface?  <small>_(easy · single)_</small>

- A. AccessDecisionManagerInterface
- B. AuthenticatorInterface
- C. UserProviderInterface
- D. TokenStorageInterface

??? success "Answer Q4"
    **A**

    AuthorizationChecker reads the current token from TokenStorage, then calls AccessDecisionManager::decide().

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/AccessDecisionManager.php)

**Q5.** The password_hashers map in security.yaml is keyed by…  <small>_(easy · config)_</small>

- A. A user class or interface name
- B. A firewall name
- C. A provider name
- D. An algorithm name

??? success "Answer Q5"
    **A**

    You map a user class (commonly PasswordAuthenticatedUserInterface) to an algorithm such as 'auto'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html)

**Q6.** Which of these are valid top-level keys under security: in Symfony 8? (choose 4)  <small>_(easy · multiple)_</small>

- A. providers
- B. firewalls
- C. access_control
- D. role_hierarchy
- E. enable_authenticator_manager

??? success "Answer Q6"
    **A, B, C, D**

    providers, firewalls, access_control, password_hashers and role_hierarchy are the core keys of security.yaml. enable_authenticator_manager was removed in Symfony 8 — the authenticator system is the only one — so it is not a valid key anymore.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/security.html)

**Q7.** Which method loads a user by identifier in Symfony 8?  <small>_(easy · single)_</small>

- A. loadUserByIdentifier()
- B. loadUserByUsername()
- C. findUser()
- D. getUser()

??? success "Answer Q7"
    **A**

    loadUserByUsername() was removed; the UserProviderInterface loader is loadUserByIdentifier().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/user_providers.html)

**Q8.** True or False: a firewall with stateless: true still calls refreshUser() on every request.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q8"
    **B**

    False. refreshUser() is invoked by the ContextListener, which only exists on stateful firewalls. A stateless firewall stores no token in the session, so there is nothing to refresh — the user is re-loaded from scratch by the authenticator on each request instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/user_providers.html)

**Q9.** How many firewalls are active for a given request?  <small>_(easy · single)_</small>

- A. Exactly one — the first whose matcher matches
- B. All firewalls that match
- C. One per HTTP method
- D. Zero or many

??? success "Answer Q9"
    **A**

    The FirewallMap returns the first matching FirewallContext; matching stops there.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#the-firewall)

**Q10.** Which methods does UserInterface declare in Symfony 8?  <small>_(easy · trap)_</small>

- A. getRoles() and getUserIdentifier()
- B. getUsername() and getRoles()
- C. getRoles(), getUserIdentifier() and eraseCredentials()
- D. getId() and getPassword()

??? success "Answer Q10"
    **A**

    Symfony 8 trimmed UserInterface to two methods; eraseCredentials() and getUsername() were removed.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/UserInterface.php)

**Q11.** True or False: UserInterface::getUsername() still exists in Symfony 8.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q11"
    **B**

    False. getUsername() was replaced by getUserIdentifier() (mandatory since 6.0) and no longer exists on UserInterface in Symfony 8. Use getUserIdentifier() for the login identifier the session stores and refreshUser() reloads from.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/UserInterface.php)

**Q12.** Which password algorithm is the recommended default?  <small>_(easy · single)_</small>

- A. auto
- B. plaintext
- C. md5
- D. pbkdf2

??? success "Answer Q12"
    **A**

    'auto' selects the best available algorithm (currently bcrypt) and can adapt over time; it also enables automatic rehash on cost changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html)

**Q13.** Which statement about the plaintext hasher is correct?  <small>_(easy · trap)_</small>

- A. It is intended for tests only and must never be used in production
- B. It is a fast, secure production option
- C. It is the default when none is configured
- D. It enables automatic rehashing

??? success "Answer Q13"
    **A**

    plaintext stores passwords unhashed; it exists to speed up test fixtures and is a production anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html)

**Q14.** In Symfony 8, how do you allow everyone (including not-logged-in) on a path?  <small>_(easy · trap)_</small>

- A. PUBLIC_ACCESS
- B. IS_AUTHENTICATED_ANONYMOUSLY
- C. ROLE_ANONYMOUS
- D. IS_ANONYMOUS

??? success "Answer Q14"
    **A**

    Anonymous tokens were removed; PUBLIC_ACCESS is the attribute that opts a path out of authentication.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q15.** True or False: IS_AUTHENTICATED_ANONYMOUSLY is still a valid access attribute in Symfony 8.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q15"
    **B**

    False. Symfony 8 has no anonymous tokens, so IS_AUTHENTICATED_ANONYMOUSLY no longer exists. To open a path to everyone (including not-logged-in visitors) use PUBLIC_ACCESS instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q16.** How many access_control rules apply to a request?  <small>_(easy · single)_</small>

- A. Only the first matching rule
- B. All rules that match
- C. The most specific match
- D. The last matching rule

??? success "Answer Q16"
    **A**

    AccessMap returns the first match and evaluation stops. Order rules from specific to general.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#securing-url-patterns-access-control)

**Q17.** What does an authenticator's authenticate() method return?  <small>_(easy · single)_</small>

- A. A Passport
- B. A TokenInterface
- C. A Response
- D. A UserInterface

??? success "Answer Q17"
    **A**

    authenticate() builds a Passport of badges; the token is produced later by createToken() after CheckPassportEvent resolves the badges.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/custom_authenticator.html)

**Q18.** Which built-in authenticator uses a token_handler returning a UserBadge?  <small>_(easy · single)_</small>

- A. access_token
- B. form_login
- C. http_basic
- D. remember_me

??? success "Answer Q18"
    **A**

    The access_token authenticator delegates to an AccessTokenHandlerInterface whose getUserBadgeFrom() validates the bearer token and returns a UserBadge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/access_token.html)

**Q19.** What is the default AccessDecisionManager strategy?  <small>_(easy · single)_</small>

- A. affirmative
- B. unanimous
- C. consensus
- D. priority

??? success "Answer Q19"
    **A**

    Affirmative is the default: access is granted if at least one voter returns ACCESS_GRANTED.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html#changing-the-access-decision-strategy)

**Q20.** What are the integer values of the voter constants?  <small>_(easy · internals)_</small>

- A. ACCESS_GRANTED = 1, ACCESS_ABSTAIN = 0, ACCESS_DENIED = -1
- B. GRANTED = 0, DENIED = 1, ABSTAIN = 2
- C. GRANTED = true, DENIED = false
- D. All three are 0

??? success "Answer Q20"
    **A**

    These integer constants drive the strategy arithmetic in the AccessDecisionManager.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/VoterInterface.php)

**Q21.** In Symfony 8, where are a Passport's badges validated?  <small>_(medium · internals)_</small>

- A. Inside the authenticator's authenticate() method
- B. By listeners on the CheckPassportEvent
- C. In createToken()
- D. In the Firewall listener before routing

??? success "Answer Q21"
    **B**

    authenticate() only builds the Passport. Badge resolution and credential verification happen on CheckPassportEvent (UserProviderListener, CheckCredentialsListener, CsrfProtectionListener…).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/custom_authenticator.html)

**Q22.** A stateless firewall (stateless: true) does NOT do which of these?  <small>_(medium · internals)_</small>

- A. Persist the token in the session via ContextListener
- B. Build a Passport
- C. Create a token for the current request
- D. Dispatch CheckPassportEvent

??? success "Answer Q22"
    **A**

    Stateless firewalls skip the ContextListener, so nothing is stored or restored between requests; each request re-authenticates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q23.** An authenticator's supports() returns null. What does that mean?  <small>_(medium · trap)_</small>

- A. Authenticate lazily when the token is needed
- B. The request is rejected
- C. The authenticator never runs
- D. A 500 error is thrown

??? success "Answer Q23"
    **A**

    null means 'unsure — call me lazily'. Many stateless authenticators use it so authentication is deferred until required.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authenticator/AuthenticatorInterface.php)

**Q24.** A controller runs $security->getUser()->getUserIdentifier() and fatals on some requests. What is the cause?  <small>_(medium · debug)_</small>

- A. On an anonymous request getUser() returns null, so calling a method on null fatals; guard with ?->, ?? or an IsGranted check
- B. getUser() throws an AccessDeniedException for guests
- C. getUserIdentifier() was removed in Symfony 8
- D. TokenStorage is not registered as a service

??? success "Answer Q24"
    **A**

    Security::getUser() returns ?UserInterface — it is null whenever no token holds a user (a truly anonymous request, or a lazy firewall whose token was never read). Dereferencing null is a fatal error. Guard with $user?->…, a ?? fallback, or an earlier #[IsGranted('IS_AUTHENTICATED_FULLY')] / denyAccessUnlessGranted() so $user is guaranteed non-null past that point. getUserIdentifier() is very much part of the 8.0 interface, and getUser() never throws for guests — it simply returns null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q25.** A #[IsGranted] check fails for an unauthenticated user. What happens?  <small>_(medium · internals)_</small>

- A. The entry point starts authentication (e.g. login redirect)
- B. An immediate 403 is always returned
- C. A 404 is returned
- D. The request continues unrestricted

??? success "Answer Q25"
    **A**

    An AccessDeniedException for an unauthenticated user is converted to the entry point response; an authenticated-but-unauthorized user gets a 403.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#access-control)

**Q26.** In #[IsGranted('EDIT', subject: 'post')], what does subject: 'post' do?  <small>_(medium · code)_</small>

- A. Passes the controller argument named $post to the voters as the subject of the EDIT decision
- B. Names the voter class that should handle the check
- C. Restricts the route to a {post} placeholder
- D. Combines with EDIT to require the role EDIT_POST

??? success "Answer Q26"
    **A**

    The subject option references a controller argument by name; Symfony resolves $post and passes it to AccessDecisionManager::decide() as the subject, so a voter's voteOnAttribute() receives the actual Post instance and can apply per-object rules (ownership, state). It is not a voter name, a route requirement, or a role suffix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#access-controllers)

**Q27.** Which statement about access_control vs isGranted() is correct?  <small>_(medium · trap)_</small>

- A. access_control is URL-based and cannot pass a subject; only isGranted()/#[IsGranted] can
- B. access_control can pass the matched entity to voters as the subject
- C. Both can pass a subject to voters
- D. Neither reaches voters — access_control uses its own logic

??? success "Answer Q27"
    **A**

    access_control runs through the same AccessDecisionManager and voters as isGranted(), but it only supplies the rule's roles/allow_if — there is no subject, because it matches on the URL, not on a domain object. Per-object decisions ("can edit THIS post?") must use #[IsGranted]/denyAccessUnlessGranted() with a subject. Both do reach voters, so the "neither" option is wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html)

**Q28.** Which of these funnel through AuthorizationCheckerInterface::isGranted()? (choose 3)  <small>_(medium · multiple)_</small>

- A. The #[IsGranted] attribute
- B. denyAccessUnlessGranted() in a controller
- C. Twig's is_granted() function
- D. A user provider's loadUserByIdentifier()

??? success "Answer Q28"
    **A, B, C**

    #[IsGranted], denyAccessUnlessGranted() and Twig's is_granted() are all thin wrappers over AuthorizationCheckerInterface::isGranted(), which delegates to the AccessDecisionManager and voters. loadUserByIdentifier() belongs to the authentication/provider layer (loading users), not authorization, so it does not go through isGranted().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#access-control-authorization)

**Q29.** Two providers are defined and a firewall omits the provider key. Result?  <small>_(medium · trap)_</small>

- A. Configuration error — the provider is ambiguous
- B. It silently uses the first provider
- C. It merges both providers
- D. The firewall becomes anonymous

??? success "Answer Q29"
    **A**

    With multiple providers there is no implicit default; each firewall must name its provider explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/user_providers.html)

**Q30.** Why must the dev firewall (security: false) be listed first?  <small>_(medium · internals)_</small>

- A. Firewalls are first-match, so it must precede protecting firewalls
- B. Alphabetical ordering is enforced
- C. It sets global defaults for later firewalls
- D. Order is irrelevant for firewalls

??? success "Answer Q30"
    **A**

    Firewall matching is top-to-bottom, first match wins. Listing the dev firewall first stops the profiler/assets being intercepted by login.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#the-firewall)

**Q31.** Requests under /api are being handled by the session-based main firewall instead of the stateless api firewall. What is wrong?  <small>_(medium · debug)_</small>

- A. The catch-all main firewall is listed before api; firewalls are first-match, so api must come first
- B. You must set enable_authenticator_manager: true for the api firewall
- C. stateless: true disables pattern matching on that firewall
- D. Defining two providers makes the api firewall be skipped

??? success "Answer Q31"
    **A**

    Firewalls match top-to-bottom, first match wins. A catch-all main firewall (no pattern) placed before api matches every request, so /api never reaches the stateless firewall. Move the specific ^/api firewall above main. enable_authenticator_manager no longer exists in Symfony 8, stateless does not affect matching, and multiple providers do not skip a firewall.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#the-firewall)

**Q32.** How do you configure eraseCredentials behaviour in security.yaml in Symfony 8?  <small>_(medium · trap)_</small>

- A. You don't — eraseCredentials() was removed in 8.0; strip secrets in the user's __serialize()
- B. Add erase_credentials: true under each firewall
- C. Set it inside the password_hashers map
- D. It is enabled by default via the erase_credentials key

??? success "Answer Q32"
    **A**

    There is no eraseCredentials configuration key, and there never was — it was a UserInterface method. In Symfony 8 both UserInterface::eraseCredentials() and TokenInterface::eraseCredentials() were removed; the documented replacement is to strip sensitive data (the password) in your user's __serialize() method, which is what runs when the token/user is stored in the session.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/UPGRADE-8.0.md)

**Q33.** When is refreshUser() called?  <small>_(medium · internals)_</small>

- A. On every stateful request, to re-sync the session user
- B. Only during the login request
- C. Never for custom providers
- D. Only on logout

??? success "Answer Q33"
    **A**

    The ContextListener refreshes the stored user on each request of a stateful firewall; a stateless firewall never calls it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall/ContextListener.php)

**Q34.** Does a user provider verify the user's password?  <small>_(medium · trap)_</small>

- A. No — credentials are checked on CheckPassportEvent
- B. Yes, in loadUserByIdentifier()
- C. Yes, in refreshUser()
- D. Only the memory provider does

??? success "Answer Q34"
    **A**

    Providers only load and refresh users. CheckCredentialsListener verifies the PasswordCredentials badge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/custom_authenticator.html)

**Q35.** A custom provider does `return $repo->find($id);` in loadUserByIdentifier() and sometimes throws a TypeError. What is the fix?  <small>_(medium · debug)_</small>

- A. find() can return null but the return type is a non-nullable UserInterface; throw UserNotFoundException when no user matches
- B. loadUserByIdentifier() must return an array of users
- C. The method must be renamed to loadUserByUsername()
- D. Return false instead of the user object

??? success "Answer Q35"
    **A**

    loadUserByIdentifier(): UserInterface has a non-nullable return type. Returning null (as find() may) is a contract violation and causes a TypeError. When no user matches you must throw UserNotFoundException, which Symfony normalises to a generic BadCredentialsException so an attacker cannot distinguish "unknown user" from "wrong password". You never return null or false, and the method returns a single UserInterface, not an array.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/user_providers.html)

**Q36.** A provider is configured as `all_users: { chain: { providers: [in_memory, api_users] } }`. What does it do?  <small>_(medium · config)_</small>

- A. Tries each listed provider in order; the first that supports/loads the user wins
- B. Merges the users from both providers into a single set
- C. Requires the user to exist in both providers to authenticate
- D. Picks one of the providers at random per request

??? success "Answer Q36"
    **A**

    A chain provider delegates to its sub-providers in the declared order and returns the first successful match; if none support/find the user it throws. It does not merge users, require presence in all providers, or choose randomly. Correct supportsClass()/UnsupportedUserException handling in each sub-provider is what lets the chain fall through cleanly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/user_providers.html#chaining-user-providers)

**Q37.** What does security: false on a firewall do?  <small>_(medium · internals)_</small>

- A. Disables the security layer for that zone (and still counts as the match)
- B. Denies all access to that zone
- C. Enables anonymous voting
- D. Makes the firewall stateless

??? success "Answer Q37"
    **A**

    It turns off all security listeners for matching requests (used for the profiler and dev assets) and, being first-match, prevents later firewalls from matching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q38.** Two firewalls should share a logged-in session. What do you configure?  <small>_(medium · single)_</small>

- A. The same context: name on both firewalls
- B. The same provider on both
- C. stateless: true on both
- D. Nothing — sharing is automatic

??? success "Answer Q38"
    **A**

    Token sharing between firewalls requires an explicit matching context key; otherwise each firewall keeps its own token.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q39.** What does lazy: true achieve on a firewall?  <small>_(medium · internals)_</small>

- A. Authentication is deferred until the token is actually read
- B. It disables the session entirely
- C. It caches the authenticated token forever
- D. It runs all authenticators eagerly on every request

??? success "Answer Q39"
    **A**

    A lazy firewall only authenticates when the token is accessed (e.g. is_granted/getUser), so fully public pages skip auth and session loading.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q40.** A firewall configured with `pattern: /api` unexpectedly also intercepts /my-api-docs. Why?  <small>_(medium · debug)_</small>

- A. pattern is a regex; without a leading ^ it matches anywhere in the path. Anchor it as ^/api
- B. Symfony matches patterns as substrings and cannot be anchored
- C. /my-api-docs is physically located under /api
- D. You must also set methods: to make patterns exact

??? success "Answer Q40"
    **A**

    Firewall pattern is an unanchored regular expression, so /api matches any path containing that sequence — including /my-api-docs. Anchoring with ^ (^/api) fixes it to the start of the path. Patterns are regexes (anchorable), the doc route is unrelated to physical location, and methods: narrows HTTP verbs, not path matching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#the-firewall)

**Q41.** Given firewalls declared as main (no pattern) then api (pattern: ^/api), what happens to /api requests?  <small>_(medium · trap)_</small>

- A. main (the catch-all) matches first, so /api never reaches the api firewall; list api first
- B. Both firewalls run in sequence for /api
- C. api wins because its pattern is more specific
- D. A container compile error is thrown for overlapping firewalls

??? success "Answer Q41"
    **A**

    Firewall selection is first-match, top-to-bottom — not most-specific-wins. A patternless main firewall matches everything, so it swallows /api before the api firewall is considered. The fix is ordering: specific firewalls (^/api) before the catch-all. Symfony does not run multiple firewalls per request, nor does it error on overlap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#the-firewall)

**Q42.** How do you keep a user's password out of the session in Symfony 8?  <small>_(medium · code)_</small>

- A. Override __serialize() and unset the password field
- B. Implement eraseCredentials()
- C. Annotate the property with #[Ignore]
- D. It happens automatically with no code

??? success "Answer Q42"
    **A**

    eraseCredentials() was removed in 8.0; the documented replacement is to strip sensitive data in __serialize().

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/UPGRADE-8.0.md)

**Q43.** Which interface declares getPassword()?  <small>_(medium · trap)_</small>

- A. PasswordAuthenticatedUserInterface
- B. UserInterface
- C. EquatableInterface
- D. PasswordUpgraderInterface

??? success "Answer Q43"
    **A**

    getPassword(): ?string is declared by PasswordAuthenticatedUserInterface, an opt-in interface — not by UserInterface (which only has getRoles() and getUserIdentifier() in 8.0). EquatableInterface adds isEqualTo(); PasswordUpgraderInterface (a provider concern) adds upgradePassword(). A token-only/SSO user may skip PasswordAuthenticatedUserInterface entirely.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/PasswordAuthenticatedUserInterface.php)

**Q44.** A token-only API user declares getPassword(): string. Login works, but the security layer throws a TypeError when serialising the user. Why?  <small>_(medium · debug)_</small>

- A. Such a user has no local password, so the stored hash is null; getPassword() must be typed ?string
- B. getPassword() must return an int hash code
- C. The method has to be named getHash() in Symfony 8
- D. You must also implement eraseCredentials()

??? success "Answer Q44"
    **A**

    PasswordAuthenticatedUserInterface::getPassword() is typed ?string precisely because passwordless accounts (OAuth/LDAP/token-only) legitimately have a null hash. Declaring a non-nullable string return type makes PHP throw a TypeError the moment null is returned during verification or serialization. The CheckCredentialsListener treats a null hash as non-verifiable. The method name and return type are fixed by the interface, and eraseCredentials() no longer exists.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#the-user)

**Q45.** Where is a login password actually verified?  <small>_(medium · internals)_</small>

- A. In CheckCredentialsListener on CheckPassportEvent
- B. In the user's getPassword() method
- C. In the user provider
- D. In the controller action

??? success "Answer Q45"
    **A**

    The authenticator adds a PasswordCredentials badge; the listener verifies it against the hash using the configured hasher.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/custom_authenticator.html)

**Q46.** A hasher entry is `algorithm: sodium, migrate_from: ['bcrypt']`. What does it mean?  <small>_(medium · config)_</small>

- A. Hash new passwords with sodium, but still accept existing bcrypt hashes and upgrade them on the next successful login
- B. Reject any password stored with bcrypt
- C. Hash with bcrypt and verify with sodium
- D. Store each password hashed by both algorithms at once

??? success "Answer Q46"
    **A**

    The primary algorithm (sodium/Argon2id) is used to hash new passwords, while migrate_from lists legacy algorithms whose hashes are still verifiable. On a valid login against an old bcrypt hash, needsRehash() returns true and the PasswordUpgradeBadge flow rehashes with sodium and persists it — transparent, no reset. It does not reject bcrypt, swap hashing/verifying roles, or double-hash.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html#password-migration)

**Q47.** Which special attribute is broader?  <small>_(medium · trap)_</small>

- A. IS_AUTHENTICATED_REMEMBERED (fully-authenticated users also satisfy it)
- B. IS_AUTHENTICATED_FULLY
- C. They are equal
- D. Neither implies the other

??? success "Answer Q47"
    **A**

    Fully-authenticated users satisfy IS_AUTHENTICATED_REMEMBERED, but remember-me users do NOT satisfy IS_AUTHENTICATED_FULLY.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#security-authorization-access-decision)

**Q48.** An attribute 'EDITOR' (no ROLE_ prefix) is checked. How does RoleVoter treat it?  <small>_(medium · single)_</small>

- A. It is ignored — RoleVoter only handles ROLE_-prefixed attributes
- B. Granted if the user has it
- C. Always denied
- D. It throws an exception

??? success "Answer Q48"
    **A**

    RoleVoter supports only ROLE_* attributes; unprefixed strings abstain there (a custom voter could still handle them).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#roles)

**Q49.** Given role_hierarchy ROLE_ADMIN: [ROLE_USER], a user with ROLE_ADMIN…  <small>_(medium · internals)_</small>

- A. Is also granted ROLE_USER (reachable roles are expanded)
- B. Is not granted ROLE_USER
- C. Loses ROLE_ADMIN
- D. Must re-login to gain ROLE_USER

??? success "Answer Q49"
    **A**

    RoleHierarchyVoter expands reachable roles, so ROLE_ADMIN transitively includes ROLE_USER. Hierarchy flows downward.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#hierarchical-roles)

**Q50.** With role_hierarchy ROLE_ADMIN: [ROLE_USER] and ROLE_SUPER_ADMIN: [ROLE_ADMIN], which roles does a ROLE_SUPER_ADMIN user satisfy?  <small>_(medium · config)_</small>

- A. ROLE_SUPER_ADMIN, ROLE_ADMIN and ROLE_USER (transitively reachable)
- B. Only ROLE_SUPER_ADMIN
- C. ROLE_SUPER_ADMIN and ROLE_ADMIN only
- D. Every role defined anywhere in the map

??? success "Answer Q50"
    **A**

    RoleHierarchy::getReachableRoleNames() expands roles transitively: ROLE_SUPER_ADMIN reaches ROLE_ADMIN, which reaches ROLE_USER, so the user satisfies all three. Inheritance flows downward and is transitive (not just one level), but it does not grant unrelated roles that are not on the reachable path.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Role/RoleHierarchy.php)

**Q51.** Which attribute protects a 'change email' action so that a remember-me cookie is not sufficient?  <small>_(medium · scenario)_</small>

- A. IS_AUTHENTICATED_FULLY
- B. IS_AUTHENTICATED_REMEMBERED
- C. IS_AUTHENTICATED
- D. PUBLIC_ACCESS

??? success "Answer Q51"
    **A**

    IS_AUTHENTICATED_FULLY is granted only to users who authenticated fresh in the current session — not via a remember-me cookie. A stolen remember-me cookie satisfies IS_AUTHENTICATED_REMEMBERED and IS_AUTHENTICATED, so those would wrongly permit a sensitive identity change; PUBLIC_ACCESS allows everyone. Use _FULLY to force a fresh login for payments/identity changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#security-authorization-access-decision)

**Q52.** A rule has roles: [ROLE_A, ROLE_B]. Access is granted when the user has…  <small>_(medium · single)_</small>

- A. Either ROLE_A or ROLE_B
- B. Both ROLE_A and ROLE_B
- C. Neither
- D. Exactly one of them

??? success "Answer Q52"
    **A**

    Multiple roles within a single access_control rule are OR-combined.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#securing-url-patterns-access-control)

**Q53.** No access_control rule matches the request. What happens?  <small>_(medium · trap)_</small>

- A. Access is allowed (deferred to controller-level guards)
- B. 403 Forbidden
- C. 401 Unauthorized
- D. The firewall re-authenticates

??? success "Answer Q53"
    **A**

    access_control only restricts on a matching rule; with no match there is no URL-level restriction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q54.** What does requires_channel: https do, and when?  <small>_(medium · internals)_</small>

- A. Redirects matching paths to HTTPS before authentication runs
- B. Rejects HTTPS requests
- C. Runs only after a successful login
- D. Encrypts the session cookie

??? success "Answer Q54"
    **A**

    The ChannelListener enforces requires_channel before authentication, so even the login page is redirected to HTTPS.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q55.** After adding { path: ^/, roles: PUBLIC_ACCESS } at the top of access_control, the ^/admin rule below stops protecting admin. Why?  <small>_(medium · debug)_</small>

- A. First match wins; ^/ matches every path including /admin, so the catch-all is enforced and the admin rule is never reached
- B. PUBLIC_ACCESS globally disables all other access_control rules
- C. roles must be given as a list, not a string, to take effect
- D. The admin rule needs a requires_channel to be evaluated

??? success "Answer Q55"
    **A**

    access_control is first-match, top-to-bottom. ^/ matches all paths, so placing it first means /admin hits the PUBLIC_ACCESS rule and the ^/admin rule underneath is never evaluated — admin becomes public. Order specific rules before the ^/ catch-all. PUBLIC_ACCESS is a normal attribute (it does not disable other rules), and the roles syntax/requires_channel are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#securing-url-patterns-access-control)

**Q56.** Which passport type suits a valid-API-token flow with no password to verify?  <small>_(medium · scenario)_</small>

- A. SelfValidatingPassport with a UserBadge
- B. Passport with an empty PasswordCredentials
- C. PreAuthenticatedToken
- D. UsernamePasswordToken

??? success "Answer Q56"
    **A**

    When the credential itself proves identity, use SelfValidatingPassport, which carries only a UserBadge — there is nothing further to check.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/custom_authenticator.html#the-passport)

**Q57.** In which namespace does PasswordCredentials live?  <small>_(medium · trap)_</small>

- A. Symfony\Component\Security\Http\Authenticator\Passport\Credentials
- B. Symfony\Component\Security\Http\Authenticator\Passport\Badge
- C. Symfony\Component\Security\Core\Authentication\Token
- D. Symfony\Component\Security\Http\EntryPoint

??? success "Answer Q57"
    **A**

    PasswordCredentials and CustomCredentials live under Passport\\Credentials; UserBadge, CsrfTokenBadge, RememberMeBadge, PasswordUpgradeBadge and PreAuthenticatedUserBadge live under Passport\\Badge.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport)

**Q58.** Which of these live in Passport\Badge (i.e. are badges, not credentials)? (choose 3)  <small>_(medium · multiple)_</small>

- A. UserBadge
- B. CsrfTokenBadge
- C. RememberMeBadge
- D. PasswordCredentials

??? success "Answer Q58"
    **A, B, C**

    UserBadge, CsrfTokenBadge, RememberMeBadge (plus PasswordUpgradeBadge and PreAuthenticatedUserBadge) live under Passport\\Badge. PasswordCredentials — like CustomCredentials — lives under Passport\\Credentials, not Badge. This namespace split is a classic exam distinction.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport)

**Q59.** What does AbstractLoginFormAuthenticator provide that AbstractAuthenticator does not?  <small>_(medium · internals)_</small>

- A. supports() (POST to the check path), the entry point via getLoginUrl(), and a default onAuthenticationFailure() that redirects back to the login page
- B. A default authenticate() that verifies the password for you
- C. The CheckPassportEvent listeners themselves
- D. The firewall's user provider
- E. A createToken() that returns a PostAuthenticationToken

??? success "Answer Q59"
    **A**

    AbstractLoginFormAuthenticator adds form-login plumbing on top of AbstractAuthenticator: supports() (POST to the check path), the entry point start() built from the abstract getLoginUrl(), and a default onAuthenticationFailure() redirecting to the login page — leaving you to write authenticate(), getLoginUrl() and onAuthenticationSuccess(). It does not verify passwords (that is CheckCredentialsListener), does not own the event listeners or the provider; and returning a PostAuthenticationToken is AbstractAuthenticator's default, which FormLoginAuthenticator overrides to a UsernamePasswordToken.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authenticator/AbstractLoginFormAuthenticator.php)

**Q60.** The base Voter's supports() returns false. What is the resulting vote?  <small>_(medium · internals)_</small>

- A. ACCESS_ABSTAIN
- B. ACCESS_DENIED
- C. ACCESS_GRANTED
- D. An exception is thrown

??? success "Answer Q60"
    **A**

    The abstract Voter abstains for unsupported attributes/subjects; it never calls voteOnAttribute() in that case.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/Voter.php)

**Q61.** All voters abstain and allow_if_all_abstain keeps its default. Result?  <small>_(medium · trap)_</small>

- A. Access is denied
- B. Access is granted
- C. It depends on the user's roles
- D. An exception is thrown

??? success "Answer Q61"
    **A**

    allow_if_all_abstain defaults to false, so if every voter abstains and no one grants, access is denied.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html)

**Q62.** In a Voter, voteOnAttribute() starts with `if (!$user instanceof AppUser) { return false; }`. Why return false rather than abstain?  <small>_(medium · code)_</small>

- A. supports() already accepted the attribute, so this voter owns the decision; with no valid user it must deny — abstaining would wrongly delegate an attribute it claimed
- B. It should really return ACCESS_ABSTAIN there instead
- C. $token->getUser() can never be null, so the branch is dead code
- D. It should throw an AccessDeniedException from the voter

??? success "Answer Q62"
    **A**

    By the time voteOnAttribute() runs, supports() has already said "this attribute/subject is mine", so the voter must return a real yes/no. An unauthenticated request carries a NullToken whose getUser() is null (or a user of the wrong class), so there is nobody to authorize — deny (return false). Abstaining would contradict supports(); getUser() genuinely can be null; and voters signal decisions via return values, not by throwing.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html)

**Q63.** With access_decision_manager.strategy set to priority, how is the decision made?  <small>_(medium · config)_</small>

- A. The first voter that does not abstain decides the outcome
- B. All voters must agree to grant
- C. The majority of grants over denies wins
- D. A single grant is always enough regardless of order

??? success "Answer Q63"
    **A**

    The priority strategy takes the vote of the first (highest-priority) non-abstaining voter as final, letting a high-priority voter short-circuit (e.g. a global "banned user" voter denying before feature voters run). "All must agree" describes unanimous, "majority" describes consensus, and "one grant is enough" describes affirmative.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html#changing-the-access-decision-strategy)

**Q64.** During a successful login, in which order does the AuthenticatorManager dispatch these events?  <small>_(hard · internals)_</small>

- A. CheckPassportEvent → AuthenticationTokenCreatedEvent → LoginSuccessEvent
- B. LoginSuccessEvent → CheckPassportEvent → AuthenticationTokenCreatedEvent
- C. AuthenticationTokenCreatedEvent → CheckPassportEvent → LoginSuccessEvent
- D. CheckPassportEvent → LoginSuccessEvent → AuthenticationTokenCreatedEvent

??? success "Answer Q64"
    **A**

    authenticate() builds the Passport; CheckPassportEvent listeners then resolve the badges; createToken() runs; AuthenticationTokenCreatedEvent is the last chance to swap/decorate the token; the token is stored; finally LoginSuccessEvent fires (invoking onAuthenticationSuccess()). On error a LoginFailureEvent is dispatched instead. Any ordering that runs LoginSuccessEvent before the passport is checked, or creates the token before CheckPassportEvent, contradicts the manager's pipeline.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authentication/AuthenticatorManager.php)

**Q65.** On a logged-out request, what does isGranted('ROLE_ADMIN') do internally?  <small>_(hard · internals)_</small>

- A. The AuthorizationChecker substitutes a NullToken and voters run; RoleVoter finds no matching role and it returns a clean false
- B. It throws because the token in storage is null
- C. It returns true because no access_control rule restricts it
- D. It redirects to the firewall entry point

??? success "Answer Q65"
    **A**

    When TokenStorage holds no token, AuthorizationChecker substitutes a NullToken rather than crashing, and voting proceeds normally. RoleVoter finds ROLE_ADMIN is not present, so the decision is false — not an exception. (AuthenticatedVoter denies the IS_AUTHENTICATED_* attributes for a NullToken, while PUBLIC_ACCESS still grants.) Authorization never starts authentication by itself; only an AccessDeniedException handled by the firewall triggers the entry point.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authentication/Token/NullToken.php)

**Q66.** For each firewall, what does SecurityExtension compile at container build time?  <small>_(hard · internals)_</small>

- A. A FirewallContext bundling its listeners, the authenticator list, an AuthenticatorManager, and (unless stateless) a ContextListener — all indexed in a FirewallMap
- B. A single global Firewall service shared unchanged by every firewall
- C. One controller per firewall generated from the config
- D. Nothing at build time — firewalls are assembled lazily on the first request

??? success "Answer Q66"
    **A**

    SecurityExtension reads the security.yaml tree and, per firewall, compiles a dedicated FirewallContext (its listeners, the list of authenticators, an AuthenticatorManager, an exception listener, and a ContextListener unless the firewall is stateless). All contexts are registered in the FirewallMap; at runtime the single Firewall listener asks the map which context matches. The work happens at compile time, not lazily per request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/SecurityBundle/DependencyInjection/SecurityExtension.php)

**Q67.** An admin deletes a user's account while that user is browsing under a stateful firewall. What happens on the user's next request?  <small>_(hard · scenario)_</small>

- A. refreshUser() can no longer load them and throws; the ContextListener discards the token, effectively logging them out
- B. Nothing changes until the PHP session cookie expires
- C. A fatal 500 error is returned on every request
- D. The user keeps full access until they click logout

??? success "Answer Q67"
    **A**

    On each stateful request the ContextListener calls refreshUser() to re-sync the session user. A now-missing account makes refreshUser() throw (UserNotFoundException / UnsupportedUserException), so the ContextListener treats the user as unloadable, discards the token and clears storage — an immediate, clean logout. It is not a fatal error, and access does not persist until the cookie expires precisely because the user is re-checked every request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall/ContextListener.php)

**Q68.** When does the Firewall listener run in the kernel lifecycle?  <small>_(hard · internals)_</small>

- A. On kernel.request at priority 8 (after routing), it asks the FirewallMap for the first matching FirewallContext
- B. On kernel.controller, just before the controller is resolved
- C. On kernel.response, after the action has run
- D. On kernel.terminate, asynchronously after the response
- E. On kernel.request but before routing, at the highest priority

??? success "Answer Q68"
    **A**

    The Firewall listener subscribes to kernel.request at priority 8, which runs after the RouterListener (routing), then queries the FirewallMap for the matching FirewallContext and runs its listeners. It is a request-phase concern, not controller/response/terminate, and it deliberately runs after routing so route attributes are available.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall.php)

**Q69.** isEqualTo() returns false when a stored user is refreshed. Effect?  <small>_(hard · internals)_</small>

- A. The token is invalidated — the user is logged out
- B. Nothing happens
- C. The password is rehashed
- D. A 500 error is thrown

??? success "Answer Q69"
    **A**

    A negative EquatableInterface comparison on refresh tells the framework the stored identity is stale, so the token is dropped.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/EquatableInterface.php)

**Q70.** You need a user's role change to immediately end their existing sessions. What do you implement?  <small>_(hard · scenario)_</small>

- A. EquatableInterface::isEqualTo() comparing roles; returning false on refresh invalidates the token
- B. An eraseCredentials() override that clears the roles
- C. A kernel listener that calls logout() on every request
- D. Setting stateless: true on the firewall

??? success "Answer Q70"
    **A**

    When a user implements EquatableInterface, the ContextListener compares the session copy with the freshly refreshed user on each request via isEqualTo(). Including getRoles() in that comparison means a role change yields false, which invalidates the token and logs the user out immediately. eraseCredentials() no longer exists; a manual logout-everywhere listener is crude; and stateless would drop sessions entirely rather than invalidate on change.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/EquatableInterface.php)

**Q71.** Transparent password rehash on login requires…  <small>_(hard · internals)_</small>

- A. Both migrate_from and a provider implementing PasswordUpgraderInterface
- B. Only migrate_from in security.yaml
- C. Only a PasswordUpgraderInterface provider
- D. Calling password_hash() manually in the controller

??? success "Answer Q71"
    **A**

    migrate_from lets needsRehash() detect the old hash; the PasswordUpgradeBadge triggers PasswordMigratingListener, which persists the new hash via upgradePassword().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html#password-migration)

**Q72.** A user with a very long passphrase can change the trailing characters and still log in. Which hasher is in use and why?  <small>_(hard · trap)_</small>

- A. bcrypt — it truncates input at 72 bytes, so bytes beyond that are ignored
- B. sodium — Argon2id trims trailing whitespace
- C. auto — it hashes only the first word of the input
- D. pbkdf2 — it lowercases the input before hashing

??? success "Answer Q72"
    **A**

    bcrypt has a hard 72-byte input limit; any bytes past 72 are silently ignored, so two passphrases sharing the first 72 bytes verify identically. Very long passphrases therefore lose entropy under bcrypt. sodium (Argon2id) has no such truncation, which is one reason to prefer it for long secrets. The other options invent behaviour that does not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html)

**Q73.** You set migrate_from and needsRehash() returns true, yet stored hashes are never upgraded. What is missing?  <small>_(hard · debug)_</small>

- A. The user provider does not implement PasswordUpgraderInterface, so upgradePassword() is never called to persist the new hash
- B. migrate_from only works with the plaintext algorithm
- C. You must call password_hash() yourself in the controller
- D. needsRehash() is not supported in Symfony 8

??? success "Answer Q73"
    **A**

    migrate_from + needsRehash() computes a fresh hash, but persisting it is the provider's job: only a provider implementing PasswordUpgraderInterface's upgradePassword() actually stores it (triggered by the PasswordUpgradeBadge / PasswordMigratingListener). Without it, the rehash is computed and discarded every login. migrate_from is not plaintext-only, you must not hash manually, and needsRehash() is fully supported.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html#password-migration)

**Q74.** Can an access_control rule pass the matched entity to a voter as the subject?  <small>_(hard · trap)_</small>

- A. No — access_control has no subject; it calls AccessDecisionManager with only roles/allow_if. Use #[IsGranted] with a subject for per-object rules
- B. Yes, via a subject: key on the rule
- C. Yes, the matched path parameter is passed as the subject
- D. Only when allow_if is also set

??? success "Answer Q74"
    **A**

    access_control routes through the same AccessDecisionManager and voters as isGranted(), but it is purely URL-driven: the AccessListener calls decide() with the rule's roles/expression and no subject. There is no subject: key and path parameters are not passed as subjects. Per-object decisions require #[IsGranted]/denyAccessUnlessGranted() with an explicit subject.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html)

**Q75.** A rule sets both roles: ROLE_USER and an allow_if expression. When is access granted?  <small>_(hard · config)_</small>

- A. Only when BOTH the role check and the expression pass (AND)
- B. When either the role or the expression passes (OR)
- C. Only the expression is evaluated; roles is ignored
- D. Only roles is evaluated; allow_if is ignored

??? success "Answer Q75"
    **A**

    Within one rule, multiple roles are OR-combined, but when roles and allow_if are both present they must BOTH pass — it is an AND. (allow_if runs the expression through the ExpressionVoter.) Neither key is ignored, and combining them does not turn the rule into an OR.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/expressions.html)

**Q76.** An authenticator adds a badge that no CheckPassportEvent listener resolves. What happens?  <small>_(hard · internals)_</small>

- A. Passport::checkIfCompletelyResolved() throws, so authentication fails — you cannot forget to validate a badge
- B. The badge is silently ignored and login proceeds
- C. The token is created with the unresolved badge attached
- D. A raw 500 with no security exception is produced

??? success "Answer Q76"
    **A**

    After CheckPassportEvent, the manager calls Passport::checkIfCompletelyResolved(), which throws if any badge was never marked resolved. This is a deliberate safety net: an unregistered/forgotten badge (e.g. a CsrfTokenBadge with no listener) fails authentication as an AuthenticationException rather than letting an unverified credential slip through. It is neither ignored nor attached to a successful token.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport)

**Q77.** Under the unanimous strategy, one voter denies while another grants. Outcome?  <small>_(hard · scenario)_</small>

- A. Access is denied — unanimous grants only if no voter denies
- B. Access is granted — one grant is enough
- C. The tie is resolved by roles
- D. An exception is thrown

??? success "Answer Q77"
    **A**

    unanimous requires that no voter denies. A single ACCESS_DENIED blocks access regardless of grants (unlike affirmative).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html)

**Q78.** Under the unanimous strategy, a voter returns false from voteOnAttribute() for an attribute it does not actually care about. Effect?  <small>_(hard · trap)_</small>

- A. false is ACCESS_DENIED, which blocks access under unanimous; unrelated attributes must be filtered out in supports() so the voter abstains
- B. false is treated as abstain and has no effect on the outcome
- C. false grants access under unanimous
- D. It throws because the attribute is unsupported

??? success "Answer Q78"
    **A**

    Returning false from voteOnAttribute() maps to ACCESS_DENIED, not abstain. Under unanimous a single deny blocks access, so a voter that "says no to what isn't mine" silently breaks authorization. The correct pattern is to reject unrelated attributes/subjects in supports(), which makes the base Voter abstain (ACCESS_ABSTAIN, no effect). abstain and deny are distinct, and an unsupported attribute does not throw.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/Voter.php)

---

<small>Back to [Chapter Exams](index.md) · [Security](../security/index.md)</small>

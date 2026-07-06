# Lab: Custom Voter — Fine-Grained Authorization (`POST_EDIT`)

<!--
PRACTICAL LAB — Security. Mode: TDD (code behaviour: a Voter you instantiate and assert on).
All code: Symfony 8 / PHP 8.4. Complete <?php snippets compile with php -l.
-->

!!! abstract "Practical Lab"
    **Objective:** build and unit-test a custom `Voter` that grants `POST_EDIT`
    only to a post's owner or a `ROLE_ADMIN`, and abstains for everything else ·
    **Difficulty:** Medium ·
    **Theory:** [Voters](../security/voters.md) · [Authorization](../security/authorization.md) ·
    **Mode:** TDD

## Objective

After this lab you can:

- Extend `Symfony\Component\Security\Core\Authorization\Voter\Voter` and split the
  decision cleanly between `supports()` (filter) and `voteOnAttribute()` (decide).
- **Unit-test** `voteOnAttribute()` in isolation — with a stub `TokenInterface`
  returning a `User` and real subject objects — asserting `ACCESS_GRANTED`,
  `ACCESS_DENIED` and `ACCESS_ABSTAIN`.
- Wire the voter into a controller with `#[IsGranted]` / `denyAccessUnlessGranted()`
  and explain how the **affirmative** strategy consumes the vote.

## Prerequisites

- Chapters: [Voters](../security/voters.md), [Authorization](../security/authorization.md),
  [Roles](../security/roles.md).
- Assumed skills: PHPUnit basics (`TestCase`, stubs), Symfony autoconfiguration,
  `UserInterface` fundamentals.

## TD Instructions

1. Create a `Post` entity-shaped class with a `getOwner(): User` accessor (no
   Doctrine — a plain class is enough for the unit test).
2. Create a `User` implementing `UserInterface` with an id and roles.
3. **Write the test first** (`tests/Security/Voter/PostVoterTest.php`): instantiate
   the voter directly and call the public `vote()` (inherited from `Voter`) with a
   **stub** `TokenInterface`. Cover:
   - owner requesting `POST_EDIT` → `ACCESS_GRANTED`;
   - `ROLE_ADMIN` (non-owner) requesting `POST_EDIT` → `ACCESS_GRANTED`;
   - a different, non-admin user → `ACCESS_DENIED`;
   - an unsupported attribute (`POST_DELETE`) → `ACCESS_ABSTAIN`;
   - an unsupported subject (a plain `\stdClass`) → `ACCESS_ABSTAIN`;
   - an anonymous token (`getUser()` returns `null`) → `ACCESS_DENIED`.
4. Run it — watch it fail (**Red**). The class does not exist yet.
5. Implement `PostVoter` extending `Voter` with a `POST_EDIT` constant. Make the
   test pass (**Green**).
6. **Refactor**: use a `match` and a private `canEdit()` helper; add the generic
   `@extends Voter<string, Post>` docblock.
7. Add a controller using `#[IsGranted(PostVoter::EDIT, subject: 'post')]` and note
   in a comment how the default **affirmative** strategy turns one `ACCESS_GRANTED`
   into a pass.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · no libraries outside the certification scope · follow
    best practices (attributes, `strict_types`, `readonly` where apt).

## Implementation Guide (partial)

- Extend `Symfony\Component\Security\Core\Authorization\Voter\Voter`. It already
  implements `VoterInterface::vote()`; you only write the two `protected` methods.
- `supports(string $attribute, mixed $subject): bool` must return `true` **only**
  when the attribute is yours **and** `$subject instanceof Post`. Anything else →
  the base class votes **ABSTAIN** (it never calls `voteOnAttribute()`).
- `voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool`
  returns `true` (GRANTED) / `false` (DENIED). Read the user with
  `$token->getUser()`; if it is not your `User`, deny.
- To test the ADMIN branch without the role hierarchy, compare against
  `$user->getRoles()` directly (a unit test has no container). The vote **constants**
  `ACCESS_GRANTED` (1), `ACCESS_DENIED` (-1), `ACCESS_ABSTAIN` (0) live on
  `VoterInterface`.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red:** write the failing test below; run it, watch it fail.
    2. **Green:** write the minimum code to pass.
    3. **Refactor:** clean up with the test as your safety net.

**Behaviour (Given/When/Then):**

- **Given** a `Post` owned by user *alice* **When** *alice* asks for `POST_EDIT`
  **Then** the voter returns `ACCESS_GRANTED`.
- **Given** a `Post` owned by *alice* **When** *bob* (`ROLE_ADMIN`) asks for
  `POST_EDIT` **Then** `ACCESS_GRANTED` (admin override).
- **Given** a `Post` owned by *alice* **When** *bob* (`ROLE_USER`) asks for
  `POST_EDIT` **Then** `ACCESS_DENIED`.
- **Given** any subject **When** the attribute is `POST_DELETE`, or the subject is
  not a `Post` **Then** `ACCESS_ABSTAIN`.

```php
<?php
declare(strict_types=1);

namespace App\Tests\Security\Voter;

use App\Entity\Post;
use App\Security\User;
use App\Security\Voter\PostVoter;
use PHPUnit\Framework\TestCase;
use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\Authorization\Voter\VoterInterface;

final class PostVoterTest extends TestCase
{
    private PostVoter $voter;

    protected function setUp(): void
    {
        $this->voter = new PostVoter();
    }

    /** Build a stub token whose getUser() returns the given user (or null). */
    private function tokenFor(?User $user): TokenInterface
    {
        $token = $this->createStub(TokenInterface::class);
        $token->method('getUser')->willReturn($user);

        return $token;
    }

    public function testOwnerCanEdit(): void
    {
        $alice = new User('alice', ['ROLE_USER']);
        $post = new Post($alice);

        $vote = $this->voter->vote($this->tokenFor($alice), $post, [PostVoter::EDIT]);

        self::assertSame(VoterInterface::ACCESS_GRANTED, $vote);
    }

    public function testAdminCanEditAnyPost(): void
    {
        $alice = new User('alice', ['ROLE_USER']);
        $admin = new User('bob', ['ROLE_USER', 'ROLE_ADMIN']);
        $post = new Post($alice);

        $vote = $this->voter->vote($this->tokenFor($admin), $post, [PostVoter::EDIT]);

        self::assertSame(VoterInterface::ACCESS_GRANTED, $vote);
    }

    public function testNonOwnerNonAdminIsDenied(): void
    {
        $alice = new User('alice', ['ROLE_USER']);
        $bob = new User('bob', ['ROLE_USER']);
        $post = new Post($alice);

        $vote = $this->voter->vote($this->tokenFor($bob), $post, [PostVoter::EDIT]);

        self::assertSame(VoterInterface::ACCESS_DENIED, $vote);
    }

    public function testAnonymousIsDenied(): void
    {
        $post = new Post(new User('alice', ['ROLE_USER']));

        $vote = $this->voter->vote($this->tokenFor(null), $post, [PostVoter::EDIT]);

        self::assertSame(VoterInterface::ACCESS_DENIED, $vote);
    }

    public function testUnsupportedAttributeAbstains(): void
    {
        $alice = new User('alice', ['ROLE_USER']);
        $post = new Post($alice);

        $vote = $this->voter->vote($this->tokenFor($alice), $post, ['POST_DELETE']);

        self::assertSame(VoterInterface::ACCESS_ABSTAIN, $vote);
    }

    public function testUnsupportedSubjectAbstains(): void
    {
        $alice = new User('alice', ['ROLE_USER']);

        $vote = $this->voter->vote($this->tokenFor($alice), new \stdClass(), [PostVoter::EDIT]);

        self::assertSame(VoterInterface::ACCESS_ABSTAIN, $vote);
    }
}
```

!!! tip "Setup hints"
    Run it: `vendor/bin/phpunit tests/Security/Voter/PostVoterTest.php`.
    Use `$this->createStub(TokenInterface::class)` — a **stub**, not a mock:
    you are asserting on the voter's return value, not on token interactions, so
    there is nothing to verify on the token. Calling the inherited public
    `vote()` (rather than the `protected` `voteOnAttribute()`) exercises the real
    `supports()` → `voteOnAttribute()` dispatch, which is exactly what you want to
    lock down.

## Validation Steps

Once wired into the app (voters are autoconfigured via the `security.voter` tag):

- [ ] `php bin/console debug:container --tag=security.voter` lists `App\Security\Voter\PostVoter`.
- [ ] Logged in as the owner, `GET /posts/{id}/edit` returns **200**.
- [ ] Logged in as a different non-admin user, the same URL returns **403**.
- [ ] The **profiler → Security** panel shows the access-decision log with your
      voter's `ACCESS_GRANTED` / `ACCESS_DENIED` vote and the **affirmative**
      strategy.

## Review — Common Mistakes

- **Returning `false` for "not my attribute."** In `voteOnAttribute()` `false` means
  **DENY**, not abstain. Filter unrelated attributes/subjects in `supports()` so the
  base class abstains — otherwise, under `unanimous`, your voter blocks unrelated
  checks.
- **Assuming `getUser()` is your `User`.** An anonymous request yields `null`; always
  `instanceof`-guard before reading ownership.
- **Testing `voteOnAttribute()` directly by making it public.** Keep it `protected`
  and call the inherited public `vote()` — you then also cover `supports()` and the
  ABSTAIN path for free.
- **Checking `ROLE_ADMIN` against a hierarchy in a unit test.** There is no container,
  so `role_hierarchy` is not applied; compare raw `getRoles()`, or inject
  `AccessDecisionManagerInterface`/`Security` only in a `KernelTestCase`.
- **Expecting `ACCESS_ABSTAIN` to grant.** All-abstain denies by default
  (`allow_if_all_abstain: false`).

## Exam Connection

The certification tests the **three-vote model** and the fact that
`Voter::supports()` returning `false` yields **ABSTAIN** (never DENY), plus the
default **affirmative** strategy (one `ACCESS_GRANTED` is enough). It also probes
that only the `isGranted()` path (`#[IsGranted]`, `denyAccessUnlessGranted()`,
Twig `is_granted()`) can pass a **subject** to a voter — `access_control` cannot.
This lab drills all of it in code you can run.

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    ```php
    <?php
    declare(strict_types=1);

    // src/Security/User.php
    namespace App\Security;

    use Symfony\Component\Security\Core\User\UserInterface;

    final class User implements UserInterface
    {
        /** @param list<string> $roles */
        public function __construct(
            private readonly string $username,
            private readonly array $roles = ['ROLE_USER'],
        ) {
        }

        public function getUserIdentifier(): string
        {
            return $this->username;
        }

        /** @return list<string> */
        public function getRoles(): array
        {
            return $this->roles;
        }

        // Symfony 8: UserInterface declares only getUserIdentifier() + getRoles().
        // eraseCredentials() was removed in 8.0 — strip secrets in __serialize().
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    // src/Entity/Post.php
    namespace App\Entity;

    use App\Security\User;

    final class Post
    {
        public function __construct(private readonly User $owner)
        {
        }

        public function getOwner(): User
        {
            return $this->owner;
        }

        public function isOwnedBy(User $user): bool
        {
            return $this->owner->getUserIdentifier() === $user->getUserIdentifier();
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    // src/Security/Voter/PostVoter.php
    namespace App\Security\Voter;

    use App\Entity\Post;
    use App\Security\User;
    use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
    use Symfony\Component\Security\Core\Authorization\Voter\Voter;

    /**
     * Grants POST_EDIT to the post's owner or any ROLE_ADMIN.
     *
     * @extends Voter<string, Post>
     */
    final class PostVoter extends Voter
    {
        public const string EDIT = 'POST_EDIT';

        protected function supports(string $attribute, mixed $subject): bool
        {
            return self::EDIT === $attribute && $subject instanceof Post;
        }

        protected function voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool
        {
            $user = $token->getUser();
            if (!$user instanceof User) {
                return false; // not authenticated → deny
            }

            /** @var Post $subject (guaranteed by supports()) */
            return $this->canEdit($subject, $user);
        }

        private function canEdit(Post $post, User $user): bool
        {
            if (\in_array('ROLE_ADMIN', $user->getRoles(), true)) {
                return true; // admin override
            }

            return $post->isOwnedBy($user);
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    // src/Controller/PostController.php
    namespace App\Controller;

    use App\Entity\Post;
    use App\Security\Voter\PostVoter;
    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Attribute\Route;
    use Symfony\Component\Security\Http\Attribute\IsGranted;

    final class PostController extends AbstractController
    {
        // #[IsGranted] resolves 'post' by argument name and passes it as the
        // subject. The AccessDecisionManager polls every security.voter; under the
        // default AFFIRMATIVE strategy, PostVoter's single ACCESS_GRANTED is enough
        // to pass — a 403 (AccessDeniedException) is thrown otherwise.
        #[Route('/posts/{id}/edit', name: 'post_edit')]
        #[IsGranted(PostVoter::EDIT, subject: 'post')]
        public function edit(Post $post): Response
        {
            // ... render/update the post; access already enforced by the voter.
            return $this->render('post/edit.html.twig', ['post' => $post]);
        }

        // Equivalent imperative form, without the attribute:
        public function editImperative(Post $post): Response
        {
            $this->denyAccessUnlessGranted(PostVoter::EDIT, $post);

            return $this->render('post/edit.html.twig', ['post' => $post]);
        }
    }
    ```

    Autoconfiguration tags the class `security.voter` automatically — no manual
    service wiring. In Twig the same rule reads `{% if is_granted('POST_EDIT', post) %}`.

## Alternative Approaches (optional)

- **Option A (simple):** collapse `canEdit()` into a single boolean expression in
  `voteOnAttribute()` — fine for one rule, but the helper scales to more attributes.
- **Option B (advanced):** inject `Symfony\Bundle\SecurityBundle\Security` into the
  voter and call `$this->security->isGranted('ROLE_ADMIN')` so the **role hierarchy**
  is honoured (e.g. `ROLE_SUPER_ADMIN` inherits `ROLE_ADMIN`). This needs a
  `KernelTestCase` to test, since it depends on the container.
- **Option C (exam-style):** add a `banned` voter that always returns
  `ACCESS_DENIED` and switch the strategy to `unanimous` — observe how one deny now
  blocks even the owner, contrasting with affirmative.

---

<small>Theory: [Voters](../security/voters.md) · [Authorization](../security/authorization.md) · Labs: [all labs](index.md)</small>
</content>

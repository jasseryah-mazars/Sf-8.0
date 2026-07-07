---
tags:
  - Labs
  - Security
---

# Lab : Voter personnalisé — autorisation fine (`POST_EDIT`)

<!--
PRACTICAL LAB — Security. Mode: TDD (code behaviour: a Voter you instantiate and assert on).
All code: Symfony 8 / PHP 8.4. Complete <?php snippets compile with php -l.
-->

!!! abstract "Practical Lab"
    **Objective:** construire et tester unitairement un `Voter` personnalisé qui
    n'accorde `POST_EDIT` qu'au propriétaire d'un post ou à un `ROLE_ADMIN`, et
    s'abstient pour tout le reste ·
    **Difficulty:** Medium ·
    **Theory:** [Voters](../security/voters.md) · [Authorization](../security/authorization.md) ·
    **Mode:** TDD

## Objective

À l'issue de ce lab, vous saurez :

- Étendre `Symfony\Component\Security\Core\Authorization\Voter\Voter` et répartir
  proprement la décision entre `supports()` (filtre) et `voteOnAttribute()` (décision).
- **Tester unitairement** `voteOnAttribute()` en isolation — avec un stub de
  `TokenInterface` retournant un `User` et de vrais objets sujets — en vérifiant
  `ACCESS_GRANTED`, `ACCESS_DENIED` et `ACCESS_ABSTAIN`.
- Brancher le voter dans un controller avec `#[IsGranted]` / `denyAccessUnlessGranted()`
  et expliquer comment la stratégie **affirmative** consomme le vote.

## Prerequisites

- Chapitres : [Voters](../security/voters.md), [Authorization](../security/authorization.md),
  [Roles](../security/roles.md).
- Compétences supposées acquises : les bases de PHPUnit (`TestCase`, stubs),
  l'autoconfiguration Symfony, les fondamentaux de `UserInterface`.

## TD Instructions

1. Créez une classe `Post` de type entité avec un accesseur `getOwner(): User`
   (pas de Doctrine — une classe simple suffit pour le test unitaire).
2. Créez un `User` implémentant `UserInterface` avec un identifiant et des rôles.
3. **Écrivez d'abord le test** (`tests/Security/Voter/PostVoterTest.php`) : instanciez
   le voter directement et appelez la méthode publique `vote()` (héritée de `Voter`)
   avec un **stub** de `TokenInterface`. Couvrez :
   - le propriétaire demandant `POST_EDIT` → `ACCESS_GRANTED` ;
   - un `ROLE_ADMIN` (non propriétaire) demandant `POST_EDIT` → `ACCESS_GRANTED` ;
   - un autre utilisateur, non admin → `ACCESS_DENIED` ;
   - un attribut non supporté (`POST_DELETE`) → `ACCESS_ABSTAIN` ;
   - un sujet non supporté (une simple `\stdClass`) → `ACCESS_ABSTAIN` ;
   - un token anonyme (`getUser()` retourne `null`) → `ACCESS_DENIED`.
4. Lancez-le — regardez-le échouer (**Red**). La classe n'existe pas encore.
5. Implémentez `PostVoter` en étendant `Voter` avec une constante `POST_EDIT`.
   Faites passer le test (**Green**).
6. **Refactor** : utilisez un `match` et une méthode privée `canEdit()` ; ajoutez le
   docblock générique `@extends Voter<string, Post>`.
7. Ajoutez un controller utilisant `#[IsGranted(PostVoter::EDIT, subject: 'post')]`
   et notez en commentaire comment la stratégie **affirmative** par défaut transforme
   un seul `ACCESS_GRANTED` en accès accordé.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · aucune bibliothèque hors du périmètre de la certification ·
    suivez les bonnes pratiques (attributs, `strict_types`, `readonly` quand c'est pertinent).

## Implementation Guide (partial)

- Étendez `Symfony\Component\Security\Core\Authorization\Voter\Voter`. Elle implémente
  déjà `VoterInterface::vote()` ; vous n'écrivez que les deux méthodes `protected`.
- `supports(string $attribute, mixed $subject): bool` ne doit retourner `true` **que**
  lorsque l'attribut est le vôtre **et** que `$subject instanceof Post`. Pour tout le
  reste → la classe de base vote **ABSTAIN** (elle n'appelle jamais `voteOnAttribute()`).
- `voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool`
  retourne `true` (GRANTED) / `false` (DENIED). Lisez l'utilisateur avec
  `$token->getUser()` ; si ce n'est pas votre `User`, refusez.
- Pour tester la branche ADMIN sans la hiérarchie de rôles, comparez directement avec
  `$user->getRoles()` (un test unitaire n'a pas de container). Les **constantes** de
  vote `ACCESS_GRANTED` (1), `ACCESS_DENIED` (-1), `ACCESS_ABSTAIN` (0) vivent sur
  `VoterInterface`.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red :** écrivez le test en échec ci-dessous ; lancez-le, regardez-le échouer.
    2. **Green :** écrivez le minimum de code pour le faire passer.
    3. **Refactor :** nettoyez avec le test comme filet de sécurité.

**Comportement (Given/When/Then) :**

- **Given** un `Post` appartenant à l'utilisatrice *alice* **When** *alice* demande
  `POST_EDIT` **Then** le voter retourne `ACCESS_GRANTED`.
- **Given** un `Post` appartenant à *alice* **When** *bob* (`ROLE_ADMIN`) demande
  `POST_EDIT` **Then** `ACCESS_GRANTED` (passe-droit admin).
- **Given** un `Post` appartenant à *alice* **When** *bob* (`ROLE_USER`) demande
  `POST_EDIT` **Then** `ACCESS_DENIED`.
- **Given** n'importe quel sujet **When** l'attribut est `POST_DELETE`, ou le sujet
  n'est pas un `Post` **Then** `ACCESS_ABSTAIN`.

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
    Lancez-le : `vendor/bin/phpunit tests/Security/Voter/PostVoterTest.php`.
    Utilisez `$this->createStub(TokenInterface::class)` — un **stub**, pas un mock :
    vous faites des assertions sur la valeur de retour du voter, pas sur les
    interactions avec le token, il n'y a donc rien à vérifier sur celui-ci. Appeler
    la méthode publique héritée `vote()` (plutôt que `voteOnAttribute()` qui est
    `protected`) exerce le vrai dispatch `supports()` → `voteOnAttribute()`, ce qui
    est exactement ce que vous voulez verrouiller.

## Validation Steps

Une fois le voter branché dans l'application (les voters sont autoconfigurés via le tag `security.voter`) :

- [ ] `php bin/console debug:container --tag=security.voter` liste `App\Security\Voter\PostVoter`.
- [ ] Connecté en tant que propriétaire, `GET /posts/{id}/edit` retourne **200**.
- [ ] Connecté en tant qu'autre utilisateur non admin, la même URL retourne **403**.
- [ ] Le panneau **profiler → Security** montre le journal de décision d'accès avec
      le vote `ACCESS_GRANTED` / `ACCESS_DENIED` de votre voter et la stratégie
      **affirmative**.

## Review — Common Mistakes

- **Retourner `false` pour « ce n'est pas mon attribut ».** Dans `voteOnAttribute()`,
  `false` signifie **DENY**, pas abstention. Filtrez les attributs/sujets sans rapport
  dans `supports()` pour que la classe de base s'abstienne — sinon, en stratégie
  `unanimous`, votre voter bloque des vérifications qui ne le concernent pas.
- **Supposer que `getUser()` est votre `User`.** Une request anonyme donne `null` ;
  protégez-vous toujours avec un `instanceof` avant de lire la propriété de possession.
- **Tester `voteOnAttribute()` directement en la rendant publique.** Gardez-la
  `protected` et appelez la méthode publique héritée `vote()` — vous couvrez alors
  aussi `supports()` et le chemin ABSTAIN gratuitement.
- **Vérifier `ROLE_ADMIN` via une hiérarchie dans un test unitaire.** Il n'y a pas de
  container, donc `role_hierarchy` n'est pas appliquée ; comparez les `getRoles()`
  bruts, ou n'injectez `AccessDecisionManagerInterface`/`Security` que dans un
  `KernelTestCase`.
- **S'attendre à ce qu'`ACCESS_ABSTAIN` accorde l'accès.** L'abstention générale
  refuse par défaut (`allow_if_all_abstain: false`).

## Exam Connection

La certification teste le **modèle à trois votes** et le fait que
`Voter::supports()` retournant `false` produit **ABSTAIN** (jamais DENY), ainsi que
la stratégie **affirmative** par défaut (un seul `ACCESS_GRANTED` suffit). Elle
vérifie aussi que seul le chemin `isGranted()` (`#[IsGranted]`,
`denyAccessUnlessGranted()`, `is_granted()` dans Twig) peut transmettre un **sujet**
à un voter — `access_control` ne le peut pas. Ce lab fait travailler tout cela dans
du code que vous pouvez exécuter.

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

    L'autoconfiguration applique automatiquement le tag `security.voter` à la classe —
    aucun câblage manuel de service. Dans Twig, la même règle s'écrit
    `{% if is_granted('POST_EDIT', post) %}`.

## Alternative Approaches (optional)

- **Option A (simple) :** fusionnez `canEdit()` en une seule expression booléenne dans
  `voteOnAttribute()` — acceptable pour une règle unique, mais la méthode privée passe
  mieux à l'échelle avec plusieurs attributs.
- **Option B (avancée) :** injectez `Symfony\Bundle\SecurityBundle\Security` dans le
  voter et appelez `$this->security->isGranted('ROLE_ADMIN')` afin que la **hiérarchie
  de rôles** soit respectée (par ex. `ROLE_SUPER_ADMIN` hérite de `ROLE_ADMIN`). Cela
  exige un `KernelTestCase` pour le test, puisque cela dépend du container.
- **Option C (façon examen) :** ajoutez un voter `banned` qui retourne toujours
  `ACCESS_DENIED` et basculez la stratégie sur `unanimous` — observez comment un seul
  refus bloque désormais même le propriétaire, par contraste avec affirmative.

---

<small>Theory: [Voters](../security/voters.md) · [Authorization](../security/authorization.md) · Labs: [all labs](index.md)</small>

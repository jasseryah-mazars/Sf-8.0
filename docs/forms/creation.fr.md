# Creating Forms

!!! tip "In a nutshell"
    Vous décrivez un form dans une classe de type réutilisable (`buildForm` + `configureOptions`)
    et laissez le framework le construire via `createForm()`. Point d'examen : `data_class`
    lie le form à un objet — sans lui, les données d'un form composé sont un simple **array**.

!!! example "Real-world analogy"
    Un form type est un **formulaire papier vierge** ; `createForm()` vous en remet un
    exemplaire neuf accompagné d'un **greffier**. Quand vous soumettez, le greffier lit
    chaque champ et classe les réponses dans votre **dossier** — `data_class` nomme le
    dossier en question (un `RegistrationData`). Sans `data_class`, le greffier garde
    juste une pile de notes étiquetées (un **array** associatif).

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Construire un form à partir d'une **classe de form type** réutilisable avec `buildForm` et `configureOptions`.
    - [ ] Créer un form ad hoc avec `createFormBuilder` dans un controller.
    - [ ] Expliquer comment `data_class` lie un form à un objet PHP et comment la `FormFactory` résout un type.

    **Syllabus:** `Forms → Creating forms` ·
    **Level:** Advanced → Expert ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Controllers](../controllers/index.md) · [DI](../dependency-injection/index.md)

---

## Pour les nuls

### L'idée en une phrase
Un type de formulaire est un modèle de papier réutilisable — tu le décris une fois dans une classe, et Symfony construit le formulaire réel à partir de ce modèle.

### Imagine dans la vraie vie
Un type de formulaire est un **formulaire papier vierge** ; `createForm()` te remet une copie neuve avec un **employé** attaché. Quand tu soumets, l'employé lit chaque champ et classe les réponses dans ton **dossier** — `data_class` nomme quel dossier (une classe `InscriptionData`). Sans `data_class`, l'employé garde juste une pile de notes libres (un tableau associatif).

### Dans Symfony
`ProduitType` (une classe de type de formulaire) peut être réutilisée pour créer le formulaire d'ajout **et** le formulaire d'édition d'un produit — même code, deux contextes différents.

### Exemple simple
```php
$form = $this->createForm(ProduitType::class, $produit); // $produit = data_class
```

### Comment le mémoriser 🧠
Sans `data_class`, les données soumises restent un simple **tableau** — pas un objet. C'est le piège classique : oublier `data_class` et se demander pourquoi `$data->getNom()` plante.


## Theory

Un form Symfony est un graphe d'objets d'instances de `Symfony\Component\Form\FormInterface`
construit par une `Symfony\Component\Form\FormFactory`. Vous touchez rarement la
factory directement. Vous décrivez plutôt *ce que* contient le form dans une
**classe de form type** et laissez le framework l'assembler.

```php
// The FormFactory builds the object graph...
$form = $formFactory->create(TaskType::class);

// ...and returns the root of a FormInterface tree
assert($form instanceof \Symfony\Component\Form\FormInterface);
$title = $form->get('title'); // each child is also a FormInterface
```

Deux façons de créer un form :

| Approach | Use when |
|---|---|
| **Classe de form type** (`AbstractType`) | Form réutilisable, testé isolément, applications réelles |
| **`createFormBuilder`** | Form ponctuel, local à un seul controller/action |

Le helper de controller `AbstractController::createForm(FqcnType::class, $data, $options)`
est le point d'entrée au quotidien. Sous le capot, il appelle
`FormFactoryInterface::create(...)`.

```php
// Everyday entry point (AbstractController::createForm):
$form = $this->createForm(RegistrationType::class, $data, $options);

// What it calls under the hood (FormFactoryInterface::create):
$form = $formFactory->create(RegistrationType::class, $data, $options);
```

!!! question "Predict first"
    Vous appelez `createForm(RegistrationType::class)` sur un form composé qui ne
    définit **pas** `data_class`, puis lisez `getData()` avant tout submit.
    Qu'obtenez-vous ?

??? note "Reveal"
    Un **array** associatif indexé par le nom des champs enfants (ou `null`/l'array
    initial que vous avez passé). Ce n'est qu'avec `data_class` défini que le form
    matérialise un `new $dataClass()` via `empty_data` et mappe les enfants sur cet
    objet à travers le data mapper.

## Deep Dive — how it works internally

### The form type class

Un form type étend `Symfony\Component\Form\AbstractType` (qui implémente
`Symfony\Component\Form\FormTypeInterface`) et surcharge deux méthodes :

- `buildForm(FormBuilderInterface $builder, array $options)` — ajoute les champs et
  configure le comportement (event listeners, data mappers).
- `configureOptions(OptionsResolver $resolver)` — déclare les options acceptées par
  le type et leurs valeurs par défaut, via `Symfony\Component\OptionsResolver\OptionsResolver`.

```php
// AbstractType already implements FormTypeInterface for you
final class TaskType extends AbstractType
{
    // buildForm(): add fields, listeners, data mappers
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder->add('title', TextType::class);
    }

    // configureOptions(): declare options via the OptionsResolver
    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults(['data_class' => Task::class]);
    }
}
```

`getBlockPrefix()` (par défaut le nom de la classe en snake case, sans le suffixe
`Type`) pilote le nommage des blocs Twig — voir [theming](theming.md).

### How the factory builds the tree

```mermaid
flowchart LR
    A["createForm(Type::class)"] --> B[FormFactory::create]
    B --> C[FormRegistry::getType]
    C --> D[ResolvedFormType]
    D --> E["newBuilder + buildForm()"]
    E --> F["getForm(): FormInterface tree"]
```

1. `FormFactory::create()` appelle `createBuilder()`, qui demande au
   `Symfony\Component\Form\FormRegistry` une
   `Symfony\Component\Form\ResolvedFormTypeInterface` (un *resolved type* enveloppe
   le type, sa chaîne de parents et toutes les type extensions — voir [types](types.md)).
2. Le resolved type crée un `Symfony\Component\Form\FormBuilder`, puis parcourt la
   chaîne **parent → enfant** en appelant le `buildForm()` de chaque type et le
   `buildForm()` de chaque type extension enregistrée.
3. `getForm()` transforme récursivement l'arbre de builders en un arbre immuable de
   `FormInterface`. Chaque champ est lui-même un `Form` dont la config est une
   `Symfony\Component\Form\FormConfigInterface`.

```php
// Inside FormFactory::create() → createBuilder():
$resolvedType = $registry->getType(TaskType::class);       // FormRegistry → ResolvedFormTypeInterface
$builder = $resolvedType->createBuilder($factory, 'task'); // a FormBuilder
// parent → child chain: each type's (and extension's) buildForm() runs
$resolvedType->buildForm($builder, $builder->getOptions());
$form = $builder->getForm();   // immutable FormInterface tree
$config = $form->getConfig();  // each field exposes a FormConfigInterface
```

!!! note "Source reference"
    `Symfony\Component\Form\FormFactory` et `AbstractType` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/FormFactory.php).

### `data_class` and object binding

`data_class` indique au form quelle classe PHP est le modèle sous-jacent. Quand
elle est définie :

- À la construction, les données vides deviennent un `new $dataClass()` (via
  l'option `empty_data` / le `getData` du type), et la validation résout les
  constraints depuis les métadonnées de cette classe.
- Au submit, les valeurs soumises sont réécrites sur cet objet via le
  **data mapper** (`Symfony\Component\Form\Extension\Core\DataMapper\DataMapper`,
  qui utilise PropertyAccess). Sans `data_class`, un form composé produit un
  **array** associatif.

```php
// data_class binds the model; empty_data materialises it when input is missing
$form = $this->createForm(RegistrationType::class); // data_class = RegistrationData::class
$data = $form->getData(); // RegistrationData instance, never an array here

// On submit, the DataMapper writes values back via PropertyAccess, roughly:
// $accessor->setValue($data, 'username', $form->get('username')->getData());
```

### Null behavior

Juste après `createForm()` — **avant tout submit** — `getData()` retourne ce que
vous avez passé. Ne passez rien alors que `data_class` est défini et le form
matérialise quand même un `new $dataClass()` depuis l'option `empty_data` : il
n'est donc jamais `null` au moment du rendu. Ne passez rien *sans* `data_class` et
`getData()` vaut `null` (ou l'array initial que vous avez fourni). Les champs non
mappés (`'mapped' => false`, comme `plainPassword`) ne sont jamais écrits sur
l'objet — lisez-les via `$form->get('plainPassword')->getData()`, pas via le
modèle. Le bug classique : typer `getData()` comme votre DTO et le déréférencer sur
un form **non lié et sans `data_class`**, et tomber sur `null`.

```php
$form = $this->createForm(FilterType::class);       // no data_class in this type
$form->getData();  // null (or the initial array you passed)

$form = $this->createForm(RegistrationType::class); // data_class is set
$form->getData();  // fresh RegistrationData built via empty_data — never null

// 'mapped' => false fields never reach the model — read them on the form:
$plain = $form->get('plainPassword')->getData();
```

!!! note "Null in real life"
    `null` = une fiche vierge sur laquelle le greffier n'a encore rien classé — avec
    un dossier nommé (`data_class`), il vous en ouvre toujours un neuf.

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Form;

    use App\Dto\RegistrationData;
    use Symfony\Component\Form\AbstractType;
    use Symfony\Component\Form\Extension\Core\Type\EmailType;
    use Symfony\Component\Form\Extension\Core\Type\PasswordType;
    use Symfony\Component\Form\Extension\Core\Type\TextType;
    use Symfony\Component\Form\FormBuilderInterface;
    use Symfony\Component\OptionsResolver\OptionsResolver;

    final class RegistrationType extends AbstractType
    {
        public function buildForm(FormBuilderInterface $builder, array $options): void
        {
            $builder
                ->add('username', TextType::class)
                ->add('email', EmailType::class)
                ->add('plainPassword', PasswordType::class, [
                    'mapped' => false, // not written back to the model
                ]);
        }

        public function configureOptions(OptionsResolver $resolver): void
        {
            $resolver->setDefaults([
                'data_class' => RegistrationData::class,
                'csrf_token_id' => 'registration',
            ]);
        }
    }
    ```

=== "Controller"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use App\Dto\RegistrationData;
    use App\Form\RegistrationType;
    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Attribute\Route;

    final class RegistrationController extends AbstractController
    {
        #[Route('/register', name: 'register', methods: ['GET', 'POST'])]
        public function register(Request $request): Response
        {
            $data = new RegistrationData();
            $form = $this->createForm(RegistrationType::class, $data);

            // Handling covered in the next chapter.
            return $this->render('registration/index.html.twig', [
                'form' => $form, // pass the FormInterface, not createView()
            ]);
        }
    }
    ```

=== "createFormBuilder"

    ```php
    <?php
    declare(strict_types=1);

    // Inside a controller action — ad-hoc, no dedicated type class:
    $form = $this->createFormBuilder(['q' => ''])
        ->add('q', \Symfony\Component\Form\Extension\Core\Type\SearchType::class)
        ->add('search', \Symfony\Component\Form\Extension\Core\Type\SubmitType::class)
        ->getForm();
    ```

!!! info "Pass the form, not the view"
    Depuis Symfony 6.2, vous passez le `FormInterface` au template et appelez
    `form(form)` dans Twig ; Symfony rend `createView()` pour vous. Vous pouvez
    encore appeler `$form->createView()` manuellement, mais ce n'est plus requis.

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Un `AbstractType` réutilisable par form | Construire des forms complexes inline dans les controllers |
| Déclarer chaque option dans `configureOptions` | Lire un `$options['x']` jamais défini |
| Lier à un DTO/entité typé via `data_class` | Parser `$request->request` à la main |
| Garder les types stateless et autowirés | Injecter des données de la request dans le constructeur du type |

## When (not) to use it / alternatives

Utilisez `createFormBuilder` uniquement pour des forms jetables (une boîte de
recherche). Tout ce qui est réutilisé, testé ou non trivial mérite une classe de
type. Pour des API JSON pures sans rendu HTML, le composant Form est souvent
surdimensionné — un DTO + le Serializer + le Validator est plus léger (mais le
composant Form gère quand même pour vous les soumissions partielles et le CSRF).

!!! danger "Certification traps"
    - `buildForm` reçoit une **`FormBuilderInterface`**, pas une `FormInterface`.
      Le form n'existe pas encore — vous ne pouvez pas y lire les données soumises.
    - Sans `data_class`, les données d'un form composé sont un **array**, pas un objet.
    - `configureOptions` utilise `OptionsResolver`, et **non** le retour d'un
      simple array.
    - `getBlockPrefix()` — et non `getName()` (supprimée depuis longtemps) —
      contrôle les noms de blocs Twig.

!!! warning "Common mistakes"
    - Passer `$form` et *aussi* `$form->createView()` — choisissez l'un des deux.
    - Oublier `methods: ['GET', 'POST']` sur la route, et le POST renvoie un 405.
    - Mettre la logique d'ajout de champs dans `configureOptions` au lieu de `buildForm`.

## Exercises

1. **(Advanced)** Écrivez un `ContactType` lié à un DTO `ContactData` avec les
   champs `name`, `email` et `message`, plus un `csrf_token_id`.
2. **(Expert)** Expliquez ce que retourne `$form->getData()` immédiatement après
   `createForm(ContactType::class)` quand (a) `data_class` est défini et (b) il ne l'est pas.

??? success "Solutions"

    **1.**

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Form;

    use App\Dto\ContactData;
    use Symfony\Component\Form\AbstractType;
    use Symfony\Component\Form\Extension\Core\Type\EmailType;
    use Symfony\Component\Form\Extension\Core\Type\TextareaType;
    use Symfony\Component\Form\Extension\Core\Type\TextType;
    use Symfony\Component\Form\FormBuilderInterface;
    use Symfony\Component\OptionsResolver\OptionsResolver;

    final class ContactType extends AbstractType
    {
        public function buildForm(FormBuilderInterface $builder, array $options): void
        {
            $builder
                ->add('name', TextType::class)
                ->add('email', EmailType::class)
                ->add('message', TextareaType::class);
        }

        public function configureOptions(OptionsResolver $resolver): void
        {
            $resolver->setDefaults([
                'data_class' => ContactData::class,
                'csrf_token_id' => 'contact',
            ]);
        }
    }
    ```

    **2.** (a) Avec `data_class`, `getData()` retourne l'objet que vous avez passé
    (ou un `new ContactData()` si aucun), donc une instance fraîche. (b) Sans,
    `getData()` retourne `null` (ou l'array initial fourni à `createForm`).

## Certification questions

??? question "Q1. Which two methods do you override on `AbstractType`?"
    - [ ] A. `build()` and `getOptions()`
    - [x] B. `buildForm()` and `configureOptions()` ✅
    - [ ] C. `configureFields()` and `setDefaults()`
    - [ ] D. `getName()` and `buildView()`

    **Why:** `buildForm(FormBuilderInterface, array)` ajoute les champs ;
    `configureOptions(OptionsResolver)` déclare les options. `getName` a été
    supprimée ; `buildView` existe mais n'est pas la paire principale.
    **Ref:** [Creating forms](https://symfony.com/doc/8.0/forms.html).

??? question "Q2. What does a compound form return from `getData()` when `data_class` is unset?"
    - [ ] A. `null` always
    - [x] B. An associative array keyed by child name ✅
    - [ ] C. A `stdClass`
    - [ ] D. A `FormInterface`

    **Why:** Sans `data_class`, le data mapper mappe les enfants vers/depuis un
    array. Définissez `data_class` pour lier à un objet.
    **Ref:** [Form types](https://symfony.com/doc/8.0/forms.html).

## Key takeaways

- Un form type = `buildForm` (champs) + `configureOptions` (options via
  `OptionsResolver`).
- `createForm()` → `FormFactory` → `ResolvedFormType` → arbre de builders → arbre
  immuable de `FormInterface`.
- `data_class` lie le form à un objet ; sans lui, vous obtenez un array.
- `getBlockPrefix()` pilote le theming Twig, pas `getName()`.

## Last-minute revision

!!! tip "Cheat sheet"
    - `AbstractType::buildForm(FormBuilderInterface $b, array $o)`
    - `configureOptions(OptionsResolver $r)` → `$r->setDefaults([...])`
    - Controller : `$this->createForm(Type::class, $data, $options)`
    - Ad hoc : `$this->createFormBuilder($data)->add(...)->getForm()`
    - Passez `$form` (la `FormInterface`) à Twig ; `createView()` est implicite.

## Connections

- **Depends on:** [Dependency injection](../dependency-injection/index.md) — les types sont des services autowirés (tag `form.type`) ; [Controllers](../controllers/index.md) fournit `createForm()`.
- **Reused in:** [Handling submissions](handling.md) — le form construit ici est exactement ce que `handleRequest()` lie.
- **Confused with:** [Form types](types.md) — une *classe de type* décrit les champs ; le *resolved type* est ce que la factory construit réellement.

## Official References
- [Official Symfony docs — Forms](https://symfony.com/doc/8.0/forms.html)
- [Official Symfony docs — How to define the data_class](https://symfony.com/doc/8.0/forms.html)
- [Symfony source — FormFactory](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/FormFactory.php)

## Video references

!!! tip "Watch & learn"
    Ce sont des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    « Symfony forms » pour consolider ce chapitre. Nous lions des chaînes stables
    plutôt que des vidéos individuelles pour que les références ne périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences et keynotes SymfonyCon.
    - [Official docs for this topic](https://symfony.com/doc/8.0/forms.html) — certaines pages de la doc Symfony embarquent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** une classe de type réutilisable vaut mieux qu'un `createFormBuilder` inline
- [ ] construire un form avec `buildForm` + `configureOptions` et `createForm()` en Symfony 8
- [ ] déboguer un form non lié et sans `data_class` qui vous renvoie `null` depuis `getData()`
- [ ] repérer la mauvaise réponse prétendant qu'un form composé retourne un objet sans `data_class`
- [ ] expliquer le chemin `createForm` → `FormFactory` → `ResolvedFormType` → arbre de builders

---

<small>Related: [Handling submissions](handling.md) · [Form types](types.md) ·
[Rendering](rendering.md)</small>

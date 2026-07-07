# Creating Forms

!!! tip "In a nutshell"
    You describe a form in a reusable type class (`buildForm` + `configureOptions`)
    and let the framework build it via `createForm()`. Exam hook: `data_class`
    binds the form to an object — without it, a compound form's data is a plain **array**.

!!! example "Real-world analogy"
    A form type is a **blank paper form**; `createForm()` hands you a fresh copy
    with a **clerk** attached. When you submit, the clerk reads each field and files
    the answers onto your **record** — `data_class` names which record file
    (a `RegistrationData`). With no `data_class`, the clerk just keeps a loose stack
    of labelled notes (an associative **array**).

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Build a form from a reusable **form type class** with `buildForm` and `configureOptions`.
    - [ ] Create an ad-hoc form with `createFormBuilder` inside a controller.
    - [ ] Explain how `data_class` binds a form to a PHP object and how the `FormFactory` resolves a type.

    **Syllabus:** `Forms → Creating forms` ·
    **Level:** Advanced → Expert ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Controllers](../controllers/index.md) · [DI](../dependency-injection/index.md)

---

## Theory

A Symfony form is an object graph of `Symfony\Component\Form\FormInterface`
instances built by a `Symfony\Component\Form\FormFactory`. You rarely touch the
factory directly. Instead you describe *what* the form contains in a **form type
class** and let the framework assemble it.

Two ways to create a form:

| Approach | Use when |
|---|---|
| **Form type class** (`AbstractType`) | Reusable form, tested in isolation, real apps |
| **`createFormBuilder`** | One-off form local to a single controller/action |

The controller helper `AbstractController::createForm(FqcnType::class, $data, $options)`
is the everyday entry point. Under the hood it calls
`FormFactoryInterface::create(...)`.

!!! question "Predict first"
    You call `createForm(RegistrationType::class)` on a compound form that does **not**
    set `data_class`, then read `getData()` before any submit. What comes back?

??? note "Reveal"
    An associative **array** keyed by child field name (or `null`/the initial array you
    passed). Only with `data_class` set does the form materialise a `new $dataClass()`
    via `empty_data` and map children onto that object through the data mapper.

## Deep Dive — how it works internally

### The form type class

A form type extends `Symfony\Component\Form\AbstractType` (which implements
`Symfony\Component\Form\FormTypeInterface`) and overrides two methods:

- `buildForm(FormBuilderInterface $builder, array $options)` — add fields and
  configure behaviour (event listeners, data mappers).
- `configureOptions(OptionsResolver $resolver)` — declare the options the type
  accepts and their defaults, using `Symfony\Component\OptionsResolver\OptionsResolver`.

`getBlockPrefix()` (defaults to the snake-cased class name without the `Type`
suffix) drives Twig block naming — see [theming](theming.md).

### How the factory builds the tree

```mermaid
flowchart LR
    A["createForm(Type::class)"] --> B[FormFactory::create]
    B --> C[FormRegistry::getType]
    C --> D[ResolvedFormType]
    D --> E["newBuilder + buildForm()"]
    E --> F["getForm(): FormInterface tree"]
```

1. `FormFactory::create()` calls `createBuilder()`, which asks the
   `Symfony\Component\Form\FormRegistry` for a
   `Symfony\Component\Form\ResolvedFormTypeInterface` (a *resolved type* wraps the
   type, its parent chain and all type extensions — see [types](types.md)).
2. The resolved type creates a `Symfony\Component\Form\FormBuilder`, then walks
   the **parent → child** chain calling each type's `buildForm()` and every
   registered type extension's `buildForm()`.
3. `getForm()` recursively turns the builder tree into an immutable
   `FormInterface` tree. Each field is itself a `Form` whose config is a
   `Symfony\Component\Form\FormConfigInterface`.

!!! note "Source reference"
    `Symfony\Component\Form\FormFactory` and `AbstractType` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/FormFactory.php).

### `data_class` and object binding

`data_class` tells the form which PHP class the underlying model is. When set:

- On build, the empty data becomes a `new $dataClass()` (via the `empty_data`
  option / the type's `getData`), and validation resolves constraints from that
  class's metadata.
- On submit, submitted values are written back onto that object through the
  **data mapper** (`Symfony\Component\Form\Extension\Core\DataMapper\DataMapper`,
  which uses PropertyAccess). Without `data_class`, a compound form yields an
  associative **array**.

### Null behavior

Right after `createForm()` — **before any submit** — `getData()` returns whatever
you passed. Pass nothing while `data_class` is set and the form still materialises
a `new $dataClass()` from the `empty_data` option, so it is never `null` at render
time. Pass nothing *without* `data_class` and `getData()` is `null` (or the initial
array you gave). Unmapped fields (`'mapped' => false`, like `plainPassword`) are
never written to the object — read them via `$form->get('plainPassword')->getData()`,
not the model. The common bug: type-hinting `getData()` as your DTO and
dereferencing it on an **unbound, `data_class`-less** form, hitting `null`.

!!! note "Null in real life"
    `null` = a blank record card the clerk has not filed anything onto yet — with a
    named record file (`data_class`) they always start you a fresh one.

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
    Since Symfony 6.2 you pass the `FormInterface` to the template and call
    `form(form)` in Twig; Symfony renders `createView()` for you. You may still
    call `$form->createView()` manually, but it is no longer required.

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| One reusable `AbstractType` per form | Building complex forms inline in controllers |
| Declare every option in `configureOptions` | Reading `$options['x']` that was never defined |
| Bind to a typed DTO/entity via `data_class` | Hand-parsing `$request->request` |
| Keep types stateless & autowired | Injecting request data into the type constructor |

## When (not) to use it / alternatives

Use `createFormBuilder` only for throwaway forms (a search box). Anything reused,
tested, or non-trivial belongs in a type class. For pure JSON APIs with no HTML
rendering, the Form component is often overkill — a DTO + the Serializer +
Validator is lighter (but the Form component still handles partial submits and
CSRF for you).

!!! danger "Certification traps"
    - `buildForm` receives a **`FormBuilderInterface`**, not a `FormInterface`.
      The form does not exist yet — you cannot read submitted data there.
    - Without `data_class`, a compound form's data is an **array**, not an object.
    - `configureOptions` uses `OptionsResolver`, **not** a plain array return.
    - `getBlockPrefix()` — not `getName()` (removed long ago) — controls Twig
      block names.

!!! warning "Common mistakes"
    - Passing `$form` and *also* `$form->createView()` — pick one.
    - Forgetting `methods: ['GET', 'POST']` on the route, so the POST 405s.
    - Putting field-add logic in `configureOptions` instead of `buildForm`.

## Exercises

1. **(Advanced)** Write a `ContactType` bound to a `ContactData` DTO with
   `name`, `email` and `message` fields, plus a `csrf_token_id`.
2. **(Expert)** Explain what `$form->getData()` returns immediately after
   `createForm(ContactType::class)` when (a) `data_class` is set and (b) it is not.

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

    **2.** (a) With `data_class`, `getData()` returns the object you passed
    (or a `new ContactData()` if none), so a fresh instance. (b) Without it,
    `getData()` returns `null` (or the initial array you gave `createForm`).

## Certification questions

??? question "Q1. Which two methods do you override on `AbstractType`?"
    - [ ] A. `build()` and `getOptions()`
    - [x] B. `buildForm()` and `configureOptions()` ✅
    - [ ] C. `configureFields()` and `setDefaults()`
    - [ ] D. `getName()` and `buildView()`

    **Why:** `buildForm(FormBuilderInterface, array)` adds fields;
    `configureOptions(OptionsResolver)` declares options. `getName` was removed;
    `buildView` exists but is not the primary pair.
    **Ref:** [Creating forms](https://symfony.com/doc/current/forms.html).

??? question "Q2. What does a compound form return from `getData()` when `data_class` is unset?"
    - [ ] A. `null` always
    - [x] B. An associative array keyed by child name ✅
    - [ ] C. A `stdClass`
    - [ ] D. A `FormInterface`

    **Why:** With no `data_class`, the data mapper maps children into/out of an
    array. Set `data_class` to bind to an object.
    **Ref:** [Form types](https://symfony.com/doc/current/form/data_class.html).

## Key takeaways

- A form type = `buildForm` (fields) + `configureOptions` (options via
  `OptionsResolver`).
- `createForm()` → `FormFactory` → `ResolvedFormType` → builder tree → immutable
  `FormInterface` tree.
- `data_class` binds the form to an object; without it you get an array.
- `getBlockPrefix()` drives Twig theming, not `getName()`.

## Last-minute revision

!!! tip "Cheat sheet"
    - `AbstractType::buildForm(FormBuilderInterface $b, array $o)`
    - `configureOptions(OptionsResolver $r)` → `$r->setDefaults([...])`
    - Controller: `$this->createForm(Type::class, $data, $options)`
    - Ad-hoc: `$this->createFormBuilder($data)->add(...)->getForm()`
    - Pass `$form` (the `FormInterface`) to Twig; `createView()` is implicit.

## Connections

- **Depends on:** [Dependency injection](../dependency-injection/index.md) — types are autowired services (`form.type` tag); [Controllers](../controllers/index.md) supplies `createForm()`.
- **Reused in:** [Handling submissions](handling.md) — the built form is exactly what `handleRequest()` binds.
- **Confused with:** [Form types](types.md) — a *type class* describes fields; the *resolved type* is what the factory actually builds.

## Official References
- [Official Symfony docs — Forms](https://symfony.com/doc/current/forms.html)
- [Official Symfony docs — How to define the data_class](https://symfony.com/doc/current/form/data_class.html)
- [Symfony source — FormFactory](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/FormFactory.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony forms" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/forms.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** a reusable type class beats an inline `createFormBuilder`
- [ ] build a form with `buildForm` + `configureOptions` and `createForm()` in Symfony 8
- [ ] debug an unbound, `data_class`-less form that hands you `null` from `getData()`
- [ ] spot the wrong answer claiming a compound form returns an object without `data_class`
- [ ] explain the `createForm` → `FormFactory` → `ResolvedFormType` → builder tree path

---

<small>Related: [Handling submissions](handling.md) · [Form types](types.md) ·
[Rendering](rendering.md)</small>

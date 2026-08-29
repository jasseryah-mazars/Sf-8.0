# Revision Sheet — Forms

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Forms](../../forms/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Une **fiche imprimable, tenant sur une page**, qui résume chaque sous-chapitre de Forms en quelques puces "à retenir" suivies d'une ligne "Cheat" très dense.

**Pourquoi ça existe ?** Dans les derniers jours avant l'examen, on veut un support papier ou PDF unique par domaine — pas 10 onglets de navigateur ouverts. Cette fiche condense un domaine entier sur une seule page imprimable.

**🏠 Analogie de la vraie vie :** C'est la **fiche de révision recto-verso** qu'un étudiant prépare avant un examen universitaire : tout le cours du semestre réduit à une page, à relire dans le métro le matin de l'épreuve.

**Symfony dans la vraie vie :** Chaque puce "à retenir" → une règle déjà apprise en détail dans le chapitre / La ligne "Cheat:" → la version ultra-compacte, presque un aide-mémoire de syntaxe / Lien "Full detail" → retour au chapitre complet si un point ne "sonne" plus familier.

**⚠️ Erreur fréquente :** Imprimer cette fiche *avant* d'avoir étudié Forms en détail, en espérant apprendre directement dessus — le format est trop dense pour un premier apprentissage, il ne fonctionne qu'en rappel.

**🧠 Comment le mémoriser :** *« Une page, un domaine, la veille de l'examen »* — cette fiche est le tout dernier support à consulter, pas le premier.

## Built-in Form Types Catalogue
- Core types live in `Extension\Core\Type\*`; `EntityType` (Doctrine) is out of
  scope — use `ChoiceType` with `choices`.
- `ChoiceType` widget = `expanded` × `multiple`.
- `CollectionType` (dynamic lists) and `RepeatedType` (confirmations) are
  compound helpers; buttons are unmapped.
- Numeric/date types carry transformers; prefer `single_text` dates.

**Cheat:** Text: `Text/Textarea/Email/Password(always_empty)/Integer/Number/Money/Hidden`. `Choice`: `choices`, `expanded`, `multiple`, `placeholder`. `Date/Time/DateTime`: `widget` (choice/text/single_text), `input`. `Collection`: `entry_type`, `allow_add/delete`, `by_reference:false`, `prototype`. `Repeated`: `type`, `first_options`/`second_options`.

## Creating Forms
- A form type = `buildForm` (fields) + `configureOptions` (options via
  `OptionsResolver`).
- `createForm()` → `FormFactory` → `ResolvedFormType` → builder tree → immutable
  `FormInterface` tree.
- `data_class` binds the form to an object; without it you get an array.
- `getBlockPrefix()` drives Twig theming, not `getName()`.

**Cheat:** `AbstractType::buildForm(FormBuilderInterface $b, array $o)` `configureOptions(OptionsResolver $r)` → `$r->setDefaults([...])` Controller: `$this->createForm(Type::class, $data, $options)` Ad-hoc: `$this->createFormBuilder($data)->add(...)->getForm()` Pass `$form` (the `FormInterface`) to Twig; `createView()` is implicit.

## CSRF Protection in Forms
- CSRF protection is on by default; a hidden `_token` field is added and checked.
- Options: `csrf_protection`, `csrf_field_name` (`_token`), `csrf_token_id`.
- Validation happens on **PRE_SUBMIT** via `CsrfValidationListener`.
- Stateless CSRF (7.2+/8) via `stateless_token_ids` needs no session.

**Cheat:** Default field: `_token`; default id: form block prefix. Validate: PRE_SUBMIT, `CsrfValidationListener`. Stateless: `framework.csrf_protection.stateless_token_ids: [...]`. Manual: `csrf_token('intention')` in Twig · `isCsrfTokenValid('intention', $t)`. Never disable CSRF for cookie-authenticated state changes.

## Data Transformers
- `transform` = model→view (display); `reverseTransform` = view→model (submit).
- Model transformer = model↔norm; view transformer = norm↔view.
- On submit, view transformers run before model transformers (reverse order).
- Bad input ⇒ `TransformationFailedException` ⇒ invalid field, not a 500.

**Cheat:** `transform()` → toward VIEW · `reverseTransform()` → toward MODEL. `addViewTransformer` (norm↔view) · `addModelTransformer` (model↔norm). Empty/null handling first, always. Failure: `throw new TransformationFailedException(...)`.

## Form Events
- Five events on `FormEvents`; two sequences (set vs submit).
- Set: PRE_SET_DATA → POST_SET_DATA. Submit: PRE_SUBMIT → SUBMIT → POST_SUBMIT.
- Data shape per event: PRE_SET_DATA=model, PRE_SUBMIT=raw view, SUBMIT=norm,
  POST_SUBMIT=model.
- Add/remove fields only on PRE_* events; validation is a POST_SUBMIT listener.

**Cheat:** `PRE_SET_DATA`(model) · `POST_SET_DATA`(model) `PRE_SUBMIT`(raw) · `SUBMIT`(norm) · `POST_SUBMIT`(model) Dynamic fields: PRE_SET_DATA (initial), PRE_SUBMIT (submitted). `addEventListener` / `addEventSubscriber` on the builder. No `PRE_VALIDATE`; validation = POST_SUBMIT listener.

## Handling File Uploads
- `FileType` → `UploadedFile`; read unmapped uploads via `->get('x')->getData()`.
- Rename with a slug + `uniqid()`; never trust client name/MIME.
- Validate with `File`/`Image` constraints (content-based checks).
- `form_start` sets multipart automatically when a file field is present.

**Cheat:** `UploadedFile`: `move($dir, $name)`, `guessExtension()`, `getMimeType()`. Untrusted: `getClientOriginalName()`, `getClientMimeType()`. `mapped => false` → still validated; fetch via `->getData()`. `File(maxSize: '5m', mimeTypes: [...])` / `Image(...)`. See also controllers/file-upload.

## Handling Submissions
- Canonical flow: `handleRequest` → `isSubmitted() && isValid()` → `getData()` →
  **redirect**.
- Three data shapes: model ↔ norm ↔ view, bridged by transformers.
- Submit events: **PRE_SUBMIT → SUBMIT → POST_SUBMIT**; validation on the last.
- `PATCH` ⇒ `clearMissing = false` (partial update).

**Cheat:** `handleRequest` delegates to `HttpFoundationRequestHandler`. `submit($data, $clearMissing = true)`; PATCH ⇒ `false`. `getData()` = model, `getNormData()` = norm, `getViewData()` = view. `getErrors(true)` = deep error iterator. Always **redirect** after a successful POST.

## Rendering Forms with Twig
- `form(form)` renders everything; `form_start`/`form_end` bracket manual layouts.
- `form_row` = label + widget + errors + help; the granular functions split it.
- `form_end`/`form_rest` emit hidden + CSRF fields — never lose them.
- Rendering works on the `FormView` via `FormRenderer` resolving theme blocks.

**Cheat:** `form_start(form, {attr:{...}})` / `form_end(form, {render_rest:false})` `form_row / form_label / form_widget / form_errors / form_help` `form_rest(form)` → hidden + CSRF. Override label: `form_label(field, 'Text')`. Pass the `FormInterface`; Twig calls `createView()`.

## Form Theming
- A theme is a set of Twig blocks; default is `form_div_layout.html.twig`.
- Apply via `{% form_theme %}` or `twig.form_themes` (last wins).
- Block lookup: unique id → field name → block prefix → parent → `form_*`.
- Built-in framework layouts are **markup themes only**.

**Cheat:** `{% form_theme form 'x.html.twig' %}` · `_self` (no `extend`). Global: `twig.form_themes: [...]` (order matters). Blocks: `{prefix}_row/_label/_widget/_errors/_help`. `{% use 'base' %}` to inherit blocks, override deltas. Bootstrap layout = markup, not CSS.

## Form Type Extensions
- A type extension augments existing types without subclassing; one class can
  target many types.
- Extend `AbstractTypeExtension`; implement static `getExtendedTypes(): iterable`.
- Autoconfiguration tags it `form.type_extension` — **no attribute** exists.
- Extension hooks run after the extended type's hooks; `FormType::class` = all
  forms.

**Cheat:** `class X extends AbstractTypeExtension`. `public static function getExtendedTypes(): iterable` → `[FooType::class]`. Hooks: `configureOptions/buildForm/buildView/finishView`. Register: autoconfig → `form.type_extension`; manual tag needs `extended_type`. No `#[AsFormTypeExtension]`; `getExtendedType()` (singular) is gone.

## Form Types & the Type Hierarchy
- Types form an inheritance chain rooted at `FormType`; `getParent()` returns a
  class string.
- `ResolvedFormType` = type + parent chain + type extensions; it drives build.
- Parent hooks run before child hooks (options and build).
- Options are declared/validated with `OptionsResolver`; FQCN is the type id.

**Cheat:** Built-in: `Symfony\Component\Form\Extension\Core\Type\*`. `getParent(): string` → e.g. `TextType::class`. `OptionsResolver`: `setDefaults / setRequired / setAllowedTypes / setNormalizer`. No `getName()`; `getBlockPrefix()` for theming; FQCN is the id. `form.type` tag autoconfigured → inject services into types.

# Flashcards — Forms

72 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

??? question "1. Which two methods do you typically override in an AbstractType?"
    **✅ buildForm(FormBuilderInterface, array) and configureOptions(OptionsResolver)**

    buildForm() adds fields to the builder; configureOptions() declares the type's options via OptionsResolver. getName() was removed; buildView() exists but is not the primary pair.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "2. A compound form with no data_class set returns what from getData()?"
    **✅ An associative array keyed by child field name**

    Without data_class the data mapper maps children into and out of an array. Set data_class to bind the form to an object instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_class.html)

??? question "3. Where should field-adding logic live in a form type?"
    **✅ In buildForm(), using the FormBuilderInterface**

    buildForm() receives the builder and is where ->add() calls belong. configureOptions() only declares options via OptionsResolver.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "4. A developer writes `public function configureOptions(OptionsResolver $resolver): void { return ['data_class' => Contact::class]; }`. Why does the form type fail to compile / behave?"
    **✅ configureOptions() returns void; you must call $resolver->setDefaults([...]), not return an array**

    configureOptions() has a void return type and configures the injected OptionsResolver imperatively via setDefaults()/setRequired()/setAllowedTypes(). Returning an array does nothing. ::class constants are perfectly valid option values, and there is no requirement to call the parent (AbstractType's is empty).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_custom_field_type.html)

??? question "5. When you call $this->createForm(RegistrationType::class, $data), which object resolves the type's parent chain and extensions before the builder tree is built?"
    **✅ FormFactory::create() asks FormRegistry for a ResolvedFormType, which builds the FormBuilder and walks buildForm() parent→child**

    createForm() delegates to FormFactory::create(), which via FormRegistry obtains a ResolvedFormType wrapping the type, its resolved parent chain and applicable type extensions. The resolved type creates a FormBuilder and runs each buildForm() from parent to child; getForm() then produces the immutable FormInterface tree. OptionsResolver only resolves options; the DataMapper maps data at submit/view time.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/FormFactory.php)

??? question "6. Inside buildForm(FormBuilderInterface $builder, array $options), can you read the user's submitted values (e.g. $builder->getData() as posted input)?"
    **✅ No — buildForm() runs at build time on a FormBuilderInterface; the form is not submitted yet, so there is no request data to read**

    buildForm() receives a FormBuilderInterface, not a submitted FormInterface. The form does not exist yet and handleRequest()/submit() have not run, so submitted input is unavailable. To react to submitted values, add a PRE_SUBMIT listener, which fires later with the raw view data. There is no $builder->getRequest().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "7. What determines the Twig block name used to theme a custom form type?"
    **✅ getBlockPrefix() (defaults to the snake_cased class name without the Type suffix)**

    getBlockPrefix() drives Twig block naming; it defaults to the snake-cased short class name minus the Type suffix. getName() was removed long ago — the FQCN is now the type identifier, but the FQCN is not used verbatim for block names.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_custom_field_type.html)

??? question "8. What is the canonical order of the controller form-handling calls?"
    **✅ handleRequest(), then isSubmitted() && isValid(), then getData()**

    handleRequest() inspects the request and submits the form; only then are isSubmitted()/isValid() meaningful, after which getData() holds the model.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "9. For a PATCH submission, handleRequest passes which clearMissing value?"
    **✅ false, enabling partial updates (absent fields keep their value)**

    handleRequest passes clearMissing: false for PATCH so fields missing from the payload retain their current value, enabling partial updates.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Form.php)

??? question "10. Which service does FormInterface::handleRequest() delegate to under FrameworkBundle?"
    **✅ HttpFoundationRequestHandler**

    With HttpFoundation available, the form's request handler is HttpFoundationRequestHandler; NativeRequestHandler is the fallback when working with PHP superglobals directly.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Extension/HttpFoundation/HttpFoundationRequestHandler.php)

??? question "11. Why redirect after a successful POST (POST-redirect-GET)?"
    **✅ So a browser refresh re-fetches a GET instead of re-submitting the form**

    Without the redirect, refreshing re-POSTs the data and duplicates side effects. Redirecting lands the browser on a safe GET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "12. What happens if you call $form->isValid() on a form that was never submitted?"
    **✅ It throws a LogicException ('Cannot check if an unsubmitted form is valid')**

    isValid() is only meaningful after submission, so calling it on an unsubmitted form throws a LogicException. Always guard with isSubmitted() first (isSubmitted() && isValid()). It does not auto-submit or silently return a value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "13. A form posts to a controller and the browser gets a 405 Method Not Allowed on submit, though the page renders fine on GET. What is the most likely cause?"
    **✅ The route restricts methods to GET (missing POST in methods: ['GET','POST'])**

    A 405 comes from the router rejecting the HTTP method before the controller runs, so the route must allow POST as well as GET. A missing handleRequest() or CSRF token would let the request through and manifest as a form not submitting or an invalid-token error, not a 405; data_class is unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "14. Which accessor returns each of a field's three data representations after submit?"
    **✅ getData() = model, getNormData() = normalized, getViewData() = view**

    A field holds data in three shapes: model (your PHP value), normalized (transport-neutral canonical), and view (strings for HTML). They are read with getData()/getNormData()/getViewData() respectively; transformers convert between adjacent shapes. There are no getModelData()/getRenderedData() methods.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "15. What does a form type's getParent() return?"
    **✅ The parent type's fully-qualified class name (a string)**

    getParent() returns a class string (default FormType::class). The registry resolves it into the parent chain of a ResolvedFormType.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_custom_field_type.html)

??? question "16. Which object bundles a type with its parent chain and applicable extensions?"
    **✅ ResolvedFormType**

    FormRegistry produces a ResolvedFormType wrapping the type, its resolved parent, and every type extension that applies.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/ResolvedFormType.php)

??? question "17. In what order do configureOptions() run along the type hierarchy?"
    **✅ Parent first, then child (child can override parent defaults)**

    The resolved type walks the chain top-down, so parent defaults are set before the child's, letting the child override them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "18. A custom type does `public function getParent(): string { return new TextType(); }`. What is wrong?"
    **✅ getParent() must return a class-string (TextType::class), not an instance**

    getParent() is declared to return string; returning an object violates the return type and the registry expects an FQCN to resolve. Use TextType::class. It is not static and returns a single string, not an array.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_custom_field_type.html)

??? question "19. In configureOptions(), which OptionsResolver call derives one option's value from the values of others?"
    **✅ setNormalizer('opt', fn (Options $o, $value) => ...)**

    setNormalizer() receives the resolved Options plus the raw value, letting one option depend on others (e.g. force expanded when multiple is false). setAllowedTypes validates a type, setRequired marks an option mandatory, and a default closure cannot read sibling options the way a normalizer can.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/options_resolver.html)

??? question "20. How are custom form types made available by their FQCN and able to receive injected services?"
    **✅ FrameworkBundle autoconfigures FormTypeInterface implementers with the form.type tag**

    Service autoconfiguration tags any class implementing FormTypeInterface with form.type, so it is usable by FQCN and can autowire constructor dependencies. There is no #[AsFormType] attribute and no runtime directory scan; manual tagging is only needed when autoconfiguration is disabled.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_custom_field_type.html)

??? question "21. What does form_row(form.email) render?"
    **✅ Label, widget, errors and help for that field**

    form_row composes the label, widget, errors and help via the *_row theme block. form_widget renders only the control.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_customization.html)

??? question "22. How is the hidden CSRF token normally emitted into the HTML?"
    **✅ By form_rest, which form_end calls by default**

    The CSRF token is a hidden child rendered by form_rest; form_end triggers form_rest unless you pass render_rest: false.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/csrf.html)

??? question "23. Which call renders form-level (non-field) errors?"
    **✅ form_errors(form)**

    Passing the root form view to form_errors renders errors attached to the form itself; per-field errors use form_errors(form.field).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "24. A template renders each field manually and ends with `{{ form_end(form, {'render_rest': false}) }}`. Submissions now fail with an invalid CSRF token. Why?"
    **✅ render_rest: false suppresses form_rest, so the hidden _token is never emitted; render form_rest(form) yourself**

    form_end normally calls form_rest, which renders un-rendered fields including the hidden CSRF token. Passing render_rest: false skips that, so the _token is absent and PRE_SUBMIT validation fails. Render form_rest(form) (or the token) manually. Manual layouts are fully CSRF-capable; the token has nothing to do with speed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "25. How do partial rendering (form_row on some fields) and form_rest avoid rendering the same field twice?"
    **✅ Each FormView carries an isRendered() flag; form_row/form_widget set it, and form_rest skips already-rendered views**

    Rendering operates on the FormView tree. Each view has an isRendered() flag set when form_row/form_widget renders it, so form_rest emits only the leftover (un-rendered) fields — including hidden and CSRF fields. There is no string diffing.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/FormExtension.php)

??? question "26. Which Twig call is wrong for rendering a single field's widget?"
    **✅ form(form.email) — form() is for the whole form; use form_widget/form_row for a field**

    form() renders an entire form (start, rows, end). For an individual field use form_row (label+widget+errors+help) or the granular form_widget/form_label/ form_errors/form_help. Calling form() on a child view is a common mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_customization.html)

??? question "27. In which order does the renderer try candidate theme blocks?"
    **✅ Most specific (unique field id) down to least specific (form_widget)**

    The block-prefix hierarchy is walked from the unique per-field name down to the root form_* block; the first existing block wins.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_themes.html)

??? question "28. What does the built-in bootstrap_5_layout.html.twig provide?"
    **✅ Twig blocks producing Bootstrap-compatible markup (a theme only)**

    Built-in layouts are theme templates (markup only). You still load the CSS framework yourself; the Form component ships no assets.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/bootstrap5.html)

??? question "29. When two global form themes define the same block, which wins?"
    **✅ The theme listed last in twig.form_themes**

    Themes in twig.form_themes are applied in order; later entries override earlier ones on a block clash.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_themes.html)

??? question "30. Which twig.yaml block applies a Bootstrap theme app-wide, then lets your own file override its blocks?"
    **✅ twig: { form_themes: ['bootstrap_5_layout.html.twig', 'form/fields.html.twig'] }**

    form_themes are applied in order and the last wins on conflicts, so your file must come after the Bootstrap layout to override its blocks. The key is twig.form_themes (a list), not twig.theme or a framework.* key.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_themes.html)

??? question "31. What is required to theme a form with {% form_theme form _self %}?"
    **✅ The template must NOT {% extends %} another template**

    _self references the current template's own blocks, which requires that the template does not extend another (extending re-scopes blocks). It works for any field's blocks, not just CSRF, and does not need a form_themes entry or macros.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_themes.html)

??? question "32. A field with block prefix 'rating' (parent 'integer') ignores your integer_widget override, but rating_widget works. Why?"
    **✅ The renderer tries rating_widget before integer_widget; the more specific block exists and wins, so integer_widget is never reached**

    Block-name resolution goes most-specific to least-specific along the block-prefix chain (rating → integer → form). Since rating_widget exists, it wins and the more generic integer_widget is never consulted. Override rating_widget (or remove it to fall through). inherit_data and caching are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_themes.html)

??? question "33. At which form event is the CSRF token validated?"
    **✅ PRE_SUBMIT**

    CsrfValidationListener runs on PRE_SUBMIT: it pops the _token field from the raw submitted data and validates it, adding a form error on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/csrf.html)

??? question "34. What does the csrf_token_id option control?"
    **✅ The token intention/namespace used to generate and validate it**

    csrf_token_id is the intention string. csrf_field_name sets the HTML field name (default _token); csrf_protection toggles the feature.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/form.html)

??? question "35. Stateless CSRF (Symfony 7.2+/8) primarily removes the need for what?"
    **✅ A server-side session to store the token**

    With framework.csrf_protection.stateless_token_ids, the SameOriginCsrfTokenManager validates via a double-submit cookie plus origin checks, so no token is stored in the session.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/csrf.html)

??? question "36. Which configuration enables stateless CSRF for the login and logout token ids?"
    **✅ framework: { csrf_protection: { stateless_token_ids: ['authenticate', 'logout'] } }**

    Stateless CSRF is enabled per token id by listing them under framework.csrf_protection.stateless_token_ids; forms whose csrf_token_id is in that list use SameOriginCsrfTokenManager. There is no boolean stateless/session flag, and the key lives under framework, not security.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/csrf.html)

??? question "37. When a submission arrives with a missing or invalid _token, what does CsrfValidationListener do?"
    **✅ It adds a form error (so isValid() returns false) — it does not throw an exception**

    On PRE_SUBMIT the listener pops _token from the raw data and validates it; a missing/invalid token results in a form error, so isValid() is false and you re-render with csrf_message. It does not throw or short-circuit with a 403 — that is the pattern for the manual isCsrfTokenValid() helper in a controller.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Extension/Csrf/Type/FormTypeCsrfExtension.php)

??? question "38. If csrf_token_id is not set explicitly on a form, what is its default value?"
    **✅ The form's block prefix**

    The default csrf_token_id is the form's block prefix; setting it explicitly makes the intention stable regardless of the class name. '_token' is the default csrf_field_name (the HTML name), not the id, and the token is not the app secret nor regenerated per request within a namespace.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/form.html)

??? question "39. How do you read the value of an unmapped FileType field?"
    **✅ $form->get('field')->getData()**

    mapped => false excludes the field from the data mapper, so it is not written to the model; you fetch it directly from the child form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

??? question "40. Which UploadedFile value is safe to trust for validating file type?"
    **✅ getMimeType()/guessExtension() (content-based)**

    Client-supplied name and MIME are spoofable. Content-based guessing (used by the File/Image constraints) is authoritative.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)

??? question "41. When does form_start emit enctype="multipart/form-data"?"
    **✅ When the form contains a file field**

    The form's multipart view variable is set when a child (e.g. FileType) requires it, and form_start renders the enctype accordingly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/file.html)

??? question "42. On an optional upload field, the controller calls $file->move(...) and occasionally crashes with a fatal error. What is the fix?"
    **✅ Guard with `if ($file instanceof UploadedFile)` — getData() is null when no file was uploaded**

    An optional FileType returns null from getData() when nothing is uploaded, so calling move() on null is fatal. Check `$file instanceof UploadedFile` first. Forcing required doesn't fit an optional field, re-running handleRequest is wrong, and bypassing the form loses validation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

??? question "43. Is a FileType field with mapped => false still validated by its constraints?"
    **✅ Yes — mapped => false only stops data-mapping; the field is still rendered, submitted and validated**

    mapped => false only disconnects the field from the data mapper (it is not written to the model). The field is still part of the form: rendered, submitted, and validated via its constraints option — which is exactly why the pattern is safe for uploads and plain passwords.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

??? question "44. What is the recommended way to name an uploaded file before move()?"
    **✅ Slug the original basename, append uniqid(), and use guessExtension()**

    Generate a safe name: slug the original filename, add uniqid() for uniqueness, and derive the extension from guessExtension() (content-based). Using the client name risks path traversal, the tmp_name is transient, and persisting the UploadedFile object (Doctrine is out of scope) is wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

??? question "45. Which ChoiceType options render checkboxes?"
    **✅ expanded => true, multiple => true**

    expanded + multiple renders checkboxes; expanded + single renders radios; collapsed renders a select element.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/choice.html)

??? question "46. What does MoneyType's divisor option do?"
    **✅ Scales the model value (e.g. 100 lets you store integer cents)**

    The displayed amount is divided by divisor to form the model value, so 100 lets you store amounts in cents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/money.html)

??? question "47. For a mapped CollectionType to call the parent's adder/remover methods, set…"
    **✅ by_reference => false**

    by_reference => false forces the form to call add/remove methods instead of mutating the returned collection in place, keeping associations in sync.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/collection.html)

??? question "48. Which type is out of scope here because it belongs to the Doctrine bridge?"
    **✅ EntityType**

    EntityType lives in the Doctrine bridge and is out of scope. Use ChoiceType with explicit choices for the non-Doctrine equivalent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/choice.html)

??? question "49. For a DateType that renders one HTML5 date input and produces a \DateTimeImmutable model, which options do you set?"
    **✅ widget => 'single_text', input => 'datetime_immutable'**

    widget controls rendering: single_text is one type=\"date\" input (best with HTML5); choice renders dropdowns and text renders three text fields. input picks the model type — datetime_immutable is the recommended value, whereas string, timestamp and array yield other model shapes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/date.html)

??? question "50. What is RepeatedType used for?"
    **✅ Rendering one inner type twice (e.g. password + confirmation) that only passes if both entries match**

    RepeatedType renders its inner type (via the type option) twice — configured with first_options/second_options — and validates only if both values match, ideal for password confirmation. The dynamic add/remove list is CollectionType, not RepeatedType.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/repeated.html)

??? question "51. Which statements about PasswordType and button types are correct? (choose 2)"
    **✅ PasswordType is not re-rendered with its value by default (always_empty => true) ; SubmitType/ButtonType/ResetType are not part of the mapped form data**

    PasswordType defaults to always_empty => true, so the field renders blank after submit for safety. Buttons (Submit/Button/Reset) are unmapped — they carry no data — though SubmitType lets you detect the clicked button via getClickedButton().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/password.html)

??? question "52. In which direction does reverseTransform() run?"
    **✅ View to model (on submission)**

    transform() converts toward the view (display); reverseTransform() converts toward the model (submission). Reversing these is the classic trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "53. addModelTransformer() converts between which representations?"
    **✅ Model and normalized data**

    Model transformers bridge model<->norm; view transformers bridge norm<->view. Pick a model transformer when the underlying type changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "54. What should a transformer throw when input cannot be converted?"
    **✅ TransformationFailedException**

    TransformationFailedException is caught by the form and turned into a field-level invalid state showing the field's invalid_message, not a 500.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Form.php)

??? question "55. On submit, which transformers run first?"
    **✅ View transformers (view->norm), then model transformers (norm->model)**

    On submission data flows view -> norm -> model, so view transformers' reverseTransform runs before model transformers' reverseTransform.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "56. In a DataTransformer, what should transform(null) return when the model value is unset?"
    **✅ '' (an empty string the widget can display)**

    On display, transform(null) fires for an unset model value and should return '' so the input renders cleanly and later value comparisons hold; returning null can make the widget render oddly. Throwing is for genuinely unconvertible input on reverseTransform, not for a normal empty value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "57. An optional text field with a custom transformer reports 'invalid' whenever it is left blank. What is the likely cause?"
    **✅ reverseTransform('') runs the parser on an empty string and throws TransformationFailedException; guard for ''/null and return the empty model value first**

    An empty submission arrives as '' (or null) at reverseTransform(); if you parse it instead of short-circuiting, you raise a spurious TransformationFailedException and the field is marked invalid. Guard the first line for emptiness and return the model's empty value (null/[]/0). This is a format-handling bug, not a validation constraint issue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "58. You need a field whose view is an id string but whose model is a domain object. Which transformer slot fits?"
    **✅ A model transformer (the underlying type changes: id string <-> object)**

    Use a model transformer when the type of the underlying object changes (id <-> rich object); it bridges model<->norm. A view transformer is for pure string formatting (norm<->view). The slot matters because it determines where in the pipeline the conversion runs and what the norm data looks like.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "59. What is the correct order of the submit-phase form events?"
    **✅ PRE_SUBMIT -> SUBMIT -> POST_SUBMIT**

    Submission dispatches PRE_SUBMIT (raw view data), SUBMIT (normalized), then POST_SUBMIT (bound model), in that order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "60. What is the correct order of the set-data-phase form events?"
    **✅ PRE_SET_DATA -> POST_SET_DATA**

    Setting data (on create/populate) dispatches PRE_SET_DATA then POST_SET_DATA. There is no SET_DATA constant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "61. On PRE_SUBMIT, what does $event->getData() return?"
    **✅ The raw submitted view data (an array/string)**

    PRE_SUBMIT fires before transformation, so the data is the raw request values — not your object.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "62. To add a field based on the submitted value, which event do you listen on?"
    **✅ PRE_SUBMIT**

    Fields must be added before binding. PRE_SUBMIT exposes the raw submitted value while the form is still mutable (dynamic/dependent fields).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/dynamic_form_modification.html)

??? question "63. Which event does the validator form extension hook to run validation?"
    **✅ POST_SUBMIT**

    Validation runs after data is bound to the model, via a POST_SUBMIT listener. There is no PRE_VALIDATE/POST_VALIDATE in FormEvents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "64. In a PRE_SUBMIT listener you read the submitted country. Which line is safe?"
    **✅ $country = $event->getData()['country'] ?? null;**

    PRE_SUBMIT data is the raw request array, so a blank field is simply an absent key — read it with ?? null to avoid an undefined-key warning. Treating the data as an object (->getCountry()) is wrong: it is not transformed yet, and the model on the form is not yet populated from this submission.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "65. Which of these is NOT a real FormEvents constant?"
    **✅ FormEvents::PRE_VALIDATE**

    There is no PRE_VALIDATE (nor POST_VALIDATE) in FormEvents. The five constants are PRE_SET_DATA, POST_SET_DATA, PRE_SUBMIT, SUBMIT and POST_SUBMIT; validation is simply a POST_SUBMIT listener registered by the validator extension.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/FormEvents.php)

??? question "66. How do you attach a reusable event subscriber to a form?"
    **✅ Implement EventSubscriberInterface (with getSubscribedEvents()) and call $builder->addEventSubscriber($subscriber)**

    Form subscribers implement the EventDispatcher's EventSubscriberInterface (the Form component has no dedicated FormEventSubscriberInterface) declaring getSubscribedEvents(), and are added with $builder->addEventSubscriber(). There is no #[AsFormSubscriber] attribute or framework.form.subscribers config for this.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "67. Which method declares the types a form type extension applies to?"
    **✅ public static function getExtendedTypes(): iterable**

    getExtendedTypes() is static and returns an iterable of type FQCNs. It replaced the removed singular getExtendedType().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_form_type_extension.html)

??? question "68. With autoconfiguration enabled, how is a type extension registered?"
    **✅ Automatically, via the form.type_extension tag on FormTypeExtensionInterface services**

    Symfony auto-tags implementers of FormTypeExtensionInterface with form.type_extension. There is no dedicated attribute for this in core.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_form_type_extension.html)

??? question "69. What is the effect of returning FormType::class from getExtendedTypes()?"
    **✅ The extension applies to every form type (all descend from FormType)**

    Because all types inherit from FormType, the extension attaches to every form — powerful for global concerns but risky to overuse.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_form_type_extension.html)

??? question "70. Which attribute registers a form type extension in core Symfony?"
    **✅ There is none — core has no #[AsFormTypeExtension]; registration is by interface + getExtendedTypes() (autoconfig) or a manual tag**

    Unlike #[AsEventListener] or #[AsCommand], form type extensions have no dedicated attribute in core. Autoconfiguration tags FormTypeExtensionInterface services with form.type_extension, and getExtendedTypes() tells the registry which types to attach them to; a manual form.type_extension tag with extended_type is the fallback when autoconfiguration is off.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_form_type_extension.html)

??? question "71. A type extension defines `public function getExtendedType(): string { return FileType::class; }` but never applies. What is wrong?"
    **✅ The singular getExtendedType() was removed; you must implement the static getExtendedTypes(): iterable returning [FileType::class]**

    Registration keys off the static getExtendedTypes(): iterable; the old singular getExtendedType() no longer exists, so the extension is never matched to a type. Any type (including FileType) can be extended, and the method is static/public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_form_type_extension.html)

??? question "72. With autoconfiguration disabled, which services.yaml tag correctly registers an extension for FileType?"
    **✅ tags: [{ name: form.type_extension, extended_type: Symfony\Component\Form\Extension\Core\Type\FileType }]**

    Without autoconfiguration you must both use the form.type_extension tag and supply the extended_type attribute (the FQCN of the extended type) — it is not inferred from getExtendedTypes() in the manual case. form.type is for form types, and form.extension is not a real tag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_form_type_extension.html)

---

<small>Back to [Flashcards](index.md) · [Forms](../../forms/index.md)</small>

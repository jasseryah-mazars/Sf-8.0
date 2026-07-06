# Flashcards — Forms

38 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

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

??? question "4. What is the canonical order of the controller form-handling calls?"
    **✅ handleRequest(), then isSubmitted() && isValid(), then getData()**

    handleRequest() inspects the request and submits the form; only then are isSubmitted()/isValid() meaningful, after which getData() holds the model.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "5. For a PATCH submission, handleRequest passes which clearMissing value?"
    **✅ false, enabling partial updates (absent fields keep their value)**

    handleRequest passes clearMissing: false for PATCH so fields missing from the payload retain their current value, enabling partial updates.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Form.php)

??? question "6. Which service does FormInterface::handleRequest() delegate to under FrameworkBundle?"
    **✅ HttpFoundationRequestHandler**

    With HttpFoundation available, the form's request handler is HttpFoundationRequestHandler; NativeRequestHandler is the fallback when working with PHP superglobals directly.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Extension/HttpFoundation/HttpFoundationRequestHandler.php)

??? question "7. Why redirect after a successful POST (POST-redirect-GET)?"
    **✅ So a browser refresh re-fetches a GET instead of re-submitting the form**

    Without the redirect, refreshing re-POSTs the data and duplicates side effects. Redirecting lands the browser on a safe GET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "8. What does a form type's getParent() return?"
    **✅ The parent type's fully-qualified class name (a string)**

    getParent() returns a class string (default FormType::class). The registry resolves it into the parent chain of a ResolvedFormType.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_custom_field_type.html)

??? question "9. Which object bundles a type with its parent chain and applicable extensions?"
    **✅ ResolvedFormType**

    FormRegistry produces a ResolvedFormType wrapping the type, its resolved parent, and every type extension that applies.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/ResolvedFormType.php)

??? question "10. In what order do configureOptions() run along the type hierarchy?"
    **✅ Parent first, then child (child can override parent defaults)**

    The resolved type walks the chain top-down, so parent defaults are set before the child's, letting the child override them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "11. What does form_row(form.email) render?"
    **✅ Label, widget, errors and help for that field**

    form_row composes the label, widget, errors and help via the *_row theme block. form_widget renders only the control.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_customization.html)

??? question "12. How is the hidden CSRF token normally emitted into the HTML?"
    **✅ By form_rest, which form_end calls by default**

    The CSRF token is a hidden child rendered by form_rest; form_end triggers form_rest unless you pass render_rest: false.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/csrf.html)

??? question "13. Which call renders form-level (non-field) errors?"
    **✅ form_errors(form)**

    Passing the root form view to form_errors renders errors attached to the form itself; per-field errors use form_errors(form.field).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "14. In which order does the renderer try candidate theme blocks?"
    **✅ Most specific (unique field id) down to least specific (form_widget)**

    The block-prefix hierarchy is walked from the unique per-field name down to the root form_* block; the first existing block wins.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_themes.html)

??? question "15. What does the built-in bootstrap_5_layout.html.twig provide?"
    **✅ Twig blocks producing Bootstrap-compatible markup (a theme only)**

    Built-in layouts are theme templates (markup only). You still load the CSS framework yourself; the Form component ships no assets.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/bootstrap5.html)

??? question "16. When two global form themes define the same block, which wins?"
    **✅ The theme listed last in twig.form_themes**

    Themes in twig.form_themes are applied in order; later entries override earlier ones on a block clash.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/form_themes.html)

??? question "17. At which form event is the CSRF token validated?"
    **✅ PRE_SUBMIT**

    CsrfValidationListener runs on PRE_SUBMIT: it pops the _token field from the raw submitted data and validates it, adding a form error on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/csrf.html)

??? question "18. What does the csrf_token_id option control?"
    **✅ The token intention/namespace used to generate and validate it**

    csrf_token_id is the intention string. csrf_field_name sets the HTML field name (default _token); csrf_protection toggles the feature.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/form.html)

??? question "19. Stateless CSRF (Symfony 7.2+/8) primarily removes the need for what?"
    **✅ A server-side session to store the token**

    With framework.csrf_protection.stateless_token_ids, the SameOriginCsrfTokenManager validates via a double-submit cookie plus origin checks, so no token is stored in the session.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/csrf.html)

??? question "20. How do you read the value of an unmapped FileType field?"
    **✅ $form->get('field')->getData()**

    mapped => false excludes the field from the data mapper, so it is not written to the model; you fetch it directly from the child form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

??? question "21. Which UploadedFile value is safe to trust for validating file type?"
    **✅ getMimeType()/guessExtension() (content-based)**

    Client-supplied name and MIME are spoofable. Content-based guessing (used by the File/Image constraints) is authoritative.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)

??? question "22. When does form_start emit enctype="multipart/form-data"?"
    **✅ When the form contains a file field**

    The form's multipart view variable is set when a child (e.g. FileType) requires it, and form_start renders the enctype accordingly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/file.html)

??? question "23. Which ChoiceType options render checkboxes?"
    **✅ expanded => true, multiple => true**

    expanded + multiple renders checkboxes; expanded + single renders radios; collapsed renders a select element.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/choice.html)

??? question "24. What does MoneyType's divisor option do?"
    **✅ Scales the model value (e.g. 100 lets you store integer cents)**

    The displayed amount is divided by divisor to form the model value, so 100 lets you store amounts in cents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/money.html)

??? question "25. For a mapped CollectionType to call the parent's adder/remover methods, set…"
    **✅ by_reference => false**

    by_reference => false forces the form to call add/remove methods instead of mutating the returned collection in place, keeping associations in sync.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/collection.html)

??? question "26. Which type is out of scope here because it belongs to the Doctrine bridge?"
    **✅ EntityType**

    EntityType lives in the Doctrine bridge and is out of scope. Use ChoiceType with explicit choices for the non-Doctrine equivalent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/choice.html)

??? question "27. In which direction does reverseTransform() run?"
    **✅ View to model (on submission)**

    transform() converts toward the view (display); reverseTransform() converts toward the model (submission). Reversing these is the classic trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "28. addModelTransformer() converts between which representations?"
    **✅ Model and normalized data**

    Model transformers bridge model<->norm; view transformers bridge norm<->view. Pick a model transformer when the underlying type changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "29. What should a transformer throw when input cannot be converted?"
    **✅ TransformationFailedException**

    TransformationFailedException is caught by the form and turned into a field-level invalid state showing the field's invalid_message, not a 500.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Form.php)

??? question "30. On submit, which transformers run first?"
    **✅ View transformers (view->norm), then model transformers (norm->model)**

    On submission data flows view -> norm -> model, so view transformers' reverseTransform runs before model transformers' reverseTransform.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

??? question "31. What is the correct order of the submit-phase form events?"
    **✅ PRE_SUBMIT -> SUBMIT -> POST_SUBMIT**

    Submission dispatches PRE_SUBMIT (raw view data), SUBMIT (normalized), then POST_SUBMIT (bound model), in that order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "32. What is the correct order of the set-data-phase form events?"
    **✅ PRE_SET_DATA -> POST_SET_DATA**

    Setting data (on create/populate) dispatches PRE_SET_DATA then POST_SET_DATA. There is no SET_DATA constant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "33. On PRE_SUBMIT, what does $event->getData() return?"
    **✅ The raw submitted view data (an array/string)**

    PRE_SUBMIT fires before transformation, so the data is the raw request values — not your object.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "34. To add a field based on the submitted value, which event do you listen on?"
    **✅ PRE_SUBMIT**

    Fields must be added before binding. PRE_SUBMIT exposes the raw submitted value while the form is still mutable (dynamic/dependent fields).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/dynamic_form_modification.html)

??? question "35. Which event does the validator form extension hook to run validation?"
    **✅ POST_SUBMIT**

    Validation runs after data is bound to the model, via a POST_SUBMIT listener. There is no PRE_VALIDATE/POST_VALIDATE in FormEvents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/events.html)

??? question "36. Which method declares the types a form type extension applies to?"
    **✅ public static function getExtendedTypes(): iterable**

    getExtendedTypes() is static and returns an iterable of type FQCNs. It replaced the removed singular getExtendedType().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_form_type_extension.html)

??? question "37. With autoconfiguration enabled, how is a type extension registered?"
    **✅ Automatically, via the form.type_extension tag on FormTypeExtensionInterface services**

    Symfony auto-tags implementers of FormTypeExtensionInterface with form.type_extension. There is no dedicated attribute for this in core.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_form_type_extension.html)

??? question "38. What is the effect of returning FormType::class from getExtendedTypes()?"
    **✅ The extension applies to every form type (all descend from FormType)**

    Because all types inherit from FormType, the extension attaches to every form — powerful for global concerns but risky to overuse.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_form_type_extension.html)

---

<small>Back to [Flashcards](index.md) · [Forms](../../forms/index.md)</small>

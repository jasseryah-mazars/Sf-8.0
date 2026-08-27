# Chapter Exam — Forms

!!! abstract "How to use"
    72 questions spanning every subchapter of **Forms**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Forms](../forms/index.md).

---

**Q1.** Which two methods do you typically override in an AbstractType?  <small>_(easy · single)_</small>

- A. buildForm(FormBuilderInterface, array) and configureOptions(OptionsResolver)
- B. build() and getOptions()
- C. getName() and buildView()
- D. configureFields() and setDefaults()

??? success "Answer Q1"
    **A**

    buildForm() adds fields to the builder; configureOptions() declares the type's options via OptionsResolver. getName() was removed; buildView() exists but is not the primary pair.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q2.** Where should field-adding logic live in a form type?  <small>_(easy · single)_</small>

- A. In buildForm(), using the FormBuilderInterface
- B. In configureOptions(), returning an array of fields
- C. In the constructor
- D. In buildView()

??? success "Answer Q2"
    **A**

    buildForm() receives the builder and is where ->add() calls belong. configureOptions() only declares options via OptionsResolver.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q3.** What is the canonical order of the controller form-handling calls?  <small>_(easy · single)_</small>

- A. handleRequest(), then isSubmitted() && isValid(), then getData()
- B. isValid(), then handleRequest()
- C. submit(), then handleRequest()
- D. createView(), then isSubmitted()

??? success "Answer Q3"
    **A**

    handleRequest() inspects the request and submits the form; only then are isSubmitted()/isValid() meaningful, after which getData() holds the model.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q4.** Why redirect after a successful POST (POST-redirect-GET)?  <small>_(easy · single)_</small>

- A. So a browser refresh re-fetches a GET instead of re-submitting the form
- B. Because forms cannot render on a POST response
- C. To trigger CSRF validation
- D. It is required for isValid() to return true

??? success "Answer Q4"
    **A**

    Without the redirect, refreshing re-POSTs the data and duplicates side effects. Redirecting lands the browser on a safe GET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q5.** What does form_row(form.email) render?  <small>_(easy · single)_</small>

- A. Label, widget, errors and help for that field
- B. Only the input element
- C. The whole form
- D. Just the label

??? success "Answer Q5"
    **A**

    form_row composes the label, widget, errors and help via the *_row theme block. form_widget renders only the control.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_customization.html)

**Q6.** How is the hidden CSRF token normally emitted into the HTML?  <small>_(easy · single)_</small>

- A. By form_rest, which form_end calls by default
- B. By form_start
- C. Only by hand-writing an <input name="_token">
- D. It is never rendered inside the form

??? success "Answer Q6"
    **A**

    The CSRF token is a hidden child rendered by form_rest; form_end triggers form_rest unless you pass render_rest: false.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/csrf.html)

**Q7.** Which call renders form-level (non-field) errors?  <small>_(easy · single)_</small>

- A. form_errors(form)
- B. form_errors(form.name)
- C. form_widget(form)
- D. form_help(form)

??? success "Answer Q7"
    **A**

    Passing the root form view to form_errors renders errors attached to the form itself; per-field errors use form_errors(form.field).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q8.** Which Twig call is wrong for rendering a single field's widget?  <small>_(easy · trap)_</small>

- A. form(form.email) — form() is for the whole form; use form_widget/form_row for a field
- B. form_widget(form.email)
- C. form_row(form.email)
- D. form_label(form.email)

??? success "Answer Q8"
    **A**

    form() renders an entire form (start, rows, end). For an individual field use form_row (label+widget+errors+help) or the granular form_widget/form_label/ form_errors/form_help. Calling form() on a child view is a common mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_customization.html)

**Q9.** What does the built-in bootstrap_5_layout.html.twig provide?  <small>_(easy · trap)_</small>

- A. Twig blocks producing Bootstrap-compatible markup (a theme only)
- B. Bootstrap CSS and JS assets
- C. A PHP form type
- D. CSRF protection

??? success "Answer Q9"
    **A**

    Built-in layouts are theme templates (markup only). You still load the CSS framework yourself; the Form component ships no assets.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/bootstrap5.html)

**Q10.** When two global form themes define the same block, which wins?  <small>_(easy · single)_</small>

- A. The theme listed last in twig.form_themes
- B. The first listed theme
- C. Twig throws an error
- D. Both render in sequence

??? success "Answer Q10"
    **A**

    Themes in twig.form_themes are applied in order; later entries override earlier ones on a block clash.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_themes.html)

**Q11.** What does the csrf_token_id option control?  <small>_(easy · single)_</small>

- A. The token intention/namespace used to generate and validate it
- B. The HTML name of the hidden field
- C. Whether CSRF protection is enabled
- D. The session cookie name

??? success "Answer Q11"
    **A**

    csrf_token_id is the intention string. csrf_field_name sets the HTML field name (default _token); csrf_protection toggles the feature.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/form.html)

**Q12.** Stateless CSRF (Symfony 7.2+/8) primarily removes the need for what?  <small>_(easy · single)_</small>

- A. A server-side session to store the token
- B. The hidden _token field
- C. HTTPS
- D. The Validator component

??? success "Answer Q12"
    **A**

    With framework.csrf_protection.stateless_token_ids, the SameOriginCsrfTokenManager validates via a double-submit cookie plus origin checks, so no token is stored in the session.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/csrf.html)

**Q13.** How do you read the value of an unmapped FileType field?  <small>_(easy · single)_</small>

- A. $form->get('field')->getData()
- B. From the bound model object
- C. $request->request->get('field')
- D. $form->getViewData()

??? success "Answer Q13"
    **A**

    mapped => false excludes the field from the data mapper, so it is not written to the model; you fetch it directly from the child form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

**Q14.** When does form_start emit enctype="multipart/form-data"?  <small>_(easy · single)_</small>

- A. When the form contains a file field
- B. Always
- C. Only if set manually
- D. Never — you must add it yourself

??? success "Answer Q14"
    **A**

    The form's multipart view variable is set when a child (e.g. FileType) requires it, and form_start renders the enctype accordingly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/file.html)

**Q15.** Which ChoiceType options render checkboxes?  <small>_(easy · single)_</small>

- A. expanded => true, multiple => true
- B. expanded => false, multiple => true
- C. expanded => true, multiple => false
- D. widget => 'checkbox'

??? success "Answer Q15"
    **A**

    expanded + multiple renders checkboxes; expanded + single renders radios; collapsed renders a select element.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/choice.html)

**Q16.** What does MoneyType's divisor option do?  <small>_(easy · single)_</small>

- A. Scales the model value (e.g. 100 lets you store integer cents)
- B. Sets the currency symbol
- C. Rounds to N decimals
- D. Limits the maximum amount

??? success "Answer Q16"
    **A**

    The displayed amount is divided by divisor to form the model value, so 100 lets you store amounts in cents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/money.html)

**Q17.** Which type is out of scope here because it belongs to the Doctrine bridge?  <small>_(easy · trap)_</small>

- A. EntityType
- B. ChoiceType
- C. MoneyType
- D. CollectionType

??? success "Answer Q17"
    **A**

    EntityType lives in the Doctrine bridge and is out of scope. Use ChoiceType with explicit choices for the non-Doctrine equivalent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/choice.html)

**Q18.** What is RepeatedType used for?  <small>_(easy · single)_</small>

- A. Rendering one inner type twice (e.g. password + confirmation) that only passes if both entries match
- B. Rendering a dynamic list of sub-forms you can add/remove
- C. Repeating a form submission N times server-side
- D. Rendering the same field for every locale

??? success "Answer Q18"
    **A**

    RepeatedType renders its inner type (via the type option) twice — configured with first_options/second_options — and validates only if both values match, ideal for password confirmation. The dynamic add/remove list is CollectionType, not RepeatedType.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/repeated.html)

**Q19.** What is the correct order of the submit-phase form events?  <small>_(easy · internals)_</small>

- A. PRE_SUBMIT -> SUBMIT -> POST_SUBMIT
- B. SUBMIT -> PRE_SUBMIT -> POST_SUBMIT
- C. PRE_SUBMIT -> POST_SUBMIT -> SUBMIT
- D. PRE_SET_DATA -> SUBMIT -> POST_SUBMIT

??? success "Answer Q19"
    **A**

    Submission dispatches PRE_SUBMIT (raw view data), SUBMIT (normalized), then POST_SUBMIT (bound model), in that order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/events.html)

**Q20.** What is the correct order of the set-data-phase form events?  <small>_(easy · internals)_</small>

- A. PRE_SET_DATA -> POST_SET_DATA
- B. POST_SET_DATA -> PRE_SET_DATA
- C. PRE_SET_DATA -> SUBMIT
- D. SET_DATA -> POST_SET_DATA

??? success "Answer Q20"
    **A**

    Setting data (on create/populate) dispatches PRE_SET_DATA then POST_SET_DATA. There is no SET_DATA constant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/events.html)

**Q21.** To add a field based on the submitted value, which event do you listen on?  <small>_(easy · single)_</small>

- A. PRE_SUBMIT
- B. POST_SUBMIT
- C. SUBMIT
- D. POST_SET_DATA

??? success "Answer Q21"
    **A**

    Fields must be added before binding. PRE_SUBMIT exposes the raw submitted value while the form is still mutable (dynamic/dependent fields).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/dynamic_form_modification.html)

**Q22.** Which of these is NOT a real FormEvents constant?  <small>_(easy · trap)_</small>

- A. FormEvents::PRE_VALIDATE
- B. FormEvents::PRE_SET_DATA
- C. FormEvents::PRE_SUBMIT
- D. FormEvents::POST_SUBMIT

??? success "Answer Q22"
    **A**

    There is no PRE_VALIDATE (nor POST_VALIDATE) in FormEvents. The five constants are PRE_SET_DATA, POST_SET_DATA, PRE_SUBMIT, SUBMIT and POST_SUBMIT; validation is simply a POST_SUBMIT listener registered by the validator extension.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/FormEvents.php)

**Q23.** Which method declares the types a form type extension applies to?  <small>_(easy · single)_</small>

- A. public static function getExtendedTypes(): iterable
- B. public function getExtendedType(): string
- C. public function configureOptions()
- D. public function getParent(): string

??? success "Answer Q23"
    **A**

    getExtendedTypes() is static and returns an iterable of type FQCNs. It replaced the removed singular getExtendedType().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_form_type_extension.html)

**Q24.** A compound form with no data_class set returns what from getData()?  <small>_(medium · single)_</small>

- A. An associative array keyed by child field name
- B. Always null
- C. A stdClass instance
- D. A FormInterface

??? success "Answer Q24"
    **A**

    Without data_class the data mapper maps children into and out of an array. Set data_class to bind the form to an object instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_class.html)

**Q25.** A developer writes `public function configureOptions(OptionsResolver $resolver): void { return ['data_class' => Contact::class]; }`. Why does the form type fail to compile / behave?  <small>_(medium · code)_</small>

- A. configureOptions() returns void; you must call $resolver->setDefaults([...]), not return an array
- B. data_class must be a string literal, never a ::class constant
- C. You must call parent::configureOptions() first or it throws
- D. Options can only be declared inside buildForm()

??? success "Answer Q25"
    **A**

    configureOptions() has a void return type and configures the injected OptionsResolver imperatively via setDefaults()/setRequired()/setAllowedTypes(). Returning an array does nothing. ::class constants are perfectly valid option values, and there is no requirement to call the parent (AbstractType's is empty).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_custom_field_type.html)

**Q26.** Inside buildForm(FormBuilderInterface $builder, array $options), can you read the user's submitted values (e.g. $builder->getData() as posted input)?  <small>_(medium · trap)_</small>

- A. No — buildForm() runs at build time on a FormBuilderInterface; the form is not submitted yet, so there is no request data to read
- B. Yes — $builder->getData() returns the POSTed values
- C. Yes — via $builder->getRequest()
- D. Only for PATCH submissions

??? success "Answer Q26"
    **A**

    buildForm() receives a FormBuilderInterface, not a submitted FormInterface. The form does not exist yet and handleRequest()/submit() have not run, so submitted input is unavailable. To react to submitted values, add a PRE_SUBMIT listener, which fires later with the raw view data. There is no $builder->getRequest().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q27.** What determines the Twig block name used to theme a custom form type?  <small>_(medium · single)_</small>

- A. getBlockPrefix() (defaults to the snake_cased class name without the Type suffix)
- B. getName(), which returns the block name
- C. The fully-qualified class name, lowercased
- D. The value passed as the field's second ->add() argument

??? success "Answer Q27"
    **A**

    getBlockPrefix() drives Twig block naming; it defaults to the snake-cased short class name minus the Type suffix. getName() was removed long ago — the FQCN is now the type identifier, but the FQCN is not used verbatim for block names.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_custom_field_type.html)

**Q28.** For a PATCH submission, handleRequest passes which clearMissing value?  <small>_(medium · trap)_</small>

- A. false, enabling partial updates (absent fields keep their value)
- B. true, clearing all absent fields
- C. It is undefined for PATCH
- D. It depends on data_class

??? success "Answer Q28"
    **A**

    handleRequest passes clearMissing: false for PATCH so fields missing from the payload retain their current value, enabling partial updates.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Form.php)

**Q29.** What happens if you call $form->isValid() on a form that was never submitted?  <small>_(medium · trap)_</small>

- A. It throws a LogicException ('Cannot check if an unsubmitted form is valid')
- B. It returns false silently
- C. It returns true because there are no errors yet
- D. It implicitly submits the form first

??? success "Answer Q29"
    **A**

    isValid() is only meaningful after submission, so calling it on an unsubmitted form throws a LogicException. Always guard with isSubmitted() first (isSubmitted() && isValid()). It does not auto-submit or silently return a value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q30.** A form posts to a controller and the browser gets a 405 Method Not Allowed on submit, though the page renders fine on GET. What is the most likely cause?  <small>_(medium · debug)_</small>

- A. The route restricts methods to GET (missing POST in methods: ['GET','POST'])
- B. handleRequest() was not called
- C. The CSRF token is missing
- D. data_class is not set on the form

??? success "Answer Q30"
    **A**

    A 405 comes from the router rejecting the HTTP method before the controller runs, so the route must allow POST as well as GET. A missing handleRequest() or CSRF token would let the request through and manifest as a form not submitting or an invalid-token error, not a 405; data_class is unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q31.** What does a form type's getParent() return?  <small>_(medium · trap)_</small>

- A. The parent type's fully-qualified class name (a string)
- B. A FormBuilderInterface instance
- C. A ResolvedFormType instance
- D. null for all custom types

??? success "Answer Q31"
    **A**

    getParent() returns a class string (default FormType::class). The registry resolves it into the parent chain of a ResolvedFormType.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_custom_field_type.html)

**Q32.** Which object bundles a type with its parent chain and applicable extensions?  <small>_(medium · internals)_</small>

- A. ResolvedFormType
- B. FormBuilder
- C. FormConfig
- D. OptionsResolver

??? success "Answer Q32"
    **A**

    FormRegistry produces a ResolvedFormType wrapping the type, its resolved parent, and every type extension that applies.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/ResolvedFormType.php)

**Q33.** In what order do configureOptions() run along the type hierarchy?  <small>_(medium · internals)_</small>

- A. Parent first, then child (child can override parent defaults)
- B. Child first, then parent
- C. Alphabetically by class name
- D. The order is undefined

??? success "Answer Q33"
    **A**

    The resolved type walks the chain top-down, so parent defaults are set before the child's, letting the child override them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q34.** A custom type does `public function getParent(): string { return new TextType(); }`. What is wrong?  <small>_(medium · code)_</small>

- A. getParent() must return a class-string (TextType::class), not an instance
- B. Nothing — Symfony instantiates the returned object as the parent
- C. It should return an array of parent FQCNs
- D. getParent() must be static

??? success "Answer Q34"
    **A**

    getParent() is declared to return string; returning an object violates the return type and the registry expects an FQCN to resolve. Use TextType::class. It is not static and returns a single string, not an array.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_custom_field_type.html)

**Q35.** A template renders each field manually and ends with `{{ form_end(form, {'render_rest': false}) }}`. Submissions now fail with an invalid CSRF token. Why?  <small>_(medium · debug)_</small>

- A. render_rest: false suppresses form_rest, so the hidden _token is never emitted; render form_rest(form) yourself
- B. form_end always drops the token; you must add it in form_start
- C. CSRF only works with form(form), never with manual layouts
- D. The token expired because manual rendering is slower

??? success "Answer Q35"
    **A**

    form_end normally calls form_rest, which renders un-rendered fields including the hidden CSRF token. Passing render_rest: false skips that, so the _token is absent and PRE_SUBMIT validation fails. Render form_rest(form) (or the token) manually. Manual layouts are fully CSRF-capable; the token has nothing to do with speed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q36.** Which twig.yaml block applies a Bootstrap theme app-wide, then lets your own file override its blocks?  <small>_(medium · config)_</small>

- A. twig: { form_themes: ['bootstrap_5_layout.html.twig', 'form/fields.html.twig'] }
- B. twig: { form_themes: ['form/fields.html.twig', 'bootstrap_5_layout.html.twig'] }
- C. twig: { theme: 'bootstrap_5_layout.html.twig' }
- D. framework: { form_theme: 'bootstrap_5_layout.html.twig' }

??? success "Answer Q36"
    **A**

    form_themes are applied in order and the last wins on conflicts, so your file must come after the Bootstrap layout to override its blocks. The key is twig.form_themes (a list), not twig.theme or a framework.* key.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_themes.html)

**Q37.** What is required to theme a form with {% form_theme form _self %}?  <small>_(medium · trap)_</small>

- A. The template must NOT {% extends %} another template
- B. You must also list the template in twig.form_themes
- C. The blocks must be defined in a macro
- D. _self only works for the CSRF field

??? success "Answer Q37"
    **A**

    _self references the current template's own blocks, which requires that the template does not extend another (extending re-scopes blocks). It works for any field's blocks, not just CSRF, and does not need a form_themes entry or macros.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_themes.html)

**Q38.** At which form event is the CSRF token validated?  <small>_(medium · internals)_</small>

- A. PRE_SUBMIT
- B. POST_SUBMIT
- C. SUBMIT
- D. PRE_SET_DATA

??? success "Answer Q38"
    **A**

    CsrfValidationListener runs on PRE_SUBMIT: it pops the _token field from the raw submitted data and validates it, adding a form error on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/csrf.html)

**Q39.** Which configuration enables stateless CSRF for the login and logout token ids?  <small>_(medium · config)_</small>

- A. framework: { csrf_protection: { stateless_token_ids: ['authenticate', 'logout'] } }
- B. framework: { csrf_protection: { stateless: true } }
- C. framework: { csrf_protection: { session: false } }
- D. security: { stateless_csrf: true }

??? success "Answer Q39"
    **A**

    Stateless CSRF is enabled per token id by listing them under framework.csrf_protection.stateless_token_ids; forms whose csrf_token_id is in that list use SameOriginCsrfTokenManager. There is no boolean stateless/session flag, and the key lives under framework, not security.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/csrf.html)

**Q40.** If csrf_token_id is not set explicitly on a form, what is its default value?  <small>_(medium · trap)_</small>

- A. The form's block prefix
- B. The literal string '_token'
- C. The application secret
- D. A random value regenerated every request

??? success "Answer Q40"
    **A**

    The default csrf_token_id is the form's block prefix; setting it explicitly makes the intention stable regardless of the class name. '_token' is the default csrf_field_name (the HTML name), not the id, and the token is not the app secret nor regenerated per request within a namespace.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/form.html)

**Q41.** Which UploadedFile value is safe to trust for validating file type?  <small>_(medium · trap)_</small>

- A. getMimeType()/guessExtension() (content-based)
- B. getClientOriginalName()
- C. getClientMimeType()
- D. The HTML accept attribute

??? success "Answer Q41"
    **A**

    Client-supplied name and MIME are spoofable. Content-based guessing (used by the File/Image constraints) is authoritative.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)

**Q42.** On an optional upload field, the controller calls $file->move(...) and occasionally crashes with a fatal error. What is the fix?  <small>_(medium · debug)_</small>

- A. Guard with `if ($file instanceof UploadedFile)` — getData() is null when no file was uploaded
- B. Set required => true so getData() is never null
- C. Call handleRequest() a second time to populate the file
- D. Use $request->files->get() instead of the form

??? success "Answer Q42"
    **A**

    An optional FileType returns null from getData() when nothing is uploaded, so calling move() on null is fatal. Check `$file instanceof UploadedFile` first. Forcing required doesn't fit an optional field, re-running handleRequest is wrong, and bypassing the form loses validation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

**Q43.** Is a FileType field with mapped => false still validated by its constraints?  <small>_(medium · trap)_</small>

- A. Yes — mapped => false only stops data-mapping; the field is still rendered, submitted and validated
- B. No — unmapped fields skip validation entirely
- C. Only if you also set required => true
- D. Only when constraints are on the model class, not the field

??? success "Answer Q43"
    **A**

    mapped => false only disconnects the field from the data mapper (it is not written to the model). The field is still part of the form: rendered, submitted, and validated via its constraints option — which is exactly why the pattern is safe for uploads and plain passwords.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

**Q44.** What is the recommended way to name an uploaded file before move()?  <small>_(medium · scenario)_</small>

- A. Slug the original basename, append uniqid(), and use guessExtension()
- B. Use getClientOriginalName() directly as the target path
- C. Use the raw $_FILES tmp_name
- D. Store the UploadedFile object on the entity and let Doctrine name it

??? success "Answer Q44"
    **A**

    Generate a safe name: slug the original filename, add uniqid() for uniqueness, and derive the extension from guessExtension() (content-based). Using the client name risks path traversal, the tmp_name is transient, and persisting the UploadedFile object (Doctrine is out of scope) is wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

**Q45.** For a DateType that renders one HTML5 date input and produces a \DateTimeImmutable model, which options do you set?  <small>_(medium · config)_</small>

- A. widget => 'single_text', input => 'datetime_immutable'
- B. widget => 'choice', input => 'string'
- C. widget => 'text', input => 'timestamp'
- D. widget => 'single_text', input => 'array'

??? success "Answer Q45"
    **A**

    widget controls rendering: single_text is one type=\"date\" input (best with HTML5); choice renders dropdowns and text renders three text fields. input picks the model type — datetime_immutable is the recommended value, whereas string, timestamp and array yield other model shapes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/date.html)

**Q46.** Which statements about PasswordType and button types are correct? (choose 2)  <small>_(medium · multiple)_</small>

- A. PasswordType is not re-rendered with its value by default (always_empty => true)
- B. SubmitType/ButtonType/ResetType are not part of the mapped form data
- C. PasswordType always re-renders the submitted value for convenience
- D. SubmitType values are written to the data_class object

??? success "Answer Q46"
    **A, B**

    PasswordType defaults to always_empty => true, so the field renders blank after submit for safety. Buttons (Submit/Button/Reset) are unmapped — they carry no data — though SubmitType lets you detect the clicked button via getClickedButton().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/password.html)

**Q47.** In which direction does reverseTransform() run?  <small>_(medium · trap)_</small>

- A. View to model (on submission)
- B. Model to view (on display)
- C. Norm to view only
- D. It never runs for view transformers

??? success "Answer Q47"
    **A**

    transform() converts toward the view (display); reverseTransform() converts toward the model (submission). Reversing these is the classic trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q48.** What should a transformer throw when input cannot be converted?  <small>_(medium · single)_</small>

- A. TransformationFailedException
- B. InvalidArgumentException
- C. ValidatorException
- D. Nothing — return null

??? success "Answer Q48"
    **A**

    TransformationFailedException is caught by the form and turned into a field-level invalid state showing the field's invalid_message, not a 500.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Form.php)

**Q49.** In a DataTransformer, what should transform(null) return when the model value is unset?  <small>_(medium · code)_</small>

- A. '' (an empty string the widget can display)
- B. null (let the widget decide)
- C. It must throw TransformationFailedException
- D. false

??? success "Answer Q49"
    **A**

    On display, transform(null) fires for an unset model value and should return '' so the input renders cleanly and later value comparisons hold; returning null can make the widget render oddly. Throwing is for genuinely unconvertible input on reverseTransform, not for a normal empty value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q50.** You need a field whose view is an id string but whose model is a domain object. Which transformer slot fits?  <small>_(medium · single)_</small>

- A. A model transformer (the underlying type changes: id string <-> object)
- B. A view transformer (only formatting changes)
- C. Either — the slot makes no difference
- D. A PRE_SET_DATA listener instead of any transformer

??? success "Answer Q50"
    **A**

    Use a model transformer when the type of the underlying object changes (id <-> rich object); it bridges model<->norm. A view transformer is for pure string formatting (norm<->view). The slot matters because it determines where in the pipeline the conversion runs and what the norm data looks like.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q51.** On PRE_SUBMIT, what does $event->getData() return?  <small>_(medium · trap)_</small>

- A. The raw submitted view data (an array/string)
- B. The fully transformed model object
- C. Normalized data
- D. A FormView

??? success "Answer Q51"
    **A**

    PRE_SUBMIT fires before transformation, so the data is the raw request values — not your object.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/events.html)

**Q52.** Which event does the validator form extension hook to run validation?  <small>_(medium · internals)_</small>

- A. POST_SUBMIT
- B. PRE_SUBMIT
- C. SUBMIT
- D. A dedicated POST_VALIDATE event

??? success "Answer Q52"
    **A**

    Validation runs after data is bound to the model, via a POST_SUBMIT listener. There is no PRE_VALIDATE/POST_VALIDATE in FormEvents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/events.html)

**Q53.** In a PRE_SUBMIT listener you read the submitted country. Which line is safe?  <small>_(medium · code)_</small>

- A. $country = $event->getData()['country'] ?? null;
- B. $country = $event->getData()->getCountry();
- C. $country = $event->getData()['country'];
- D. $country = $event->getForm()->getData()->country;

??? success "Answer Q53"
    **A**

    PRE_SUBMIT data is the raw request array, so a blank field is simply an absent key — read it with ?? null to avoid an undefined-key warning. Treating the data as an object (->getCountry()) is wrong: it is not transformed yet, and the model on the form is not yet populated from this submission.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/events.html)

**Q54.** How do you attach a reusable event subscriber to a form?  <small>_(medium · config)_</small>

- A. Implement EventSubscriberInterface (with getSubscribedEvents()) and call $builder->addEventSubscriber($subscriber)
- B. Implement FormEventSubscriberInterface and tag it form.subscriber
- C. Add a #[AsFormSubscriber] attribute to the class
- D. Register it under framework.form.subscribers in YAML

??? success "Answer Q54"
    **A**

    Form subscribers implement the EventDispatcher's EventSubscriberInterface (the Form component has no dedicated FormEventSubscriberInterface) declaring getSubscribedEvents(), and are added with $builder->addEventSubscriber(). There is no #[AsFormSubscriber] attribute or framework.form.subscribers config for this.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/events.html)

**Q55.** What is the effect of returning FormType::class from getExtendedTypes()?  <small>_(medium · trap)_</small>

- A. The extension applies to every form type (all descend from FormType)
- B. It disables the extension
- C. It applies only to the root form
- D. It throws an exception

??? success "Answer Q55"
    **A**

    Because all types inherit from FormType, the extension attaches to every form — powerful for global concerns but risky to overuse.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_form_type_extension.html)

**Q56.** Which attribute registers a form type extension in core Symfony?  <small>_(medium · trap)_</small>

- A. There is none — core has no #[AsFormTypeExtension]; registration is by interface + getExtendedTypes() (autoconfig) or a manual tag
- B. #[AsFormTypeExtension]
- C. #[AsFormExtension]
- D. #[FormTypeExtension]

??? success "Answer Q56"
    **A**

    Unlike #[AsEventListener] or #[AsCommand], form type extensions have no dedicated attribute in core. Autoconfiguration tags FormTypeExtensionInterface services with form.type_extension, and getExtendedTypes() tells the registry which types to attach them to; a manual form.type_extension tag with extended_type is the fallback when autoconfiguration is off.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_form_type_extension.html)

**Q57.** A type extension defines `public function getExtendedType(): string { return FileType::class; }` but never applies. What is wrong?  <small>_(medium · debug)_</small>

- A. The singular getExtendedType() was removed; you must implement the static getExtendedTypes(): iterable returning [FileType::class]
- B. FileType cannot be extended; only FormType can
- C. The method must be private
- D. You must also return the parent chain from getExtendedType()

??? success "Answer Q57"
    **A**

    Registration keys off the static getExtendedTypes(): iterable; the old singular getExtendedType() no longer exists, so the extension is never matched to a type. Any type (including FileType) can be extended, and the method is static/public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_form_type_extension.html)

**Q58.** When you call $this->createForm(RegistrationType::class, $data), which object resolves the type's parent chain and extensions before the builder tree is built?  <small>_(hard · internals)_</small>

- A. FormFactory::create() asks FormRegistry for a ResolvedFormType, which builds the FormBuilder and walks buildForm() parent→child
- B. The controller instantiates the FormInterface tree directly
- C. OptionsResolver builds the form tree from the declared defaults
- D. The DataMapper creates the child forms from data_class metadata

??? success "Answer Q58"
    **A**

    createForm() delegates to FormFactory::create(), which via FormRegistry obtains a ResolvedFormType wrapping the type, its resolved parent chain and applicable type extensions. The resolved type creates a FormBuilder and runs each buildForm() from parent to child; getForm() then produces the immutable FormInterface tree. OptionsResolver only resolves options; the DataMapper maps data at submit/view time.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/FormFactory.php)

**Q59.** Which service does FormInterface::handleRequest() delegate to under FrameworkBundle?  <small>_(hard · internals)_</small>

- A. HttpFoundationRequestHandler
- B. NativeRequestHandler
- C. FormFactory
- D. RequestStack

??? success "Answer Q59"
    **A**

    With HttpFoundation available, the form's request handler is HttpFoundationRequestHandler; NativeRequestHandler is the fallback when working with PHP superglobals directly.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Extension/HttpFoundation/HttpFoundationRequestHandler.php)

**Q60.** Which accessor returns each of a field's three data representations after submit?  <small>_(hard · internals)_</small>

- A. getData() = model, getNormData() = normalized, getViewData() = view
- B. getData() = view, getViewData() = model, getNormData() = raw
- C. getModelData(), getNormalizedData(), getRenderedData()
- D. All three return the same array

??? success "Answer Q60"
    **A**

    A field holds data in three shapes: model (your PHP value), normalized (transport-neutral canonical), and view (strings for HTML). They are read with getData()/getNormData()/getViewData() respectively; transformers convert between adjacent shapes. There are no getModelData()/getRenderedData() methods.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q61.** In configureOptions(), which OptionsResolver call derives one option's value from the values of others?  <small>_(hard · config)_</small>

- A. setNormalizer('opt', fn (Options $o, $value) => ...)
- B. setAllowedTypes('opt', 'string')
- C. setRequired('opt')
- D. setDefault('opt', fn () => ...) only

??? success "Answer Q61"
    **A**

    setNormalizer() receives the resolved Options plus the raw value, letting one option depend on others (e.g. force expanded when multiple is false). setAllowedTypes validates a type, setRequired marks an option mandatory, and a default closure cannot read sibling options the way a normalizer can.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/options_resolver.html)

**Q62.** How are custom form types made available by their FQCN and able to receive injected services?  <small>_(hard · internals)_</small>

- A. FrameworkBundle autoconfigures FormTypeInterface implementers with the form.type tag
- B. You must register each type manually in config/services.yaml with form.type
- C. Types are discovered by a #[AsFormType] attribute
- D. The FormFactory scans the Form/ directory at runtime

??? success "Answer Q62"
    **A**

    Service autoconfiguration tags any class implementing FormTypeInterface with form.type, so it is usable by FQCN and can autowire constructor dependencies. There is no #[AsFormType] attribute and no runtime directory scan; manual tagging is only needed when autoconfiguration is disabled.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_custom_field_type.html)

**Q63.** How do partial rendering (form_row on some fields) and form_rest avoid rendering the same field twice?  <small>_(hard · internals)_</small>

- A. Each FormView carries an isRendered() flag; form_row/form_widget set it, and form_rest skips already-rendered views
- B. form_rest re-renders everything and Twig de-duplicates the HTML
- C. The renderer diffs the output string to remove duplicates
- D. Fields can only be rendered once per request globally

??? success "Answer Q63"
    **A**

    Rendering operates on the FormView tree. Each view has an isRendered() flag set when form_row/form_widget renders it, so form_rest emits only the leftover (un-rendered) fields — including hidden and CSRF fields. There is no string diffing.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/FormExtension.php)

**Q64.** In which order does the renderer try candidate theme blocks?  <small>_(hard · internals)_</small>

- A. Most specific (unique field id) down to least specific (form_widget)
- B. Least specific to most specific
- C. Alphabetically
- D. Randomly per request

??? success "Answer Q64"
    **A**

    The block-prefix hierarchy is walked from the unique per-field name down to the root form_* block; the first existing block wins.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_themes.html)

**Q65.** A field with block prefix 'rating' (parent 'integer') ignores your integer_widget override, but rating_widget works. Why?  <small>_(hard · scenario)_</small>

- A. The renderer tries rating_widget before integer_widget; the more specific block exists and wins, so integer_widget is never reached
- B. integer_widget is a reserved block that cannot be overridden
- C. Parent-prefix blocks are ignored unless you set inherit_data
- D. You must clear the Twig cache for parent blocks to apply

??? success "Answer Q65"
    **A**

    Block-name resolution goes most-specific to least-specific along the block-prefix chain (rating → integer → form). Since rating_widget exists, it wins and the more generic integer_widget is never consulted. Override rating_widget (or remove it to fall through). inherit_data and caching are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_themes.html)

**Q66.** When a submission arrives with a missing or invalid _token, what does CsrfValidationListener do?  <small>_(hard · internals)_</small>

- A. It adds a form error (so isValid() returns false) — it does not throw an exception
- B. It throws an AccessDeniedException immediately
- C. It returns a 403 response before the controller runs
- D. It silently regenerates a fresh token and continues

??? success "Answer Q66"
    **A**

    On PRE_SUBMIT the listener pops _token from the raw data and validates it; a missing/invalid token results in a form error, so isValid() is false and you re-render with csrf_message. It does not throw or short-circuit with a 403 — that is the pattern for the manual isCsrfTokenValid() helper in a controller.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Extension/Csrf/Type/FormTypeCsrfExtension.php)

**Q67.** For a mapped CollectionType to call the parent's adder/remover methods, set…  <small>_(hard · trap)_</small>

- A. by_reference => false
- B. allow_add => false
- C. prototype => false
- D. mapped => false

??? success "Answer Q67"
    **A**

    by_reference => false forces the form to call add/remove methods instead of mutating the returned collection in place, keeping associations in sync.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/collection.html)

**Q68.** addModelTransformer() converts between which representations?  <small>_(hard · internals)_</small>

- A. Model and normalized data
- B. Normalized and view data
- C. View data and HTML
- D. Request and response

??? success "Answer Q68"
    **A**

    Model transformers bridge model<->norm; view transformers bridge norm<->view. Pick a model transformer when the underlying type changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q69.** On submit, which transformers run first?  <small>_(hard · internals)_</small>

- A. View transformers (view->norm), then model transformers (norm->model)
- B. Model transformers, then view transformers
- C. Only model transformers run on submit
- D. Order is undefined

??? success "Answer Q69"
    **A**

    On submission data flows view -> norm -> model, so view transformers' reverseTransform runs before model transformers' reverseTransform.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q70.** An optional text field with a custom transformer reports 'invalid' whenever it is left blank. What is the likely cause?  <small>_(hard · debug)_</small>

- A. reverseTransform('') runs the parser on an empty string and throws TransformationFailedException; guard for ''/null and return the empty model value first
- B. The field needs a NotBlank constraint removed
- C. transform() must return null for empty values
- D. Model transformers cannot handle optional fields

??? success "Answer Q70"
    **A**

    An empty submission arrives as '' (or null) at reverseTransform(); if you parse it instead of short-circuiting, you raise a spurious TransformationFailedException and the field is marked invalid. Guard the first line for emptiness and return the model's empty value (null/[]/0). This is a format-handling bug, not a validation constraint issue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q71.** With autoconfiguration enabled, how is a type extension registered?  <small>_(hard · internals)_</small>

- A. Automatically, via the form.type_extension tag on FormTypeExtensionInterface services
- B. With an #[AsFormTypeExtension] attribute
- C. By calling addTypeExtension() in a controller
- D. It cannot be autoconfigured

??? success "Answer Q71"
    **A**

    Symfony auto-tags implementers of FormTypeExtensionInterface with form.type_extension. There is no dedicated attribute for this in core.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_form_type_extension.html)

**Q72.** With autoconfiguration disabled, which services.yaml tag correctly registers an extension for FileType?  <small>_(hard · config)_</small>

- A. tags: [{ name: form.type_extension, extended_type: Symfony\Component\Form\Extension\Core\Type\FileType }]
- B. tags: [{ name: form.type_extension }]  # extended_type inferred
- C. tags: [{ name: form.type, extended_type: FileType }]
- D. tags: [{ name: form.extension, class: FileType }]

??? success "Answer Q72"
    **A**

    Without autoconfiguration you must both use the form.type_extension tag and supply the extended_type attribute (the FQCN of the extended type) — it is not inferred from getExtendedTypes() in the manual case. form.type is for form types, and form.extension is not a real tag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_form_type_extension.html)

---

<small>Back to [Chapter Exams](index.md) · [Forms](../forms/index.md)</small>

# Chapter Exam — Data Validation

!!! abstract "How to use"
    74 questions spanning every subchapter of **Data Validation**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Data Validation](../validation/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Cette page est une **banque de 74 questions type QCM** sur Data Validation, avec correction dépliable sous chaque question. Ce n'est pas un cours : c'est un entraînement, à faire après avoir lu le chapitre.

**Pourquoi ça existe ?** Lire un chapitre donne l'impression d'avoir compris, mais répondre à une question sous forme d'examen (sans relire ses notes) révèle les vraies lacunes — c'est ce que fera l'examen officiel.

**🏠 Analogie de la vraie vie :** C'est le **permis de conduire**. Le code de la route (le cours) explique les règles ; les séries de questions du permis blanc (cette page) vérifient que tu sais les appliquer sous forme de question piège, sans l'aide du livre.

**Symfony dans la vraie vie :** Cours du chapitre → code de la route appris / Question du QCM → question du permis blanc / Réponse dépliable → correction avec explication / Score obtenu → indicateur "prêt à passer l'examen ou pas".

**⚠️ Erreur fréquente :** Déplier la réponse avant d'avoir vraiment tranché son choix. Le cerveau retient beaucoup mieux une explication lue *après* s'être trompé (ou avoir hésité) que lue en passant, sans effort de rappel préalable.

**🧠 Comment le mémoriser :** *« Je réponds d'abord, je vérifie ensuite »* — jamais l'inverse. Note les questions ratées : ce sont exactement les pièges que l'examinateur pose aussi.

---

**Q1.** What does ValidatorInterface::validate() return when the value is invalid?  <small>_(easy · single)_</small>

- A. A ConstraintViolationListInterface containing the violations
- B. false
- C. It throws a ValidationFailedException
- D. An array of error message strings

??? success "Answer Q1"
    **A**

    validate() always returns a ConstraintViolationListInterface. It never returns a bool and never throws on failure; you inspect the result with count() and by iterating it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q2.** Which method validates a hypothetical value without changing the object?  <small>_(easy · single)_</small>

- A. validatePropertyValue($objectOrClass, $property, $value)
- B. validateProperty($object, $property)
- C. validate($object)
- D. startContext()

??? success "Answer Q2"
    **A**

    validatePropertyValue() takes an explicit value and validates it against the property's constraints without touching the object. validateProperty() uses the object's current value instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q3.** In framework.yaml, what is the default of framework.validation.enable_attributes?  <small>_(easy · config)_</small>

- A. true — #[Assert\...] attribute mapping is enabled by default
- B. false — you must enable it manually
- C. It does not exist; mapping is always on
- D. auto

??? success "Answer Q3"
    **A**

    enable_attributes defaults to true, and YAML/XML files under config/validator/ are also auto-loaded. All active loaders are merged for the same class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q4.** True or False: ValidatorInterface::validate() throws a ValidationFailedException when the object is invalid.  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q4"
    **A**

    validate() never throws on failure and never returns a bool — it returns a ConstraintViolationListInterface. ValidationFailedException is thrown by higher-level helpers (e.g. the MapRequestPayload resolver), not by validate() itself.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q5.** To apply constraints to every element of an indexed array, which constraint do you use?  <small>_(easy · single)_</small>

- A. All
- B. Collection
- C. Count
- D. Unique

??? success "Answer Q5"
    **A**

    All applies the given constraints to each element of a collection. Collection validates the keys of an associative array; they are not interchangeable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/All.html)

**Q6.** What does #[Assert\Length(max: 10)] count by default?  <small>_(easy · single)_</small>

- A. Characters (respecting the charset), not bytes
- B. Bytes
- C. Words
- D. Array elements

??? success "Answer Q6"
    **A**

    Length counts characters using its charset (UTF-8 by default) with min/max/charset/countUnit options. To constrain the number of elements in an array use Count instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Length.html)

**Q7.** How do you make GreaterThan compare against another property of the same object (e.g. endDate > startDate)?  <small>_(easy · single)_</small>

- A. Use the propertyPath option: #[Assert\GreaterThan(propertyPath: 'startDate')]
- B. Pass the other property as the first constructor argument
- C. It is impossible; you must use a Callback
- D. Use a compareField: 'startDate' option

??? success "Answer Q7"
    **A**

    All comparison constraints (GreaterThan, LessThan, EqualTo, IdenticalTo…) accept a propertyPath option to compare against another field of the same object instead of a fixed value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/GreaterThan.html)

**Q8.** True or False: #[Assert\IsTrue] considers the integer 1 and the string '1' as passing.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q8"
    **A**

    IsTrue passes for true, 1 and '1' (a loose truthy check); IsFalse likewise passes for false, 0 and '0'. Both are commonly placed on getters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/IsTrue.html)

**Q9.** What causes the validator to recurse into a nested object property?  <small>_(easy · single)_</small>

- A. #[Assert\Valid] on the property holding the nested object
- B. Nothing — it always recurses automatically
- C. Calling validateProperty() on the nested object
- D. A class-level Valid constraint on the parent

??? success "Answer Q9"
    **A**

    Valid marks a property for cascading; the ValidValidator tells the context to descend so the nested object's own constraints (and, for collections, each element's) are validated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Valid.html)

**Q10.** For class App\Entity\User with no group sequence, what is the {ClassName} group?  <small>_(easy · single)_</small>

- A. 'User' (the short class name), equivalent to 'Default' here
- B. 'App\Entity\User' (the FQCN)
- C. 'app_entity_user'
- D. There is no such group

??? success "Answer Q10"
    **A**

    The {ClassName} group uses the short class name. Every Default-group constraint is also in it, so with no sequence 'User' and 'Default' are equivalent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q11.** Which default group name does an unqualified constraint belong to?  <small>_(easy · trap)_</small>

- A. Default (capital D)
- B. default (lowercase)
- C. the fully qualified class name
- D. Base

??? success "Answer Q11"
    **A**

    The implicit group is 'Default' with a capital D; group names are case-sensitive, so 'default' would be a different (empty) group.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q12.** What must a class annotated with #[Assert\GroupSequenceProvider] provide?  <small>_(easy · single)_</small>

- A. An implementation of GroupSequenceProviderInterface::getGroupSequence()
- B. A static groupSequence() method
- C. It must extend the GroupSequence class
- D. A compiler pass registration

??? success "Answer Q12"
    **A**

    The provider attribute delegates to getGroupSequence() from GroupSequenceProviderInterface, evaluated on each validation so the sequence can depend on the object's state.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q13.** How does a callback validator register an error?  <small>_(easy · single)_</small>

- A. $context->buildViolation('...')->addViolation();
- B. return 'the error message';
- C. return false;
- D. throw new ValidationException('...');

??? success "Answer Q13"
    **A**

    Violations are built and committed through the execution context. The callback's return value is ignored.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Callback.html)

**Q14.** By default, which validator class validates the constraint App\Validator\Foo?  <small>_(easy · single)_</small>

- A. App\Validator\FooValidator (constraint name + 'Validator')
- B. FooConstraintValidator
- C. Any service implementing ConstraintValidatorInterface
- D. You must always override validatedBy()

??? success "Answer Q14"
    **A**

    Constraint::validatedBy() returns static::class.'Validator' by convention. Override it only when the validator service id differs from that name.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q15.** Which method returns the message with its {{ placeholders }} still unresolved?  <small>_(easy · single)_</small>

- A. getMessageTemplate()
- B. getMessage()
- C. getParameters()
- D. getCode()

??? success "Answer Q15"
    **A**

    getMessage() returns the interpolated message; getMessageTemplate() keeps the raw template with {{ x }} placeholders, and getParameters() holds the substitution map.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q16.** On the violation builder, which method attaches the error to a different property?  <small>_(easy · single)_</small>

- A. atPath('otherField')
- B. setPropertyPath('otherField')
- C. setInvalidValue('otherField')
- D. setCode('otherField')

??? success "Answer Q16"
    **A**

    atPath() relocates the violation to a path relative to the current node, commonly used in class-level constraints to blame a specific field.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q17.** What is $this->context->addViolation($message, $params) a shortcut for?  <small>_(easy · single)_</small>

- A. buildViolation($message, $params)->addViolation() — the common case with no extra setters
- B. Resetting the violation list
- C. Reading the existing violations
- D. Throwing a ValidationFailedException

??? success "Answer Q17"
    **A**

    The context's addViolation() is a convenience for the simple case; use buildViolation() when you need atPath/setCode/setInvalidValue before committing.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q18.** What is the purpose of the builder's setCode() value?  <small>_(easy · single)_</small>

- A. A stable machine-readable code for the violation, usable via findByCodes() and independent of translated text
- B. The HTTP status code returned to the client
- C. The translation domain
- D. The property path

??? success "Answer Q18"
    **A**

    setCode() attaches a stable code (often a constant) so application code can branch on it without depending on translated message text; the list's findByCodes() filters by it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q19.** Which constraint passes only when the value IS strictly null?  <small>_(easy · single)_</small>

- A. IsNull
- B. NotNull
- C. NotBlank
- D. Blank

??? success "Answer Q19"
    **A**

    IsNull requires the value to be exactly null (fails otherwise). It is the inverse of NotNull. Blank (its cousin) passes for null or ''.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/IsNull.html)

**Q20.** A constraint declared without any explicit 'groups' option belongs to which validation group?  <small>_(easy · single)_</small>

- A. The special 'Default' group
- B. No group at all, so it is never validated
- C. A group named after the property
- D. The 'Strict' group

??? success "Answer Q20"
    **A**

    Every constraint with no explicit groups is placed in the Default group, which is the group used when you call validate() without specifying groups.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q21.** How is #[Assert\...] attribute metadata turned into constraints at runtime?  <small>_(medium · internals)_</small>

- A. AttributeLoader builds ClassMetadata once, cached in a PSR-6 pool
- B. It is re-parsed by reflection on every validate() call
- C. It is compiled into the DI container and never changes
- D. It is read from a database mapping table

??? success "Answer Q21"
    **A**

    LazyLoadingMetadataFactory uses AttributeLoader to reflect over the class and build ClassMetadata, which is cached (validator.mapping.cache) so the reflection cost is paid once per class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q22.** Given:
```php
class Author { #[Assert\Email] public ?string $email = null; }
$violations = $validator->validate(new Author());
```
What is count($violations)?
  <small>_(medium · code)_</small>

- A. 0 — Email skips null, so the unset property produces no violation
- B. 1 — the email is required and missing
- C. 1 — null is not a valid email
- D. A TypeError is thrown

??? success "Answer Q22"
    **A**

    Most value constraints, Email included, skip null/empty and return no violation; only NotBlank/NotNull enforce presence. Stack NotBlank with Email when a missing value must be rejected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Email.html)

**Q23.** A developer writes `if ($validator->validate($dto)) { throw ...; }` and it throws even for valid objects. What is the cause?  <small>_(medium · debug)_</small>

- A. validate() returns a ConstraintViolationList object, which is always truthy; you must check count() > 0
- B. validate() returns true on success
- C. The DTO has a hidden constraint that always fails
- D. You must always pass groups explicitly

??? success "Answer Q23"
    **A**

    The returned list is a non-null object, so it is truthy even when empty. Test count($violations) > 0 (or iterate); treating the list itself as a boolean is the classic mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q24.** What does the #[MapRequestPayload] argument resolver do regarding validation?  <small>_(medium · scenario)_</small>

- A. It deserializes the request into the DTO and automatically validates it, producing a 422 on violations
- B. It only deserializes; you must call the validator yourself
- C. It validates but does not deserialize
- D. It requires a Form to be defined

??? success "Answer Q24"
    **A**

    The argument resolver maps the request into the typed DTO and runs the validator, returning a 422 automatically when there are violations. In a controller you rarely call the validator directly; Forms invoke it during handleRequest() too.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q25.** Which statement about NotBlank and NotNull is correct?  <small>_(medium · trap)_</small>

- A. NotBlank rejects an empty string; NotNull accepts an empty string
- B. They are aliases for the same check
- C. NotNull rejects an empty string; NotBlank accepts it
- D. Both reject the integer 0

??? success "Answer Q25"
    **A**

    NotBlank fails on '', [], and blank strings; NotNull only fails on a strict null, so '' and 0 pass NotNull. This is a classic exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/NotBlank.html)

**Q26.** A nested object's own constraints never run during validation. Why?  <small>_(medium · debug)_</small>

- A. The property is missing #[Assert\Valid] to cascade into it
- B. The validator cannot handle nested objects
- C. You must call validateProperty() for nested objects
- D. Nested objects need their own validator service

??? success "Answer Q26"
    **A**

    Cascading is opt-in: without #[Assert\\Valid] on the property, the validator does not descend into the related object, so its constraints are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Valid.html)

**Q27.** What does #[Assert\Email] report for an empty string value?  <small>_(medium · trap)_</small>

- A. No violation — empty and null values pass most constraints
- B. A violation, because '' is not a valid email
- C. A PHP TypeError
- D. It depends on the charset option

??? success "Answer Q27"
    **A**

    Like Url, Regex and most value constraints, Email skips empty/null values. Combine it with NotBlank when an empty value must be rejected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Email.html)

**Q28.** Which of these constraints return NO violation for a null value? (choose three)  <small>_(medium · multiple)_</small>

- A. Email
- B. Length
- C. Range
- D. NotNull
- E. NotBlank

??? success "Answer Q28"
    **A, B, C**

    Email, Length, Range (and virtually all value constraints) bail out on null/empty and add no violation. NotNull fails on null; NotBlank fails on null/''/[]. To require and validate a value, stack the presence check with the shape check.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q29.** What are the defaults for allowExtraFields and allowMissingFields in:
```php
#[Assert\Collection(fields: [ 'street' => new Assert\NotBlank() ])]
public array $address = [];
```
  <small>_(medium · config)_</small>

- A. Both default to false — extra keys and missing keys both cause violations
- B. Both default to true
- C. allowExtraFields true, allowMissingFields false
- D. They default to null and are ignored

??? success "Answer Q29"
    **A**

    allowExtraFields and allowMissingFields both default to false, so Collection rejects partial or extra arrays unless you opt in. Per-field Required/Optional wrappers control whether a specific key may be absent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Collection.html)

**Q30.** A rule must compare two properties of the same object. Which scope fits best?  <small>_(medium · single)_</small>

- A. Class scope (e.g. a Callback or Expression constraint)
- B. A property constraint on each of the two fields
- C. A getter constraint
- D. It cannot be expressed with the Validator component

??? success "Answer Q30"
    **A**

    Cross-field rules need access to the whole object, so they belong on a class-target constraint such as Callback or Expression.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Expression.html)

**Q31.** A constraint on the getter isActive() reports a violation under which property path?  <small>_(medium · trap)_</small>

- A. active
- B. isActive
- C. getActive
- D. isActive()

??? success "Answer Q31"
    **A**

    Getter constraints validate the return value of isX/getX/hasX and report under the property-ised name, so isActive() maps to 'active'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q32.** For a property holding a collection of Address OBJECTS, how do you validate each element's own constraints?  <small>_(medium · trap)_</small>

- A. Put #[Assert\Valid] on the property; it cascades into every element
- B. Use #[Assert\All([new Assert\Valid()])]
- C. Use #[Assert\Collection]
- D. Nothing is needed; object collections cascade automatically

??? success "Answer Q32"
    **A**

    For a collection of objects, a single #[Assert\\Valid] on the property cascades into each element. All([new Valid()]) is a redundant anti-pattern; All is for applying scalar constraints to elements.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Valid.html)

**Q33.** Given:
```php
class Order {
    #[Assert\Valid]
    /** @var list<OrderLine> */
    public array $lines = [];
}
```
lines[2] has an invalid price. What property path does the violation carry?
  <small>_(medium · code)_</small>

- A. lines[2].price
- B. price
- C. lines.price
- D. Order.lines.2.price

??? success "Answer Q33"
    **A**

    The ExecutionContext builds the property path from the traversed nodes; a cascaded collection element uses index notation, giving lines[2].price.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q34.** You call validate($obj, groups: ['edit']). Which constraints run?  <small>_(medium · single)_</small>

- A. Only constraints assigned to the 'edit' group
- B. The 'Default' group plus the 'edit' group
- C. All constraints, regardless of group
- D. Only the 'Default' group

??? success "Answer Q34"
    **A**

    Only the requested groups run. Passing a custom group does NOT implicitly include Default; list ['Default', 'edit'] if you need both.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q35.** In a Symfony form, how do you tell the validator to validate the bound object with the 'registration' group?  <small>_(medium · scenario)_</small>

- A. Set the form's 'validation_groups' option to ['registration']
- B. Pass the groups to $form->handleRequest()
- C. Call $validator->validate() manually in the controller
- D. Set 'groups' on the form type's constructor

??? success "Answer Q35"
    **A**

    Forms invoke the validator during handleRequest(); the validation_groups option selects which groups run (default ['Default']). It can also be a callback for dynamic group selection.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q36.** Given:
```php
class User {
    #[Assert\NotBlank] public string $email = '';                 // ''
    #[Assert\NotBlank(groups: ['registration'])] public ?string $password = null; // null
}
$validator->validate($user, groups: ['registration']);
```
How many violations are returned?
  <small>_(medium · code)_</small>

- A. 1 — only the 'registration' group runs, so only $password's NotBlank fires; $email's Default NotBlank is skipped
- B. 2 — both NotBlank constraints fire
- C. 0 — Default must be requested for any violation
- D. 1 — only $email fires

??? success "Answer Q36"
    **A**

    Passing a custom group does not include Default. Only registration-group constraints run, so $password fails but the blank $email (Default) is skipped. List ['Default','registration'] to get both.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q37.** You call validate($user, groups: ['Default', 'edit']). Which constraints run? (choose two)  <small>_(medium · multiple)_</small>

- A. Constraints in the Default group
- B. Constraints in the 'edit' group
- C. Constraints in every group defined on the class
- D. Only constraints in whichever group is listed first

??? success "Answer Q37"
    **A, B**

    Listing both groups runs both sets. A custom group never implies Default, which is exactly why you list Default explicitly when you also need it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q38.** When does a group sequence stop early?  <small>_(medium · single)_</small>

- A. After the first group in the sequence that produces any violation
- B. After the first individual constraint that fails
- C. Only after all groups have run
- D. It never stops early

??? success "Answer Q38"
    **A**

    Each group runs fully, but the sequence halts after the first group that yields a violation, so later (often more expensive) groups are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q39.** What does this YAML configure?
```yaml
App\Entity\Registration:
    group_sequence:
        - Registration
        - Strict
```
  <small>_(medium · config)_</small>

- A. A group sequence: validate the Registration (class-name) group first, then Strict, stopping at the first failing group
- B. Two independent validation runs whose violations are merged
- C. A GroupSequenceProvider
- D. It disables the Default group

??? success "Answer Q39"
    **A**

    group_sequence declares the ordered sequence used when validating Default. The class-name group (Registration) means the class's own Default constraints; Strict runs only if the first step passes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q40.** When is a #[Assert\GroupSequenceProvider] class's getGroupSequence() called?  <small>_(medium · internals)_</small>

- A. Each time the object is validated, so the sequence can depend on the object's state
- B. Once, then cached in ClassMetadata
- C. At container compile time
- D. Only when invoked from the console

??? success "Answer Q40"
    **A**

    The provider is evaluated per validation, letting the returned array or GroupSequence adapt to runtime state (e.g. premium vs free account).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q41.** What is the signature of an instance-method #[Assert\Callback]?  <small>_(medium · single)_</small>

- A. public function m(ExecutionContextInterface $context, mixed $payload): void
- B. public function m(mixed $value): bool
- C. public function m(ExecutionContextInterface $context): string
- D. public function m(object $object, mixed $payload): void

??? success "Answer Q41"
    **A**

    An instance callback receives the ExecutionContext and the optional payload and returns void; violations are added through the context. The static form additionally receives the object as the first argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Callback.html)

**Q42.** #[Assert\Callback] is which kind of constraint?  <small>_(medium · single)_</small>

- A. A class-level constraint; the callback reads the whole object
- B. A property constraint that receives the property value
- C. A getter-only constraint
- D. A collection constraint

??? success "Answer Q42"
    **A**

    Callback targets the class, so it does not receive a single property value; you read the object from $this or $context->getObject() and can report on any path with atPath().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Callback.html)

**Q43.** A static #[Assert\Callback] method (referenced via the callback: option) receives what as its first argument?  <small>_(medium · trap)_</small>

- A. The object being validated (then the ExecutionContext, then the payload)
- B. The ExecutionContext
- C. The property value
- D. The payload

??? success "Answer Q43"
    **A**

    The static form has no $this, so its signature is (object $object, ExecutionContextInterface $context, mixed $payload). The instance form is (context, payload).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Callback.html)

**Q44.** A callback compares $this->start >= $this->end and occasionally throws a TypeError in production. What is the most likely cause?  <small>_(medium · debug)_</small>

- A. One of the properties is null; callbacks run even when fields are unset, so you must guard against null first
- B. Callbacks cannot compare dates
- C. The callback is missing a return value
- D. The ExecutionContext is null

??? success "Answer Q44"
    **A**

    Callbacks always run regardless of field state, so nullable properties are the classic callback bug. Guard with null checks (or ?-> / ??) and let each field's own NotNull enforce presence.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Callback.html)

**Q45.** Given:
```php
#[Assert\Callback]
public function check(ExecutionContextInterface $context, mixed $payload): void {
    if ($this->percent > 50 && $this->stackable) {
        $context->buildViolation('Large discounts cannot stack.')
            ->atPath('stackable')
            ->addViolation();
    }
}
```
Where is the violation reported?
  <small>_(medium · code)_</small>

- A. On the 'stackable' property path
- B. On the class root
- C. On 'percent'
- D. Nowhere; the method returns void

??? success "Answer Q45"
    **A**

    atPath('stackable') relocates the violation to that field. The void return is normal — the error is committed by addViolation(), not by returning a value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Callback.html)

**Q46.** Where must #[Assert\Callback] be placed?  <small>_(medium · trap)_</small>

- A. On a method (or on the class via the callback: option) — never on a property
- B. On any property
- C. Only on a getter
- D. On the constructor

??? success "Answer Q46"
    **A**

    Callback is a class-level constraint attached to a method; placing it on a property is a mistake. Read the object via $this or $context->getObject().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Callback.html)

**Q47.** How do you make a custom constraint apply at class scope?  <small>_(medium · single)_</small>

- A. Override getTargets() to return Constraint::CLASS_CONSTRAINT
- B. Set only #[\Attribute(\Attribute::TARGET_CLASS)]
- C. Rename the class with a 'Class' suffix
- D. Register a compiler pass

??? success "Answer Q47"
    **A**

    The validator uses getTargets() (defaulting to PROPERTY_CONSTRAINT) to decide placement. Returning CLASS_CONSTRAINT makes the validator receive the whole object as $value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q48.** What is the recommended first step in ConstraintValidator::validate()?  <small>_(medium · single)_</small>

- A. Check $constraint instanceof YourConstraint and throw UnexpectedTypeException otherwise
- B. Add a violation unconditionally
- C. Call initialize() manually
- D. Read $this->context->getRoot()

??? success "Answer Q48"
    **A**

    Guarding the constraint type documents intent and fails fast if the validator is mis-wired. It is the documented convention in the Symfony examples.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q49.** What do the first two statements accomplish?
```php
public function validate(mixed $value, Constraint $constraint): void {
    if (!$constraint instanceof ContainsAlphanumeric) {
        throw new UnexpectedTypeException($constraint, ContainsAlphanumeric::class);
    }
    if (null === $value || '' === $value) { return; }
    // ...
}
```
  <small>_(medium · code)_</small>

- A. Guard the constraint type (fail fast if mis-wired) and skip null/empty so the rule composes with NotBlank
- B. They are optional boilerplate with no effect
- C. They register the violation
- D. They enable group sequences

??? success "Answer Q49"
    **A**

    The instanceof guard documents intent and throws UnexpectedTypeException if mis-wired; the null/empty early return keeps the constraint composable with presence checks like NotBlank.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q50.** What does IS_REPEATABLE enable here?
```php
#[\Attribute(\Attribute::TARGET_PROPERTY | \Attribute::IS_REPEATABLE)]
final class ContainsAlphanumeric extends Constraint { /* ... */ }
```
  <small>_(medium · config)_</small>

- A. The same constraint attribute can be applied more than once on the same property
- B. It makes the validator re-run until it passes
- C. It registers the constraint in every group
- D. It allows the constraint on both properties and classes

??? success "Answer Q50"
    **A**

    IS_REPEATABLE is a native PHP attribute flag allowing multiple instances on one target. Allowing both property and class placement instead needs TARGET_CLASS in the flags AND getTargets() returning both.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q51.** How does a ConstraintValidator obtain $this->context (the ExecutionContext)?  <small>_(medium · internals)_</small>

- A. The validator calls initialize($context) before validate(); ConstraintValidator stores it as $this->context
- B. It is passed as a third argument to validate()
- C. You must autowire ExecutionContextInterface
- D. It is a static property on ConstraintValidator

??? success "Answer Q51"
    **A**

    For each constraint the validator resolves its ConstraintValidator, calls initialize($context) (which sets $this->context on the base class) and then validate($value, $constraint).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q52.** When is a violation built with buildViolation() actually recorded?  <small>_(medium · trap)_</small>

- A. Only when addViolation() is called on the builder
- B. Immediately when buildViolation() is called
- C. When the validator method returns
- D. When setParameter() is called

??? success "Answer Q52"
    **A**

    buildViolation() returns a fluent builder; nothing is added to the list until addViolation() commits it. Forgetting it makes the validator pass silently.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q53.** Why use setParameter('{{ value }}', ...) instead of concatenating the value into the message string?  <small>_(medium · trap)_</small>

- A. Placeholders keep the message translatable; the {{ x }} template is interpolated later and preserved by getMessageTemplate()
- B. Concatenation is faster and preferred
- C. setParameter is required to commit the violation
- D. Messages cannot contain any variables otherwise

??? success "Answer Q53"
    **A**

    {{ }} placeholders filled by setParameter keep the raw template translatable and available via getMessageTemplate(); inlining values into the string breaks translation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q54.** Given:
```php
foreach ($violations as $v) {
    $errors[$v->getPropertyPath()][] = $v->getMessage();
}
```
What does $v->getMessage() return here?
  <small>_(medium · code)_</small>

- A. The fully interpolated message (placeholders resolved)
- B. The raw template with {{ }} placeholders
- C. The violation code
- D. The invalid value

??? success "Answer Q54"
    **A**

    getMessage() is interpolated; getMessageTemplate() keeps the raw {{ x }} template. getPropertyPath() returns the path (e.g. 'code').

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q55.** In #[Assert\GroupSequence(['A', 'B'])], if a constraint in group 'A' fails, group 'B' is…  <small>_(medium · single)_</small>

- A. Not validated — the sequence stops at the first group that produces a violation
- B. Still validated, and all violations are merged
- C. Validated only if 'A' had exactly one violation
- D. Validated in a separate pass afterwards

??? success "Answer Q55"
    **A**

    A GroupSequence validates groups in order and stops as soon as one group yields a violation, so later groups (and their expensive checks) never run.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q56.** You put #[Assert\Valid] on a property holding a Collection/array of Address objects. What happens on validate()?  <small>_(medium · single)_</small>

- A. Each element is traversed and its own constraints are validated (cascade)
- B. Only the first element is validated
- C. The collection count is validated but not the elements
- D. Nothing — Valid works only on single objects

??? success "Answer Q56"
    **A**

    Assert\Valid cascades into nested objects, and for a traversable/array it validates every element's constraints. Without it, nested objects are not validated at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Valid.html)

**Q57.** You call $validator->validate(null). What happens?  <small>_(hard · trap)_</small>

- A. You get back an empty ConstraintViolationListInterface — no error, no TypeError
- B. A TypeError, because null is not an object
- C. A ValidationFailedException is thrown
- D. It returns null

??? success "Answer Q57"
    **A**

    Passing null is legal: the value is wrapped in a node, no class metadata is found, and an empty violation list comes back. Validation is values against constraints, and a bare null carries none. The trap is that a null object silently passes when you expected a required value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q58.** A class has a #[Assert\NotBlank] attribute on $name, and a YAML mapping file adds Length to the same $name. Which constraints apply?  <small>_(hard · internals)_</small>

- A. Both — all enabled loaders are merged; attributes do not override YAML, the constraints accumulate
- B. Only the attribute; attributes take precedence
- C. Only the YAML; file mapping wins
- D. A MappingException is thrown for the conflict

??? success "Answer Q58"
    **A**

    LazyLoadingMetadataFactory merges every active loader's constraints for a class, so attribute and YAML constraints add up rather than one silently overriding the other.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q59.** You have an indexed array of email strings and place #[Assert\Collection([...])] on it. Why is that wrong?  <small>_(hard · trap)_</small>

- A. Collection validates the KEYS of an associative array; to validate every element of an indexed array use All
- B. Nothing is wrong; Collection validates each element
- C. Collection only works on objects
- D. You must also add Valid

??? success "Answer Q59"
    **A**

    Collection maps per-key constraints for associative arrays (with Required/Optional wrappers), whereas All applies constraints to every element of an indexed collection. They are not interchangeable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/All.html)

**Q60.** Given:
```php
#[Assert\When(
    expression: 'this.getType() === "premium"',
    constraints: [new Assert\NotBlank()],
)]
public ?string $vatNumber = null;
```
For a non-premium object with $vatNumber = null, what happens?
  <small>_(hard · code)_</small>

- A. No violation — the inner NotBlank runs only when the expression is true
- B. A violation, because NotBlank always runs
- C. A syntax error; When cannot wrap NotBlank
- D. The expression is ignored for null values

??? success "Answer Q60"
    **A**

    When applies its inner constraints only if the ExpressionLanguage expression evaluates to true. Here getType() is not 'premium', so NotBlank is skipped and null passes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/When.html)

**Q61.** #[Assert\Choice(choices: ['a','b','c'])] is placed on an array property $roles, and elements outside the list are NOT rejected. Why?  <small>_(hard · trap)_</small>

- A. Choice validates the whole value as one choice unless multiple: true is set
- B. Choice never works on arrays
- C. You must use All instead of Choice
- D. The choices array is malformed

??? success "Answer Q61"
    **A**

    Without multiple: true, Choice checks that the value itself is one of the allowed choices. Setting multiple: true validates each element of the array (with optional min/max counts).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Choice.html)

**Q62.** You place a property-target-only constraint at class scope. What happens?  <small>_(hard · trap)_</small>

- A. A ConstraintDefinitionException is thrown — its getTargets() does not allow CLASS_CONSTRAINT
- B. It silently validates the first property
- C. It validates every property
- D. Nothing happens; it is ignored

??? success "Answer Q62"
    **A**

    A class-scope constraint must target the class (getTargets() returns CLASS_CONSTRAINT). Placing a property-target constraint at class scope raises a ConstraintDefinitionException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q63.** When a #[Assert\Valid] property is cascaded, which validation group is used for the nested object?  <small>_(hard · internals)_</small>

- A. The current group being validated is passed down to the nested object
- B. Always the nested object's own Default group
- C. All groups defined on the nested object
- D. No group; cascading disables groups

??? success "Answer Q63"
    **A**

    Cascading passes the current group down. A custom group propagates as-is, so a nested object only validates its custom-group constraints if that group actually reaches it. Valid never changes groups.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q64.** For a class that defines a GroupSequence, validating the 'Default' group will…  <small>_(hard · internals)_</small>

- A. Trigger the group sequence (stepwise, stop on first failing group)
- B. Run every constraint flat, ignoring the sequence
- C. Run no constraints at all
- D. Throw an exception

??? success "Answer Q64"
    **A**

    On a sequenced class, the special Default group is remapped to the sequence. To run the same constraints flat (bypassing the sequence), validate the {ClassName} group instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q65.** A parent cascades into a child with #[Assert\Valid] and validate() is called with the Default group. The child has a constraint only in a custom 'strict' group. Does it run?  <small>_(hard · trap)_</small>

- A. No — only the Default group reaches the child, so its 'strict'-only constraint is skipped
- B. Yes — Valid runs all of the child's groups
- C. Yes — custom groups always run on cascade
- D. Only if the child defines a group sequence

??? success "Answer Q65"
    **A**

    The cascaded group is the current one (Default). A child's custom-group constraint runs only if that custom group actually propagates to it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q66.** Inside a class's #[Assert\GroupSequence], how do you reference the class's own basic constraints?  <small>_(hard · trap)_</small>

- A. Use the short class-name group (e.g. 'User')
- B. Use 'Default'
- C. Use 'self'
- D. Use 'Basic'

??? success "Answer Q66"
    **A**

    Referencing 'Default' inside its own sequence would loop, because Default is remapped to the sequence. Use the {ClassName} group to mean the class's Default-group constraints run flat.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q67.** A class defines #[Assert\GroupSequence(['User','Strong'])]. You call validate($user, groups: ['User']). What runs?  <small>_(hard · trap)_</small>

- A. The class's Default-group constraints flat, WITHOUT the sequence (bypassing stop-on-first-fail)
- B. The full sequence, stopping on the first failing group
- C. Nothing, because 'User' is remapped to the sequence
- D. Only the 'Strong' group

??? success "Answer Q67"
    **A**

    Validating the {ClassName} group ('User') runs the class's Default constraints flat, bypassing the sequence. Only validating 'Default' triggers the sequence.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q68.** Given:
```php
#[Assert\GroupSequence(['Login', 'Strict'])]
class Login {
    #[Assert\NotBlank] public string $email = '';    // ''
    #[Assert\NotBlank] public string $password = '';  // ''
    #[Assert\Email(groups: ['Strict'])] public string $email2 = 'bad';
}
$validator->validate($login); // Default
```
Which violations are returned?
  <small>_(hard · code)_</small>

- A. Only the two NotBlank violations from step 1 (Login); the Strict Email check never runs
- B. All three violations
- C. Only the Email violation
- D. None; the sequence stops immediately

??? success "Answer Q68"
    **A**

    Step 1 is 'Login' (the class's Default constraints). Both NotBlank checks fail, so the sequence halts before the 'Strict' step and the Email check on $email2 is skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q69.** A #[Assert\Callback(groups: ['checkout'])] never fires during a plain validate($obj). Why, and does it join sequences?  <small>_(hard · internals)_</small>

- A. It runs only when the 'checkout' group is validated; being class-scoped, it also participates in group sequences like any constraint
- B. Callbacks ignore groups; the attribute is malformed
- C. Callbacks can never run inside groups
- D. It runs only in the Default group regardless of the option

??? success "Answer Q69"
    **A**

    Callback honours its groups option (default Default). A non-Default callback runs only when that group is validated, and it participates in group sequences exactly like any other constraint.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Callback.html)

**Q70.** What does #[HasNamedArguments] do on a custom Constraint constructor?  <small>_(hard · internals)_</small>

- A. Passes attribute arguments as named constructor arguments (typed options)
- B. Marks the constraint as repeatable
- C. Automatically registers the validator service
- D. Enables group sequences for the constraint

??? success "Answer Q70"
    **A**

    #[HasNamedArguments] (Symfony\\Component\\Validator\\Attribute) opts into typed, named-argument construction instead of the legacy options-array style; remember to forward $groups and $payload to parent::__construct().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q71.** How is a ConstraintValidator subclass wired so you can inject dependencies (e.g. a repository) into it?  <small>_(hard · internals)_</small>

- A. It is autoconfigured as a service tagged validator.constraint_validator (via ConstraintValidatorInterface), so normal autowiring applies
- B. You must register it manually in services.yaml with a factory
- C. Validators cannot have dependencies
- D. You register a compiler pass for each validator

??? success "Answer Q71"
    **A**

    Implementing ConstraintValidatorInterface (via ConstraintValidator) triggers autoconfiguration with the validator.constraint_validator tag, so validators are services and can have dependencies autowired.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q72.** In a custom Constraint with #[HasNamedArguments], why forward $groups and $payload to parent::__construct()?  <small>_(hard · trap)_</small>

- A. Otherwise the constraint ignores its groups/payload, so group assignment silently stops working
- B. It is optional decoration with no effect
- C. It registers the validator service
- D. It makes the constraint repeatable

??? success "Answer Q72"
    **A**

    The base Constraint stores groups and payload. Forgetting to forward them means the constraint always lands in Default and the payload is lost.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q73.** A developer uses $violations[0] (works) but array_map(..., $violations) (fails). Why?  <small>_(hard · trap)_</small>

- A. The list is a Countable/IteratorAggregate/ArrayAccess object, not a plain array; use foreach/count() or iterator_to_array()
- B. The list is null when empty
- C. array_map only works on associative arrays
- D. Violations are stored as strings

??? success "Answer Q73"
    **A**

    ConstraintViolationList implements ArrayAccess (so [0] works) but is not an array. Iterate it, call count(), use findByCodes(), or convert via iterator_to_array() for array functions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q74.** To make a single custom constraint usable on BOTH a property and a class, getTargets() should return…  <small>_(hard · single)_</small>

- A. [self::PROPERTY_CONSTRAINT, self::CLASS_CONSTRAINT]
- B. self::ALL_CONSTRAINTS
- C. self::PROPERTY_CONSTRAINT only
- D. an empty array to allow any target

??? success "Answer Q74"
    **A**

    getTargets() may return a single string or an array of them. Returning both PROPERTY_CONSTRAINT and CLASS_CONSTRAINT lets the same constraint be placed on a property and on a class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

---

<small>Back to [Chapter Exams](index.md) · [Data Validation](../validation/index.md)</small>

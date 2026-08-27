# Flashcards — Data Validation

74 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

??? question "1. What does ValidatorInterface::validate() return when the value is invalid?"
    **✅ A ConstraintViolationListInterface containing the violations**

    validate() always returns a ConstraintViolationListInterface. It never returns a bool and never throws on failure; you inspect the result with count() and by iterating it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "2. Which method validates a hypothetical value without changing the object?"
    **✅ validatePropertyValue($objectOrClass, $property, $value)**

    validatePropertyValue() takes an explicit value and validates it against the property's constraints without touching the object. validateProperty() uses the object's current value instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "3. How is #[Assert\...] attribute metadata turned into constraints at runtime?"
    **✅ AttributeLoader builds ClassMetadata once, cached in a PSR-6 pool**

    LazyLoadingMetadataFactory uses AttributeLoader to reflect over the class and build ClassMetadata, which is cached (validator.mapping.cache) so the reflection cost is paid once per class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "4. You call $validator->validate(null). What happens?"
    **✅ You get back an empty ConstraintViolationListInterface — no error, no TypeError**

    Passing null is legal: the value is wrapped in a node, no class metadata is found, and an empty violation list comes back. Validation is values against constraints, and a bare null carries none. The trap is that a null object silently passes when you expected a required value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "5. Given:
```php
class Author { #[Assert\Email] public ?string $email = null; }
$violations = $validator->validate(new Author());
```
What is count($violations)?
"
    **✅ 0 — Email skips null, so the unset property produces no violation**

    Most value constraints, Email included, skip null/empty and return no violation; only NotBlank/NotNull enforce presence. Stack NotBlank with Email when a missing value must be rejected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Email.html)

??? question "6. A developer writes `if ($validator->validate($dto)) { throw ...; }` and it throws even for valid objects. What is the cause?"
    **✅ validate() returns a ConstraintViolationList object, which is always truthy; you must check count() > 0**

    The returned list is a non-null object, so it is truthy even when empty. Test count($violations) > 0 (or iterate); treating the list itself as a boolean is the classic mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "7. In framework.yaml, what is the default of framework.validation.enable_attributes?"
    **✅ true — #[Assert\...] attribute mapping is enabled by default**

    enable_attributes defaults to true, and YAML/XML files under config/validator/ are also auto-loaded. All active loaders are merged for the same class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "8. A class has a #[Assert\NotBlank] attribute on $name, and a YAML mapping file adds Length to the same $name. Which constraints apply?"
    **✅ Both — all enabled loaders are merged; attributes do not override YAML, the constraints accumulate**

    LazyLoadingMetadataFactory merges every active loader's constraints for a class, so attribute and YAML constraints add up rather than one silently overriding the other.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "9. True or False: ValidatorInterface::validate() throws a ValidationFailedException when the object is invalid."
    **✅ False**

    validate() never throws on failure and never returns a bool — it returns a ConstraintViolationListInterface. ValidationFailedException is thrown by higher-level helpers (e.g. the MapRequestPayload resolver), not by validate() itself.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "10. What does the #[MapRequestPayload] argument resolver do regarding validation?"
    **✅ It deserializes the request into the DTO and automatically validates it, producing a 422 on violations**

    The argument resolver maps the request into the typed DTO and runs the validator, returning a 422 automatically when there are violations. In a controller you rarely call the validator directly; Forms invoke it during handleRequest() too.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "11. Which statement about NotBlank and NotNull is correct?"
    **✅ NotBlank rejects an empty string; NotNull accepts an empty string**

    NotBlank fails on '', [], and blank strings; NotNull only fails on a strict null, so '' and 0 pass NotNull. This is a classic exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/NotBlank.html)

??? question "12. To apply constraints to every element of an indexed array, which constraint do you use?"
    **✅ All**

    All applies the given constraints to each element of a collection. Collection validates the keys of an associative array; they are not interchangeable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/All.html)

??? question "13. A nested object's own constraints never run during validation. Why?"
    **✅ The property is missing #[Assert\Valid] to cascade into it**

    Cascading is opt-in: without #[Assert\\Valid] on the property, the validator does not descend into the related object, so its constraints are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Valid.html)

??? question "14. What does #[Assert\Email] report for an empty string value?"
    **✅ No violation — empty and null values pass most constraints**

    Like Url, Regex and most value constraints, Email skips empty/null values. Combine it with NotBlank when an empty value must be rejected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Email.html)

??? question "15. What does #[Assert\Length(max: 10)] count by default?"
    **✅ Characters (respecting the charset), not bytes**

    Length counts characters using its charset (UTF-8 by default) with min/max/charset/countUnit options. To constrain the number of elements in an array use Count instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Length.html)

??? question "16. How do you make GreaterThan compare against another property of the same object (e.g. endDate > startDate)?"
    **✅ Use the propertyPath option: #[Assert\GreaterThan(propertyPath: 'startDate')]**

    All comparison constraints (GreaterThan, LessThan, EqualTo, IdenticalTo…) accept a propertyPath option to compare against another field of the same object instead of a fixed value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/GreaterThan.html)

??? question "17. You have an indexed array of email strings and place #[Assert\Collection([...])] on it. Why is that wrong?"
    **✅ Collection validates the KEYS of an associative array; to validate every element of an indexed array use All**

    Collection maps per-key constraints for associative arrays (with Required/Optional wrappers), whereas All applies constraints to every element of an indexed collection. They are not interchangeable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/All.html)

??? question "18. Given:
```php
#[Assert\When(
    expression: 'this.getType() === "premium"',
    constraints: [new Assert\NotBlank()],
)]
public ?string $vatNumber = null;
```
For a non-premium object with $vatNumber = null, what happens?
"
    **✅ No violation — the inner NotBlank runs only when the expression is true**

    When applies its inner constraints only if the ExpressionLanguage expression evaluates to true. Here getType() is not 'premium', so NotBlank is skipped and null passes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/When.html)

??? question "19. #[Assert\Choice(choices: ['a','b','c'])] is placed on an array property $roles, and elements outside the list are NOT rejected. Why?"
    **✅ Choice validates the whole value as one choice unless multiple: true is set**

    Without multiple: true, Choice checks that the value itself is one of the allowed choices. Setting multiple: true validates each element of the array (with optional min/max counts).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Choice.html)

??? question "20. Which of these constraints return NO violation for a null value? (choose three)"
    **✅ Email ; Length ; Range**

    Email, Length, Range (and virtually all value constraints) bail out on null/empty and add no violation. NotNull fails on null; NotBlank fails on null/''/[]. To require and validate a value, stack the presence check with the shape check.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "21. What are the defaults for allowExtraFields and allowMissingFields in:
```php
#[Assert\Collection(fields: [ 'street' => new Assert\NotBlank() ])]
public array $address = [];
```
"
    **✅ Both default to false — extra keys and missing keys both cause violations**

    allowExtraFields and allowMissingFields both default to false, so Collection rejects partial or extra arrays unless you opt in. Per-field Required/Optional wrappers control whether a specific key may be absent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Collection.html)

??? question "22. True or False: #[Assert\IsTrue] considers the integer 1 and the string '1' as passing."
    **✅ True**

    IsTrue passes for true, 1 and '1' (a loose truthy check); IsFalse likewise passes for false, 0 and '0'. Both are commonly placed on getters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/IsTrue.html)

??? question "23. What causes the validator to recurse into a nested object property?"
    **✅ #[Assert\Valid] on the property holding the nested object**

    Valid marks a property for cascading; the ValidValidator tells the context to descend so the nested object's own constraints (and, for collections, each element's) are validated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Valid.html)

??? question "24. A rule must compare two properties of the same object. Which scope fits best?"
    **✅ Class scope (e.g. a Callback or Expression constraint)**

    Cross-field rules need access to the whole object, so they belong on a class-target constraint such as Callback or Expression.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Expression.html)

??? question "25. A constraint on the getter isActive() reports a violation under which property path?"
    **✅ active**

    Getter constraints validate the return value of isX/getX/hasX and report under the property-ised name, so isActive() maps to 'active'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "26. You place a property-target-only constraint at class scope. What happens?"
    **✅ A ConstraintDefinitionException is thrown — its getTargets() does not allow CLASS_CONSTRAINT**

    A class-scope constraint must target the class (getTargets() returns CLASS_CONSTRAINT). Placing a property-target constraint at class scope raises a ConstraintDefinitionException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "27. When a #[Assert\Valid] property is cascaded, which validation group is used for the nested object?"
    **✅ The current group being validated is passed down to the nested object**

    Cascading passes the current group down. A custom group propagates as-is, so a nested object only validates its custom-group constraints if that group actually reaches it. Valid never changes groups.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "28. For a property holding a collection of Address OBJECTS, how do you validate each element's own constraints?"
    **✅ Put #[Assert\Valid] on the property; it cascades into every element**

    For a collection of objects, a single #[Assert\\Valid] on the property cascades into each element. All([new Valid()]) is a redundant anti-pattern; All is for applying scalar constraints to elements.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Valid.html)

??? question "29. Given:
```php
class Order {
    #[Assert\Valid]
    /** @var list<OrderLine> */
    public array $lines = [];
}
```
lines[2] has an invalid price. What property path does the violation carry?
"
    **✅ lines[2].price**

    The ExecutionContext builds the property path from the traversed nodes; a cascaded collection element uses index notation, giving lines[2].price.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "30. You call validate($obj, groups: ['edit']). Which constraints run?"
    **✅ Only constraints assigned to the 'edit' group**

    Only the requested groups run. Passing a custom group does NOT implicitly include Default; list ['Default', 'edit'] if you need both.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "31. For a class that defines a GroupSequence, validating the 'Default' group will…"
    **✅ Trigger the group sequence (stepwise, stop on first failing group)**

    On a sequenced class, the special Default group is remapped to the sequence. To run the same constraints flat (bypassing the sequence), validate the {ClassName} group instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "32. For class App\Entity\User with no group sequence, what is the {ClassName} group?"
    **✅ 'User' (the short class name), equivalent to 'Default' here**

    The {ClassName} group uses the short class name. Every Default-group constraint is also in it, so with no sequence 'User' and 'Default' are equivalent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "33. Which default group name does an unqualified constraint belong to?"
    **✅ Default (capital D)**

    The implicit group is 'Default' with a capital D; group names are case-sensitive, so 'default' would be a different (empty) group.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "34. In a Symfony form, how do you tell the validator to validate the bound object with the 'registration' group?"
    **✅ Set the form's 'validation_groups' option to ['registration']**

    Forms invoke the validator during handleRequest(); the validation_groups option selects which groups run (default ['Default']). It can also be a callback for dynamic group selection.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

??? question "35. Given:
```php
class User {
    #[Assert\NotBlank] public string $email = '';                 // ''
    #[Assert\NotBlank(groups: ['registration'])] public ?string $password = null; // null
}
$validator->validate($user, groups: ['registration']);
```
How many violations are returned?
"
    **✅ 1 — only the 'registration' group runs, so only $password's NotBlank fires; $email's Default NotBlank is skipped**

    Passing a custom group does not include Default. Only registration-group constraints run, so $password fails but the blank $email (Default) is skipped. List ['Default','registration'] to get both.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "36. A parent cascades into a child with #[Assert\Valid] and validate() is called with the Default group. The child has a constraint only in a custom 'strict' group. Does it run?"
    **✅ No — only the Default group reaches the child, so its 'strict'-only constraint is skipped**

    The cascaded group is the current one (Default). A child's custom-group constraint runs only if that custom group actually propagates to it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "37. You call validate($user, groups: ['Default', 'edit']). Which constraints run? (choose two)"
    **✅ Constraints in the Default group ; Constraints in the 'edit' group**

    Listing both groups runs both sets. A custom group never implies Default, which is exactly why you list Default explicitly when you also need it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "38. When does a group sequence stop early?"
    **✅ After the first group in the sequence that produces any violation**

    Each group runs fully, but the sequence halts after the first group that yields a violation, so later (often more expensive) groups are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "39. Inside a class's #[Assert\GroupSequence], how do you reference the class's own basic constraints?"
    **✅ Use the short class-name group (e.g. 'User')**

    Referencing 'Default' inside its own sequence would loop, because Default is remapped to the sequence. Use the {ClassName} group to mean the class's Default-group constraints run flat.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "40. What must a class annotated with #[Assert\GroupSequenceProvider] provide?"
    **✅ An implementation of GroupSequenceProviderInterface::getGroupSequence()**

    The provider attribute delegates to getGroupSequence() from GroupSequenceProviderInterface, evaluated on each validation so the sequence can depend on the object's state.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "41. A class defines #[Assert\GroupSequence(['User','Strong'])]. You call validate($user, groups: ['User']). What runs?"
    **✅ The class's Default-group constraints flat, WITHOUT the sequence (bypassing stop-on-first-fail)**

    Validating the {ClassName} group ('User') runs the class's Default constraints flat, bypassing the sequence. Only validating 'Default' triggers the sequence.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "42. What does this YAML configure?
```yaml
App\Entity\Registration:
    group_sequence:
        - Registration
        - Strict
```
"
    **✅ A group sequence: validate the Registration (class-name) group first, then Strict, stopping at the first failing group**

    group_sequence declares the ordered sequence used when validating Default. The class-name group (Registration) means the class's own Default constraints; Strict runs only if the first step passes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "43. When is a #[Assert\GroupSequenceProvider] class's getGroupSequence() called?"
    **✅ Each time the object is validated, so the sequence can depend on the object's state**

    The provider is evaluated per validation, letting the returned array or GroupSequence adapt to runtime state (e.g. premium vs free account).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "44. Given:
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
"
    **✅ Only the two NotBlank violations from step 1 (Login); the Strict Email check never runs**

    Step 1 is 'Login' (the class's Default constraints). Both NotBlank checks fail, so the sequence halts before the 'Strict' step and the Email check on $email2 is skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "45. What is the signature of an instance-method #[Assert\Callback]?"
    **✅ public function m(ExecutionContextInterface $context, mixed $payload): void**

    An instance callback receives the ExecutionContext and the optional payload and returns void; violations are added through the context. The static form additionally receives the object as the first argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "46. How does a callback validator register an error?"
    **✅ $context->buildViolation('...')->addViolation();**

    Violations are built and committed through the execution context. The callback's return value is ignored.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "47. #[Assert\Callback] is which kind of constraint?"
    **✅ A class-level constraint; the callback reads the whole object**

    Callback targets the class, so it does not receive a single property value; you read the object from $this or $context->getObject() and can report on any path with atPath().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "48. A static #[Assert\Callback] method (referenced via the callback: option) receives what as its first argument?"
    **✅ The object being validated (then the ExecutionContext, then the payload)**

    The static form has no $this, so its signature is (object $object, ExecutionContextInterface $context, mixed $payload). The instance form is (context, payload).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "49. A callback compares $this->start >= $this->end and occasionally throws a TypeError in production. What is the most likely cause?"
    **✅ One of the properties is null; callbacks run even when fields are unset, so you must guard against null first**

    Callbacks always run regardless of field state, so nullable properties are the classic callback bug. Guard with null checks (or ?-> / ??) and let each field's own NotNull enforce presence.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "50. A #[Assert\Callback(groups: ['checkout'])] never fires during a plain validate($obj). Why, and does it join sequences?"
    **✅ It runs only when the 'checkout' group is validated; being class-scoped, it also participates in group sequences like any constraint**

    Callback honours its groups option (default Default). A non-Default callback runs only when that group is validated, and it participates in group sequences exactly like any other constraint.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "51. Given:
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
"
    **✅ On the 'stackable' property path**

    atPath('stackable') relocates the violation to that field. The void return is normal — the error is committed by addViolation(), not by returning a value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "52. Where must #[Assert\Callback] be placed?"
    **✅ On a method (or on the class via the callback: option) — never on a property**

    Callback is a class-level constraint attached to a method; placing it on a property is a mistake. Read the object via $this or $context->getObject().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "53. By default, which validator class validates the constraint App\Validator\Foo?"
    **✅ App\Validator\FooValidator (constraint name + 'Validator')**

    Constraint::validatedBy() returns static::class.'Validator' by convention. Override it only when the validator service id differs from that name.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "54. How do you make a custom constraint apply at class scope?"
    **✅ Override getTargets() to return Constraint::CLASS_CONSTRAINT**

    The validator uses getTargets() (defaulting to PROPERTY_CONSTRAINT) to decide placement. Returning CLASS_CONSTRAINT makes the validator receive the whole object as $value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "55. What is the recommended first step in ConstraintValidator::validate()?"
    **✅ Check $constraint instanceof YourConstraint and throw UnexpectedTypeException otherwise**

    Guarding the constraint type documents intent and fails fast if the validator is mis-wired. It is the documented convention in the Symfony examples.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "56. What does #[HasNamedArguments] do on a custom Constraint constructor?"
    **✅ Passes attribute arguments as named constructor arguments (typed options)**

    #[HasNamedArguments] (Symfony\\Component\\Validator\\Attribute) opts into typed, named-argument construction instead of the legacy options-array style; remember to forward $groups and $payload to parent::__construct().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "57. How is a ConstraintValidator subclass wired so you can inject dependencies (e.g. a repository) into it?"
    **✅ It is autoconfigured as a service tagged validator.constraint_validator (via ConstraintValidatorInterface), so normal autowiring applies**

    Implementing ConstraintValidatorInterface (via ConstraintValidator) triggers autoconfiguration with the validator.constraint_validator tag, so validators are services and can have dependencies autowired.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "58. In a custom Constraint with #[HasNamedArguments], why forward $groups and $payload to parent::__construct()?"
    **✅ Otherwise the constraint ignores its groups/payload, so group assignment silently stops working**

    The base Constraint stores groups and payload. Forgetting to forward them means the constraint always lands in Default and the payload is lost.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "59. What do the first two statements accomplish?
```php
public function validate(mixed $value, Constraint $constraint): void {
    if (!$constraint instanceof ContainsAlphanumeric) {
        throw new UnexpectedTypeException($constraint, ContainsAlphanumeric::class);
    }
    if (null === $value || '' === $value) { return; }
    // ...
}
```
"
    **✅ Guard the constraint type (fail fast if mis-wired) and skip null/empty so the rule composes with NotBlank**

    The instanceof guard documents intent and throws UnexpectedTypeException if mis-wired; the null/empty early return keeps the constraint composable with presence checks like NotBlank.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "60. What does IS_REPEATABLE enable here?
```php
#[\Attribute(\Attribute::TARGET_PROPERTY | \Attribute::IS_REPEATABLE)]
final class ContainsAlphanumeric extends Constraint { /* ... */ }
```
"
    **✅ The same constraint attribute can be applied more than once on the same property**

    IS_REPEATABLE is a native PHP attribute flag allowing multiple instances on one target. Allowing both property and class placement instead needs TARGET_CLASS in the flags AND getTargets() returning both.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "61. How does a ConstraintValidator obtain $this->context (the ExecutionContext)?"
    **✅ The validator calls initialize($context) before validate(); ConstraintValidator stores it as $this->context**

    For each constraint the validator resolves its ConstraintValidator, calls initialize($context) (which sets $this->context on the base class) and then validate($value, $constraint).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "62. When is a violation built with buildViolation() actually recorded?"
    **✅ Only when addViolation() is called on the builder**

    buildViolation() returns a fluent builder; nothing is added to the list until addViolation() commits it. Forgetting it makes the validator pass silently.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "63. Which method returns the message with its {{ placeholders }} still unresolved?"
    **✅ getMessageTemplate()**

    getMessage() returns the interpolated message; getMessageTemplate() keeps the raw template with {{ x }} placeholders, and getParameters() holds the substitution map.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "64. On the violation builder, which method attaches the error to a different property?"
    **✅ atPath('otherField')**

    atPath() relocates the violation to a path relative to the current node, commonly used in class-level constraints to blame a specific field.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "65. What is $this->context->addViolation($message, $params) a shortcut for?"
    **✅ buildViolation($message, $params)->addViolation() — the common case with no extra setters**

    The context's addViolation() is a convenience for the simple case; use buildViolation() when you need atPath/setCode/setInvalidValue before committing.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "66. Why use setParameter('{{ value }}', ...) instead of concatenating the value into the message string?"
    **✅ Placeholders keep the message translatable; the {{ x }} template is interpolated later and preserved by getMessageTemplate()**

    {{ }} placeholders filled by setParameter keep the raw template translatable and available via getMessageTemplate(); inlining values into the string breaks translation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "67. Given:
```php
foreach ($violations as $v) {
    $errors[$v->getPropertyPath()][] = $v->getMessage();
}
```
What does $v->getMessage() return here?
"
    **✅ The fully interpolated message (placeholders resolved)**

    getMessage() is interpolated; getMessageTemplate() keeps the raw {{ x }} template. getPropertyPath() returns the path (e.g. 'code').

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "68. A developer uses $violations[0] (works) but array_map(..., $violations) (fails). Why?"
    **✅ The list is a Countable/IteratorAggregate/ArrayAccess object, not a plain array; use foreach/count() or iterator_to_array()**

    ConstraintViolationList implements ArrayAccess (so [0] works) but is not an array. Iterate it, call count(), use findByCodes(), or convert via iterator_to_array() for array functions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "69. What is the purpose of the builder's setCode() value?"
    **✅ A stable machine-readable code for the violation, usable via findByCodes() and independent of translated text**

    setCode() attaches a stable code (often a constant) so application code can branch on it without depending on translated message text; the list's findByCodes() filters by it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "70. Which constraint passes only when the value IS strictly null?"
    **✅ IsNull**

    IsNull requires the value to be exactly null (fails otherwise). It is the inverse of NotNull. Blank (its cousin) passes for null or ''.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/IsNull.html)

??? question "71. In #[Assert\GroupSequence(['A', 'B'])], if a constraint in group 'A' fails, group 'B' is…"
    **✅ Not validated — the sequence stops at the first group that produces a violation**

    A GroupSequence validates groups in order and stops as soon as one group yields a violation, so later groups (and their expensive checks) never run.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "72. A constraint declared without any explicit 'groups' option belongs to which validation group?"
    **✅ The special 'Default' group**

    Every constraint with no explicit groups is placed in the Default group, which is the group used when you call validate() without specifying groups.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "73. To make a single custom constraint usable on BOTH a property and a class, getTargets() should return…"
    **✅ [self::PROPERTY_CONSTRAINT, self::CLASS_CONSTRAINT]**

    getTargets() may return a single string or an array of them. Returning both PROPERTY_CONSTRAINT and CLASS_CONSTRAINT lets the same constraint be placed on a property and on a class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "74. You put #[Assert\Valid] on a property holding a Collection/array of Address objects. What happens on validate()?"
    **✅ Each element is traversed and its own constraints are validated (cascade)**

    Assert\Valid cascades into nested objects, and for a traversable/array it validates every element's constraints. Without it, nested objects are not validated at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Valid.html)

---

<small>Back to [Flashcards](index.md) · [Data Validation](../../validation/index.md)</small>

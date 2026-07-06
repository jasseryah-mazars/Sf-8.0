# Flashcards — Data Validation

27 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

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

??? question "4. Which statement about NotBlank and NotNull is correct?"
    **✅ NotBlank rejects an empty string; NotNull accepts an empty string**

    NotBlank fails on '', [], and blank strings; NotNull only fails on a strict null, so '' and 0 pass NotNull. This is a classic exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/NotBlank.html)

??? question "5. To apply constraints to every element of an indexed array, which constraint do you use?"
    **✅ All**

    All applies the given constraints to each element of a collection. Collection validates the keys of an associative array; they are not interchangeable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/All.html)

??? question "6. A nested object's own constraints never run during validation. Why?"
    **✅ The property is missing #[Assert\Valid] to cascade into it**

    Cascading is opt-in: without #[Assert\\Valid] on the property, the validator does not descend into the related object, so its constraints are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Valid.html)

??? question "7. What does #[Assert\Email] report for an empty string value?"
    **✅ No violation — empty and null values pass most constraints**

    Like Url, Regex and most value constraints, Email skips empty/null values. Combine it with NotBlank when an empty value must be rejected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Email.html)

??? question "8. What causes the validator to recurse into a nested object property?"
    **✅ #[Assert\Valid] on the property holding the nested object**

    Valid marks a property for cascading; the ValidValidator tells the context to descend so the nested object's own constraints (and, for collections, each element's) are validated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Valid.html)

??? question "9. A rule must compare two properties of the same object. Which scope fits best?"
    **✅ Class scope (e.g. a Callback or Expression constraint)**

    Cross-field rules need access to the whole object, so they belong on a class-target constraint such as Callback or Expression.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Expression.html)

??? question "10. A constraint on the getter isActive() reports a violation under which property path?"
    **✅ active**

    Getter constraints validate the return value of isX/getX/hasX and report under the property-ised name, so isActive() maps to 'active'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "11. You call validate($obj, groups: ['edit']). Which constraints run?"
    **✅ Only constraints assigned to the 'edit' group**

    Only the requested groups run. Passing a custom group does NOT implicitly include Default; list ['Default', 'edit'] if you need both.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "12. For a class that defines a GroupSequence, validating the 'Default' group will…"
    **✅ Trigger the group sequence (stepwise, stop on first failing group)**

    On a sequenced class, the special Default group is remapped to the sequence. To run the same constraints flat (bypassing the sequence), validate the {ClassName} group instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "13. For class App\Entity\User with no group sequence, what is the {ClassName} group?"
    **✅ 'User' (the short class name), equivalent to 'Default' here**

    The {ClassName} group uses the short class name. Every Default-group constraint is also in it, so with no sequence 'User' and 'Default' are equivalent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "14. Which default group name does an unqualified constraint belong to?"
    **✅ Default (capital D)**

    The implicit group is 'Default' with a capital D; group names are case-sensitive, so 'default' would be a different (empty) group.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

??? question "15. When does a group sequence stop early?"
    **✅ After the first group in the sequence that produces any violation**

    Each group runs fully, but the sequence halts after the first group that yields a violation, so later (often more expensive) groups are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "16. Inside a class's #[Assert\GroupSequence], how do you reference the class's own basic constraints?"
    **✅ Use the short class-name group (e.g. 'User')**

    Referencing 'Default' inside its own sequence would loop, because Default is remapped to the sequence. Use the {ClassName} group to mean the class's Default-group constraints run flat.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "17. What must a class annotated with #[Assert\GroupSequenceProvider] provide?"
    **✅ An implementation of GroupSequenceProviderInterface::getGroupSequence()**

    The provider attribute delegates to getGroupSequence() from GroupSequenceProviderInterface, evaluated on each validation so the sequence can depend on the object's state.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

??? question "18. What is the signature of an instance-method #[Assert\Callback]?"
    **✅ public function m(ExecutionContextInterface $context, mixed $payload): void**

    An instance callback receives the ExecutionContext and the optional payload and returns void; violations are added through the context. The static form additionally receives the object as the first argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "19. How does a callback validator register an error?"
    **✅ $context->buildViolation('...')->addViolation();**

    Violations are built and committed through the execution context. The callback's return value is ignored.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "20. #[Assert\Callback] is which kind of constraint?"
    **✅ A class-level constraint; the callback reads the whole object**

    Callback targets the class, so it does not receive a single property value; you read the object from $this or $context->getObject() and can report on any path with atPath().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

??? question "21. By default, which validator class validates the constraint App\Validator\Foo?"
    **✅ App\Validator\FooValidator (constraint name + 'Validator')**

    Constraint::validatedBy() returns static::class.'Validator' by convention. Override it only when the validator service id differs from that name.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "22. How do you make a custom constraint apply at class scope?"
    **✅ Override getTargets() to return Constraint::CLASS_CONSTRAINT**

    The validator uses getTargets() (defaulting to PROPERTY_CONSTRAINT) to decide placement. Returning CLASS_CONSTRAINT makes the validator receive the whole object as $value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "23. What is the recommended first step in ConstraintValidator::validate()?"
    **✅ Check $constraint instanceof YourConstraint and throw UnexpectedTypeException otherwise**

    Guarding the constraint type documents intent and fails fast if the validator is mis-wired. It is the documented convention in the Symfony examples.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "24. What does #[HasNamedArguments] do on a custom Constraint constructor?"
    **✅ Passes attribute arguments as named constructor arguments (typed options)**

    #[HasNamedArguments] (Symfony\\Component\\Validator\\Attribute) opts into typed, named-argument construction instead of the legacy options-array style; remember to forward $groups and $payload to parent::__construct().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "25. When is a violation built with buildViolation() actually recorded?"
    **✅ Only when addViolation() is called on the builder**

    buildViolation() returns a fluent builder; nothing is added to the list until addViolation() commits it. Forgetting it makes the validator pass silently.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

??? question "26. Which method returns the message with its {{ placeholders }} still unresolved?"
    **✅ getMessageTemplate()**

    getMessage() returns the interpolated message; getMessageTemplate() keeps the raw template with {{ x }} placeholders, and getParameters() holds the substitution map.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

??? question "27. On the violation builder, which method attaches the error to a different property?"
    **✅ atPath('otherField')**

    atPath() relocates the violation to a path relative to the current node, commonly used in class-level constraints to blame a specific field.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

---

<small>Back to [Flashcards](index.md) · [Data Validation](../../validation/index.md)</small>

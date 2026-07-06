# Lab: <Concept> — <Short Title>

<!--
PRACTICAL LAB TEMPLATE. Follow this section order exactly.
Pick the mode per the concept:
  - TDD lab (code behaviour): include the full TDD block.
  - Manual-verification lab (config/infra): replace TDD with Validation Steps
    (CLI / profiler / curl checks).
  - Conceptual Simulation (pure theory): replace Task+TDD with predict-output /
    order-the-steps / debug-the-scenario questions (+ hidden answers).
All code: Symfony 8 / PHP 8.4, no out-of-scope deps. Complete <?php snippets must compile.
-->

!!! abstract "Practical Lab"
    **Objective:** <the one concept this lab makes you able to apply> ·
    **Difficulty:** Easy | Medium | Advanced ·
    **Theory:** [<chapter>](../<area>/<chapter>.md) ·
    **Mode:** TDD | Manual verification | Conceptual simulation

## Objective

What you will be able to *do* after this lab (not just know).

## Prerequisites

- Chapters: [links]
- Assumed skills: …

## TD Instructions

Numbered, university-TD-style steps. Each step is a concrete action, not a solution.

1. …
2. …

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · no libraries outside the certification scope · follow
    best practices (attributes, strict types, readonly where apt).

## Implementation Guide (partial)

High-level pointers only — the classes/interfaces to reach for and the shape of the
solution. **Not** the full code.

## TDD — write the test first
<!-- Include this block ONLY for code-behaviour labs; otherwise delete it. -->

!!! note "Red → Green → Refactor"
    1. **Red:** write the failing test below; run it, watch it fail.
    2. **Green:** write the minimum code to pass.
    3. **Refactor:** clean up with the test as your safety net.

**Behaviour (Given/When/Then):**

- **Given** … **When** … **Then** …

```php
<?php
declare(strict_types=1);

namespace App\Tests\...;

use PHPUnit\Framework\TestCase;
// ... the test skeleton with real assertions (arrange/act/assert)
```

!!! tip "Setup hints"
    How to run it: `vendor/bin/phpunit tests/...`. Fixtures/mocks to use
    (e.g. `MockHttpClient`, a stub `TokenInterface`, `ContainerBuilder`).

## Validation Steps
<!-- For manual/config labs, or in ADDITION to TDD. -->

- [ ] `php bin/console <cmd>` shows …
- [ ] Profiler / debug toolbar shows …
- [ ] `curl -I …` returns header …

## Review — Common Mistakes

- Mistake → why it fails → the fix.

## Exam Connection

How this maps to what the certification tests (the trap it defends against).

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    ```php
    <?php
    declare(strict_types=1);
    // full, compiling reference implementation
    ```

## Alternative Approaches (optional)

- **Option A (simple)** … **Option B (advanced)** … **Option C (exam-style)** …

---

<small>Theory: [<chapter>](../<area>/<chapter>.md) · Labs: [all labs](index.md)</small>

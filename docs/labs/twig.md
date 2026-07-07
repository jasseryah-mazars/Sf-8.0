---
tags:
  - Labs
  - Twig
---

# Lab: Custom Twig Extension — an `excerpt` filter

!!! abstract "Practical Lab"
    **Objective:** build and register a custom Twig **filter** whose logic you can
    unit-test in isolation, and understand when its output must be escaped ·
    **Difficulty:** Easy ·
    **Theory:** [Filters & Functions](../twig/filters-functions.md) ·
    **Mode:** TDD

## Objective

After this lab you can **write a custom Twig filter**, expose it through a
`Twig\Extension\AbstractExtension` (and the `#[AsTwigFilter]` attribute variant),
**test the underlying callable directly** with edge cases, render it inside a real
`Twig\Environment`, and decide correctly whether it needs `is_safe: ['html']`.

The running example is an `excerpt` filter: `{{ post.body|excerpt(20) }}` truncates
text to *N* characters on a word boundary and appends an ellipsis.

## Prerequisites

- Chapters: [Filters & Functions](../twig/filters-functions.md),
  [Twig Syntax](../twig/syntax.md), [Auto-Escaping](../twig/auto-escaping.md)
- Assumed skills: writing a PHPUnit `TestCase`, PHP 8.4 syntax (first-class
  callable `$this->method(...)`, named args), basic `mb_*` string functions.

## TD Instructions

Numbered, do them in order — do **not** jump to the reference solution.

1. Create `App\Twig\ContentExtension` extending `Twig\Extension\AbstractExtension`.
2. Add a public method `excerpt(string $text, int $limit = 100, string $ellipsis = '…'): string`
   that returns `$text` unchanged when it is at or under `$limit` characters, and
   otherwise truncates to at most `$limit` characters **without cutting a word in
   half**, then appends `$ellipsis`.
3. Implement `getFilters(): array` returning one `Twig\TwigFilter` named `excerpt`
   wired to the method via first-class callable syntax `$this->excerpt(...)`.
4. Decide the `is_safe` option deliberately: the filter returns **plain text**, so it
   must stay auto-escaped. Do **not** mark it safe.
5. **Write the failing test first** (see the TDD block) covering the edge cases:
   short string, exact boundary, long string, multibyte input, custom ellipsis.
6. Add one test that registers the extension on a `Twig\Environment` (with an
   `ArrayLoader`) and asserts the rendered string of `{{ text|excerpt(10) }}`.
7. Run the tests red → make them green → refactor.
8. **Level up:** re-expose the same logic with `#[AsTwigFilter('excerpt')]` on a plain
   class and confirm the behaviour is identical.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · Twig 3.x · no libraries outside the certification scope ·
    follow best practices (attributes, strict types, `final`, first-class callables).

## Implementation Guide (partial)

High-level pointers only — not the full code.

- Reach for `Twig\Extension\AbstractExtension` and `Twig\TwigFilter`.
- Register with `new TwigFilter('excerpt', $this->excerpt(...))` — the second arg is
  any callable; first-class callable syntax keeps it type-safe.
- For "don't cut a word", find the last space at or before the limit with
  `mb_strrpos(mb_substr($text, 0, $limit), ' ')`; fall back to a hard cut when there
  is no space. Use the `mb_*` family so multibyte input counts characters, not bytes.
- **Escaping:** the callable returns plain text; leave `is_safe` unset so Twig escapes
  it. You would only add `is_safe: ['html']` if the filter itself produced trusted
  markup (it does not here).
- With Symfony autoconfiguration an `AbstractExtension` is auto-tagged
  `twig.extension`; a class using `#[AsTwigFilter]` is registered automatically. No
  manual service wiring is needed.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red:** write the failing test below; run it, watch it fail (class missing).
    2. **Green:** write the minimum `ContentExtension` to pass.
    3. **Refactor:** clean up the truncation logic with the test as your safety net.

**Behaviour (Given/When/Then):**

- **Given** a string at or under the limit, **When** `excerpt` runs, **Then** it
  returns the string unchanged (no ellipsis).
- **Given** a longer string, **When** `excerpt(limit)` runs, **Then** the result is at
  most `limit` characters of text, cut on a word boundary, plus the ellipsis.
- **Given** the extension registered on a `Twig\Environment`, **When** a template uses
  `{{ text|excerpt(10) }}`, **Then** the rendered output matches the callable.

```php
<?php
declare(strict_types=1);

namespace App\Tests\Twig;

use App\Twig\ContentExtension;
use PHPUnit\Framework\TestCase;
use Twig\Environment;
use Twig\Loader\ArrayLoader;

final class ContentExtensionTest extends TestCase
{
    private ContentExtension $extension;

    protected function setUp(): void
    {
        $this->extension = new ContentExtension();
    }

    // --- unit-test the callable directly (fast, no Twig needed) ---

    public function testShortStringIsReturnedUnchanged(): void
    {
        self::assertSame('Hello', $this->extension->excerpt('Hello', 100));
    }

    public function testExactBoundaryIsNotTruncated(): void
    {
        // 5 chars, limit 5 -> unchanged, no ellipsis
        self::assertSame('Hello', $this->extension->excerpt('Hello', 5));
    }

    public function testLongStringIsTruncatedOnWordBoundary(): void
    {
        $result = $this->extension->excerpt('The quick brown fox jumps', 12);

        // cut at the last space at/under 12, no half words
        self::assertSame('The quick…', $result);
    }

    public function testHardCutWhenNoSpaceBeforeLimit(): void
    {
        self::assertSame('abcde…', $this->extension->excerpt('abcdefghij', 5));
    }

    public function testMultibyteCountsCharactersNotBytes(): void
    {
        // 5 accented chars = 10 bytes; limit 5 counts CHARACTERS -> unchanged
        self::assertSame('ééééé', $this->extension->excerpt('ééééé', 5));
    }

    public function testCustomEllipsis(): void
    {
        self::assertSame(
            'The quick...',
            $this->extension->excerpt('The quick brown fox', 12, '...'),
        );
    }

    // --- render through a real Twig\Environment with the extension registered ---

    public function testFilterRendersInTemplate(): void
    {
        $twig = new Environment(new ArrayLoader([
            'p' => '{{ text|excerpt(10) }}',
        ]));
        $twig->addExtension($this->extension);

        self::assertSame(
            'Lorem…',
            $twig->render('p', ['text' => 'Lorem ipsum dolor']),
        );
    }

    public function testFilterOutputIsAutoEscaped(): void
    {
        // Not is_safe -> HTML in the (short) value must come out escaped.
        $twig = new Environment(new ArrayLoader([
            'p' => '{{ text|excerpt(100) }}',
        ]));
        $twig->addExtension($this->extension);

        self::assertSame(
            '&lt;b&gt;hi&lt;/b&gt;',
            $twig->render('p', ['text' => '<b>hi</b>']),
        );
    }
}
```

!!! tip "Setup hints"
    Run it with `vendor/bin/phpunit tests/Twig/ContentExtensionTest.php`. No
    container or kernel is needed — `new Environment(new ArrayLoader([...]))` plus
    `addExtension()` is enough to exercise the filter end-to-end. The auto-escaping
    test relies on the default `html` autoescape strategy of `Environment`.

## Validation Steps

In addition to the green test suite, verify the wiring inside a real app:

- [ ] `php bin/console debug:twig --filter=excerpt` lists your filter and its class.
- [ ] `php bin/console debug:twig` shows `ContentExtension` under *Extensions*.
- [ ] A page using `{{ post.body|excerpt(20) }}` renders truncated, escaped text.

## Review — Common Mistakes

- **Marking the filter `is_safe: ['html']` "to be safe".** → It disables escaping, so
  a `<b>hi</b>` value would render as live markup (XSS risk). → Leave `is_safe` unset
  for a plain-text filter; only trusted-markup filters get it.
- **Using `substr`/`strlen` instead of `mb_*`.** → Multibyte input is miscounted and
  can be cut mid-character, producing mojibake. → Use `mb_substr`/`mb_strlen`.
- **Appending the ellipsis even when nothing was truncated.** → `assertSame` on the
  boundary case fails. → Return early when `mb_strlen($text) <= $limit`.
- **Passing a string callable like `'excerpt'` to `TwigFilter`.** → Twig can't resolve
  the method. → Use `$this->excerpt(...)` (first-class callable) or `[$this, 'excerpt']`.
- **Forgetting the extension is auto-tagged.** → Manually declaring a
  `twig.extension` service causes a duplicate. → With autoconfigure on, do nothing.

## Exam Connection

The certification tests the **filter-vs-function** distinction, the **registration
API** (`AbstractExtension::getFilters()` returning `TwigFilter`, or the
`#[AsTwigFilter]` attribute), and the **escaping trap**: filter output is
auto-escaped unless declared `is_safe: ['html']`. This lab drills all three, and the
`is_safe` decision (plain text ⇒ stay escaped) is exactly the trap the exam sets.

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    === "AbstractExtension (classic)"

        ```php
        <?php
        declare(strict_types=1);

        namespace App\Twig;

        use Twig\Extension\AbstractExtension;
        use Twig\TwigFilter;

        final class ContentExtension extends AbstractExtension
        {
            /**
             * @return list<TwigFilter>
             */
            public function getFilters(): array
            {
                return [
                    // No is_safe: output is plain text and must stay auto-escaped.
                    new TwigFilter('excerpt', $this->excerpt(...)),
                ];
            }

            public function excerpt(string $text, int $limit = 100, string $ellipsis = '…'): string
            {
                if ($limit <= 0 || mb_strlen($text) <= $limit) {
                    return $text;
                }

                $slice = mb_substr($text, 0, $limit);
                $lastSpace = mb_strrpos($slice, ' ');

                // Cut on the last word boundary; hard-cut when there is no space.
                $cut = false !== $lastSpace ? mb_substr($slice, 0, $lastSpace) : $slice;

                return $cut.$ellipsis;
            }
        }
        ```

    === "Attribute (Twig 3.x)"

        ```php
        <?php
        declare(strict_types=1);

        namespace App\Twig;

        use Twig\Attribute\AsTwigFilter;

        final class ContentExtension
        {
            #[AsTwigFilter('excerpt')]
            public function excerpt(string $text, int $limit = 100, string $ellipsis = '…'): string
            {
                if ($limit <= 0 || mb_strlen($text) <= $limit) {
                    return $text;
                }

                $slice = mb_substr($text, 0, $limit);
                $lastSpace = mb_strrpos($slice, ' ');
                $cut = false !== $lastSpace ? mb_substr($slice, 0, $lastSpace) : $slice;

                return $cut.$ellipsis;
            }
        }
        ```

    Both register `excerpt` automatically under Symfony autoconfiguration and share
    the identical, unit-tested method body — so the test suite above passes for either.

## Alternative Approaches (optional)

- **Option A (simple):** a closure inline in `getFilters()` —
  `new TwigFilter('excerpt', fn (string $s, int $n = 100) => ...)`. Fine for trivial
  logic, but harder to unit-test in isolation than a named method.
- **Option B (advanced):** move the logic into a
  `RuntimeExtensionInterface` runtime class (or an `#[AsTwigFilter]` on a runtime) so
  it is lazily instantiated only when the filter is used — the right choice when the
  filter needs injected services.
- **Option C (exam-style):** expose it as a **function** instead —
  `new TwigFunction('excerpt', ...)` used as `{{ excerpt(text, 20) }}`. Same callable,
  different call site; know which reads more naturally (a value transform ⇒ filter).

---

<small>Theory: [Filters & Functions](../twig/filters-functions.md) · Labs: [all labs](index.md)</small>

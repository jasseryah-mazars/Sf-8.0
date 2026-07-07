# Filesystem & Finder Components

!!! tip "In a nutshell"
    Filesystem wraps PHP's file functions with cross-platform methods that throw
    on failure; Finder is a fluent builder that yields matching files as
    `SplFileInfo`. Exam gold: `dumpFile()` writes atomically (temp + rename), and
    Finder always needs directories via `in()`.

!!! example "Real-world analogy"
    Filesystem is a careful mover who shouts the moment something goes wrong rather than
    silently dropping a box (it throws instead of returning `false`). Its `dumpFile()` is
    like a chef plating a dish completely on a spare plate and only then swapping it onto
    the table, so a diner never glimpses a half-arranged plate (the temp-file-plus-rename
    atomic write). Finder is the librarian you send to fetch books: you must point them at
    rooms and shelves (`in()`), not at a single book, and then they filter by title, date
    or size and hand back each match as a labelled index card (an `SplFileInfo`).

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Perform safe file operations with the `Filesystem` class and `Path` helpers.
    - [ ] Build fluent file queries with `Finder` (name/date/size/sort).
    - [ ] Iterate `SplFileInfo` results and know Finder's limits.

    **Syllabus:** `Miscellaneous → Filesystem & Finder` ·
    **Level:** Advanced ·
    **Est. time:** 30 min ·
    **Prerequisites:** [PHP](../php-web-security/index.md)

---

## Theory

**Filesystem** wraps PHP's file functions with cross-platform, exception-throwing
methods (atomic writes, recursive copy/remove). **Finder** is a fluent builder
that finds files and directories matching criteria and yields them as
`SplFileInfo` objects.

```php
use Symfony\Component\Filesystem\Filesystem;
use Symfony\Component\Finder\Finder;

// Filesystem: cross-platform operations that throw on failure
$fs = new Filesystem();
$fs->mkdir('/tmp/reports');                    // recursive create
$fs->dumpFile('/tmp/reports/r.txt', 'done');   // atomic write

// Finder: fluent query yielding SplFileInfo objects
foreach ((new Finder())->files()->in('/tmp/reports')->name('*.txt') as $file) {
    echo $file->getFilename();
}
```

## Deep Dive — how it works internally

!!! question "Predict first"
    You point `Finder::in()` at a single **file** path and iterate. What happens?

??? note "Reveal"
    It throws — `Finder` searches **directories**, not one file. Give it a directory
    and narrow with `name()`/`path()`; there is no "search a single file" mode.

### Filesystem

`Symfony\Component\Filesystem\Filesystem` methods throw
`Symfony\Component\Filesystem\Exception\IOExceptionInterface` on failure instead
of returning `false`:

| Method | Does |
|---|---|
| `exists($path)` | Test existence (accepts array/iterable) |
| `mkdir($dirs, $mode)` | Recursive create |
| `copy($src, $dst, $overwrite)` | Copy a file |
| `remove($files)` | Recursive delete |
| `dumpFile($path, $content)` | **Atomic** write (temp file + rename) |
| `appendToFile($path, $content)` | Append |
| `rename($origin, $target)` | Move/rename |
| `symlink`, `chmod`, `chown` | Links/permissions |

```php
use Symfony\Component\Filesystem\Exception\IOExceptionInterface;
use Symfony\Component\Filesystem\Filesystem;

$fs = new Filesystem();

try {
    $fs->mkdir('/srv/app/exports');                       // recursive create
    $fs->copy('in.csv', '/srv/app/exports/in.csv', true); // overwrite = true
    $fs->dumpFile('/srv/app/exports/status.txt', 'ok');   // atomic write
    $fs->remove(['/srv/app/exports/tmp', '/srv/old.lock']); // recursive delete
} catch (IOExceptionInterface $e) {
    echo 'Failed at '.$e->getPath(); // no silent false returns
}
```

`dumpFile()` writes to a temporary file then renames it — so readers never see a
half-written file. The static `Symfony\Component\Filesystem\Path` helper
normalises and manipulates path **strings** without touching the disk:
`Path::canonicalize()`, `Path::makeAbsolute()`, `Path::makeRelative()`,
`Path::join()`, `Path::isAbsolute()`.

```php
use Symfony\Component\Filesystem\Path;

// Pure string manipulation — nothing on disk is read or written
Path::canonicalize('/var/www/../log/./app.log'); // "/var/log/app.log"
Path::makeAbsolute('config/app.yaml', '/srv');   // "/srv/config/app.yaml"
Path::makeRelative('/srv/config', '/srv');       // "config"
Path::join('/srv', 'config', 'app.yaml');        // "/srv/config/app.yaml"
Path::isAbsolute('C:\\Programs');                // true (cross-platform aware)
```

### Finder

`Symfony\Component\Finder\Finder` builds an immutable-ish query then acts as an
`IteratorAggregate` of `Symfony\Component\Finder\SplFileInfo`:

```php
<?php
declare(strict_types=1);

use Symfony\Component\Finder\Finder;

$finder = (new Finder())
    ->files()
    ->in(__DIR__.'/var/log')
    ->name('*.log')
    ->notName('debug.log')
    ->size('> 1K')
    ->date('since yesterday')
    ->sortByModifiedTime();

foreach ($finder as $file) {
    // $file is a Finder SplFileInfo
    echo $file->getRelativePathname().' '.$file->getContents();
}
```

Key builders: `files()`/`directories()`, `in($dirs)`, `name()/notName()`,
`contains()`, `path()`, `size()`, `date()`, `depth()`, `exclude()`,
`ignoreDotFiles()`, `ignoreVCS()`, `sortByName()/sortByModifiedTime()`,
`filter(callable)`. `count($finder)` gives the match count; `hasResults()` tests
non-empty.

```mermaid
flowchart LR
    F[Finder] --> IN[in dirs] --> FL[filters: name/size/date] --> IT[iterate SplFileInfo]
```

!!! note "Source reference"
    `Symfony\Component\Finder\Finder` and `Filesystem::dumpFile()` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Finder/Finder.php).

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    use Symfony\Component\Filesystem\Filesystem;
    use Symfony\Component\Filesystem\Path;

    $fs = new Filesystem();
    $target = Path::join(sys_get_temp_dir(), 'reports', 'r.txt');
    $fs->mkdir(Path::getDirectory($target));
    $fs->dumpFile($target, "generated\n"); // atomic
    ```

=== "Console"

    ```console
    $ php bin/console debug:container filesystem
    ```

=== "YAML"

    ```yaml
    # No YAML: these components are used in PHP, not configured via YAML.
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `dumpFile()` for atomic writes | `file_put_contents` for critical files |
| Catch `IOExceptionInterface` | Ignoring silent `false` returns |
| Use `Path::join`/`canonicalize` for portability | Concatenating paths with hardcoded `/` |
| Scope `Finder` with `in()` + filters | Loading whole trees into arrays |

## When (not) to use it / alternatives

Use Filesystem/Finder for build steps, log rotation, import scanning. `Finder`
works on the **local** filesystem (and streams); for remote storage use a
dedicated flysystem-like library (out of scope). Finder cannot search a single
file — it needs directories via `in()`.

!!! danger "Certification traps"
    - `Filesystem` methods **throw** on error; they don't return `false`.
    - `dumpFile()` is **atomic** (temp + rename); `appendToFile()` is not.
    - `Path` manipulates strings only — it does **not** touch the disk.
    - `Finder` yields its own `SplFileInfo` with `getRelativePathname()`; you must call `in()`.
    - A `Finder` cannot be re-iterated in some source modes — rebuild it if needed.

!!! warning "Common mistakes"
    - Calling `Finder::in()` on a file path instead of a directory.
    - Forgetting `files()`/`directories()` and getting both.

## Exercises

1. **(Advanced)** Atomically write a file, creating its parent directory first.
2. **(Advanced)** Find all `*.log` files over 1 KB modified since yesterday,
   newest first.

??? success "Solutions"

    **1.** See the `dumpFile()` snippet above (`mkdir` + `dumpFile`).

    **2.** See the `Finder` snippet: `->files()->name('*.log')->size('> 1K')->date('since yesterday')->sortByModifiedTime()`.

## Certification questions

??? question "Q1. What makes `dumpFile()` safe against partial reads?"
    - [x] A. It writes to a temp file then atomically renames ✅
    - [ ] B. It locks the file with flock
    - [ ] C. It compresses the content

    **Why:** The temp-write + rename means readers see either old or complete new content.
    **Ref:** [Filesystem](https://symfony.com/doc/current/components/filesystem.html).

??? question "Q2. `Finder` requires which call to define where to search?"
    - [x] A. `in($dirs)` ✅
    - [ ] B. `from($dirs)`
    - [ ] C. `search($dirs)`

    **Why:** `in()` sets the search directories; without it Finder throws.
    **Ref:** [Finder](https://symfony.com/doc/current/components/finder.html).

??? question "Q3. On failure, `Filesystem::copy()`…"
    - [x] A. throws an `IOExceptionInterface` ✅
    - [ ] B. returns `false`
    - [ ] C. returns `null`

    **Why:** Filesystem methods signal errors via exceptions. **Ref:** [Filesystem](https://symfony.com/doc/current/components/filesystem.html#error-handling).

## Key takeaways

- Filesystem: exception-throwing, cross-platform file ops; `dumpFile()` is atomic.
- `Path` helpers normalise/join paths without disk access.
- Finder: fluent `in()`+filters, yields `SplFileInfo`; needs directories.

## Last-minute revision

!!! tip "Cheat sheet"
    - FS: `exists`, `mkdir`, `copy`, `remove`, `dumpFile`, `appendToFile`, `rename`.
    - `Path::canonicalize/join/makeAbsolute/makeRelative`.
    - Finder: `files()->in()->name()->size('> 1K')->date('since yesterday')->sortByModifiedTime()`.
    - `count()`, `hasResults()`, `getRelativePathname()`.

## Connections

- **Depends on:** PHP file functions — `Filesystem` wraps them with exceptions instead of `false` returns.
- **Reused in:** [Deployment](deployment.md) — build/scan steps; [Process](process.md) — often paired to shell out over discovered files.
- **Confused with:** raw `glob()`/`scandir()` — Finder adds fluent filters and yields `SplFileInfo`.

## Official References
- [Official docs — Filesystem](https://symfony.com/doc/current/components/filesystem.html)
- [Official docs — Finder](https://symfony.com/doc/current/components/finder.html)
- [Symfony source — Finder](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Finder/Finder.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony components" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/components/filesystem.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** `dumpFile()` is atomic (temp + rename)
- [ ] write files safely and build a `Finder` query in Symfony 8
- [ ] debug a `Finder` that found nothing (missing `in()`, wrong `files()`/`directories()`)
- [ ] spot the trick: `Filesystem` throws, it doesn't return `false`; `Path` never touches disk
- [ ] describe how Finder yields its own `SplFileInfo` with `getRelativePathname()`

---

<small>Related: [Process](process.md) · [Lock](lock.md) · [Deployment](deployment.md)</small>

# Verbosity Levels

!!! tip "In a nutshell"
    Verbosity controls how much a command prints without changing what it does;
    users pick it with `-q`, `-v`, `-vv` or `-vvv`. Remember for the exam: the
    constants are 16/32/64/128/256 and they live on the output, not the input.

!!! example "Real-world analogy"
    Verbosity is like the zoom level on a digital map. Zooming in or out never changes the
    territory itself — the roads and rivers are the same, just as a command's logic is
    unchanged — it only controls how much detail is drawn. At the furthest-out view you see
    just major cities (`-q`), and as you zoom in you progressively reveal towns, then
    streets, then every labelled alley (`-vvv`). And that setting belongs to the display
    you're looking through, not to the map's underlying data — which is why verbosity lives
    on the output, not the input.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Map `-q`, `-v`, `-vv`, `-vvv` to the `VERBOSITY_*` constants
    - [ ] Gate output using `isVerbose()`, `isVeryVerbose()`, `isDebug()`
    - [ ] Emit a line only at a chosen verbosity
    - [ ] Explain how verbosity is set on the output and its integer values

    **Syllabus:** `Console → Verbosity` ·
    **Level:** Advanced ·
    **Est. time:** 20 min ·
    **Prerequisites:** [Input & output](input-output.md)

    **Examen Symfony 8 :** OUI

---

## Pour les nuls

### L'idée en une phrase
La verbosité contrôle **combien** une commande affiche, sans jamais changer **ce qu'elle fait** — c'est un réglage d'affichage, pas de logique.

### Imagine dans la vraie vie
La verbosité est comme le niveau de zoom sur une carte numérique. Zoomer ou dézoomer ne change jamais le territoire lui-même — les routes et rivières restent les mêmes, comme la logique d'une commande reste inchangée — ça ne fait que contrôler le niveau de détail affiché.

### Dans Symfony
`$output->writeln('Détail interne', OutputInterface::VERBOSITY_DEBUG)` n'affiche cette ligne que si l'utilisateur a lancé la commande avec `-vvv` — invisible en usage normal, utile pour le débogage fin.

### Exemple simple
```php
if ($output->isVerbose()) { $io->writeln('Traitement du fichier ' . $fichier); }
```

### Comment le mémoriser 🧠
La verbosité vit sur la **sortie** (`OutputInterface`), jamais sur l'entrée — logique, puisque c'est le réglage de "combien on affiche", pas de "quoi on lit".

---

## Theory

Verbosity controls **how much** a command prints, without changing its logic. Users
choose it with global flags; commands respect it when writing output.

| Flag | Level constant | Integer |
|---|---|---|
| `--quiet` / `-q` | `VERBOSITY_QUIET` | 16 |
| *(default)* | `VERBOSITY_NORMAL` | 32 |
| `-v` | `VERBOSITY_VERBOSE` | 64 |
| `-vv` | `VERBOSITY_VERY_VERBOSE` | 128 |
| `-vvv` | `VERBOSITY_DEBUG` | 256 |

`-q` silences all normal output (errors still surface); higher levels reveal more
diagnostic detail. The constants live on
`Symfony\Component\Console\Output\OutputInterface`.

```php
use Symfony\Component\Console\Output\OutputInterface;

OutputInterface::VERBOSITY_QUIET;         // 16  (-q)
OutputInterface::VERBOSITY_NORMAL;        // 32  (default)
OutputInterface::VERBOSITY_VERBOSE;       // 64  (-v)
OutputInterface::VERBOSITY_VERY_VERBOSE;  // 128 (-vv)
OutputInterface::VERBOSITY_DEBUG;         // 256 (-vvv)
```

!!! question "Predict first"
    To decide whether to print a diagnostic line, do you check the verbosity on the
    `InputInterface` or the `OutputInterface`?

??? note "Reveal"
    On the **output**. The Application parses `-v/-vv/-vvv/-q` and calls
    `$output->setVerbosity()`, so verbosity is an output property. Gate with
    `$output->isVerbose()` / `isDebug()` (mirrored on `SymfonyStyle`).

## Deep Dive — how it works internally

The `Application` parses the global `-v/-vv/-vvv/-q` flags **before** dispatching to
a command and calls `$output->setVerbosity()` accordingly. Verbosity is therefore a
property of the **output**, not the input.

```php
// What the Application does from the flags, before your command runs
$output->setVerbosity(OutputInterface::VERBOSITY_VERBOSE);   // user passed -v
$output->getVerbosity();                                     // 64
```

Two ways to honour it:

1. **Guards** — `isQuiet()`, `isVerbose()`, `isVeryVerbose()`, `isDebug()` on the
   output (and mirrored on `SymfonyStyle`). Wrap expensive/diagnostic output in
   these.
2. **Per-message level** — pass a verbosity mask as the second argument to
   `write()` / `writeln()`; the message prints only if the current level is at least
   that value:

```php
$output->writeln('debug detail', OutputInterface::VERBOSITY_DEBUG);
```

```php
// Guards on the output (mirrored on SymfonyStyle)
if ($output->isQuiet())       { /* -q */ }
if ($output->isVerbose())     { /* -v, -vv and -vvv */ }
if ($output->isVeryVerbose()) { /* -vv and -vvv */ }
if ($output->isDebug())       { /* -vvv only */ }
```

Because the constants are ordered integers (16 < 32 < 64 < 128 < 256), a message
tagged `VERBOSITY_VERBOSE` (64) shows at `-v`, `-vv` and `-vvv`, but not at normal
(32) or quiet (16). Internally `write()` compares
`$this->verbosity >= $messageVerbosity`.

```php
// -v sets the level to VERBOSITY_VERBOSE (64): 64 >= 64 -> printed
$output->writeln('shown at -v, -vv and -vvv', OutputInterface::VERBOSITY_VERBOSE);
// at the default level (32): 32 >= 64 is false -> suppressed
```

```mermaid
flowchart LR
    A["-q/-v/-vv/-vvv"] --> B["Application parses flags"]
    B --> C["output->setVerbosity(level)"]
    C --> D{"level >= message level?"}
    D -- yes --> E["print"]
    D -- no --> F["suppress"]
```

!!! note "Source reference"
    `OutputInterface::VERBOSITY_*` and `Output::write()`'s verbosity check —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Console/Output/OutputInterface.php).

## Configuration & code

=== "Guards"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Command;

    use Symfony\Component\Console\Attribute\AsCommand;
    use Symfony\Component\Console\Command\Command;
    use Symfony\Component\Console\Output\OutputInterface;
    use Symfony\Component\Console\Style\SymfonyStyle;

    #[AsCommand(name: 'app:sync')]
    final class SyncCommand
    {
        public function __invoke(SymfonyStyle $io, OutputInterface $output): int
        {
            $io->writeln('Syncing…');                       // normal

            if ($output->isVerbose()) {
                $io->writeln('Connecting to remote host');  // -v and up
            }

            if ($output->isDebug()) {
                $io->writeln('Payload dump: {...}');         // -vvv only
            }

            return Command::SUCCESS;
        }
    }
    ```

=== "Per-message level"

    ```php
    <?php
    declare(strict_types=1);

    use Symfony\Component\Console\Output\OutputInterface;

    function report(OutputInterface $output): void
    {
        $output->writeln('always');                                   // normal+
        $output->writeln('more', OutputInterface::VERBOSITY_VERBOSE); // -v+
        $output->writeln('trace', OutputInterface::VERBOSITY_DEBUG);  // -vvv
    }
    ```

=== "Console"

    ```console
    $ php bin/console app:sync            # normal
    $ php bin/console app:sync -v         # verbose
    $ php bin/console app:sync -vvv       # debug
    $ php bin/console app:sync -q         # quiet (suppress normal output)
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Put diagnostics behind `isVerbose()`/`isDebug()` | Always dumping stack traces |
| Tag messages with a verbosity level | Printing everything at normal level |
| Keep essential result at normal level | Hiding the actual result behind `-v` |
| Respect `-q` for scripts/cron | Forcing output regardless of `-q` |

## When (not) to use it / alternatives

Verbosity is for *human diagnostics*. For machine-readable output prefer an explicit
`--format=json` option or write structured data to STDOUT (see
[input & output](input-output.md)); do not rely on verbosity to toggle data
formats. In `-vvv` (debug), Symfony also shows full exception traces on errors.

!!! danger "Certification traps"
    - The constants are **16/32/64/128/256** (QUIET/NORMAL/VERBOSE/VERY_VERBOSE/DEBUG).
    - `-v` = verbose, `-vv` = very verbose, `-vvv` = debug.
    - Verbosity lives on the **output**, set by the Application from the flags.
    - `-q` suppresses normal output but the command still runs and returns its code.
    - A higher level shows all messages tagged at that level **or lower**.

!!! warning "Common mistakes"
    - Reading verbosity from the *input* — it is on the *output*.
    - Assuming `-q` skips execution; it only silences output.

## Exercises

1. **(Basic)** Print `"connecting"` only at `-v` or higher and `"raw response"` only
   at `-vvv`.
2. **(Intermediate)** Write the same three lines using per-message verbosity masks
   instead of `if` guards.

??? success "Solutions"

    **1.**

    ```php
    if ($output->isVerbose())  { $output->writeln('connecting'); }
    if ($output->isDebug())    { $output->writeln('raw response'); }
    ```

    **2.**

    ```php
    $output->writeln('connecting', OutputInterface::VERBOSITY_VERBOSE);
    $output->writeln('raw response', OutputInterface::VERBOSITY_DEBUG);
    ```

## Certification questions

*Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.*

??? question "Q1. Which flag corresponds to `VERBOSITY_VERY_VERBOSE`?"
    - [ ] A. `-v`
    - [x] B. `-vv` ✅
    - [ ] C. `-vvv`
    - [ ] D. `-q`

    **Why:** `-vv` is very verbose (128); `-vvv` is debug (256). **Ref:**
    [Console verbosity](https://symfony.com/doc/8.0/console/verbosity.html).

??? question "Q2. What is the integer value of `VERBOSITY_NORMAL`?"
    - [ ] A. 0
    - [ ] B. 16
    - [x] C. 32 ✅
    - [ ] D. 64

    **Why:** QUIET=16, NORMAL=32, VERBOSE=64, VERY_VERBOSE=128, DEBUG=256. **Ref:**
    [Console verbosity](https://symfony.com/doc/8.0/console/verbosity.html).

??? question "Q3. Where does the current verbosity level live?"
    - [x] A. On the `OutputInterface` (set by the Application) ✅
    - [ ] B. On the `InputInterface`
    - [ ] C. On the `Command`
    - [ ] D. In an environment variable only

    **Why:** the Application calls `$output->setVerbosity()` from the flags. **Ref:**
    [Console verbosity](https://symfony.com/doc/8.0/console/verbosity.html).

??? question "Q4. A message written with `VERBOSITY_VERBOSE` appears at…"
    - [x] A. `-v`, `-vv`, and `-vvv` ✅
    - [ ] B. only `-v`
    - [ ] C. normal and above
    - [ ] D. `-q` and above

    **Why:** any level ≥ the message's level prints it. **Ref:**
    [Console verbosity](https://symfony.com/doc/8.0/console/verbosity.html).

## Key takeaways

- Flags: `-q` (quiet), *(none)* normal, `-v`, `-vv`, `-vvv` (debug).
- Constants: 16/32/64/128/256 on `OutputInterface`.
- Guard with `isVerbose()`/`isVeryVerbose()`/`isDebug()` or tag messages by level.
- Verbosity is an **output** property; `-q` silences output, not execution.

## Last-minute revision

!!! tip "Cheat sheet"
    - `-v`→VERBOSE(64), `-vv`→VERY_VERBOSE(128), `-vvv`→DEBUG(256), `-q`→QUIET(16).
    - `writeln($msg, OutputInterface::VERBOSITY_VERBOSE)`.
    - `$output->isVerbose()`, `isVeryVerbose()`, `isDebug()`, `isQuiet()`.
    - `-vvv` also prints full exception traces.

## Connections

- **Depends on:** [Input & output](input-output.md) — verbosity is a property of
  `OutputInterface`, the same object you write through.
- **Reused in:** [Built-in commands](built-in-commands.md) — `-v/-vv/-vvv/-q` are
  global options every command inherits.
- **Confused with:** [Input & output](input-output.md) — verbosity toggles *how much*
  to print, not machine formats (use `--format`/STDOUT for data).

## Official References
- [Official Symfony docs — Console verbosity](https://symfony.com/doc/8.0/console/verbosity.html)
- [Symfony source — OutputInterface](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Console/Output/OutputInterface.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony console" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/console/verbosity.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** verbosity exists (tune diagnostics without changing behaviour)
- [ ] gate output with `isVerbose()`/`isDebug()` or per-message masks in Symfony 8
- [ ] debug output that vanishes under `-q` or never shows without `-v`
- [ ] spot the trick on the 16/32/64/128/256 constants and input-vs-output placement
- [ ] explain how `write()` compares the level and why higher shows lower-tagged lines

---

<small>Related: [Input & output](input-output.md) · [Events](events.md) · [Built-in commands](built-in-commands.md)</small>

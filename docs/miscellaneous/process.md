# Process Component

!!! tip "In a nutshell"
    Process runs OS commands in sub-processes cleanly across platforms. Build it
    with an array of arguments so each is auto-escaped, then `run()` (blocking)
    or `start()`/`wait()` (async). Exam gold: `fromShellCommandline()` is NOT
    escaped (injection risk), and the default timeout is 60 seconds.

!!! example "Real-world analogy"
    Process is **handing an errand to an assistant**. Writing the command as an
    array puts **each word in its own labelled bag** (auto-escaped, nothing
    mis-read) — versus barking one shell string they might misinterpret
    (`fromShellCommandline`). They either go do it while you wait (`run()`) or set
    off while you keep working and check back later (`start()`/`wait()`), then
    report what they said (stdout) and whether it went fine (exit code).

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Run a subprocess with `Process` and read output/exit code.
    - [ ] Choose between `run()` and `start()`/`wait()` and stream output.
    - [ ] Set timeouts and handle `ProcessFailedException`; avoid shell pitfalls.

    **Syllabus:** `Miscellaneous → Process` ·
    **Level:** Advanced ·
    **Est. time:** 30 min ·
    **Prerequisites:** [Console](../console/index.md)

    **Examen Symfony 8 :** OUI

---

## Pour les nuls

### L'idée en une phrase
Construis toujours une commande shell avec un tableau d'arguments — chaque élément est automatiquement échappé, ce qu'une simple chaîne shell n'offre jamais.

### Imagine dans la vraie vie
Process, c'est **confier une course à un assistant**. Écrire la commande sous forme de tableau met **chaque mot dans son propre sac étiqueté** (auto-échappé, rien de mal interprété) — contre aboyer une seule chaîne shell qu'il pourrait mal interpréter.

### Dans Symfony
```php
new Process(['ls', '-la', $dossierUtilisateur]); // sûr même si $dossierUtilisateur contient des espaces ou `;`
```

### Exemple simple
```php
$process = new Process(['git', 'log', '--oneline']);
$process->run();
echo $process->getOutput();
```

### Comment le mémoriser 🧠
`fromShellCommandline()` n'échappe **rien** — c'est un risque d'injection de commande si tu y insères une valeur utilisateur. Préfère toujours le constructeur avec un tableau d'arguments.

---

## Theory

The Process component runs OS commands in sub-processes cleanly across platforms.
Construct `Symfony\Component\Process\Process` with an **array of arguments**
(each auto-escaped), then run synchronously or asynchronously and inspect the
exit code, stdout and stderr.

```php
use Symfony\Component\Process\Process;

$process = new Process(['ls', '-la']); // array form: each argument auto-escaped
$process->run();                       // blocking; returns the exit code

$process->isSuccessful();              // true when exit code === 0
$process->getOutput();                 // stdout
$process->getErrorOutput();            // stderr
```

## Deep Dive — how it works internally

!!! question "Predict first"
    `Process::fromShellCommandline("git log $userInput")` runs with attacker-set
    `$userInput`. What's the risk, and would `new Process(['git', 'log', $userInput])`
    behave the same?

??? note "Reveal"
    The shell form is **command injection** — it runs through `/bin/sh` unescaped.
    The array form auto-escapes each element, so `$userInput` becomes a single
    literal argument, not shell syntax. Prefer the array constructor for any
    untrusted input.

### Two ways to construct

- `new Process(['git', 'log', '--oneline'])` — the array form. Each element is a
  separate, **automatically escaped** argument. Prefer this.
- `Process::fromShellCommandline('echo "$FOO"')` — a raw shell string run through
  `/bin/sh`. It supports shell features (pipes, redirections, variable
  expansion) but you are responsible for escaping — **command-injection risk** if
  you interpolate untrusted input.

```php
// Array form — auto-escaped, safe with untrusted input
$safe = new Process(['git', 'log', $userInput]); // $userInput = one literal argument

// Shell string — runs through /bin/sh, NOT escaped (pipes work, injection risk)
$shell = Process::fromShellCommandline('git log | head -n 5');
```

### Sync vs async

- `run(?callable $callback = null): int` — starts and **blocks** until the
  process ends, returning the exit code. An optional callback receives streamed
  output chunks.
- `start(?callable $callback = null): void` then `wait()` — starts the process
  **non-blocking**; do other work and `wait()` (or poll `isRunning()`) later.
- `mustRun()` — like `run()` but throws
  `Symfony\Component\Process\Exception\ProcessFailedException` on a non-zero exit.

```php
// Blocking: run() returns the exit code once the process ends
$exitCode = $process->run();

// Non-blocking: start(), keep working, then wait() (or poll isRunning())
$process->start();
while ($process->isRunning()) {
    // ... do other work ...
}
$process->wait();

// mustRun(): like run() but throws ProcessFailedException on non-zero exit
$other = new Process(['pg_dump', 'app']);
$other->mustRun();
```

```mermaid
sequenceDiagram
    participant App
    participant P as Process
    participant OS
    App->>P: start()
    P->>OS: fork/exec
    App->>App: do other work
    App->>P: wait() / getIterator()
    OS-->>P: stdout/stderr + exit code
    P-->>App: output, exit code
```

### Reading output

`getOutput()` / `getErrorOutput()` return the full buffers; `getIncrementalOutput()`
returns only new data since the last call. `getIterator()` streams output chunks
lazily (great for long-running commands / large output without buffering it all
in memory). `getExitCode()` returns the code; `isSuccessful()` is `code === 0`.

```php
$process->getOutput();            // full stdout buffer
$process->getErrorOutput();       // full stderr buffer
$process->getIncrementalOutput(); // only what is new since the last call
$process->getExitCode();          // int (null while still running)
$process->isSuccessful();         // exit code === 0

foreach ($process->getIterator() as $type => $chunk) {
    echo $chunk;                  // streamed lazily, no full buffering
}
```

### Timeouts

`setTimeout(float $seconds)` limits total runtime; `setIdleTimeout()` limits time
without output. Exceeding either throws
`Symfony\Component\Process\Exception\ProcessTimedOutException`. **You must call
`checkTimeout()` periodically** in an async loop, or use `wait()`/`run()` which
check for you. Default timeout is 60 s; `setTimeout(null)` disables it.

```php
$process->setTimeout(120);     // max total runtime in seconds (default 60)
$process->setIdleTimeout(10);  // max seconds without any new output
// $process->setTimeout(null); // disables the timeout entirely

$process->start();
while ($process->isRunning()) {
    $process->checkTimeout();  // throws ProcessTimedOutException when exceeded
    usleep(100_000);
}
```

!!! note "Source reference"
    `Symfony\Component\Process\Process` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Process/Process.php).

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Service;

    use Symfony\Component\Process\Exception\ProcessFailedException;
    use Symfony\Component\Process\Process;

    final class Backup
    {
        public function dump(string $target): string
        {
            $process = new Process(['pg_dump', '--file', $target, 'app']);
            $process->setTimeout(120);
            $process->run();

            if (!$process->isSuccessful()) {
                throw new ProcessFailedException($process);
            }

            return $process->getOutput();
        }
    }
    ```

=== "Console"

    ```console
    $ php bin/console app:backup   # a command wrapping the Process above
    ```

=== "YAML"

    ```yaml
    # No YAML config: Process is instantiated in code, not a service you configure.
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Use the **array** constructor (auto-escaping) | Building shell strings from user input |
| Set an explicit `setTimeout()` | Relying on the 60 s default silently |
| Stream with `getIterator()` for large output | Buffering gigabytes with `getOutput()` |
| Use `mustRun()`/`ProcessFailedException` for control flow | Ignoring non-zero exit codes |

## When (not) to use it / alternatives

Use Process for CLI tools you must shell out to (image processing, git, dumps).
For work that should be deferred/retried, dispatch a
[Messenger](../messenger/index.md) message instead of blocking the request. Never use
`fromShellCommandline` with untrusted input.

!!! danger "Certification traps"
    - Array args are **auto-escaped**; `fromShellCommandline` is **not** — injection risk.
    - `run()` blocks; `start()` returns immediately and needs `wait()`.
    - Default timeout is **60 seconds**; `null` disables it.
    - `mustRun()` throws `ProcessFailedException` on failure; `run()` returns the code.
    - In async loops you must call `checkTimeout()` yourself.

!!! warning "Common mistakes"
    - Passing a whole command as one array element (`['git log']`) instead of `['git', 'log']`.
    - Forgetting that `getOutput()` buffers everything in memory.

## Exercises

1. **(Advanced)** Run `pg_dump` with a 120 s timeout and throw on failure.
2. **(Advanced)** Stream a long-running command's output line-by-line without
   buffering it all.

??? success "Solutions"

    **1.** See `Backup::dump()` above.

    **2.**
    ```php
    <?php
    declare(strict_types=1);

    use Symfony\Component\Process\Process;

    $p = new Process(['tail', '-f', '/var/log/app.log']);
    $p->setTimeout(null);
    $p->start();
    foreach ($p as $type => $chunk) {
        echo $chunk; // streamed as it arrives
    }
    ```

## Certification questions

*Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.*

??? question "Q1. Which constructor auto-escapes each argument?"
    - [x] A. `new Process(['ls', '-la'])` ✅
    - [ ] B. `Process::fromShellCommandline('ls -la')`
    - [ ] C. both equally

    **Why:** The array form escapes each element; the shell form does not.
    **Ref:** [Process](https://symfony.com/doc/8.0/components/process.html).

??? question "Q2. What does `run()` return?"
    - [x] A. The process exit code ✅
    - [ ] B. The stdout string
    - [ ] C. `void`

    **Why:** `run()` returns the integer exit code; use `getOutput()` for stdout.
    **Ref:** [Process](https://symfony.com/doc/8.0/components/process.html#usage).

??? question "Q3. The default process timeout is…"
    - [x] A. 60 seconds ✅
    - [ ] B. unlimited
    - [ ] C. 30 seconds

    **Why:** The default is 60 s; pass `null` to disable. **Ref:** [Process timeout](https://symfony.com/doc/8.0/components/process.html#process-timeout).

## Key takeaways

- Prefer the array constructor (auto-escaped) over `fromShellCommandline`.
- `run()` blocks; `start()`+`wait()` is async; `mustRun()` throws on failure.
- Read via `getOutput()`, `getIncrementalOutput()`, or stream with `getIterator()`.
- Default 60 s timeout; `ProcessTimedOutException` / `ProcessFailedException`.

## Last-minute revision

!!! tip "Cheat sheet"
    - `new Process([...])` vs `Process::fromShellCommandline('...')` (unsafe with input).
    - `run(): int`, `start()`/`wait()`, `mustRun()`.
    - `getOutput()`, `getErrorOutput()`, `getExitCode()`, `isSuccessful()`, `getIterator()`.
    - `setTimeout(120)` / `setIdleTimeout()` / default 60 s.

## Connections

- **Depends on:** [Console](../console/index.md) — commands frequently wrap `Process` to shell out.
- **Reused in:** [Messenger](../messenger/index.md) — defer/retry long shell work as a message; [Filesystem & Finder](filesystem-finder.md) discovers the files you process.
- **Confused with:** running work inline — for deferrable/retriable jobs, dispatch a message instead of blocking the request.

## Official References
- [Official docs — Process](https://symfony.com/doc/8.0/components/process.html)
- [Symfony source — Process](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Process/Process.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony components" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/components/process.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** the array constructor is safer than `fromShellCommandline`
- [ ] run sync/async processes and read output/exit code in Symfony 8
- [ ] debug a hung/killed process (default 60 s timeout, missing `checkTimeout()`)
- [ ] spot the trick: array args auto-escape, shell strings don't; default timeout 60 s
- [ ] describe `run()` vs `start()`/`wait()` and streaming with `getIterator()`

---

<small>Related: [Console](../console/index.md) · [Messenger](../messenger/index.md) · [Lock](../appendices/out-of-syllabus/lock.md)</small>

# Console Events

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Name the four `ConsoleEvents` and their firing order
    - [ ] Listen with `#[AsEventListener]` and change the exit code
    - [ ] Handle OS signals via `SignalableCommandInterface` or the SIGNAL event
    - [ ] Explain how exit codes propagate through `TERMINATE`

    **Syllabus:** `Console → Events` ·
    **Level:** Advanced ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Custom commands](custom-commands.md)

---

## Theory

When commands run inside the framework, the `Application` dispatches events on the
event dispatcher. `Symfony\Component\Console\ConsoleEvents` defines four:

| Constant | Event name | When |
|---|---|---|
| `ConsoleEvents::COMMAND` | `console.command` | Before the command executes |
| `ConsoleEvents::SIGNAL` | `console.signal` | An OS signal was received |
| `ConsoleEvents::ERROR` | `console.error` | An exception/error was thrown |
| `ConsoleEvents::TERMINATE` | `console.terminate` | After the command, always |

Each carries a dedicated event object exposing the command, input, output and — for
error/terminate — the exit code.

## Deep Dive — how it works internally

`Symfony\Bundle\FrameworkBundle\Console\Application` (via
`Symfony\Component\Console\Application::doRunCommand()`) orchestrates the flow:

```mermaid
flowchart TD
    A["COMMAND (ConsoleCommandEvent)"] --> B{disabled?}
    B -- yes --> Z["exit 113 (RETURN_CODE_DISABLED)"]
    B -- no --> C["Command::run() -> execute()"]
    C -- throws --> E["ERROR (ConsoleErrorEvent)"]
    C -- returns int --> T
    E --> T["TERMINATE (ConsoleTerminateEvent)"]
    T --> X["process exit code"]
```

- **`ConsoleCommandEvent`** — inspect/prepare; `disableCommand()` skips execution and
  makes the run return `ConsoleCommandEvent::RETURN_CODE_DISABLED` (**113**).
- **`ConsoleErrorEvent`** — fired on any `\Throwable`; a listener can replace the
  throwable or set a custom exit code with `setExitCode()`. After it, `TERMINATE`
  still runs.
- **`ConsoleTerminateEvent`** — always runs (success or failure); `getExitCode()` /
  `setExitCode()` give the **last chance** to change the process exit code. Ideal for
  cleanup/metrics.
- **`ConsoleSignalEvent`** — fired when a subscribed POSIX signal arrives; exposes
  `getHandlingSignal()` and can `setExitCode()` / `abortExit()`.

Exit codes are clamped to **0–255** (`$code % 256` when out of range); a negative or
`>255` return is normalised. By convention a signal-terminated process exits with
`128 + signalNumber`.

### Signal handling

Two ways to react to signals (needs `ext-pcntl`):

1. **`Symfony\Component\Console\Command\SignalableCommandInterface`** — implement
   `getSubscribedSignals(): array` (e.g. `[\SIGINT, \SIGTERM]`) and
   `handleSignal(int $signal, int|false $previousExitCode = 0): int|false`. Return an
   int to set the exit code, or `false` to continue.
2. **`ConsoleEvents::SIGNAL`** listener — a global hook, useful for cross-cutting
   concerns (flush logs on `SIGTERM`).

!!! note "Source reference"
    `ConsoleEvents`, `ConsoleTerminateEvent`, `SignalableCommandInterface` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Console/ConsoleEvents.php).

## Configuration & code

=== "Listener (#[AsEventListener])"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Console;

    use Symfony\Component\Console\ConsoleEvents;
    use Symfony\Component\Console\Event\ConsoleTerminateEvent;
    use Symfony\Component\EventDispatcher\Attribute\AsEventListener;

    #[AsEventListener(event: ConsoleEvents::TERMINATE)]
    final class ExitCodeAuditor
    {
        public function __invoke(ConsoleTerminateEvent $event): void
        {
            if (0 !== $event->getExitCode()) {
                // e.g. record the failure; could also setExitCode()
                $event->getOutput()->writeln(
                    sprintf('<comment>%s exited %d</comment>',
                        $event->getCommand()?->getName(),
                        $event->getExitCode(),
                    ),
                );
            }
        }
    }
    ```

=== "SignalableCommandInterface"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Command;

    use Symfony\Component\Console\Attribute\AsCommand;
    use Symfony\Component\Console\Command\Command;
    use Symfony\Component\Console\Command\SignalableCommandInterface;
    use Symfony\Component\Console\Input\InputInterface;
    use Symfony\Component\Console\Output\OutputInterface;

    #[AsCommand(name: 'app:worker')]
    final class WorkerCommand extends Command implements SignalableCommandInterface
    {
        private bool $stop = false;

        public function getSubscribedSignals(): array
        {
            return [\SIGINT, \SIGTERM];
        }

        public function handleSignal(int $signal, int|false $previousExitCode = 0): int|false
        {
            $this->stop = true;

            return 0; // graceful exit code
        }

        protected function execute(InputInterface $input, OutputInterface $output): int
        {
            while (!$this->stop) {
                // process one job
            }

            return Command::SUCCESS;
        }
    }
    ```

=== "Console"

    ```console
    $ php bin/console app:worker      # Ctrl-C sends SIGINT -> handleSignal()
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Use `TERMINATE` for cleanup/metrics | Cleanup only inside `execute()` (skipped on error) |
| Handle `SIGTERM` for graceful worker shutdown | Ignoring signals in long-running loops |
| Set exit codes via the event when needed | Calling `exit()` directly in a listener |
| Return `Command::FAILURE` for real failures | Swallowing exceptions silently |

## When (not) to use it / alternatives

Events are only dispatched when running through the **framework Application** (they
require an event dispatcher). A standalone Console app without a dispatcher will not
fire them. Prefer `SignalableCommandInterface` for command-specific signal logic;
use the `SIGNAL` event for app-wide concerns.

!!! danger "Certification traps"
    - Firing order: **COMMAND → (ERROR on throw) → TERMINATE**. `TERMINATE` **always**
      runs.
    - `disableCommand()` yields exit code **113** (`RETURN_CODE_DISABLED`).
    - Exit codes are clamped to **0–255**; `>255` wraps via `% 256`.
    - `ConsoleErrorEvent::setExitCode()` overrides the failure code, but `TERMINATE`
      still runs afterwards.
    - Signal handling needs the **pcntl** extension.

!!! warning "Common mistakes"
    - Assuming events fire for the raw Console component without a dispatcher.
    - Expecting `handleSignal()` without `ext-pcntl` installed.

## Exercises

1. **(Basic)** Write a `TERMINATE` listener that logs the command name and exit code.
2. **(Intermediate)** Make a long-running command stop gracefully on `SIGTERM` using
   `SignalableCommandInterface`.

??? success "Solutions"

    **1.** See the `ExitCodeAuditor` listener above — attach it with
    `#[AsEventListener(event: ConsoleEvents::TERMINATE)]`.

    **2.** Implement `getSubscribedSignals(): [\SIGTERM]` and set a `$stop` flag in
    `handleSignal()`, then break the loop in `execute()` (see `WorkerCommand`).

## Certification questions

??? question "Q1. What is the correct dispatch order for a successful command?"
    - [x] A. `COMMAND` then `TERMINATE` ✅
    - [ ] B. `TERMINATE` then `COMMAND`
    - [ ] C. `ERROR` then `COMMAND`
    - [ ] D. `COMMAND` then `ERROR`

    **Why:** `ERROR` only fires on a throwable; `TERMINATE` always fires last.
    **Ref:** [Console events](https://symfony.com/doc/current/components/console/events.html).

??? question "Q2. Which event lets you change the exit code no matter what happened?"
    - [ ] A. `ConsoleEvents::COMMAND`
    - [ ] B. `ConsoleEvents::SIGNAL`
    - [x] C. `ConsoleEvents::TERMINATE` ✅
    - [ ] D. It cannot be changed after execution

    **Why:** `ConsoleTerminateEvent::setExitCode()` is the last chance. **Ref:**
    [Console events](https://symfony.com/doc/current/components/console/events.html).

??? question "Q3. What exit code results from `ConsoleCommandEvent::disableCommand()`?"
    - [ ] A. 0
    - [ ] B. 1
    - [x] C. 113 ✅
    - [ ] D. 255

    **Why:** `RETURN_CODE_DISABLED` is 113. **Ref:**
    [Console events](https://symfony.com/doc/current/components/console/events.html).

??? question "Q4. Which interface lets a command react to `SIGTERM`?"
    - [x] A. `SignalableCommandInterface` ✅
    - [ ] B. `SignalHandlerInterface`
    - [ ] C. `TerminableInterface`
    - [ ] D. `EventSubscriberInterface`

    **Why:** implement `getSubscribedSignals()` and `handleSignal()`. **Ref:**
    [Console signals](https://symfony.com/doc/current/components/console/events.html#handling-command-signals).

## Key takeaways

- Four events: `COMMAND`, `SIGNAL`, `ERROR`, `TERMINATE`.
- Order: `COMMAND → [ERROR] → TERMINATE`; `TERMINATE` always runs.
- `disableCommand()` → exit **113**; exit codes clamp to 0–255.
- Signals via `SignalableCommandInterface` or the `SIGNAL` event (needs pcntl).

## Last-minute revision

!!! tip "Cheat sheet"
    - `ConsoleEvents::COMMAND|SIGNAL|ERROR|TERMINATE`.
    - Events fire only with a dispatcher (framework Application).
    - `getSubscribedSignals()` + `handleSignal($sig, $prevExit)`.
    - Signal-terminated convention: exit `128 + signal`.

## References

- [Official Symfony docs — Console events](https://symfony.com/doc/current/components/console/events.html)
- [Official Symfony docs — Handling signals](https://symfony.com/doc/current/components/console/events.html#handling-command-signals)
- [Symfony source — ConsoleEvents](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Console/ConsoleEvents.php)

---

<small>Related: [Custom commands](custom-commands.md) · [Verbosity](verbosity.md) · [Configuration](configuration.md)</small>

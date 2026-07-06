# Revision Sheet — Console

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Console](../../console/index.md).

## Built-in Commands & the Application
- `list` (default), `help`, `about`, `completion` exist in every application.
- FrameworkBundle adds `cache:clear`, `cache:warmup`, `debug:*`.
- `make:*` is the **MakerBundle**, not core.
- `bin/console` boots the kernel and `Application` through the Runtime component.

**Cheat:** Default command = `list`. Help = `help <cmd>` or `<cmd> --help`. Core: `list`, `help`, `about`, `completion`. Framework: `cache:clear`, `cache:warmup`, `debug:container|router|autowiring|config|event-dispatcher`. `Application` = `Symfony\Component\Console\Application`; framework subclass boots the kernel.

## Command Configuration
- Metadata: name, description, help, aliases, hidden — set via attribute or setters.
- Lifecycle: **configure → initialize → interact → execute** (validate between the
  last two).
- `configure()` runs in the constructor — no input yet.
- The name belongs in `#[AsCommand]` to keep loading lazy.

**Cheat:** `configure()` = constructor-time structure only. `initialize()` = shared setup after binding. `interact()` = prompt for missing values, interactive only. `execute()` = returns `int`. `hidden` hides from `list`, still runnable.

## Custom Commands
- `#[AsCommand]` declares name/description/aliases/hidden/help.
- Invokable commands (`__invoke`) are the modern default; classic `extends Command`
  still works.
- Return `Command::SUCCESS` (0), `FAILURE` (1), or `INVALID` (2).
- Autoconfiguration tags commands `console.command`; loading is lazy.

**Cheat:** `Symfony\Component\Console\Attribute\AsCommand`. Invokable attrs: `#[Argument]`, `#[Option]` from `...Console\Attribute`. `SUCCESS=0`, `FAILURE=1`, `INVALID=2`. Tag `console.command` is applied automatically.

## Console Events
- Four events: `COMMAND`, `SIGNAL`, `ERROR`, `TERMINATE`.
- Order: `COMMAND → [ERROR] → TERMINATE`; `TERMINATE` always runs.
- `disableCommand()` → exit **113**; exit codes clamp to 0–255.
- Signals via `SignalableCommandInterface` or the `SIGNAL` event (needs pcntl).

**Cheat:** `ConsoleEvents::COMMAND|SIGNAL|ERROR|TERMINATE`. Events fire only with a dispatcher (framework Application). `getSubscribedSignals()` + `handleSignal($sig, $prevExit)`. Signal-terminated convention: exit `128 + signal`.

## Console Helpers
- Helpers come from the `HelperSet`; fetch by name with `getHelper()`.
- `QuestionHelper`: `Question`, `ConfirmationQuestion`, `ChoiceQuestion`; hidden for
  secrets.
- `ProgressBar` and `Table` render progress/data; throttle redraws for scale.
- `Cursor` is the low-level primitive; `SymfonyStyle` covers most needs.

**Cheat:** `getHelper('question'|'formatter'|'process')`. `ask`/`askHidden`/`confirm`/`choice` via `SymfonyStyle`. `ProgressBar`: `start($max)`, `advance()`, `finish()`. `Table`: `setHeaders()`, `setRows()`, `render()`.

## Input & Output
- Read via `InputInterface`, write via `OutputInterface`.
- `SymfonyStyle(input, output)` is the go-to styled UI (title/table/progress/ask).
- STDERR is `ConsoleOutputInterface::getErrorOutput()` — keep piped data on STDOUT.
- Output **sections** allow live, independent re-writes.

**Cheat:** `new SymfonyStyle($input, $output)`. `title/section/text/listing/table/progressBar/ask/confirm/choice`. `write()` no newline, `writeln()` newline. STDERR: `$output->getErrorOutput()` (ConsoleOutputInterface only).

## Arguments & Options
- Arguments are positional; options are named with optional `-x` shortcuts.
- Argument modes: `REQUIRED=1`, `OPTIONAL=2`, `IS_ARRAY=4`.
- Option modes: `VALUE_NONE=1`, `REQUIRED=2`, `OPTIONAL=4`, `IS_ARRAY=8`,
  `NEGATABLE=16`.
- The `InputDefinition` binds and validates; `VALUE_NONE` has no default.

**Cheat:** `addArgument(name, mode, desc, default)`. `addOption(name, shortcut, mode, desc, default)`. Array argument = last; only one. Read via `$input->getArgument()` / `$input->getOption()`.

## Verbosity Levels
- Flags: `-q` (quiet), *(none)* normal, `-v`, `-vv`, `-vvv` (debug).
- Constants: 16/32/64/128/256 on `OutputInterface`.
- Guard with `isVerbose()`/`isVeryVerbose()`/`isDebug()` or tag messages by level.
- Verbosity is an **output** property; `-q` silences output, not execution.

**Cheat:** `-v`→VERBOSE(64), `-vv`→VERY_VERBOSE(128), `-vvv`→DEBUG(256), `-q`→QUIET(16). `writeln($msg, OutputInterface::VERBOSITY_VERBOSE)`. `$output->isVerbose()`, `isVeryVerbose()`, `isDebug()`, `isQuiet()`. `-vvv` also prints full exception traces.

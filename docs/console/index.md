# Console

The **Console** component turns a PHP class into a first-class command-line
application. In a Symfony app every `php bin/console …` invocation runs through it:
it parses the input, resolves a `Command`, drives the
**configure → initialize → interact → execute** lifecycle, dispatches console
events, and returns a Unix exit code. It is mostly self-contained, but it leans on
the [service container](../dependency-injection/index.md) for command registration
and lazy loading, which is why it sits after DI in the roadmap.

!!! info "Stage at a glance"
    | Property | Value |
    |---|---|
    | **Prerequisites** | [Dependency Injection](../dependency-injection/index.md) |
    | **Level** | Advanced |
    | **Difficulty** | ★☆☆ |
    | **Dependencies** | Stage 4 (autoconfiguration, tags, lazy services) |
    | **Revision priority** | Medium |
    | **Est. time** | 2–3 h |

## Why this stage matters

CLI tooling is where cron jobs, workers, migrations and maintenance scripts live.
The exam tests the *mechanics*: which return constant means success, how option
modes differ, what order lifecycle methods fire in, and which verbosity constant
maps to `-vv`. These are precise, memorisable facts — cheap points if you drill
them, easy to lose if you guess.

Modern Symfony 8 favours **invokable commands** (`#[AsCommand]` on a class with an
`__invoke()` method and `#[Argument]` / `#[Option]` parameters) alongside the
classic `extends Command` style. Both compile to the same `Command` object and the
same lifecycle, so you must recognise either form.

## Micro-chapters

Work through them in order:

- [ ] [Built-in commands & the Application](built-in-commands.md) — `about`,
  `list`, `help`, `cache:clear`, `debug:*`, how `bin/console` boots the
  `Application`.
- [ ] [Custom commands](custom-commands.md) — `#[AsCommand]`, extending `Command`,
  invokable style, `SUCCESS`/`FAILURE`/`INVALID`, autoconfiguration.
- [ ] [Command configuration](configuration.md) — name, description, help,
  aliases, hidden; `configure()` vs attribute; lazy loading.
- [ ] [Arguments & options](options-arguments.md) — `InputArgument` /
  `InputOption` modes, shortcuts, defaults, negatable flags.
- [ ] [Input & output](input-output.md) — `InputInterface`, `OutputInterface`,
  `SymfonyStyle`, output sections, STDERR.
- [ ] [Helpers](helpers.md) — `QuestionHelper`, `ProgressBar`, `Table`,
  `FormatterHelper`, `Cursor`, the `HelperSet`.
- [ ] [Console events](events.md) — `ConsoleEvents::COMMAND` / `SIGNAL` / `ERROR`
  / `TERMINATE`, listeners, exit codes, signal handling.
- [ ] [Verbosity levels](verbosity.md) — `-q`/`-v`/`-vv`/`-vvv`, the
  `VERBOSITY_*` constants, `isVerbose()` and friends.

## How to study it

1. Get oriented with [built-in commands](built-in-commands.md) and how the
   `Application` runs.
2. Write your own with [custom commands](custom-commands.md) and
   [configuration](configuration.md).
3. Master the input contract: [arguments & options](options-arguments.md).
4. Master the output contract: [input & output](input-output.md) and
   [helpers](helpers.md).
5. Finish with the cross-cutting mechanics: [events](events.md) and
   [verbosity](verbosity.md).

---

<small>Related: [Dependency Injection](../dependency-injection/index.md) ·
[Symfony Architecture](../architecture/index.md) ·
[Automated Tests](../testing/index.md)</small>

## Official References

- [Symfony documentation — Console](https://symfony.com/doc/current/console.html)
- [Symfony documentation home](https://symfony.com/doc/current/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)

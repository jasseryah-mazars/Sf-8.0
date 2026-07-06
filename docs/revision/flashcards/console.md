# Flashcards — Console

32 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. Which command runs when you execute `php bin/console` with no arguments?"
    **✅ list**

    The Application's default command is `list`, which prints all available commands grouped by namespace.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

??? question "2. Which command is provided by an optional bundle (MakerBundle), not by Symfony core?"
    **✅ make:command**

    `make:*` generators ship with the optional symfony/maker-bundle dev dependency; `cache:clear`, `debug:router` and `about` are core/framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/SymfonyMakerBundle/index.html)

??? question "3. How does `bin/console` obtain the console Application in Symfony 8?"
    **✅ It returns a closure that the Runtime component executes to build the kernel and Application**

    bin/console requires vendor/autoload_runtime.php and returns a closure; the Runtime component runs it to build the Kernel and FrameworkBundle Application.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

??? question "4. What does `php bin/console ca:cl` do when the abbreviation is unambiguous?"
    **✅ Runs cache:clear via command-name abbreviation**

    Application::find() resolves unambiguous abbreviations to the full command name.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

??? question "5. What integer value does `Command::INVALID` represent?"
    **✅ 2**

    The return constants are SUCCESS=0, FAILURE=1, INVALID=2.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

??? question "6. In Symfony 8, what does an invokable command class require?"
    **✅ The #[AsCommand] attribute and an __invoke() method returning int**

    Invokable commands only need #[AsCommand] plus an __invoke() method; they do not extend Command, though they still use its SUCCESS/FAILURE constants.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

??? question "7. How is a command normally registered in the service container?"
    **✅ Autoconfiguration tags #[AsCommand]/Command subclasses with 'console.command'**

    Autoconfiguration applies the console.command tag; a compiler pass builds a ContainerCommandLoader mapping name to service id for lazy loading.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/commands_as_services.html)

??? question "8. What must a command's execute()/__invoke() return in Symfony 8?"
    **✅ An int exit code**

    The returned int becomes the process exit code; returning void is invalid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

??? question "9. What is the correct command lifecycle order?"
    **✅ configure → initialize → interact → execute**

    configure() runs in the constructor; then run() calls initialize(), interact() (if interactive), input validation, and finally execute().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

??? question "10. When is interact() called?"
    **✅ Only when the input is interactive**

    interact() is skipped for non-interactive input (e.g. -n / --no-interaction).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

??? question "11. Why declare the command name in #[AsCommand] rather than only in configure()?"
    **✅ It lets the command loader know the name without instantiating the class (lazy loading)**

    The attribute exposes name/aliases at compile time so ContainerCommandLoader maps name→id and instantiates the command only when invoked.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/commands_as_services.html)

??? question "12. A command declared with hidden: true …"
    **✅ Does not appear in `list` but can still be executed**

    The hidden flag only affects listing; the command remains runnable by name.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

??? question "13. Which mode declares a valueless boolean flag option?"
    **✅ InputOption::VALUE_NONE**

    VALUE_NONE takes no value; the option is false unless present, then true. It cannot have a default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/input.html)

??? question "14. What is the integer value of InputOption::VALUE_IS_ARRAY?"
    **✅ 8**

    Option modes are VALUE_NONE=1, VALUE_REQUIRED=2, VALUE_OPTIONAL=4, VALUE_IS_ARRAY=8, VALUE_NEGATABLE=16.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/input.html)

??? question "15. Which statement about an IS_ARRAY argument is correct?"
    **✅ There can be only one and it must be declared last**

    An array argument greedily consumes the remaining tokens, so only one is allowed and it must come last. It may be REQUIRED or OPTIONAL.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/input.html)

??? question "16. Which option mode adds a `--no-foo` counterpart to `--foo`?"
    **✅ InputOption::VALUE_NEGATABLE**

    VALUE_NEGATABLE (16) generates the --no- twin; the value is true, false, or its default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/input.html)

??? question "17. Which InputArgument mode value is OPTIONAL?"
    **✅ 2**

    Argument modes are REQUIRED=1, OPTIONAL=2, IS_ARRAY=4.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/input.html)

??? question "18. Which method returns the STDERR stream in a CLI command?"
    **✅ ConsoleOutputInterface::getErrorOutput()**

    The split-stream getErrorOutput() lives on ConsoleOutputInterface, not the base OutputInterface, so check the type first.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/verbosity.html)

??? question "19. Which two arguments does SymfonyStyle require?"
    **✅ An InputInterface and an OutputInterface**

    SymfonyStyle wraps both input (for prompts) and output (for styled writing).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/style.html)

??? question "20. What does $output->section() return?"
    **✅ A ConsoleSectionOutput that can be overwritten or cleared independently**

    Output sections are independently re-writable regions; require ConsoleOutputInterface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

??? question "21. How does a classic command obtain the QuestionHelper?"
    **✅ $this->getHelper('question')**

    Helpers are fetched by their string name from the command's HelperSet.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/helpers/questionhelper.html)

??? question "22. Which question class offers a fixed list of selectable answers?"
    **✅ ChoiceQuestion**

    ChoiceQuestion presents options and supports single or multi-select.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/helpers/questionhelper.html)

??? question "23. What does ProgressBar::setRedrawFrequency(100) do?"
    **✅ Redraws the bar only every 100 steps to reduce terminal I/O**

    Redraw throttling avoids expensive terminal writes on every micro-step.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/helpers/progressbar.html)

??? question "24. Which class moves or hides the terminal cursor?"
    **✅ Symfony\Component\Console\Cursor**

    Cursor issues ANSI escape sequences to move/hide/show the cursor and clear lines.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/helpers/index.html)

??? question "25. What is the dispatch order for a successful framework command?"
    **✅ COMMAND then TERMINATE**

    ERROR fires only on a thrown Throwable; TERMINATE always fires last, after COMMAND and execution.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/events.html)

??? question "26. Which event lets you change the exit code regardless of outcome?"
    **✅ ConsoleEvents::TERMINATE**

    ConsoleTerminateEvent::setExitCode() runs on every command and is the last chance to alter the exit code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/events.html)

??? question "27. What exit code results from ConsoleCommandEvent::disableCommand()?"
    **✅ 113**

    Disabling the command in the COMMAND event returns ConsoleCommandEvent::RETURN_CODE_DISABLED, which is 113.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/events.html)

??? question "28. Which interface lets a command react to OS signals such as SIGTERM?"
    **✅ SignalableCommandInterface**

    Implement getSubscribedSignals() and handleSignal(); requires the pcntl extension.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/events.html)

??? question "29. Which flag maps to VERBOSITY_VERY_VERBOSE?"
    **✅ -vv**

    -v is VERBOSE, -vv is VERY_VERBOSE, -vvv is DEBUG, -q is QUIET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/verbosity.html)

??? question "30. What is the integer value of VERBOSITY_NORMAL?"
    **✅ 32**

    QUIET=16, NORMAL=32, VERBOSE=64, VERY_VERBOSE=128, DEBUG=256.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/verbosity.html)

??? question "31. Where is the current verbosity level stored?"
    **✅ On the OutputInterface, set by the Application from the flags**

    The Application parses -v/-vv/-vvv/-q and calls $output->setVerbosity(); verbosity is a property of the output.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/verbosity.html)

??? question "32. A message written with VERBOSITY_VERBOSE is displayed at which levels?"
    **✅ -v, -vv and -vvv**

    A message prints when the current level is greater than or equal to the message's level, so VERBOSE (64) shows at -v, -vv and -vvv.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/verbosity.html)

---

<small>Back to [Flashcards](index.md) · [Console](../../console/index.md)</small>

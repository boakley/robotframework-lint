Welcome to Robot Framework Lint
===============================

Static analysis for robot framework plain text files.

This is a static analysis tool for robot framework plain text files.

Installation Instructions
-------------------------

The preferred method of installation is to use pip:

    $ pip install --upgrade robotframework-lint

This will install a package named "rflint", and an executable named "rflint"

Running the linter
------------------

To run, use the command "rflint", or use the `-m` option to python to
run the rflint module. Add one or more filenames as arguments, and
those files will be checked for rule violations.

Custom rules
------------

Rules are simple python classes. For more information about how to
write rules, see the
[robotframework-lint wiki](https://github.com/boakley/robotframework-lint/wiki)

Argument files
--------------

rflint supports argument files much in the same way as robot framework. You can
put arguments one per line in a file, and reference that file with the option
`-A` or `--argument-file`.

Argument files are a convenient way to create a set of rules and rule configurations
that you want to apply to your files.

Examples
--------

    $ rflint myTestSuite.robot

To see a list of all of the built-in rules, run the following command

    $ rflint --list

To see documentation, add the --verbose option:

    $ rflint --list --verbose

Some rules are configurable. For example, to configure the "LineTooLong"
rule to flag lines longer than 80 characters (the default is 100), you
can change the default value with the configure option:

    $ rflint --configure LineTooLong:80 myTestSuite.robot

You can disable any rule, or configure it to be a warning or error
with the options --warning, --error and --ignore. For example, to
ignore the LineTooLong rule you can do this:

    $ rflint --ignore LineTooLong myTestSuite.robot

To see a list of all command line options, use the `--help` option:

    $ python -m rflint --help

Example output:

    $ python -m rflint myTestSuite.robot
    + myTestSuite.robot
    W: 2, 0: No suite documentation (RequireSuiteDocumentation)
    E: 15, 0: No keyword documentation (RequireKeywordDocumentation)

This show a warning on line two, character 0, where there should be suite
documentation but isn't. It also shows an error on line 15, character 0,
where there should be keyword documentation but there isn't.

Acknowledgements
================

A huge thank-you to Echo Global Logistics (http://www.echo.com) for
supporting the development of this package.

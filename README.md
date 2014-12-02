Welcome to Robot Framework Lint
===============================

Linter for robot framework plain text files. 

This is a static analysis tool for robot framework plain text files. 

Installation Instructions
-------------------------

The preferred method of installation is to use pip:

    $ pip install robotframework-lint

This will install a package named "rflint".

Running the linter
------------------

To run, use the `-m` option to python, to run the rflint module. It takes one or
more .txt, .tsv or .robot files and will analyze each.

Example:

    $ python -m rflint myTestSuite.robot

To see a list of options, use the `--help` option:

    $ python -m rflint --help

Example output:

    $ python -m rflint myTestSuite.robot
    + myTestSuite.robot
    W: 2, 0: No suite documentation (RequireSuiteDocumentation)
    E: 15, 0: No keyword documentation (RequireKeywordDocumentation)
    

Acknowledgements
================
A huge thank-you to Echo Global Logistics (echo.com) for supporting the development of this package.

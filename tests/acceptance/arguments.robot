*** Settings ***
| Documentation
| ... | This suite includes tests for the command line arguments
| #
| Library    | OperatingSystem
| Library    | Process
| Library    | SharedKeywords.py
| Resource   | SharedKeywords.robot
| Force Tags | smoke
| #
| Test Teardown
| # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| No filenames
| | [Documentation]
| | ... | Verify that the --no-filenames supresses filenames
| |
| | Run rf-lint with the following options:
| | ... | --ignore  | all
| | ... | --warning | RequireSuiteDocumentation
| | ... | --no-filenames
| | ... | test_data/acceptance/nodoc.robot
| |
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | W: 1, 0: No suite documentation (RequireSuiteDocumentation)

| Default output includes filenames
| | [Documentation]
| | ... | Verify that the --no-filenames supresses filenames
| |
| | Run rf-lint with the following options:
| | ... | --ignore  | all
| | ... | --warning | RequireSuiteDocumentation
| | ... | test_data/acceptance/nodoc.robot
| |
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | + test_data/acceptance/nodoc.robot
| | ... | W: 1, 0: No suite documentation (RequireSuiteDocumentation)

| Same file twice should show filename twice
| | [Documentation]
| | ... | Verify that we print each filename that is processed
| | ... |
| | ... | If a filename is given on the command line twice, that
| | ... | filename should be printed twice.
| |
| | Run rf-lint with the following options:
| | ... | --ignore  | all
| | ... | --warning | RequireSuiteDocumentation
| | ... | test_data/acceptance/nodoc.robot
| | ... | test_data/acceptance/nodoc.robot
| |
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | + test_data/acceptance/nodoc.robot
| | ... | W: 1, 0: No suite documentation (RequireSuiteDocumentation)
| | ... | + test_data/acceptance/nodoc.robot
| | ... | W: 1, 0: No suite documentation (RequireSuiteDocumentation)

| Rulefile option
| | [Documentation]
| | ... | Verify that rules in a rulefile are listed
| |
| | Run rf-lint with the following options:
| | ... | --rulefile | test_data/acceptance/customRules.py
| | ... | --list
| | Stderr should be | ${EMPTY}
| | Output should contain
| | ... | W CustomTestRule
| | ... | W CustomSuiteRule
| | ... | W CustomGeneralRule
| | ... | W CustomKeywordRule

| The --describe option with one named rule
| | [Documentation]
| | ... | Verify that --describe works
| | Run rf-lint with the following options:
| | ... | --describe | RequireKeywordDocumentation
| | rflint return code should be | 0
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | RequireKeywordDocumentation
| | ... | ${SPACE*4}Verify that a keyword has documentation

| The --describe option with invalid rule name
| | [Documentation]
| | ... | Verify that rflint --describe fails if given unknown rule name
| | Run rf-lint with the following options:
| | ... | --describe | BogusRule
| | rflint return code should be | 1
| | Stderr should be |
| | ... | unknown rule: 'BogusRule'
| | Stdout should be | ${EMPTY}

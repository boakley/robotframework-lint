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
| ... | # provide some debugging information if things go bad
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



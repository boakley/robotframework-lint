*** Settings ***
| Documentation
| ... | Issue 41 - TooFewSteps failing when a statement contains a comment anywhere
| #
| Resource   | ../SharedKeywords.robot
| #
| Test Teardown
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Issue 41 - TooFewKeywordSteps 
| |     
| | [tags] | issue-41
| | [Documentation]
| | ... | Verify TooFewKeywordSteps works when every step has a comment
| |
| | Run rf-lint with the following options:
| | ... | --ignore | all
| | ... | --warning  | TooFewKeywordSteps
| | ... | --configure | TooFewKeywordSteps:1
| | ... | test_data/acceptance/issue-41.robot
| | 
| | rflint return code should be | 0
| | Stderr should be | ${EMPTY}
| | Stdout should be | ${EMPTY}

| Issue 41 - TooFewTestSteps 
| |     
| | [tags] | issue-41
| | [Documentation]
| | ... | Verify TooFewTestSteps works when every step has a comment
| |
| | Run rf-lint with the following options:
| | ... | --ignore | all
| | ... | --warning  | TooFewTestSteps
| | ... | --configure | TooFewTestSteps:1
| | ... | test_data/acceptance/issue-41.robot
| | 
| | rflint return code should be | 0
| | Stderr should be | ${EMPTY}
| | Stdout should be | ${EMPTY}

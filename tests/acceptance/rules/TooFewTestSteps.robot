*** Settings ***
| Documentation | Tests for the testcase rule 'TooFewTestSteps'
| Resource      | tests/acceptance/SharedKeywords.robot
| #
| Test Teardown
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify TooFewTestSteps default catches less than two steps
| | [Documentation]
| | ... | Verify that TooFewTestSteps raises errors with less than two steps
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooFewTestSteps
| | ... | test_data/acceptance/rules/TooFewTestSteps_Data.robot
| |
| | rflint return code should be | 2
| | rflint should report 2 errors
| | rflint should report 0 warnings

| Verify TooFewTestSteps configurability
| | [Documentation]
| | ... | Verify that TooFewTestSteps can be configured
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --configure | TooFewTestSteps:0
| | ... | --error  | TooFewTestSteps
| | ... | test_data/acceptance/rules/TooFewTestSteps_Data.robot
| |
| | rflint return code should be | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings


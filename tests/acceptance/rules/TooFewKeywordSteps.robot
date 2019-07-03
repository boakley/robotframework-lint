*** Settings ***
| Documentation | Tests for the testcase rule 'TooFewTestSteps'
| Resource      | ../SharedKeywords.robot
| 
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify TooFewKeywordSteps default catches less than two steps
| | [Documentation]
| | ... | Verify that TooFewKeywordSteps raises errors with less than two steps
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooFewKeywordSteps
| | ... | test_data/acceptance/rules/TooFewKeywordSteps_Data.robot
| |
| | rflint return code should be | 2
| | rflint should report 2 errors
| | rflint should report 0 warnings

| Verify TooFewKeywordSteps configurability
| | [Documentation]
| | ... | Verify that TooFewKeywordSteps can be configured
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --configure | TooFewKeywordSteps:0
| | ... | --error  | TooFewKeywordSteps
| | ... | test_data/acceptance/rules/TooFewKeywordSteps_Data.robot
| |
| | rflint return code should be | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings


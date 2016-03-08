*** Settings ***
| Documentation | Tests for the suite rule 'PeriodInSuiteName'
| Resource      | ../SharedKeywords.robot
| 
| Test Teardown
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Suite WITH a period in the name
| | [Documentation]
| | ... | Verify that a suite with a period in the name triggers the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | PeriodInSuiteName
| | ... | test_data/acceptance/rules/PeriodInSuiteName.foo.robot
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings

| Suite WITHOUT a period in the name
| | [Documentation]
| | ... | Verify that a suite without a period in the name does NOT trigger the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | PeriodInSuiteName
| | ... | ${SUITE SOURCE} | # use this file as input
| |
| | rflint return code should be | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings

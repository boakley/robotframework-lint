*** Settings ***
| Documentation | Tests for the suite rule 'DuplicateTestNames'
| Resource      | tests/acceptance/SharedKeywords.robot
| #
| Test Teardown 
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify all defined tests have unique names
| | [Documentation]
| | ... | Verify that all defined tests have unique names.
| | ... | If a test name is duplicated, the rule should flag
| | ... | the duplicates but not the original. 
| | 
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all 
| | ... | --error  | DuplicateTestNames
| | ... | test_data/acceptance/rules/DuplicateTestNames_Data.robot
| | 
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings

*** Settings ***
| Documentation | Tests for the suite rule 'DuplicateKeywordNames'
| Resource      | ../SharedKeywords.robot
|
| Test Teardown
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify all defined keywords have unique names
| | [Documentation]
| | ... | Verify that all defined keywords have unique names.
| | ... | If a keyword name is duplicated, the rule should flag
| | ... | the duplicates but not the original.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | DuplicateKeywordNames
| | ... | test_data/acceptance/rules/DuplicateKeywordNames_Data.robot
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings

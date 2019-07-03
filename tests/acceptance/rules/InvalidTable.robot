*** Settings ***
| Documentation | Tests for the rule 'InvalidTable'
| Resource      | ../SharedKeywords.robot
|
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify all invalid table names are detected
| | [Documentation]
| | ... | Verify that all invalid table names cause errors,
| | ... | and all valid names do not. Note: the test data
| | ... | is a collection of both valid and invalid names.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | InvalidTable
| | ... | test_data/acceptance/rules/InvalidTable_Data.robot
| |
| | rflint return code should be | 7
| | rflint should report 7 errors
| | rflint should report 0 warnings

| Verify that the proper error message is returned
| | [Documentation]
| | ... | Verify that InvalidTable returns the expected message
| | ... | for every error
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | InvalidTable
| | ... | test_data/acceptance/rules/InvalidTable_Data.robot
| |
| | Output should contain
| | ... | E: 6, 0: Unknown table name '' (InvalidTable)
| | ... | E: 7, 0: Unknown table name '' (InvalidTable)
| | ... | E: 8, 0: Unknown table name '' (InvalidTable)
| | ... | E: 9, 0: Unknown table name 'Testcase' (InvalidTable)
| | ... | E: 10, 0: Unknown table name 'Key word' (InvalidTable)
| | ... | E: 34, 0: Unknown table name 'bogus' (InvalidTable)
| | ... | E: 35, 0: Unknown table name 'Comments' (InvalidTable)

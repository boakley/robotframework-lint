*** Settings ***
| Documentation | Tests for the rule 'InvalidTable'
| Resource      | ../SharedKeywords.robot
|
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify all invalid table names in Robot 2 are detected
| | [Documentation]
| | ... | Verify that all invalid table names cause errors,
| | ... | and all valid names do not. Note: the test data
| | ... | is a collection of both valid and invalid names.
| | ... | Robot 2 accepted a few synonyms that were deprecated
| | ... | in Robot 3.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore    | all
| | ... | --error     | InvalidTable
| | ... | --configure | InvalidTable:robot2
| | ... | test_data/acceptance/rules/InvalidTable_Data.robot
| |
| | rflint return code should be | 6
| | rflint should report 6 errors
| | rflint should report 0 warnings

| Verify that the proper error message is returned with Robot 2 option
| | [Documentation]
| | ... | Verify that InvalidTable returns the expected message
| | ... | for every error
| | ... | Robot 2 accepted a few synonyms that were deprecated
| | ... | in Robot 3.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore    | all
| | ... | --error     | InvalidTable
| | ... | --configure | InvalidTable:robot2
| | ... | test_data/acceptance/rules/InvalidTable_Data.robot
| |
| | Output should contain
| | ... | E: 6, 0: Unknown table name '' (InvalidTable)
| | ... | E: 7, 0: Unknown table name '' (InvalidTable)
| | ... | E: 8, 0: Unknown table name '' (InvalidTable)
| | ... | E: 9, 0: Unknown table name 'Testcase' (InvalidTable)
| | ... | E: 10, 0: Unknown table name 'Key word' (InvalidTable)
| | ... | E: 37, 0: Unknown table name 'bogus' (InvalidTable)

| Verify all invalid table names in Robot 3 are detected
| | [Documentation]
| | ... | Verify that all invalid table names cause errors,
| | ... | and all valid names do not. Note: the test data
| | ... | is a collection of both valid and invalid names.
| | ... | Robot 3 obsoleted some synonyms that were valid with
| | ... | Robot 2.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore    | all
| | ... | --error     | InvalidTable
| | ... | --configure | InvalidTable:robot3
| | ... | test_data/acceptance/rules/InvalidTable_Data.robot
| |
| | rflint return code should be | 10
| | rflint should report 10 errors
| | rflint should report 0 warnings

| Verify that the proper error message is returned
| | [Documentation]
| | ... | Verify that InvalidTable returns the expected message
| | ... | for every error, using default option (Robot 3 syntax).
| | ... | Robot 3 obsoleted some synonyms that were valid with
| | ... | Robot 2.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore    | all
| | ... | --error     | InvalidTable
| | ... | test_data/acceptance/rules/InvalidTable_Data.robot
| |
| | Output should contain
| | ... | E: 6, 0: Unknown table name '' (InvalidTable)
| | ... | E: 7, 0: Unknown table name '' (InvalidTable)
| | ... | E: 8, 0: Unknown table name '' (InvalidTable)
| | ... | E: 9, 0: Unknown table name 'Testcase' (InvalidTable)
| | ... | E: 10, 0: Unknown table name 'Key word' (InvalidTable)
| | ... | E: 24, 0: Unknown table name 'Metadata' (InvalidTable)
| | ... | E: 25, 0: Unknown table name 'Cases' (InvalidTable)
| | ... | E: 32, 0: Unknown table name 'User Keyword' (InvalidTable)
| | ... | E: 33, 0: Unknown table name 'User Keywords' (InvalidTable)
| | ... | E: 37, 0: Unknown table name 'bogus' (InvalidTable)

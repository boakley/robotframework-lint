*** Settings ***
| Documentation | Tests for the suite rule 'DuplicateVariables'
| Resource      | ../SharedKeywords.robot
|
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify duplicate variable definitions raise an error
| | [Documentation]
| | ... | Verify duplicate variable definitions raise an error
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | DuplicateVariablesInSuite
| | ... | test_data/acceptance/rules/DuplicateVariables_Data.robot
| |
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | E: 3, 0: Variable 'some_var' defined twice, previous definition line 2 (DuplicateVariablesInSuite)
| | ... | E: 4, 0: Variable 'SomeVar' defined twice, previous definition line 2 (DuplicateVariablesInSuite)

| Verify duplicate variable definitions in a Resource file raise an error
| | [Documentation]
| | ... | Verify duplicate variable definitions in a Resource file raise an error
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | DuplicateVariablesInResource
| | ... | test_data/acceptance/rules/DuplicateVariablesInResource_Data.robot
| |
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | E: 3, 0: Variable 'some_var' defined twice, previous definition line 2 (DuplicateVariablesInResource)
| | ... | E: 4, 0: Variable 'SomeVar' defined twice, previous definition line 2 (DuplicateVariablesInResource)

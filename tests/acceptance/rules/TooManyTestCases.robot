*** Settings ***
| Documentation | Tests for the testcase rule 'TooManyTestCases'
| Resource      | ../SharedKeywords.robot
|
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Test suite WITH too many test cases
| | [Documentation]
| | ... | Verify that a test suite with too many test cases triggers the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooManyTestCases
| | ... | test_data/acceptance/rules/TooManyTestCases.robot
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings

| Verify correct linenumber is displayed
| | [Documentation]
| | ... | Verify that the reported line number points to the Nth test
| | ... |
| | ... | ie: if the max is 10, the error should point to the start
| | ... | of the 11th test case.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooManyTestCases
| | ... | test_data/acceptance/rules/TooManyTestCases.robot
| |
| | Output should contain
| | ... | E: 46, 0: Too many test cases (11 > 10) in test suite (TooManyTestCases)

| | rflint should report 1 errors
| | rflint should report 0 warnings

| Testcase WITHOUT too many test cases
| | [Documentation]
| | ... | Verify that a test suite without too many test cases does NOT trigger the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooManyTestCases
| | ... | ${SUITE SOURCE}
| |
| | rflint return code should be | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings

| Test suite WITH too many test cases after configuration
| | [Documentation]
| | ... | Verify that a test suite with too many test cases triggers the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooManyTestCases
| | ... | --configure  | TooManyTestCases:1
| | ... | test_data/acceptance/rules/TooManyTestCases.robot
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings

| Testcase WITHOUT too many test cases after configuration
| | [Documentation]
| | ... | Verify that a test suite without too many test cases does NOT trigger the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooManyTestCases
| | ... | --configure  | TooManyTestCases:20
| | ... | test_data/acceptance/rules/TooManyTestCases.robot
| |
| | rflint return code should be | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings

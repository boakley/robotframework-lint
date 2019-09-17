*** Settings ***
| Documentation | Tests for the testcase rule 'TooFewTestCases'
| Resource      | ../SharedKeywords.robot
|
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Test suite WITH too few test cases
| | [Documentation]
| | ... | Verify that a test suite with too few test cases triggers the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooFewTestCases
| | ... | test_data/acceptance/rules/TooFewTestCases.robot
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
| | ... | --error  | TooFewTestCases
| | ... | test_data/acceptance/rules/TooFewTestCases.robot
| |
| | Output should contain
| | ... | E: 6, 0: Too few test cases (1 < 2) in test suite (TooFewTestCases)

| | rflint should report 1 errors
| | rflint should report 0 warnings

| Testcase WITHOUT too few test cases
| | [Documentation]
| | ... | Verify that a test suite without too few test cases does NOT trigger the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooFewTestCases
| | ... | ${SUITE SOURCE} | use this file as input
| |
| | rflint return code should be | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings

| Test suite WITH too few test cases after configuration
| | [Documentation]
| | ... | Verify that a test suite with too few test cases triggers the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooFewTestCases
| | ... | --configure  | TooFewTestCases:5
| | ... | test_data/acceptance/rules/TooFewTestCases.robot
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings

| Testcase WITHOUT too few test cases after configuration
| | [Documentation]
| | ... | Verify that a test suite without too few test cases does NOT trigger the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooFewTestCases
| | ... | --configure  | TooFewTestCases:1
| | ... | test_data/acceptance/rules/TooFewTestCases.robot
| |
| | rflint return code should be | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings

*** Settings ***
| Documentation | Tests for the rule 'LineTooLong'
| Resource      | tests/acceptance/SharedKeywords.robot
| #
| Test Teardown
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify all long lines are detected
| | [Documentation]
| | ... | Verify that all long lines in the file are detected.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | LineTooLong
| | ... | test_data/acceptance/rules/LineTooLong_Data.robot
| |
| | rflint return code should be | 2
| | rflint should report 2 errors
| | rflint should report 0 warnings

| Verify that the proper error message is returned
| | [Documentation]
| | ... | Verify that LineTooLong returns the expected message
| | ... | for every error
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | LineTooLong
| | ... | test_data/acceptance/rules/LineTooLong_Data.robot
| |
| | Output should contain
| | ... | E: 9, 100: Line is too long (exceeds 100 characters) (LineTooLong)
| | ... | E: 10, 100: Line is too long (exceeds 100 characters) (LineTooLong)

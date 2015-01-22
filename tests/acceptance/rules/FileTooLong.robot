*** Settings ***
| Documentation | Tests for the rule 'FileTooLong'
| Resource      | tests/acceptance/SharedKeywords.robot
| #
| Test Teardown
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify a short file passes FileTooLong
| | [Documentation]
| | ... | Verify that a file of reasonable length passes the FileTooLong rule
| |
| | # We know this file isn't too long, so we'll use it for 
| | # our test data
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | FileTooLong
| | ... | ${SUITE_SOURCE}
| |
| | rflint return code should be | 0

| Verify the default limit of 300 is caught
| | [Documentation]
| | ... | Verify that FileTooLong gives the expected message
| | ... | for a long file.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | FileTooLong
| | ... | test_data/acceptance/rules/FileTooLong_Data.robot
| |
| | rflint return code should be | 1
| | Output should contain
| | ... | E: 301, 0: File has too many lines (302) (FileTooLong)

| Verify we can reconfigure the limit
| | [Documentation]
| | ... | Verify that we can reconfigure FileTooLong to accept
| | ... | a different limit
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | FileTooLong
| | ... | --configure | FileTooLong:400
| | ... | test_data/acceptance/rules/FileTooLong_Data.robot
| |
| | rflint return code should be | 0


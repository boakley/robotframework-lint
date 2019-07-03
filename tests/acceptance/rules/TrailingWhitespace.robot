*** Settings ***
| Documentation | Tests for the general rule 'TrailingWhitespace'
| Resource   | ../SharedKeywords.robot
|
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify TrailingWhitespace is triggered properly
| | [tags] | issue-37
| | [Documentation] |
| | ... | Verify that TrailingWhitespace rule is triggered
| | ... | for lines that have trailing whitespace
| |
| | [Setup]
| | ... | Run rf-lint with the following options:
| | ... | --ignore  | all
| | ... | --warning | TrailingWhitespace
| | ... | test_data/acceptance/issue-37.robot
| |
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | + test_data/acceptance/issue-37.robot
| | ... | W: 3, 0: Line has trailing whitespace (TrailingWhitespace)
| | ... | W: 4, 0: Line has trailing whitespace (TrailingWhitespace)

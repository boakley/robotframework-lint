*** Settings ***
| Documentation
| ... | This suite includes tests for specific issues in the issue tracker
| #
| Resource   | ../SharedKeywords.robot
| #
| Test Teardown
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Issue 30
| | [tags] | issue-30
| | [Documentation]
| | ... | Verify that you can configure a custom ResourceRule
| |
| | Run rf-lint with the following options:
| | ... | --ignore    | all
| | ... | --rulefile  | test_data/acceptance/issue-30.py
| | ... | --warning   | Issue30
| | ... | --configure | Issue30:42
| | ... | test_data/keywords.robot
| | 
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | + test_data/keywords.robot
| | ... | W: 0, 0: the configured value is 42 (Issue30)




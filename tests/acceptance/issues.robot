*** Settings ***
| Documentation
| ... | This suite includes tests for specific issues in the issue tracker
| #
| Resource   | SharedKeywords.robot
| #
| Test Teardown
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Issue 31
| | [tags] | issue-31
| | [Documentation]
| | ... | Verify that GeneralRule is passed an object with a type attribute
| |
| | Run rf-lint with the following options:
| | ... | --ignore  | all
| | ... | --rulefile  | test_data/acceptance/issue-31.py
| | ... | --warning | Issue31
| | ... | test_data/acceptance/nodoc.robot
| | ... | test_data/keywords.robot
| |
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | + test_data/acceptance/nodoc.robot
| | ... | W: 1, 0: the type is suite (Issue31)
| | ... | + test_data/keywords.robot
| | ... | W: 1, 0: the type is resource (Issue31)



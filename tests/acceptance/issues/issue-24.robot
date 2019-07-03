*** Settings ***
| Documentation
| ... | This suite includes tests for specific issues in the issue tracker
| #
| Resource   | ../SharedKeywords.robot
| #
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Issue 24
| | [tags] | issue-24
| | [Documentation]
| | ... | Verify that InvalidTable does anchored match
| | ... | 
| | ... | This issue resulted in strings like *** Keywordsz ***
| | ... | being considered valid, because we searched for "Keywords".
| | ... | The fix was to do an anchored search (eg: ^Keywords$) 
| | ... | (though the actual regex is a bit more complicated)
| |
| | Run rf-lint with the following options:
| | ... | --ignore | all
| | ... | --error  | InvalidTable
| | ... | test_data/acceptance/issue-24.robot
| | 
| | rflint return code should be | 4
| | Stderr should be | ${EMPTY}
| | Stdout should be 
| | ... | + test_data/acceptance/issue-24.robot
| | ... | E: 1, 0: Unknown table name 'Test case post' (InvalidTable)
| | ... | E: 5, 0: Unknown table name 'pre Test case' (InvalidTable)
| | ... | E: 9, 0: Unknown table name 'Keyword post' (InvalidTable)
| | ... | E: 13, 0: Unknown table name 'pre Keywords' (InvalidTable)

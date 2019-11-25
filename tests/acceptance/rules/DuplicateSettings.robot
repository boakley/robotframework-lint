*** Settings ***
| Documentation | Tests for the suite rule 'DuplicateSettings'
| Resource      | ../SharedKeywords.robot
|
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Verify duplicate settings raise an error
| | [Documentation]
| | ... | Verify duplicate settings raise an error
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | DuplicateSettingsInSuite
| | ... | test_data/acceptance/rules/DuplicateSettings_Data.robot
| |
| | Stderr should be | ${EMPTY}
| | Stdout should be
| | ... | E: 4, 0: Setting 'Documentation' used multiple times (previously used line 2) (DuplicateSettingsInSuite)
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings

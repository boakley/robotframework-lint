*** Settings ***
| Documentation | Tests for the rule 'InvalidTable'
| Resource      | ../SharedKeywords.robot
|
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Report an error on non-existent file
| | [Documentation]
| | ... | Check an error is raised when specifying a file that
| | ... | does not exist
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | test_data/does/not/exist.robot
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings
| |
| | Output should contain
| | ... | + test_data/does/not/exist.robot
| | ... | E: 0, 0: * No such file or directory* (RfLint)

| Report an error on non-existent file with custom format
| | [Documentation]
| | ... | Check an error is raised when specifying a file that
| | ... | does not exist, and that the error message is formatted
| | ... | according to custom rule
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --format={severity}: {filename}:{linenumber}: {message}
| | ... | test_data/does/not/exist.robot
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings
| |
| | Output should contain
| | ... | E: test_data/does/not/exist.robot:0: * No such file or directory*

*** Settings ***
| Documentation
| ... | Tests related to the handling of unicode data
|
| Library    | OperatingSystem
| Library    | Process
| Library    | SharedKeywords.py
| Resource   | SharedKeywords.robot
| Force Tags | smoke
|
| Test Teardown
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
    
| Testcase with unicode in the name
| | [Documentation] 
| | ... | Verify we can properly report issues in test cases with unicode
| | ... | in the test case name
| | [tags] | issue-35 | unicode

| | run rf-lint with the following options:
| | ... | --ignore | all
| | ... | --warning | PeriodInTestName
| | ... | test_data/acceptance/issue-35.robot
| | rflint return code should be | 0
| | rflint should report 1 warnings
| | Stdout should be
| | ... | + test_data/acceptance/issue-35.robot
| | ... | W: 2, 0: '.' in testcase name 'Пример тест-кейса.' (PeriodInTestName)

| Test suite with unicode in the file name
| | [Documentation]
| | ... | Verify that we can process files with unicode in the file name
| | [tags] | unicode

| | run rf-lint with the following options:
| | ... | --ignore | all
| | ... | --warning | RequireSuiteDocumentation
| | ... | test_data/acceptance/名稱與unicode.robot
| | rflint return code should be | 0
| | rflint should report 1 warnings
| | stdout should be
| | ... | + test_data/acceptance/名稱與unicode.robot
| | ... | W: 1, 0: No suite documentation (RequireSuiteDocumentation)

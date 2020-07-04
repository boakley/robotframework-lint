*** Settings ***
| Documentation
| ... | Runs rflint against the rflint test suites and resource files
|
| Library    | OperatingSystem
| Library    | Process
| Resource   | SharedKeywords.robot

*** Test Cases ***
| Run rflint and check if output contains given warnings and errors
| | Run rf-lint with the following options:
| | ... | test_data/acceptance/noqa.robot
| |
| | @{messages}= | Split to lines | ${result.stdout}
| | ${warnings}= | Get match count | ${messages} | regexp=^W:
| | ${errors}=   | Get match count | ${messages} | regexp=^E:
| |
| | Run keyword if | "${result.rc}" != "${1}" or ${warnings} != 3 or ${errors} != 1
| | ... | Fail | unexpectected errors or warnings: \n${result.stdout}\n${result.stderr}
| |
| | Output should contain
| | ... | W: 35, 100: Line is too long (exceeds 100 characters) (LineTooLong)
| | ... | E: 14, 0: space not allowed in tag name: 'Tag With Spaces' (TagWithSpaces)
| | ... | W: 23, 0: '.' in testcase name 'Do Not Skip This Test Case With Dot.' (PeriodInTestName)
| | ... | W: 38, 0: Too few steps (1) in test case (TooFewTestSteps)
| | Output should not contain
| | ... | W: 30, 100: Line is too long (exceeds 100 characters) (LineTooLong)
| | ... | E: 8, 0: space not allowed in tag name: 'Tag With Spaces' (TagWithSpaces)
| | ... | W: 18, 0: '.' in testcase name 'Skip This Test Case With Dot.' (PeriodInTestName)

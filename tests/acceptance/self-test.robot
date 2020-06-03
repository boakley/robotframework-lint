*** Settings ***
| Documentation
| ... | Runs rflint against the rflint test suites and resource files
|
| Library    | OperatingSystem
| Library    | Process
| Resource   | SharedKeywords.robot
| Test Template | Run rflint and verify there are no errors or warnings

*** Test Cases ***
  # file to run rflint against                           | # expected return code
| tests/unit/robotfile.robot                             | 0
| tests/unit/testcase.robot                              | 0
| tests/unit/keyword.robot                               | 0
| tests/unit/UnitTestResources.robot                     | 0
| tests/acceptance/smoke.robot                           | 0
| tests/acceptance/self-test.robot                       | 0
| tests/acceptance/arguments.robot                       | 0
| tests/acceptance/rules/InvalidTable.robot              | 0
| tests/acceptance/rules/DuplicateKeywordNames.robot     | 0
| tests/acceptance/rules/PeriodInSuiteName.robot         | 0
| tests/acceptance/rules/PeriodInTestName.robot          | 0
| tests/acceptance/rules/TooManyTestCases.robot          | 0
| tests/acceptance/rules/TooManyTestSteps.robot          | 0
| tests/acceptance/rules/LineTooLong.robot               | 0
| tests/acceptance/rules/FileTooLong.robot               | 0

*** Keywords ***
| Run rflint and verify there are no errors or warnings
| | [Arguments] | ${expected_rc}
| | [Documentation]
| | ... | Run rflint against the rflint tests
| |
| | ... | Note: it is assumed that the test name is the path of the file to test
| |
| | Run rf-lint with the following options:
| | ... | --format | {severity}: {linenumber}, {char}: {message} ({rulename})
| | ... | --configure | TooFewTestSteps:1
| |     # because the test cases reference filenames, they all have
| |     # periods in their name...
| | ... | --ignore | PeriodInTestName
| | ... | ${test name}
| |
| | @{messages}= | Split to lines | ${result.stdout}
| | ${warnings}= | Get match count | ${messages} | regexp=^W:
| | ${errors}=   | Get match count | ${messages} | regexp=^E:
| |
| | Run keyword if | "${result.rc}" != "${expected_rc}" or ${warnings} != 0 or ${errors} != 0
| | ... | Fail | unexpectected errors or warnings: \n${result.stdout}\n${result.stderr}

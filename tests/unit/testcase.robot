*** Settings ***
| Documentation
| ... | A collection of tests for the rflint testcase object
| #
| Library     | Collections
| Resource    | UnitTestResources.robot
| #
| Suite Setup | Run Keywords
| ... | Parse a robot file and save as a suite variable
| ... | AND | Set suite variable | ${testcase_table} | ${rf.tables[2]}

*** Test Cases ***
| Testcase table has expected number of test cases
| | [Documentation] | Verify that the testcase table has the expected number of rows
| | Length should be | ${testcase_table.testcases} | 3
| | ... | Expected the testcase table to have 3 tests but it did not.

| Test cases have the expected number of rows
| | [Documentation]
| | ... | Fail if the parsed testcase has the wrong number of rows
| |
| | # N.B. using the template lets all keywords run even when some fail
| | [Template] | Run keyword
| | Verify test case 0 has 8 rows
| | Verify test case 1 has 5 rows
| | Verify test case 2 has 5 rows

*** Keywords ***
| Verify test case ${test_num} has ${expected} rows
| | [Documentation]
| | ... | Fail if the given test doesn't have the correct number of rows
| |
| | ${testcase}= | Set variable | ${testcase_table.testcases[${test_num}]}
| | ${actual}= | Get length | ${testcase.rows}
| | Should be equal as numbers | ${actual} | ${expected}
| | ... | Expected '${testcase.name}' to have ${expected} rows but it had ${actual}
| | ... | values=False
| |
| | [Teardown] | Run keyword if | "${Keyword Status}" == "FAIL"
| | ... | log list | ${testcase.rows}

*** Settings ***
| Documentation | Unit tests for the RobotFile object
| Library  | Collections
| Resource | UnitTestResources.robot
| Suite Setup | Parse a robot file and save as a suite variable

*** Test Cases ***
| Parsed object has correct .name attribute
| | [Documentation] | Verify that the parsed data has a name attribute
| | Should be equal | ${rf.name} | pipes

| Parsed object has correct .path attribute
| | [Documentation] | Verify that the path attribute is correct
| | ${expected}= | Evaluate | os.path.abspath("${test_data}") | os
| | ${actual}= | Set variable | ${rf.path}
| | Should be equal as strings | ${actual} | ${expected}
| | ... | Expected .path to be '${expected}' but it was '${actual}'
| | ... | values=False

| All tables are correctly identified
| | [Documentation] | Verify that the parser found all of the tables, and in the right order
| | # N.B. using [template] allows all keywords to run even if some fail...
| | [Template] | Run keyword
| | Length should be | ${rf.tables} | 5
| | ... | Expected to find 5 tables but did not (see test teardown for more information)
| | Should be equal as strings
| | ... | ${rf.tables[0].__class__} | <class 'rflint.parser.tables.SettingTable'>
| | Should be equal as strings
| | ... | ${rf.tables[1].__class__} | <class 'rflint.parser.tables.VariableTable'>
| | Should be equal as strings
| | ... | ${rf.tables[2].__class__} | <class 'rflint.parser.parser.TestcaseTable'>
| | Should be equal as strings
| | ... | ${rf.tables[3].__class__} | <class 'rflint.parser.tables.UnknownTable'>
| | Should be equal as strings
| | ... | ${rf.tables[4].__class__} | <class 'rflint.parser.parser.KeywordTable'>
| |
| | [Teardown] | Run keyword if | "${Test Status}" == "FAIL"
| | ... | Log list | ${rf.tables}

| Tables have expected number of rows
| | [Documentation]
| | ... | Verify that each table has the expected number of rows
| | ... |
| | ... | Note: the parser doesn't keep track of rows in a testcase or
| | ... | keyword table since that information is tracked in each testcase
| | ... | and keyword object. Therefore this test only covers the settings,
| | ... | variables and bogus tables
| | ... |
| | ... | Also, the parser treats blank lines as rows, so the number of
| | ... | rows needs to account for trailing blank lines.
| |
| | [Template] | Run keyword
| | Verify table 0 has 8 rows
| | Verify table 1 has 5 rows
| | Verify table 3 has 2 rows

| Tables have header information
| | [Documentation]
| | ... | Verify that table objects have header information
| |
| | Should be equal as strings | ${rf.tables[0].header} | *** Settings ***
| | Should be equal as strings | ${rf.tables[1].header} | ** Variables
| | Should be equal as strings | ${rf.tables[2].header} | * Test Cases *
| | Should be equal as strings | ${rf.tables[3].header} | *** Bogus Table
| | Should be equal as strings | ${rf.tables[4].header} | * Keywords ***


*** Keywords ***
| Verify table ${table_num} has ${expected} rows
| | [Documentation]
| | ... | Fail if the given table doesn't have the correct number of rows
| |
| | ${table}= | Set variable | ${rf.tables[${table_num}]}
| | ${actual}= | Get length | ${table.rows}
| | Should be equal as numbers | ${actual} | ${expected}
| | ... | Expected '${table.name}' to  have ${expected} rows but it had ${actual}
| | ... | values=False
| |
| | [Teardown] | Run keyword if | "${Keyword Status}" == "FAIL"
| | ... | log list | ${table.rows}


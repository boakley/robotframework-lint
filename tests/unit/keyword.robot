*** Settings ***
| Documentation 
| ... | A collection of tests for the rflint keyword object
| #
| Library     | Collections
| Resource    | UnitTestResources.robot
| #
| Suite Setup | Run Keywords 
| ... | Parse a robot file and save as a suite variable
| ... | AND | Set suite variable | ${keyword_table} | ${rf.tables[4]}

*** Test Cases ***
| Keywords table has expected number of keywords
| | [Documentation]
| | ... | Verify that the keyword table has the expected number of keywords
| | 
| | Length should be | ${rf.tables[4].keywords} | 2
| | ... | Expected the keyword table to have 2 keywords but it did not.

| Keywords have the expected number of rows
| | [Documentation]
| | ... | Verify that that each keyword has the expected number of rows
| | 
| | [Setup] | Set test variable | ${keyword_table} | ${rf.tables[4]}
| | [Template] | Run keyword and continue on failure
| | Length should be | ${keyword_table.keywords[0].rows} | 6
| | Length should be | ${keyword_table.keywords[1].rows} | 3

*** Keywords ***
| Verify keyword ${keyword_num} has ${expected} rows
| | [Documentation]
| | ... | Fail if the given keyword doesn't have the correct number of rows
| | 
| | ${keyword}= | Set variable | ${keyword_table.keywords[${keyword_num}]}
| | ${actual}= | Get length | ${keyword.rows}
| | Should be equal as numbers | ${actual} | ${expected}
| | ... | Expected '${keyword.name}' to  have ${expected} rows but it had ${actual}
| | ... | values=False
| | 
| | [Teardown] | Run keyword if | "${Keyword Status}" == "FAIL"
| | ... | log list | ${keyword.rows}

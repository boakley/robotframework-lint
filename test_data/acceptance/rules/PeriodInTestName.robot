*** Settings ***
| Documentation 
| ... | This suite has a test with a period in the name
| ... | to trigger the PeriodInTestName rule. 

*** Test cases ***
| Test.1
| | [Documentation] | example test; should trigger PeriodInTestName rule
| | No operation

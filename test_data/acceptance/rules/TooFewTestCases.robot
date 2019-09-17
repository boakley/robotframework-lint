*** Settings ***
| Documentation
| ... | This suite has too many tests to trigger the TooFewTestCases rule.

*** Test cases ***
| Test 1
| | [Documentation] | example test; should trigger TooFewTestCases rule
| | No operation

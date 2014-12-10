*** Settings ***
| Documentation
| ... | This suite has a test with too many test steps
| ... | to trigger the TooManyTestSteps rule.

*** Test cases ***
| Test with too many steps
| | [Documentation] | example test; should trigger TooManyTestSteps rule
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation

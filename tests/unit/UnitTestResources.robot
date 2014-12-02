*** Settings ***
| Documentation | Resources used by the rflint unit tests

*** Variables ***
| ${test_data} | tests/unit/data/pipes.robot

*** Keywords ***
| Parse a robot file and save as a suite variable
| | [Documentation]
| | ... | Parse a robot file and save it as a suite variable
| | ${rf}= | Evaluate | rflint.RobotFile("${test_data}") | rflint
| | Set suite variable | ${rf}

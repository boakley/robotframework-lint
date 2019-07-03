*** Settings ***
| Documentation | Resources used by the rflint unit tests
| Library       | OperatingSystem

*** Variables ***
| ${test_data} | testdata/pipes.robot
| ${ROOT}      | ${CURDIR}/../..

*** Keywords ***
| Parse a robot file and save as a suite variable
| | [Documentation]
| | ... | Parse a robot file and save it as a suite variable
| |
| | # Make sure we're picking up the local rflint!
| | Evaluate | $root not in sys.path and sys.path.insert(0, $root) | sys
| |
| | # parse the file
| | ${rf}= | Evaluate | rflint.RobotFactory($test_data) | rflint
| | Set suite variable | ${rf}

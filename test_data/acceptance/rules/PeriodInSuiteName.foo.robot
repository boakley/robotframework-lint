# 
#
# N.B. a test case is required so that this file is interpreted
# as a suite rather than resource file

*** Settings ***
| Documentation 
| ... | This suite should have a period in its name, which will
| ... | trigger the PeriodInSuiteName rule. 

*** Test cases ***
| Test case #1
| | [Documentation] | example test
| | No operation

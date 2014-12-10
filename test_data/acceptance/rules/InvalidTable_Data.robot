## Test data for the rule InvalidTable
##

# these should fail the rule 

*
* *
*** 
*** Testcase ***
* Key word

# these should be valid:

* Setting
* Setting
* Setting *
** Setting
| *** Setting ***
  *** Setting ***
*** Setting ***
*** Settings ***
*** Metadata ***
*** Test Case ***
*** Test Cases ***
*** Variable ***
*** Variables ***
*** Keyword ***
*** Keywords ***
*** User Keyword ***
*** User Keywords ***

# these should fail the rule

*** bogus ***
*** Comments ***



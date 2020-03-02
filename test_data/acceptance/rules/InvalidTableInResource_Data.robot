## Test data for the rule InvalidTable
##

# these should fail the rule

*
* *
*** 
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
*** Comment ***
*** Comments ***
*** Metadata ***
*** Variable ***
*** Variables ***
*** Keyword ***
*** Keywords ***
*** User Keyword ***
*** User Keywords ***

# these should fail the rule

*** bogus ***



*** Settings ***
Documentation    Having two documentation sections is illegal.
                 ...    Use continuation lines for multiple lines.
Documentation    Error here.

# Several Library settings is okay
Library    DateTime
Library    Collections

*** Test Cases ***
Test 1
    No operation

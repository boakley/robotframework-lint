*** Settings ***
Documentation    Having two documentation sections is illegal.
                 ...    Use continuation lines for multiple lines.
Documentation    Error here.

# Metadata can used multiple times
Metadata    Version        2.0
Metadata    More Info      For more information about *Robot Framework* see http://robotframework.org
Metadata    Executed At    ${HOST}

# Several Library settings is okay
Library    DateTime
Library    Collections

*** Test Cases ***
Test 1
    No operation

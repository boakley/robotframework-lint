*** Settings ***
Documentation       Test cases with skip line indicator (# noqa)


*** Test Cases ***
Skip Tag With Spaces
    [Documentation]     Skip next line containing tag with spaces
    [Tags]      Tag With Spaces     TagWithNoSpace      # noqa
    ${foo}      Set Variable        some variable
    ${bar}      Set Variable        another variable

Do Not Skip Tag With Spaces
    [Documentation]     Report tag with spaces
    [Tags]      Tag With Spaces     TagWithNoSpace
    ${foo}      Set Variable        some variable
    ${bar}      Set Variable        another variable

Skip This Test Case With Dot.     #noqa
    [Documentation]     Do not report improper test case name
    ${foo}      Set Variable        some variable
    ${bar}      Set Variable        another variable

Do Not Skip This Test Case With Dot.
    [Documentation]     Report dot presence in test case name
    ${foo}      Set Variable        some variable
    ${bar}      Set Variable        another variable

Skip Very Long Line
    [Documentation]         Do not report very long line (+100 chars)
    ${long_variable}        Set Variable        This is a very long sentence with too many characters that should not be reported because of the 'noqa' comment at the end of this line  # noqa and something else
    ${short_variable}       Set Variable        This is a short variable

Do Not Skip Very Long Line
    [Documentation]         Report very long line (+100 chars)
    ${long_variable}        Set Variable        This is a very long sentence with too many characters that will be reported because of lack of 'noqa' comment at the end of this line
    ${short_variable}       Set Variable        This is a short variable

Do Not Skip Line Because Of Improper Comment    # noqaa
    [Documentation]         Improper comment should not make rflint omit the line
    ${var}                  Set Variable        This test case contains only one test step

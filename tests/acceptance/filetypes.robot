*** Settings ***
Documentation   Check if rflint reads supported file formats
Library         OperatingSystem
Library         Process
Library         String
Resource        SharedKeywords.robot


*** Test Cases ***
All Supported File Types
    [Template]      Run Rflint And Verify There Are No Errors For Supported File Types
    robot   resource    tsv

.robot And .resource Supported File Types
    [Template]      Run Rflint And Verify There Are No Errors For Supported File Types
    robot   resource

.resource And .tsv Supported File Types
    [Template]      Run Rflint And Verify There Are No Errors For Supported File Types
            resource    tsv

.robot And .tsv Supported File Types
    [Template]      Run Rflint And Verify There Are No Errors For Supported File Types
    robot               tsv

Only .robot Supported File Type
    [Template]      Run Rflint And Verify There Are No Errors For Supported File Types
    robot

Only .resource Supported File Type
    [Template]      Run Rflint And Verify There Are No Errors For Supported File Types
            resource

Only .tsv Supported File Type
    [Template]      Run Rflint And Verify There Are No Errors For Supported File Types
                        tsv

Only .pdf Unsupported File Type
    [Template]      Run Rflint And Verify That Unsupported File Types Returned Errors
    pdf

Specific .txt File With .robot Provided File Type
    [Template]      Run Rflint And Verify There Are No Output For Not Matching File Types
    test_data/acceptance/filetypes/test.txt         robot

Specific .robot File With .resource Provided File Type
    [Template]      Run Rflint And Verify There Are No Output For Not Matching File Types
    test_data/acceptance/filetypes/test.robot       resource

Specific .resource File With .robot And .tsv Provided File Type
    [Template]      Run Rflint And Verify There Are No Output For Not Matching File Types
    test_data/acceptance/filetypes/test.resource    robot   tsv

Specific .tsv File With .robot And .resource Provided File Type
    [Template]      Run Rflint And Verify There Are No Output For Not Matching File Types
    test_data/acceptance/filetypes/test.tsv         robot   resource


*** Keywords ***
Run Rflint And Verify There Are No Errors For Supported File Types
    [Arguments]                 @{extensions}
    ${file_types}               Parse File Types    @{extensions}
    Run rf-lint with the following options:
    ...     --filetypes         ${file_types}
    ...     test_data/acceptance/filetypes
    FOR     ${file_type}   IN   @{extensions}
            Should Contain      ${result.stdout}    test.${file_type}
    END
    Should Be Empty             ${result.stderr}

Run Rflint And Verify That Unsupported File Types Returned Errors
    [Arguments]                 @{extensions}
    ${file_types}               Parse File Types    @{extensions}
    Run rf-lint with the following options:
    ...     --filetypes         ${file_types}
    ...     test_data/acceptance/filetypes
    FOR     ${file_type}   IN   @{extensions}
            Should Contain      ${result.stderr}    rflint: File extension .${file_type} is not supported
    END
    Should Be Empty             ${result.stdout}

Run Rflint And Verify There Are No Output For Not Matching File Types
    [Arguments]                 ${path_to_file}     @{extensions}
    ${file_types}               Parse File Types    @{extensions}
    Run rf-lint with the following options:
    ...     -t                 ${file_types}
    ...     ${path_to_file}
    FOR     ${file_type}   IN   @{extensions}
            Should Be Empty     ${result.stdout}    ${EMPTY}
            Should Be Empty     ${result.stderr}    ${EMPTY}
    END
    Should Be Empty             ${result.stderr}

Parse File Types
    [Arguments]         @{filetypes}
    ${types}            Set Variable    ${EMPTY}
    FOR     ${index}    ${file_type}    IN ENUMERATE     @{filetypes}
        ${types}        Run Keyword If  ${index}==${0}
        ...             Set Variable    ${file_type}
        ...             ELSE
        ...             Set Variable    ${types},${file_type}
    END
    Log                 Provided filetypes: ${types}
    [Return]            ${types}

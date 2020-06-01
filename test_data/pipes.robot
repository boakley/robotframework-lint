# This test isn't designed to be run, it's used as an input
# for some unit tests
#
# Note: this test intentionally uses different styles for the
# table headings and there's a test for each style, so modify
# at your own risk.

*** Settings ***
| # comment in the settings table
| Documentation  | A simple test with some basic features
| Force tags     | test-data
| Metadata       | test format | pipe-separated
| Suite Setup    | No operation
| Suite Teardown | No operation
# whole-line comment in the settings table

** Variables
| # comment in the variable table
| ${FOO} | this is foo
| @{bar} | one | two | three
# whole-line comment in the variables table

* Test Cases *
| Test case #1
| # comment in a test case
| | [Documentation]
| | ... | This is the documentation for test case #1
| | [Setup] | No operation
| | [Tags] | tag1 | tag2 | # comment; not a tag
| | No operation | # comment in a statement
| | [Teardown] | No operation

| Test case #2
| | [Documentation]
| | ... | This is the documentation for test case #2
| | [Tags] | tag1 | tag2
| | No operation

| Test case #3
| | [Documentation] | make sure we can support whole-line comments
# whole-line comment in a test case, followed by blank line

| | No operation

*** Bogus Table
this table should parse even though the table

* Keywords ***
| Keyword #1
| | [Documentation]
| | ... | This is the documentation for keyword #1
# whole-line comment in a keyword, followed by a blank line

| | No operation

| Keyword #2
| | [Documentation]
| | ... | This is the documentation for keyword #2
| | No operation

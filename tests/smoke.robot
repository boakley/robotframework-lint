*** Settings ***
| Documentation
| ... | This suite includes some very basic smoke tests for rflint
| # 
| Library  | OperatingSystem
| Library  | Process
| Library  | SharedKeywords.py
| Resource | SharedKeywords.robot
| Force Tags | smoke

*** Test Cases ***
| Command line help 
| | [Documentation]
| | ... | This test verifies that --help doesn't crash
| | ... | 
| | ... | Not exactly an exhaustive test, but it at least
| | ... | verifies that the command works. 
| | 
| | Run rf-lint with the following options:
| | ... | --help
| | 
| | Should be equal as numbers | ${result.rc} | 0
| | # instead of doing an exhaustive test, let's just make 
| | # a quick spot-check
| | Output should contain
| | ... | usage:*
| | ... | positional arguments:
| | ... | optional arguments:
| | ... | *-h, --help*
| | ... | *--error RuleName, -e RuleName*
| | ... | *--ignore RuleName, -i RuleName*
| | ... | *--warn RuleName, -w RuleName*
| | ... | *--list*
| | ... | *--no-filenames*
| | ... | *--format FORMAT, -f FORMAT*

| | log | STDOUT:\n${result.stdout}
| | log | STDERR:\n${result.stderr}

| --list option
| | [Documentation]
| | ... | Verify that the --list option works.
| | 
| | Run rf-lint with the following options:
| | ... | --list
| | Should be equal as numbers | ${result.rc} | 0
| | log | STDOUT:\n${result.stdout}
| | log | STDERR:\n${result.stderr}

| rflint smoke.robot
| | [Documentation]
| | ... | Run rflint against this test suite
| | 
| | Run rf-lint with the following options:
| | ... | --format | {severity}: {linenumber}, {char}: {message} ({rulename})
| | ... | --no-filenames
| | ... | ${SUITE_SOURCE}
| | Should be equal as numbers | ${result.rc} | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings

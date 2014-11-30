*** Settings ***
| Documentation
| ... | This suite includes some very basic smoke tests for rflint
| # 
| Library    | OperatingSystem
| Library    | Process
| Library    | SharedKeywords.py
| Resource   | SharedKeywords.robot
| Force Tags | smoke

*** Test Cases ***
| Command line help 
| | [Documentation]
| | ... | This test verifies that --help returns some useful information
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
| | ... | optional arguments:
| | ... | *-h, --help*
| | ... | *--error <RuleName>, -e <RuleName>*
| | ... | *--ignore <RuleName>, -i <RuleName>*
| | ... | *--warn <RuleName>, -w <RuleName>*
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

| smoke.tsv
| | [Documentation]
| | ... | Run rflint against this file in .tsv format
| | [Setup] | Convert ${SUITE_SOURCE} to .tsv
| | [Teardown] | Run keyword if | ${result.rc} == 0 | Remove file | ${TEMPDIR}/smoke.tsv
| | Run rf-lint with the following options: | ${TEMPDIR}/smoke.tsv
| | Should be equal as numbers | ${result.rc} | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings

| smoke.txt (spaces, not pipes or tabs)
| | [Documentation] 
| | ... | Run rflint against this file in space separated format
| | [Setup] | Convert ${SUITE_SOURCE} to .txt
| | run rf-lint with the following options: | ${TEMPDIR}/smoke.txt
| | Should be equal as numbers | ${result.rc} | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings
| | [Teardown] | Run keyword if | ${result.rc} == 0 
| | ... | Remove file | ${TEMPDIR}/smoke.txt

*** Keywords ***
| Convert ${path} to ${format}
| | [Documentation]
| | ... | Converts this file to the given format, and save it to \${TEMPDIR}
| | ... | Note: a type of .txt will be saved in the space-sepraated format.
| | ... | 
| | ... | Example:
| | ... | 
| | ... | Convert smoke.robot to .txt
| | 
| | ${python}= | Evaluate | sys.executable | sys | # use same python used to run the tests
| | ${outfile}= | Set variable | ${TEMPDIR}/smoke${format}
| | ${result}= | Run process 
| | ... | ${python} | -m | robot.tidy | ${SUITE_SOURCE} | ${outfile}
| | log | saving file as ${outfile} | DEBUG
| | [return] | ${result}


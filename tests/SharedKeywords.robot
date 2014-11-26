*** Settings ***
| Documentation | Common keywords used by all the tests
| Library | String
| Library | Collections

*** Keywords ***
| Run rf-lint with the following options:
| | [Arguments] | @{options}
| | [Documentation]
| | ... | Attempt to start the hub with the given options
| | ... | 
| | ... | The stdout of the process will be in a test suite
| | ... | variable named \${output}
| | 
| | ${python}= | Evaluate | sys.executable | sys | # use same python used to run the tests
| | ${result}= | Run process | ${python} | -m | rflint | @{options}
| | Set test variable | ${result}
| | log | stdout: ${result.stdout} | DEBUG
| | log | stderr: ${result.stderr} | DEBUG


| rflint should report ${expected} errors
| | [Documentation]
| | ... | Verify that the output contains a specific number of errors.
| | ... | 
| | ... | Note: this keyword assumes that the output format is
| | ... | {severity}: {linenumber}, {char}: {message} ({rulename})
| | 
| | @{lines}= | Split to lines | ${result.stdout}
| | ${actual}= | Get match count | ${lines} | regexp=^E:
| | Should be equal as numbers | ${expected} | ${actual}
| | ... | Expected ${expected} errors but found ${actual}

| rflint should report ${expected} warnings
| | [Documentation]
| | ... | Verify that the output contains a specific number of warings
| | ... | 
| | ... | Note: this keyword assumes that the output format is
| | ... | {severity}: {linenumber}, {char}: {message} ({rulename})
| | 
| | @{lines}= | Split to lines | ${result.stdout}
| | ${actual}= | Get match count | ${lines} | regexp=^W:
| | Should be equal as numbers | ${expected} | ${actual}
| | ... | Expected ${expected} errors but found ${actual}

| Output should contain
| | [Arguments] | @{patterns}
| | [Documentation]
| | ... | Fail if the output from the previous command doesn't contain the given string
| | ... | 
| | ... | This keyword assumes the output of the command is in
| | ... | a test suite variable named \${result.stdout}
| | ... |
| | ... | To match against a regular expression, prefix the pattern with 'regexp='
| | ... | (this uses Collections.Should contain match to do the matching)
| | ... | 
| | ... | Note: the help will be automatically wrapped, so
| | ... | you can only search for relatively short strings.
| | 
| | @{lines}= | Split to lines | ${result.stdout}
| | log | ${lines}
| | :FOR | ${pattern} | IN | @{patterns}
| | | Should contain match | ${lines} | ${pattern}
| | | ... | expected:\n${pattern}\nbut got:\n${lines}

| Output should not contain
| | [Arguments] | @{patterns}
| | [Documentation]
| | ... | Fail if the output from the previous command contains the given string
| | ... | 
| | ... | This keyword assumes the output of the command is in
| | ... | a test suite variable named \${result.stdout}
| | ... | 
| | ... | Note: the help will be automatically wrapped, so
| | ... | you can only search for relatively short strings.
| | 
| | ${lines}= | Split to lines | ${result.stdout}
| | :FOR | ${pattern} | IN | @{patterns}
| | | Should not contain match | ${lines} | ${pattern}
| | | ... | stdout should not contain '${pattern}' but it did:\n${result.stdout}
| | | ... | values=False

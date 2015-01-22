*** Settings ***
| Documentation | Common keywords used by all the tests
| Library | String
| Library | Collections
| Library | Process

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
| | ${result}= | Run process | ${python} | -m | rflint | 
| | ... | # Define a specific format for all messages (but can be overridden)
| | ... | --format | {severity}: {linenumber}, {char}: {message} ({rulename})
| | ... | @{options}
| | Set test variable | ${result}
| | 
| | log | stdout: ${result.stdout} | DEBUG
| | log | stderr: ${result.stderr} | DEBUG

| rflint return code should be
| | [Documentation]
| | ... | Validate the return code of the most recent run of rflint
| |
| | [Arguments] | ${expected}
| | Should be equal as integers | ${result.rc} | ${expected}
| | ... | Expected a result code of ${expected} but got ${result.rc} 
| | ... | values=False

| rflint should report ${expected} errors
| | [Documentation]
| | ... | Verify that the output contains a specific number of errors.
| | ... | 
| | ... | Note: this keyword assumes that the output format is
| | ... | {severity}: {linenumber}, {char}: {message} ({rulename})
| | 
| | @{lines}= | Split to lines | ${result.stdout}
| | ${actual}= | Get match count | ${lines} | regexp=^E:
| | Run keyword if | ${actual} != ${expected}
| | ... | log | ${result.stdout}
| | Should be equal as numbers | ${expected} | ${actual}
| | ... | Expected ${expected} errors but found ${actual}
| | ... | values=False

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

| Stdout should be
| | [Arguments] | @{lines}
| | [Documentation] 
| | ... | Verify that stdout of rflint matches the given set of lines.
| | ... | All arguments are joined together with newlines
| | 
| | ${expected}= | Catenate | SEPARATOR=\n | @{lines}
| | Should be equal | ${result.stdout} | ${expected}
| | ... | Unexpected output on stdout.\nExpected:\n${expected}\nActual:\n${result.stdout}
| | ... | values=False

| Stderr should be
| | [Arguments] | @{lines}
| | [Documentation] 
| | ... | Verify that stderr of rflint matches the given set of lines.
| | ... | All arguments are joined together with newlines
| | 
| | ${expected}= | Catenate | SEPARATOR=\n | @{lines}
| | Should be equal | ${result.stderr} | ${expected}
| | ... | Unexpected output on stderr. \nExpected:\n${expected}\nActual:\n${result.stderr}
| | ... | values=False

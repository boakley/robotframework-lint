from robot.libraries.BuiltIn import BuiltIn

def create_a_test_suite(filename, *args):
    '''Create a test suite file that mirrors the input

    This creates a test suite file in pipe-separated format.
    The input needs to include explicit newlines for each line,
    and variables must be escaped. 

    If you want literal variables or comments, you must escape
    the $ and/or #

    Example:

    *** Test Cases ***
    | Example test case
    | | [Setup] | Create a temporary suite | ${test_suite}
    | | ... | *** Test Cases ***\n
    | | ... | An example test case\n
    | | ... | | [Documentation] | this is a sample testcase\n
    | | ... | | ... | \n
    | | ... | | ... | blah blah blah\n
    | | ... | | log | hello from \${TEST NAME}\n

    '''
    suite = args[0]
    # In order to make it as easy as possible to create and read 
    # the test, we don't require that the caller escape the
    # pipes. So, we have to insert literal pipes between each 
    # argument, and add a leading pipe after each newline.
    for arg in args[1:]:

            if suite[-1] != "\n" and suite[-1] != "|":
                suite += " "

            if suite[-1] == "\n" and arg.startswith("#"):
                suite += arg

            elif arg == "\n" or arg.startswith("*"):
                # blank lines and headers get appended as-is
                suite += arg
            else:
                # everything else we add a separator and then the argument
                suite += "| " + arg
    with open(filename, "w") as f:
        f.write(suite)

    return suite

    

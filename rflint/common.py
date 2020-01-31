import sys

ERROR = "E"
WARNING = "W"
IGNORE = "I"


def normalize_name(string):
    '''convert to lowercase, remove spaces and underscores'''
    return string.replace(" ", "").replace("_", "").lower()


class Rule(object): 
    # default severity; subclasses may override
    severity = WARNING
    output_format = "{severity}: {linenumber}, {char}: {message} ({rulename})"

    def __init__(self, controller, severity=None):
        self.controller = controller
        if severity is not None:
            self.severity = severity

    def configure(self, *args, **kwargs):
        # subclasses can override this if they want to be configurable.
        raise Exception("rule '%s' is not configurable" % self.__class__.__name__)

    @property
    def name(self):
        return self.__class__.__name__

    def report(self, obj, message, linenum, char_offset=0):
        """Report an error or warning"""
        self.controller.report(linenumber=linenum, filename=obj.path,
                               severity=self.severity, message=message,
                               rulename = self.__class__.__name__,
                               char=char_offset)

    @property
    def doc(self):
        '''Algorithm from https://www.python.org/dev/peps/pep-0257/'''
        if not self.__doc__:
            return ""

        lines = self.__doc__.expandtabs().splitlines()

        # Determine minimum indentation (first line doesn't count):
        indent = sys.maxsize
        for line in lines[1:]:
            stripped = line.lstrip()
            if stripped:
                indent = min(indent, len(line) - len(stripped))

        # Remove indentation (first line is special):
        trimmed = [lines[0].strip()]
        if indent < sys.maxsize:
            for line in lines[1:]:
                trimmed.append(line[indent:].rstrip())

        # Strip off trailing and leading blank lines:
        while trimmed and not trimmed[-1]:
            trimmed.pop()
        while trimmed and not trimmed[0]:
            trimmed.pop(0)

        # Return a single string:
        return '\n'.join(trimmed)

    def __repr__(self):
        return "%s %s" % (self.severity, self.__class__.__name__)

class TestRule(Rule): 
    """Rule that runs against test cases. 

    The object that is passed in will be of type rflint.parser.Testcase
    """
    pass

class ResourceRule(Rule):
    """Rule that runs against a resource file

    The object that is passed in will be of type rflint.parser.ResourceFile
    """

class SuiteRule(Rule): 
    """Rule that runs against test cases. 

    The object that is passed in will be of type rflint.parser.SuiteFile
    """
    pass

class KeywordRule(Rule): 
    """Rule that runs against keywords

    The object that is passed in will be of type rflint.parser.Keyword
    """
    pass

class GeneralRule(Rule):
    """Rule that requires a suite or resource file, but may apply to child objects

    This rule is identical to a SuiteRule, but exists in case you want
    to write a rule that accepts a suite but doesn't necessarily apply
    to the suite (ie: you may iterate over tests, or keywords, or some
    other child object)
    """
    pass


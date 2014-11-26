import rflint

ERROR="E"
WARNING="W"

class Rule(object): 
    # default severity; subclasses may override
    severity = WARNING
    rule_type = "general"
    output_format = "{severity}: {linenumber}, {char}: {message} ({rulename})"

    def __init__(self, severity=None):
        if severity is not None:
            self.severity = severity

    @property
    def name(self):
        return self.__class__.__name__

    def report(self, obj, linenum, message, char_offset=0):
        print self.output_format.format(linenumber=linenum, filename=obj.path, 
                                        severity=self.severity, message=message,
                                        rulename = self.__class__.__name__,
                                        char=char_offset)

    def __repr__(self):
        return "%s %s" % (self.severity, self.__class__.__name__)

class TestRule(Rule): 
    '''Rule that runs against test cases. 

    The object that is passed in will be of type rflint.parser.Testcase
    '''
    rule_type = "test"

class SuiteRule(Rule): 
    '''Rule that runs against test cases. 

    The object that is passed in will be of type rflint.parser.Suite
    '''
    rule_type = "suite"
class KeywordRule(Rule): 
    rule_type = "keyword"
class GeneralRule(Rule):
    rule_type = "general"


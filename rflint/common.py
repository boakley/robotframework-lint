import rflint

ERROR="E"
WARNING="W"

class Rule(object): 
    # default severity; subclasses may override
    severity = WARNING
    output_format = "{severity}: {linenumber}, {char}: {message} ({rulename})"

    def __init__(self, controller, severity=None):
        self.controller = controller
        if severity is not None:
            self.severity = severity

    @property
    def name(self):
        return self.__class__.__name__

    def report(self, obj, message, linenum, char_offset=0):
        '''Report an error or warning'''
        self.controller.report(linenumber=linenum, filename=obj.path,
                               severity=self.severity, message=message,
                               rulename = self.__class__.__name__,
                               char=char_offset)

    def __repr__(self):
        return "%s %s" % (self.severity, self.__class__.__name__)

class TestRule(Rule): 
    '''Rule that runs against test cases. 

    The object that is passed in will be of type rflint.parser.Testcase
    '''
    pass

class SuiteRule(Rule): 
    '''Rule that runs against test cases. 

    The object that is passed in will be of type rflint.parser.Suite
    '''
    pass
class KeywordRule(Rule): 
    '''Rule that runs against keywords

    The object that is passed in will be of type rflint.parser.Keyword
    '''
    pass
class GeneralRule(Rule):
    '''Rule that requires a suite, but may apply to child objects

    This rule is identical to a SuiteRule, but exists in case you want
    to write a rule that accepts a suite but doesn't necessarily apply
    to the suite (ie: you may iterate over tests, or keywords, or some
    other child object)
    '''
    pass


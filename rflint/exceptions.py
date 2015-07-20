'''
This file defines custom exceptions used by robotframework-lint

'''

class UnknownRuleException(Exception):
    def __init__(self, rulename):
        super(UnknownRuleException, self).__init__("unknown rule: '%s'" % rulename)

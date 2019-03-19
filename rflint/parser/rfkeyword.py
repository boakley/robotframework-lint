# Does this need to be in its own file, or can I combine 
# testcase and keyword into one file? 
from .common import RobotStatements

class Keyword(RobotStatements):
    '''A robotframework keyword

    A keyword is identical to a testcase in almost all respects
    except for some of the metadata it supports (which this definition
    doesn't (yet) account for...).
    '''
    def __init__(self, parent, linenumber, name):
        RobotStatements.__init__(self)
        self.linenumber = linenumber
        self.name = name
        self.rows = []
        self.parent = parent

    def __repr__(self):
        # should this return the fully qualified name?
        return "<Keyword: %s>" % self.name

    # this is great, except that we don't return the line number
    # or character position of each tag. The linter needs that. :-(
    @property
    def tags(self):
        tags = []
        for statement in self.statements:
            if len(statement) > 2 and statement[1].lower() == "[tags]":
                tags = tags + statement[2:]
        return tags

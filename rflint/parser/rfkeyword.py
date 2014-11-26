# Does this need to be in its own file, or can I combine 
# testcase and keyword into one file? 
from testcase import Testcase

class Keyword(Testcase):
    '''A robotframework keyword

    A keyword is identical to a testcase in almost all respects
    except for some of the metadata it supports (which this definition
    doesn't (yet) account for...).
    '''
    def __repr__(self):
        # should this return the fully qualified name?
        return "<Keyword: %s>" % self.name


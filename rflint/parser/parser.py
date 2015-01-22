'''
A custom robotframework parser that retains line numbers (though
it doesn't retain character positions for each cell)

Note: this only works on pipe-separated files. It uses part of
the TxtReader robot parser to divide a line into cells. 

(probably works for space-separated too. I haven't tried. )

Performance is pretty spiffy! At the time I write this (where
admittedly I don't fully parse everything) it is about 3x-5x faster
than the official robot parser. It can read a file with 500
test cases and 500 keywords in about 30ms, compared to 150ms
for the robot parser. Sweet.  

'''

import re
import sys
import os.path
from robot.parsing.txtreader import TxtReader
from robot.errors import DataError
from robot.utils import Utf8Reader
from util import timeit, Matcher
from tables import *
from testcase import Testcase
from rfkeyword import Keyword
from common import Row, Statement

def RobotFileFactory(path, parent=None):
    '''Return an instance of SuiteFile or ResourceFile

    Exactly which is returned depends on the contents of the
    file. If there is a testcase table, this will return an
    instance of SuiteFile, otherwise it will return an
    instance of ResourceFile.
    '''
    rf = RobotFile(path, parent)

    for table in rf.tables:
        if isinstance(table, TestcaseTable):
            rf.__class__ = SuiteFile
            return rf

    rf.__class__ = ResourceFile
    return rf
    
class RobotFile(object):
    '''
    Terminology:

    - A file is a set of tables
    - A table begins with a heading and extends to the next table or EOF
    - Each table may be made up of smaller tables that define test cases or keywords
    - Each line of text in a table becomes a "Row". 
    - A Row object contains a list of cells.
    - A cell is all of the data between pipes, stripped of leading and
      trailing spaces

    '''
    def __init__(self, path, parent=None):
        self.parent = None
        self.name = os.path.splitext(os.path.basename(path))[0]
        self.path = os.path.abspath(path)
        self.tables = []
        self.rows = []

        self._load(path)


    def _load(self, path):

        '''
        The general idea is to do a quick parse, creating a list of
        tables. Each table is nothing more than a list of rows, with
        each row being a list of cells. Additional parsing such as
        combining rows into statements is done on demand. This first 
        pass is solely to read in the plain text and organize it by table.
        '''

        self.tables = []
        current_table = DefaultTable(self)

        with Utf8Reader(path) as f:
            self.raw_text = f.read()
            f._file.seek(0) # bleh; wish this wasn't a private property
            matcher = Matcher(re.IGNORECASE)
            for linenumber, raw_text in enumerate(f.readlines()):
                linenumber += 1; # start counting at 1 rather than zero

                # this mimics what the robot TSV reader does --
                # it replaces non-breaking spaces with regular spaces,
                # and strips trailing whitespace
                raw_text = raw_text.replace(u'\xA0', ' ')
                raw_text = raw_text.rstrip()

                # FIXME: I'm keeping line numbers but throwing away
                # where each cell starts. I should be preserving that
                # (though to be fair, robot is throwing that away so
                # I'll have to write my own splitter if I want to save 
                # the character position)
                cells = TxtReader.split_row(raw_text)
                _heading_regex = r'^\s*\*+\s*(.*?)[ *]*$'

                if matcher(_heading_regex, cells[0]):
                    # we've found the start of a new table
                    table_name = matcher.group(1)
                    current_table = tableFactory(self, linenumber, table_name)
                    self.tables.append(current_table)
                else:
                    current_table.append(Row(linenumber, raw_text, cells))

    def __repr__(self):
        return "<RobotFile(%s)>" % self.path

    @property 
    def warnings(self):
        '''This isn't fully working. The idea is to return all parse errors
        I need to create a Warning or ParseError class that has
        line numbers and warning messages and whatnot. Or do I?
        '''
        warnings = []
        for table in self.tables:
            if isinstance(table, UnknownTable):
                warnings.append([table.linenumber, "unknown table '%s'" % table.name])
            if table.type is None:
                # line number, column number, message
                # line numbers start at 1, columns start at zero. 
                warnings.append([1, 0, "no testcases or keywords"])

#        for table in self.tables:
#            warnings += table.warnings
#            # where table.warnings might do:
#            # for testcase in table.testcases:
#            #     warnings += testcase.warnings
        return warnings
            
    @property
    def type(self):
        '''Return 'suite' or 'resource' or None
        
        This will return 'suite' if a testcase table is found;
        It will return 'resource' if at least one robot table
        is found. If no tables are found it will return None
        '''
        
        robot_tables = [table for table in self.tables if table.type is not None]
        if len(robot_tables) == 0:
            # no robot tables were found
            return None

        for table in self.tables:
            if isinstance(table, TestcaseTable):
                return "suite"

        return "resource"

    @property
    def keywords(self):
        '''Generator which returns all keywords in the suite'''
        for table in self.tables:
            if isinstance(table, KeywordTable):
                for keyword in table.keywords:
                    yield keyword

    @property
    def testcases(self):
        '''Generator which returns all test cases in the suite'''
        for table in self.tables:
            if isinstance(table, TestcaseTable):
                for testcase in table.testcases:
                    yield testcase
        
    def dump(self):
        '''Regurgitate the tables and rows'''
        for table in self.tables:
            print "*** %s ***" % table.name
            table.dump()
                

def tableFactory(parent, linenumber, name):
    match = Matcher(re.IGNORECASE)
    if name is None:
        table = UnknownTable(parent, linenumber, name)
    elif match(r'settings?|metadata', name):
        table = SettingTable(parent, linenumber, name)
    elif match(r'variables?', name):
        table = VariableTable(parent, linenumber, name)
    elif match(r'test( cases?)', name):
        table = TestcaseTable(parent, linenumber, name)
    elif match(r'(user )?keywords?', name):
        table = KeywordTable(parent, linenumber, name)
    else:
        table = UnknownTable(parent, linenumber, name)

    return table


class SuiteFile(RobotFile):
    def __repr__(self):
        return "<SuiteFile(%s)>" % self.path

class ResourceFile(RobotFile):
    def __repr__(self):
        return "<ResourceFile(%s)>" % self.path

class TestcaseTable(AbstractContainerTable):
    _childClass = Testcase
    def __init__(self, parent, *args, **kwargs):
        super(TestcaseTable, self).__init__(parent, *args, **kwargs)
        self.testcases = self._children

class KeywordTable(AbstractContainerTable):
    _childClass = Keyword
    def __init__(self, parent, *args, **kwargs):
        super(KeywordTable, self).__init__(parent, *args, **kwargs)
        self.keywords = self._children

@timeit
def dump(suite):
    result = []
    for table in suite.tables:
#        print "table:", table
#        for row in table.rows:
#            print "=>", row
        if isinstance(table, TestcaseTable):
            for tc in table.testcases:
                # force parsing of individual steps
                steps = [step for step in tc.steps]

def try_to_run_it(suite):
    print "here we go!"

    # create a test suite object
    from robot.api import TestSuite
    suite = TestSuite('Autogenerated Suite')

    for testcase in suite.testcases:
        import pdb; pdb.set_trace()

if __name__ == "__main__":
    from robot.parsing import TestData, ResourceFile
    import sys

    # parse with the robot parser and this parser, to
    # see which is faster. Of course, this parser will
    # be faster :-)
    @timeit
    def test_robot():
        try:
            suite = TestData(parent=None, source=sys.argv[1])
        except DataError:
            # if loading the suite failed, assume it's a resource file
            # (bad assumption, but _whatever_)
            suite = ResourceFile(source=sys.argv[1])
        return suite

    @timeit
    def test_mine():
        suite = RobotFile(sys.argv[1])
        # force parsing of every line
        for tc in suite.testcases:
            statements = tc.statements
            tags = tc.tags
        return suite

    if len(sys.argv) == 1:
        print "give me a filename on the command line"
        sys.exit(1)
        
    suite1 = test_robot()
    suite2 = test_mine()
    import pdb; pdb.set_trace()

    print suite2.warnings

#    tc = [x for x in suite2.testcases][0]
#    import pdb; pdb.set_trace()

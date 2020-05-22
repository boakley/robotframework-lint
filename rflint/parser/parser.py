'''

A custom robotframework parser that retains line numbers (though
it doesn't (yet!) retain character positions for each cell)


Note: this only works on pipe and space separated files. It uses a
copy of the deprecated TxtReader robot parser to divide a line into cells.

(probably works for space-separated too. I haven't tried. )

Performance is pretty spiffy! At the time I write this (where
admittedly I don't fully parse everything) it is about 3x-5x faster
than the official robot parser. It can read a file with 500
test cases and 500 keywords in about 30ms, compared to 150ms
for the robot parser. Sweet.

'''
from __future__ import print_function

import re
import sys
import os.path
from robot.errors import DataError
from robot.utils import FileReader
from .util import timeit, Matcher
from .tables import AbstractContainerTable, DefaultTable, SettingTable, VariableTable, UnknownTable
from .testcase import Testcase
from .rfkeyword import Keyword
from .common import Row, Statement


def RobotFactory(path, parent=None):
    '''Return an instance of SuiteFile, ResourceFile, SuiteFolder

    Exactly which is returned depends on whether it's a file or
    folder, and if a file, the contents of the file. If there is a
    testcase table, this will return an instance of SuiteFile,
    otherwise it will return an instance of ResourceFile.
    '''

    if os.path.isdir(path):
        return SuiteFolder(path, parent)

    else:
        rf = RobotFile(path, parent)

        for table in rf.tables:
            if isinstance(table, TestcaseTable):
                rf.__class__ = SuiteFile
                return rf

        rf.__class__ = ResourceFile
        return rf

class SuiteFolder(object):
    def __init__(self, path, parent=None):

        self.path = os.path.abspath(path)
        self.parent = parent
        self.name = os.path.splitext(os.path.basename(path))[0]
        self.initfile = None

        # see if there's an initialization file. If so,
        # attempt to load it
        for filename in ("__init__.robot", "__init__.txt"):
            if os.path.exists(os.path.join(self.path, filename)):
                self.initfile = RobotFile(os.path.join(self.path, filename))
                break


    def walk(self, *types):
        '''
        Iterator which visits all suites and suite files,
        yielding test cases and keywords
        '''
        requested = types if len(types) > 0 else [SuiteFile, ResourceFile, SuiteFolder, Testcase, Keyword]

        for thing in self.robot_files:
            if thing.__class__ in requested:
                yield thing
            if isinstance(thing, SuiteFolder):
                for child in thing.walk():
                    if child.__class__ in requested:
                        yield child
            else:
                for child in thing.walk(*types):
                    yield child

    @property
    def robot_files(self):
        '''Return a list of all folders, and test suite files (.txt, .robot)
        '''
        result = []
        for name in os.listdir(self.path):
            fullpath = os.path.join(self.path, name)
            if os.path.isdir(fullpath):
                result.append(RobotFactory(fullpath, parent=self))
            else:
                if ((name.endswith(".txt") or name.endswith(".robot")) and
                    (name not in ("__init__.txt", "__init__.robot"))):

                    result.append(RobotFactory(fullpath, parent=self))
        return result


class RobotFile(object):
    '''
    Terminology:

    - A file is a set of tables
    - A table begins with a heading and extends to the next table or EOF
    - Each table may be made up of smaller tables that define test cases
      or keywords
    - Each line of text in a table becomes a "Row".
    - A Row object contains a list of cells.
    - A cell is all of the data between pipes, stripped of leading and
      trailing spaces

    '''
    def __init__(self, path, parent=None):
        self.parent = parent
        self.name = os.path.splitext(os.path.basename(path))[0]
        self.path = os.path.abspath(path)
        self.tables = []
        self.rows = []

        try:
            self._load(path)
        except Exception as e:
            sys.stderr.write("there was a problem reading '%s': %s\n" % (path, str(e)))

    def walk(self, *types):
        '''
        Iterator which can return all test cases and/or keywords

        You can specify with objects to return as parameters; if
        no parameters are given, both tests and keywords will
        be returned.

        For example, to get only test cases, you could call it
        like this:

            robot_file = RobotFactory(...)
            for testcase in robot_file.walk(Testcase): ...

        '''
        requested = types if len(types) > 0 else [Testcase, Keyword]

        if Testcase in requested:
            for testcase in self.testcases:
                yield testcase

        if Keyword in requested:
            for keyword in self.keywords:
                yield keyword

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

        with FileReader(path) as f:
            # N.B. the caller should be catching errors
            self.raw_text = f.read()
            f.file.seek(0)

            matcher = Matcher(re.IGNORECASE)
            for linenumber, raw_text in enumerate(f.readlines()):
                linenumber += 1; # start counting at 1 rather than zero

                # this mimics what the robot TSV reader does --
                # it replaces non-breaking spaces with regular spaces,
                # and then strips trailing whitespace
                raw_text = raw_text.replace(u'\xA0', ' ')
                raw_text = raw_text.rstrip()

                # FIXME: I'm keeping line numbers but throwing away
                # where each cell starts. I should be preserving that
                # (though to be fair, robot is throwing that away so
                # I'll have to write my own splitter if I want to save
                # the character position)
                cells = self.split_row(raw_text)
                _heading_regex = r'^\s*\*+\s*(.*?)[ *]*$'

                if matcher(_heading_regex, cells[0]):
                    # we've found the start of a new table
                    table_name = matcher.group(1)
                    current_table = tableFactory(self, linenumber, table_name, raw_text)
                    self.tables.append(current_table)
                else:
                    current_table.append(Row(linenumber, raw_text, cells))

    def split_row(self, row):
        """ function copied from
        https://github.com/robotframework/robotframework/blob/v3.1.2/src/robot/parsing/robotreader.py
        """
        space_splitter = re.compile(u'[ \t\xa0]{2,}|\t+')
        pipe_splitter = re.compile(u'[ \t\xa0]+\|(?=[ \t\xa0]+)')
        pipe_starts = ('|', '| ', '|\t', u'|\xa0')
        pipe_ends = (' |', '\t|', u'\xa0|')
        if row[:2] in pipe_starts:
            row = row[1:-1] if row[-2:] in pipe_ends else row[1:]
            return [cell.strip()
                    for cell in pipe_splitter.split(row)]
        return space_splitter.split(row)

    def __repr__(self):
        return "<RobotFile(%s)>" % self.path

    @property
    def type(self):
        '''Return 'suite' or 'resource' or None

        This will return 'suite' if a testcase table is found;
        It will return 'resource' if at least one robot table
        is found. If no tables are found it will return None
        '''

        robot_tables = [table for table in self.tables if not isinstance(table, UnknownTable)]
        if len(robot_tables) == 0:
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
            print("*** %s ***" % table.name)
            table.dump()


def tableFactory(parent, linenumber, name, header):
    match = Matcher(re.IGNORECASE)
    if name is None:
        table = UnknownTable(parent, linenumber, name, header)
    elif match(r'settings?|metadata', name):
        table = SettingTable(parent, linenumber, name, header)
    elif match(r'variables?', name):
        table = VariableTable(parent, linenumber, name, header)
    elif match(r'test ?cases?', name):
        table = TestcaseTable(parent, linenumber, name, header)
    elif match(r'(user )?keywords?', name):
        table = KeywordTable(parent, linenumber, name, header)
    else:
        table = UnknownTable(parent, linenumber, name, header)

    return table


class SuiteFile(RobotFile):
    def __repr__(self):
        return "<SuiteFile(%s)>" % self.path

    @property
    def settings(self):
        '''Generator which returns all of the statements in all of the settings tables'''
        for table in self.tables:
            if isinstance(table, SettingTable):
                for statement in table.statements:
                    yield statement

    @property
    def variables(self):
        '''Generator which returns all of the statements in all of the variables tables'''
        for table in self.tables:
            if isinstance(table, VariableTable):
                # FIXME: settings have statements, variables have rows WTF? :-(
                for statement in table.rows:
                    if statement[0] != "":
                        yield statement

class ResourceFile(RobotFile):
    def __repr__(self):
        return "<ResourceFile(%s)>" % self.path

    @property
    def settings(self):
        '''Generator which returns all of the statements in all of the settings tables'''
        for table in self.tables:
            if isinstance(table, SettingTable):
                for statement in table.statements:
                    yield statement

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
        print("give me a filename on the command line")
        sys.exit(1)

    suite1 = test_robot()
    suite2 = test_mine()

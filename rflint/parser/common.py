from __future__ import print_function
import re

class RobotStatements(object):
    def append(self, linenumber, raw_text, cells):
        """Add another row of data from a test suite"""
        self.rows.append(Row(linenumber, raw_text, cells))

    @property
    def path(self):
        # this property exists so that the linter doesn't
        # have to have this logic
        return self.parent.path

    @property
    def steps(self):
        """Return a list of steps (statements that are not settings or comments)"""
        steps = []
        for statement in self.statements:
            if ((not statement.is_comment()) and
                (not statement.is_setting())):
                steps.append(statement)
        return steps

    @property
    def settings(self):
        """Return a list of settings (statements with cell[1] matching \[.*?\])

        Note: this returns any statement that *looks* like a setting. If you have
        a misspelled or completely bogus setting, it'll return that too
        (eg: | | [Blockumentation] | hello, world)
        """
        return [statement for statement in self.statements
                if (statement.is_setting() and not statement.is_comment())]

    @property
    def statements(self):
        """Return a list of statements

        This is done by joining together any rows that
        have continuations
        """
        # FIXME: no need to do this every time; we should cache the
        # result
        if len(self.rows) == 0:
            return []

        current_statement = Statement(self.rows[0])
        current_statement.startline = self.rows[0].linenumber
        current_statement.endline = self.rows[0].linenumber
        statements = []
        for row in self.rows[1:]:
            if len(row) > 1 and row[0] == "" and row[1] == "...":
                # we found a continuation
                current_statement += row[2:]
                current_statement.endline = row.linenumber
            else:
                if len(current_statement) > 0:
                    # append current statement to the list of statements...
                    statements.append(current_statement)
                # start a new statement
                current_statement = Statement(row)
                current_statement.startline = row.linenumber
                current_statement.endline = row.linenumber

        if len(current_statement) > 0:
            statements.append(current_statement)

        return statements


# TODO: make Row and Statement more similar -- either
# both should inherit from list, or neither should.
class Row(object):
    """A row is made up of a list of cells plus metadata"""
    def __init__(self, linenumber, raw_text, cells):
        self.linenumber = linenumber
        self.raw_text = raw_text
        self.cells = cells

    def dump(self):
        print("|" + " | ".join([cell.strip() for cell in self.cells]))
    def __len__(self):
        return len(self.cells)
    def __setitem__(self, key, value):
        self.cells[key] = value
        return self.cells[key]
    def __getitem__(self, key):
        return self.cells[key]
    def __repr__(self):
        return "<line: %s cells: %s>" % (self.linenumber, str(self.cells))
    def __contains__(self, key):
        return key in self.cells

class Comment(Row):
    # this isn't entirely correct or well thought out.
    # I need a way to capture comments rather than
    # throw them away (mainly so I can recreate the original
    # file from the parsed data)
    pass

class Statement(list):
    """A Statement is a list of cells, plus some metadata"""
    startline = None
    endline = None

    def is_setting(self):
        if ((len(self) > 1) and
            (re.match(r'\[.*?\]', self[1]))):
            return True
        return False

    def is_comment(self):
        '''Return True if the first non-empty cell starts with "#"'''

        for cell in self[:]:
            if cell == "":
                continue

            # this is the first non-empty cell. Check whether it is
            # a comment or not.
            if cell.lstrip().startswith("#"):
                return True
            else:
                return False
        return False

    def __repr__(self):
        return "(%.4s-%.4s)%s" % (self.startline, self.endline, list.__repr__(self))

from tables import SettingTable
from common import Row, Statement
import re

class Testcase(object):
    def __init__(self, parent, linenumber, name):
        self.linenumber = linenumber
        self.name = name
        self.rows = []
        self.parent = parent

    def append(self, linenumber, raw_text, cells):
        """Add another row of data from a test suite"""
        self.rows.append(Row(linenumber, raw_text, cells))

    @property 
    def is_templated(self):
        """Return True if the test is part of a suite that uses a Test Template"""
        for table in self.parent.tables:
            if isinstance(table, SettingTable):
                for row in table.rows:
                    if row[0].lower() == "test template":
                        return True
        return False

    @property
    def path(self):
        # this property exists so that the linter doesn't
        # have to have this logic 
        return self.parent.path

    @property
    def settings(self):
        '''Return a list of settings (statements with cell[1] matching \[.*?\])

        Note: this returns any statement that *looks* like a setting. If you have
        a misspelled or completely bogus setting, it'll return that too
        (eg: | | [Blockumentation] | hello, world)
        '''
        return [statement for statement in self.statements if statement.is_setting()]

    @property
    def steps(self):
        '''Return a list of steps (statements that are not settings or comments)'''
        steps = []
        for statement in self.statements:
            if ((not statement.is_comment()) and 
                (not statement.is_setting())):
                steps.append(statement)
        return steps

    @property
    def statements(self):
        '''Return a list of statements

        This is done by joining together any rows that
        have continuations
        '''
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

    # this is great, except that we don't return the line number
    # or character position of each tag. The linter needs that. :-(
    @property 
    def tags(self):
        tags = []
        for statement in self.statements:
            if len(statement) > 2 and statement[1].lower() == "[tags]":
                tags = tags + statement[2:]
        return tags
            

    def __repr__(self):
        # should this return the fully qualified name?
        return "<Testcase: %s>" % self.name


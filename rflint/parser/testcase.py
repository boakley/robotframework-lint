from .tables import SettingTable
from .common import Row, Statement, RobotStatements
import re


class Testcase(RobotStatements):
    def __init__(self, parent, linenumber, name):
        RobotStatements.__init__(self)
        self.linenumber = linenumber
        self.name = name
        self.rows = []
        self.parent = parent

    @property
    def is_templated(self):
        """Return True if the test is part of a suite that uses a Test Template"""
        for table in self.parent.tables:
            if isinstance(table, SettingTable):
                for row in table.rows:
                    if row[0].lower() == "test template":
                        return True
        return False

    # this is great, except that we don't return the line number
    # or character position of each tag. The linter needs that. :-(
    @property
    def tags(self):
        tags = []
        for statement in self.statements:
            if len(statement) > 2 and statement[1].lower() == "[tags]":
                for tag in statement[2:]:
                    if tag.startswith("#"):
                        # the start of a comment, so skip rest of the line
                        break
                    else:
                        tags.append(tag)
                break
        return tags

    def __repr__(self):
        # should this return the fully qualified name?
        return "<Testcase: %s>" % self.name

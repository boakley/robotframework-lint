import re

from rflint.common import ResourceRule

class InvalidTableInResource(ResourceRule):
    '''Verify that there are no invalid table headers'''
    valid_tables_re = None
    default_robot_level = "robot3"

    def configure(self, robot_level):
        valid_tables = ['comments?', 'settings?', 'keywords?', 'variables?']
        if robot_level == "robot2":
            valid_tables += ['metadata', 'user keywords?']
        self.valid_tables_re = re.compile('^(' + '|'.join(valid_tables) + ')$',
                                          re.I)

        if robot_level == "robot2":
            valid_tables += ['metadata', 'user keyword']
        self.valid_tables_re = re.compile('^(' + '|'.join(valid_tables) + ')$',
                                          re.I)

    def apply(self, resource):
        if not self.valid_tables_re:
            self.configure(self.default_robot_level)
        for table in resource.tables:
            if not self.valid_tables_re.match(table.name):
                self.report(resource, "Unknown table name '%s'" % table.name,
                            table.linenumber)

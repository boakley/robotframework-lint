from rflint.common import SuiteRule, ERROR, WARNING, normalize_name
from rflint.parser import SettingTable
import re

class PeriodInSuiteName(SuiteRule):
    '''Warn about periods in the suite name

    Since robot uses "." as a path separator, using a "." in a suite
    name can lead to ambiguity.
    '''
    severity = WARNING

    def apply(self,suite):
        if "." in suite.name:
            self.report(suite, "'.' in suite name '%s'" % suite.name, 0)

class InvalidTable(SuiteRule):
    '''Verify that there are no invalid table headers

    Parameter robot_level to be set to 'robot3' (default) or 'robot2'.'''
    valid_tables_re = None
    default_robot_level = "robot3"

    def configure(self, robot_level):
        valid_tables = ['comments?', 'settings?', 'tasks?', 'test cases?',
                        'keywords?', 'variables?']
        if robot_level == "robot2":
            valid_tables += ['cases?', 'metadata', 'user keywords?']
        self.valid_tables_re = re.compile('^(' + '|'.join(valid_tables) + ')$',
                                          re.I)

    def apply(self, suite):
        if not self.valid_tables_re:
            self.configure(self.default_robot_level)
        for table in suite.tables:
            if not self.valid_tables_re.match(table.name):
                self.report(suite, "Unknown table name '%s'" % table.name,
                            table.linenumber)


class DuplicateKeywordNames(SuiteRule):
    '''Verify that no keywords have a name of an existing keyword in the same file'''
    severity = ERROR

    def apply(self, suite):
        cache = []
        for keyword in suite.keywords:
            # normalize the name, so we catch things like
            # Smoke Test vs Smoke_Test, vs SmokeTest, which
            # robot thinks are all the same
            name = normalize_name(keyword.name)
            if name in cache:
                self.report(suite, "Duplicate keyword name '%s'" % keyword.name, keyword.linenumber)
            cache.append(name)

class DuplicateTestNames(SuiteRule):
    '''Verify that no tests have a name of an existing test in the same suite'''
    severity = ERROR

    def apply(self, suite):
        cache = []
        for testcase in suite.testcases:
            # normalize the name, so we catch things like
            # Smoke Test vs Smoke_Test, vs SmokeTest, which
            # robot thinks are all the same
            name = normalize_name(testcase.name)
            if name in cache:
                self.report(suite, "Duplicate testcase name '%s'" % testcase.name, testcase.linenumber)
            cache.append(name)

class RequireSuiteDocumentation(SuiteRule):
    '''Verify that a test suite has documentation'''
    severity=WARNING

    def apply(self, suite):
        for table in suite.tables:
            if isinstance(table, SettingTable):
                for row in table.rows:
                    if row[0].lower() == "documentation":
                        return
        # we never found documentation; find the first line of the first
        # settings table, default to the first line of the file
        linenum = 1
        for table in suite.tables:
            if isinstance(table, SettingTable):
                linenum = table.linenumber + 1
                break

        self.report(suite, "No suite documentation", linenum)

class TooManyTestCases(SuiteRule):
    '''
    Should not have too many tests in one suite.

    The exception is if they are data-driven.

    https://code.google.com/p/robotframework/wiki/HowToWriteGoodTestCases#Test_suite_structure

    You can configure the maximum number of tests. The default is 10.
    '''
    severity = WARNING
    max_allowed = 10

    def configure(self, max_allowed):
        self.max_allowed = int(max_allowed)

    def apply(self, suite):
        # check for template (data-driven tests)
        for table in suite.tables:
            if isinstance(table, SettingTable):
                for row in table.rows:
                    if row[0].lower() == "test template":
                        return
        # we didn't find a template, so these aren't data-driven
        testcases = list(suite.testcases)
        if len(testcases) > self.max_allowed:
            self.report(
                suite, "Too many test cases (%s > %s) in test suite"
                % (len(testcases), self.max_allowed), testcases[self.max_allowed].linenumber
            )

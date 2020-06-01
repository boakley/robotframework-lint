from rflint.common import TestRule, KeywordRule, GeneralRule, ERROR, WARNING

import re


class LineTooLong(GeneralRule):
    '''Check that a line is not too long (configurable; default=100)'''

    severity = WARNING
    maxchars = 100

    def configure(self, maxchars):
        self.maxchars = int(maxchars)

    def apply(self, robot_file):
        for linenumber, line in enumerate(robot_file.raw_text.splitlines()):
            if len(line) > self.maxchars:
                message = "Line is too long (exceeds %s characters)" % self.maxchars
                self.report(robot_file, message, linenumber+1, self.maxchars)

class TrailingBlankLines(GeneralRule):
    '''Check for multiple blank lines at the end of a file

    This is a configurable. The default value is 2.
    '''

    severity = WARNING
    max_allowed = 2

    def configure(self, max_allowed):
        self.max_allowed=int(max_allowed)

    def apply(self, robot_file):
        # I realize I'm making two full passes over the data, but
        # python is plenty fast enough. Even processing a file with
        # over six thousand lines, this takes a couple of
        # milliseconds.  Plenty fast enough for the intended use case,
        # since most files should be about two orders of magnitude
        # smaller than that.

        match=re.search(r'(\s*)$', robot_file.raw_text)
        if match:
            count = len(re.findall(r'\n', match.group(0)))
            if count > self.max_allowed:
                numlines = len(robot_file.raw_text.splitlines())
                message = "Too many trailing blank lines"
                linenumber = numlines-count
                self.report(robot_file, message, linenumber+self.max_allowed, 0)


class TrailingWhitespace(GeneralRule):
    severity = WARNING

    def apply(self, robot_file):
        for linenumber, line in enumerate(robot_file.raw_text.splitlines()):
            if len(line) != len(line.rstrip()):
                message = "Line has trailing whitespace"
                self.report(robot_file, message, linenumber+1)


class FileTooLong(GeneralRule):
    '''Verify the file has fewer lines than a given threshold.

    You can configure the maximum number of lines. The default is 300.
    '''

    severity = WARNING
    max_allowed = 300

    def configure(self, max_allowed):
        self.max_allowed = int(max_allowed)

    def apply(self, robot_file):
        lines = robot_file.raw_text.splitlines()
        if len(lines) > self.max_allowed:
            message = "File has too many lines (%s)" % len(lines)
            linenumber = self.max_allowed+1
            self.report(robot_file, message, linenumber, 0)

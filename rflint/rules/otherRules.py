from rflint.common import TestRule, KeywordRule, GeneralRule, ERROR, WARNING

class LineTooLong(GeneralRule):
    '''Check that a line is not too long (configurable; default=100)'''

    severity = WARNING
    maxchars = 100

    def configure(self, maxchars):
        self.maxchars = int(maxchars)

    def apply(self, robot_file):
        for linenumber, line in enumerate(robot_file.raw_text.split("\n")):
            if len(line) > self.maxchars:
                message = "Line is too long (exceeds %s characters)" % self.maxchars
                self.report(robot_file, message, linenumber+1, self.maxchars)
    
                


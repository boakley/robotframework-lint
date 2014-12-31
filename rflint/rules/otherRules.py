from rflint.common import TestRule, KeywordRule, GeneralRule, ERROR, WARNING

class LineTooLong(GeneralRule):
    severity = WARNING
    maxchars = 100

    def apply(self, robot_file):
        for linenumber, line in enumerate(robot_file.raw_text.split("\n")):
            if len(line) > self.maxchars:
                message = "Line is too long (exceeds %s characters)" % self.maxchars
                self.report(robot_file, message, linenumber+1, self.maxchars)
    
                


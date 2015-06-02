from rflint.common import GeneralRule

class Issue31(GeneralRule):
    def apply(self,robot_file):
        message = "the type is %s" % robot_file.type
        linenumber = 0
        self.report(robot_file, message, linenumber+1, 0)



from rflint.common import ResourceRule

class Issue30(ResourceRule):
    def configure(self, value):
        self.value = value

    def apply(self,resource):
        message = "the configured value is %s" % self.value
        self.report(resource, message, 0, 0)

from rflint.common import TestRule, KeywordRule, SuiteRule, GeneralRule

class CustomTestRule(TestRule):
    def apply(self, testcase):
        pass

class CustomSuiteRule(SuiteRule):
    def apply(self, suite):
        pass

class CustomGeneralRule(GeneralRule):
    def apply(self, suite):
        pass

class CustomKeywordRule(KeywordRule):
    def apply(self, keyword):
        pass


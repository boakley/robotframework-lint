'''
Copyright 2014 Bryan Oakley

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from rflint.common import TestRule, ERROR, WARNING
from rflint.parser import SettingTable


class PeriodInTestName(TestRule):
    '''Warn about periods in the testcase name
    
    Since robot uses "." as a path separator, using a "." in a testcase
    name can lead to ambiguity. 
    '''
    severity = WARNING
    
    def apply(self,testcase):
        if "." in testcase.name:
            self.report(testcase, "'.' in testcase name '%s'" % testcase.name, testcase.linenumber)

class TagWithSpaces(TestRule):
    '''Flags tags that have spaces in the tag name'''
    severity=ERROR

    def apply(self, testcase):
        for tag in testcase.tags:
            if ((" " in tag) or ("\t" in tag)):
                self.report(testcase, "space not allowed in tag name: '%s'" % tag, testcase.linenumber)

class RequireTestDocumentation(TestRule):
    '''Verify that a test suite has documentation

    This rule is not enforced for data driven tests ("Test Template" in Settings)
    '''
    severity=ERROR

    def apply(self, testcase):
        if testcase.is_templated:
            return

        for setting in testcase.settings:
            if setting[1].lower() == "[documentation]" and len(setting) > 2:
                return

        # set the line number to the line immediately after the testcase name
        self.report(testcase, "No testcase documentation", testcase.linenumber+1)

class TooFewTestSteps(TestRule):
    '''Tests should have at least a minimum number of steps

    This rule is configurable. The default number of required steps is 2.
    '''

    min_required = 2

    def configure(self, min_required):
        self.min_required = int(min_required)

    def apply(self, testcase):
        if testcase.is_templated:
            return

        # ignore empty test steps
        steps = [step for step in testcase.steps if not (len(step) == 1
                                                         and not step[0])]
        if len(steps) < self.min_required:
            msg = "Too few steps (%s) in test case" % len(steps)
            self.report(testcase, msg,  testcase.linenumber)

class TooManyTestSteps(TestRule):
    '''Workflow tests should have no more than ten steps.

    https://code.google.com/p/robotframework/wiki/HowToWriteGoodTestCases#Workflow_tests
    '''

    severity=WARNING
    max_allowed = 10

    def configure(self, max_allowed):
        self.max_allowed = int(max_allowed)

    def apply(self, testcase):
        if testcase.is_templated:
            return

        # ignore empty test steps
        steps = [step for step in testcase.steps if not (len(step) == 1
                                                         and not step[0])]
        if len(steps) > self.max_allowed:
            self.report(testcase,
                        "Too many steps (%s) in test case" % len(steps),
                        steps[self.max_allowed].startline)

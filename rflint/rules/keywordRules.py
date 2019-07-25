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

from rflint.common import KeywordRule, ERROR
from rflint.parser import SettingTable

class RequireKeywordDocumentation(KeywordRule):
    '''Verify that a keyword has documentation'''
    severity=ERROR

    def apply(self, keyword):
        for setting in keyword.settings:
            if setting[1].lower() == "[documentation]" and len(setting) > 2:
                return

        # set the line number to the line immediately after the keyword name
        self.report(keyword, "No keyword documentation", keyword.linenumber+1)


class TooFewKeywordSteps(KeywordRule):
    '''Keywords should have at least a minimum number of steps

    This rule is configurable. The default number of required steps is 2.
    '''

    min_required = 2

    def configure(self, min_required):
        self.min_required = int(min_required)

    def apply(self, keyword):
        # ignore empty steps
        steps = [step for step in keyword.steps if not (len(step) == 1 and not step[0])]
        if len(steps) < self.min_required:
            msg = "Too few steps (%s) in keyword" % len(steps)
            self.report(keyword, msg, keyword.linenumber)

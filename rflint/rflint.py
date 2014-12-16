"""
rflint - a lint-like tool for robot framework plain text files

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

"""

import os
import sys
import glob
import argparse
import imp

from .common import SuiteRule, TestRule, KeywordRule, GeneralRule, Rule
from .common import ERROR, WARNING, IGNORE
from version import __version__
from parser import RobotFileFactory

from robot.utils.argumentparser import ArgFileParser

class RfLint(object):
    """Robot Framework Linter"""

    def __init__(self):
        here = os.path.abspath(os.path.dirname(__file__))
        builtin_rules = os.path.join(here, "rules")
        site_rules = os.path.join(here, "site-rules")
        for path in (builtin_rules, site_rules):
            for filename in glob.glob(path+"/*.py"):
                if filename.endswith(".__init__.py"):
                    continue
                self._load_rule_file(filename)

    def run(self, args):
        """Parse command line arguments, and run rflint"""

        self.suite_rules = self._get_rules(SuiteRule)
        self.testcase_rules = self._get_rules(TestRule)
        self.keyword_rules = self._get_rules(KeywordRule)
        self.general_rules = self._get_rules(GeneralRule)

        self.all_rules = self.suite_rules + self.testcase_rules + self.keyword_rules + self.general_rules

        self.args = self.parse_and_process_args(args)

        if self.args.version:
            print __version__
            sys.exit(0)
            
        if self.args.rulefile:
            for filename in self.args.rulefile:
                self._load_rule_file(filename)

        if self.args.list:
            self.list_rules()
            sys.exit(0)
        
        self.counts = { ERROR: 0, WARNING: 0, "other": 0}
            
        for filename in self.args.args:
            if not (os.path.exists(filename)):
                sys.stderr.write("rflint: %s: No such file or directory\n" % filename)
                continue
            if not (self.args.no_filenames):
                print "+ "+filename
            suite = RobotFileFactory(filename)
            for rule in self.suite_rules:
                if rule.severity != IGNORE:
                    rule.apply(suite)
            for testcase in suite.testcases:
                for rule in self.testcase_rules:
                    if rule.severity != IGNORE:
                        rule.apply(testcase)
            for keyword in suite.keywords:
                for rule in self.keyword_rules:
                    if rule.severity != IGNORE:
                        rule.apply(keyword)

        if self.counts[ERROR] > 0:
            sys.exit(self.counts[ERROR] if self.counts[ERROR] < 254 else 255)
        sys.exit(0)

    def list_rules(self):
        """Print a list of all rules"""
        all_rules = [repr(x) for x in self.suite_rules] + \
                    [repr(x) for x in self.testcase_rules] + \
                    [repr(x) for x in self.keyword_rules] + \
                    [repr(x) for x in self.general_rules] 

        print "\n".join(sorted([repr(x) for x in all_rules], 
                               key=lambda s: s[2:]))

    def report(self, linenumber, filename, severity, message, rulename, char):
        if severity in (WARNING, ERROR):
            self.counts[severity] += 1
        else:
            self.counts["other"] += 1

        print self.args.format.format(linenumber=linenumber, filename=filename, 
                                      severity=severity, message=message,
                                      rulename = rulename, char=char)
    def _get_rules(self, cls):
        """Returns a list of rules of a given class"""
        result = []
        for rule_class in cls.__subclasses__():
            rule_name = rule_class.__name__.lower()
            result.append(rule_class(self))

        return result

    def _load_rule_file(self, filename):
        '''Import the given rule file'''
        if not (os.path.exists(filename)):
            sys.stderr.write("rflint: %s: No such file or directory\n" % filename)
            return
        try:
            basename = os.path.basename(filename)
            (name, ext) = os.path.splitext(basename)
            imp.load_source(name, filename)
        except Exception as e:
            sys.stderr.write("rflint: %s: exception while loading: %s\n" % (filename, str(e)))

    def parse_and_process_args(self, args):
        """Handle the parsing of command line arguments."""

        parser = argparse.ArgumentParser(
            prog="python -m rflint",
            description="A style checker for robot framework plain text files",
            epilog = (
                "You can use 'all' in place of <RuleName> to refer to all rules. "
                "For example: '--ignore all --warn DuplicateTestNames' will ignore all rules "
                "except DuplicateTestNames."
                "  "
                "FORMAT is a string that performs a substitution on the following "
                "patterns: {severity}, {linenumber}, {char}, {message}, and {rulename}. "
                "For example: --format 'line: {linenumber}: message: {message}'. "
                )
            )
        parser.add_argument("--error", "-e", metavar="<RuleName>", action=SetErrorAction,
                            help="Assign a severity of ERROR to the given RuleName")
        parser.add_argument("--ignore", "-i", metavar="<RuleName>", action=SetIgnoreAction,
                            help="Ignore the given RuleName")
        parser.add_argument("--warning", "-w", metavar="<RuleName>", action=SetWarningAction,
                            help="Assign a severity of WARNING for the given RuleName")
        parser.add_argument("--list", "-l", action="store_true",
                            help="show a list of known rules, then exit")
        parser.add_argument("--no-filenames", action="store_true",
                            help="suppress the printing of filenames")
        parser.add_argument("--format", "-f", 
                            help="Define the output format",
                            default='{severity}: {linenumber}, {char}: {message} ({rulename})')
        parser.add_argument("--version", action="store_true", default=False,
                            help="Display version number and exit")
        parser.add_argument("--rulefile", "-R", action="append",
                            help="import additional rules from the given RULEFILE")
        parser.add_argument("--argumentfile", "-A", action=ArgfileLoader)
        parser.add_argument('args', metavar="<filenames>", nargs=argparse.REMAINDER)

        # create a custom namespace, in which we can store a reference to
        # our rules. This lets the custom argument actions access the list
        # of rules
        ns = argparse.Namespace()
        setattr(ns, "_rules", self.all_rules)
        args = parser.parse_args(args, ns)

        Rule.output_format = args.format

        return args
        
class SetWarningAction(argparse.Action):
    '''Called when the argument parser encounters --warning'''
    def __call__(self, parser, namespace, rulename, option_string = None):
        for rule in getattr(namespace, "_rules"):
            if rulename == rule.name or rulename == "all":
                rule.severity = WARNING

class SetErrorAction(argparse.Action):
    '''Called when the argument parser encounters --error'''
    def __call__(self, parser, namespace, rulename, option_string = None):
        for rule in getattr(namespace, "_rules"):
            if rulename == rule.name or rulename == "all":
                rule.severity = ERROR

class SetIgnoreAction(argparse.Action):
    '''Called when the argument parser encounters --ignore'''
    def __call__(self, parser, namespace, rulename, option_string = None):
        for rule in getattr(namespace, "_rules"):
            if rulename == rule.name or rulename == "all":
                rule.severity = IGNORE

class ArgfileLoader(argparse.Action):
    '''Called when the argument parser encounters --argumentfile'''
    def __call__ (self, parser, namespace, values, option_string = None):
        ap = ArgFileParser(["--argumentfile","-A"])
        args = ap.process(["-A", values])
        parser.parse_args(args, namespace)

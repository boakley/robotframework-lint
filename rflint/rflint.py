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
            if os.path.isdir(filename):
                self._process_folder(filename)
            else:
                self._process_file(filename)

        if self.counts[ERROR] > 0:
            sys.exit(self.counts[ERROR] if self.counts[ERROR] < 254 else 255)
        sys.exit(0)

    def _process_folder(self, path):
        for root, dirs, files in os.walk(path):
            for filename in files:
                name, ext = os.path.splitext(filename)
                if ext.lower() in (".robot", ".txt", ".tsv"):
                    self._process_file(os.path.join(root, filename))
            if self.args.recursive:
                for dirname in dirs:
                    self._process_folder(os.path.join(root, dirname))
 
    def _process_file(self, filename):
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

    def list_rules(self):
        """Print a list of all rules"""
        all_rules = self.suite_rules + self.testcase_rules + self.keyword_rules + self.general_rules
        for rule in sorted(all_rules, key=lambda rule: rule.name):
            print rule
            if self.args.verbose:
                for line in rule.doc.split("\n"):
                    print "    ", line

    def report(self, linenumber, filename, severity, message, rulename, char):
        '''Report a rule violation'''
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
            description="A style checker for robot framework plain text files.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog = (
                "You can use 'all' in place of RULENAME to refer to all rules. \n"
                "\n"
                "For example: '--ignore all --warn DuplicateTestNames' will ignore all\n"
                "rules except DuplicateTestNames.\n"
                "\n"
                "FORMAT is a string that performs a substitution on the following \n"
                "patterns: {severity}, {linenumber}, {char}, {message}, and {rulename}.\n"
                "\n"
                "For example: --format 'line: {linenumber}: message: {message}'. \n"
                "\n"
                "ARGUMENTFILE is a filename with contents that match the format of \n"
                "standard robot framework argument files\n"
                "\n"
                "If you give a directory as an argument, all files in the directory\n"
                "with the suffix .txt, .robot or .tsv will be processed. With the \n"
                "--recursive option, subfolders within the directory will also be\n"
                "processed."
                )
            )
        parser.add_argument("--error", "-e", metavar="RULENAME", action=SetErrorAction,
                            help="Assign a severity of ERROR to the given RULENAME")
        parser.add_argument("--ignore", "-i", metavar="RULENAME", action=SetIgnoreAction,
                            help="Ignore the given RULENAME")
        parser.add_argument("--warning", "-w", metavar="RULENAME", action=SetWarningAction,
                            help="Assign a severity of WARNING for the given RULENAME")
        parser.add_argument("--list", "-l", action="store_true",
                            help="show a list of known rules and exit")
        parser.add_argument("--no-filenames", action="store_true",
                            help="suppress the printing of filenames")
        parser.add_argument("--format", "-f", 
                            help="Define the output format",
                            default='{severity}: {linenumber}, {char}: {message} ({rulename})')
        parser.add_argument("--version", action="store_true", default=False,
                            help="Display version number and exit")
        parser.add_argument("--verbose", "-v", action="store_true", default=False,
                            help="Give verbose output")
        parser.add_argument("--recursive", "-r", action="store_true", default=False,
                            help="Recursively scan subfolders in a directory")
        parser.add_argument("--rulefile", "-R", action="append",
                            help="import additional rules from the given RULEFILE")
        parser.add_argument("--argumentfile", "-A", action=ArgfileLoader,
                            help="read arguments from the given file")
        parser.add_argument('args', metavar="file", nargs=argparse.REMAINDER)

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

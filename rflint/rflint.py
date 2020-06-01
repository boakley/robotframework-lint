"""
rflint - a lint-like tool for robot framework plain text files

Copyright 2014-2015 Bryan Oakley

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
from __future__ import print_function

import os
import sys
import glob
import argparse
import imp

from .common import SuiteRule, ResourceRule, TestRule, KeywordRule, GeneralRule, Rule
from .common import ERROR, WARNING, IGNORE
from .version import __version__
from .parser import RobotFactory, SuiteFile, ResourceFile
from .exceptions import UnknownRuleException

from robot.utils.argumentparser import ArgFileParser

# Used to track which files have already been imported
IMPORTED_RULE_FILES = []


class RfLint(object):
    """Robot Framework Linter"""

    def __init__(self):
        here = os.path.abspath(os.path.dirname(__file__))
        builtin_rules = os.path.join(here, "rules")
        site_rules = os.path.join(here, "site-rules")

        # mapping of class names to instances, to enable us to
        # instantiate each rule exactly once
        self._rules = {}

        for path in (builtin_rules, site_rules):
            for filename in glob.glob(path+"/*.py"):
                if filename.endswith(".__init__.py"):
                    continue
                self._load_rule_file(filename)

    @property
    def suite_rules(self):
        return self._get_rules(SuiteRule)

    @property
    def resource_rules(self):
        return self._get_rules(ResourceRule)

    @property
    def testcase_rules(self):
        return self._get_rules(TestRule)

    @property
    def keyword_rules(self):
        return self._get_rules(KeywordRule)

    @property
    def general_rules(self):
        return self._get_rules(GeneralRule)

    @property
    def all_rules(self):
        all = self.suite_rules + self.resource_rules + self.testcase_rules + self.keyword_rules + self.general_rules
        return all

    def run(self, args):
        """Parse command line arguments, and run rflint"""

        self.args = self.parse_and_process_args(args)

        if self.args.version:
            print(__version__)
            return 0

        if self.args.rulefile:
            for filename in self.args.rulefile:
                self._load_rule_file(filename)

        if self.args.list:
            self.list_rules()
            return 0

        if self.args.describe:
            self._describe_rules(self.args.args)
            return 0

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
            return self.counts[ERROR] if self.counts[ERROR] < 254 else 255

        return 0

    def _is_valid_rule(self, rule_name):
        for rule in self.all_rules:
            if rule_name.lower() == rule.name.lower():
                return True
        return False

    def _describe_rules(self, rule_names):
        for rulename in rule_names:
            if not self._is_valid_rule(rulename):
                raise UnknownRuleException(rulename)

        requested_rules = [rule.strip().lower() for rule in rule_names]
        for rule in sorted(self.all_rules, key=lambda rule: rule.name):
            if rule.name.lower() in requested_rules or len(requested_rules) == 0:
                print(rule.name)
                for line in rule.doc.splitlines():
                    print("    " + line)

    def _process_folder(self, path):
        if self.args.recursive:
            for root, subdirs, filenames in os.walk(path):
                self._process_files(root, filenames)
        else:
            self._process_files(path, os.listdir(path))

    def _process_files(self, folder, filenames):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext.lower() in (".robot", ".txt", ".tsv", ".resource"):
                self._process_file(os.path.join(folder, filename))

    def _process_file(self, filename):
        # this is used by the reporting mechanism to know if it
        # should print the filename. Once it has been printed it
        # will be reset so that it won't get printed again until
        # we process the next file.
        self._print_filename = filename if self.args.print_filenames else None

        robot_file = RobotFactory(filename)
        for rule in self.general_rules:
            if rule.severity != IGNORE:
                rule.apply(robot_file)

        if isinstance(robot_file, SuiteFile):
            for rule in self.suite_rules:
                if rule.severity != IGNORE:
                    rule.apply(robot_file)
            for testcase in robot_file.testcases:
                for rule in self.testcase_rules:
                    if rule.severity != IGNORE:
                        rule.apply(testcase)

        if isinstance(robot_file, ResourceFile):
            for rule in self.resource_rules:
                if rule.severity != IGNORE:
                    rule.apply(robot_file)

        for keyword in robot_file.keywords:
            for rule in self.keyword_rules:
                if rule.severity != IGNORE:
                    rule.apply(keyword)

    def list_rules(self):
        """Print a list of all rules"""
        for rule in sorted(self.all_rules, key=lambda rule: rule.name):
            print(rule)
            if self.args.verbose:
                for line in rule.doc.splitlines():
                    print("    ", line)

    def report(self, linenumber, filename, severity, message, rulename, char):
        """Report a rule violation"""

        if self._print_filename is not None:
            # we print the filename only once. self._print_filename
            # will get reset each time a new file is processed.
            print("+ " + self._print_filename)
            self._print_filename = None

        if severity in (WARNING, ERROR):
            self.counts[severity] += 1
        else:
            self.counts["other"] += 1

        if sys.version_info[0] == 2:
            # I _really_ hate doing this, but I can't figure out a
            # better way to handle unicode such that it works both
            # in python 2 and 3. There must be a better way, but
            # my unicode fu is weak.
            message = message.encode('utf-8')

        print(self.args.format.format(linenumber=linenumber, filename=filename,
                                      severity=severity, message=message,
                                      rulename=rulename, char=char))

    def _get_rules(self, cls):
        """Returns a list of rules of a given class

        Rules are treated as singletons - we only instantiate each
        rule once.
        """

        result = []
        for rule_class in cls.__subclasses__():
            rule_name = rule_class.__name__.lower()
            if rule_name not in self._rules:
                rule = rule_class(self)
                self._rules[rule_name] = rule
            result.append(self._rules[rule_name])
        return result

    def _load_rule_file(self, filename):
        """Import the given rule file"""
        abspath = os.path.abspath(filename)
        if abspath in IMPORTED_RULE_FILES:
            return
        if not (os.path.exists(filename)):
            sys.stderr.write("rflint: %s: No such file or directory\n" % filename)
            return
        try:
            basename = os.path.basename(filename)
            (name, ext) = os.path.splitext(basename)
            imp.load_source(name, filename)
            IMPORTED_RULE_FILES.append(abspath)
        except Exception as e:
            sys.stderr.write("rflint: %s: exception while loading: %s\n" % (filename, str(e)))

    def parse_and_process_args(self, args):
        """Handle the parsing of command line arguments."""

        parser = argparse.ArgumentParser(
            prog="python -m rflint",
            description="A static analyzer for robot framework plain text files.",
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
                "with the suffix .txt, .robot, .resource, or .tsv will be processed. \n"
                "With the --recursive option, subfolders within the directory will \n"
                "also be processed."
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
        parser.add_argument("--describe", "-d", action="store_true",
                            help="describe the given rules")
        parser.add_argument("--no-filenames", action="store_false", dest="print_filenames",
                            default=True,
                            help="suppress the printing of filenames")
        parser.add_argument("--format", "-f",
                            help="Define the output format",
                            default='{severity}: {linenumber}, {char}: {message} ({rulename})')
        parser.add_argument("--version", action="store_true", default=False,
                            help="Display version number and exit")
        parser.add_argument("--verbose", "-v", action="store_true", default=False,
                            help="Give verbose output")
        parser.add_argument("--configure", "-c", action=ConfigureAction,
                            help="Configure a rule")
        parser.add_argument("--recursive", "-r", action="store_true", default=False,
                            help="Recursively scan subfolders in a directory")
        parser.add_argument("--rulefile", "-R", action=RulefileAction,
                            help="import additional rules from the given RULEFILE")
        parser.add_argument("--argumentfile", "-A", action=ArgfileLoader,
                            help="read arguments from the given file")
        parser.add_argument('args', metavar="file", nargs=argparse.REMAINDER)

        # create a custom namespace, in which we can store a reference to
        # our rules. This lets the custom argument actions access the list
        # of rules
        ns = argparse.Namespace()
        setattr(ns, "app", self)
        args = parser.parse_args(args, ns)

        Rule.output_format = args.format

        return args


class RulefileAction(argparse.Action):
    def __call__(self, parser, namespace, arg, option_string=None):
        app = getattr(namespace, "app")
        app._load_rule_file(arg)


class ConfigureAction(argparse.Action):
    def __call__(self, parser, namespace, arg, option_string=None):
        rulename, argstring = arg.split(":", 1)
        args = argstring.split(":")
        app = getattr(namespace, "app")

        for rule in app.all_rules:
            if rulename == rule.name:
                rule.configure(*args)
                return
        raise UnknownRuleException(rulename)


class SetStatusAction(argparse.Action):
    """Abstract class which provides a method for checking the rule name"""
    def check_rule_name(self, rulename, rules):
        if (rulename != "all" and
            rulename.lower() not in [rule.name.lower() for rule in rules]):
            raise UnknownRuleException(rulename)


class SetWarningAction(SetStatusAction):
    """Called when the argument parser encounters --warning"""
    def __call__(self, parser, namespace, rulename, option_string = None):

        app = getattr(namespace, "app")
        self.check_rule_name(rulename, app.all_rules)

        for rule in app.all_rules:
            if rulename == rule.name or rulename == "all":
                rule.severity = WARNING


class SetErrorAction(SetStatusAction):
    """Called when the argument parser encounters --error"""
    def __call__(self, parser, namespace, rulename, option_string = None):

        app = getattr(namespace, "app")
        self.check_rule_name(rulename, app.all_rules)

        for rule in app.all_rules:
            if rulename == rule.name or rulename == "all":
                rule.severity = ERROR


class SetIgnoreAction(SetStatusAction):
    """Called when the argument parser encounters --ignore"""
    def __call__(self, parser, namespace, rulename, option_string = None):

        app = getattr(namespace, "app")
        self.check_rule_name(rulename, app.all_rules)

        for rule in app.all_rules:
            if rulename == rule.name or rulename == "all":
                rule.severity = IGNORE


class ArgfileLoader(argparse.Action):
    """Called when the argument parser encounters --argumentfile"""
    def __call__ (self, parser, namespace, values, option_string = None):
        ap = ArgFileParser(["--argumentfile","-A"])
        args = ap.process(["-A", values])
        parser.parse_args(args, namespace)

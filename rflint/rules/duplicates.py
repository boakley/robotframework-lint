from rflint.common import SuiteRule, ResourceRule, ERROR, normalize_name

def check_duplicates(report_duplicate, table,
                     permitted_dups=None, normalize_itemname=normalize_name):
    # `table` is a SettingsTable or a VariableTable; either contains rows,
    # but only VariableTable also contains statements.
    seen_rows = {}
    for row in table.rows:
        item = normalize_itemname(row[0])

        # skip empty lines, comments and continuation lines
        if item == "":
            continue
        if item.startswith("#"):
            continue
        if item.startswith("..."):
            continue

        # some tables allow duplicates
        if permitted_dups and item in permitted_dups:
            continue

        if item in seen_rows:
            prev_row = seen_rows[item]
            report_duplicate(row, prev_row)
        else:
            seen_rows[item] = row


class DuplicateSettingsCommon(object):
    '''Verify that settings are not repeated in a Settings table

    This has been made an error in Robot3.0
    https://github.com/robotframework/robotframework/issues/2204'''
    severity = ERROR

    def apply(self, suite):
        def report_duplicate_setting(setting, prev_setting):
            self.report(suite,
                "Setting '%s' used multiple times (previously used line %d)" % \
                (setting[0], prev_setting.linenumber), setting.linenumber)

        for table in suite.tables:
            if table.name == "Settings":
                check_duplicates(report_duplicate_setting, table,
                    permitted_dups=["library", "resource", "variables"])

class DuplicateSettingsInSuite(DuplicateSettingsCommon, SuiteRule):
    pass

class DuplicateSettingsInResource(DuplicateSettingsCommon, ResourceRule):
    pass


def strip_variable_name(varname):
    return varname.lstrip("${").rstrip("}= ")

def normalize_variable_name(varname):
    return normalize_name(strip_variable_name(varname))

class DuplicateVariablesCommon(object):
    '''Verify that variables are not defined twice in the same table

    This is not an error, but leads to surprising result (first definition
    wins, later is ignored).'''
    def apply(self, suite):
        def report_duplicate_variable(variable, prev_variable):
            self.report(suite,
                "Variable '%s' defined twice, previous definition line %d" % \
                (strip_variable_name(variable[0]), prev_variable.linenumber),
                variable.linenumber)

        for table in suite.tables:
            if table.name == "Variables":
                check_duplicates(report_duplicate_variable, table,
                                 normalize_itemname=normalize_variable_name)

class DuplicateVariablesInSuite(DuplicateVariablesCommon, SuiteRule):
    pass

class DuplicateVariablesInResource(DuplicateVariablesCommon, ResourceRule):
    pass

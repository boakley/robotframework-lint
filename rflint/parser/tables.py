class RobotTable(object):
    '''A table made up of zero or more rows'''
    def __init__(self, parent, linenumber=0, name=None):
        self.linenumber = linenumber
        self.name = name
        self.rows = []
        self.comments = []
        self.parent = parent

    def dump(self):
        for row in self.rows:
            print "| " + " | ".join(row)

    def append(self, row):
        self.rows.append(row)

    def __str__(self):
        if self.name is None:
            return "None"
        else:
            return self.name

    def __repr__(self):
        return "<%s(linenumbmer=%s, name=\"%s\")>" % (self.__class__.__name__, self.linenumber, self.name)

class DefaultTable(RobotTable): pass  # the table with no name
class UnknownTable(RobotTable): pass  # a table with an 
class SettingTable(RobotTable): pass
class VariableTable(RobotTable): pass
class MetadataTable(RobotTable): pass

class AbstractContainerTable(RobotTable):
    '''Parent class of Keyword and Testcase tables'''
    _childClass = None
    def __init__(self, parent, *args, **kwargs):
        if self._childClass is None:
            # hey! Don't try to instantiate this class directly.
            raise Exception("D'oh! This is an abstract class.")
        super(AbstractContainerTable, self).__init__(parent, *args, **kwargs)
        self._children = []
        self.parent = parent

    def dump(self):
        for child in self._children:
            print "| " + child.name
            for row in child.rows:
                row.dump()

    def append(self, row):
        ''' 
        The idea is, we recognize when we have a new testcase by 
        checking the first cell. If it's not empty, we have a new
        test case.

        '''
        if len(row) == 0:
            # blank line. Should we throw it away, or append a BlankLine object?
            return

        if row[0] != "":
            # we have a new child table
            self._children.append(self._childClass(self.parent, row.linenumber, row[0]))
            if len(row.cells) > 1:
                # It appears the first row -- which contains the test case or
                # keyword name -- also has the first logical row of cells.
                # We'll create a Row, but we'll make the first cell empty instead
                # of leaving the name in it, since other code always assumes the
                # first cell is empty. 
                #
                # To be honest, I'm not sure this is the Right Thing To Do, but 
                # I'm too lazy to audit the code to see if it matters if we keep 
                # the first cell intact. Sorry if this ends up causing you grief
                # some day...
                row[0] = ""
                self._children[-1].append(row.linenumber, row, row.cells)

        elif len(self._children) == 0:
            # something before the first test case
            # For now, append it to self.comments; eventually we should flag
            # an error if it's NOT a comment
            self.comments.append(row)

        else:
            # another row for the testcase
            if len(row.cells) > 0:
                self._children[-1].append(row.linenumber, row, row.cells)



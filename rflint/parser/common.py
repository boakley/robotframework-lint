# TODO: make Row and Statement more similar -- either
# both should inherit from list, or neither should. 
class Row(object):
    '''A row is made up of a list of cells plus metadata'''
    def __init__(self, linenumber, raw_text, cells):
        self.linenumber = linenumber
        self.raw_text = raw_text
        self.cells = cells

    def dump(self):
        print "|" + " | ".join([cell.strip() for cell in self.cells])
    def __len__(self):
        return len(self.cells)
    def __setitem__(self, key, value):
        self.cells[key] = value
        return self.cells[key]
    def __getitem__(self, key):
        return self.cells[key]
    def __repr__(self):
        return "<line: %s cells: %s>" % (self.linenumber, str(self.cells))

class Comment(Row):
    # this isn't entirely correct or well thought out. 
    # I need a way to capture comments rather than 
    # throw them away (mainly so I can recreate the original
    # file from the parsed data)
    pass

class Statement(list):
    '''A Statement is a list of cells, plus some metadata'''
    startline = None
    endline = None

    def __repr__(self):
        return "(%.4s-%.4s)%s" % (self.startline, self.endline, list.__repr__(self))


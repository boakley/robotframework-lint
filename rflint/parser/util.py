from __future__ import print_function

import time
import re

class Matcher(object):
    '''A convenience class for regular expression matching

    Example:
        match = Matcher(re.IGNORECASE)
        if match(pattern1, string):
            print match.group(1)
        elif match(pattern2, string):
            print match.group(1)
        ...
    '''

    def __init__(self, flags=None):
        self.flags = flags

    def __call__(self, pattern, string, flags=None):
        if flags is None:
            self.result = re.match(pattern, string, flags=self.flags)
        else:
            self.result = re.match(pattern, string)
        return self.result

    def __getattr__(self, attr):
        return getattr(self.result, attr)


def timeit(func):
    def wrapper(*arg, **kw):
        '''source: http://www.daniweb.com/code/snippet368.html'''
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        print(func.__name__, ":", int(1000*(t2-t1)), "ms")
        return res
    return wrapper


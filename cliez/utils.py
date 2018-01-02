import os
import sys


def include_file(filename, global_vars=None, local_vars=None):
    """
    .. deprecated 2.1::
        Don't use this any more.

        It's not pythonic.


    include file like php include.

    include is very useful when we need to split large config file
    """
    if global_vars is None:
        global_vars = sys._getframe(1).f_globals
    if local_vars is None:
        local_vars = sys._getframe(1).f_locals

    with open(filename, 'r') as f:
        code = compile(f.read(), os.path.basename(filename), 'exec')
        exec(code, global_vars, local_vars)
        pass


def hump_to_underscore(name):
    """
    Convert Hump style to underscore

    :param name: Hump Character
    :return: str
    """
    new_name = ''

    pos = 0
    for c in name:
        if pos == 0:
            new_name = c.lower()
        elif 65 <= ord(c) <= 90:
            new_name += '_' + c.lower()
            pass
        else:
            new_name += c
        pos += 1
        pass
    return new_name



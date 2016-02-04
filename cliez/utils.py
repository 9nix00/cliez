# -*- coding: utf-8 -*-

import os
import sys


def include_file(filename, global_vars=None, local_vars=None):
    """
    include file like php include.

    include is very useful when we need to split large config file

    :param filename:
    :param global_vars:
    :param local_vars:
    :return:
    """
    if global_vars is None:
        global_vars = sys._getframe(1).f_globals
    if local_vars is None:
        local_vars = sys._getframe(1).f_locals

    with open(filename, 'r') as f:
        code = compile(f.read(), os.path.basename(filename), 'exec')
        exec(code, global_vars, local_vars)

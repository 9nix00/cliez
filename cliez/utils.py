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


def append_arguments(klass, sub_parsers, default_epilog, general_arguments):
    """
    Add class options to argparser options.

    :param cliez.component.Component klass: subclass of Component
    :param Namespace sub_parsers:
    :param str default_epilog: default_epilog
    :param list general_arguments: global options, defined by user
    :return: None
    """

    entry_name = hump_to_underscore(klass.__name__).replace(
        '_component',
        '')

    # set sub command document
    epilog = default_epilog if default_epilog \
        else 'This tool generate by `cliez` ' \
             'https://www.github.com/wangwenpei/cliez'

    sub_parser = sub_parsers.add_parser(entry_name, help=klass.__doc__,
                                        epilog=epilog)
    sub_parser.description = klass.add_arguments.__doc__

    # add slot arguments
    if hasattr(klass, 'add_slot_args'):
        slot_args = klass.add_slot_args() or []
        for v in slot_args:
            sub_parser.add_argument(*v[0], **v[1])
        sub_parser.description = klass.add_slot_args.__doc__
        pass

    user_arguments = klass.add_arguments() or []

    for v in user_arguments:
        sub_parser.add_argument(*v[0], **v[1])

    if not klass.exclude_global_option:
        for v in general_arguments:
            sub_parser.add_argument(*v[0], **v[1])

    pass

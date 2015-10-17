# -*- coding: utf-8 -*-

import sys
import os
import importlib


def command_list(root):
    if root is None:
        sys.stderr.write("cliez.conf.PACKAGE_ROOT not set.\n")
        sys.exit(2)
        pass

    if not os.path.exists(root):
        sys.stderr.write("please set a valid path for `cliez.conf.PACKAGE_ROOT`\n")
        sys.exit(2)
        pass

    path = os.listdir(os.path.join(root, 'component'))
    return [f[:-3] for f in path if f.endswith('.py') and f != '__init__.py']


def parse(parser, argv=sys.argv):
    """
    ...todo::
        support pkg_resources

    :return:
    """

    from cliez.conf import PACKAGE_ROOT
    commands = command_list(PACKAGE_ROOT)

    # skip load all component to improve performance
    if not argv:
        raise ValueError("argv can't be null")
    elif len(argv) == 1 or (len(argv) == 2 and argv[1] in ['-h', '--help']):
        parser.usage = '{} [options] <command>'.format(os.path.basename(argv[0]))
        parser.print_help()
        sys.exit(0)
    elif len(argv) == 2 and argv[1] not in commands:
        if not parser.description:
            sub_parsers = parser.add_subparsers()
            [sub_parsers.add_parser(v) for v in commands]
            pass
        pass
        parser.print_help()
        parser.error("invalid argument")
    else:
        sub_parsers = parser.add_subparsers()
        class_name = argv[1].capitalize() + 'Component'
        mod = importlib.import_module('component.{}'.format(argv[1]), package=os.path.basename(PACKAGE_ROOT))
        klass = getattr(mod, class_name)
        klass.append_arguments(sub_parsers)
        pass
    options = parser.parse_args(argv[1:])
    obj = klass(parser)
    obj.run(options)
    pass

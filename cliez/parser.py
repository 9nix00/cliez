# -*- coding: utf-8 -*-

import sys
import os
import importlib
import logging
from cliez.conf import Settings


def command_list():
    """
    find sub-parser full list.
    depends on `cliez.COMPONENT_ROOT` path

    :return: `list` matched sub-parser
    """
    from cliez.conf import COMPONENT_ROOT

    root = COMPONENT_ROOT

    if root is None:
        sys.stderr.write("cliez.conf.COMPONENT_ROOT not set.\n")
        sys.exit(2)
        pass

    if not os.path.exists(root):
        sys.stderr.write("please set a valid path for `cliez.conf.COMPONENT_ROOT`\n")
        sys.exit(2)
        pass

    try:
        path = os.listdir(os.path.join(root, 'components'))
        return [f[:-3] for f in path if f.endswith('.py') and f != '__init__.py']
    except FileNotFoundError:
        return []


def parse(parser, argv=None, settings_module=None, no_args_func=None):
    """
    parser cliez app

    :param parser: an instance of argparse.ArgumentParser
    :type parser:  `argparse.ArgumentParser`
    :param argv: argument list,default is `sys.argv`
    :type argv: `list` or `tuple`
    :param settings_module: settings class name, default is `cliez.conf.Settings`
    :type settings_module: `str`
    :param function no_args_func: execute when no argument apply.

    :return: `Component`

    """

    argv = argv or sys.argv
    commands = command_list()
    settings = None if not settings_module else Settings.bind(settings_module)

    assert type(argv) in [list, tuple], TypeError("argv only can be list or tuple")

    # match sub-parser
    if len(argv) >= 2 and argv[1] in commands:
        sub_parsers = parser.add_subparsers()
        class_name = argv[1].capitalize() + 'Component'
        from cliez.conf import COMPONENT_ROOT
        sys.path.insert(0, os.path.dirname(COMPONENT_ROOT))
        mod = importlib.import_module('{}.components.{}'.format(os.path.basename(COMPONENT_ROOT), argv[1]))
        klass = getattr(mod, class_name)
        klass.append_arguments(sub_parsers)
        options = parser.parse_args(argv[1:])

        logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.ERROR)

        if hasattr(options, 'debug') and options.debug:
            logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.DEBUG)
            pass

        if hasattr(options, 'verbose'):
            if options.verbose == 1:
                logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.CRITICAL)
            elif options.verbose == 2:
                logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.WARNING)
            elif options.verbose == 3:
                logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)
            pass

        obj = klass(parser, options=options, settings=settings)
        obj.run(options)
        # easier to create unittest case
        return obj

    if not parser.description and len(commands):
        sub_parsers = parser.add_subparsers()
        [sub_parsers.add_parser(v) for v in commands]
        pass
    pass

    options = parser.parse_args(argv[1:])
    if no_args_func:
        return no_args_func(options)
    else:
        parser._print_message("nothing to do...\n")
    pass

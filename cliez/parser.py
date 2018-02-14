"""
=============
Parser
=============

Parser is used to handle components.

"""

import importlib
import logging
import os
import sys
from logging import config as logging_config

from cliez.conf import Settings
from .utils import hump_to_underscore


def command_list():
    """
    Get sub-command list

    .. note::

        Don't use logger handle this function errors.

        Because the error should be a code error,not runtime error.


    :return: `list` matched sub-parser
    """
    from cliez.conf import COMPONENT_ROOT

    root = COMPONENT_ROOT

    if root is None:
        sys.stderr.write("cliez.conf.COMPONENT_ROOT not set.\n")
        sys.exit(2)
        pass

    if not os.path.exists(root):
        sys.stderr.write(
            "please set a valid path for `cliez.conf.COMPONENT_ROOT`\n")
        sys.exit(2)
        pass

    try:
        path = os.listdir(os.path.join(root, 'components'))
        return [f[:-3] for f in path if
                f.endswith('.py') and f != '__init__.py']
    except FileNotFoundError:
        return []


def append_arguments(klass, sub_parsers, default_epilog, general_arguments):
    """
    Add class options to argparser options.

    :param cliez.component.Component klass: subclass of Component
    :param Namespace sub_parsers:
    :param str default_epilog: default_epilog
    :param list general_arguments: global options, defined by user
    :return: Namespace subparser
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

    return sub_parser


def parse(parser, argv=None, settings_key='settings', no_args_func=None):
    """
    parser cliez app

    :param argparse.ArgumentParser parser: an instance
        of argparse.ArgumentParser
    :param argv: argument list,default is `sys.argv`
    :type argv: list or tuple

    :param str settings: settings option name,
        default is settings.

    :param object no_args_func: a callable object.if no sub-parser matched,
        parser will call it.

    :return:  an instance of `cliez.component.Component` or its subclass
    """

    argv = argv or sys.argv
    commands = command_list()

    if type(argv) not in [list, tuple]:
        raise TypeError("argv only can be list or tuple")

    # match sub-parser
    if len(argv) >= 2 and argv[1] in commands:
        sub_parsers = parser.add_subparsers()
        class_name = argv[1].capitalize() + 'Component'

        from cliez.conf import (COMPONENT_ROOT,
                                LOGGING_CONFIG,
                                EPILOG,
                                GENERAL_ARGUMENTS)

        sys.path.insert(0, os.path.dirname(COMPONENT_ROOT))
        mod = importlib.import_module(
            '{}.components.{}'.format(os.path.basename(COMPONENT_ROOT),
                                      argv[1]))

        # dynamic load component
        klass = getattr(mod, class_name)
        sub_parser = append_arguments(klass, sub_parsers, EPILOG,
                                      GENERAL_ARGUMENTS)
        options = parser.parse_args(argv[1:])

        settings = Settings.bind(
            getattr(options, settings_key)
        ) if settings_key and hasattr(options, settings_key) else None

        obj = klass(parser, sub_parser, options, settings)

        # init logger
        logger_level = logging.CRITICAL
        if hasattr(options, 'verbose'):
            if options.verbose == 1:
                logger_level = logging.ERROR
            elif options.verbose == 2:
                logger_level = logging.WARNING
            elif options.verbose == 3:
                logger_level = logging.INFO
                obj.logger.setLevel(logging.INFO)
            pass

        if hasattr(options, 'debug') and options.debug:
            logger_level = logging.DEBUG
            # http lib use a strange way to logging
            try:
                import http.client as http_client
                http_client.HTTPConnection.debuglevel = 1
            except Exception:
                # do nothing
                pass
            pass

        loggers = LOGGING_CONFIG['loggers']
        for k, v in loggers.items():
            v.setdefault('level', logger_level)
            if logger_level in [logging.INFO, logging.DEBUG]:
                v['handlers'] = ['stdout']
            pass

        logging_config.dictConfig(LOGGING_CONFIG)
        # this may not necessary
        # obj.logger.setLevel(logger_level)

        obj.run(options)

        # return object to make unit test easy
        return obj

    # print all sub commands when user set.
    if not parser.description and len(commands):
        sub_parsers = parser.add_subparsers()
        [sub_parsers.add_parser(v) for v in commands]
        pass
    pass

    options = parser.parse_args(argv[1:])
    if no_args_func and callable(no_args_func):
        return no_args_func(options)
    else:
        parser._print_message("nothing to do...\n")
    pass

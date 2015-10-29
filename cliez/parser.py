# -*- coding: utf-8 -*-

import sys
import os
import importlib
from cliez.conf import Settings


def command_list():
    """
    根据 `cliez.COMPONENT_ROOT` 查找所支持的完整 sub-parser 列表

    :return: `list` 当前支持的组件列表
    """
    from cliez import COMPONENT_ROOT

    root = COMPONENT_ROOT

    if root is None:
        sys.stderr.write("cliez.COMPONENT_ROOT not set.\n")
        sys.exit(2)
        pass

    if not os.path.exists(root):
        sys.stderr.write("please set a valid path for `cliez.COMPONENT_ROOT`\n")
        sys.exit(2)
        pass

    path = os.listdir(os.path.join(root, 'component'))
    return [f[:-3] for f in path if f.endswith('.py') and f != '__init__.py']


def parse(parser, argv=None, settings_module=None):
    """
    parser cliez app

    :param parser: 用户预定义的 parser
    :type parser:  `argparse.ArgumentParser`
    :param argv: 如果用户不指定,默认为 `sys.argv`
    :type argv: `list` or `tuple`
    :param settings_module: 模块名称, 指定后会将该模块中的变量绑定至全局 `cliez.conf.Settings`
    :type settings_module: `str`
    :return: `Component` 实际调用的组件,
                *返回组件在运行中并没有太大意义,但是在做测试用例时,返回组件可以大大简化撰写测试用例的难度*


    """

    argv = argv or sys.argv
    commands = command_list()
    settings = None if not settings_module else Settings.bind(settings_module)

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
        from cliez import COMPONENT_ROOT
        sys.path.insert(0, COMPONENT_ROOT)
        mod = importlib.import_module('{}.component.{}'.format(os.path.basename(COMPONENT_ROOT), argv[1]))
        klass = getattr(mod, class_name)
        klass.append_arguments(sub_parsers)
        pass
    options = parser.parse_args(argv[1:])
    obj = klass(parser, options=options, settings=settings)
    obj.run(options)

    # easier to create unittest case
    return obj

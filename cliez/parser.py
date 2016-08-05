# -*- coding: utf-8 -*-

import sys
import os
import importlib

from . import  settings


def command_list():
    """
    根据 `cliez.COMPONENT_ROOT` 查找所支持的完整 sub-parser 列表

    :return: `list` 当前支持的组件列表
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
        path = os.listdir(os.path.join(root, 'component'))
        return [f[:-3] for f in path if f.endswith('.py') and f != '__init__.py']
    except FileNotFoundError:
        return []


def parse(parser, argv=None, settings_module=None, active_one=None):
    """
    parser cliez app

    :param parser: 用户预定义的 parser
    :type parser:  `argparse.ArgumentParser`
    :param argv: 如果用户不指定,默认为 `sys.argv`
    :type argv: `list` or `tuple`
    :param settings_module: 模块名称, 指定后会将该模块中的变量绑定至全局 `cliez.conf.Settings`
    :type settings_module: `str`
    :param object active_one: 如果指定该参数,当用户不设置任何参数时,执行,多用于兼容flask模式

    .. note::
        当指定active_one时候,只有全局参数会生效,同时如果文档为手工撰写,请同时更新文档说明

    :return: `Component` 实际调用的组件,
                *返回组件在运行中并没有太大意义,但是在做测试用例时,返回组件可以大大简化撰写测试用例的难度*


    """

    from . import conf

    argv = argv or sys.argv
    commands = command_list()
    settings = conf

    #: 细节分支:
    #:
    #: * 当没有参数时,抛出异常,通常是因为测试用例忘记添加参数
    #: * 当有两个参数时,如果第二个参数不是 option 类型,则尝试使用subparser模式加载,不匹配则加载文档,退出
    #: * 当为其他场景时,直接尝试做parser.
    #: * 如果指定了active_one,则调用active_one

    assert type(argv) in [list, tuple], TypeError("argv only can be list or tuple")

    if len(argv) >= 2 and argv[1] in commands:
        sub_parsers = parser.add_subparsers()
        class_name = argv[1].capitalize() + 'Component'
        from cliez.conf import COMPONENT_ROOT
        sys.path.insert(0, os.path.dirname(COMPONENT_ROOT))
        mod = importlib.import_module('{}.component.{}'.format(os.path.basename(COMPONENT_ROOT), argv[1]))
        klass = getattr(mod, class_name)
        klass.append_arguments(sub_parsers)
        options = parser.parse_args(argv[1:])
        obj = klass(parser, options=options, settings=settings)
        obj.run(options)
        # easier to create unittest case
        return obj

    #: 暂时关闭对usage的显示优化,因为场景略复杂
    #  parser.usage = '{} [options] <command>'.format(os.path.basename(argv[0]))
    #: 如果未指定文档,且存在子parser,则尝试加载文档
    if not parser.description and len(commands):
        sub_parsers = parser.add_subparsers()
        [sub_parsers.add_parser(v) for v in commands]
        pass
    pass

    options = parser.parse_args(argv[1:])
    if active_one:
        return active_one(options)
    else:
        parser._print_message("nothing to do...\n")
    pass

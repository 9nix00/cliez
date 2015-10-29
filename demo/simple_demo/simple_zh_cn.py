# -*- coding: utf-8 -*-

from cliez.loader import ArgLoader


def pp(loader):
    """
    创建一个子parser

    :param loader: 经过编译后的 argloader
    :type loader: `cliez.loader.ArgLoader`
    :return:
    """
    usage = (
        ("--opt3", "comment for opt", '-c'),
        ("--opt4:", "comment for opt", '-d')
    )

    b = ArgLoader(options=usage, sys_argv=a.argv)
    print(b.options['--opt3'])
    pass


def hello(loader):
    """

    :param loader: 经过编译后的 argloader
    :type loader: `cliez.loader.ArgLoader`

    :param loader:
    :return:
    """

    if loader.options['--debug']:
        print("open debug mode:")

        # 可以通过 `repr` 获取到argparser内部的所有状态
        print("load data: ", repr(a))
        pass

    print("called hello")
    pass


def main(a):
    """
    程序入口
    :param a: 经过编译后的 argloader
    :type `cliez.loader.ArgLoader`
    :return: `int` or None
    """

    if a.options['--help']:
        # 使用print即可输出帮助文档"
        print(a)
        return

    if a.actions['hello']:
        # 每个 action 只有两个值 true or false
        # 当设定 hello 参数时,调用
        hello(a)
        return

    if a.actions['parent']:
        # 一个创建子parser的演示
        pp(a)
        return

    pass


# 请把options放置在 if __name__ == "__main__" 之外
# options还会用于测试用例中

options = (
    "Usage: command [options] arguments",
    "",
    "document line1",
    "document line2",
    "document line3",
    "",  # 输出一个空行
    "Options:",
    ("--opt1", "comment for opt", '-a'),
    ("--opt2:", "comment for opt", '-b'),
    "Actions",
    ("@hello", "call hello"),
    ("@parent", "support sub argument"),
    "",
    ("--help", "print help document", '-h'),
    ("--debug", "debug mode"),
)

if __name__ == "__main__":
    a = ArgLoader(options=options)
    main(a)
    pass

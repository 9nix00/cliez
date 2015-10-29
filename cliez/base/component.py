# -*- coding: utf-8 -*-

import pkg_resources
import os
import sys

import termcolor
import time


class Component(object):
    def __init__(self, parser=None, options=None, settings=None, *args, **kwargs):
        """
        组件基础类

        用于在argparser加载subparser后的逻辑执行
        上层继承该类后,业务逻辑覆写在 `run()`

        :param parser:
        :type parser:  `argparse.ArgumentParser`
        :param settings: 由 `cliez.parser.parse` 传入 package.settings
        :type settings: module
        :param args: `tuple`
        :param kwargs: `dict`
        """

        self.parser = parser
        self.settings = settings
        pass

    def print_message(self, message, file=None):
        """
        输出消息

        :param message: 显示的信息
        :type message: `str`
        :param file: 如果不指定则默认为 `sys.stdout`
        :type file: fd
        :return: None
        """
        return self.parser._print_message(message + "\n", file)

    def print_loading(self, wait, message):
        """
        在 `wait` 之内显示加载中的提示

        .. note::
            loading只写入到 `sys.stdout` 中


        :param wait: 等待时间
        :type wait: `int`
        :param message: 显示消息
        :type message: `str`
        :return: None
        """
        tags = ['\\', '|', '/', '-']

        for i in range(wait):
            time.sleep(0.25)
            sys.stdout.write("{}... {}\r".format(message, tags[i % 4]))
            sys.stdout.flush()
            pass

        sys.stdout.write("{}... Done...\n".format(message))
        sys.stdout.flush()
        pass

    def warn(self, message, file=None, prefix="[warn]:", suffix="..."):
        """
        输出警告信息
        当输出为 `sys.stdout` 时,以彩色方式输出


        :param message: 警告信息
        :type message: `str`
        :param file: 输出的文件符,默认为 `sys.stdout`
        :type file: fd
        :param prefix: 显示前缀,默认为 [warn]
        :type prefix: `str`
        :param suffix: 显示后缀,默认为 ...
        :type suffix: `str`
        :return: None
        """

        msg = prefix + message + suffix

        file = file or sys.stdout

        if file is sys.stdout:
            termcolor.cprint(msg, color="yellow")
        else:
            file.write(msg)

        pass

    def error(self, message):
        """
        输出错误消息并退出,退出状态位为2


        :param message:消息体
        :type message: `str`

        :return:None
        """
        return self.parser.error(message)

    @staticmethod
    def load_resource(path, root=''):
        """
        装载资源文件,通常用于提升加载包和待安装包的兼容性.

        举例说明:

        比如如果我们在当前文件,需要加载 `cliez.conf` 包中的 __init__.py 文件.最常用的做法是:

        .. code-block:: python

            open('../conf/__init__.py').read()



        这种写法会带了一个明显的问题是,如果我们的运行目录发生了变化,..的解释不同的.

        load_resource用来解决这个问题,只要是在package中的内容,当前进程能够正常获取到package,即能被正常加载.

        以下代码都是等价的
        .. code-block:: python

            a = Component()
            a.load_resource('component.py', root='cliez/base')
            a.load_resource('base/component.py', root='cliez')
            a.load_resource('/base/component.py', root='cliez')
            a.load_resource('cliez/base/component.py')
            a.load_resource(__file__.rsplit('/', 2)[0] + '/cliez/base/component.py')



        :param path: 文件路径
        :type path: `str`
        :param root: 根目录,默认为空字符串
        :type root: `str`
        :return: `str` 读取的内容
        """

        try:
            buf = open(os.path.join(root, path)).read()
        except (IOError, FileNotFoundError):
            full_path = root + path
            pkg, path = full_path.split('/', 1)
            buf = pkg_resources.resource_string(pkg, path)
        return buf

    @staticmethod
    def load_description(name, root=''):
        """
        读取文档

        该方法底层调用 `self.load_resource`

        不同的是当文件不存在时,该方法不会抛出异常而是


        :param path: 文件路径
        :type path: `str`
        :param root: 根目录,默认为空字符串
        :type root: `str`
        :return: `str` 返回描述
        """
        desc = ''

        try:
            desc = Component.load_resource(name, root=root)
        except (IOError, ImportError):
            pass

        return desc

    pass

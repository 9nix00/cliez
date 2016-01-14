# -*- coding: utf-8 -*-

import pkg_resources
import os
import sys
import signal

import termcolor
import time
import threading
from time import sleep


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
        self.options = options
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


        .. note::

            如果是python3版本,则文档编码格式必须为utf-8


        :param path: 文件路径
        :type path: `str`
        :param root: 根目录,默认为空字符串
        :type root: `str`
        :return: `str` 读取的内容
        """

        if root:
            full_path = root + '/' + path.strip('/')
        else:
            full_path = path

        try:
            buf = open(full_path).read()
        except IOError:
            pkg, path = full_path.split('/', 1)
            buf = pkg_resources.resource_string(pkg, path)

            # compatible python3 and only support utf-8
            if type(buf) != str:
                buf = buf.decode('utf-8')
                pass

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


class SlotComponent(Component):
    slot_class = None
    entry_name = None
    entry_help = 'run component as service'

    def get_slot_class(self):
        """
        返回slot类
        :return:
        """
        return self.slot_class(self)

    def set_signal(self):
        """
        设置信号处理

        默认直接中断,考虑到一些场景用户需要等待线程结束.
        可在此自定义操作

        :return:
        """

        def signal_handle(signum, frame):
            self.error("User interrupt.kill threads.")
            sys.exit(-1)
            pass

        signal.signal(signal.SIGINT, signal_handle)
        pass

    def run(self, options):
        """
        对于大多数场景,用户并不需要覆写此函数

        :param options:
        :return:
        """

        if not self.slot_class:
            raise NotImplementedError('please set your `cls.slot_class` attribute.')

        self.set_signal()

        slot = self.get_slot_class()

        # start thread
        i = 0
        while i < options.threads:
            t = threading.Thread(target=self.worker, args=[slot])
            # only set daemon when once is False
            if options.once is True or options.no_daemon is True:
                t.daemon = False
            else:
                t.daemon = True

            t.start()
            i += 1

        # waiting thread
        if options.once is False:
            while True:
                if threading.active_count() > 1:
                    sleep(1)
                else:
                    if threading.current_thread().name == "MainThread":
                        sys.exit(0)

        pass

    def worker(self, iterator):
        t = self.options.sleep

        while True:
            with iterator as result:
                if result is not False:
                    iterator.slot(result)
                    t = self.options.sleep
                else:
                    # if set options.once,exit.
                    if self.options.once is True:
                        sys.exit(0)

                    t += self.options.sleep
                    if t > self.options.sleep_max_time:
                        t = self.options.sleep
                    sleep(t)
                    # else:
                    #     print("User interrupt on thread:", threading.current_thread())
                    #     sys.exit(0)

    @classmethod
    def append_slot_arguments(cls, sub_parser):
        return None

    @classmethod
    def append_arguments(cls, sub_parsers):
        if not cls.entry_name:
            raise NotImplementedError('please set your `CLASS.entry_name` attribute')

        sub_parser = sub_parsers.add_parser(cls.entry_name, help=cls.entry_help)
        sub_parser.add_argument('--once', action='store_true', help='execute once and exit.')
        sub_parser.add_argument('--no-daemon', action='store_true', help='set service works in no daemon mode.')
        sub_parser.add_argument('--sleep', nargs='?', type=int, default=2, help='set sleep time,default is 2s.')
        sub_parser.add_argument('--sleep-max-time', nargs='?', type=int, default=60, help='set max sleep time, default is 60s.')
        sub_parser.add_argument('--thread-sleep', nargs='?', default='0', help='set thread sleep time.')
        sub_parser.add_argument('--threads', nargs='?', type=int, default=10, help='set slot threads num,default is 10.')

        cls.append_slot_arguments(sub_parser)
        pass

    pass

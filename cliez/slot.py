# -*- coding: utf-8 -*-

import os
import signal
import threading
from time import sleep

from .component import Component


class SlotComponent(Component):
    class Handle(object):
        """

        * `initialize`

        initial resource, e.g: database handle

        * `__enter__`

        get next data to do,you can fetch one or more data.

        * `slot`

        user custom code

        * `__exit__`

        when slot finished, call this method

        """

        def __init__(self, component):
            """
            Don't override this method unless you know what you're doing.
            :param component:
            :return:
            """
            self.component = component
            self.options = component.options
            self.initialize()

        def initialize(self):
            """
            Hook for subclass initialization.

            This block is execute before thread initial
            """
            pass

        def __enter__(self):
            """
            ...note::
                You **MUST** return False when no data to do.

            The return value will be used in `Slot.slot`
            """
            self.component.error_message("please overwrite `__enter__` method,and make sure return False when no data to execute.")
            return False

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            When slot done, will call this method.
            """

            if self.options.thread_sleep_time:

                if self.options.thread_sleep_range:
                    sleep_time = random.randint(self.options.thread_sleep_time, self.options.thread_sleep_time + self.options.thread_sleep_range)
                    pass
                else:
                    sleep_time = self.options.thread_sleep_time
                    pass

                sleep(sleep_time)

            pass

        def slot(self, msg):
            """
            Add your custom code at here.
            """

            pass

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

    def check_exclusive_mode(self):
        """
        检查是否是独占模式

        参数顺序必须一致,也就是说如果参数顺序不一致,则判定为是两个不同的进程
        这么设计是考虑到:

        - 一般而言,排他模式的服务启动都是crontab等脚本来完成的,不存在顺序变更的可能
        - 这在调试的时候可以帮助我们不需要结束原有进程就可以继续调试

        :return:
        """

        if self.options.exclusive_mode:
            import psutil
            current_pid = os.getpid()
            current = psutil.Process(current_pid).cmdline()

            for pid in psutil.pids():
                p = psutil.Process(pid)
                try:
                    if current_pid != pid and current == p.cmdline():
                        self.error_message("process exist. pid:{}".format(p.pid))
                        sys.exit(-1)
                        pass

                except psutil.ZombieProcess:
                    # 僵尸进程,无视
                    pass
                except psutil.AccessDenied:
                    # 不具备用户权限
                    pass
                pass
            pass

        pass

    def run(self, options):
        """
        In general, you don't need to overwrite this method.

        :param options:
        :return:
        """

        self.set_signal()
        self.check_exclusive_mode()

        slot = self.Handle(self)

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

    # user custom method
    # @classmethod
    # def add_slot_args(cls):
    #
    #     pass

    @classmethod
    def add_arguments(cls):
        return [
            (('--once',), dict(action='store_true', help='execute once and exit.')),
            (('--exclusive-mode',), dict(action='store_true', help='open this will limit one progress to work.')),
            (('--no-daemon',), dict(action='store_true', help='set service works in no daemon mode.')),
            (('--sleep',), dict(nargs='?', type=int, default=2, help='set sleep time,default is 2s.')),
            (('--sleep-max-time',), dict(nargs='?', type=int, default=60, help='set max sleep time, default is 60s.')),
            (('--thread-sleep-time',), dict(nargs='?', type=int, default=0, help='set thread sleep min time.')),
            (('--thread-sleep-range',), dict(nargs='?',
                                             type=int,
                                             default=0,
                                             help='when set thread-sleep-time, pickup a random value from ${thread-sleep-time} to ${thread-sleep-time}+range')),
            (('--threads',), dict(nargs='?', type=int, default=10, help='set slot threads num,default is 10.')),
        ]

    pass

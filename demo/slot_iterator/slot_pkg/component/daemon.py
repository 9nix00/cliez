# -*- coding: utf-8 -*-

from cliez.base.component import SlotComponent
from cliez.base.slot import Slot

import threading
from time import sleep


class threadsafe_iter:
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """

    def __init__(self, it, lock):
        self.it = it
        self.lock = lock

    def __iter__(self):
        return self

    def next(self):
        # with self.lock:
        #     return next(self.it)
        return next(self.it)

    pass


def threadsafe_generator(f):
    """A decorator that takes a generator function and makes it thread-safe.
    """

    def g(*a, **kw):
        return threadsafe_iter(f(*a, **kw))

    return g


class TodoSlot(Slot):
    def initialize(self):
        # self.lock = threading.Lock()

        # print('lock is ', self.lock)
        self.lock = None
        self.todo_list = threadsafe_iter(iter(self.generate_todo_list()), self.lock)

        self.todo_list1 = iter(self.generate_todo_list())

        self.i = 0
        self.ending = False

        pass

    def generate_todo_list(self):
        if self.component.options.small:
            return list(range(0, 10))
        else:
            return list(range(0, 40))
        pass

    def slot(self, msg):

        self.i += 1

        if threading.current_thread().name in ['Thread-8', 'Thread-1']:
            self.component.print_message("{}:Get todo id:{},self.i is {}".format(threading.current_thread().name, msg, self.i))
            pass

        # sleep(1)
        pass

    def __enter__(self):
        try:
            return next(self.todo_list1)
            # return self.todo_list.next()
        except StopIteration:
            # if not self.todo_list1:
            if self.ending is False:
                self.ending = True
                self.component.print_message("{}:execute {} times... this message should show only once.".format(threading.current_thread().name, self.i))

            if not self.options.once and not self.todo_list1:
                self.todo_list1 = iter(self.generate_todo_list())
                self.i = 0
            # self.todo_list = threadsafe_iter(iter(self.generate_todo_list()), self.lock)
            # self.component.print_message("{}:No todo data found, waiting {}s...".format(threading.current_thread().name, self.options.sleep))
            return False

    pass


class DaemonComponent(SlotComponent):
    """
    slot component
    """
    slot_class = TodoSlot
    entry_name = 'daemon'

    @staticmethod
    def append_slot_arguments(sub_parser):
        sub_parser.description = DaemonComponent.load_description('slot_pkg/manual/daemon.txt')
        sub_parser.add_argument('--small', action='store_true', help='set list from 0 to 10')
        pass

    pass

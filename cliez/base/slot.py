# -*- coding: utf-8 -*-

import random
from time import sleep


class Slot(object):
    """
    To use slot, you should create a python module file. we named *slot*.

    A legal slot must be named 'Slot' in your module file and it must be at least contain four method:

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
        Don't override this method unless what you're doing.
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

        Example::

            class UserSlot(Slot):
                def initialize(self):
                    ...
                    pass

                def slot(self, result):
                    ...
                    pass

        """
        pass

    def __enter__(self):
        """
        ...note::
            You **MUST** return False when no data to do.

        The return value will be used in `Slot.slot`
        """
        self.component.warn("no data found. will sleep {}s.".format(self.component.options.sleep))
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

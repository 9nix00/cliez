# -*- coding: utf-8 -*-

from cliez.base.component import SlotComponent
from cliez.base.slot import Slot

import threading
from time import sleep


class TodoSlot(Slot):
    def initialize(self):
        if self.component.options.small:
            self.todo_list = list(range(0, 10))
        else:
            self.todo_list = list(range(0, 20))
        pass

    def slot(self, msg):
        self.component.print_message("{}:Get todo id:{}".format(threading.current_thread().name, msg))
        sleep(1)
        pass

    def __enter__(self):
        if not self.todo_list:
            self.component.print_message("{}:No todo data found, waiting {}s...".format(threading.current_thread().name, self.options.sleep))
            return False
        else:
            return self.todo_list.pop()
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

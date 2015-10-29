# -*- coding: utf-8 -*-

import pkg_resources
import os
import sys

import termcolor
import time


class Component(object):
    """
    Base Component
    """

    def __init__(self, parser=None, options=None, settings=None, *args, **kwargs):
        """
        component base class

        :param parser:
        :param settings:
        :param args:
        :param kwargs:
        :return:
        """

        self.parser = parser
        self.settings = settings
        pass

    def print_message(self, message, file=None):
        """
        simple output
        :param message:
        :param file:
        :return:
        """
        return self.parser._print_message(message + "\n", file)

    def print_loading(self, wait, message):
        """
        print loading message,this only display in stdout
        :param wait:
        :param message:
        :return:
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

        msg = prefix + message + suffix

        if file is sys.stdout:
            termcolor.cprint(msg, color="yellow")
        else:
            print(msg)

        pass

    def error(self, message):
        """

        :param message:
        :return:
        """
        return self.parser.error(message)

    @staticmethod
    def load_resource(path, root=''):
        """
        load resources file.
        this is useful when we need to load files from package.
        the below code can get same result


        :param path:
        :param root:
        :return:
        """

        try:
            buf = open(os.path.join(root, path)).read()
        except (IOError, FileNotFoundError):
            full_path = root + path
            pkg, path = full_path.split('/', 1)
            buf = pkg_resources.resource_string(pkg, path)
        return buf

    @staticmethod
    def load_description(name):
        """
        load custom document
        :param name:
        :return:
        """
        desc = None

        try:
            desc = Component.load_resource(name)
        except (IOError, ImportError):
            pass

        return desc

    pass

# -*- coding: utf-8 -*-

import pkg_resources
import os
import sys


class Component(object):
    def __init__(self, parser=None, settings=None, *args, **kwargs):
        self.parser = parser
        self.settings = settings
        pass

    def print_message(self, message, file=None):
        """
        a wrapper for `argparse.ArgumentParser._print_message()`
        :param message:
        :param file:
        :return:
        """
        return self.parser._print_message(message, file)

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

    def error(self, message):
        """
        a wrapper for `argparse.ArgumentParser._print_message()`
        :param message:
        :return:
        """
        return self.parser.error(message)

    @staticmethod
    def load_resource(path, root=None):
        """
        load resouces file
        :param path:
        :param root:
        :return:
        """
        from cliez import conf

        root = root or conf.PACKAGE_ROOT
        # root = root or __file__.rsplit('/', 2)[0]
        try:
            buf = open(os.path.join(root, path)).read()
        except IOError:
            buf = pkg_resources.resource_string(os.path.dirname(root), path)
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

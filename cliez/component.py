# -*- coding: utf-8 -*-

import os
import sys
import logging
import termcolor
import time
from cliez import conf


class Component(object):
    exclude_global_option = False
    logger_name = None
    logger = None

    def __init__(self, parser=None, options=None, settings=None, *args, **kwargs):
        """

        Don't overwrite this method.

        in most case,you should custom  `run()` method

        :param parser:
        :type parser:  `argparse.ArgumentParser`
        :param settings: a settings created by `cliez.parser.parse`
        :type settings: module
        :param args: `tuple`
        :param kwargs: `dict`
        """

        self.parser = parser
        self.options = options
        self.settings = settings

        if not self.logger_name:
            self.logger_name = self.__class__.__name__.lower().replace('component', '')

        self.logger = logging.getLogger(self.logger_name)
        pass

    def print_message(self, message, file=None):
        """
        print message when user logging level is not INFO

        :param message: message to print
        :type message: `str`
        :param file: file to write,default is  `sys.stdout`
        :type file: fd
        :return: None
        """
        if message.strip():
            self.logger.info(message)

        if self.logger.level != logging.INFO:
            return self.parser._print_message(message + "\n", file)
        pass

    def print_loading(self, wait, message):
        """
        print loading message on screen

        .. note::
            loading message only write to `sys.stdout`


        :param wait: wait seconds
        :type wait: `int`
        :param message: message to print
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

    def warn_message(self, message, file=None, prefix="[warn]:", suffix="..."):
        """
        print warn type message
        if file handle is `sys.stdout`, print color message


        :param message: message to print
        :type message: `str`
        :param file: file handle,default is `sys.stdout`
        :type file: fd
        :param prefix: message prefix,default is `[warn]`
        :type prefix: `str`
        :param suffix: message suffix ,default is `...`
        :type suffix: `str`
        :return: None
        """

        msg = prefix + message + suffix

        file = file or sys.stdout

        self.logger.warn(message)

        if file is sys.stdout:
            if self.logger.level != logging.WARNING:
                termcolor.cprint(msg, color="yellow")
        else:
            file.write(msg)

        pass

    def warn(self, *args, **kwargs):
        """
        alias for `warn_message`
        :param args:
        :param kwargs:
        :return:
        """

        return self.warn_message(*args, **kwargs)

    def error_message(self, message, file=None, prefix="[error]:", suffix="..."):
        """
        print error type message
        if file handle is `sys.stderr`, print color message

        :param message: message to print
        :type message: `str`
        :param file: file handle, default is  `sys.stdout`
        :type file: fd
        :param prefix: message prefix,default is `[error]`
        :type prefix: `str`
        :param suffix: message suffix ,default is `...`
        :type suffix: `str`
        :return: None
        """

        msg = prefix + message + suffix

        file = file or sys.stderr

        self.logger.critical(message)

        if file is sys.stderr:
            if self.logger.level != logging.CRITICAL:
                termcolor.cprint(msg, color="red")
        else:
            file.write(msg)

        pass

    def error(self, message=''):
        """
        print error message and exit.

        this method call `argparser.error`

        the default exit status is 2

        :param message: message to print
        :type message: `str`

        :return:None
        """

        if self.logger.handlers:
            self.logger.error(message)

        return self.parser.error(message)

    def system(self, cmd, fake_code=0):
        if self.options.dry_run:
            def fake_system(cmd):
                self.print_message(cmd)
                return fake_code

            return fake_system(cmd)

        self.logger.debug(cmd)
        return os.system(cmd)

    @staticmethod
    def load_resource(path, root=''):
        """

        load resource file in package.

        this method is used to load file easier in different environment.


        .. note::

            experiment feature.
            this feature only work in python3


        e.g:

        if we need load resource file `resource.io` from package `cliez.conf` .the easiest way may like this:

        .. code-block:: python

            open('../conf/resource.io').read()


        An obvious question is if we change working directory. `..` is relative path. it will cause error.

        `load_resource` is designed for solve this problem.


        The following code are equivalent:

        .. code-block:: python

            a = Component()
            a.load_resource('resource.io', root='cliez/base')
            a.load_resource('base/resource.io', root='cliez')
            a.load_resource('/base/resource.io', root='cliez')
            a.load_resource('cliez/base/resource.io')
            a.load_resource(__file__.rsplit('/', 2)[0] + '/cliez/base/resource.io')


        .. note::

            if you use python3, the document charset *must* be utf-8


        :param path: file path
        :type path: `str`
        :param root: root path
        :type root: `str`
        :return: `str`
        """

        if root:
            full_path = root + '/' + path.strip('/')
        else:
            full_path = path

        buf = ''

        try:
            buf = open(full_path).read()
        except IOError:
            pkg, path = full_path.split('/', 1)
            try:
                import pkg_resources
                buf = pkg_resources.resource_string(pkg, path)
                # compatible python3 and only support utf-8
                if type(buf) != str:
                    buf = buf.decode('utf-8')
                    pass
            except AttributeError:
                buf = 'document not work in python2'
                pass

        return buf

    @staticmethod
    def load_description(name, root=''):
        """
        load resource file as description but ignore `IOError` and `ImportError`

        :param path: name resource path
        :type path: `str`
        :param root: same as `load_resource()` root
        :type root: `str`
        :return: `str`
        """
        desc = ''

        try:
            desc = Component.load_resource(name, root=root)
        except (IOError, ImportError):
            pass

        return desc

    @staticmethod
    def hump_to_underscore(name):
        new_name = ''

        pos = 0
        for c in name:
            if pos == 0:
                new_name = c.lower()
            elif 65 <= ord(c) <= 90:
                new_name += '_' + c.lower()
                pass
            else:
                new_name += c
            pos += 1
            pass
        return new_name

    @classmethod
    def append_arguments(cls, sub_parsers):
        entry_name = cls.hump_to_underscore(cls.__name__).replace('_component', '')
        epilog = conf.EPILOG if conf.EPILOG else 'This tool generate by `cliez` https://www.github.com/wangwenpei/cliez'

        sub_parser = sub_parsers.add_parser(entry_name, help=cls.__doc__, epilog=epilog)
        sub_parser.description = cls.add_arguments.__doc__

        if hasattr(cls, 'add_slot_args'):
            slot_args = cls.add_slot_args() or []
            for v in slot_args:
                sub_parser.add_argument(*v[0], **v[1])
            sub_parser.description = cls.add_slot_args.__doc__
            pass

        user_arguments = cls.add_arguments() or []

        for v in user_arguments:
            sub_parser.add_argument(*v[0], **v[1])

        if not cls.exclude_global_option:
            for v in conf.GENERAL_ARGUMENTS:
                sub_parser.add_argument(*v[0], **v[1])

        pass

    @classmethod
    def add_arguments(cls):
        pass

    pass

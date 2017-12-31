"""
=============
Component
=============

A component is used to constuct user command.

"""

import logging
import os
import sys
import time

import termcolor

from cliez import conf


class Component(object):
    exclude_global_option = False
    logger_name = None
    logger = None

    def __init__(self, parser=None, options=None, settings=None,
                 *args, **kwargs):
        """
        Don't overwrite this method.
        In most case,you should custom  `run()` method
        """

        self.parser = parser
        self.options = options
        self.settings = settings

        if not self.logger_name:
            self.logger_name = 'component.{}'.format(
                self.__class__.__name__.lower().replace('component', ''))

        self.logger = logging.getLogger(self.logger_name)
        pass

    def print_message(self, message, fh=None):
        """
        print message on screen

        :param str message:
        :param file fh: file handle,default is None
        :return: None
        """
        return self.parser._print_message(message + "\n", fh)

    def print_loading(self, wait, message):
        """
        print loading message on screen

        .. note::

            loading message only write to `sys.stdout`


        :param int wait: seconds to wait
        :param str message: message to print
        :return: None
        """
        tags = ['\\', '|', '/', '-']

        for i in range(wait):
            time.sleep(0.25)
            sys.stdout.write("%(message)s... %(tag)s\r" % {
                'message': message,
                'tag': tags[i % 4]
            })

            sys.stdout.flush()
            pass

        sys.stdout.write("%s... Done...\n" % message)
        sys.stdout.flush()
        pass

    def warn_message(self, message, fh=None, prefix="[warn]:", suffix="..."):
        """
        print warn type message,
        if file handle is `sys.stdout`, print color message


        :param str message: message to print
        :param file fh: file handle,default is `sys.stdout`
        :param str prefix: message prefix,default is `[warn]`
        :param str suffix: message suffix ,default is `...`
        :return: None
        """

        msg = prefix + message + suffix
        fh = fh or sys.stdout

        if fh is sys.stdout:
            termcolor.cprint(msg, color="yellow")
        else:
            fh.write(msg)

        pass

    def warn(self, *args, **kwargs):
        """
        alias for `warn_message`
        """

        return self.warn_message(*args, **kwargs)

    def error_message(self, message, fh=None, prefix="[error]:",
                      suffix="..."):
        """
        print error type message
        if file handle is `sys.stderr`, print color message

        :param str message: message to print
        :param file fh: file handle, default is `sys.stdout`
        :param str prefix: message prefix,default is `[error]`
        :param str suffix: message suffix ,default is '...'
        :return: None
        """

        msg = prefix + message + suffix
        fh = fh or sys.stderr

        if fh is sys.stderr:
            if self.logger.level != logging.CRITICAL:
                termcolor.cprint(msg, color="red")
        else:
            fh.write(msg)

        pass

    def error(self, message=None, exit_code=2):
        """
        print error message and exit.
        this method call `argparser.exit` to exit.

        :param str message: message to print
        :param int exit_code: exit code,default is 2

        :return: None
        """

        return self.parser.exit(exit_code, message)

    def system(self, cmd, fake_code=False):
        """
        a built-in wrapper make dry-run easier.
        you should use this instead use `os.system`

        .. note::

            to use it,you need add '--dry-run' option in
            your argparser options


        :param str cmd: command to execute
        :param bool fake_code: only display command when is True,default is False
        :return:
        """
        try:
            if self.options.dry_run:
                def fake_system(cmd):
                    self.print_message(cmd)
                    return fake_code

                return fake_system(cmd)
        except AttributeError:
            self.logger.warnning("fake mode enabled,"
                                 "but you don't set '--dry-run' option "
                                 "in your argparser options")
            pass

        return os.system(cmd)

    @staticmethod
    def load_resource(path, root=''):
        """
        .. warning::

            Experiment feature.

            BE CAREFUL! WE MAY REMOVE THIS FEATURE!


        load resource file which in package.
        this method is used to load file easier in different environment.

        e.g:

        consume we have a file named `resource.io` in package `cliez.conf`,
        and we want to load it.
        the easiest way may like this:

        .. code-block:: python

            open('../conf/resource.io').read()


        An obvious problem is `..` is relative path.
        it will cause an error.

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

            The document charset *MUST BE* utf-8


        :param str path: file path
        :param str root: root path

        :return: str
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
                # load resource feature not work in python2
                pass

        return buf

    @staticmethod
    def load_description(name, root=''):
        """
        .. warning::

            Experiment feature.

            BE CAREFUL! WE MAY REMOVE THIS FEATURE!


        Load resource file as description,
        if resource file not exist,will return empty string.

        :param str path: name resource path
        :param str root: same as `load_resource` root
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
        """
        Convert Hump style to underscore

        :param name: Hump Character
        :return: str
        """
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
        """
        Add class options to argparser options.

        :param sub_parsers:
        :return: None
        """

        entry_name = cls.hump_to_underscore(cls.__name__).replace('_component',
                                                                  '')

        # set sub command document
        epilog = conf.EPILOG if conf.EPILOG else 'This tool generate by `cliez` https://www.github.com/wangwenpei/cliez'

        sub_parser = sub_parsers.add_parser(entry_name, help=cls.__doc__,
                                            epilog=epilog)
        sub_parser.description = cls.add_arguments.__doc__

        # add slot arguments
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
        """
        User can overwrite this method add custom options
        """
        pass

    pass

# -*- coding: utf-8 -*-

import os
import sys
import importlib

COMPONENT_ROOT = None
GENERAL_ARGUMENTS = []
EPILOG = None


def settings(path=None, with_path=None):
    """
    a wrapper for `Settings._wrapped`


    :return: `Settings`
    """

    if path:
        Settings.bind(path, with_path=with_path)

    return Settings._wrapped


class Settings(object):
    """
    cliez global config class

    """

    _path = None
    # _db_patch_path = None

    _wrapped = None

    @staticmethod
    def bind(mod_path, with_path=None):
        """
        bind user variable to `_wrapped`


        .. note::

            you don't need call this method by yourself.

            program will call it in  `cliez.parser.parse`
            只有在撰写自定义测试用例时,为了区分环境,我们才需要手动声明


        :param `str` mod_path: module path, *use 'mod.mod1' not 'mod/mod1' *

        :param str with_path: add path to `sys.path`, if path is file,use its parent.

        :return: `settings`
        """

        if with_path:
            if os.path.isdir(with_path):
                sys.path.insert(0, with_path)
            else:
                sys.path.insert(0, with_path.rsplit('/', 2)[0])
            pass

        try:
            mod = importlib.import_module(mod_path)
        except ImportError:
            raise

        settings = Settings()

        for v in dir(mod):
            if v[0] == '_' or type(getattr(mod, v)).__name__ == 'module':
                continue
            setattr(settings, v, getattr(mod, v))
            pass

        Settings._path = mod_path
        # Settings._db_patch_path = mod_path.rsplit('.', 1)[0] + '.db_patch'
        Settings._wrapped = settings

        return settings

    pass

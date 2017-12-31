"""
=====================
Default Config
=====================
"""

import importlib
import logging
import os
import sys

COMPONENT_ROOT = None
GENERAL_ARGUMENTS = []
EPILOG = None

LOGGING_CONFIG = {  #: default logging config
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(name)s %(asctime)s:: %(message)s'
        },
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
        'stderr': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'component': {
            'handlers': ['stderr'],
            'level': logging.CRITICAL,
            'propagate': True,
        },
    }
}


def settings(path=None, with_path=None):
    """
    Get or set `Settings._wrapped`

    :param str path: a python module file,
        if user set it,write config to `Settings._wrapped`
    :param str with_path: search path
    :return: A instance of `Settings`
    """

    if path:
        Settings.bind(path, with_path=with_path)

    return Settings._wrapped


class Settings(object):
    """
    cliez global config class
    """

    _path = None
    _wrapped = None

    @staticmethod
    def bind(mod_path, with_path=None):
        """
        bind user variable to `_wrapped`

        .. note::

            you don't need call this method by yourself.

            program will call it in  `cliez.parser.parse`


        .. expection::

            if path is not correct,will cause an `ImportError`


        :param str mod_path: module path, *use dot style,'mod.mod1'*
        :param str with_path: add path to `sys.path`,
            if path is file,use its parent.
        :return: A instance of `Settings`
        """

        if with_path:
            if os.path.isdir(with_path):
                sys.path.insert(0, with_path)
            else:
                sys.path.insert(0, with_path.rsplit('/', 2)[0])
            pass

        # raise `ImportError` mod_path if not exist
        mod = importlib.import_module(mod_path)

        settings = Settings()

        for v in dir(mod):
            if v[0] == '_' or type(getattr(mod, v)).__name__ == 'module':
                continue
            setattr(settings, v, getattr(mod, v))
            pass

        Settings._path = mod_path
        Settings._wrapped = settings

        return settings

    pass

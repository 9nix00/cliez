# -*- coding: utf-8 -*-

import importlib

PACKAGE_ROOT = None


class Settings(object):
    _path = None
    _wrapped = None

    @staticmethod
    def bind(mod_path):

        try:
            mod = importlib.import_module(mod_path)
        except ImportError:
            raise

        Settings._path = mod_path
        Settings._wrapped = mod

        settings = Settings()

        for v in dir(mod):
            if v[0] == '_' or type(getattr(mod, v)).__name__ == 'module':
                continue
            setattr(settings, v, getattr(mod, v))
            pass

        return settings

    pass

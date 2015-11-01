# -*- coding: utf-8 -*-

import os
import sys
import importlib

COMPONENT_ROOT = None


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
    全局配置模块

    用于生成全局配置,提升代码的可移植性

    """

    _path = None
    _db_patch_path = None

    _wrapped = None

    @staticmethod
    def bind(mod_path, with_path=None):
        """
        绑定用户的settings至全局

        .. note::

            用户配置中内部变量和引用不会加入到全局配置中


        .. note::

            该方法一般不需要由用户自己调用.系统会在 `cliez.parser.parse` 环节自动执行
            只有在撰写自定义测试用例时,为了区分环境,我们才需要手动声明


        :param `str` mod_path: 模块路径, *使用标准的模块语法 'mod.mod1' 而不是文件路径 'mod/mod1' *

            .. note::
                db_patch必须与setting放置在同一目录,设置settings时,会同时设置db_patch路径

        :param str with_path: 如果指定是文件,则设置上级目录的上级目录为path,如果是目录则直接指定

            .. todo::
                需要关注在多依赖环境下,是否重复插入

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
        Settings._db_patch_path = mod_path.rsplit('.', 1)[0] + '.db_patch'
        Settings._wrapped = settings

        return settings

    pass

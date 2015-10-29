# -*- coding: utf-8 -*-

import importlib


def settings():
    """
    a wrapper for `Settings._wrapped`


    :return: `Settings`
    """
    return Settings._wrapped


class Settings(object):
    """
    全局配置模块

    用于生成全局配置,提升代码的可移植性

    """

    _path = None
    _wrapped = None

    @staticmethod
    def bind(mod_path):
        """
        绑定用户的settings至全局

        .. note::

            用户配置中内部变量和引用不会加入到全局配置中


        .. note::

            该方法一般不需要由用户自己调用.系统会在 `cliez.parser.parse` 环节自动执行
            只有在撰写自定义测试用例时,为了区分环境,我们才需要手动声明


        :param mod_path: 模块路径, *使用标准的模块语法 'mod.mod1' 而不是文件路径 'mod/mod1' *
        :type mod_path: `str`
        :return: `settings`
        """


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
        Settings._wrapped = settings

        return settings

    pass

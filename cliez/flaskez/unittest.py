# -*- coding: utf-8 -*-

"""
基于此例测试用例的使用限制

* 目前只支持对peewee和mongoengine的数据库自动化测试.

    * 使用mongoengine无限制,策略为直接创建和删除数据库
    * 使用peewee限制为:

        * 目前只支持一个database.
        * 目前一个测试用例只支持一种db连接


"""

import unittest
from cliez.conf import settings, Settings
from builtins import dict


class TestCase(unittest.TestCase):
    _db = None
    _db_type = None
    _db_name = None

    settings = None
    app_binding = None
    blueprint_binding = None
    db_node = None



    @classmethod
    def _replaceDatabaseHandler(self,handlers):


        pass




    @classmethod
    def setUpClass(cls):
        """
        底层测试用例初始化
        目前支持对 `mongoengine` 和 `peewee.MySQLDatabase` 的数据库测试

        如果是mongodb,尝试重建数据库

        如果是peewee,尝试执行用户自定义的 `db_patch`


        :return:
        """

        super(TestCase, cls).setUpClass()

        app = settings(cls.settings).app
        app.config.from_object(settings().DevelopmentConfig)
        app.config['TESTING'] = True

        if cls.app_binding:
            try:
                print("todo feature")
            except ImportError:

                pass
            pass

        if cls.blueprint_binding:
            import importlib
            try:
                mod_name, entry_name = cls.blueprint_binding.rsplit('.', 1)
                mod = importlib.import_module(mod_name)
                app.register_blueprint(getattr(mod, entry_name))
                pass
            except ImportError:
                raise ImportError("can't find blueprint:{}".format(cls.blurprint_binding))
                pass
            pass

        db = app.config.get('DATABASE')
        cls.app = app.test_client()



        # if isinstance(db, dict):
        #
        #     for v in db.values():
        #
        #         pass
        #
        #     pass
        #
        # else:
        #



        if db:
            if db.__class__.__module__ == 'peewee' and db.__class__.__name__ == 'MySQLDatabase':
                cls._db_type = 'mysql'
                cls._db = db
                cls._db_name = db.database + '_test'
                db.database = cls._db_name

                app.config['DATABASE'] = cls._db

                try:
                    import importlib
                    mod = importlib.import_module(Settings._db_patch_path)

                    for m in mod.__all__:
                        patch = importlib.import_module(Settings._db_patch_path + '.' + m)
                        patch.commit()
                        pass

                except ImportError:
                    pass

                pass
            elif cls._db.__class__.__module__ == 'pymongo.mongo_client':
                import mongoengine
                mongo_settings = mongoengine.connection._connection_settings.get('default')
                if mongo_settings:
                    mongo_settings['name'] += '_test'
                    mongodb_handler = mongoengine.connect(**mongo_settings)
                    mongodb_use_db = mongo_settings['name']
                    mongodb_handler.drop_database(mongodb_use_db)
                    cls._db = mongodb_handler
                    cls._db_type = 'mongodb'
                    cls._db_name = mongodb_use_db
                pass
            pass
        pass

    @classmethod
    def tearDownClass(cls):
        """
        底层测试用例初始化还原
        目前支持对 `mongoengine` 和 `peewee.MySQLDatabase` 的数据库测试

        如果是mongodb,则直接删除数据库

        如果是peewee,倒序执行revert

        :return:
        """

        if cls._db_type == 'mongodb':
            cls._db.drop_database(cls._db_name)
        elif cls._db_type == 'mysql':
            try:
                import importlib
                mod = importlib.import_module(Settings._db_patch_path)

                for m in reversed(mod.__all__):
                    patch = importlib.import_module(Settings._db_patch_path + '.' + m)
                    if hasattr(patch, 'revert'):
                        patch.revert()
                    pass

            except ImportError:
                pass
            pass
        pass

        super(TestCase, cls).tearDownClass()
        pass

    pass

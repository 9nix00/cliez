# -*- coding: utf-8 -*-

import os
from cliez.base.component import Component
from cliez.conf import settings
import importlib
import inspect
from builtins import dict
import json


class DumpComponent(Component):
    models = None

    def run(self, options):
        """
        ...experimental::

            实验性质的内容,目前并不太确定还要不要继续

            实际的体验,SPA的模式也有SPA的问题,相比我更喜欢传统的模式


        该模式灵感来源于在对django和flask的思考.


        flask完全与db无关,而django高度整合db.
        但是在我们现有的架构中,前端与后端是完全分离的.

        django的检测策略显得很纠结.
        要么实现单独的逻辑,要么直接依赖于后端

        而flask则什么都没有,要么引入wtf,再复制一个django.
        要么还是依赖于前端自己实现.


        所幸,无论对于flask还是django.在model层,我们都有基础的控制.
        比如长度超限,比如格式的基本检查,这些都是会检测异常的.

        而服务器后端所作的检查其实非常有限.

        那么我们可以想象到这样的场景:

        如果我们把django的form机制,转移到前端来实现呢?

        这个答案看上去让人很满意: 我们既解决了前端的复杂度,在后端仍然能保证安全和数据准确性.


        策略:

        * 根据选项装载环境,目前支持django和flask

            模拟链接:

                * peewee 严格算并不依赖于数据库链接,但是因为我们框架中默认实现了db的加载方式,所以强制需要链接
                * mongoengine 使用model强制依赖链接


        * 加载指定的models文件,python 做 import

        * 尝试解析内部的model类型,目前支持 peewee 和 mongoengine 两种

        * 生成json文件至指定的目录


        :param argparser options:
        :return: None
        """

        module_name = options.module_name

        if options.flask:
            if options.settings:
                app = settings(options.settings).app
            else:
                app = settings(module_name + '.settings').app

            app.config.from_object(settings().DevelopmentConfig)

        elif options.django:

            if not options.settings:
                self.error("when you use django mode,you must set `--settings` to DJANGO_SETTINGS_MODULE")

            os.environ.setdefault('DJANGO_SETTINGS_MODULE', options.settings)

            # try:
            #     importlib.import_module(options.settings)
            # except ImportError:
            #     self.error("can't find config.path:`{}`".format(options.path))
            # pass

        pass

        try:
            models = importlib.import_module(module_name + '.models')
        except ImportError:
            self.error("can't find models.path:`{}`".format(options.path))
            pass

        classes = inspect.getmembers(models, inspect.isclass)

        models = self.filter_peewee_models(classes)
        models += self.filter_mongoengine_models(classes)
        models += self.filter_django_models(classes)

        fields = self.parse(models)

        buffer = json.dumps(fields)

        # open(options.output,'w').write(buffer)

        real_path = os.path.expanduser(options.output)

        if os.path.exists(real_path) and not options.replace:
            self.error("file exist. if you want to replace it. please add `--replace` option")
            pass

        open(real_path, 'w').write(buffer)
        pass

    def filter_peewee_models(self, models):
        import peewee
        return [('peewee', v[1]) for v in models if issubclass(v[1], peewee.Model) and v[1] != peewee.Model]

    def filter_django_models(self, models):
        """
        Django Model 过滤规则说明:

        - 过滤掉了基类
        - 过滤掉结尾为Mixin的类


        :param models:
        :return:
        """
        from django.db.models import Model

        return [('django', v[1]) for v in models if issubclass(v[1], Model) \
                and v[1] != Model \
                and not v[1].__name__.endswith('Mixin') \
                and v[1]._meta.abstract is False
                ]

    def filter_mongoengine_models(self, models):
        import mongoengine
        return [('mongo', v[1]) for v in models if issubclass(v[1], mongoengine.Document) and v[1] not in [mongoengine.Document, mongoengine.DynamicDocument]]

    def parse(self, models):
        """

        策略:

        - 调用能识别的依赖
        - 筛选出所有非方法字段\隐藏字段\tuple数据结构
        - 遍历数据生成关注列表,目前关注的项目

            - name:用于提交字段
            - verbose_name: 显示名称,用于组合错误提示
            - max_length: 仅在字符串类型时出现
            - choices: 选项列表
            - help_text:帮助消息
            - api_unique:唯一字段时,如果指定了api接口出现


        :param models: 数据模型
        :return:
        """

        data = {}

        for type_name, model in models:
            method = getattr(self, 'parse_{}'.format(type_name))
            data[model.__name__] = method(model)
            pass

        return data

    def parse_peewee(self, model):
        """
        peewee 分类
        处理单个model,并获取最终的fields

        :param model:
        :return:
        """

        data = {}
        data_variable = [v for v in dir(model) if not v.startswith('_') \
                         and not callable(getattr(model, v)) \
                         and not isinstance(v, tuple)
                         ]

        for field_name in data_variable:

            field = getattr(model, field_name)

            if hasattr(field, 'name') and field.name != 'id':
                tmp = dict(
                    verbose_name=field.verbose_name,
                    name=field.name,
                    help_text=field.help_text,
                    choices=field.choices,
                    max_length=field.max_length if hasattr(field, 'max_length') else None,
                    type=getattr(field, 'extra_type', field.db_field),
                    api_unique=getattr(field, 'api_unique', None) if field.unique else None
                )

                tmp = dict((k, v) for k, v in tmp.items() if v is not None)
                data[field_name] = tmp
                pass

            pass

        return data

    def convert_django_to_type(self, field):

        from django.db import models

        if field in (models.BigIntegerField, models.IntegerField):
            return 'int'
        elif field in (models.CharField,):
            return 'string'
        elif field in (models.URLField,):
            return 'url'
        elif field in (models.EmailField,):
            return 'email'

        pass

    def parse_django(self, model):
        """
        处理django的model

        .. todo::
           目前不支持的选项是verbose_name因为django底层使用了translate. 而这个proxy又依赖AppRegistry,导致转换失败.
           暂时使用filed.name替代


        :param model:
        :return:
        """

        import django
        django.setup()

        data = {}
        model = model._meta.get_fields()

        data_variable = [v for v in model]

        for field in data_variable:

            if hasattr(field, 'name') and field.name != 'id' and field.name != 'pk':
                tmp = dict(
                    verbose_name=str(field.name),
                    name=field.name,
                    help_text=str(field.help_text),
                    choices=field._choices if field._choices else None,
                    max_length=field.max_length if hasattr(field, 'max_length') else None,
                    type=self.convert_django_to_type(field),
                    api_unique=getattr(field, 'api_unique', None) if field.unique else None
                )

                tmp = dict((k, v) for k, v in tmp.items() if v is not None)
                data[field.name] = tmp
                pass

            pass

        return data

    def parse_mongo(self, model):
        """

        处理单个model,并获取最终的fields

        :param model:
        :return:
        """

        data = {}
        data_variable = [v for v in dir(model) if not v.startswith('_') \
                         and not callable(getattr(model, v)) \
                         and not isinstance(getattr(model, v), tuple) \
                         and v != 'STRICT'
                         ]

        for field_name in data_variable:

            field = getattr(model, field_name)

            if hasattr(field, 'name') and field.name != 'id' and field.name != 'pk':
                tmp = dict(
                    verbose_name=field.verbose_name,
                    name=field.name,
                    help_text=field.help_text,
                    choices=field.choices,
                    max_length=field.max_length if hasattr(field, 'max_length') else None,
                    type=getattr(field, 'extra_type', field.db_field),
                    api_unique=getattr(field, 'api_unique', None) if field.unique else None
                )

                tmp = dict((k, v) for k, v in tmp.items() if v is not None)
                data[field_name] = tmp
                pass

            pass

        return data

    @staticmethod
    def append_arguments(sub_parsers):
        sub_parser = sub_parsers.add_parser('dump', help='dump json from web models')
        sub_parser.add_argument('module_name', help='cliez style flask module')
        sub_parser.add_argument('output', help='file write path')
        sub_parser.add_argument('--replace', action='store_true', help='force rewrite allow file')
        sub_parser.add_argument('--settings', help='set cliez-flask settings')
        sub_parser.add_argument('--flask', action='store_true', help='init flask config resource')
        sub_parser.add_argument('--django', action='store_true', help='init django config resource')
        pass

    pass

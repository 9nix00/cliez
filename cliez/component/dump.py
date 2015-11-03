# -*- coding: utf-8 -*-

import os
from datetime import datetime
from cliez.base.component import Component
import importlib


class DumpComponent(Component):
    def run(self, options):
        """
        输出关于web model的前端验证策略

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

        加载指定的models文件,python 做 import
        尝试解析内部的model类型,目前支持 peewee 和 mongoengine 两种
        生成json文件至指定的目录

        :param argparser options:
        :return: None
        """

        load_models = options.path

        try:
            models = importlib.import_module(load_models)
        except ImportError:
            self.error("can't find models.path:{}", options.path)
            pass




        pass

    @staticmethod
    def append_arguments(sub_parsers):
        sub_parser = sub_parsers.add_parser('dump', help='dump json from web models')
        sub_parser.add_argument('path', help='python models full-name.e.g: pkg.module.models')

        sub_parser.add_argument('--output', action='store_true', help='create cli-app with simple mode')
        sub_parser.add_argument('--prefix', nargs='?', help='replace package prefix to null')
        sub_parser.description = InitComponent.load_description('cliez/manual/main.txt')
        pass

    pass

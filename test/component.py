# -*- coding: utf-8 -*-

import unittest
from cliez.base.component import Component


class ComponentTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_resource(self):
        """
        资源加载测试,正常情况以下功能不抛出异常
        :return:
        """
        a = Component()
        a.load_resource('component.py', root='cliez/base')
        a.load_resource('base/component.py', root='cliez')
        a.load_resource('/base/component.py', root='cliez')
        a.load_resource('cliez/base/component.py')
        a.load_resource(__file__.rsplit('/', 2)[0] + '/cliez/base/component.py')
        pass

    pass

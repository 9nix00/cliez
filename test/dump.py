# -*- coding: utf-8 -*-

"""
please make sure you have `~/Downloads` path
"""

import os
import sys
from cliez.main import main
from unittest import TestCase


class DumpTestCase(TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.join(__file__.rsplit('/', 2)[0], 'demo', 'blueprint_demo'))

        import mongoengine
        mongoengine.connect('test', host='mongodb://127.0.0.1')
        pass

    def test_ok(self):
        sys.argv = ['cmd', 'dump', 'blueprint_demo', '~/Downloads/accounts.json', '--replace', '--flask']
        main()
        pass

    pass


class DumpMongoTestCase(TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.join(__file__.rsplit('/', 2)[0], 'demo', 'blueprint_demo'))
        pass

    def test_ok(self):
        sys.argv = ['cmd', 'dump', 'blueprint_demo', '~/Downloads/accounts.json', '--replace', '--settings', 'blueprint_demo.settings_mongo', '--flask']
        main()
        pass

    pass


class DumpDjangoModelTestCase(TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.join(__file__.rsplit('/', 2)[0], 'demo', 'django_demo'))
        pass

    def test_ok(self):
        sys.argv = ['cmd', 'dump', 'django_demo', '~/Downloads/accounts.json', '--replace', '--django', '--settings', 'django_config.settings']
        main()
        pass

    pass

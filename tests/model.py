# -*- coding: utf-8 -*-

import unittest
from cliez.conf import settings, Settings


class Model(object):
    config_none = settings()

    def __init__(self):
        self.config = settings()
        pass

    pass


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        Settings.bind('cliez.conf')
        pass

    def test_ok(self):
        a = Model()
        self.assertEqual(None, a.config_none)
        self.assertEqual(Settings, a.config.__class__)
        pass

    pass

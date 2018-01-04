import os
import sys
from unittest import TestCase, main

from cliez.conf import settings, Settings


class Model(object):
    config_none = settings()

    def __init__(self):
        self.config = settings()
        pass

    pass


class SettingsTests(TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.dirname(__file__))
        Settings.bind('res_settings.demo', __file__)
        self.model = Model()
        pass

    def test_ok(self):
        self.assertEqual(Settings, self.model.config.__class__)

        self.assertEqual(2, self.model.config.public_var)
        with self.assertRaises(AttributeError):
            _ = self.model.config._private_var

        pass

    def test_is_none(self):
        self.assertEqual(None, self.model.config_none)
        pass

    pass


if __name__ == '__main__':
    main()

from unittest import TestCase
import argparse
import os
import cliez
from cliez import conf, parser, version


class NormalTest(TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(version))
        conf.COMPONENT_ROOT = os.path.join(__file__.rsplit('/', 2)[0], 'demo', 'argparse_demo', 'argparse_pkg')

    pass

    def test_ignore_set_root(self):
        with self.assertRaises(SystemExit):
            conf.COMPONENT_ROOT = None
            parser.parse(self.parser, argv=['anything'])
            pass
        pass

    # 测试用例参数通常会>2
    # def test_none(self):
    #     with self.assertRaises(Exception):
    #         parser.parse(self.parser, argv=[])
    #         pass
    #     pass

    def test_ok(self):
        parser.parse(self.parser, argv=['command', 'init'])
        pass

    def test_allow_show_version(self):
        with self.assertRaises(SystemExit):  # "will call parser.exit"
            parser.parse(self.parser, argv=['command', '--version'])
        pass

    def test_no_value(self):
        with self.assertRaises(AttributeError):
            result = parser.parse(self.parser, argv=['command'], active_one=lambda option: option.version)
            pass
        pass

    def test_active_one(self):
        self.parser.add_argument('--port', nargs='?', type=int, default=8000)
        result = parser.parse(self.parser, argv=['command'], active_one=lambda option: option.port)
        self.assertEqual(result, 8000)
        pass

    def test_active_show_invalid(self):
        with self.assertRaises(SystemExit):  # "unknow params"
            result = parser.parse(self.parser, argv=['command', '--port'])
            self.assertEqual(result, version)
        pass

    def test_ok_with_config(self):
        from cliez.conf import Settings
        obj = parser.parse(self.parser, argv=['command', 'init'], settings_module='cliez.loader')
        self.assertEqual(True, isinstance(obj.settings, Settings))
        pass

    pass

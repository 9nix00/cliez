from unittest import TestCase, main
import argparse
import os
import cliez
from cliez import conf, parser, version


class NormalTest(TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(version))
        conf.COMPONENT_ROOT = os.path.dirname(__file__)

    pass

    def test_ignore_set_root(self):
        with self.assertRaises(SystemExit):
            conf.COMPONENT_ROOT = None
            parser.parse(self.parser, argv=['anything'])
            pass
        pass

    # it cloudn't be happen in real world. skip it.
    # def test_none(self):
    #     with self.assertRaises(Exception):
    #         parser.parse(self.parser, argv=[])
    #         pass
    #     pass

    def test_allow_show_version(self):
        with self.assertRaises(SystemExit):  # "will call parser.exit"
            parser.parse(self.parser, argv=['command', '--version'])
        pass

    def test_no_value(self):
        with self.assertRaises(AttributeError):
            result = parser.parse(self.parser, argv=['command'], no_args_func=lambda option: option.version)
            pass
        pass

    def test_no_args_func(self):
        self.parser.add_argument('--port', nargs='?', type=int, default=8000)
        result = parser.parse(self.parser, argv=['command'], no_args_func=lambda option: option.port)
        self.assertEqual(result, 8000)
        pass

    def test_active_show_invalid(self):
        with self.assertRaises(SystemExit):  # "unknow params"
            result = parser.parse(self.parser, argv=['command', '--port'])
            self.assertEqual(result, version)
        pass

    pass


if __name__ == '__main__':
    main()

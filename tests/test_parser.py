import argparse
import os
from unittest import TestCase, main

from cliez import conf, parser, version


class ParserTests(TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--version', action='version',
                                 version='%(prog)s v{}'.format(version))
        conf.COMPONENT_ROOT = os.path.dirname(__file__)

    pass

    def test_ignore_set_root(self):
        with self.assertRaises(SystemExit) as cm:
            conf.COMPONENT_ROOT = None
            parser.parse(self.parser, argv=['anything'])
            pass

        self.assertEqual(cm.exception.code, 2)
        pass

    # def test_none(self):
    #     """
    #     it cloudn't be happen in real world.
    #     skip it.
    #
    #     :return:
    #     """
    #     with self.assertRaises(Exception):
    #         parser.parse(self.parser, argv=[])
    #         pass
    #     pass

    def test_allow_show_version(self):
        with self.assertRaises(SystemExit) as cm:
            parser.parse(self.parser, argv=['command', '--version'])

        self.assertEqual(cm.exception.code, 0)
        pass

    def test_no_value(self):
        result = parser.parse(self.parser, argv=['command'],
                              no_args_func=lambda option: 'ok')

        self.assertEqual('ok', result)
        pass

    def test_no_args_func(self):
        self.parser.add_argument('--port', nargs='?', type=int, default=8000)
        result = parser.parse(self.parser, argv=['command'],
                              no_args_func=lambda option: option.port)
        self.assertEqual(result, 8000)
        pass

    def test_active_show_invalid(self):
        with self.assertRaises(SystemExit) as cm:
            result = parser.parse(self.parser, argv=['command', '--port'])
            self.assertEqual(result, version)

        self.assertEqual(cm.exception.code, 2)
        pass

    pass


if __name__ == '__main__':
    main()

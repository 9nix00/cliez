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

    def test_none(self):
        with self.assertRaises(ImportError):
            parser.parse(self.parser, argv=[])
            pass
        pass

    def test_ok(self):
        parser.parse(self.parser, argv=['command', 'init'])
        pass

    def test_ok_with_config(self):
        from cliez.conf import Settings
        obj = parser.parse(self.parser, argv=['command', 'init'], settings_module='cliez.loader')
        self.assertEqual(True, isinstance(obj.settings, Settings))
        pass

    pass

from unittest import TestCase
import argparse
import os
import sys
from cliez import conf, parser, version


class NormalTest(TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(version))
        conf.PACKAGE_ROOT = os.path.join(__file__.rsplit('/', 2)[0], 'demo', 'argparse_demo', 'argparse_pkg')

    pass

    def test_ignore_set_root(self):
        with self.assertRaises(SystemExit):
            conf.PACKAGE_ROOT = None
            parser.parse(self.parser, argv=['anything'])
            pass
        pass

    def test_none(self):
        with self.assertRaises(ValueError):
            parser.parse(self.parser, argv=[])
            pass
        pass

    # def test_ok(self):
    #     sys.path.append(conf.PACKAGE_ROOT)
    #     parser.parse(self.parser, argv=['command', 'init'])
    #     pass

    pass

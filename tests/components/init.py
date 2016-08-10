# -*- coding: utf-8 -*-

import unittest
import argparse
import mock
import tempfile
from cliez import parser

try:
    input = raw_input
    mock_input = '__builtin__.raw_input'
except NameError:
    mock_input = 'builtins.input'
    pass


class InitComponentTestCase(unittest.TestCase):
    def setUp(self):
        from cliez import main
        pass

    def test_ok(self):
        """
        缺失参数
        :return:
        """

        with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
            parser.parse(argparse.ArgumentParser(), argv=['command', 'init'])

        pass

    def test_no_confirm(self):
        """
        缺失参数
        :return:
        """

        with self.assertRaises(SystemExit):
            parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--yes'])

        pass

    pass

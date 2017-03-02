# -*- coding: utf-8 -*-

import os
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
        dp = tempfile.TemporaryDirectory()
        parser.parse(argparse.ArgumentParser(), argv=['command', 'create', 'wangwenpei/cliez-kickstart', '--dir', dp.name, '--debug'])

        with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
            parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--dir', dp.name, '--debug'])

        pass

    def test_with_variables(self):
        """
        custom variable
        :return:
        """

        with tempfile.TemporaryDirectory() as dp:
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create', 'wangwenpei/cliez-kickstart', '--dir', dp, '--debug'])

            with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
                parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--dir', dp, '--debug', '-s', 'keywords:a-keyword'])

        pass

    def test_skip_builtin(self):
        """
        custom variable
        :return:
        """

        with tempfile.TemporaryDirectory() as dp:
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create', 'wangwenpei/cliez-kickstart', '--dir', dp, '--debug'])
            parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--dir', dp, '--debug', '-s', 'keywords:a-keyword', '--skip-builtin', '--yes'])

        pass

    # def test_in_invalid_root(self):
    #     """
    #     missing argument
    #     :return:
    #     """
    #
    #     dp = tempfile.TemporaryDirectory()
    #     os.chdir(dp.name)
    #
    #     with self.assertRaises(SystemExit):
    #         with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
    #             parser.parse(argparse.ArgumentParser(), argv=['command', 'init'])
    #
    #     pass

    def test_in_dange_root(self):
        """
        缺失参数
        :return:
        """

        with self.assertRaises(SystemExit):
            with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
                parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--dir', '/'])

        os.chdir(os.path.expanduser('~'))
        with self.assertRaises(SystemExit):
            with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
                parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--dir', '/'])

        pass

    def test_no_confirm(self):
        """
        :return:
        """

        with tempfile.TemporaryDirectory() as dp:
            with mock.patch(mock_input, side_effect=['pkg_demo', "\n", "\n"]):
                parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--yes', '--dir', dp])

        pass

    pass

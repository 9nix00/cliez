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
        """
        缺失参数
        :return:
        """

        dp = tempfile.TemporaryDirectory()
        parser.parse(argparse.ArgumentParser(), argv=['command', 'create', '9nix00/cliez-kickstart', '--dir', dp.name, '--debug'])

        with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
            parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--dir', dp.name, '--debug'])

        pass

    def test_with_variables(self):
        """
        缺失参数
        :return:
        """

        dp = tempfile.TemporaryDirectory()
        parser.parse(argparse.ArgumentParser(), argv=['command', 'create', '9nix00/cliez-kickstart', '--dir', dp.name, '--debug'])

        with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
            parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--dir', dp.name, '--debug', '-s', 'keywords:a-keyword'])

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
        os.chdir('/')

        with self.assertRaises(SystemExit):
            with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
                parser.parse(argparse.ArgumentParser(), argv=['command', 'init'])

        os.chdir(os.path.expanduser('~'))
        with self.assertRaises(SystemExit):
            with mock.patch(mock_input, side_effect=['yes', 'pkg_demo', "\n", "\n"]):
                parser.parse(argparse.ArgumentParser(), argv=['command', 'init'])

        pass

    def test_no_confirm(self):
        """
        :return:
        """
        dp = tempfile.TemporaryDirectory()
        os.chdir(dp.name)

        with mock.patch(mock_input, side_effect=['pkg_demo', "\n", "\n"]):
            parser.parse(argparse.ArgumentParser(), argv=['command', 'init', '--yes'])

        pass

    pass

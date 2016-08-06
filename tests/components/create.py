# -*- coding: utf-8 -*-

import unittest
import argparse

import tempfile
from cliez import parser


class CreateComponentTestCase(unittest.TestCase):
    def setUp(self):
        from cliez import main
        pass

    def test_missing(self):
        """
        缺失参数
        :return:
        """

        with self.assertRaises(SystemExit):
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create'])

        pass

    def test_github_mode(self):
        """
        github模式
        :return:
        """

        with tempfile.TemporaryDirectory() as dp:
            os.chdir(dp)
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create', '9nix00/cliez'])
            pass

        pass

    def test_local_mode(self):
        """
        本地模式
        :return:
        """

        with tempfile.TemporaryDirectory() as dp:
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create', __file__.rsplit('/', 3)[0], dp, '--local'])
            pass
        pass

    def test_bitbucket_mode(self):
        """
        本地模式
        :return:
        """

        with tempfile.TemporaryDirectory() as dp:
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create', __file__.rsplit('/', 3)[0], dp, '--bitbucket'])
            pass
        pass

    pass

# -*- coding: utf-8 -*-

import unittest
import argparse
import os

import tempfile
from cliez import parser


class CreateComponentTestCase(unittest.TestCase):
    def setUp(self):
        from cliez import main
        pass

    def test_missing(self):
        """
        missing argument
        :return:
        """

        with self.assertRaises(SystemExit):
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create'])

        pass

    def test_github_mode(self):
        """
        github mode
        :return:
        """

        with self.assertRaises(SystemExit):
            with tempfile.TemporaryDirectory() as dp:
                os.chdir(dp)
                parser.parse(argparse.ArgumentParser(), argv=['command', 'create', '9nix00/cliez',
                                                              '--dir', os.getcwd(),  # you must be specify `--dir` option in testcase
                                                              '--debug'])
            pass

        pass

    def test_local_mode(self):
        """
        local mode
        :return:
        """
        with self.assertRaises(SystemExit):
            with tempfile.TemporaryDirectory() as dp:
                parser.parse(argparse.ArgumentParser(), argv=['command', 'create', __file__.rsplit('/', 3)[0], dp,
                                                              '--dir', os.getcwd(),  # you must be specify `--dir` option in testcase
                                                              '--local'])
                pass
        pass

    def test_bitbucket_mode(self):
        """
        bitbucket first-order mode
        :return:
        """

        with tempfile.TemporaryDirectory() as dp:
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create', __file__.rsplit('/', 3)[0], dp, '--bitbucket'])
            pass
        pass

    pass

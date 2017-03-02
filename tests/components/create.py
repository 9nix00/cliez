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

        with tempfile.TemporaryDirectory() as dp:
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create', 'wangwenpei/cliez-kickstart',
                                                          '--dir', dp,  # you must be specify `--dir` option in testcase
                                                          '--debug'])
        pass




    pass


# class CreateComponentTestCase2(unittest.TestCase):
#
#     def test_local_mode(self):
#         """
#         local mode
#         :return:
#         """
#
#         with tempfile.TemporaryDirectory() as dp:
#             parser.parse(argparse.ArgumentParser(), argv=['command', 'create', __file__.rsplit('/', 3)[0], dp,
#                                                           '--dir', dp,  # you must be specify `--dir` option in testcase
#                                                           '--local'])
#             pass
#         pass
#
#     pass
#
#
# class CreateComponentTestCase3(unittest.TestCase):
#
#     def test_bitbucket_mode(self):
#         """
#         bitbucket first-order mode
#         :return:
#         """
#
#         with tempfile.TemporaryDirectory() as dp:
#             parser.parse(argparse.ArgumentParser(), argv=['command', 'create', 'nextoa/cliez-kickstart',
#                                                           '--dir', dp,  # you must be specify `--dir` option in testcase
#                                                           '--debug', '--bitbucket'])
#             pass
#         pass
#
#     pass
#


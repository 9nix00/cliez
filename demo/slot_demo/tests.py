# -*- coding: utf-8 -*-

from unittest import TestCase
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import slot_pkg

from cliez import conf, parser

conf.COMPONENT_ROOT = os.path.dirname(slot_pkg.__file__)


class DemoTests(TestCase):
    def test_ok(self):
        """
        数据无效时
        :return:
        """
        parser.parse(argparse.ArgumentParser(), argv=['command', 'daemon', '--once', '--threads', '1'])
        pass

    def test_ok(self):
        """
        排他模式,排他模式时,只允许运行一个
        :return:
        """
        parser.parse(argparse.ArgumentParser(), argv=['command', 'daemon', '--once', '--exclusive-mode', '--threads', '1'])
        pass

    pass

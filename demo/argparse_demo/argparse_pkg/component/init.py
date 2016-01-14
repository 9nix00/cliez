# -*- coding: utf-8 -*-

import os
from cliez.base.component import Component


class InitComponent(Component):
    """
    init component
    """

    def run(self, options):
        print("init called...")
        print("argument list:", options)
        pass

    @staticmethod
    def append_arguments(sub_parsers):
        sub_parser = sub_parsers.add_parser('init', help='init project')
        sub_parser.description = InitComponent.load_description('argparser_pkg/manual/init.txt')
        pass

    pass

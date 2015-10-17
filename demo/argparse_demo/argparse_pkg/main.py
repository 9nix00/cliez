# -*- coding: utf-8 -*-

from cliez.parser import parse
from cliez.base.component import Component
from cliez import conf

import argparse
import os
import sys

import argparse_pkg

conf.PACKAGE_ROOT = os.path.dirname(__file__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=Component.load_description(os.path.join(os.path.dirname(__file__), 'manual', 'main.txt')),
        epilog='You can submit issues at: https://www.github.com/9nix00/cliez',
    )
    parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(argparse_pkg.version))
    parse(parser)
    pass

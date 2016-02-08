# -*- coding: utf-8 -*-

from cliez.parser import parse
from cliez.base.component import Component
from cliez import conf

import argparse
import os
import sys

sys.path.insert(0, __file__.rsplit('/', 2)[0])

import slot_pkg

conf.COMPONENT_ROOT = os.path.dirname(__file__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description=Component.load_description('slot/manual/main.txt'),
            epilog='You can submit issues at: https://www.github.com/9nix00/cliez',
    )
    parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(slot_pkg.version))
    parse(parser)
    pass

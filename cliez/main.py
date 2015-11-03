# -*- coding: utf-8 -*-

import os
import argparse
from cliez import conf, version
from cliez.base.component import Component
from cliez.parser import parse

conf.COMPONENT_ROOT = os.path.dirname(__file__)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=Component.load_description('cliez/manual/main.txt'),
        epilog='You can submit issues at: https://www.github.com/9nix00/cliez',
    )
    parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(version))
    parser.add_argument('--dir', nargs='?', default=os.getcwd(), help='set working directory')
    parse(parser)
    pass


if __name__ == "__main__":
    main()
    pass

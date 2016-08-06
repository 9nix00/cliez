# -*- coding: utf-8 -*-

import os
import argparse
from cliez import conf, version
from cliez.parser import parse

conf.COMPONENT_ROOT = os.path.dirname(__file__)
conf.GENERAL_ARGUMENTS = [
    (('--dir',), dict(nargs='?', default=os.getcwd(), help='set working directory')),
]
conf.EPILOG = 'You can submit issues at: https://www.github.com/9nix00/cliez'

def main():
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=conf.EPILOG,
    )

    for v in conf.GENERAL_ARGUMENTS:
        parser.add_argument(*v[0], **v[1])

    parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(version))
    parse(parser)
    pass


if __name__ == "__main__":
    main()
    pass

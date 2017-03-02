# -*- coding: utf-8 -*-

import os
import argparse
from cliez import conf, version
from cliez.parser import parse

conf.COMPONENT_ROOT = os.path.dirname(__file__)
conf.GENERAL_ARGUMENTS = [
    (('--dir',), dict(nargs='?', default=os.getcwd(), help='set working directory')),
    (('--debug',), dict(action='store_true', help='open debug mode')),
    (('--dry-run',), dict(action='store_true', help='print command instead execute it')),
    (('--verbose', '-v'), dict(action='count')),
]
conf.EPILOG = 'You can submit issues at: https://www.github.com/wangwenpei/cliez'


def main():
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=conf.EPILOG,
    )

    for v in conf.GENERAL_ARGUMENTS:
        parser.add_argument(*v[0], **v[1])

    parser.add_argument('--version', '-V', action='version', version='%(prog)s v{}'.format(version))
    parse(parser)
    pass


if __name__ == "__main__":
    main()
    pass

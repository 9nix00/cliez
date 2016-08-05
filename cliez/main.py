# -*- coding: utf-8 -*-

import os
import argparse
from cliez import version
from cliez.parser import parse


def main():
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="popular python project code generator",
            epilog='You can submit issues at: https://www.github.com/9nix00/cliez',
    )
    parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(version))
    parser.add_argument('--dir', nargs='?', default=os.getcwd(), help='set working directory')
    parse(parser)
    pass


if __name__ == "__main__":
    main()
    pass

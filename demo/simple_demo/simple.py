# -*- coding: utf-8 -*-

from cliez.loader import ArgLoader


def pp(loader):
    usage = (
        ("--opt3", "comment for opt", '-c'),
        ("--opt4:", "comment for opt", '-d')
    )

    b = ArgLoader(options=usage, sys_argv=a.argv)
    print(b.options['--opt3'])
    pass


def hello(loader):
    if loader.options['--debug']:
        print("open debug mode:")
        print("load data: ", repr(a))
        pass

    print("called hello")
    pass


def main(a):
    if a.options['--help']:
        print(a)
        return

    if a.actions['hello']:
        hello(a)
        return

    if a.actions['parent']:
        pp(a)
        return

    pass


if __name__ == "__main__":
    options = (
        "Usage: command [options] arguments",
        "",
        "document line1",
        "document line2",
        "document line3",
        "",  # blank line
        "Options:",
        ("--opt1", "comment for opt", '-a'),
        ("--opt2:", "comment for opt", '-b'),
        "Actions",
        ("@hello", "call hello"),
        ("@parent", "support sub argument"),
        "",
        ("--help", "print help document", '-h'),
        ("--debug", "debug mode"),
    )

    a = ArgLoader(options=options)
    main(a)
    pass

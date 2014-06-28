import cliez.loader

if __name__ == "__main__":
    options = (
        "Useage: cliez.ArgLoader Example",
        "",
        "Options",
        ('--help', 'print help document.', '-h'),
        "",
        "HOW-TO:",
        "    Format:",
        "        options = (argument-list)",
        "        argument-list = ('-option[:]|@action','docs','alias1','alias2','alias...')",
        "",
        "    Options-Demo:",
        "        options = (",
        "           ('--help', 'print help document', '-h')",
        "           ('@checkout', 'checkout repo', 'co')",
        "        )",
        "        a = ArgLoader(options=options)"
        "        if '--help' in  a.options:"
        "           print a"
    )

    a = cliez.loader.ArgLoader(options=options)

    print "****This is used for document****"
    print a
    #
    print "****This is used for debug****"
    print repr(a)
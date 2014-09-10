Cliez
==================

`Cliez <http://cliez.kbonez.com>`_ is a Python library for CLI environment


Upgrade notes
-------------

As of Cliez 0.9, we change  ``--sleep_max`` option to ``--sleep-max``.

Quick links
-----------

* `Documentation <http://cliez.kbonez.com/>`_
* `Source (github) <https://github.com/kbonez/cliez>`_



A Demo
------------

Here is a simple "How to use" example for Cliez::

    import cliez

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
        "        if a.options['--help']:"
        "           print a"
    )

    a = ArgLoader(options=options)

    print "****This is used for document****"
    print a
    #
    print "****This is used for debug****"
    print repr(a)



Installation
------------

**Automatic installation**::

    pip install cliez

Cliez is listed in `PyPI <http://pypi.python.org/pypi/cliez/>`_ and
can be installed with ``pip`` or ``easy_install``.
it includes demo applications.


**Manual installation**: Download the latest source from `Github
<http://www.github.com/kbonez/cliez/>`_.

.. parsed-literal::

    git clone  https://github.com/kbonez/cliez.git
    cd cliez
    python setup.py build
    sudo python setup.py install

The Cliez source code is `hosted on GitHub
<https://github.com/kbonez/cliez/>`_.

**Prerequisites**: Cliez was only test on Python 2.7.  It may be runs on
all Python versions.


Discussion and support
----------------------

You can discuss and report bugs on
the `GitHub issue tracker
<https://github.com/kbonez/cliez/issues>`_.


This web site and all documentation is licensed under `Creative
Commons 3.0 <http://creativecommons.org/licenses/by/3.0/>`_.

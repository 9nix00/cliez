Cliez
==================

`Cliez <http://cliez.kbonez.com>`_ Parser for command-line options,easier but limited than :py:class:`sys.argparse`


Quick links
-----------

* `Documentation <http://cliez.readthedocs.org/>`_
* `Source (github) <https://github.com/nextoa/cliez>`_


Why Cliez
------------------------------------------------------------------------------------------------

python :py:class:`sys.argparse` is powerful,but it's a little complex in most case when we create a small CLI-APP.
we just need recognize which param is option,action or just a argv parameter. and can publish with a simple manual.

the below command syntax is support:

.. code-block:: shell

    git clone URL

    curl -d OPTION ARGV


the below syntax is not support:

.. code-block:: shell

    command --a=1

    command --a=1 --a=2



A Demo
------------

Here is a simple "How to use" example for Cliez

.. code-block:: python

    from cliez.loader import ArgLoader

    useage = (
        "Useage  COMMAND [options]  arguments",
        "",
        "document line1",
        "document line2",
        "",  # blank line
        "Options:",
        ("--opt1", "comment for opt", '-a'),
        ("--opt2:", "comment for opt", '-b'),
        "Actions",
        ("@hello", "call hello"),
        "",
        ("--help", "print help document", '-h'),
        ("--debug", "debug mode"),
    )


    a = ArgLoader(options=options)

    print "****This is used for document****"
    print(a)
    #
    print("****This is used for debug****")
    print(repr(a))

    print(a.options,a.actions,a.argv)








Installation
------------

**Automatic installation**::

    pip install cliez

Cliez is listed in `PyPI <http://pypi.python.org/pypi/cliez/>`_ and
can be installed with ``pip`` or ``easy_install``.
it includes demo applications.


**Manual installation**: Download the latest source from `Github
<http://www.github.com/nextoa/cliez/>`_.

.. parsed-literal::

    git clone  https://github.com/nextoa/cliez.git
    cd cliez
    python setup.py build
    sudo python setup.py install

The Cliez source code is `hosted on GitHub
<https://github.com/nextoa/cliez/>`_.

**Prerequisites**: Cliez was only test on Python 2.7.  It may be runs on
all Python versions.


Discussion and support
----------------------

You can discuss and report bugs on
the `GitHub issue tracker
<https://github.com/nextoa/cliez/issues>`_.


This web site and all documentation is licensed under `Creative Commons 3.0 <http://creativecommons.org/licenses/by/3.0/>`_.

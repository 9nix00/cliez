Cliez
==================

A Cli App framework to make CLI-App easier.


Quick links
-----------

* `Documentation <http://cliez.readthedocs.org/>`_
* `Source (github) <https://github.com/9nix00/cliez>`_
* `Chinese Documentation <http://cliez.readthedocs.org/en/latest/i18n/zh_cn/>`_


Why Cliez
------------------------------------------------------------------------------------------------

python `argparser <https://docs.python.org/3/library/argparse.html>`_ is powerful,
but it's a little complex in most case when we create a small CLI-APP,like `ls`.
we just need recognize which param is option,action or just a argv parameter. and can publish with a simple manual.


In other case. when we need to create complex CLI-App. like `git`,
use `argparser` is a good way,but we still need to write some code by ourselves.
for new python guy. you may make your code style looks ugly.


that's why I create cliez. make simple is simple. complex is elegant.



Limit
------------------------------------------------------------------------------------------------

For simple style.

the below syntax is not support:

.. code-block:: shell

    command --a=1

    command --a=1 --a=2


For argparse style.

currently, argparse mode doesn't support installed package. I will add this feature in my spare time.


Demo
------------

I create demo for easier use this, or you can use `cliez init` to touch them


`Simple Style <https://github.com/9nix00/cliez/blob/master/demo/simple_demo/simple.py>`_


`Argparse Style <https://github.com/9nix00/cliez/blob/master/demo/argparse_demo/argparse_pkg>`_


`Flask(blueprint) Style <https://github.com/9nix00/cliez/blob/master/demo/blueprint_demo/>`_



Installation
------------

**Automatic installation**::

    pip install cliez

Cliez is listed in `PyPI <http://pypi.python.org/pypi/cliez/>`_ and
can be installed with ``pip`` or ``easy_install``.
it includes demo applications.


**Manual installation**: Download the latest source from `Github
<http://www.github.com/9nix00/cliez/>`_.

.. parsed-literal::

    git clone  https://github.com/9nix00/cliez.git
    cd cliez
    python setup.py build
    sudo python setup.py install

The Cliez source code is `hosted on GitHub
<https://github.com/9nix00/cliez/>`_.

**Prerequisites**: Cliez was only test on Python 3.4.  But it should be runs on
all Python versions.


Discussion and support
----------------------

You can discuss and report bugs on
the `GitHub issue tracker <https://github.com/9nix00/cliez/issues>`_.


Contribute Code
----------------------

In order to obtain a faster development speed, now we accept Chinese comments.
but the display tips in code *must* be english.


Copyright
-----------

This web site and all documentation is licensed under `Creative Commons 3.0 <http://creativecommons.org/licenses/by/3.0/>`_.

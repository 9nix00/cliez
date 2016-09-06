cliez
==================

A framework to make CLI-App easier.


Quick links
-----------

* `Documentation <http://cliez.nextoa.com/>`_
* `Source (github) <https://github.com/9nix00/cliez>`_
* `cliez-kickstart source code(github) <https://github.com/9nix00/cliez-kickstart>`_


Why cliez
---------

python `argparser <https://docs.python.org/3/library/argparse.html>`_ is powerful,
but we still need to write some code by ourselves,
especially for new python guy. you may make your code style looks ugly.


that's why we create cliez. make cli app easier and more elegant.



Installation
------------

**Automatic installation**::

    pip install cliez

cliez is listed in `PyPI <http://pypi.python.org/pypi/cliez/>`_ and
can be installed with ``pip``.


**Manual installation**: Download the latest source from `Github
<http://www.github.com/9nix00/cliez/>`_.

.. parsed-literal::

    git clone  https://github.com/9nix00/cliez.git
    cd cliez
    python setup.py build
    sudo python setup.py install

The cliez source code is `hosted on GitHub
<https://github.com/9nix00/cliez/>`_.

**Prerequisites**: cliez depends on Git and Mercurial.


**Important Note**: cliez 2.0 is not compatible forward.



Quick Start
-----------

.. parsed-literal::

    cliez check                                                                 # check cliez depends

    cd /tmp                                                                     # change to tmp directory
    cliez create 9nix00/cliez-kickstart cli-app                                 # clone project from github

    cd cli-app                                                                  # change into cli-app directory
    cliez init cli-app                                                          # replace template variables





Discussion and support
----------------------

You can discuss and report bugs on
the `GitHub issue tracker <https://github.com/9nix00/cliez/issues>`_.


Copyright
---------

This web site and all documentation is licensed under `Creative Commons 3.0 <http://creativecommons.org/licenses/by/3.0/>`_.

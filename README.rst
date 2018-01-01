Cliez
==================

A framework to make CLI-App easier.


|build-status| |license| |pyimp|



Quick links
-----------

* `Documentation <https://cliez.readthedocs.io/>`_
* `Source (github) <https://github.com/wangwenpei/cliez>`_
* `cliez-kickstart source code(github) <https://github.com/wangwenpei/cliez-kickstart>`_


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
<http://www.github.com/wangwenpei/cliez/>`_.

.. parsed-literal::

    git clone  https://github.com/wangwenpei/cliez.git
    cd cliez
    python setup.py build
    sudo python setup.py install

The cliez source code is `hosted on GitHub
<https://github.com/wangwenpei/cliez/>`_.

**Prerequisites**: cliez depends on Git and Mercurial.


**Important Note**: cliez 2.0 is not compatible forward and only works on python3+.



Quick Start
-----------

.. parsed-literal::

    cliez check                                                          # check cliez depends

    cd /tmp                                                              # change to tmp directory
    cliez create wangwenpei/cliez-kickstart cli-app                          # clone project from github

    cd cli-app                                                           # change into cli-app directory
    cliez init                                                           # replace template variables



More tips
-----------

Although `cliez` is designed to create a cli app. but you can use it to create any project from github or bitbucket more easier.

you can create your own kickstart project to clone it and replace it.

* create a project from bitbucket

.. parsed-literal::

    cliez create  <bitbucket-team>/<project>  local-project-name  --bitbucket


* create a project from local repository,support Git and Mercurial

.. parsed-literal::

    cliez create  <local-path>  local-project-name



* init code with custom variable,the template variable name must be prefix 3 underline `___` and suffix `___`, like this: `___NAME___`

.. parsed-literal::

    cliez init -s NAME:Jack -s SEX:male

    cliez init -s NAME:Jack -s SEX:male --skip-builtin --yes              # skip set builtin template variable.





Discussion and support
----------------------

You can discuss and report bugs on
the `GitHub issue tracker <https://github.com/wangwenpei/cliez/issues>`_.


Copyright
---------

This web site and all documentation is licensed under `Creative Commons 3.0 <http://creativecommons.org/licenses/by/3.0/>`_.




.. |build-status| image:: https://secure.travis-ci.org/wangwenpei/cliez.png?branch=master
    :alt: Build status
    :target: https://travis-ci.org/wangwenpei/cliez

.. |coverage| image:: https://codecov.io/github/wangwenpei/cliez/coverage.svg?branch=master
    :target: https://codecov.io/github/wangwenpei/cliez?branch=master

.. |license| image:: https://img.shields.io/pypi/l/cliez.svg
    :alt: MIT License
    :target: https://opensource.org/licenses/MIT

.. |wheel| image:: https://img.shields.io/pypi/wheel/cliez.svg
    :alt: Cliez can be installed via wheel
    :target: http://pypi.python.org/pypi/cliez/

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/cliez.svg
    :alt: Supported Python versions.
    :target: http://pypi.python.org/pypi/cliez/

.. |pyimp| image:: https://img.shields.io/pypi/implementation/cliez.svg
    :alt: Support Python implementations.
    :target: http://pypi.python.org/pypi/cliez/



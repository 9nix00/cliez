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

    import tornado.ioloop
    import tornado.web

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")

    application = tornado.web.Application([
        (r"/", MainHandler),
    ])

    if __name__ == "__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

This example does not use any of Tornado's asynchronous features; for
that see this `simple chat room
<https://github.com/tornadoweb/tornado/tree/stable/demos/chat>`_.

Installation
------------

**Automatic installation**::

    pip install cliez

Cliez is listed in `PyPI <http://pypi.python.org/pypi/cliez/>`_ and
can be installed with ``pip`` or ``easy_install``.
it includes demo applications.


**Manual installation**: Download the latest source from `PyPI
<http://pypi.python.org/pypi/tornado/>`_.

.. parsed-literal::

    tar xvzf tornado-$VERSION.tar.gz
    cd tornado-$VERSION
    python setup.py build
    sudo python setup.py install

The Tornado source code is `hosted on GitHub
<https://github.com/tornadoweb/tornado>`_.

**Prerequisites**: Cliez test on Python 2.7.  It shoule be runs on
all Python versions.


Discussion and support
----------------------

You can discuss and report bugs on
the `GitHub issue tracker
<https://github.com/kbonez/cliez/issues>`_.


This web site and all documentation is licensed under `Creative
Commons 3.0 <http://creativecommons.org/licenses/by/3.0/>`_.

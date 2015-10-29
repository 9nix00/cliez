Cliez 中文文档
============================

*Cliez* 用于快速构建CLI程序的python框架


传送门
-----------

* `Documentation <http://cliez.readthedocs.org/>`_
* `Source (github) <https://github.com/9nix00/cliez>`_
* `Chinese Documentation <http://cliez.readthedocs.org/en/latest/i18n/zh_cn/>`_


为什么使用Cliez
------------------------------------------------------------------------------------------------

python `argparser <https://docs.python.org/3/library/argparse.html>`_ 是一个非常方便的工具.
但是在我们撰写CLI程序时,使用argparser有很明显的两个问题:

- 如果我们的程序功能非常简单,用argparser其实是比较麻烦的.比如 `ls`,在大多数情况下,我们只是需要一个帮助手册,能够解析参数,功能上足够了.

- 当我们在构造比较庞大的CLI-App程序时,argparser由于并不涉及到框架的层面,所以很多程序员特别是新手会把代码写的非常糟糕,只完成了功能,保证不了后续的可维护性.


这就是我撰写Cliez的原因,让简单的功能,用简单的方法实现.让复杂的功能,用优雅的方式实现.




Demo
------------


.. toctree::

   demo/simple.rst
   demo/complex.rst




一些使用限制
------------------------------------------------------------------------------------------------

在简单模式下,argparser的 = 号语法不支持.

.. code-block:: shell

    command --a=1

    command --a=1 --a=2




安装
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

**Prerequisites**: 目前我个人的开发环境是Python3.4,个人精力有限,毕竟是业余时间开发,并没有太多关注Python2的测试.不过理论上,应该能兼容Python2.7+版本.


Discussion and support
----------------------

You can discuss and report bugs on
the `GitHub issue tracker <https://github.com/9nix00/cliez/issues>`_.


贡献代码
-----------

目前为了提高开发速度,决定允许中文注释以及提交中文commit(真相是其实我的英文水平实在不怎么滴),但是在代码中的任何输出,必须使用英文.


Copyright
-----------

This web site and all documentation is licensed under `Creative Commons 3.0 <http://creativecommons.org/licenses/by/3.0/>`_.

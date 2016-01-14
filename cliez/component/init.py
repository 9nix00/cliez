# -*- coding: utf-8 -*-

import os
from datetime import datetime
from cliez.base.component import Component


class InitComponent(Component):
    def create_base(self, options):
        """
        通用创建部分

        创建一个安装包程序

        :param options:
        :return:
        """

        pkg_path = self.pkg_path

        os.mkdir(self.path)
        os.mkdir(pkg_path)

        open(os.path.join(pkg_path, '__init__.py'), 'w').write('''# -*- coding: utf-8 -*-

version = '0.1'
version_info = (0, 1, 0)

''')

        open(os.path.join(self.path, 'setup.py'), 'w').write('''from setuptools import find_packages, setup

import {0}

setup(
    name='{0}',
    version={0}.version,
    packages=find_packages(exclude=["tests"]),
    install_requires=['cliez'],
    url='https://github.com/<project-address>',
    license='http://opensource.org/licenses/MIT',
    download_url='https://github.com/<project-address>/archive/master.zip',
    include_package_data=True,
    author='{1}',
    author_email='{1}@nextoa.com',
    description='<description>',
    keywords='{0},',
    entry_points={{
        'console_scripts': [
            '{0} = {0}.main:main'
        ]
    }},

)

'''.format(options.name, os.getlogin()))

        open(os.path.join(self.path, 'requirements.txt'), 'w').write('''# add your package for development
cliez
''')

        open(os.path.join(self.path, 'README.rst'), 'w').write('''{}
{}

'''.format(options.name, '=' * len(options.name) * 2))

        open(os.path.join(self.path, 'LICENSE'), 'w').write('''The MIT License (MIT)

Copyright (c) {} {},Inc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

'''.format(datetime.now().year, 'NextOA'))

        pass

    def create_simple(self, options):
        pass

    def create_complex(self, options):
        """
        创建复杂模式类型应用


        :param options:
        :return:
        """

        open(os.path.join(self.pkg_path, 'main.py'), 'w').write('''# -*- coding: utf-8 -*-
import os
import argparse
from {0} import version
from cliez import conf
from cliez.base.component import Component
from cliez.parser import parse

conf.COMPONENT_ROOT = os.path.dirname(__file__)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=Component.load_description('{0}/manual/main.txt'),
        epilog='You can submit issues at: https://www.github.com/<project-address>',
    )
    parser.add_argument('--version', action='version', version='%(prog)s v{{}}'.format(version))
    parse(parser)
    pass


if __name__ == "__main__":
    main()
    pass

'''.format(options.name))

        manual_path = os.path.join(self.pkg_path, 'manual')
        os.mkdir(manual_path)

        open(os.path.join(self.pkg_path, 'main.txt'), 'w').write('''
Hello,{}

'''.format(options.name))

        component_path = os.path.join(self.pkg_path, 'component')
        os.mkdir(component_path)

        open(os.path.join(component_path, '__init__.py'), 'w').write('''# -*- coding: utf-8 -*-

''')

        pass

    def run(self, options):
        """
        创建一个CLI应用

        目前支持的应用类型有:

        * complex 模式. 此模式为默认模式,创建一个基于 argparser 的cli应用
        * simple 模式.  创建一个简单应用

        .. note::
            文件名会将大写和减号自动转换为小写和下划线

        :param argparser options:
        :return: None
        """

        options.name = options.name.lower().replace('-', '_')

        self.path = os.path.join(options.dir, options.name)
        self.pkg_path = os.path.join(self.path, options.name)

        if options.force:
            from builtins import input
            y = input("set `--force` will clean your exits files and re-create it! continue?[y/n]:")

            if y.lower() != 'y':
                self.error("user interrupt...")
            pass

        if os.path.exists(self.path):
            if options.force:
                import shutil
                shutil.rmtree(self.path)
                pass
            else:
                self.error("`{}` exists. can't init.exit...".format(options.name))
            pass

        self.create_base(options)
        self.create_complex(options)
        pass

    @classmethod
    def append_arguments(cls, sub_parsers):
        sub_parser = sub_parsers.add_parser('init', help='init project')
        sub_parser.add_argument('name', help='project name')
        # disable simple mode
        # sub_parser.add_argument('--simple', action='store_true', help='create cli-app with simple mode')
        sub_parser.add_argument('--force', action='store_true', help='force rewrite app')
        sub_parser.description = InitComponent.load_description('cliez/manual/main.txt')
        pass

    pass

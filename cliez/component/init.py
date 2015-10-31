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

version = '0.1b1'
version_info = (0, 1, -1)

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

    def create_flask(self, options):
        """
        创建flask应用

        :param options:
        :return:
        """
        open(os.path.join(self.pkg_path, 'main.py'), 'w').write('''# -*- coding: utf-8 -*-
from cliez import conf, version


try:
    app = conf.settings().app
except AttributeError:
    conf.Settings.bind('{0}.settings')
    app = conf.settings().app


@app.route('/', methods=['GET'])
def hello():
    """
    hello world demo

    :return:
    """

    return "hello,world", 200, {{"Content-Type": "text/html"}}


def run(options):
    if options.testing:
        app.config.from_object(conf.settings().TestingConfig)
    elif options.production:
        app.config.from_object(conf.settings().ProductionConfig)
    else:
        app.config.from_object(conf.settings().DevelopmentConfig)
    app.run(port=options.port)
    pass

def main():
    import os
    import argparse
    from cliez.parser import parse

    conf.COMPONENT_ROOT = os.path.dirname(__file__)

    parser = argparse.ArgumentParser(
        epilog='You can submit issues at: https://www.github.com/<project-address>',
    )
    parser.add_argument('--version', action='version', version='%(prog)s v{{}}'.format(version))
    parser.add_argument('--port', nargs='?', type=int, default=8000)
    parser.add_argument('--testing', action='store_true', help='use testing config instead development config.')
    parser.add_argument('--production', action='store_true', help='use production config instead development config.')
    parse(parser, active_one=run)
    pass

if __name__ == '__main__':
    main()


'''.format(options.name))

        open(os.path.join(self.pkg_path, 'settings.py'), 'w').write('''# -*- coding: utf-8 -*-
import sys
from flask import Flask

class Config(object):
    DEBUG=False
    TESTING=False
    pass


class DevelopmentConfig(Config):
    DEBUG=True
    pass


class TestingConfig(Config):
    TESTING=True
    pass


class ProductionConfig(Config):
    DEBUG=False
    TESTING=False
    pass


app = Flask(__name__)


'''.format(options.name))

        open(os.path.join(self.pkg_path, 'wsgi.py'), 'w').write('''# -*- coding: utf-8 -*-
from werkzeug.contrib.fixers import LighttpdCGIRootFix
from .main import app


if '--dev' in sys.argv:
    app.config.from_object('{0}.settings.DevelopmentConfig')
elif '--testing' in sys.argv:
    app.config.from_object('{0}.settings.TestingConfig')
else:
    app.config.from_object('{0}.settings.ProductionConfig')

app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
app.run()

'''.format(options.name))

        pass

    def create_blueprint(self, options):
        """
        一个blueprint本质上也是一个flask应用.
        所以我们先调用flask进行创建,然后对不一样的文件进行覆写

        :param options:
        :return:
        """

        self.create_flask(options)

        blueprint_path = os.path.join(self.pkg_path, 'blueprint')
        os.mkdir(blueprint_path)

        open(os.path.join(blueprint_path, '__init__.py'), 'w').write('''# -*- coding: utf-8 -*-

''')

        open(os.path.join(blueprint_path, 'demo.py'), 'w').write('''# -*- coding: utf-8 -*-
from flask import Blueprint

demo_api = Blueprint('demo_api', __name__)


@demo_api.route('/')
def demo():
    return "hello,world", 200, {"Content-Type": "text/html"}

''')

        open(os.path.join(self.pkg_path, 'main.py'), 'w').write('''# -*- coding: utf-8 -*-
from cliez import conf, version


try:
    app = conf.settings().app
except AttributeError:
    conf.Settings.bind('{0}.settings')
    app = conf.settings().app


from {0}.blueprint.demo import demo_api
app.register_blueprint(demo_api,url_prefix='/demo')


def run(options):
    if options.testing:
        app.config.from_object(conf.settings().TestingConfig)
    elif options.production:
        app.config.from_object(conf.settings().ProductionConfig)
    else:
        app.config.from_object(conf.settings().DevelopmentConfig)
    app.run(port=options.port)
    pass

def main():
    import os
    import argparse
    from cliez.parser import parse

    conf.COMPONENT_ROOT = os.path.dirname(__file__)

    parser = argparse.ArgumentParser(
        epilog='You can submit issues at: https://www.github.com/<project-address>',
    )
    parser.add_argument('--version', action='version', version='%(prog)s v{{}}'.format(version))
    parser.add_argument('--port', nargs='?', type=int, default=8000)
    parser.add_argument('--testing', action='store_true', help='use testing config instead development config.')
    parser.add_argument('--production', action='store_true', help='use production config instead development config.')
    parse(parser, active_one=run)
    pass

if __name__ == '__main__':
    main()


'''.format(options.name))

        pass

    def create_dispatcher(self, options):
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
        * flask 模式. 创建一个 flask应用
        * blueprint 模式. 创建一个 flask blueprint 应用
        * dispatcher 模式, 创建一个并发调度器类型的应用

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

        if options.flask:
            self.create_flask(options)
            pass

        elif options.blueprint:
            self.create_blueprint(options)
            pass

        else:
            self.create_complex(options)
            pass

        pass

    @staticmethod
    def append_arguments(sub_parsers):
        sub_parser = sub_parsers.add_parser('init', help='init project')
        sub_parser.add_argument('name', help='project name')
        sub_parser.add_argument('--simple', action='store_true', help='create cli-app with simple mode')
        sub_parser.add_argument('--flask', action='store_true', help='create a flask app')
        sub_parser.add_argument('--blueprint', action='store_true', help='create a flask blueprint app')
        sub_parser.add_argument('--dispatcher', action='store_true', help='create a dispatcher app')
        sub_parser.add_argument('--force', action='store_true', help='force rewrite app')
        sub_parser.description = InitComponent.load_description('cliez/manual/main.txt')
        pass

    pass

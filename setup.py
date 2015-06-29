from setuptools import setup, find_packages

import cliez

setup(
    name='cliez',
    version=cliez.version,
    packages=['cliez'],
    url='https://github.com/nextoa/cliez',
    download_url='https://github.com/nextoa/cliez/tarball/master',
    license='http://opensource.org/licenses/MIT',
    author='WANG WENPEI',
    author_email='wangwenpei@nextoa.com',
    description='Parser for command-line options,easier but limited than sys.argparse',
    keywords='cli'
)

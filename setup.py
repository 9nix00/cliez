from setuptools import find_packages, setup


import cliez

setup(
    name='cliez',
    version=cliez.version,
    install_requires=['termcolor', 'future'],
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/9nix00/cliez',
    download_url='https://github.com/9nix00/cliez/tarball/master',
    license='http://opensource.org/licenses/MIT',
    author='WANG WENPEI',
    author_email='wangwenpei@nextoa.com',
    description='make CLI-App easier',
    keywords='cli',
    entry_points={
        'console_scripts': [
            'cliez = cliez.main:main'
        ]
    },
)

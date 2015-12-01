from setuptools import find_packages, setup

import blueprint_demo

setup(
    name='blueprint_demo',
    version=blueprint_demo.version,
    packages=find_packages(exclude=["tests"]),
    install_requires=['cliez'],
    url='https://github.com/<project-address>',
    license='http://opensource.org/licenses/MIT',
    download_url='https://github.com/<project-address>/archive/master.zip',
    include_package_data=True,
    author='wangwenpei',
    author_email='wangwenpei@nextoa.com',
    description='<description>',
    keywords='blueprint_demo,',
    entry_points={
        'console_scripts': [
            'blueprint_demo = blueprint_demo.main:main'
        ]
    },

)


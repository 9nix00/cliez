from setuptools import find_packages, setup

import cliez

setup(
        name='{{package_name}}',
        version=cliez.version,
        install_requires=[],
        packages=find_packages(exclude=["tests"]),
        url='https://github.com/{{ URL }}',
        download_url='https://github.com/{{ URL }}/tarball/master',
        license='http://opensource.org/licenses/MIT',
        author='{{ YOUR NAME }}',
        zip_safe=False,
        author_email='{{ YOUR EMAIL }}',
        description='{{ YOUR DESCRIPTION }}',
        keywords='{{ YOUR KEYWORDS }}',
        # entry_points={
        #     'console_scripts': [
        #         'cliez = cliez.main:main'
        #     ]
        # },
)

from setuptools import find_packages, setup

import cliez

setup(
        name='cliez',
        version=cliez.version,
        install_requires=['termcolor', 'future', 'psutil'],
        packages=find_packages(exclude=["tests"]),
        url='https://github.com/wangwenpei/cliez',
        download_url='https://github.com/wangwenpei/cliez/tarball/master',
        license='MIT',
        author='WANG WENPEI',
        zip_safe=False,
        test_suite="tests",
        author_email='wangwenpei@nextoa.com',
        description='make CLI-App easier',
        keywords='cli',
        entry_points={
            'console_scripts': [
                'cliez = cliez.main:main'
            ]
        },
)

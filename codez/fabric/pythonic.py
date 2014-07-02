# -*- coding: utf-8 -*-


import os
from fabric.api import *
from classic import (base, gito)


def setup_py(code_dir=None, python='python'):
    '''
    short for cd path && python setup.py install
    :param code_dir: path
    :param python: python path,default is python
    '''
    with cd(code_dir):
        run('%s setup.py install' % python)


def uninstall_setup_py(code_dir=None,python='python'):
    '''
    @TODO uninstall package install manual
    :param code_dir:user dir
    :param python:python
    '''
    # with cd(code_dir):
    #     run('%s setup.py uninstall' % python)
    abort("please use uninstall_pip to remove package")
    pass




def supervisor():
    '''
    Install supervisor
    '''

    with settings(warn_only=True):
        run('pip install supervisor')
        if run('test -d /usr/local/etc/supervisor.d').failed:
            run('mkdir /usr/local/etc/supervisor.d')
        run(
            "grep '\[supervisord\]' /usr/local/etc/supervisord.conf || echo \"[supervisord]\nlogfile=/tmp/supervisord.log\nlogfile_maxbytes=50MB\nlogfile_backups=10\nloglevel=info\" >>  /usr/local/etc/supervisord.conf")

        run(
            "grep '\[unix_http_server\]' /usr/local/etc/supervisord.conf || echo '[unix_http_server]\nfile = /usr/local/var/run/supervisor.sock' >> /usr/local/etc/supervisord.conf")

        run(
            "grep '\[rpcinterface:supervisor\]' /usr/local/etc/supervisord.conf || echo '[rpcinterface:supervisor]\nsupervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface' >> /usr/local/etc/supervisord.conf")

        run(
            "grep '\[supervisorctl\]' /usr/local/etc/supervisord.conf || echo \"[supervisorctl]\nserverurl=unix:///usr/local/var/run/supervisor.sock\" >>  /usr/local/etc/supervisord.conf")

        run(
            "grep '\[include\]' /usr/local/etc/supervisord.conf || echo '[include]\nfiles = supervisor.d/*.ini' >> /usr/local/etc/supervisord.conf")

        run(
            "grep 'supervisord' /etc/rc.local || echo '/usr/local/bin/supervisord -c /usr/local/etc/supervisord.conf  --pidfile=/usr/local/var/run/supervisord.pid' >> /etc/rc.local")

    pass



def uninstall_supervisor():
    with settings(warn_only=True):
        run('pip uninstall supervisor -y')
        run('rm -rf /usr/local/etc/supervisor*')
    pass


def python(pip_index_url=None):
    '''
    install python. include python,setuptools,pip and supervisord
    :param pip_index_url:proxy url
    '''
    base()
    gito('/tmp/python', 'https://github.com/kbonez/python.git')
    gito('/tmp/pip', 'https://github.com/kbonez/pip.git')
    gito('/tmp/setuptools', 'https://github.com/kbonez/setuptools.git')

    with cd('/tmp/python'):
        run('./configure')
        run('make && make install')

    setup_py('/tmp/setuptools', '/usr/local/bin/python')
    setup_py('/tmp/pip', '/usr/local/bin/python')

    if pip_index_url:
        with settings(warn_only=True):
            if run('test -d ~/.pip').failed:
                run('mkdir ~/.pip')
            run(
                "grep 'index_url' ~/.pip/pip.conf || echo '[global]\nindex_url = %s' >> ~/.pip/pip.conf" % pip_index_url)

    supervisor()



def uninstall_python():
    with settings(warn_only=True):
        uninstall_pip('setuptools')
        run('rm -rf /usr/local/bin/pip*')
        run('rm -rf /usr/local/bin/python*')
        run('rm -rf /usr/local/*/python*')
        run('rm -rf /usr/local/etc/supervisor*')
        run('rm -rf /tmp/python')
        run('rm -rf /tmp/pip')
        run('rm -rf /tmp/setuptools')
    pass



def pip(package=None, upgrade=None):
    '''
    install package use pip
    :param package: package name
    :param upgrade: true
    '''
    if package:
        run('pip install %s' % package)
        if upgrade:
            run('pip install %s --upgrade' % package)


def uninstall_pip(package):
    '''
    uninstall package from pip
    :param package:
    :return:
    '''
    with settings(warn_only=True):
        run('pip uninstall %s -y' % package)



def tornado(ez=None):
    '''
    install tornado
    :param ez:
    :return:
    '''
    if ez:
        pip('tornadoez', True)
    else:
        pip('tornado', True)


def putc_supervisor(path):
    '''
    put supervisor config file
    :param path: local path
    '''
    remote_path = '/usr/local/etc/supervisor.d/'
    put(path, remote_path)

    pass
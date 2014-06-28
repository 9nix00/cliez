# -*- coding: utf-8 -*-


from classic import git


def supervisor():

    pass


def pip():

    pass


def setup_py(code_dir=None):
    with cd(code_dir):
        run('python setup.py install')




def python():
    git()
    with cd('/tmp'):
        run('git clone https://github.com/kbonez/python.git')


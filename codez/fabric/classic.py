# -*- coding: utf-8 -*-


def web():
    run('mkdir /webdata')
    pass

def storage():
    run('mkdir /storage')
    pass


def nginx():
    web()
    run('yum install nginx -y')
    pass

def redis():
    storage()
    run('yum install redis -y')
    pass


def repo():
    run('mkdir /repo')
    run('yum install gitolite -y')
    pass


def git():
    run('yum install git -y')
    pass


def base():
    run('yum install g++ make -y')
    pass



def clone(parent=None,url=None):
    with cd(parent):
        run('git clone '+url)




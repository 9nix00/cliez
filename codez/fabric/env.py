# -*- coding: utf-8 -*-

import os

# def pssh(file):
#
#     if file[0] == '~':
#         file = os.path.realpath(os.getenv('HOME'))+file[1:]
#
#
#
#     with open(file,'r') as fp:
#         buffer = fp.read()
#
#     host_list=buffer.strip("\n").split("\n")
#
#     user = None
#     machines=[]
#
#     for addr in host_list:
#         pos = addr.strip().find('@')
#         if pos > 0:
#             user = addr[0:pos]
#             machines.append(addr[pos+1:])
#
#     return user,machines



def pssh(file):
    if file[0:2] == '~/':
        file = os.path.realpath(os.getenv('HOME'))+file[1:]

    with open(file,'r') as fp:
        buffer = fp.read()

    host_list=buffer.strip("\n").split("\n")
    machines=[]
    for addr in host_list[:]:
        addr.strip()
        if addr.find('#') == -1:
            machines.append(addr)

    return machines
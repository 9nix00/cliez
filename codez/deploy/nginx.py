# -*- coding: utf-8 -*-


import codez.deploy.base.base as General
import sys


class Deploy(General.Deploy):
    def __init__(self, config,general, **kwargs):
        super(Deploy, self).__init__()
        self.quiet = kwargs.get('--quiet', False)
        self.config = config

        self.general = general

        # prepare env
        # if self.platform == self.platforms.centos:
        #     self.root = '/etc/nginx'
        #     self.conf_d = '/etc/nginx/conf.d'
        #     pass

        # 基础流程
        # 检测是否安装了nginx，没有安装
        # 匹配user，如果不符合，覆盖
        # 匹配upstream,复写
        self.general.host_group()

        # 生成供pssh调用的server list








    def upstream(self):

        if self.quiet:
            print "prepear"
            pass
        else:
            pass

        'sed xxxxxx'
        pass



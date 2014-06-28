# -*- coding: utf-8 -*-


from codez.deploy.base.config import dict2obj


class Platform(object):
    centos = 1
    macosx = 2
    ubuntu = 3


class Deploy(object):
    def __init__(self):
        # self.platforms = Platform()
        # self.platform = self.check_platform()
        # self.version = self.check_version()
        pass


    def check_platform(self):
        # return self.platform.centos
        pass

    def check_version(self):
        return dict2obj({
            'major': 6,
            'minor': 4,
            'patch': 1,
            'fix': 'r1'
        })
        pass

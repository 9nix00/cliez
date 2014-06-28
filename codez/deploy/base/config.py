# -*- coding: utf-8 -*-

from collections import namedtuple


# not my wish
# Template = namedtuple('Struct',_Template.keys())(*_Template.values())
# print Template.Nginx['upstream']


# for python
class dict2obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [dict2obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, dict2obj(b) if isinstance(b, dict) else b)




_Template = {
    'Nginx': {
        'upstream': 0,
        'php': 1,
    }
}

Template = dict2obj(_Template)


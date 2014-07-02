# -*- coding: utf-8 -*-

from collections import namedtuple


# not my wish
# Template = namedtuple('Struct',_Template.keys())(*_Template.values())
# print Template.Nginx['upstream']






_Template = {
    'Nginx': {
        'upstream': 0,
        'php': 1,
    }
}

Template = dict2obj(_Template)


# -*- coding: utf-8 -*-


import mongoengine
mongoengine.connect('test', host='mongodb://127.0.0.1')


SECRET_KEY = 'hello world'
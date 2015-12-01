# -*- coding: utf-8 -*-
import sys
from flask import Flask
import mongoengine


class Config(object):
    DEBUG = False
    TESTING = False
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = mongoengine.connect('test', host='mongodb://127.0.0.1')
    pass


class TestingConfig(Config):
    TESTING = True
    pass


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    pass


app = Flask(__name__)

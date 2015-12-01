# -*- coding: utf-8 -*-
import sys
import peewee
from flask import Flask


class Config(object):
    DEBUG = False
    TESTING = False
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = peewee.MySQLDatabase('test', host='127.0.0.1', user='root', passwd='')
    pass


class TestingConfig(Config):
    TESTING = True
    pass


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    pass


app = Flask(__name__)

# -*- coding: utf-8 -*-
import sys
from flask import Flask

class Config(object):
    DEBUG=False
    TESTING=False
    pass


class DevelopmentConfig(Config):
    DEBUG=True
    pass


class TestingConfig(Config):
    TESTING=True
    pass


class ProductionConfig(Config):
    DEBUG=False
    TESTING=False
    pass


app = Flask(__name__)



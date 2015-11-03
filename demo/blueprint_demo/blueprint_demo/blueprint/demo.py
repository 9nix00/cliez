# -*- coding: utf-8 -*-
from flask import Blueprint

demo_api = Blueprint('demo_api', __name__)


@demo_api.route('/')
def demo():
    return "hello,world", 200, {"Content-Type": "text/html"}


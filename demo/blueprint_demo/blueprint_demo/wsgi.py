# -*- coding: utf-8 -*-
from werkzeug.contrib.fixers import LighttpdCGIRootFix
from .main import app


if '--dev' in sys.argv:
    app.config.from_object('blueprint_demo.settings.DevelopmentConfig')
elif '--testing' in sys.argv:
    app.config.from_object('blueprint_demo.settings.TestingConfig')
else:
    app.config.from_object('blueprint_demo.settings.ProductionConfig')

app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
app.run()


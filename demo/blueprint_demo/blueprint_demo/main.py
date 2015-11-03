# -*- coding: utf-8 -*-
from cliez import conf, version


try:
    app = conf.settings().app
except AttributeError:
    conf.Settings.bind('blueprint_demo.settings' , __file__)
    app = conf.settings().app


from blueprint_demo.blueprint.demo import demo_api
app.register_blueprint(demo_api,url_prefix='/demo')


def run(options):
    if options.testing:
        app.config.from_object(conf.settings().TestingConfig)
    elif options.production:
        app.config.from_object(conf.settings().ProductionConfig)
    else:
        app.config.from_object(conf.settings().DevelopmentConfig)
    app.run(port=options.port)
    pass

def main():
    import os
    import argparse
    from cliez.parser import parse

    conf.COMPONENT_ROOT = os.path.dirname(__file__)

    parser = argparse.ArgumentParser(
        epilog='You can submit issues at: https://www.github.com/<project-address>',
    )
    parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(version))
    parser.add_argument('--port', nargs='?', type=int, default=8000)
    parser.add_argument('--testing', action='store_true', help='use testing config instead development config.')
    parser.add_argument('--production', action='store_true', help='use production config instead development config.')
    parse(parser, active_one=run)
    pass

if __name__ == '__main__':
    main()



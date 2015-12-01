# -*- coding: utf-8 -*-

import os
from datetime import datetime
from cliez.base.component import Component


class PatchComponent(Component):

    def run(self, options):
        """



        """

        options.name = options.name.lower().replace('-', '_')

        self.path = os.path.join(options.dir, options.name)
        self.pkg_path = os.path.join(self.path, options.name)

        if options.force:
            from builtins import input
            y = input("set `--force` will clean your exits files and re-create it! continue?[y/n]:")

            if y.lower() != 'y':
                self.error("user interrupt...")
            pass

        if os.path.exists(self.path):
            if options.force:
                import shutil
                shutil.rmtree(self.path)
                pass
            else:
                self.error("`{}` exists. can't init.exit...".format(options.name))
            pass

        self.create_base(options)

        if options.flask:
            self.create_flask(options)
            pass

        elif options.blueprint:
            self.create_blueprint(options)
            pass

        else:
            self.create_complex(options)
            pass

        pass

    @staticmethod
    def append_arguments(sub_parsers):
        sub_parser = sub_parsers.add_parser('init', help='init project')
        sub_parser.add_argument('name', help='project name')
        sub_parser.add_argument('--simple', action='store_true', help='create cli-app with simple mode')
        sub_parser.add_argument('--flask', action='store_true', help='create a flask app')
        sub_parser.add_argument('--blueprint', action='store_true', help='create a flask blueprint app')
        sub_parser.add_argument('--dispatcher', action='store_true', help='create a dispatcher app')
        sub_parser.add_argument('--force', action='store_true', help='force rewrite app')
        sub_parser.description = InitComponent.load_description('cliez/manual/main.txt')
        pass

    pass

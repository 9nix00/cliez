# -*- coding: utf-8 -*-

import os
import sys
from cliez.component import Component

try:
    input = raw_input
except NameError:
    pass

try:
    import ConfigParser

    Parser = ConfigParser.ConfigParser
except (NameError, ImportError):
    import configparser

    Parser = configparser.ConfigParser


class InitComponent(Component):
    def load_gitconfig(self):
        gitconfig_path = os.path.expanduser('~/.gitconfig')

        if os.path.exists(gitconfig_path):
            parser = Parser()
            parser.read(gitconfig_path)
            parser.sections()
            return parser

        pass

    def render(self, match_string, new_string):
        print("replace {} to {}".format(match_string, new_string))




        pass

    def render_email(self):

        parser = self.load_gitconfig()

        try:
            default_email = parser['user']['email']
        except AttributeError:
            default_email = ''

        while True:
            if default_email:
                t = input("email [%s]:" % default_email, default_email)
            else:
                t = input("email:")

            t = default_email if not t.strip() else t

            if t:
                self.render('___email___', t)
                break
            pass

        pass

    def render_author(self):

        parser = self.load_gitconfig()

        try:
            default_user = parser['github']['user']
        except AttributeError:
            default_user = ''

        while True:
            if default_user:
                t = input("author [%s]:" % default_user, default_user)
            else:
                t = input("author:")

            t = default_user if not t.strip() else t

            if t:
                self.render('___author___', t)
                break

            break

        pass

    def render_pkg(self):
        while True:
            pkg = input("package name:")
            if pkg:
                self.render('___pkg___', pkg)
                break
            pass
        pass

    def render_confirm(self):

        self.warn_message("this tool will delete your repo")

        while True:
            k = input("continue?[yes/no]:")
            if k == 'yes':
                break
            elif k == 'no':
                break
            else:
                self.warn_message("please input `yes` or `no`")
            pass

        pass

    def run(self, options):
        system_call = os.system

        if options.debug:
            system_call = lambda x: print(x) or 0

        if not options.yes:
            self.render_confirm()

        self.render_pkg()
        self.render_author()
        self.render_email()
        pass

    @classmethod
    def add_arguments(cls):
        """
        Init project.
        """
        return [
            (('--yes',), dict(action='store_true', help='clean .git repo'))
        ]

    pass

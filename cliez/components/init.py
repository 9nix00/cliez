# -*- coding: utf-8 -*-

import os
import random
import shutil
import string
import sys
from datetime import datetime, timedelta

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
    exclude_directories = ['.git', '.hg', '__pycache__', '.idea']

    def load_gitconfig(self):
        gitconfig_path = os.path.expanduser('~/.gitconfig')

        if os.path.exists(gitconfig_path):
            parser = Parser()
            parser.read(gitconfig_path)
            parser.sections()
            return parser

        pass

    def render(self, match_string, new_string):

        current_dir = self.options.dir

        if os.path.expanduser(current_dir) in ['/', os.path.expanduser("~")]:
            self.error_message("invalid directory")
            sys.exit(-1)
            pass

        # .git or .hg may not exist before init execute.
        # if not os.path.exists('.git') and not os.path.exists('.hg'):
        #     self.error_message("invalid directory")
        #     sys.exit(-1)
        #     pass

        def match_directory(path):
            skip = False
            for include_dir in ['/{}/'.format(s) for s in
                                self.exclude_directories]:
                if path.find(include_dir) > -1:
                    skip = True
                    break
                pass
            return skip

        # handle files
        for v in os.walk(current_dir):
            # skip exclude directories
            if os.path.basename(v[0]) in self.exclude_directories:
                continue
            if match_directory(v[0]):
                continue

            for base_name in v[2]:
                file_name = os.path.join(v[0], base_name)

                buffer = ''
                # ignore binary files
                try:
                    with open(file_name, 'r') as fh:
                        buffer = fh.read()
                        buffer = buffer.replace(match_string, new_string)
                        pass

                    with open(file_name, 'w') as fh:
                        fh.write(buffer)
                        pass
                except UnicodeDecodeError:
                    continue

                pass
            pass

        # handle directory
        redo_directories = []
        redo_files = []

        for v in os.walk(current_dir):
            if os.path.basename(v[0]) in self.exclude_directories:
                continue
            if match_directory(v[0]):
                continue

            for sub_dir in v[1]:
                if match_string in sub_dir:
                    redo_directories.append(os.path.join(v[0], sub_dir))
                    pass

            for f in v[2]:
                if match_string in f:
                    redo_files.append(os.path.join(v[0], f))
                    pass
            pass

        redo_directories.reverse()
        redo_files.reverse()

        # redo files first
        for v in redo_files:
            dir_name = os.path.dirname(v)
            file_name = os.path.basename(v)
            shutil.move(v, os.path.join(
                dir_name,
                file_name.replace(match_string, new_string)))
            pass

        for v in redo_directories:
            shutil.move(v, v.replace(match_string, new_string))
            pass

        pass

    def render_email(self):

        parser = self.load_gitconfig()

        try:
            default_email = parser['user']['email']
        except (AttributeError, KeyError):
            default_email = 'mail@example.com'

        while True:
            if default_email:
                t = input("email [%s]:" % default_email)
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
        except (AttributeError, KeyError):
            default_user = 'username'

        while True:
            if default_user:
                t = input("author [%s]:" % default_user)
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
                self.render('___Pkg___', pkg[0].upper() + pkg[1:].lower())
                self.render('___PKG___', pkg.upper())
                break
            pass
        pass

    def render_random(self):
        self.render('___random___', ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(64)))
        pass

    def render_release_datetime(self):
        self.render('___release-datetime___',
                    (datetime.now() + timedelta(days=30)).strftime(
                        '%Y-%m-%dT%H:%M:%s'))
        pass

    def render_confirm(self):

        self.warn_message("this tool may destroy current code")

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

        self.render_random()
        self.render_pkg()
        self.render_release_datetime()

        if not options.skip_builtin:
            self.render_author()
            self.render_email()
            pass

        options.variable = options.variable or []

        if options.debug:
            print(options.variable)

        self.logger.debug("user variable list:%s", options.variable)

        for v in options.variable:
            try:
                key, value = v.split(':')
            except ValueError:
                continue
            self.render('___{}___'.format(key), value)
            pass

        pass

    @classmethod
    def add_arguments(cls):
        """
        Init project.
        """
        return [
            (('--yes',), dict(action='store_true', help='clean .git repo')),
            (('--variable', '-s'),
             dict(nargs='+', help='set extra variable,format is name:value')),
            (('--skip-builtin',),
             dict(action='store_true', help='skip replace builtin variable')),
        ]

    pass

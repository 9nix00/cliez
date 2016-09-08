# -*- coding: utf-8 -*-

import os
import logging

from cliez.component import Component


class CreateComponent(Component):
    def run(self, options):

        system_call = self.system

        orders = ['github', 'bitbucket']

        if options.bitbucket:
            orders.remove('bitbucket')
            orders.insert(0, 'bitbucket')

        if options.local:
            orders.insert(0, 'localhost')

        project_root = os.path.join(options.dir, options.name) if options.name else options.dir

        if options.debug:
            self.print_message("project will clone to %s" % project_root)

        repo_path = os.path.expanduser(options.repo)
        rtn = -1

        for v in orders:
            if v == 'localhost':
                if os.path.exists(repo_path):
                    self.logger.debug('try clone from %s' % repo_path)

                    if os.path.exists(os.path.join(repo_path, '.git')):
                        rtn = system_call('git clone {} {}'.format(repo_path, project_root))

                        if rtn == 0:
                            break
                        pass
                    elif os.path.exists(os.path.join(repo_path, '.hg')):
                        rtn = system_call('hg clone {} {}'.format(repo_path, project_root))

                        if rtn == 0:
                            break
                        pass

            elif v == 'github':

                cmd_path = 'git clone ssh:git@github.com:{}.git {}'.format(repo_path, project_root)
                self.logger.debug('try clone from %s' % cmd_path)
                rtn = system_call(cmd_path)

                if rtn == 0:
                    break

                cmd_path = 'git clone https://github.com/{}.git {}'.format(repo_path, project_root)
                self.logger.debug('try clone from %s' % cmd_path)
                rtn = system_call(cmd_path)

                if rtn == 0:
                    break

                pass

            elif v == 'bitbucket':
                cmd_path = 'hg clone ssh://hg@bitbucket.org/{} {}'.format(repo_path, project_root)
                self.logger.debug('try clone from %s' % cmd_path)
                rtn = system_call(cmd_path)
                if rtn == 0:
                    break

                pass
            pass

        if rtn != 0:
            self.print_message("")
            self.error("can't find repo %s" % options.repo)

        pass

    @classmethod
    def add_arguments(cls):
        """
        Create project.
        By default cliez find github first, if not found, then try to search bitbucket


        if user define `--local` option. search local path first.

        if user define `--bitbucket`, search bitbucket first,then search github.


        * note *
        * currently,we only support ssh mode when use bitbucket *

        """
        return [
            (('repo',), dict(help='repo path.')),
            (('name',), dict(nargs='?', default='', help='project name.')),
            (('--local',), dict(action='store_true', help='try load repo local path.')),
            (('--bitbucket',), dict(action='store_true', help='search bitbucket first.')),
        ]

        pass

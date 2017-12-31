"""
====================
Check Component
====================

Currently, check component only check if user install `git`.

You can append '--debug' or '-vvv' to see how `Cliez` work.

"""

import shutil

import termcolor

from cliez.component import Component


class CheckComponent(Component):
    exclude_global_option = True  #: ignore global option

    def run(self, options):
        """
        .. todo::

            check network connection

        :param Namespace options: parse result from argparse
        :return:
        """
        self.logger.debug("debug enabled...")

        depends = ['git']
        nil_tools = []

        self.logger.info("depends list: %s", depends)

        for v in depends:
            real_path = shutil.which(v)
            if real_path:
                self.print_message("Found {}:{}..."
                                   "    {}".format(v,
                                                   real_path,
                                                   termcolor.colored(
                                                       '[OK]',
                                                       color='blue')))
            else:
                nil_tools.append(v)
                self.error_message(
                    'Missing tool:`{}`...    {}'.format(v, '[ERR]'), prefix='',
                    suffix='')

            pass

        if nil_tools:
            self.print_message('')
            self.error("please install missing tools...")
        else:
            self.print_message("\nNo error found,"
                               "you can use cliez in right way.")
            self.logger.debug("check finished...")
            pass

        pass

    @classmethod
    def add_arguments(cls):
        """
        check cliez depends envrioument.
        """
        return [
            (('--debug',), dict(action='store_true', help='open debug mode')),
            (('--verbose', '-v'), dict(action='count')),
        ]

    pass

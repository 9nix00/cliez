# -*- coding: utf-8 -*-

import shutil
import termcolor

from cliez.component import Component


class CheckComponent(Component):

    exclude_global_option = True

    def run(self, options):
        """
        ..todo:
            check network connection

        :param options:
        :return:
        """

        depends = ['git']
        nil_tools = []

        for v in depends:
            real_path = shutil.which(v)
            if real_path:
                self.print_message("found {}:{}...    {}".format(v, real_path, termcolor.colored('[OK]', color='blue')))
            else:
                nil_tools.append(v)
                self.error_message('missing tool:`{}`...    {}'.format(v, '[ERR]'), prefix='', suffix='')

            pass

        if nil_tools:
            self.print_message("")
            self.error('please install missing tools...')
        else:
            self.print_message("\nNo issues,you cloud use cliez in right way.")
            pass

        pass

    @classmethod
    def add_arguments(cls):
        """
        check cliez depends envrioument
        """

        pass

    pass

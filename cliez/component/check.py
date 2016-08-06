# -*- coding: utf-8 -*-

import shutil
import termcolor

from cliez.base.component import Component


class CheckComponent(Component):
    def run(self, options):
        """
        检查依赖环境

        ..todo:
            对网络环境进行检查,如果是离线,则给出警告

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
    def add_arguments(cls, parser):
        """
        check cliez depends envrioument
        """

        pass

    pass
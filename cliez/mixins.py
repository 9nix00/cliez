"""
=============
Mixins
=============
"""

import shutil

import termcolor


class CheckCommandMixin(object):
    check_cmd_list = []

    def run(self, options):
        self.logger.info("check command list: %s", self.check_cmd_list)
        nil_tools = []

        for v in self.check_cmd_list:
            real_path = shutil.which(v)
            if real_path:
                self.print_message("Found %(name)s:%(path)s..."
                                   "    %(status)s" % {
                                       'name': v,
                                       'path': real_path,
                                       'status': termcolor.colored(
                                           '[OK]', color='blue')
                                   })
            else:
                nil_tools.append(v)
                self.error_message(
                    "Missing tool:`%(name)s`...    %(status)s" % {
                        'name': v,
                        'status': '[ERR]'
                    },
                    prefix='',
                    suffix='')

        if nil_tools:
            self.error("please install missing depends.")
        pass

    pass

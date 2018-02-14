"""
=============
Mixins
=============
"""

import shutil

import termcolor


class CheckCommandMixin(object):
    """
    create check component easier.
    """
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


class RequireConfigMixin(object):
    """
    check key value for user input and
    config file
    """

    def parse_require(self, env, keys, defaults={}):
        """
        check and get require config
        :param dict env: user config node
        :param list keys: check keys
            .. note::

                option and key name must be same.

        :param dict defaults: default value for keys
        :return: dict.env with verified.


        .. exception::

            will raise `ValueError` when some key missed.

        """

        for k in keys:
            env[k] = getattr(self.options, k) or env.get(k, None)

            if env[k] is None:
                self.error("config syntax error,"
                           "please set `%s` in your env: %s" % (k, env))

            pass

        for k, v in defaults.items():
            env.setdefault(k, v)

        return env

    pass

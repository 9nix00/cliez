# -*- coding: utf-8 -*-
import sys
import os


class Error(object):
    required = 1


class ArgLoader(object):
    def __init__(self, options=tuple(), sys_argv=None):
        """Parse arguments from options argument.

        :param options: user defined options.something like this

        .. code-block:: python

            options = (
                "Useage  COMMAND [options]  arguments",
                "",
                "document line1",
                "document line2",
                "",  # blank line
                "Options:",
                ("--opt1", "comment for opt", '-a'),
                ("--opt2:", "comment for opt", '-b'),
                "Actions",
                ("@hello", "call hello"),
                "",
                ("--help", "print help document", '-h'),
                ("--debug", "debug mode"),
            )


        .. note::
           `ArgLoader` will save value into: `self.actions`,`self.options` and `self.argv`.
           the value of self.argv and self.options with arguments will be treat as `str`


        :param sys_argv: argv input,use :py:obj:`sys.argv` if not set
        :type sys_argv: `list`
        """

        self.parse_args(options)
        sys_argv = sys_argv if sys_argv is not None else sys.argv

        self.argv = sys_argv[:]

        for k, v in enumerate(sys_argv):

            if k == 0:
                commander = os.path.basename(v).lower()
                if '.py' in commander:
                    commander = commander[:commander.find('.py')]
                self.commander = commander[0].upper() + commander[1:]
                continue
            else:
                if v[0:2] == '--':
                    self.set_option(k, v, sys_argv)
                elif v[0:1] == '-':
                    i = 1
                    try:
                        while i < len(v):
                            if i == len(v) - 1:
                                self.set_option(k, '-' + v[i], sys_argv)
                            else:
                                self.set_option(k, '-' + v[i], sys_argv, delete=False)
                            i += 1
                    except:
                        # argument `-' will ignore
                        pass

                else:
                    self.set_action(k, v)

        if sys.version_info[0] == 2:
            self.argv = filter(lambda x: x is not False, self.argv)
        else:
            self.argv = list(filter(lambda x: x is not False, self.argv))

    def error(self, a, value):
        if value == Error.required:
            print("Error:`", a, "' Require value")
            os._exit(1)

    def set_option(self, k, _opt, sys_argv, delete=True):
        # process alias  first
        _refer = _opt

        if _opt in self.alias:
            _opt = self.alias[_opt]

        if _opt in self.options:
            # if option is already set. skip? this complex. so it will be error
            if self.required[_opt]:  # and self.options[_opt] is None:
                try:
                    next = sys_argv[k + 1]

                    if next[0] == '-':
                        self.error(_refer, Error.required)
                    else:
                        self.options[_opt] = next
                        if delete:
                            self.argv[k] = False
                            self.argv[k + 1] = False

                except:
                    self.error(_refer, Error.required)

            else:
                # no argument option
                self.options[_opt] = True
                if delete:
                    self.argv[k] = False

    def set_action(self, k, _opt):
        if _opt in self.alias:
            _opt = self.alias[_opt]

        if _opt in self.actions:
            self.actions[_opt] = True
            self.argv[k] = False

    def __repr__(self):
        return "Action List:\n {}\nOptions List:\n {}\nArguemnts List:\n {}\nAlias List:\n {}\nRequired List:\n {}\n".format(
            self.actions, \
            self.options, \
            self.argv, \
            self.alias, \
            self.required)

    def __str__(self):
        return "\n" + self.__doc__

    def parse_args(self, options):
        # parse argument and document
        self.options = {}
        self.alias = {}
        self.actions = {}
        self.required = {}
        docs = ''
        _max_space_size = 4
        _space = " __EZC_TAKEN_SPACE__ "

        for k, v in enumerate(options):
            if (type(v).__name__ == 'str'):
                # origin document
                docs += v + "\n"
            elif (type(v).__name__ == 'tuple'):

                _doc = ''
                _opt = None
                _actions = None
                _alias = []
                _required = True if v[0][-1] == ':' else False

                if v[0][0] == '-':
                    _opt = v[0][:-1] if _required else v[0]
                else:
                    _required = False
                    _actions = v[0][1:]

                # vv: --option1[:],document,--alias1,--alias2...

                for kk, vv in enumerate(v):
                    if kk == 0:
                        continue
                    if kk == 1:
                        _doc = vv + "\n"
                    else:
                        _alias.append(vv)

                _alias_str = ','.join(_alias)

                _required_msg = " <arg>" if _required else ""
                _msg = _actions if _actions else _opt
                if _alias_str:
                    _msg += "," + _alias_str + _required_msg
                else:
                    _msg += _required_msg

                _max_space_size = len(_msg) if len(_msg) > _max_space_size else _max_space_size

                docs += " " * 4 + _msg + _space + _doc

                # push message
                if _opt:
                    self.options[_opt] = None
                    self.required[_opt] = _required

                if _actions:
                    self.actions[_actions] = None
                    self.required[_actions] = _required

                if not _alias:
                    pass
                else:
                    for alias in _alias:
                        if _actions:
                            self.alias[alias] = _actions
                        else:
                            self.alias[alias] = _opt

            else:
                # type is not str and tuple
                pass

        pass

        # for beautiful helper
        self.__doc__ = ''
        _origin_docs = docs.split("\n")

        for line in _origin_docs:
            pos = line.find(_space)
            if pos > 0:
                space_pos = 12 if _max_space_size > 10 else 8
                self.__doc__ += line.replace(_space, " " * (_max_space_size - pos + space_pos))
            else:
                self.__doc__ += line

            self.__doc__ += "\n"

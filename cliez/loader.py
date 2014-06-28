#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys, os


class Error(object):
    required = 1


class ArgLoader(object):
    def __init__(self, options=tuple(), docs=NotImplemented):
        self.parseArgs(options)
        self.argv = sys.argv[:]

        for k, v in enumerate(sys.argv):

            if k == 0:
                commander = os.path.basename(v).lower()
                if '.py' in commander:
                    commander = commander[:commander.find('.py')]
                self.commander = commander[0].upper() + commander[1:]
                continue
            else:
                if v[0:2] == '--':
                    self.setOpt(k, v)
                elif v[0:1] == '-':
                    i = 1
                    try:
                        while i < len(v):
                            if i == len(v) - 1:
                                self.setOpt(k, '-' + v[i])
                            else:
                                self.setOpt(k, '-' + v[i], delete=False)
                            i += 1
                    except:
                        # argument `-' will ignore
                        pass

                else:
                    self.setAction(k, v)

        self.argv = filter(lambda x: x is not False, self.argv)


    def error(self, a, value):
        if value == Error.required:
            print "Error:`", a, "' Require value"
            os._exit(1)

    def setOpt(self, k, _opt, delete=True):
        # process alias  first
        _refer = _opt
        if _opt in self.alias:
            _opt = self.alias[_opt]

        if _opt in self.options:
            # if option is already set. skip? this complex. so it will be error
            if self.required[_opt]:  #and self.options[_opt] is None:
                try:
                    next = sys.argv[k + 1]

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
                #no argument option
                self.options[_opt] = True
                if delete:
                    self.argv[k] = False


    def setAction(self, k, _opt):
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
        return "\n"+self.__doc__


    def parseArgs(self, options):
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

                _required_msg = " *" if _required else ""
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



        #for beautiful helper
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


if __name__ == "__main__":
    options = (
        "Useage: cliez.ArgLoader Example",
        "",
        "Options",
        ('--help', 'print help document.', '-h'),
        "",
        "HOW-TO:",
        "    Format:",
        "        options = (argument-list)",
        "        argument-list = ('-option[:]|@action','docs','alias1','alias2','alias...')",
        "",
        "    Options-Demo:",
        "        options = (",
        "           ('--help', 'print help document', '-h')",
        "           ('@checkout', 'checkout repo', 'co')",
        "        )",
        "        a = ArgLoader(options=options)"
        "        if a.options['--help']:"
        "           print a"
    )

    a = ArgLoader(options=options)

    print "****This is used for document****"
    print a
    #
    print "****This is used for debug****"
    print repr(a)
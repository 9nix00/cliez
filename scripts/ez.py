# -*- coding: utf-8 -*-

import os, sys
from ConfigParser import SafeConfigParser
from cliez.loader import ArgLoader
import importlib


options = (
    'Useage: ez deploy tools  ez { deploy | upgrade } [options] config-path | branch-name',
    '',
    ('@deploy', 'options,initial server'),
    ('@upgrade', 'upgrade program by git'),
    ('@doc', '@todo generate code docs,use for team develop'),
    ('@upload', '@todo monitor directory and upload when files changed,use for development'),


    ('--root', 'pssh host group path,default is $HOME/.dsh/group/', '-h'),
    ('--deploy-package', 'user defined package'),
    ('--help', 'print help document'),
    '',
    ('--debug', 'set debug mode'),
    ('--debug1', 'set debug mode 1'),
    ('--debug2', 'set debug mode 2'),
    ('--debug3', 'set debug mode 3'),
    ('--debug4', 'set debug mode 4')
)

a = ArgLoader(options=options)
_debug = a.options['--debug']

if a.options['--help']:
    print a
    sys.exit(0)

try:
    config_file = os.path.realpath(a.argv[1])
    try:
        os.access(config_file, os.R_OK)
    except:
        print "can't read file", config_file, ",please check it."
        sys.exit(1)
except:
    print "please set your config file."
    sys.exit(1)

if a.actions['deploy']:

    deploy_package = a.options['--deploy-package'] if a.options['--deploy-package'] else 'codez.deploy'

    execfile(config_file)

    from codez.deploy.general import General
    general =  General(config)


    for active_service in config['service']:
        try:
            module_path = deploy_package + '.' + active_service
            current_module = importlib.import_module(module_path)
            current_module.Deploy(config[active_service],general)
        except Exception as e:
            if _debug:
                print "Unexpected error:", sys.exc_info()[0]
                raise
            else:
                print "unrecognized service:'{}',from package {},ignore.".format(active_service, deploy_package)

    pass
elif a.actions['upgrade']:
    print "等价我们常用的git 。。。。的工具，只是更简单"
    pass
elif a.actions['doc']:
    print "sphinx的简洁版本＋生成tag文件"
    pass
elif a.actions['upload']:

    pass

else:
    print a

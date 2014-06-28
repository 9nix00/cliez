# -*- coding: utf-8 -*-


class General(object):
    def __init__(self, config, **kwargs):
        self.config = config
        pass

    def host_group(self):
        group = self.config.get('machines', False)

        print self.config

        if type(group) == list:
            # 创建tmp文件
            import tempfile

            host_file = tempfile.TemporaryFile()
            buffer = "\n".join(group)

            host_file.write(buffer)

            # bu = open(host_file, 'r').read(len(buffer) + 1)
            # print bu
            print host_file.name


        elif type(group) == str:
            host_file = os.path.realpath(group)
        else:
            print "unsupport group type.current is ", type(group)
            sys.exit(-1)


    # 检测
    def check_env(self):
        pass

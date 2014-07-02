# -*- coding: utf-8 -*-

from fabric.api import *
import os



def airlog(size=8):
    """
    Fast Log file storage, use memory disk
    :return:
    """
    match = "tmpfs    /airlog"
    replace = "%s    tmpfs    uid=root,gid=root,size=%sG,mode=777  0 0" % (match, size)

    with settings(warn_only=True):
        run('mkdir /airlog')
        run('grep "%s" /etc/fstab && sed -i -e "s/%s.*//g" /etc/fstab' % (match, '\/'.join(match.split('/'))))
    run('grep "%s" /etc/fstab || echo "%s" >> /etc/fstab ' % (match, replace))

    with settings(warn_only=True):
        if run('df -h | grep /airlog').failed:
            run('mount /airlog')

    pass


def uninstall_airlog():
    """
    Uninstall Fast Log file disk
    :return:
    """
    with settings(warn_only=True):
        if run('df -h | grep /airlog'):
            run('umount /airlog')

    match = "tmpfs    /airlog"
    with settings(warn_only=True):
        run('grep "%s" /etc/fstab && sed -i -e "s/%s.*//g" /etc/fstab' % (match, '\/'.join(match.split('/'))))

    pass


def nginx(size=8, user='webuser', worker_processes=10240, worker_connections=65535):
    # if run("test -d %s" % '/etc/nginx').failed:
    #     run('mkdir /etc/nginx')

    run('yum install nginx -y')
    with settings(warn_only=True):
        if run("test -d %s" % '/webdata').failed:
            run('mkdir /webdata')

    # airlog('nginx')
    # mount -o size=32G -t tmpfs none /data


    # 新增用户，如果不存在的话
    with settings(warn_only=True):
        if run('cat /etc/passwd | grep ^%s' % user).failed:
            run('useradd -r %s -d /home/webuser -s `which bash` ' % user)
            run('mkdir /home/webuser && chown webuser.webuser /home/webuser')



    # 添加一块内存盘
    # 考虑到内存大小会重设的可能，我们第一次需要清空，第二次再添加
    # 如果是线上扩容，很麻烦，需要先unmout,umount带来的问题就是线上服务器会出现downtime。
    # 否则造成downtime的一律重启
    # 所以这种场景我们还是不考虑的比较，我们就强制定义一开始需要用户指定好一个合理的大小，基本上8G是很够用的

    match = "tmpfs    /webdata"
    replace = "%s    tmpfs    uid=%s,gid=%s,size=%sG,mode=700  0 0" % (match, user, user, size)

    with settings(warn_only=True):
        run('grep "%s" /etc/fstab && sed -i -e "s/%s.*//g" /etc/fstab' % (match, '\/'.join(match.split('/'))))
    run('grep "%s" /etc/fstab || echo "%s" >> /etc/fstab ' % (match, replace))

    # mount 并不会检测当前是否挂载，而是会默认直接挂载，如果不判断会被多次挂载的局面
    # /dev/vda2              36G  2.7G   31G   8% /
    # tmpfs                  12G     0   12G   0% /dev/shm
    # /dev/vdb               99G  216M   94G   1% /data
    # tmpfs                 8.0G     0  8.0G   0% /webdata
    # tmpfs                 8.0G     0  8.0G   0% /webdata
    # tmpfs                 8.0G     0  8.0G   0% /webdata
    # tmpfs                 8.0G     0  8.0G   0% /webdata

    # 因此我们需要df -h 先判断一次
    with settings(warn_only=True):
        if run('df -h | grep /webdata').failed:
            run('mount /webdata')



    # 优化配置
    run('sed -i -e "s/\(user\s*\)nginx/\\1%s/g" /etc/nginx/nginx.conf' % user)
    run('sed -i -e "s/\(worker_processes\s*\)[0-9]*/\\1%d/g" /etc/nginx/nginx.conf' % worker_processes)
    run('sed -i -e "s/\(worker_connections\s*\)[0-9]*/\\1%d/g" /etc/nginx/nginx.conf' % worker_connections)

    pass


def uninstall_nginx(user='webuser'):
    '''
    Uninstall nginx server & config & webuser device
    :param user:
    :return:
    '''

    match = "tmpfs    /webdata"

    with settings(warn_only=True):
        run('yum erase nginx -y')
        run('rm -rf /etc/nginx')
        run('umount /webdata')
        run('killall -u %s -m .' % user)
        run('rm -rf /webdata')
        run('userdel -r %s' % user)
        run('grep "%s" /etc/fstab && sed -i -e "s/%s.*//g" /etc/fstab' % (match, '\/'.join(match.split('/'))))

    pass


def putc_nginx(path):
    '''
    put nginx config file
    :param path: local path
    '''
    remote_path = '/etc/nginx/conf.d/'
    put(path, remote_path)




def redis():
    '''
    @TODO. install redis server
    :return:
    '''
    run('mkdir -p /storage/redis')
    run('yum install redis -y')
    run('chown redis.redis /storage/redis')
    pass


def mongo():
    '''
    @TODO. install mongo server
    :return:
    '''
    run('mkdir -p /storage/mongodb')
    pass


def git(proxy=None):
    '''
    Install git
    :param proxy:proxy server
    :return:
    '''
    run('yum install git -y')

    if proxy:
        run('git config --global http.proxy {}'.format(proxy))

    pass


def uninstall_git():
    '''
    remove git and git config
    :return:
    '''
    with settings(warn_only=True):
        run('yum erase git -y')
        run('rm -rf ~/.gitconfig')



def base():
    '''
    install base package
    :return:
    '''
    run(
        'yum install gcc-c++ make zlib-devel libxml2  libxml2-devel  bzip2-libs bzip2-devel  libcurl-devel  libjpeg libjpeg-devel  libpng libpng-devel  freetype freetype-devel  libmcrypt libmcrypt-devel  libtool-ltdl libtool-ltdl-devel openssl-devel -y')
    run('mkdir -p /usr/local/var/run')
    run('grep "ulimit" /etc/rc.local || echo "ulimit -SHn 65535" >> /etc/rc.local')

    pass



def expanduser(user=None):
    '''
    get userpath prefix ~ from remote server. for example: ~webuser
    :param user: username on remote
    '''
    if user is None:
        return '~'

    with settings(warn_only=True):
        if run('cat /etc/passwd | grep %s' % user).failed:
            abort("User:%s not exits" % user)
        else:
            user_path = run("cat /etc/passwd | grep webuser | awk -F ':' '{print $6}'")

    return user_path




def bind_host(ip=None,name=None):
    '''
    bind ip-name to /etc/hosts
    :param ip:ip address
    :param name: domain name
    '''
    with settings(warn_only=True):
        match = '%s %s' % (ip,name)
        if run('grep "%s" /etc/hosts' % match).failed:
            run('echo "%s" >> /etc/hosts' % match)

    pass


def clean_bind_host(ip=None,name=None):
    '''
    clean user bind ip-host
    :return:
    '''
    with settings(warn_only=True):
        match = '%s %s' % (ip,name)
        if run('grep "%s" /etc/hosts' % match):
            run('sed -i -e "s/%s//g" /etc/hosts' % match)

    pass



def known_host(name,user=None):
    '''
    set ssh figerprint
    :param name:domain
    :param user:webuser
    '''

    user_path = expanduser(user)
    command0 = 'grep %s %s/.ssh/known_hosts' % (name,user_path)
    command1 = 'ssh-keyscan %s >> %s/.ssh/known_hosts' % (name,user_path)
    command2 = 'sed -i -e "s/%s//g" %s/.ssh/known_hosts' % (name,user_path)


    if user:
        command0 = 'su - %s -c "%s"' % (user,command0)
        command1 = 'su - %s -c "%s"' % (user,command1)
        command2 = 'su - %s -c "%s"' % (user,command2)
        pass


    with settings(warn_only=True):
        if run(command0).failed:
            run(command1)
        else:
            # clean old record
            run(command2)
            run(command1)

    pass


def user_cmd(cmd,user=None):
    '''
    bind command for user with `su`
    :param cmd: command
    :param user: username
    '''
    if user:
        return 'su - %s -c "%s"' % (user,cmd)
    else:
        return cmd



def gito(path=None, url=None, branch='master',user=None,host_bind=None,tmpfs=None):
    '''
    deploy source code by git
    :param path:
    :param url:
    :param branch:
    :param user:
    :param host_known:
    :param host_bind:
    :param tmpfs: if set tmpfs,this process will write to rc.local @todo auto check
    :return:
    '''


    host_begin = url.find('@')
    host_end = url.find(':')
    request_host=url[host_begin+1:host_end].strip()

    if host_bind:
        # @todo 后期加入http协议的逻辑
        bind_host(host_bind,request_host)
        pass


    if url[0:3] == 'git':
        host_known=True
    else:
        host_known=False


    if request_host and host_known:
        known_host(request_host,user=user)


    parent = os.path.dirname(path)

    git_clone=user_cmd('git clone {} -b {} {}'.format(url, branch,path),user)

    with settings(warn_only=True):
        if run("test -d %s" % path).failed:
            with cd(parent):
                run(git_clone)

    # with cd(path):
    run(user_cmd("cd %s && git pull" % path,user))

    #基于内存盘的，需要添加rc.local
    if tmpfs:
        run("grep '%s' /etc/rc.local || echo '%s' >> /etc/rc.local" % (git_clone,git_clone))
        pass



def gitolite(pubkey=None):
    '''
    @TODO. create gitolite server
    :param pubkey:
    :return:
    '''
    run('mkdir /repo')
    gito('/tmp/gitolite', 'https://github.com/kbonez/gitolite.git')

    if pubkey is None:
        abort("please set your pubkey.")


    # put pub key
    # 执行脚本 @todo 等下次在安装的时候再说




    pass


def put_private_key(path=None, user=None):
    """
    Upload private key to remote server
    Limit: Must be a standard key generate from ssh-keygen
    :param path:local path
    :param user:remote username
    """
    if os.path.exists(os.path.expanduser(path)) is False:
        abort("private key not exist")
    else:
        # 通过解读key来判断是rsa还是dsa格式
        fp = open(os.path.expanduser(path))
        private_key = fp.read()
        pos = private_key.find("\n")

        if private_key[0:pos].find('DSA') > -1:
            dsa = True
        else:
            dsa = False

    user_path=expanduser(user)

    remote_root = '%s/.ssh' % user_path


    if dsa:
        remote_path = '%s/id_dsa' % remote_root
    else:
        remote_path = '%s/id_rsa' % remote_root

    with settings(warn_only=True):
        if run('test -d %s' % remote_root).failed:
            run('su - %s -c "mkdir %s"' % (user, remote_root))
            run('chown %s.%s %s' % (user,user, remote_root))

    put(path, remote_path, mode=0600)
    run('chown %s.%s %s' % (user,user,remote_path))
    pass


def put_public_key(path=None, user=None):
    """
    Upload pub key from remote server.
    Limit: Openssh standard key,must comment with user mail.
    :param path:local path
    :param user:remote username
    :return:
    """
    if os.path.exists(os.path.expanduser(path)) is False:
        abort("public key not exist")
    else:
        # 通过解读最后注释来判断key是否存在，如果不存在注释，判断为非法的key
        fp = open(os.path.expanduser(path))
        pub_key = fp.read()
        pos = pub_key.rfind(" ")

        mail = pub_key[pos + 1:].strip()
        if mail.find('@') == -1:
            abort('please add comment WHO YOU ARE.')


    user_path=expanduser(user)

    remote_root = '%s/.ssh' % user_path
    remote_path = '%s/authorized_keys' % remote_root

    with settings(warn_only=True):
        if run('test -d %s' % remote_root).failed:
            run('su - %s -c "mkdir %s"' % (user, remote_root))
            run('chown %s.%s %s' % (user,user, remote_root))


    put(path, '/tmp/tmp.pub', mode=0644)
    run('su - %s -c "grep %s %s | cat /tmp/tmp.pub >> %s"' % (user, mail,remote_path, remote_path))
    run('chown %s.%s %s' % (user,user,remote_path))


    pass


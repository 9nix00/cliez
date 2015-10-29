# -*- coding: utf-8 -*-


import paramiko
import os
import sys
import socket
import tty
import termios
import select
import tempfile
import requests
from functools import reduce

# if sys.version_info >= (3, 0):
from paramiko.py3compat import u


class SessionException(Exception):
    """
    发起会话时
    """

    pass


class PasswordRequiredException(paramiko.PasswordRequiredException):
    """
    密码
    """

    pass


class AuthException(Exception):
    """
    身份验证失败
    """

    pass


class SecurityException(Exception):
    """
    安全性,证书伪造
    """

    pass


class TransportException(Exception):
    """
    发起连接时,抛出
    """
    pass


class ConnectionException(Exception):
    """
    发起连接时,抛出
    """
    pass


class SSHException(Exception):
    """
    发起连接,ssh验证部分出错,等价于 paramiko.SSHException
    系统:SSH negotiation failed
    """

    pass


class SSHClient(object):
    """
    SSH 客户端工具

    .. note::

    目前我们只计划支持rsa验证方式,且为非交互式

    """

    username = None
    host = None
    port = 22
    transport = None
    server_pub_key = None
    private_key = None
    known_host = None
    client_ip=None

    sftp = None
    session = None

    def __init__(self, hostname, private_key='~/.ssh/id_rsa', cache_dir='/tmp/sshclient-cache'):
        """

        :param hostname:
        :param private_key:
        :return:
        """

        self.port = 22
        self.private_key = private_key

        if hostname.find('@') >= 0:
            self.username, self.host = hostname.split('@')
        else:
            raise ValueError("Invalid hostname")

        response = requests.get('https://api.ipify.org')
        self.client_ip = response.text

        self.connect()
        self.auth()
        pass

    def connect(self):
        """
        发起socket连接
        """

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            # sock.setsockopt()
        except ConnectionException:
            raise

        try:
            self.transport = paramiko.Transport(sock)
            try:
                self.transport.start_client()
            except paramiko.SSHException:
                raise SSHException
        except TransportException:
            raise TransportException
        pass

    def auth(self):
        """
        发起身份验证


        目前策略的设计原因:

        如果是内网机器,192.168.xxx.xxx允许忽略指纹

        我认为用户不应该通过外网部署,即使是为了省钱,一台路由也就几十块的成本,这个没必要节省

        一般必须要求拿外网部署的,都是干坏事的

        真实应用场景必然是用户和部署上传双路的,防止堵塞用户


        对于10.x A类子网段,这是更大型的应用,暂时先划分为外网规则
        """

        key = self.transport.get_remote_server_key()

        # 提取本地的known_host列表
        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            keys = {}

        # 检查known_host防止被伪造
        if self.host[:8] == '192.168.':
            # 内网不检测
            pass
        elif self.host not in keys:
            # 新的机器,不在列表中
            pass
        elif key.get_name() not in keys[self.host]:
            # 校验key类型,不在列表中
            pass
        elif keys[self.host][key.get_name()] != key:
            raise SecurityException

        path = os.path.expanduser(self.private_key)
        try:
            key = paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            raise PasswordRequiredException
        self.transport.auth_publickey(self.username, key)
        pass

    def close(self):
        """
        close
        :return:
        """
        if self.session:
            self.session.close()

        if self.sftp:
            self.sftp.close()
            pass

        self.transport.close()
        pass

    def open_session(self):
        """
        create session connection
        :return:
        """
        self.session = self.transport.open_session()
        self.session.get_pty()
        self.session.invoke_shell()
        pass

    def open_sftp(self):
        """
        create sftp connection
        :return:
        """
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        pass

    def upload(self, files, output=sys.stdout):
        """
        upload files
        :return:
        """
        sftp = self.sftp

        if sftp is None:
            raise ConnectionException("you must create a sftp connection before upload")

        size = len(files)

        for k, f in enumerate(files):
            if len(f) != 2:
                raise ValueError("Must contain src desc")

            src = os.path.expanduser(f[0])
            dest = f[1]

            output.write("uploading:{}...[{}/{}]\r".format(os.path.basename(f[0]), k + 1, size))
            output.flush()

            sftp.put(src, dest)

            # todo support upload directory
            # # dir or file
            # if os.path.isdir(src):
            #     sub_files = [(x[0], x[1]) for x in os.walk(src)]
            #     for sf in sub_files:
            #         print("upload {} to {}".format(sf, sf.replace(src, dest)))
            #         sftp.put(sf, sf.replace(src, dest))
            # else:
            #     sftp.put(src, dest)
            #     pass
        pass

    def uploads(self, files, output=sys.stdout):
        """
        将模板文件读取,转换后再上传至服务器
        :param files:
        :param output:
        :return:
        """

        sftp = self.sftp

        if sftp is None:
            raise ConnectionException("you must create a sftp connection before upload")

        size = len(files)

        for k, f in enumerate(files):
            assert len(f) == 3, "Must contain src desc replace_pair"

            src = os.path.expanduser(f[0])
            dest = f[1]

            with open(src) as h:
                origin = h.read()
                assert isinstance(f[2], tuple)
                assert isinstance(f[2][0], tuple)
                origin = reduce(lambda a, kv: a.replace(*kv), f[2], origin)
                pass

            with tempfile.NamedTemporaryFile('w') as h:
                h.write(origin)
                output.write("uploading:{}...[{}/{}]\r".format(os.path.basename(f[0]), k + 1, size))
                output.flush()
                sftp.put(h.name, dest)
                pass

        pass

    def download(self, files, output=sys.stdout):
        """
        download files
        :return:
        """

        sftp = self.sftp
        size = len(files)

        for k, f in enumerate(files):
            if len(f) != 2:
                raise ValueError("Must contain desc src")

            output.write("downloading:{}...[{}/{}]\r".format(os.path.basename(f[0]), k + 1, size))
            output.flush()
            sftp.get(f[0], os.path.expanduser(f[1]))

        pass

    def send(self, session, msg):
        """
        keep send order for tcp



        :param session:
        :param msg:
        :return:
        """

        for s in msg:
            len = session.send(s)

            if not len:
                while True:
                    len = session.send(s)
                    if len:
                        break

        pass

    def exec_command(self, command, bufsize=-1, timeout=None, get_pty=False):
        """
        Execute a command on the SSH server.  A new `.Channel` is opened and
        the requested command is executed.  The command's input and output
        streams are returned as Python ``file``-like objects representing
        stdin, stdout, and stderr.

        copy from paramiko

        :param str command: the command to execute
        :param int bufsize:
            interpreted the same way as by the built-in ``file()`` function in
            Python
        :param int timeout:
            set command's channel timeout. See `Channel.settimeout`.settimeout
        :return:
            the stdin, stdout, and stderr of the executing command, as a
            3-tuple

        :raises SSHException: if the server fails to execute the command
        """
        chan = self.transport.open_session(timeout=timeout)
        if get_pty:
            chan.get_pty()
        chan.settimeout(timeout)
        chan.exec_command(command)
        stdin = chan.makefile('wb', bufsize)
        stdout = chan.makefile('r', bufsize)
        stderr = chan.makefile_stderr('r', bufsize)
        return stdin, stdout, stderr

    def execute(self, commands, output=sys.stdout, timeout=0.0, su=None, silent=False):
        """
        execute remote command
        :return:
        """

        session = self.session

        if os.isatty(sys.stdin.fileno()):
            old_tty = termios.tcgetattr(sys.stdin)

        try:
            if os.isatty(sys.stdin.fileno()):
                tty.setraw(sys.stdin.fileno())
                tty.setcbreak(sys.stdin.fileno())

            session.settimeout(timeout)

            # 发送指令
            if commands.__class__ in (list, tuple):

                if su:
                    _ = [self.send(session, "su - {} -c '{}'\r\n".format(su, x)) for x in commands]
                else:
                    _ = [self.send(session, x + "\r\n") for x in commands]

            else:
                if su:
                    _ = [self.send(session, x) for x in "su - {} -c '{}'\r\n".format(su, str(commands))]
                else:
                    _ = [self.send(session, x) for x in str(commands) + "\r\n"]

            session.send("logout" + "\r\n")

            while True:
                r, w, e = select.select([session], [], [])

                # 接收数据
                if session in r:
                    try:
                        try:
                            x = u(session.recv(1024))
                        except (TypeError, UnicodeDecodeError):
                            x = '[?]'

                        if len(x) == 0:
                            output.write("\r\nexecute finished.renew session...\r\n")
                            self.session.close()
                            self.open_session()
                            break
                        if not silent:
                            output.write(x)
                            output.flush()
                    except socket.timeout:
                        raise SessionException("Timeout")
                    pass

                pass

        finally:
            if os.isatty(sys.stdin.fileno()):
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)

        pass

    pass

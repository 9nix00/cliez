# -*- coding: utf-8 -*-

import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from email.header import Header
from functools import reduce

import smtplib


class Mail(object):
    """
    邮件客户端

    此邮件客户端的使用场景
    适用于服务器内部指定了sendmail的场景.

    无密码,无用户名
    """

    def __init__(self, send_from, server='127.0.0.1'):
        """
        :param send_from:
        :param draft_root:
        :param server:
        :return:
        """
        self.send_from = send_from
        self.server = server
        pass

    def touch(self, send_to, subject, body=None, template=None, prefix=None, attachments=None):
        """
        :param send_to:
        :param subject:
        :param body:
        :param attachments:
        :return:
        """

        msg = MIMEMultipart(
            From=self.send_from,
            Date=formatdate(localtime=True),
        )

        if template:
            assert len(template) == 2, "tpl must contain (tpl_path,(replace tuple))"
            body = reduce(lambda a, kv: a.replace(*kv), template[1], open(os.path.expanduser(template[0]), 'r').read())

        msg.attach(MIMEText(body))

        for f in attachments or []:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
            msg.attach(part)

        msg['Subject'] = Header('[' + prefix + ']' + subject if prefix else subject, 'utf-8')
        msg['To'] = Header(COMMASPACE.join(send_to), 'utf-8')
        return msg

    def send(self, to_addrs, msg):
        server = smtplib.SMTP(self.server)
        server.sendmail(self.send_from, to_addrs, msg)
        server.quit()
        pass

    pass

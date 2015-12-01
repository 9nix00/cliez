# -*- coding: utf-8 -*-

import os
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from email.header import Header
from functools import reduce

import smtplib

import logging

logger = logging.getLogger(__name__)


# LOGGING_FORMAT = "%(levelname)s %(asctime)-15s %(message)s %(action)s %(to_mails)-8s"
# logging.basicConfig(format=LOGGING_FORMAT)


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

    def touch(self, send_to, subject, body=None, template=None, prefix=None, attachments=None, html=None):
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
            body = reduce(lambda a, kv: a.replace(kv[0], str(kv[1])), template[1], open(os.path.expanduser(template[0]), 'r').read())

        msg.attach(MIMEText(body, 'plain'))

        if html:
            assert len(html) == 2, "html must contain (tpl_path,(replace tuple))"
            html_body = reduce(lambda a, kv: a.replace(kv[0], str(kv[1])), html[1], open(os.path.expanduser(html[0]), 'r').read())

            html_msg = MIMEText(html_body, 'html')
            msg.attach(html_msg)

        for f in attachments or []:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
            msg.attach(part)

        msg['Subject'] = Header('[' + prefix + ']' + subject if prefix else subject, 'utf-8')
        msg['To'] = Header(COMMASPACE.join(send_to), 'utf-8')
        return msg

    def send(self, to_addrs, msg, timeout=None, logger_action=None):
        """
        发送邮件


        :param to_addrs:
        :param msg:
        :param timeout:
        :param logger_action: 用户自定义action名称,该名称会记录到日志中
        :return:
        """

        try:
            server = smtplib.SMTP(self.server, timeout=timeout)
            server.sendmail(self.send_from, to_addrs, msg)
            server.quit()
        except (socket.timeout, TimeoutError, smtplib.SMTPServerDisconnected):
            logger.error("timeout:%d %s %s", timeout, logger_action, ','.join(to_addrs))

            # 暂时关闭,对django支持不是很友好
            # extra={
            #     'action': logger_action,
            #     'to_mails': ','.join(to_addrs)
            # }
            pass
        pass

    pass

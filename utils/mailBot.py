#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText


class MailBot:
    def __init__(self, mail_host, mail_user, mail_pass, sender, receiver):
        """
        :param mail_host: 邮箱服务器地址(如smtp.qq.com)
        :param mail_user: 用户名(xyz123)
        :param mail_pass: 密码(部分邮箱为授权码)
        :param sender: 邮件发送方邮箱地址(xyz123.qq.com)
        :param receiver: 邮件接受方邮箱地址
        """
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender
        self.receiver = receiver

    def message_config(self, subject, content):
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = self.sender
        message['To'] = self.receiver
        message['Subject'] = subject
        return message

    def send_mail(self, message):
        """
        :param message: 邮件对象
        :return:
        """
        # 登录并发送邮件
        try:
            smtp_obj = smtplib.SMTP_SSL(self.mail_host)
            # 登录到服务器
            smtp_obj.login(self.mail_user, self.mail_pass)
            # 发送
            smtp_obj.sendmail(
                self.sender, self.receiver, message.as_string())
            # 退出
            smtp_obj.quit()
            print('Successfully sent a mail to %s' % self.receiver)
        except smtplib.SMTPException as e:
            print('Failed to send mail to xxx %s\nCaused by' % self.receiver, e)  # 打印错误

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 本文件的开发参照文档https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
import json
import logging
import requests
import urllib3
import hashlib
import base64
import hmac
from datetime import datetime

urllib3.disable_warnings()


def msg_not_null_and_blank(content):
    """
    非空字符串
    :param content: 字符串
    :return: 非空 - True，空 - False
    """
    if content and content.strip():
        return True
    else:
        return False


class FeiShuBot(object):

    def __init__(self, webhook, secret=None):
        """
        :param webhook: 飞书群自定义机器人webhook地址
        :param secret: 飞书群自定义机器人secret, 用于生成签名, 默认为None
        """
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.webhook = webhook
        self.secret = secret

    def generate_sign(self):
        # 获取当前时间戳
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        # 拼接timestamp和secret
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')

        return timestamp, sign

    def msg_config(self, content):
        """
        :param content: 消息内容
        :return: 消息对象
        """
        if not msg_not_null_and_blank(content):
            raise ValueError("text类型的消息内容不能为空！")

        if self.secret:
            timestamp, sign = self.generate_sign()
            msg = {
                "timestamp": timestamp,
                "sign": sign,
                "msg_type": "text",
                "content": {
                    "text": content
                }
            }
        else:
            msg = {
                "msg_type": "text",
                "content": {
                    "text": content
                }
            }
        return msg

    def send_msg(self, msg):
        """
        :param msg: 消息对象
        """
        try:
            response = requests.post(self.webhook, headers=self.headers, data=json.dumps(msg), verify=False)
        except requests.exceptions.HTTPError as exc:
            logging.error("飞书消息发送失败， HTTP error: %d, reason: %s" % (exc.response.status_code, exc.response.reason))
            raise
        except requests.exceptions.ConnectionError:
            logging.error("飞书消息发送失败，HTTP connection error!")
            raise
        except requests.exceptions.Timeout:
            logging.error("飞书消息发送失败，Timeout error!")
            raise
        except requests.exceptions.RequestException:
            logging.error("飞书消息发送失败, Request Exception!")
            raise
        else:
            try:
                result = response.json()
            except ValueError:
                logging.error("飞书消息发送失败，返回结果解析失败！")
                raise
            else:
                try:
                    if result["StatusMessage"] == "success":
                        logging.info("飞书消息发送成功！")
                        print("飞书消息发送成功！")
                except KeyError:
                    logging.error(f"飞书消息发送失败，错误信息{result}")
                    raise

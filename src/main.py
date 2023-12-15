import os
from datetime import date
import datetime
from borax.calendars.lunardate import LunarDate

import yaml
from cipherIO import CipherIO
from mailBot import MailBot
from FeishuBot import FeiShuBot


def get_env(env_name: str) -> str:
    """Get the value of an environment variable."""
    try:
        return os.environ[env_name]
    except KeyError:
        raise ValueError(f"Environment variable {env_name} not found")


# 从明文的yaml文件中读取数据
def get_people_info(peoplePath: str) -> list:
    peopleFile = open(peoplePath, 'r', encoding='utf-8')
    peopleDict = yaml.load(peopleFile.read(), Loader=yaml.FullLoader)
    return peopleDict


# 把一个由dict组成的list转换成bytes
def dict_list2bytes(dictList):
    bytes_str = "".encode('utf-8')
    for person in dictList:
        if bytes_str == "".encode('utf-8'):
            bytes_str = bytes(str(person), 'utf-8')
        else:
            bytes_str = bytes_str + ";".encode('utf-8') + bytes(str(person), 'utf-8')
    return bytes_str


# 输入的生日是公历生日
def solar_calendar(person):
    flag = False
    content = ""

    today = date.today()
    birth_year, birth_month, birth_day = str(person["Birthdate"]).split('-')
    if birth_year == "0000":
        age = "None"
    else:
        age = today.year - int(birth_year)
    birth_now = date(today.year, int(birth_month), int(birth_day))  # 今年的生日日期
    if birth_now < today:
        birth_now = date(today.year + 1, int(birth_month), int(birth_day))  # 明年的生日日期
    days_distance = (birth_now - today).days  # 今天的日期减去生日的日期

    if int(days_distance) == 0 or int(days_distance) == 3 or int(days_distance) == 7:
        flag = True
        content = f"您的好友{person['Name']}的{age}岁生日是公历{birth_month + '-' + birth_day}日，距今还有{days_distance}天\n"
    return flag, content


# 输入的生日是农历生日
def lunar_calendar(person):
    flag = False
    content = ""

    today = LunarDate.today()
    birth_year, birth_month, birth_day = person["Birthdate"].split('-')
    if birth_year != "0000":
        age = today.year - int(birth_year)
    else:
        age = "None"
    birth_now = LunarDate(today.year, int(birth_month), int(birth_day))  # 今年的生日日期
    if birth_now < today:
        birth_now = LunarDate(today.year + 1, int(birth_month), int(birth_day))  # 明年的生日日期
    days_distance = (birth_now - today).days

    if int(days_distance) == 0 or int(days_distance) == 3 or int(days_distance) == 7:
        flag = True
        content = f"您的好友{person['Name']}的{age}岁生日是农历{birth_month + '-' + birth_day}日，距今还有{days_distance}天\n"
    return flag, content


if __name__ == "__main__":
    sender = get_env("SENDER")
    mail_pass = get_env("MAIL_PASS")
    mail_host = "".join(["smtp.", sender.split("@")[1]])
    mail_user = sender.split("@")[0]
    receivers = get_env("RECEIVERS").split(";")  # 接收邮件的目标邮箱,可以是多个,用;分隔
    key = get_env("KEY").encode('utf-8')  # 对朋友的信息进行对称加密的密钥

    curPath = os.path.dirname(os.path.realpath(__file__))
    peoplePath = os.path.join(curPath, "../config/peopleInfo.yaml")
    peopleCipherPath = os.path.join(curPath, "../config/peopleCipherInfo.yaml")
    cipher = CipherIO(key)

    if os.path.exists(peoplePath):
        people = get_people_info(peoplePath)
        cipher.createCipherYaml(dict_list2bytes(people), peopleCipherPath)
        os.remove(peoplePath)
    elif os.path.exists(peopleCipherPath):
        strList = list(cipher.readCipherYaml(peopleCipherPath).split(";"))
        people = []
        for str0 in strList:
            people.append(eval(str0))
    else:
        raise FileNotFoundError("peopleInfo.yaml or peopleCipherInfo.yaml not found")

    send_flag = False  # 判断是否发送邮件
    content_flag = False
    contents = ""

    for person in people:
        if person["Calendar"] == "solar":
            content_flag, content = solar_calendar(person)
        elif person["Calendar"] == "lunar":
            content_flag, content = lunar_calendar(person)
        else:
            raise ValueError("Calendar must be Solar or Lunar")
        if content_flag:
            contents = contents + content
            send_flag = True

    if send_flag:
        # 发送邮件
        for receiver in receivers:
            mail = MailBot(mail_host, mail_user, mail_pass, sender, receiver)
            message = mail.message_config("生日提醒", contents)
            mail.send_mail(message)

            # # 下面是测试用的调试语句
            # print(contents)
            # print("Successfully sent a mail to %s\n" % receiver)

        # 发送飞书消息
        try:
            webhook = get_env("WEBHOOK")  # 飞书机器人的webhook地址
            try:
                secret = get_env("SECRET")  # 飞书机器人的secret
            except Exception as e:
                print("飞书机器人的secret未设置!\n")
                secret = None
            if secret:
                feishuBot = FeiShuBot(webhook, secret)
            else:
                feishuBot = FeiShuBot(webhook)
            msg = feishuBot.msg_config(contents)
            feishuBot.send_msg(msg)
        except Exception as e:
            print(f"飞书消息发送失败，原因为：{e}\n")

        # # 下面是测试用的调试语句
        # print(contents)
        # print("飞书消息发送成功\n")

    else:
        print("今天没有好友的生日\n")

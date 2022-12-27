import os
from datetime import datetime, date

import yaml

from mail import Mail


def get_env(env_name: str) -> str:
    """Get the value of an environment variable."""
    try:
        return os.environ[env_name]
    except KeyError:
        raise ValueError(f"Environment variable {env_name} not found")


def getPeopleInfo():
    curPath = os.path.dirname(os.path.realpath(__file__))
    peoplePath = os.path.join(curPath, "./peopleInfo.yaml")
    peopleFile = open(peoplePath, 'r', encoding='utf-8')
    peopleDict = yaml.load(peopleFile.read(), Loader=yaml.FullLoader)
    return peopleDict["People"]


if __name__ == "__main__":
    sender = get_env("SENDER")
    mail_pass = get_env("MAIL_PASS")
    mail_host = "".join(["smtp.", sender.split("@")[1]])
    mail_user = sender.split("@")[0]
    receivers = get_env("RECEIVERS").split(";")  # 接收邮件的目标邮箱,可以是多个,用;分隔

    people = getPeopleInfo()
    content = ""
    for p in people:
        # 获取当前日期
        today = date.today()
        birthYear, birthMonth, birthDay = p["Birthdate"].split('-')
        if birthYear == "0000":
            age = "None"
        else:
            age = today.year - int(birthYear)
        birthNow = date(today.year, int(birthMonth), int(birthDay))  # 今年的生日日期
        if birthNow < today:
            birthNow = date(today.year + 1, int(birthMonth), int(birthDay))  # 明年的生日日期
        time_distance = (birthNow - today).days  # 今天的日期减去生日的日期

        content = content + f"您的好友{p['Name']}的{age}岁生日是{birthMonth + '-' + birthDay}，距今还有{time_distance}天\n"

    # 发送邮件
    for receiver in receivers:
        # mail = Mail(mail_host, mail_user, mail_pass, sender, receiver)
        # message = mail.message_config("生日提醒", content)
        # mail.send_mail(message)
        print(content)
        print("Successfully sent a mail to %s\n" % receiver)

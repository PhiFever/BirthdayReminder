import os
from datetime import date
from borax.calendars.lunardate import LunarDate

import yaml
from cipherIO import CipherIO
from mailBot import MailBot


def get_env(env_name: str) -> str:
    """Get the value of an environment variable."""
    try:
        return os.environ[env_name]
    except KeyError:
        raise ValueError(f"Environment variable {env_name} not found")


# 从明文的yaml文件中读取数据
def getPeopleInfo(peoplePath: str) -> list:
    peopleFile = open(peoplePath, 'r', encoding='utf-8')
    peopleDict = yaml.load(peopleFile.read(), Loader=yaml.FullLoader)
    return peopleDict


# 把一个由dict组成的list转换成bytes
def dictList2bytes(dictList):
    bytes_str = "".encode('utf-8')
    for person in dictList:
        if bytes_str == "".encode('utf-8'):
            bytes_str = bytes(str(person), 'utf-8')
        else:
            bytes_str = bytes_str + ";".encode('utf-8') + bytes(str(person), 'utf-8')
    return bytes_str


# 输入的生日是公历生日
def SolarCalendar(person):
    flag = False
    content = ""

    today = date.today()
    birth_year, birth_month, birth_day = person["Birthdate"].split('-')
    if birth_year == "0000":
        age = "None"
    else:
        age = today.year - int(birth_year)
    birthNow = date(today.year, int(birth_month), int(birth_day))  # 今年的生日日期
    if birthNow < today:
        birthNow = date(today.year + 1, int(birth_month), int(birth_day))  # 明年的生日日期
    days_distance = (birthNow - today).days  # 今天的日期减去生日的日期

    if int(days_distance) == 0 or int(days_distance) == 3 or int(days_distance) == 7:
        flag = True
        content = f"您的好友{person['Name']}的{age}岁生日是公历{birth_month + '-' + birth_day}，距今还有{days_distance}天\n"
    return flag, content


# 输入的生日是农历生日
def LunarCalendar(person):
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
        content = f"您的好友{person['Name']}的{age}岁生日是农历{birth_month + '-' + birth_day}，距今还有{days_distance}天\n"
    return flag, content


if __name__ == "__main__":
    sender = get_env("SENDER")
    mail_pass = get_env("MAIL_PASS")
    mail_host = "".join(["smtp.", sender.split("@")[1]])
    mail_user = sender.split("@")[0]
    receivers = get_env("RECEIVERS").split(";")  # 接收邮件的目标邮箱,可以是多个,用;分隔

    key = get_env("KEY").encode('utf-8')  # 对朋友的信息进行对称加密的密钥

    curPath = os.path.dirname(os.path.realpath(__file__))
    peoplePath = os.path.join(curPath, "./peopleInfo.yaml")
    peopleCipherPath = os.path.join(curPath, "peopleCipherInfo.yaml")
    cipher = CipherIO(key)

    if os.path.exists(peoplePath):
        people = getPeopleInfo(peoplePath)
        cipher.createCipherYaml(dictList2bytes(people), peopleCipherPath)
        os.remove(peoplePath)
    elif os.path.exists(peopleCipherPath):
        strList = list(cipher.readCipherYaml(peopleCipherPath).split(";"))
        people = []
        for str0 in strList:
            people.append(eval(str0))
    else:
        raise FileNotFoundError("peopleInfo.yaml or peopleCipherInfo.yaml not found")

    mail_flag = False  # 判断是否发送邮件
    content_flag = False
    contents = ""

    for person in people:
        if person["Calendar"] == "solar":
            content_flag, content = SolarCalendar(person)
        elif person["Calendar"] == "lunar":
            content_flag, content = LunarCalendar(person)
        else:
            raise ValueError("Calendar must be Solar or Lunar")
        if content_flag:
            contents = contents + content
            mail_flag = True

    if mail_flag:
        # 发送邮件
        for receiver in receivers:
            mail = MailBot(mail_host, mail_user, mail_pass, sender, receiver)
            message = mail.message_config("生日提醒", contents)
            mail.send_mail(message)

            # 下面是测试用的调试语句
            # print(contents)
            # print("Successfully sent a mail to %s\n" % receiver)

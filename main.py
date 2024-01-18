import ast
import os
from datetime import date

import yaml
from borax.calendars.lunardate import LunarDate

from utils.cipherIO import CipherIO
from utils.mailBot import MailBot


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


def calculate_birthday(person, calendar_type='solar'):
    flag = False
    content = ""

    today = date.today() if calendar_type == 'solar' else LunarDate.today()
    birth_year, birth_month, birth_day = str(person["Birthdate"]).split('-')

    age = "None" if birth_year == "0000" else today.year - int(birth_year)

    date_type = date if calendar_type == 'solar' else LunarDate
    birth_now = date_type(today.year, int(birth_month), int(birth_day))  # 今年的生日日期

    if birth_now < today:
        birth_now = date_type(today.year + 1, int(birth_month), int(birth_day))  # 明年的生日日期

    days_distance = (birth_now - today).days

    if int(days_distance) in [0, 3, 7]:
        calendar_name = "公历" if calendar_type == 'solar' else "农历"
        flag = True
        content = f"您的好友{person['Name']}的{age}岁生日是{calendar_name}{birth_month + '-' + birth_day}日，距今还有{days_distance}天\n"

    return flag, content


if __name__ == "__main__":
    sender = get_env("SENDER")
    mail_pass = get_env("MAIL_PASS")
    mail_host = "".join(["smtp.", sender.split("@")[1]])
    mail_user = sender.split("@")[0]
    receivers = get_env("RECEIVERS").split(";")  # 接收邮件的目标邮箱,可以是多个,用;分隔
    key = get_env("KEY").encode('utf-8')  # 对朋友的信息进行对称加密的密钥

    curPath = os.path.dirname(os.path.realpath(__file__))
    peoplePath = os.path.join(curPath, "./config/peopleInfo.yaml")
    peopleCipherPath = os.path.join(curPath, "./config/peopleCipherInfo.yaml")
    cipher = CipherIO(key)

    if os.path.exists(peoplePath):
        people = get_people_info(peoplePath)
        cipher.createCipherYaml(dict_list2bytes(people), peopleCipherPath)
        os.remove(peoplePath)
    elif os.path.exists(peopleCipherPath):
        people_str_list = cipher.readCipherYaml(peopleCipherPath).split(";")
        people = []
        for ps in people_str_list:
            # 将单引号替换为双引号
            str_to_convert = ps.replace("'", '"')
            # 使用 ast.literal_eval 将字符串安全地转换为字典
            converted_dict = ast.literal_eval(str_to_convert)
            people.append(converted_dict)
    else:
        raise FileNotFoundError("peopleInfo.yaml or peopleCipherInfo.yaml not found")

    send_flag = False  # 判断是否发送邮件
    content_flag = False
    contents = ""

    for person in people:
        try:
            content_flag, content = calculate_birthday(person, calendar_type=person['Calendar'])
            if content_flag:
                contents = contents + content
                send_flag = True
        except ValueError:
            print("Calendar must be Solar or Lunar")

    if send_flag:
        # 发送邮件
        for receiver in receivers:
            mail = MailBot(mail_host, mail_user, mail_pass, sender, receiver)
            message = mail.message_config("生日提醒", contents)
            mail.send_mail(message)

            # # 下面是测试用的调试语句
            # print(contents)
            # print("Successfully sent a mail to %s\n" % receiver)

    else:
        print("今天没有好友的生日\n")

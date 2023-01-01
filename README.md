# 生日提醒机器人
本项目用于在你的朋友们生日前7天，3天以及当天给你自己的邮箱发送邮件作为提醒

## 项目构建
本项目使用Python3.6，建议本地运行使用Python3.6及以上版本，并添加与下文secrets同名的环境变量。

## 使用说明：
1. 首先你需要一个开启了SMTP服务邮箱，用于发送提醒邮件，此处以使用QQ邮箱为例，首先需要在QQ邮箱的设置中开启POP3/SMTP服务并记录授权码，具体操作可以参考[这里](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256)。
2. 在github上fork本项目，然后在你的仓库中点击Settings，进入Settings页面，点击左侧的Secrets->Actions，点击New repository secret，添加4个Secrets。 
   1. 名为`SENDER`，值为你用来发送信息的邮箱地址。eg.123456@qq.com
   2. 名为`MAIL_PASS`，值为你的邮箱授权码。
   3. 名为`RECEIVER`，值为你接收信息的邮箱地址。可以为多个邮箱，用英文分号`；`分隔。eg.123@qq.com;456@163.com
   4. 名为`KEY`，值为你用来加解密peopleInfo.yaml的密钥，可以为任意32 字节字符串。
3. 在peopleInfo.yaml文件中添加你的朋友们的生日信息，格式如下(可参照peopleInfor_example.yaml)：
   ```
   Name: 朋友的名字
   Birthdate: 朋友的生日，格式为yyyy-mm-dd，年份不知道的话填0000，月日必须填写正确。
   Calendar : 阴历(lunar)或者阳历(solar)
   Email: 朋友的邮箱地址，可选，不填写则不会在生日当天给朋友发送邮件。
   ```
   
   例如：
   ```
   - Birthdate: '1879-2-24'
     Calendar: solar
     Email: ''
     Name: 爱因斯坦
   ```
4. 在你的仓库中点击Actions，点击左侧的Birthday Reminder，点击右侧的Run workflow，点击Run workflow，即可开始运行测试。
5. 成功后会在每天的早上北京时间6:30开始执行，每天执行一次，你可以在Actions中查看执行结果。若有符合条件的朋友生日快到了，则会在你的邮箱中收到提醒邮件。
6. 如需修改相关信息，可以在本地添加环境变量`KEY`后运行decrypt.py解密peopleCipherInfo.yaml文件，修改后将peopleCipherInfo.yaml文件提交到你的仓库中，最后手动执行一次workflow即可完成更新。

## 致谢
本项目基于[birthdayBot](https://github.com/2892211452/birthdayBot)修改而来，感谢原作者。

## License
```
MIT License

Copyright (c) 2023 龙雀
```
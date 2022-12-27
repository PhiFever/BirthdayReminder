# 生日提醒机器人
本项目用于在你的朋友们生日前7天，3天以及当天给你自己的邮箱发送邮件作为提醒

## 使用说明：
1. 首先你需要一个开启了SMTP服务邮箱，用于发送提醒邮件，此处以使用QQ邮箱为例，首先需要在QQ邮箱的设置中开启POP3/SMTP服务并记录授权码，具体操作可以参考[这里](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256)。
2. 在github上fork本项目，然后在你的仓库中点击Settings，进入Settings页面，点击左侧的Secrets->Actions，点击New repository secret，添加三个Secrets。 
   1. 第一个名为`SENDER`，值为你用来发送信息的邮箱地址。eg.123456@qq.com
   2. 另一个名为`MAIL_PASS`，值为你的邮箱授权码。
   3. 最后一个名为`RECEIVER`，值为你接收信息的邮箱地址。可以为多个邮箱，用英文分号`；`分隔。eg.123@qq.com;456@163.com
   4. 添加完成后点击Add secret即可。
3. 在peopInfo.yaml文件中添加你的朋友们的生日信息，格式如下：
   1. name: 朋友的名字
      birthday: 朋友的生日，格式为yyyy-mm-dd
      email: 朋友的邮箱地址，可选
   2. 例如：
      name: 张三
      birthday: 1999-01-01
      email:
4. 在你的仓库中点击Actions，点击左侧的Birthday Reminder，点击右侧的Run workflow，点击Run workflow，即可开始运行。

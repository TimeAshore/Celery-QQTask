# Celery-QQTask
学习无非是为了取悦自己与别人，哈哈哈~

本文使用Celery定时任务，每天早上 6 点向手机邮箱发送一条笑话和一套最新的斗图，不仅博得清晨第一张笑脸，也减少了斗图图片重复的厌倦，每天带给自己一些新鲜感~~

本文涉及知识点：
1. 简单爬虫
2. 发送邮件
3. Celery定时任务

本项目 github :  https://github.com/TimeAshore/Celery-QQTask

关于Celery学习，请查看这篇文章[《Python异步任务之Celery》](https://timeashore.github.io/2018/06/06/Python%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1%E4%B9%8BCelery/)

项目目录结构图：

![image](https://upload-images.jianshu.io/upload_images/9136166-b6bf82395819c1bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)

`__init__.py` 文件实例化Celery

```
#encoding: utf-8
# Author: Timeashore

from celery import Celery

cele = Celery('demo')
cele.config_from_object('celery_app.celeryconfig')
```
celeryconfig.py 配置Celery

```
#encoding: utf-8
# Author: Timeashore

from celery.schedules import crontab

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'

CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

# import
CELERY_IMPORTS = (
    'celery_app.task1',
)
# schedules
CELERYBEAT_SCHEDULE = {
    'multiply-at-some-time': {
        'task': 'celery_app.task1.send_email_image',
        'schedule': crontab(hour=6, minute=20),   # 每天早上 6 点 00 分执行一次
        'args': ()                                  # 任务函数参数
    }
}
```


task1.py 是定时任务文件，发送图片邮件部分代码：

```
content = MIMEText(con + '''<html><body><table>
                              <tr>
                                    <td><img src="cid:imageid1"></td><td><img src="cid:imageid3"></td>
                               </tr>
                              <tr>
                                    <td><img src="cid:imageid2"></td><td><img src="cid:imageid4"></td>
                              </tr>
                              <tr>
                                    <td><img src="cid:imageid5"></td><td><img src="cid:imageid7"></td>
                               </tr>
                              <tr>
                                    <td><img src="cid:imageid6"></td><td><img src="cid:imageid8"></td>
                              </tr>
                        </table></body></html>''', 'html', 'utf-8')
    msg.attach(content)
    for x in range(1, 9):
        with open("{}.{}".format(x, point), "rb") as f:
            img_data = f.read()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imageid{}'.format(str(x)))
        msg.attach(img)
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, 收件人, msg.as_string())
        print u"发送成功"
    except Exception, e:
        print u"发送失败", e.message
    finally:
        s.quit()
```

邮件使用 QQ 邮箱，前提需要开启账户 POP3 和 IMAP , 具体设置请看项目代码。


**执行**


1，在celery_app同级目录下，启动Celery worker 进程

```
celery -A celery_app worker --loglevel=info
```
启动成功如下图：

![image](https://upload-images.jianshu.io/upload_images/9136166-9b43d97fb2f4f1e3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)
2，在celery_app同级目录下，开启定时任务，周期性的把 task 发送到 Broker 

```
celery beat -A celery_app
```
如下图：

![image](https://upload-images.jianshu.io/upload_images/9136166-afffa049827b3bcd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)




至此，把项目部署到服务器。每天 6 点都会收到一封邮件，包括一条笑话和最新一套斗图图片，你也可以把朋友邮件添加在程序的收件人列表中。

展示图：

![image](https://upload-images.jianshu.io/upload_images/9136166-135f26b33ca2d7f4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)

同样的，按照这个思路，可以很简单的实现天气预报实时通知，关心自己和朋友。

注：以上“朋友”仅字面朋友，女朋友就算了，毕竟稀缺 ~~

























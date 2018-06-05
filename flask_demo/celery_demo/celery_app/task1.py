# encoding: utf-8
# Author: Timeashore

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
from . import cele
from lxml import etree
import requests
import urllib2

# celery -A celery_app worker --loglevel=info
# celery beat -A celery_app

def scrapy_images():
    response = requests.get('http://www.doutula.com/article/list/')
    response = etree.HTML(response.text)
    url = response.xpath('//*[@id="home"]/div/div[2]/a[1]/@href')[0]
    res = requests.get('http://www.doutula.com/article/detail/3930377')
    res = etree.HTML(res.text)
    ans = 0
    for x in res.xpath('/html/body/div[2]/div[1]/div/div[2]/li/div[3]/div["class=artile_des"]')[:8]:
        imgurl = x.xpath('table/tbody/tr[1]/td/a/img/@src')[0]
        ans += 1
        # Save to localhost
        point = imgurl.split('.')[-1]
        with open('./{}.{}'.format(str(ans),point), 'wb') as fp:
            try:
                response = urllib2.urlopen(imgurl)
                fp.write(response.read())
            except:
                print u'【错误】当前图片无法下载'
    return point

@cele.task
def send_email_image():
    # Scrapy images
    point = scrapy_images()

    msg_from = "xxx@qq.com"  # 发送方邮箱
    passwd = 'xxx'  # 填入发送方邮箱的授权码
    msg_to = "xxx@qq.com"  # 收件人邮箱
    subject = "发送图片 "  # 主题
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to

    res = requests.get('https://www.qiushibaike.com/text/')
    res = etree.HTML(res.text)
    url = 'https://www.qiushibaike.com' + res.xpath('//*[@id="content-left"]/div[1]/a[1]/@href')[0]
    r = requests.get(url)
    r = etree.HTML(r.text)
    con = r.xpath('string(//*[@id="single-next-link"]/div)').strip()

    content = MIMEText(con+'''<html><body><table>
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
        s.sendmail(msg_from, msg_to, msg.as_string())
        s.sendmail(msg_from, '1438471386@qq.com', msg.as_string())
        print u"发送成功"
    except Exception, e:
        print u"发送失败", e.message
    finally:
        s.quit()
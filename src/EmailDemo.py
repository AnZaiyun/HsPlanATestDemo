import smtplib
import tkinter.filedialog
import openpyxl
import LoggingDemo
import os
import sys
from email.mime.text import MIMEText  # 邮件内容-文本
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import parseaddr, formataddr  # 分解、格式化地址
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders



# 格式名称和地址
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

log = LoggingDemo.setLoggingConfig()
filename = tkinter.filedialog.askopenfilename(filetypes=[('xlsx','.xlsx')])
data = openpyxl.load_workbook(filename)
sheet1 = data['邮箱参数配置']

log.debug("读取邮箱配置信息")
 # 服务器名称
mail_host = sheet1['B1'].value
# 邮箱登录名，注意不是邮箱地址
mail_user = sheet1['B2'].value
# 邮箱密码
mail_pwd = sheet1['B3'].value
# 发件人
sender = sheet1['B4'].value
# 收件人
receivers = sheet1['B5'].value.split(',')
# 抄送人
copyers = sheet1['B6'].value.split(',')

# 邮件主体
msgmultipart = MIMEMultipart()

log.debug("处理邮件正文信息")
# 邮件正文
message = MIMEText('<html><body><h2>{0}</h2></body></html>'.format(sheet1['B8'].value)+
                   '<p><img src="cid:1"></p>'+'<p><img src="cid:2"></p>', 'html', 'utf-8')

log.debug("处理邮件正文图片信息")
# 拼接图片
pic_addr1 = 'demo01.png'
pic_addr2 = 'demo02.png'

if not os.path.exists(os.getcwd() + "/" + pic_addr1):
    log.debug("未找到图片：" + pic_addr1)
    sys.exit()

if not os.path.exists(os.getcwd() + "/" + pic_addr2):
    log.debug("未找到图片：" + pic_addr2)
    sys.exit()

with open(pic_addr1, 'rb') as f:
    mime = MIMEBase('image', 'png', filename='demo01.png')
    mime.add_header('Content-Disposition', 'attachment', filename='demo01.png')
    mime.add_header('Content-ID', '<2>')
    mime.add_header('X-Attachment-Id', '2')
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    msgmultipart.attach(mime)

    # 作为附件添加
    imageApart = MIMEImage(open(pic_addr1, 'rb').read(), pic_addr1.split('.')[-1])
    imageApart.add_header('Content-Disposition', 'attachment', filename=pic_addr1)
    msgmultipart.attach(imageApart)

with open(pic_addr2, 'rb') as f:
    mime = MIMEBase('image', 'png', filename='demo02.png')
    mime.add_header('Content-Disposition', 'attachment', filename='demo02.png')
    mime.add_header('Content-ID', '<1>')
    mime.add_header('X-Attachment-Id', '1')
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    msgmultipart.attach(mime)

    # 作为附件添加
    imageApart = MIMEImage(open(pic_addr2, 'rb').read(), pic_addr2.split('.')[-1])
    imageApart.add_header('Content-Disposition', 'attachment', filename=pic_addr2)
    msgmultipart.attach(imageApart)

log.debug("处理邮件发送信息")
# 邮件内容的发件人信息
msgmultipart['From'] = _format_addr('<%s>' % sender)
# 邮件内容的收件人信息
for i in receivers:
    msgmultipart['To'] = _format_addr('<%s>' % i)
# 邮件内容的抄送人信息
for i in copyers:
    msgmultipart['CC'] = _format_addr('<%s>' % i)
# 邮件主题
subject = sheet1['B7'].value
msgmultipart['Subject'] = Header(subject, 'utf-8')
msgmultipart.attach(message)

log.debug("邮件开始发送")
# 连接服务器
smtpObj = smtplib.SMTP(mail_host, 25)

# 用户名密码登录
smtpObj.login(mail_user, mail_pwd)

# 发送邮件
smtpObj.sendmail(sender, receivers + copyers, msgmultipart.as_string())

log.debug("邮件发送成功")

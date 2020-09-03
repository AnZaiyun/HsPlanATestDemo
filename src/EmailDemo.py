import smtplib
import tkinter.filedialog
import xlrd
from email.mime.text import MIMEText  # 邮件内容-文本
from email.header import Header
from email.utils import parseaddr, formataddr  # 分解、格式化地址
from email.mime.multipart import MIMEMultipart
from fileinput import filename
from email.mime.base import MIMEBase
from email import encoders



# 格式名称和地址
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

filename = tkinter.filedialog.askopenfilename(filetypes=[('xls','.xls')])
data = xlrd.open_workbook(filename)
sheet1 = data.sheet_by_index(0)


 # 服务器名称
mail_host = sheet1.cell(0,1).value
# 邮箱登录名，注意不是邮箱地址
mail_user = sheet1.cell(1,1).value
# 邮箱密码
mail_pwd = sheet1.cell(2,1).value
# 发件人
sender = sheet1.cell(3,1).value
# 收件人
receivers = sheet1.cell(4,1).value.split(',')
# 抄送人
copyers = sheet1.cell(5,1).value.split(',')

print(mail_host+mail_user+mail_pwd+sender+str(receivers))
# 邮件主体
msgmultipart = MIMEMultipart()

# 邮件正文
message = MIMEText('<html><body><h2>这是一条由python发送的测试邮件</h2></body></html>'+
                   '<p><img src="cid:1"></p>'+'<p><img src="cid:2"></p>', 'html', 'utf-8')

# 拼接图片
pic_addr1 = 'demo01.png'
pic_addr2 = 'demo02.png'

with open(pic_addr1, 'rb') as f:
    mime = MIMEBase('image', 'png', filename='demo01.png')
    mime.add_header('Content-Disposition', 'attachment', filename='demo01.png')
    mime.add_header('Content-ID', '<2>')
    mime.add_header('X-Attachment-Id', '2')
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    msgmultipart.attach(mime)

with open(pic_addr2, 'rb') as f:
    mime = MIMEBase('image', 'png', filename='demo02.png')
    mime.add_header('Content-Disposition', 'attachment', filename='demo02.png')
    mime.add_header('Content-ID', '<1>')
    mime.add_header('X-Attachment-Id', '1')
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    msgmultipart.attach(mime)


# 邮件内容的发件人信息
msgmultipart['From'] = _format_addr('<%s>' % sender)
# 邮件内容的收件人信息
for i in receivers:
    msgmultipart['To'] = _format_addr('<%s>' % i)
# 邮件内容的抄送人信息
for i in copyers:
    msgmultipart['CC'] = _format_addr('<%s>' % i)
# 邮件主题
subject = '这是一条由python发送的测试邮件'
msgmultipart['Subject'] = Header(subject, 'utf-8')
msgmultipart.attach(message)

# 连接服务器
smtpObj = smtplib.SMTP(mail_host, 25)

# 用户名密码登录
smtpObj.login(mail_user, mail_pwd)

# 发送邮件
smtpObj.sendmail(sender, receivers + copyers, msgmultipart.as_string())
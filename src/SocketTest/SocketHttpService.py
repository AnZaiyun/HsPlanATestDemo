from socket import *
from src.SocketTest.LoggingDemo import LoggingFactory
import re
from threading import Thread

HOST = ''
PORT = 8088
BUFSIZ = 1024
ADDR = (HOST, PORT)

response_content ='''
HTTP/1.1 200 ok
Content-Type: text/html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {0}
</body>
</html>
'''

def init():
    '''
    初始化连接
    :return:
    '''
    global tcpSerSocket  #定义全局变量
    tcpSerSocket = socket(AF_INET, SOCK_STREAM)
    tcpSerSocket.bind(ADDR)
    tcpSerSocket.listen(5)  # 最大等待数
    log.debug('监听服务以启动。。。')

def accept_httprequest():
    '''
    接收新连接
    :return:
    '''
    log.debug('等待连接中。。。')
    while True:
        global addr
        tcpCliSocket, addr = tcpSerSocket.accept()  # accept方法会阻塞线程，因此对于每一个连接都需要重开线程
        log.debug('接收连接:' + str(addr))
        tcpCliSocketPool.append(tcpCliSocket)  # 加入连接池
        thread = Thread(target=message_handle,args=(tcpCliSocket,))  # 给每一个连接创建单独的线程
        thread.setDaemon(True)  # 设置成守护线程
        thread.start()

def message_handle(tcpCliSocket):
    '''
    消息处理
    :param client:
    :return:
    '''
    log.debug('开始处理请求信息。。。')
    while True:
        data = tcpCliSocket.recv(1024)
        # 如果接收数据长度为0，就认为连接已断开
        if len(data) == 0:
            tcpCliSocket.close()
            # 删除连接
            tcpCliSocketPool.remove(tcpCliSocket)
            log.debug('连接:' + str(addr)+'已下线。。。')
            log.debug('等待连接中。。。')
            break
        data = data.decode('utf-8')
        log.debug('全部请求信息：\r\n' + data)
        if data.find('POST') >= 0:
            pattern = re.compile(r'func_name[^\w]+(\w+)[^\w]+func_args[^\w]+(\w+)')
            params = re.search(pattern, data)
            if params:
                try:
                    func_name = params.group(1)
                    func_args = params.group(2)
                    log.debug('请求参数如下：\r\n' + "func_name:" + func_name + "\r\nfunc_args:" + func_args)
                    tcpCliSocket.send(response_content.format(func_name).encode())
                except Exception as ex:
                    log.warning('解析参数出错')
            else:
                log.debug('当前请求未传递参数')
                try:
                    tcpCliSocket.send(response_content.format("当前请求未传递参数").encode())
                except Exception:
                    tcpCliSocket.send(response_content.encode())
                    log.warning('返回数据出错')
        else:
            log.debug('非post请求')
            # tcpCliSocket.send("index_content".encode())
            tcpCliSocket.sendall(response_content.format("非post请求").encode())



log = LoggingFactory().getLogger()
tcpCliSocketPool = []  # 连接池

if __name__=='__main__':
    init()
    thread = Thread(target=accept_httprequest())
    thread.setDaemon(True)
    thread.start()
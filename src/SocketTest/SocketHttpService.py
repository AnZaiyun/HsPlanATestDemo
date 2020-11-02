from socket import *
from src.SocketTest.LoggingDemo import LoggingFactory
import re

HOST = ''
PORT = 8088
BUFSIZ = 1024
ADDR = (HOST, PORT)

response_content ='''
HTTP/1.1 200 ok
1231233
'''

tcpSerSocket = socket(AF_INET, SOCK_STREAM)
tcpSerSocket.bind(ADDR)
tcpSerSocket.listen(5)

log = LoggingFactory().getLogger()

log.debug('服务开启...')
while True:
    log.debug('等待连接...')
    tcpCliSocket,addr = tcpSerSocket.accept()
    log.debug('已接收连接:'+str(addr))

    data = tcpCliSocket.recv(BUFSIZ)
    if not data:
        break

    data = data.decode('utf-8')
    log.debug('****全部数据****\r\n'+data)
    if data.find('POST') >=0:
        pattern = re.compile(r'func_name[^\w]+(\w+)[^\w]+func_args[^\w]+(\w+)')
        params = re.search(pattern,data)
        if params:
            try:
                func_name= params.group(1)
                func_args = params.group(2)
                log.debug('****请求参数****\r\n' + "func_name:" + func_name + "\r\nfunc_args:" + func_args)
                tcpCliSocket.send(response_content.format(func_name).encode())
            except Exception as ex:
                log.warning('解析参数出错')
        else:
            log.debug('当前请求未传递参数')
            try:
                tcpCliSocket.send(response_content.format(func_name).encode())
            except Exception:
                tcpCliSocket.send(response_content.encode())
                log.warning('当前请求未传递参数')
    else:
        log.debug('非post请求')
        # tcpCliSocket.send("index_content".encode())
        tcpCliSocket.sendall(response_content.format("非post请求").encode())

tcpSerSocket.close()
from socket import *
from src.SocketTest.LoggingDemo import LoggingFactory
HOST = ''
PORT = 8088
BUFSIZ = 1024
ADDR = (HOST, PORT)

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
        params = data.split('\r\n')[-1]
        params = params.split('&')

        params_dict = dict()
        for item in params:
            key, value = item.split('=')
            params_dict[key] = value
        log.debug('****请求参数****\r\n'+str(params_dict))

        if 'func_name' in params_dict.keys():
            func_name = params_dict['func_name']
            func_args = ''
            try:
                func_args = params_dict['func_args']
            except:
                log.warning('当前请求未传递参数。。。')

            log.debug('开始执行方法:' + str(func_name) + '  方法参数：' + str(func_args))
        else:
            log.debug('当前请求未传递方法。。。')
            continue
    else:
        log.debug('非post请求')

tcpSerSocket.close()
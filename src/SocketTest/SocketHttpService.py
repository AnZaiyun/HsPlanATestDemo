from socket import *
from src.SocketTest.LoggingDemo import LoggingFactory
from src.Rabbitmq import ProviderFanout
import re
import json
from threading import Thread

HOST = ''
PORT = 8088
BUFSIZ = 1024
ADDR = (HOST, PORT)

#响应头与响应体需要有空行
#返回数据需要指定Content-Length，不然请求会一直等待获取数据
response_content ='''
HTTP/1.1 200 ok
Content-Type: application/json;charset=UTF-8
Content-Language: zh-CN
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: x-msg-timeout,X-Msg-Trace,csrfcheck,Shardinglnfo,Partition,broker_key,X-Original-URI,X-Request-Method,Authorization,access_token,login_account,auth_password,user_type,tenant_id,auth_code,Origin,No-Cache, X-Requested-With, lf-Modified-Since,Pragma, Last-Modified, Cache-Control, Expires,Content-Type,X-E4M-With
Access-Control-Allow-Methods: POST,OPTIONS,GET
Access-Control-Allow-Origin: *
Access-Control-Max-Age: 3600
Connection: keep-alive
Content-Length: {0}

{1}
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
        thread.setDaemon(True)  # 设置成守护线程，与主线程生命周期相同
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
            # 这里使用正则表达式解析请求体，目前这种方案为临时方案
            pattern = re.compile(r'func_\w+[^\w]+(\w+)[^\w]+func_\w+[^\w]+(\w+)')
            params = re.search(pattern, data)
            if params:
                try:
                    func_name = params.group(1)
                    func_args = params.group(2)
                    log.debug('请求参数如下：\r\n' + "func_name:" + func_name + "\r\nfunc_args:" + func_args)
                    func = {"func_name": func_name,
                            "func_args": func_args}
                    # 向mq中添加信息
                    # ProviderFanout.pushMq(func)
                    func = json.dumps(func)
                    funcLength = len(str(func).encode())
                    tcpCliSocket.send(response_content.format(funcLength,func).encode())
                except Exception as ex:
                    log.warning('请求参数不存在，请检查入参名func_name，func_args与格式json')
            else:
                result = '当前请求未传递参数'
                log.debug(result)
                tcpCliSocket.send(response_content.format(len(result.encode()), result).encode())
        else:
            # 返回长度以字节数计算
            result = "非post请求"
            log.debug(result)
            tcpCliSocket.send(response_content.format(len(result.encode()),result).encode())



log = LoggingFactory().getLogger()
tcpCliSocketPool = []  # 连接池

if __name__=='__main__':
    init()
    thread = Thread(target=accept_httprequest())
    thread.setDaemon(True)
    thread.start()
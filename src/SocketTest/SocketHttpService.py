from socket import *
from src.SocketTest.LoggingDemo import LoggingFactory
from src.Rabbitmq import ProviderFanout
import traceback
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
            paramDict = getParam(data)
            if "func_name" in paramDict.keys() or "func_args" in paramDict.keys():
                try:
                    log.debug("已接收参数："+str(paramDict))
                    func, funcLength = getReturnData(0, 'sucess', paramDict)
                    # TODO 参数解析以及调用其他函数处理的过程在这里编写，func是返回给前台的数据封装，实际返回的数据是字典resultData
                    # func只是为了将返回数据的格式封装为json
                    tcpCliSocket.send(response_content.format(funcLength, func).encode())
                except Exception as ex:
                    func,funcLength = getReturnData(-1,traceback.format_exc(),None)
                    tcpCliSocket.send(response_content.format(funcLength, func).encode())
                    log.error('参数发送时报错:'+func)
                finally:
                    log.debug('等待连接中。。。')
            else:
                result = '当前请求未传递参数func_name，func_args'
                log.debug(result)
                func, funcLength = getReturnData(-1, result, None)
                tcpCliSocket.send(response_content.format(funcLength, func).encode())
        else:
            # 返回长度以字节数计算
            result = "非post请求"
            log.debug(result)
            func, funcLength = getReturnData(-1, result, None)
            tcpCliSocket.send(response_content.format(funcLength, func).encode())

def getParam(data):
    '''
    传参的格式必须严格限制为以下样式
    {
        "func_name": "func_args22222",
        "func_args": "[1,2,3,4,5]"
    }
    key和value均需要用双引号，参数值不可有多余空格，参数体内不可有多余空行
    '''
    paramDict = dict()
    try:
        tmpParams = data.split("\r\n\r\n")[-1]  # 截取请求头和正文，只取正文信息
        tmpParams = tmpParams.replace("\r\n", "")  # 删除多余的换行符
        tmpParams = tmpParams.replace(" ", "").replace("{", "").replace("}", "")  # 删除多余的符号
        tmpParams = tmpParams[1:len(tmpParams) - 1]  # 截取头尾的双引号
        tmpParams = tmpParams.split("\",\"")  # 根据","将参数分组

        for i in tmpParams:
            param = i.split("\":\"")
            paramDict[param[0]] = param[1]  # 根据":"将每个参数的参数名和参数值分组
    except:
        log.error('解析参数时报错:' + traceback.format_exc())
    finally:
        return paramDict

def getReturnData(rcode,rstr,rdata):
    '''
    对传进来的数据进行二次封装，转换成json格式，返回前台
    :param rcode:
    :param rstr:
    :param rdata:
    :return:
    '''
    resultData['return_code'] = rcode
    resultData['return_str'] = rstr
    resultData['return_data'] = rdata
    func = json.dumps(resultData)
    funcLength = len(str(func).encode())
    return func,funcLength

log = LoggingFactory().getLogger()
tcpCliSocketPool = []  # 连接池

if __name__=='__main__':
    init()
    # 返回数据的二次封装
    # return_code 0代表成功，小于0代表失败
    # return_str 该字段不做严格要求，成功时可以填写处理成功的函数或过程名，失败时可以填写失败信息
    # return_data 函数执行成功后返回的数据
    resultData = {'return_code':0,'return_str':'sucess','return_data':None}
    thread = Thread(target=accept_httprequest())
    thread.setDaemon(True)
    thread.start()
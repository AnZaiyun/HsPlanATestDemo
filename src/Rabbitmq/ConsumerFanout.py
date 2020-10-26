import pika
'''https://www.cnblogs.com/shenh/p/10497244.html'''
from src.SocketTest.LoggingDemo import LoggingFactory
import requests

logfactory = LoggingFactory('info','debug')
log = logfactory.getLogger()
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host = '127.0.0.1',port = 5672,virtual_host = '/',credentials = credentials))
log.info('连接队列...')
channel = connection.channel()
# 创建临时队列,队列名传空字符，consumer关闭后，队列自动删除
# exclusive=False,durable=True
result = channel.queue_declare('QUEUE_C',exclusive=False,durable=True)
# 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
channel.exchange_declare(exchange = 'my-mq-exchange_C',durable = True, exchange_type='fanout')
# 绑定exchange和队列  exchange 使我们能够确切地指定消息应该到哪个队列去
channel.queue_bind(exchange = 'my-mq-exchange_C',queue = result.method.queue)
# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
log.info('获取队列(QUEUE_C)信息...')
def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag = method.delivery_tag)
    url = str(body.decode())
    log.info('队列(QUEUE_C)消息为：'+url)

    if url.startswith('http://'):
        log.info('开始发送请求调用远程接口:'+url)

        # 以下开始构建请求request信息
        session_requests = requests.session()
        response_data = session_requests.get(url)
        log.info('返回数据：'+response_data.text)


channel.basic_consume(result.method.queue,callback,# 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
                      auto_ack = False)
channel.start_consuming()
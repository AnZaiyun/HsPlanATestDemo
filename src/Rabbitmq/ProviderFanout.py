'''
这种模式下，传递到 exchange 的消息将会转发到所有与其绑定的 queue 上。

不需要指定 routing_key ，即使指定了也是无效。
需要提前将 exchange 和 queue 绑定，一个 exchange 可以绑定多个 queue，一个queue可以绑定多个exchange。
需要先启动 订阅者，此模式下的队列是 consumer 随机生成的，发布者 仅仅发布消息到 exchange ，由 exchange 转发消息至 queue。
'''

import pika
import json
from src.SocketTest.LoggingDemo import LoggingFactory

log = LoggingFactory().getLogger()

def pushMq(message):
    credentials = pika.PlainCredentials('guest', 'guest')  # mq用户名和密码
    # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = '127.0.0.1',port = 5672,virtual_host = '/',credentials = credentials))
    channel=connection.channel()
    result = channel.queue_declare(queue='QUEUE_PYTHON',durable= True)
    # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
    channel.exchange_declare(exchange = 'my-mq-exchange_PYTHON',durable = True, exchange_type='direct')
    # 将exchange和queue绑定
    channel.queue_bind(exchange = 'my-mq-exchange_PYTHON',queue = result.method.queue)

    message=json.dumps(message)
    log.debug("mq添加以下信息："+message)
    # 向队列插入数值 routing_key是路由名。delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。
    channel.basic_publish(exchange = 'my-mq-exchange_PYTHON',routing_key = 'spring-boot-routingKey_Python',body = message,
                          properties=pika.BasicProperties(delivery_mode = 2))
    connection.close()
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))

channel = connection.channel()
# 如果没有队列就创建这个队列
channel.queue_declare(queue='abc')
channel.basic_publish(exchange='',routing_key='abc',body='Hello World!')

print("[x] Sent 'Hello World!'")
connection.close()
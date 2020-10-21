import pika

# ########################### 消费者 ###########################

connection = pika.BlockingConnection(pika.ConnectionParameters( host='127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='studyExchange.An', durable=True)  # 如果队列没有创建，就创建这个队列

def callback(ch, method, propertities,body):
    print(" [x] Received %r" % body)

channel.basic_consume(on_message_callback = callback,
                      queue='studyExchange.An'
                      )

print(' [*] Waiting for message. To exit press CTRL+C')
channel.start_consuming()
import json
from kazoo.client import KazooClient
import requests

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
# 获取某个节点下所有子节点
node = zk.get_children('/services')
# 获取某个节点对应的值
value = zk.get('/services/cloud-consumer-order')
# 操作完后，别忘了关闭zk连接
zk.stop()
print(node,value)

url = "http://localhost:81/test/con/1/3"
session_requests = requests.session()
response_data = session_requests.get(url)
print(response_data.text)
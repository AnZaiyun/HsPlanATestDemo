from socket import *
from time import ctime

HOST = ''
PORT = 18001
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSocket = socket(AF_INET, SOCK_STREAM)
tcpSerSocket.bind(ADDR)
tcpSerSocket.listen(5)

while True:
    print('waiting for connection...')
    tcpCliSocket,addr = tcpSerSocket.accept()
    print('...connecting from:',addr)

    data = tcpCliSocket.recv(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))
    # while True:
    #     data = tcpCliSocket.recv(BUFSIZ)
    #     if not data:
    #         break
    #
    #     tcpCliSocket.send(('[%s] %s' % (ctime(), data)).encode())
    #     # print(data.decode('utf-8'))
    # tcpCliSocket.close()
tcpSerSocket.close()
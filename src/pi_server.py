#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket, time
import cv2
import numpy as np

# 接受图片大小的信息
def recv_size(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    print(buf)
    return buf.decode('utf-8')

# 接收图片
def recv_all(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(1024)
        if not newbuf: 
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# socket.AF_INET用于服务器与服务器之间的网络通信
# socket.SOCK_STREAM代表基于TCP的流式socket通信
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置地址与端口，如果是接收任意ip对本服务器的连接，地址栏可空，但端口必须设置
address = ('169.254.196.152', 22)
s.bind(address) # 将Socket（套接字）绑定到地址
s.listen(True) # 开始监听TCP传入连接
print ('Waiting for images...')
# 接受TCP链接并返回（conn, addr），其中conn是新的套接字对象，可以用来接收和发送数据，addr是链接客户端的地址。
conn, addr = s.accept()

while 1:
    length = recv_size(conn,5) #首先接收来自客户端发送的大小信息
    if isinstance (length,str): #若成功接收到大小信息，进一步再接收整张图片
        byteData = recv_all(conn, int(length))
        data = np.fromstring(byteData, np.uint8)
        decimg=cv2.imdecode(data,1) #解码处理，返回mat图片
        cv2.imshow('SERVER',decimg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
        print('Image recieved successfully!')
        conn.send(b'Server has recieved messages!')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

s.close()
cv2.destroyAllWindows()

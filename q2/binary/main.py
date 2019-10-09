from socket import *
import time
import os
import threading


module_path = os.path.dirname(__file__)[:-6] 
pathTxt = module_path + "in\\test.txt"     #此处test.txt路径
ip_port=("127.0.0.1",8000)
back_log =5
buffer_size = 1024
f = open(pathTxt, "r")
msg = ''
for i in f:
    msg += i
f.close()
tcp_client = socket(AF_INET,SOCK_STREAM)
tcp_client.connect(ip_port)

start = time.time()
tcp_client.sendall(msg.encode("utf-8"))
data = tcp_client.recv(buffer_size)

print(data.decode("utf-8"))
end = time.time()
past = end - start
print(past)
tcp_client.close()
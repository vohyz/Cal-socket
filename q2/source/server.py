import mmap         
import os
import time
import BytesWrite
import socketserver
import socket
import threading


module_path = os.path.dirname(__file__)[:-6]
pathSam = module_path + "in\\sample.txt"    #此处sample.txt路径
pathDat = module_path + "out\\sort.dat"     #此处sort.dat路径
pathLog = module_path + "out\\out.log"      #此处out.log路径

ip_port=("127.0.0.1",8000)
g_conn_pool = []
thread_max = 1
flag = 0

def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
    g_socket_server.bind(ip_port)
    g_socket_server.listen(5)  # 最大等待数
    print("服务端已启动，等待客户端连接...")
    

def accept_client():
    """
    接收新连接
    """
    while True:
        if len(g_conn_pool) < thread_max:
            client, _ = g_socket_server.accept()  # 阻塞，等待客户端连接
            # 加入连接池
            g_conn_pool.append(client)
            # 给每个客户端创建一个独立的线程进行管理
            thread = threading.Thread(target=message_handle, args=(client,))
            thread.setDaemon(True)
            thread.start()
        else:
            time.sleep(0.1)
 
def message_handle(client):
    """
    消息处理
    """
    global thread_max
    global flag
    while True:
        bytes = client.recv(1024)                       #客户端消息
        if bytes.decode(encoding='utf8') == '5':
            thread_max += 1
            rst = 'ok'
            print(thread_max)
            client.sendall(rst.encode(encoding='utf8'))
        elif bytes.decode(encoding='utf8') == 'end':
            rst = 'end'
            client.sendall(rst.encode(encoding='utf8'))
            flag = 1
        else:
            msg = SearchWords(bytes)
            client.sendall(msg.encode(encoding='utf8'))
        if len(bytes) == 0:
            client.close()
            # 删除连接
            g_conn_pool.remove(client)
            break

def SearchWords(data):
    wList = data.split()
    l = open(pathLog, 'a+')
    fd = os.open(pathDat, os.O_RDONLY)
    m = mmap.mmap(fd, 0,  access= mmap.ACCESS_READ)
    rst = ''
    for i in range(0, len(wList)):
        findNo = m.find(wList[i])
        if findNo == -1:
            rst += "notfound\n"
            continue
        findLength = len(wList[i])
        site = findNo + findLength
        rstLength = ''
        while chr(m[site]) in '0123456789':
            rstLength += str(chr(m[site]))
            site += 1
        rst += m[site:(site+int(rstLength))].decode()
        rst += '\n'
    l.close()
    return rst

def serverMain():
    wordList = BytesWrite.SelectWords(pathSam)
    BytesWrite.BytesWrite(wordList, pathDat)
    init()
    thread = threading.Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    while True:
        if flag == 0:
            time.sleep(0.2)
        else:
            return
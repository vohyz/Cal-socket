import mmap
import os
import time
import BytesWrite
import socketserver
import socket
import threading
import numpy as np                          #用于画图
import matplotlib.pyplot as plt             #用于画图
from scipy.interpolate import spline        #用于拟合曲线


module_path = os.path.dirname(__file__)[:-6]
pathSam = module_path + "in\\sample.txt"    #此处sample.txt路径
pathDat = module_path + "out\\sort.dat"     #此处sort.dat路径
pathLog = module_path + "out\\out.log"      #此处out.log路径

ip_port=("127.0.0.1",8000)
g_conn_pool = []
thread_max = 5

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
            # 设置成守护线程
            thread.setDaemon(True)
            thread.start()
        else:
            time.sleep(0.1)
 
 
def message_handle(client):
    """
    消息处理
    """
    while True:
        bytes = client.recv(1024)
        print("客户端消息:", bytes.decode(encoding='utf8'))
        wordList = BytesWrite.SelectWords(pathSam)
        BytesWrite.BytesWrite(wordList, pathDat)
        msg = SearchWords(bytes)
        client.sendall(msg.encode(encoding='utf8'))
        if len(bytes) == 0:
            client.close()
            # 删除连接
            g_conn_pool.remove(client)
            print("有一个客户端下线了。")
            break

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        print("conn is :",self.request)     
        print("addr is :",self.client_address)
 
        while True:
            try:
                data = self.request.recv(1024)
                if not data:break
                wordList = BytesWrite.SelectWords(pathSam)
                BytesWrite.BytesWrite(wordList, pathDat)
                msg = SearchWords(data)
                print("收到客户端的消息是",data.decode("utf-8"))
                self.request.sendall(msg.encode("utf-8"))
            except Exception as e:
                print(e)
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

def draw():
    f = open(pathLog, 'r')
    data = []
    drawdata = []
    for i in f:
        try:
            b = float(i)
            data.append(b)
        except:
            continue
    i = 0
    if len(data) < 19:
        return
    while i < len(data):
        drawdata.append(data[i]/data[i+1])
        i += 2

    x = [j for j in range(1, len(drawdata)+1)]
    y = drawdata
    xnew = np.linspace(1,len(drawdata),300)
    y_smooth = spline(x,y,xnew)
    plt.figure(figsize=(8,4)) 
    plt.plot(xnew,y_smooth, label="$sin(x)$",color="red",linewidth=2)
    plt.xlabel("Times")
    plt.ylabel("time")
    plt.title("store time / search time")
    plt.savefig(module_path + "out\\result.png")
    plt.show()

if __name__ == "__main__":
    #s = socketserver.ThreadingTCPServer(ip_port,MyServer)
    #s.serve_forever()

    #draw()
    init()
    # 新开一个线程，用于接收新连接
    thread = threading.Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    # 主线程逻辑
    while True:
        cmd = input("""--------------------------
输入1:查看当前在线人数
输入2:给指定客户端发送消息
输入3:关闭服务端
""")
        if cmd == '1':
            print("--------------------------")
            print("当前在线人数：", len(g_conn_pool))
        elif cmd == '2':
            print("--------------------------")
            index, msg = input("请输入“索引,消息”的形式：").split(",")
            g_conn_pool[int(index)].sendall(msg.encode(encoding='utf8'))
        elif cmd == '3':
            exit()
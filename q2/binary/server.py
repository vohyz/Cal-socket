import mmap
import os
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
    fd = os.open(pathDat, os.O_RDWR)
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
    s = socketserver.ThreadingTCPServer(ip_port,MyServer)
    s.serve_forever()

    draw()
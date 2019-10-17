from socket import *
import time
import os
from threading import Thread
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


module_path = os.path.dirname(__file__)[:-6] 
pathTxt = module_path + "in\\test.txt"     #此处test.txt路径
ip_port=("127.0.0.1",8000)
back_log =5
buffer_size = 1024
f = open(pathTxt, "r")
msg = ''
for i in f:
    msg += str(len(i)-1)
    msg += i
f.close()

def searchWords(full = '0'):
    tcp_client = socket(AF_INET,SOCK_STREAM)
    tcp_client.connect(ip_port)
    if full == '0':
        tcp_client.sendall(msg.encode("utf-8"))
    else:
        message = full
        tcp_client.sendall(message.encode("utf-8"))
    data = tcp_client.recv(buffer_size)
    #print(data.decode("utf-8"))   要看结果可以在这里
    tcp_client.close()

def draw(paint):
    i = 1
    x = []
    y = [[] for i in range(5)]
    while i < 6:
        j = 1
        x.append([i, i, i, i, i])
        while j < 6:
            y[i - 1].append(j)
            j += 1
        i += 1

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title("server/client time")
    ax.set_xlabel("threads - server")
    ax.set_ylabel("threads - client")
    ax.set_zlabel("time")

    figure1 = ax.plot(x[0], y[0], paint[0], c='g')
    figure2 = ax.plot(x[1], y[1], paint[1], c='b')
    figure3 = ax.plot(x[2], y[2], paint[2], c='y')
    figure4 = ax.plot(x[3], y[3], paint[3], c='orange')
    figure5 = ax.plot(x[4], y[4], paint[4], c='r')
    plt.savefig(module_path + "out\\result.png")
    plt.show()

def clientMain():
    n = 1
    count = 1
    paint = [[] for i in range(5)]
    while n < 6 and count < 6:
        li = []
        start = time.time()
        for i in range(n):
            li.append(Thread(target=searchWords))
        for i in li:
            i.setDaemon(True)
            i.start()
        for i in li:
            i.join()
        end = time.time()
        past = end - start
        paint[count-1].append(past)
        print(n)
        print(past)
        if n == 5 and count < 25:
            searchWords('5')
            n = 1
            count += 1
        elif n < 5 and count < 6:
            n += 1
        elif count >= 6:
            break
    searchWords('end')
    draw(paint)
clientMain()
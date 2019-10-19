from socket import *
import time
import os
from threading import Thread
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


module_path = os.path.dirname(__file__)[:-6] 
pathTxt = module_path + "in\\test.txt"     #此处test.txt路径
pathLog = module_path + "out\\out.log"        #此处out.log路径
ip_port=("127.0.0.1",8000)
buffer_size = 1024
f = open(pathTxt, "r")
msg = ''
for i in f:
    msg += str(len(i.strip('\n')))
    msg += i
f.close()

def DivideWords(data, count):
    List = data.split()
    part = len(List) // count
    bag = []
    for i in range(count-1):
        bag.append(List[part*i:part*(i+1)])
    bag.append(List[part*(count-1):])
    return bag

def searchWords(message, full = '0'):
    sendMessage = ''
    for i in message:
        sendMessage += i
        sendMessage += '\n'
    tcp_client = socket(AF_INET,SOCK_STREAM)
    tcp_client.connect(ip_port)
    if full == '0':
        tcp_client.sendall(sendMessage.encode("utf-8"))
    else:
        sendMessage = full
        tcp_client.sendall(sendMessage.encode("utf-8"))
    data = tcp_client.recv(buffer_size)
    if data.decode("utf-8") == 'end' or data.decode("utf-8") == 'ok':
        tcp_client.close()
    else:
        tcp_client.close()
        return data.decode("utf-8").strip('\n')
    

class Search(Thread):
    def __init__(self, arg1, arg2):
        super(Search, self).__init__()
        self.arg1 = arg1
        self.arg2 = arg2

    def run(self):
        self.result = searchWords(self.arg1, self.arg2)

    def get_result(self):
        return self.result

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

def clientMain(ths=0):
    if ths == 0:
        n = 1
        count = 1
        paint = [[] for i in range(5)]
        while n < 6 and count < 6:
            li = []
            bag = DivideWords(msg, n)
            start = time.time()
            rst = ''
            for i in range(n):
                li.append(Search(bag[i], '0'))
            for i in li:
                i.setDaemon(True)
                i.start()
            for i in li:
                i.join()
                rst += i.get_result()
            end = time.time()
            past = end - start
            l = open(pathLog, 'a+')
            print(rst, file= l)
            print(past, file= l)
            l.close()
            paint[count-1].append(past)
            print(n)
            print(past)
            if n == 5 and count < 25:
                searchWords('5', '5')
                n = 1
                count += 1
                print(count)
            elif n < 5 and count < 6:
                n += 1
            elif count >= 6:
                break
        searchWords(['end'], '0')
        draw(paint)
    else:
        li = []
        n = ths
        bag = DivideWords(msg, n)
        start = time.time()
        rst = ''
        for i in range(n):
            li.append(Search(bag[i], '0'))
        for i in li:
            i.setDaemon(True)
            i.start()
        for i in li:
            i.join()
            rst += i.get_result()
        end = time.time()
        past = end - start
        searchWords(['end'], '0')
        l = open(pathLog, 'a+')
        print(rst, file= l)
        print(past, file= l)
        l.close()
#clientMain()
'''
ii = [
    [29,28,30,28,28],
    [40,33,32,31,33],
    [58,43,35,36,38],
    [62,52,45,38,37],
    [71,58,51,49,42]
]
draw(ii)
'''
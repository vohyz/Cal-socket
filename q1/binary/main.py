import time                         
import mmap
import os
import BytesWrite
import numpy as np                  #用于画图
import matplotlib.pyplot as plt     #用于画图
from scipy.interpolate import spline#用于拟合曲线


module_path = os.path.dirname(__file__)[:-6]
pathSam = module_path + "in\\sample.txt"     #此处sample.txt路径
pathDat = module_path + "out\\sort.dat"       #此处sort.dat路径
pathTxt = module_path + "in\\test.txt"       #此处test.txt路径
pathLog = module_path + "out\\out.log"        #此处out.log路径
def SearchWords():
    t = open(pathTxt, 'r')
    l = open(pathLog, 'a+')
    fd = os.open(pathDat, os.O_RDWR)
    m = mmap.mmap(fd, 0,  access= mmap.ACCESS_READ)
    wList = []
    for i in t:
        wList += i.split()
    for i in range(0, len(wList)):
        findNo = m.find(wList[i].encode("utf-8"))
        if findNo == -1:
            print("notfound", file= l)
            continue
        findLength = len(wList[i])
        site = findNo + findLength
        rstLength = ''
        while chr(m[site]) in '0123456789':
            rstLength += str(chr(m[site]))
            site += 1
        print(m[site:(site+int(rstLength))].decode(), file= l)
    t.close()
    l.close()

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
    wordList = BytesWrite.SelectWords(pathSam)

    startTime = time.time()
    BytesWrite.BytesWrite(wordList, pathDat)
    endTime = time.time()
    costTime1 = endTime - startTime

    startTime = time.time()
    SearchWords()
    endTime = time.time()
    costTime2 = endTime - startTime
    l = open(pathLog, 'a+')
    print(costTime1, file= l)
    print(costTime2, file= l)
    l.close()
    draw()
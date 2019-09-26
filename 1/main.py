import BytesWrite
import linecache  
import random
import logging

pathDat = "C:\\Users\\ZYX\\Desktop\\Pycalculate\\1\\sort.dat"       #此处sort.dat路径
pathTxt = "C:\\Users\\ZYX\\Desktop\\Pycalculate\\1\\test.txt"       #此处test.txt路径

def SearchWords():
    f = open(pathTxt,'r')
    wList = []
    for i in f:
        wList.append(i)
    while True:
        a = random.randrange(1, 168)
        theline = linecache.getline(pathDat, a)
        for i in wList:
            if i in theline:
                

    logging.basicConfig(filename='out.log', level=logging.INFO)
    logging.debug('debug message')
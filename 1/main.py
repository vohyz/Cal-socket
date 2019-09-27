import BytesWrite
import time
import mmap
import os

pathSam = "C:\\Users\\ZYX\\Desktop\\Pycalculate\\1\\sample.txt"     #此处sample.txt路径
pathDat = "C:\\Users\\ZYX\\Desktop\\Pycalculate\\1\\sort.dat"       #此处sort.dat路径
pathTxt = "C:\\Users\\ZYX\\Desktop\\Pycalculate\\1\\test.txt"       #此处test.txt路径
pathLog = "C:\\Users\\ZYX\\Desktop\\Pycalculate\\1\\out.log"        #此处out.log路径
def SearchWords():
    t = open(pathTxt,'r')
    l = open(pathLog,'w+')
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
    l = open(pathLog,'a+')
    print(costTime1, file= l)
    print(costTime2, file= l)
    l.close()
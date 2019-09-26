import re

def SelectWords(path = "C:\\Users\\msi-\\Desktop\\Pycalculate\\1\\sample.txt"):
    f = open(path,'r')
    WordList = []
    a = 0
    for i in f:
        WordList +=(re.split('[,/.\\\n \t\r:|]',i))
        a += 1
    WordList.sort(key=str.lower)
    while WordList[0] == '':
        del WordList[0]
    return WordList

#SelectWords()
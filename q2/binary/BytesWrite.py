import re

def SelectWords(path):
    f = open(path,'r')
    WordList = []
    for i in f:
        WordList +=(re.split('[,/.\\\n \t\r:|]',i))
    f.close()
    WordList.sort(key=str.lower)
    while WordList[0] == '':
        del WordList[0]
    return WordList

def BytesWrite(WordList, pathDat):
    WordListB = []
    for i in WordList:
        length = str(len(i))
        word = length
        word += i
        WordListB.append(word.encode("utf-8")) 

    KBlist = WordListB[0]
    f = open(pathDat, 'w+')
    for i in WordListB[1:]:
        if len(KBlist) + len(i) > 1024:
            print(KBlist, file = f, end = '')
            KBlist = i
        else:
            KBlist += i
    if len(KBlist) > 1:
        print(KBlist, file = f, end = '')
    f.close()
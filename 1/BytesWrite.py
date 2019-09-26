import TextChange

pathTxt = "C:\\Users\\msi-\\Desktop\\Pycalculate\\1\\sample.txt"     #此处sample.txt路径
pathDat = "C:\\Users\\msi-\\Desktop\\Pycalculate\\1\\sort.dat"       #此处sort.dat路径
def BytesWrite(pathTxt, pathDat):
    WordListB = TextChange.Str2Bytes(pathTxt)
    KBlist = WordListB[0]
    f = open(pathDat, 'w+')
    for i in WordListB[1:]:
        if len(KBlist) + len(i) > 1024:
            print(KBlist, file= f)
            KBlist = i
        else:
            KBlist += i
    if len(KBlist) > 1:
        print(KBlist, file= f)
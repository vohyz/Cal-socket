import SelectWords

def Str2Bytes(path = "C:\\Users\\msi-\\Desktop\\Pycalculate\\1\\sample.txt"):
    WordList = SelectWords.SelectWords(path)
    WordListB = []
    for i in WordList:
        length = str(len(i))
        word = length
        word += i
        WordListB.append(word.encode("utf-8")) 
    return WordListB

#Str2Bytes()
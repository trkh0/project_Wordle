fwrite = open("words.txt","w", encoding="utf8")

words = set()
file = open("georgerr.txt", encoding="utf8")
while True:
    line = file.readline()
    for word in line.split():
        newword = ""
        for l in word:
            if l.isalpha() == True:
                newword += l
        if len(newword) == 5:
            words.add(newword.upper())
            #fwrite.write(word.upper() + " ")
            #print(word.upper())
    if not line:
        break

wordSet = set(words)
for word in wordSet:
    fwrite.write(word.upper() + " ")
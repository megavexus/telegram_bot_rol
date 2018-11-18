def parseInput(words, no):
    words = words.split()
    a = len(words) - no
    oup = words[1]
    for i in range(2, 2 + a):
        oup += words[i]
    outt = []
    outt.append(words[0].lower())
    outt.append(oup.lower())
    for i in range(2, no):
        outt.append(words[a + i].lower())
    return outt


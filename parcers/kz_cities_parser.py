import codecs
fileObj = codecs.open("parce_russian.txt", "r", "utf_8_sig" )
city = ''
region = ''
for i in range(535):
    txt = fileObj.readline()
    if i % 5 == 1:
        city = txt[4:-7]
    if i % 5 == 3:
        region = txt[4:-7]
        if city[0] == 'c':
            continue
        print("\"" + city + "(" + region + ")\",")
fileObj.close()

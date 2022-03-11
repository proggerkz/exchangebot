import codecs
fileObj = codecs.open("russian-cities.json", "r", "utf_8_sig" )
start = fileObj.readline()
city = ''
region = ''
for i in range(11170):
    txt = fileObj.readline()
    if i % 10 == 6:
        txt = txt[13:-4]
        city = txt
    if i % 10 == 8:
        txt = txt[16:-3]
        region = txt
        print("\"" + city + '(' + region + ')'"\",")
fileObj.close()

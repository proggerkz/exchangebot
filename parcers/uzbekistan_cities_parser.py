import codecs
fileObj = codecs.open("uz.txt", "r", "utf_8_sig" )
start = fileObj.readline()
city = ''
region = ''
for i in range(571):
    txt = fileObj.readline()
    if txt[1] == 't' and txt[2] == 'd' and txt[3] == '>':
        reg_or_city = txt[4:-7]
        if city == '':
            city = reg_or_city
        else:
            region = reg_or_city
            print(f'"{city}({region})",')
            city = ''
            region = ''

fileObj.close()

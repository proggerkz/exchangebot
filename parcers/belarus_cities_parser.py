import codecs
fileObj = codecs.open("uz.txt", "r", "utf_8_sig" )
start = fileObj.readline()
city = ''
region = ''
for i in range(274):
	txt = fileObj.readline()
	if txt[1] == 't' and txt[2] == 'd' and txt[3] == '>':
		reg_or_city = txt[4:-7]
		if reg_or_city != ' ' and reg_or_city != '':
			print(f'"{reg_or_city}(Белоруссия)",')

fileObj.close()

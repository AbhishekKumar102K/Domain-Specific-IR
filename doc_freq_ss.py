import json
import math


f = open('data_tkn.json','r')
doc = json.load(f)

N = 200853
dic = {}

for i in range(1,N+1):
	hdline = doc[str(i)][0]
	desc = doc[str(i)][1]

	doc_hd = {}
	doc_desc = {}
	for word in hdline.split():
		if word in doc_hd.keys():
			doc_hd[word] += 1
		else:
			doc_hd[word] = 1

	for word in desc.split():
		if word in doc_desc.keys():
			doc_desc[word] += 1
		else:
			doc_desc[word] = 1


	sshd = 0.0000
	ssdesc = 0.0000
	for word in doc_hd.keys():
		sshd += (math.log10(doc_hd[word])+1)**2

	for word in doc_desc.keys():
		ssdesc += (math.log10(doc_desc[word])+1)**2


	temp = []
	temp.append(max(0.000001,sshd**0.5))
	temp.append(max(0.000001,ssdesc**0.5))

	dic[str(i)] = temp

with open('doc_lengths.json', 'w') as write_file:
	json.dump(dic, write_file)

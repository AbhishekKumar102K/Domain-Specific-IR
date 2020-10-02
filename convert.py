import json

f = open('headline_inverted_index.json','r')
hdline = json.load(f)

dic = {}

for word in hdline.keys():
	dic[word] = len(hdline[word])-1

with open('headline_inverted_index2.json', 'w') as write_file:
    json.dump(dic, write_file)

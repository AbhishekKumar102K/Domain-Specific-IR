import json

dic = {}
ind = 0

for line in open('raw_data.json', 'r'):
	rdict = json.loads(line)
	ind += 1
	lis = []
	lis.append(rdict["headline"])
	lis.append(rdict['link'])
	lis.append(rdict['short_description'])
	dic[ind] = lis

json_obj = json.dumps(dic, indent = 4)

with open('data.json', 'w') as write_file:
	write_file.write(json_obj)
import json


inv_index = {}

f = open('data_tkn.json')
load_dic = json.load(f)


for ind in load_dic:
	desc = load_dic[ind][1]
	# print(type(hdline))
	for word in desc.split():
		if word not in inv_index.keys():
			inv_index[word] = {}
			inv_index[word][int(ind)] = 1
			continue
		if int(ind) not in inv_index[word].keys():
			inv_index[word][int(ind)] = 1
		else:
			inv_index[word][int(ind)] += 1

for word in inv_index:
	ct = 0
	for val in inv_index[word].values():
		ct += val

	inv_index[word]["total"] = ct

with open('desc_inverted_index.json', 'w') as write_file:
	json.dump(inv_index, write_file)

 

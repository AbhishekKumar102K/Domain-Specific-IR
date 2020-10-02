import json

f = open('raw_data.json', 'r')

# data = json.loads(f.read())

dic = {}
ind = 0

for i in open('raw_data.json', 'r'):
    lol = json.loads(i)
    ind += 1
    lis = []
    # print(type(lol))
    # print(i)
    # lol = dict(i)
    lis.append(lol["headline"])
    lis.append(lol['link'])
    lis.append(lol['short_description'])
    dic[ind] = lis

f.close()

with open('data.json', 'w') as write_file:
    json.dump(dic, write_file)
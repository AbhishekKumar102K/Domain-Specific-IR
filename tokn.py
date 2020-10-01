import json
import nltk
from nltk.tokenize import word_tokenize

f = open('data.json')
load_dic = json.load(f)

dic = {}

for ind in load_dic:
    lis = []
    hdline_punc = word_tokenize(load_dic[ind][0].lower())
    hdline_no_punc = [word for word in hdline_punc if word.isalnum()]
    lis.append(' '.join(hdline_no_punc))

    short_punc = word_tokenize(load_dic[ind][2].lower())
    short_no_punc = [word for word in short_punc if word.isalnum()]
    lis.append(' '.join(short_no_punc))

    dic[ind] = lis

f.close()

with open('data_tkn.json', 'w') as write_file:
    json.dump(dic, write_file)

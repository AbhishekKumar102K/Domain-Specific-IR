import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *

def stem(a):
	p = PorterStemmer()
	a = [p.stem(word) for word in a]
	return a



f = open('data_before_tkn.json')
load_dic = json.load(f)

dic = {}

unique = set()


for ind in load_dic:
    lis = []
    hdline_punc = word_tokenize(load_dic[ind][0].lower())
    # hdline_no_punc = [word for word in hdline_punc if word.isalnum()]
    lis.append(' '.join(stem(hdline_punc)))

    short_punc = word_tokenize(load_dic[ind][2].lower())
    # short_no_punc = [word for word in short_punc if word.isalnum()]
    lis.append(' '.join(stem(short_punc)))
    dic[ind] = lis
    if int(ind)%1000==0:
    	print(ind)

f.close()

with open('data_tkn.json', 'w') as write_file:
    json.dump(dic, write_file)

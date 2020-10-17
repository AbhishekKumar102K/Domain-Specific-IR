import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
import json
import math
import operator
import time

def stem(a):
	p = PorterStemmer()
	a = [p.stem(word) for word in a]
	return a
query = input()
st_time = time.time()
query_tokn = word_tokenize(query)
query_tokn = [word for word in query_tokn if word.isalnum()]

query_stemmed = (stem(query_tokn))

tf_raw_query = {}
for word in query_stemmed:
	if word not in tf_raw_query.keys():
		tf_raw_query[word] = 1
	else:
		tf_raw_query[word] += 1

for word in tf_raw_query.keys():
	tf_raw_query[word] = 1 + math.log10(tf_raw_query[word])


f = open('headline_inverted_index2.json','r')
hd_inv_index = json.load(f)


N = 200853
wt = {}
wt_sumsq = 0.00000

for word in tf_raw_query.keys():
	if word in hd_inv_index.keys(): 
		wt[word] = tf_raw_query[word] * (math.log10(N/(hd_inv_index[word])))
		wt_sumsq += wt[word]*wt[word]
	else:
		wt[word] = 0


wt_sumsq = wt_sumsq**0.5

for word in tf_raw_query.keys():
	wt[word] /= max(0.000001,wt_sumsq)


f2 = open('desc_inverted_index2.json','r')
desc_inv_index = json.load(f2)


wt_desc = {}
wt_desc_sumsq = 0.00000

for word in tf_raw_query.keys():
	if word in desc_inv_index.keys(): 
		wt_desc[word] = tf_raw_query[word] * (math.log10(N/(desc_inv_index[word])))
		wt_desc_sumsq += wt_desc[word]*wt_desc[word]
	else:
		wt_desc[word] = 0


wt_desc_sumsq = wt_desc_sumsq**0.5

for word in tf_raw_query.keys():
	wt_desc[word] /= max(0.000001,wt_desc_sumsq)


#document
f.close()
f2.close()

f = open('headline_inverted_index.json','r')
hd_inv_index = json.load(f)

f2 = open('desc_inverted_index.json','r')
desc_inv_index = json.load(f2)

f3 = open('doc_lengths.json','r')
doc_len = json.load(f3)

scores = {}

for i in range(1,N+1):
	doc_wt = {}

	for word in tf_raw_query.keys():
		if word in hd_inv_index.keys():
			if str(i) in hd_inv_index[word].keys():
				doc_wt[word] = 1+math.log10(hd_inv_index[word][str(i)])
			else:
				doc_wt[word] = 0

	sum_score_hd = 0
	for word in doc_wt.keys():
		doc_wt[word] /= doc_len[str(i)][0]
		doc_wt[word] *= wt[word]
		sum_score_hd += doc_wt[word]


	doc_wt = {}
	for word in tf_raw_query.keys():
		if word in desc_inv_index.keys():
			if str(i) in desc_inv_index[word].keys():
				doc_wt[word] = 1+math.log10(desc_inv_index[word][str(i)])
			else:
				doc_wt[word] = 0

	sum_score_desc = 0
	for word in doc_wt.keys():
		doc_wt[word] /= doc_len[str(i)][1]
		doc_wt[word] *= wt_desc[word]
		sum_score_desc += doc_wt[word]


	final_score = (3*sum_score_hd + sum_score_desc)/4.0 

	scores[str(i)] = final_score

sorted_d = dict(sorted(scores.items(), key=operator.itemgetter(1),reverse=True))

i = 0
f4 = open('data_before_tkn.json','r')
data = json.load(f4)


for no in sorted_d.keys():
	print(data[no][0])
	print(data[no][1])
	print('')

	i+=1
	if i==10:
		break

en_time = time.time()

print(en_time - st_time)



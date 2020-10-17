import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
import json
import math
import time
import operator


"""
	DESCRIPTION:
		Generates search results for a user query from the selected data set
	
	Methods:
		stem(): Calls the PorterStemmer function which implements the stemming operation on the query
	
	Inputs:
		hd_inv_index 	: Inverted index of headlines
		desc_inv_index 	: Inverted index of short description
		doc_lengths		: Normalized doc lengths of all the docs

	Variables:
		tf_wt_query 		: For storing Tf-wt for each term in the query
		N 					: Number of documents
		wt_headline 		: To store the weight (wt) of each term in the query for headlines
		wt_headline_sumsq 	: To store the sum of squares of wt of unique terms in the query for headlines
		wt_desc 			: To store the weight (wt) of each term in the query for short description
		wt_desc_sumsq		: To store the sum of squares of wt of unique terms in the query for short description
		scores 				: Dictionary to store the final score of each document
		sorted_scores		: Sort scores in decreasing order of final_scores

"""
def stem(a):
	p = PorterStemmer()
	a = [p.stem(word) for word in a]
	return a


query = input('Enter search query: ')
print("")

start_time = time.time()
query_tokn = word_tokenize(query.lower())		#Tokenization of the query
		
query_stemmed = (stem(query_tokn))				#Stemming of the query



#For storing Tf-wt for each term in the query
tf_wt_query = {}

#Traversing through the query list
for word in query_stemmed:

	#Initialize tf_raw of term as 1 if term not encountered before
	if word not in tf_wt_query.keys():
		tf_wt_query[word] = 1

	#Increasing the value of tf_raw of term by 1 
	else:
		tf_wt_query[word] += 1

#Calculating the tf-wt of each term in the query by taking the logarithm
for word in tf_wt_query.keys():
	tf_wt_query[word] = 1 + math.log10(tf_wt_query[word])



#Loading the necessary json files
hd_inv_index = json.load(open('headline_inverted_index.json','r'))	

desc_inv_index = json.load(open('desc_inverted_index.json','r'))

doc_len = json.load(open('doc_lengths.json','r'))



N = len(doc_len)


#To store the weight (wt) of each term in the query for headlines
wt_headline = {}

#To store the sum of squares of wt of unique terms in the query for headlines
wt_headline_sumsq = 0.00000


#Traversing through unique words in the query
for word in tf_wt_query.keys():

	# If term is present in any headline, compute wt for the term, given by, wt = tf * idf.
	# tf = tf_wt_query[word]
	# idf = log10( N / doc_len(headlines))))
	if word in hd_inv_index.keys(): 
		wt_headline[word] = tf_wt_query[word] * (math.log10(N/(len(hd_inv_index[word]))))
		wt_headline_sumsq += wt_headline[word]**2	#calculate sum of squares of wt values for each term

	# If term is not present in any headline, wt = 0 
	else:
		wt_headline[word] = 0


# Taking square root of sum of squares
wt_headline_sumsq = wt_headline_sumsq**0.5

# Normalizing the wt values and thus calculating the tf-idf values for headline
for word in tf_wt_query.keys():
	wt_headline[word] /= max(0.000001,wt_headline_sumsq) 	#To avoid division by zero eroor




'''
	CALCULATING tf-idf values w.r.t short description
'''

#To store the weight (wt) of each term in the query for short description
wt_desc = {}

#To store the sum of squares of wt of unique terms in the query for short description
wt_desc_sumsq = 0.00000

#Traversing through unique words in the query
for word in tf_wt_query.keys():

	# If term is present in any short description, compute wt for the term, given by, wt = tf * idf.
	# tf = tf_wt_query[word]
	# idf = log10( N / doc_len(short_desc)))
	if word in desc_inv_index.keys(): 
		wt_desc[word] = tf_wt_query[word] * (math.log10(N/(len(desc_inv_index[word]))))
		wt_desc_sumsq += wt_desc[word]*wt_desc[word]
	
	# If term is not present in any headline, wt = 0
	else:
		wt_desc[word] = 0


# Taking square root of sum of squares
wt_desc_sumsq = wt_desc_sumsq**0.5

# Normalizing the wt values and thus calculating the tf-idf values for short description
for word in tf_wt_query.keys():
	wt_desc[word] /= max(0.000001,wt_desc_sumsq)



#Dictionary to store the final score of each document
scores = {}

#Traverse through each document
for i in range(1,N+1):

	#To store the doc-wt value of the current headline
	doc_wt = {}

	#Traverse through unique words in the query
	for word in tf_wt_query.keys():

		# If term is present in any headline, compute doc-wt for the term, given by, 1 + log10(idf)
		if word in hd_inv_index.keys():

			#If term is present in the current headline, assign doc-wt = 1 + log10(idf)
			if str(i) in hd_inv_index[word].keys():
				doc_wt[word] = 1+math.log10(hd_inv_index[word][str(i)])

			#If term is not present in the current headline, doc-wt = 0
			else:
				doc_wt[word] = 0

	# Score of the document contributed by headline
	sum_score_hd = 0
	for word in doc_wt.keys():
		doc_wt[word] /= doc_len[str(i)][0]
		doc_wt[word] *= wt_headline[word]
		sum_score_hd += doc_wt[word]



	#To store the doc-wt value of the current short description
	doc_wt = {}

	#Traverse through unique words in the query
	for word in tf_wt_query.keys():

		# If term is present in any short desc, compute doc-wt for the term, given by, 1 + log10(idf)
		if word in desc_inv_index.keys():

			#If term is present in the current short desc, assign doc-wt = 1 + log10(idf)
			if str(i) in desc_inv_index[word].keys():
				doc_wt[word] = 1+math.log10(desc_inv_index[word][str(i)])

			#If term is not present in the current short desc, doc-wt = 0
			else:
				doc_wt[word] = 0


	# Score of the document contributed by short description
	sum_score_desc = 0
	for word in doc_wt.keys():
		doc_wt[word] /= doc_len[str(i)][1]
		doc_wt[word] *= wt_desc[word]
		sum_score_desc += doc_wt[word]


	# Weighted average of headline and short description scores with weights as 3:1
	final_score = (3*sum_score_hd + sum_score_desc)/4.0 

	#Append score of the document to dictionary of scores
	scores[str(i)] = final_score

# Sort the scores in decreasing order of final_score
sorted_scores = dict(sorted(scores.items(), key=operator.itemgetter(1),reverse=True))

#To keep track of number of results shown
result_no = 0

#Loading the cleaned data to display the headline and the link
data = json.load(open('data.json','r'))

#To give top 10 results from the sorted scores
for no in sorted_scores:

	#If no more results match the query
	if sorted_scores[no]==0:
		if result_no==0:
			print("No results found")
		else:
			print("No more results to show")
		break

	print(data[no][0])  	#Display the headline of the result doc
	print(data[no][1])		#Display the link to the result doc
	print('')

	result_no+=1					
	if result_no==10:		#If 10 results have been shown
		break

end_time = time.time()
print("Time taken for search :", '%.3f'%(end_time-start_time),"seconds")


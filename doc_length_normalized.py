import json
import math


"""
	DESCRIPTION:
		Finds the sum of squares of the logarithm of frequency of all 
		the terms in the document and then takes the square root of the value	
	
	Inputs:
		data_tkn.json : json file containing the tokenized and stemmed data

	Variables:
		N 		: Total number of documents
		doc_len : Dictionary containing the sum of squares of headlines and short description lengths 
				  for each news 

"""



#loading the tokenized and stemmed data
json_data = open('data_tkn.json','r')
data = json.load(json_data)

N = len(data)					
doc_len = {}

#For each doc id
for i in range(1,N+1):
	hdline = data[str(i)][0]	#current headline
	desc = data[str(i)][1]		#current short description

	doc_hd = {}					#Contains frequency of every word in the current headline
	doc_desc = {}				#Contains frequency of every word in the current short description
	
	#Traversing through each word in the current headline
	for word in hdline.split():

		#Initializing the term frequency as 1 for the current headline
		if not word in doc_hd.keys():
			doc_hd[word] = 1

		#Increasing the frequency of the term for current headline
		else:
			doc_hd[word] += 1


	#Traversing through each word in the current short description
	for word in desc.split():

		#Initializing the term frequency as 1 for the current short description
		if word in doc_desc.keys():
			doc_desc[word] += 1

		#Increasing the frequency of the term for current short description
		else:
			doc_desc[word] = 1


	sq_sum_headline = 0.0000		#to keep track of sum of squares of logs of headline lengths
	sq_sum_desc = 0.0000			#to keep track of sum of squares of logs of short description lenghts


	#Traversing through the terms in the current headline and computing sum of squares of logs
	for word in doc_hd.keys():
		sq_sum_headline += (math.log10(doc_hd[word])+1)**2

	#Traversing through the terms in the current short description and computing sum of squares of logs
	for word in doc_desc.keys():
		sq_sum_desc += (math.log10(doc_desc[word])+1)**2


	temp = []									#List containing square roots of sq_sum_headline and sq_sum_desc
	temp.append(max(0.000001,sq_sum_headline**0.5))		#To avoid division by zero error in case sq_sum_headline is 0
	temp.append(max(0.000001,sq_sum_desc**0.5))		#To avoid division by zero error in case sq_sum_desc is 0

	doc_len[str(i)] = temp						#Append temp to doc_len dictionary 


#Dumping the resultant doc_len dictionary into a json file
with open('doc_lengths.json', 'w') as write_file:
	json.dump(doc_len, write_file)

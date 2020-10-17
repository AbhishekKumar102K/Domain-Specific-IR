import json

"""
	DESCRIPTION:
		Creation of inverted index for all the distinct terms

	Inputs:
		data_tkn.json : json file containing the tokenized and stemmed data

	Variables:
		inv_index_headlines : Dictionary for constructing the inverted index of each term 
		inv_index_desc		: Dictionary for constructing the inverted index of each term 
		
		data 				: Loaded json object 
		
"""

#loading the tokenized and stemmed data
json_data = open('data_tkn.json')
data = json.load(json_data)

inv_index_headline = {}				

#Traversing through each news 
for news_no in data:
	headline = data[news_no][0]			#index 0 in the list contains the headline

	#Traversing through each word in the headline
	for word in headline.split():		

		#if the term doesn't already exist in the headlines inverted index
		if word not in inv_index_headline.keys():
			inv_index_headline[word] = {}
			inv_index_headline[word][int(news_no)] = 1		#Initialize term frequency as 1 for key: news_no
			continue

		#if the term has not appeared in the current headline before
		if int(news_no) not in inv_index_headline[word].keys():	
			inv_index_headline[word][int(news_no)] = 1
		#Increasing the count of the term frequency for the current headline
		else:
			inv_index_headline[word][int(news_no)] += 1


#Dumping the resultant dictionary into a json file
with open('headline_inverted_index.json', 'w') as write_file:
	json.dump(inv_index_headline, write_file)


inv_index_desc = {}				

#Traversing through each news 
for news_no in data:
	short_desc = data[news_no][1]			#index 1 in the list contains the short description

	#Traversing through each word in the short description
	for word in short_desc.split():		

		#if the term doesn't already exist in the short description inverted index
		if word not in inv_index_desc.keys():
			inv_index_desc[word] = {}
			inv_index_desc[word][int(news_no)] = 1		#Initialize term frequency as 1 for key: news_no
			continue

		#if the term has not appeared in the current short description before
		if int(news_no) not in inv_index_desc[word].keys():	
			inv_index_desc[word][int(news_no)] = 1
		#Increasing the count of the term frequency for the current short description
		else:
			inv_index_desc[word][int(news_no)] += 1


#Dumping the resultant dictionary into a json file
with open('desc_inverted_index.json', 'w') as write_file:
	json.dump(inv_index_desc, write_file)

import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *

"""
	DESCRIPTION:
		Used for Tokenizing and Stemming the cleaned data

	Inputs:
		data.json : json file containing the cleaned data

	Methods:
		stem(): Calling the PorterStemmer function which implements the stemming operation on the headlines
				and short descriptions

	Variables:
		news: Dictionary containing the tokenized and stemmed form of the data. 

"""

#implements the Porter Stemmer algorithm and returns the stemmed doc
def stem(doc):
	p = PorterStemmer()
	
	'''
	Traversing through each word in the list and stemming it
	into another list

	'''
	doc = [p.stem(word) for word in doc]  

	return doc

#loading the cleaned data
json_data = open('data.json')

data = json.load(json_data)

news = {}

for news_no in data:

	cur_news = []

	#Tokenizing the headline and short description
	headline = word_tokenize(data[news_no][0].lower())
	short_desc = word_tokenize(data[news_no][2].lower())

	#headline and short_desc will be Lists containing the tokenized forms of the headline and short description 
	#of the current news

	#Stemming the headline and short description
	cur_news.append(' '.join(stem(headline)))
	cur_news.append(' '.join(stem(short_desc)))
	
	news[news_no] = cur_news

json_data.close()


#Dumping the resultant dictionary into a json file
with open('data_tkn.json', 'w') as write_file:
	json.dump(news, write_file)
import json

"""
DESCRIPTION:
    Cleans the JSON file into a file containing the data we needed

    news          : Dictionary containing headline, link and short description 
    news_no       : Assigning distinct numbers to the news

    As its input, the code takes the raw_data file containing all the headlines:

"""

news = {}     
news_no = 0

for row in open('raw_data.json', 'r'):
    cur_news = json.loads(row)
    news_no += 1
    
    topics = [] #List of headline, link and short description of the current news
    topics.append(cur_news["headline"])
    topics.append(cur_news['link'])
    topics.append(cur_news['short_description'])

    news[news_no] = topics

#Dumping the resultant dictionary into a json file
with open('data.json', 'w') as write_file:
    json.dump(news, write_file)

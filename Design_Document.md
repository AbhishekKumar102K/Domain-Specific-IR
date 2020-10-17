# Design Document

**Note** - All the JSON data files are available at https://drive.google.com/drive/folders/1Wnx3h5e1U0rXXuNlewIQPaCA8zBskJJX?usp=sharing.

Raw data was taken from https://www.kaggle.com/rmisra/news-category-dataset. 

**clean.py** - The JSON file which we downloaded had more information than we needed. So first, we had to clean the JSON file into a file containing only the data we needed and modify it. We also assigned distinct numbers for all headlines. The clean data then will be used for further processing. 
The new JSON file is data.json and the raw data file was raw_data.json. The JSON file is a dictionary with the indices as the key and the values are headline, link and short description for each news. 
This took around 3.3 seconds and and now the data is pre processed for all queries.

**tokn.py** - In this file, we're applying stemming and tokenization to our data. Similar to our previous approach, we'll be having a dictionary for all the data with keys as the news number and value as a list of headline and short description which has undergone tokenization and stemming. 
From the nltk package, we're using the word_tokenize function to tokenize our headlines and short description for all the news. Porter Stemmer from the nltk package is used for stemming the data and then it is stored into the dictionary and finally converted into a new file called data_tkn.json. 
This took around 155 seconds and now the data is pre processed for all queries. The time taken is large because this is processing more than 400 thousand lines and tokenizing and stemming them.

**inverted_ind.py** - The data which is tokenized and stemmed, will now be used to create the index for all the distinct terms. To do that, we'll be creating a new dictionary for terms with the key as the term and the value is also a dictonary in which the keys are the index given to each document and the corresponding frequency in that document. 
This process is done for both headlines and short description and the corresponding data will be stored into two different files. headline_inverted_index.json will be used for headlines indices and desc_inverted_index.json will be used for description indices.
This will be used to calculate the tf-idf values. 
This took around 27 seconds and now the data is pre processed for all queries.

**doc_length_normalized.py** - We can preprocess the normalized length of the all the documents as it will not change between queries. To do so, we're just finding the sum of squares of the logarithm of frequency of all the terms in the document and then taking the square root of the value. 
For each document, we'll have two values, one for headline and one for decription. We're storing it in another json file named doc_lengths.json as a dictionary with key as the document number and value as a list of the heading value and description value.
This took around 5.5 seconds to run and the data can also be used for all queries.

**query.py** - This is the main file which the end user has to run.
First, it will use tokenization and stemming to normalize the query which the user inputs and converts it to a list of the words in the query.
Then to calculate the tf-idf value of the query, first we calculate the raw frequency and weighted frequency of every term in the search query. Then using document frequency, we calculate the idf value to calculate the tf-idf value and then normalize it.
Similarly, for the documents, we take the tf-raw value which is precalculated for each term in our search query and calculate the weighted tf value. Then using the document lengths, we calculate the tf-idf values for each document for each term and multiply it with the corresponding tf-idf value of the terms.
We have both headings and short description in our documents, we calculate tf-idf values of both the headings and short descriptions, we take the weighted average of both of them with weights as 3:1 and then calculate the final score of each document for the query.
After sorting the scores of all the documents, we're rerieving the top 10 documents and then printing or showing a prompt if no or less than 10 documents show any similarity with the query and printing the required time for the whole query.
On an average, a query takes 4 to 5 seconds for each query, but it will depend on the search query.

Sample queries are given in sample_queries.md
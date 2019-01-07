from nltk.corpus import stopwords
import nltk
from collections import Counter
import json
import requests
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize,word_tokenize
ps=PorterStemmer()
nltk.download('stopwords')
def token(ans):
    stop_words = set(stopwords.words('english'))
    file1 = open("sample.txt")
    line = file1.read()# Use this to read file content as a stream:
    words = ans.split()
    document_without_stopwords=[]
    for r in words:
        if not r in stop_words:
            document_without_stopwords.append(r)
    count_frequency= Counter(document_without_stopwords)

    dictionary_words=[]
    with open('dictionary_of_legal_terms.json') as f:
        reader = json.load(f)
    count_relevant_words=0
    total_frequent_words=0
    print("Loading")
    for i in range(int(len(count_frequency))):
        total_frequent_words+=count_frequency.most_common()[i][1]
        if reader.get(ps.stem(count_frequency.most_common()[i][0].lower())):

            count_relevant_words=count_relevant_words+int(count_frequency.most_common()[i][1])
    print(count_relevant_words/total_frequent_words)
    return count_relevant_words/total_frequent_words

        
        



import requests
from bs4 import BeautifulSoup, SoupStrainer
import urllib3
from urllib import parse
import numpy as np
import re
import pandas as pd
import relevance
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn import metrics


def getDocuments(start,end):
    output = open("results.csv", "w+")
    i = start
    save_documents = np.array([])
    target_data=[]
    while (i < end):

        search_query = list.loc[i][0]
        url = "http://www.google.com/search?q=" + parse.quote(search_query)
        url_pool_manager = urllib3.PoolManager()
        search_response = url_pool_manager.request("GET", url)
        search_response_DOM = BeautifulSoup(search_response.data, features='lxml')
        # print(soup)
        cite_ids = search_response_DOM.find_all("cite")

        # print(soup_ids)

        # Skip PDF files and select first non-pdf file in results page.
        for cite_id in cite_ids:
            print(search_query)
            print(cite_id)

            last_segment = str(cite_id.decode_contents()).split(".")[-1]
            # print(segment)
            if last_segment != "pdf":
                break
            if str(cite_id).find("books.google"):
                continue


        # print(soup_id)
        # get the anchor
        if cite_id is None:
            output.write(search_query + "," + str(match) + ",N/A,NOT LEGAL\n")
            end += 1
            i+=1
            continue

        anchor_element_cite_id = cite_id.parent.parent.parent
        if anchor_element_cite_id is None:
            output.write(search_query + "," + str(match) + ",N/A,NOT LEGAL\n")
            end += 1
            i += 1
            continue

        anchor_url = anchor_element_cite_id.find('a')['href']
        target_url = anchor_url.split('=')[1]
        target_url = target_url.split('&')[0]
        print(target_url)

        # call target url
        try:
            response = url_pool_manager.request("GET", target_url)
        except requests.exceptions.ConnectionError:
            output.write(search_query + "," + str(search_query) + ",N/A,NOT LEGAL\n")
            end += 1
            i += 1
            continue

        if response.status != 200:
            output.write(search_query + "," + str(search_query) + ",N/A,NOT LEGAL\n")
            end += 1
            i += 1
            continue

        bodysoup = BeautifulSoup(response.data, 'lxml')

        data = bodysoup.findAll(text=True)

        # print(data)
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            return True

        result = filter(visible, data)

        # print(result)

        ans = ""
        for element in result:
            ans += element
        # print(ans)
        save_documents=np.append(save_documents,ans)
        match = relevance.token(ans)
        if match > 0.25:
            target_data.append(1)
            output.write(search_query + "," + str(match) + "," + target_url + ",LEGAL\n")
        else:
            target_data.append(0)
            output.write(search_query + "," + str(match) + ",N/A,NOT LEGAL\n")
        i += 1
    output.close()
    return save_documents, target_data

# target_set=np.array([1,0,0,1,1,1,1,1,1,1])#,0,0,1,1,1,0,1,0,1,1]
# test_target=np.array([1,0,1,0,0])#1,0,0,1,1,1,0,1,0,1,1]
# # target_set=[0,0]
# # test_target=[1,1]
# print(len(target_set))
list=pd.read_csv("Bad_Citation_Searches.csv",delimiter=",", encoding="UTF-8", error_bad_lines=False)
#
#
# count_vect = CountVectorizer()
# X_train_counts = count_vect.fit_transform(getDocuments(0,10))
# X_train_counts.shape
#
#
# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# X_train_tfidf.shape
# print(X_train_tfidf.shape)
#
# clf = MultinomialNB().fit(X_train_tfidf, target_set)
#
# print("Starting test data analysis")
# #testing
# test_documents=getDocuments(10,15)
# print(len(test_documents))
#
# predicted=clf.predict(test_documents)
# mean=np.mean(predicted == test_target)
# print(predicted)
#
# #
# # X_test_counts=count_vect.transform(test_documents)
# # X_test_tfidf=tfidf_transformer.transform(X_test_counts)
# #
# # print("End of tfidf")
# # print(X_test_tfidf)
# #
# # predicted=clf.predict(X_test_tfidf)
# # for a,b in zip(test_documents,predicted):
# #     print(target_set[b])
#
# print(metrics.classification_report(test_target, predicted,target_names=["LEGAL","NOT LEGAL"]))
#
#
#
#
#





import pandas as pd
from bs4 import BeautifulSoup
import simplejson
import  urllib3
import requests
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize,word_tokenize

#Build Dictionary of Legal Terms

#Google search API Key: AIzaSyB7drVoOEtw21-m_uNyh-p-BHmvKTbljBo

file=open("dictionary_of_legal_terms.json","w+")

url="http://www.uscourts.gov/glossary"
response=requests.get(url)
soup=BeautifulSoup(response.content,"lxml")
list_of_dt=soup.findAll("dt")
list_of_dd=soup.findAll("dd")

# print(list_of_dd[0].p.text)
print(list_of_dt[0].a["id"])
dict=""
ps=PorterStemmer()
json_data={}
for i in range(len(list_of_dd)):
    if "In_forma_pauperis"!=str(list_of_dt[i].a["id"]).strip().replace("\n","").replace(";",""):

        json_data[ps.stem(str(list_of_dt[i].a["id"]).strip().replace("\n","").replace(";",",").lower())] =str(list_of_dd[i].p.text).strip().replace(";",",")
        dict=simplejson.dumps(json_data)
for i in range(ord('A'),ord('Z'),1):
    url = "https://dictionary.law.com/Default.aspx?letter="+chr(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    words=soup.findAll("span", "word")
    for i in range(len(words)):
        json_data[ps.stem(str(words[i].a.text.strip()).replace("\n","").lower())]="test"
        dict = simplejson.dumps(json_data)
print(simplejson.dumps(dict,indent=4))

file.write(dict)
file.close()

# coding: utf-8

# In[1]:

from google_search import getDocuments
import numpy as np
# Loading the data set - training data.

train_data, train_target = getDocuments(0,10)


# In[4]:

# You can check the target names (categories) and some data files by following commands.
# train_target=np.array([1,0,0,1,1,1,1,1,1,1])  # prints all the categories

# In[5]:

print("\n".join(train_data[0].split("\n")[:3]))  # prints first line of the first data file

# In[6]:

# Extracting features from text files
from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train_data)
X_train_counts.shape

# In[7]:

# TF-IDF
from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape

# In[9]:

# Machine Learning
# Training Naive Bayes (NB) classifier on training data.
from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB().fit(X_train_tfidf, train_target)

# In[14]:

# Building a pipeline: We can write less code and do all of the above, by building a pipeline as follows:
# The names ‘vect’ , ‘tfidf’ and ‘clf’ are arbitrary but will be used later.
# We will be using the 'text_clf' going forward.
from sklearn.pipeline import Pipeline

text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])

text_clf = text_clf.fit(train_data, train_target)

# In[15]:

# Performance of NB Classifier
import numpy as np

twenty_test, test_target = getDocuments(10,15)
predicted = text_clf.predict(twenty_test)
np.mean(predicted == test_target)

# In[16]:

# Training NB and calculating its performance


text_clf_svm = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB())])

text_clf_svm = text_clf_svm.fit(train_data, train_target)
predicted_svm = text_clf_svm.predict(twenty_test)
print(np.mean(predicted_svm == test_target))


# In[18]:

from sklearn.model_selection import GridSearchCV
from sklearn import metrics

parameters = {'vect__ngram_range': [(1, 1), (1, 2)], 'tfidf__use_idf': (True, False), 'clf__alpha': (1e-2, 1e-3)}

# In[19]:

# Next, we create an instance of the grid search by passing the classifier, parameters
# and n_jobs=-1 which tells to use multiple cores from user machine.

gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(train_data, train_target)
print(gs_clf.cv_results_.keys())

# In[23]:

# To see the best mean score and the params, run the following code

print(gs_clf.best_score_)
print(gs_clf.best_params_)

from sklearn.metrics import classification_report

print('Best score: %0.3f' % gs_clf.best_score_)
print('Best parameters set:')
best_parameters = gs_clf.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print('\t%s: %r' % (param_name, best_parameters[param_name]))

predictions = gs_clf.predict(twenty_test)
print(classification_report(test_target, predictions))

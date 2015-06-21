'''
This can be used to establish naive bayes model. The input is a directory('Complete Dataset' by default) which contains csv files of tweets with specified user id. The directory must in parents directory of this python file(as we hand in). If you want to remove stopwords, please include a txt file named stopwords_en.txt in the current directory. The output is 5 results(we use 5-fold) of system accuracy, classification reports(precision, recall and f1-score of each label) and confusion matrix(can be used to analyze).
'''
import IPython
import sklearn as sk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import re
import csv
import os
from sklearn.cross_validation import cross_val_score, KFold
from sklearn import cross_validation
from scipy.stats import sem
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer
from sklearn import metrics

def evaluate_cross_validation(clf, X, y, K):
    scores = cross_validation.StratifiedKFold(y, n_folds = 5) #use cross validation
    for tr, te in scores:
        xtr = [X[i] for i in tr] #training set
        ytr = [y[i] for i in tr] #training label
        xte = [X[i] for i in te] #test set
        yte = [y[i] for i in te] #test label
        train_and_evaluate(clf, xtr, xte, ytr, yte)

def get_stop_words(): #get stopwords
    result = set()
    for line in open('stopwords_en.txt', 'r').readlines():
        result.add(line.strip())
    return result

def train_and_evaluate(clf, X_train, X_test, y_train, y_test):
    
    clf.fit(X_train, y_train) #fit data
    
    y_pred = clf.predict(X_test) #y_pred is predicted label
    
    print "Accuracy on training set:"
    print clf.score(X_train, y_train)
    print "Accuracy on testing set:"
    print clf.score(X_test, y_test)
    

    print "Classification Report:"
    print metrics.classification_report(y_test, y_pred)
    print "Confusion Matrix:"
    print metrics.confusion_matrix(y_test, y_pred)


def read_data(dir, data, label_number):
    data_file_name = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    count = 0
    for item in data_file_name:
        if 'DS' in item:
            continue
        data_file_name_split = re.split('\.', item)
        userid = data_file_name_split[0]
        label = data_file_name_split[1]
        data_file = open(dir+item, 'r')
        #file_name.append(dir+item)
        data_ob = csv.reader(data_file)
        data_per_sample = ''
        for  data_item in data_ob:
            data_per_sample = data_per_sample + data_item[0] + ' '

        data.append(data_per_sample)
        label_number.append(car_brands[label])
        data_file.close()

###for train/test data
car_brands = {'bmw': 0, 'honda': 1, 'jeep': 2, 'audi': 3, 'ford': 4, 'hyundai': 5, 'kia': 6, 'lexus': 7, 'mazda': 8, 'nissan': 9, 'toyota': 10, 'ferrari': 11} #map from car branch to number

data = [] #one entry is all cascaded tweets of a user
label_number = [] #label(number instead of car branch) for each entry in data
#file_name = []
read_data('../Complete Datasets/', data, label_number) #read whole dataset
X = data
y = label_number

stopwords = get_stop_words()

clf_1 = Pipeline([                
    ('vect', CountVectorizer()),  #use CountVectorizer() as tokenizer
    ('clf', MultinomialNB()),
])
clf_2 = Pipeline([
    ('vect', HashingVectorizer(non_negative=True)),  #use HashVectorizer() as tokenizer
    ('clf', MultinomialNB()),
])
clf_3 = Pipeline([
    ('vect', TfidfVectorizer()),  #user tfidf as tokenizer
    ('clf', MultinomialNB()),
])
clf_4 = Pipeline([                #remove stopwords, and use tfidf as toknizer
    ('vect', TfidfVectorizer(  
                stop_words = stopwords,
                token_pattern=ur"\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b",
    )),
    ('clf', MultinomialNB(alpha=0.01)),
])
evaluate_cross_validation(clf_4, X, y, 5); 

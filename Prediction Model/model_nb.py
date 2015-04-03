import IPython
import sklearn as sk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import re
import csv
import os
from sklearn.cross_validation import cross_val_score, KFold
from scipy.stats import sem
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer
from sklearn import metrics

def evaluate_cross_validation(clf, X, y, K):
    # create a k-fold croos validation iterator of k=5 folds
    cv = KFold(len(y), K, shuffle=True, random_state=0)
    # by default the score used is the one returned by score method of the estimator (accuracy)
    scores = cross_val_score(clf, X, y, cv=cv)
    print scores
    print ("Mean score: {0:.3f} (+/-{1:.3f})").format(
        np.mean(scores), sem(scores))

def get_stop_words():
    result = set()
    for line in open('data/stopwords_en.txt', 'r').readlines():
        result.add(line.strip())
    return result

def train_and_evaluate(clf, X_train, X_test, y_train, y_test):
    
    clf.fit(X_train, y_train)
    
    print "Accuracy on training set:"
    print clf.score(X_train, y_train)
    print "Accuracy on testing set:"
    print clf.score(X_test, y_test)
    
    y_pred = clf.predict(X_test)
    #print y_pred
    
    print "Classification Report:"
    print metrics.classification_report(y_test, y_pred)
    print "Confusion Matrix:"
    print metrics.confusion_matrix(y_test, y_pred)


def read_data(dir, data, label_number, file_name):
#def read_data(dir):
    data_file_name = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    count = 0
    for item in data_file_name:
        if 'DS' in item:
            continue
        data_file_name_split = re.split('\.', item)
        userid = data_file_name_split[0]
        label = data_file_name_split[1]
        '''
        #only for split data
        if label not in label_name:
            label_name.append(label)
            label_name_dic[label] = count
            count += 1
        ####
        '''
        data_file = open(dir+item, 'r')
        file_name.append(dir+item)
        data_ob = csv.reader(data_file)
        data_per_sample = ''
        for  data_item in data_ob:
            data_per_sample = data_per_sample + data_item[0] + ' '

        data.append(data_per_sample)
        #label_number.append(label_name_dic[label])
        label_number.append(car_brands[label])
        data_file.close()
'''
#only for split data
data = []
label_number = []
file_name = []
label_name = []
label_name_dic = {}

read_data('samples/')

SPLIT_PERC = 0.5
split_size = int(len(data)*SPLIT_PERC)
X_train = data[:split_size]
X_test = data[split_size:]
y_train = label_number[:split_size]
y_test = label_number[split_size:]
###
'''

###for train/test data
car_brands = {'bmw': 0, 'honda': 1, 'jeep': 2, 'audi': 3, 'ford': 4, 'hyundai': 5, 'kia': 6, 'lexus': 7, 'mazda': 8, 'nissan': 9, 'toyota': 10, 'ferrari': 11}

tr_data = []
tr_label_number = []
tr_file_name = []

read_data('train/', tr_data, tr_label_number, tr_file_name)

X_train = tr_data
y_train = tr_label_number
train_label_name = tr_label_number

te_data = []
te_label_number = []
te_file_name = []

read_data('test/', te_data, te_label_number, te_file_name)
X_test = te_data
y_test = te_label_number
test_label_name = te_label_number
###

stopwords = get_stop_words()

clf_1 = Pipeline([
    ('vect', CountVectorizer()),
    ('clf', MultinomialNB()),
])
clf_2 = Pipeline([
    ('vect', HashingVectorizer(non_negative=True)),
    ('clf', MultinomialNB()),
])
clf_3 = Pipeline([
    ('vect', TfidfVectorizer()),
    ('clf', MultinomialNB()),
])
clf_4 = Pipeline([
    ('vect', TfidfVectorizer(
                stop_words = stopwords,
                token_pattern=ur"\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b",
    )),
    ('clf', MultinomialNB(alpha=0.01)),
])
train_and_evaluate(clf_4, X_train, X_test, y_train, y_test)

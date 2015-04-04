from sklearn import tree
from sklearn.externals.six import StringIO
import pydot 
from sklearn.feature_extraction.text import TfidfTransformer
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


def read_data(dir, data, label_number, file_name):
    data_file_name = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    count = 0
    for item in data_file_name:
        if 'DS' in item:
            continue
        data_file_name_split = re.split('\.', item)
        userid = data_file_name_split[0]
        label = data_file_name_split[1]
        data_file = open(dir+item, 'r')
        file_name.append(dir+item)
        data_ob = csv.reader(data_file)
        data_per_sample = ''
        for  data_item in data_ob:
            data_per_sample = data_per_sample + data_item[0] + ' '

        data.append(data_per_sample)
        label_number.append(car_brands[label])
        data_file.close()


def train_and_evaluate(clf, X_train, X_test, y_train, y_test, i_fold):
    
    clf.fit(X_train, i_fold, y_train)
    
    print "Accuracy on training set:"
    print clf.score(X_train, y_train)
    print "Accuracy on testing set:"
    print clf.score(X_test, y_test)
    
    y_pred = clf.predict(X_test)
    
    print "Classification Report:"
    print metrics.classification_report(y_test, y_pred)
    print "Confusion Matrix:"
    print metrics.confusion_matrix(y_test, y_pred)


def evaluate_cross_validation(clf, X, y):
    scores = cross_validation.StratifiedKFold(y, n_folds = 5)
    i_fold = 1;
    for tr, te in scores:
        xtr = [X[i] for i in tr]
        ytr = [y[i] for i in tr]
        xte = [X[i] for i in te]
        yte = [y[i] for i in te]
        train_and_evaluate(clf, xtr, xte, ytr, yte, i_fold)
        i_fold += 1
        

data = []
label_number = []
file_name = []
dir = 'samples1/'
car_brands = {'bmw': 0, 'honda': 1, 'jeep': 2, 'audi': 3, 'ford': 4, 'hyundai': 5, 'kia': 6, 'lexus': 7, 'mazda': 8, 'nissan': 9, 'toyota': 10, 'ferrari': 11}


read_data(dir, data, label_number, file_name)


clf_3 = Pipeline([
    ('vect', TfidfVectorizer()),
    ('clf', tree.DecisionTreeClassifier()),
])

evaluate_cross_validation(clf_3, data, label_number)



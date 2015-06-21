'''
CODE DESCRIPTION

EFFECT: This function is going to implement the SVM for predict the car brand by uers' top 200 tweets
INPUT: The  documents folder which should contain 1181 documents for 1181 distinct Twitter users
OUTPUT: The classification report and confusion matrix for each result, because this project apply the cross validation, hence it will
        produce 5 result.
REQUIRE: This program use the function from scikit-learn, hence pre-install the sklearn is needed. Besides sklarn, we also apply
         tokenizer from cmu, hence the 'twokenize.py' should be included in the same path.
'''

import os
import csv
import numpy as np
import re
from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib
from sklearn import metrics
import twokenize

'''
EFFECT: This function is going to get the contend and label from the indexed documents, the index 
should be train_index or test_index
INPUT: index: the index of the documents that needed to be retrieved
       filenames: the list that contain all the documents name in the documents corpus folder
       file_label: the list that contain the car brand label of each documents
       file_folder: the name of the folder that contain all documents
OUTPUT: partial_file_corpus: the list that contain the contend of retrieved documents, 
        each element contain the whole contend of one document
        partial_file_label: the list contain the car brand label of the retrieved documents
'''
def get_corpus_and_label(index, filenames, file_label, file_folder):
    '''get the number of documents that needed to be retrieved'''
    doc_num = len(index)
    partial_file_corpus = []
    partial_file_label = np.zeros((doc_num), dtype = np.int)
    for ind in range(0, doc_num):
        '''get the car brand label of this document'''
        filename = filenames[index[ind]]
        partial_file_label[ind] = file_label[index[ind]]
        '''get the whole contend of this document'''
        open_file = open(file_folder + filename, 'r')
        open_file_csv = csv.reader(open_file)
        '''initial the data_per_sample, different tweets will be separated by blank space'''
        data_per_sample = ''
        for item in open_file_csv:
            data_per_sample = data_per_sample + item[0] + ' '
        partial_file_corpus.append(data_per_sample)
        open_file.close()
    return partial_file_corpus, partial_file_label

'''main function begin here'''
'''define the car brand dictionary'''
car_brands = {'bmw': 0, 'honda': 1, 'jeep': 2, 'audi': 3, 'ford': 4, 'hyundai': 5, 'kia': 6, 'lexus': 7, 'mazda': 8, 'nissan': 9, 'toyota': 10, 'ferrari': 11}

'''define the data path and get the file names of this folder'''
file_folder = "Complete Datasets/"
filenames = os.listdir(file_folder)

'''remove the DS_Store document'''
for filename in filenames:
    if "DS" in filename:
        filenames.remove(filename)

'''get the car brand labels of all documents'''
doc_num = len(filenames)
file_label = np.zeros((doc_num), dtype = np.int)
for ind in range(0, doc_num):
    filename = filenames[ind]
    file_name_split = re.split('\.', filename)
    #userid = file_name_split[0]
    '''car brand label is in the second place of the file_name_split'''
    label = file_name_split[1]
    file_label[ind] = car_brands[label]

'''divide the all documents into 5 folders'''
skf = cross_validation.StratifiedKFold(file_label, n_folds = 5)

'''test one folder, while other 4 folders are training folder'''
iter_num = 1;
for train_index, test_index in skf:
    #print("TRAIN:", train_index, "TEST:", test_index)
    '''get the train_corpus, train_label, test_corpus and test_label'''
    train_corpus, train_label = get_corpus_and_label(train_index, filenames, file_label, file_folder)
    test_corpus, test_label = get_corpus_and_label(test_index, filenames, file_label, file_folder)
    '''tokenize and vectorize the train corpus and test test corpus'''
    vectorize = TfidfVectorizer(encoding='ISO-8859-1', sublinear_tf = True, max_df = 0.5, stop_words = 'english')
    #vectorize = TfidfVectorizer(encoding='ISO-8859-1', sublinear_tf = True, max_df = 0.5, stop_words = 'english', tokenizer = twokenize.tokenizeRawTweetText)
    #release this will apply the tokenizer by CMU
    train_data = vectorize.fit_transform(train_corpus)
    test_data = vectorize.transform(test_corpus)
    

    '''release from here to training the data, just remove # from every line'''
    #'''begin to training the data'''
    #cPara_range = [1.0]
    #cPara_range = list(np.logspace(-2,2,10)) # release this annotation and kill the previous sentence to run grid search
    #parameters = {'C':cPara_range}
    #clf = svm.SVC(kernel = 'linear')
    #model_tunning = GridSearchCV(clf, param_grid = parameters)
    

    #'''save the model in svm_model folder'''
    #model_tunning.fit(train_data, train_label)
    #joblib.dump(model_tunning, 'svm_model/training_model_%d.pkl' %(iter_num))
    '''end for comment of training data'''
    
    '''load the model from svm_model folder'''
    model_tunning = joblib.load('svm_model/training_model_%d.pkl' %(iter_num)) 
    predict_labels = model_tunning.predict(test_data)

    print "Classification Report:"
    print metrics.classification_report(test_label, predict_labels)
    print "Confusion Matrix:"
    print metrics.confusion_matrix(test_label, predict_labels)

    print "Accuracy on training set:"
    print model_tunning.score(train_data, train_label)
    print "Accuracy on testing set:"
    print model_tunning.score(test_data, test_label)
    
    print 'finish test %d' %(iter_num)
    iter_num += 1








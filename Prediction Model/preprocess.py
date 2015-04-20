# name: Renhan Zhang
# unique name: rhzhang

import re
from PorterStemmer import PorterStemmer

def removeSGML(str):
    return re.sub('<.+?>', '', str)

def extract(l, pat, str, sub):
    l.extend(re.findall(pat,str))
    str = re.sub(pat, sub, str)
    return str

def tokenizeText(str):
    l = []
    # extract floating numbers -xxx.xxx
    pat = '[+-]?\d+\.\d+'
    str = extract(l, pat, str, '')

    #extract integer
    pat = '[\+\-]?\d+'
    str = extract(l, pat, str, '')

    # deal with U.S.A..
    str = re.sub('\.{2}', '.', str)

    #tokenization of '.'
    pat = '(?:\w+\.){2,}'
    str = extract(l, pat, str, '')


    #tokenization of 's, 're, 'm
    pat = '\'s'
    str = re.sub(pat, ' is', str)
    pat = '\'re'
    str = re.sub(pat, ' are', str)

    pat = '\'m'
    str = re.sub(pat, ' am', str)

    # tokenization of dates: 01/01/2014, 01.01.2014, 01-01-2014, 01 01 2014,
    pat = '(\d{2}/\d{2}/\d{4}) | (\d{2}.\d{2}.\d{4}) | (\d{2}-\d{2}-\d{4}) | (\d{2}\s\d{2}\s\d{4})  '
    str = extract(l, pat, str, '')

    # tokenization of '-'
    pat = '(?:\w+-)+\w+'
    str = extract(l, pat, str, '')


    # remove special char: ,  .  "  :  ;  '  ? ( ) / - ! \n
    str = re.sub(',|\.|"|:|;|\'|\?|\(|\)|\n|!', ' ', str)
    # extract normal words
    l.extend(re.split('\s+', str))

    l = filter(None, l)      #remove empty string
    return l
    #


def removeStopwords(l, stopwords):
    for sw in stopwords:
        l = [x for x in l if x != sw]

    return l

def stemWords(l):
    ps = PorterStemmer()
    return [ps.stem(x, 0, len(x) - 1) for x in l]

def preprocess(str):
    with open('stopwords.txt', 'r') as f:
        stopwords = f.read().splitlines()
    stopwords = [x.rstrip() for x in stopwords]     # remove trailing spaces
    str = removeSGML(str)
    str = str.lower()
    l = tokenizeText(str)
    #l = removeStopwords(l, stopwords)
    #l = stemWords(l)
    word_count_dict = {}
    for word in l:
        word_count_dict[word] = word_count_dict.get(word, 0) + 1
    return word_count_dict

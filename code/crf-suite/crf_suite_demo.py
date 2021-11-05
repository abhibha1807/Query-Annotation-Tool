import pickle
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain

import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

# %matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from tabulate import tabulate

import nltk
import os
import ast
import json
from nltk.tokenize import word_tokenize, sent_tokenize 
testwords=[]
def word2features(sent, i):
    word = sent[i][0]
    testwords.append(word)
    postag = sent[i][1]
    tag = sent[i][2]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
        'ismolecule': 0,
        'isprocess': 0,
        'isquantity': 0,
        'iscondition': 0,
        'isaction': 0,
        'isother' : 0
    }
    if tag == 'MOLECULES' or tag == 'I-MOLECULES' or tag == 'B-MOLECULES':
        features['ismolecule']=1.0
    if tag == 'QUANTITY' or tag == 'I-QUANTITY' or tag == 'B-QUANTITY':
        features['isquantity']=1.0
    if tag == 'PROCESS' or tag == 'I-PROCESS' or tag == 'B-PROCESS':
        features['isprocess']=1.0
    if tag == 'CONDITION' or tag == 'I-CONDITION' or tag == 'B-CONDITION':
        features['iscondition']=1.0
    if tag == 'ACTIONS':
        features['isaction']=1.0
    if tag == 'O':
        features['isother']=1.0

    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]


key=0
final={}
for i in range(3,4):
    fnum='{0:04}'.format(i)
    #print(fnum)
    try:
        with open('together/'+fnum+'.json') as f:
            data=f.readlines()
        f.close()
    except:
        continue

    if type(data)==list:
        data=json.loads(data[0])
    try:
        data.pop('id')
    except:
        pass

    pos=nltk.pos_tag(word_tokenize(data['text']))
    words=(word_tokenize(data['text']))
    p=0
    itr=0
    # for conll format
    temp=[]
    while(itr<len(pos)):
        sind=data['text'].find(words[itr])
        data['text']=data['text'].replace(words[itr],'*'*len(words[itr]),1)
        #print(sind)
        f=0
        for l in data['labels']:
            if sind>=l[0] and sind<=l[1]:
                f=1
                # print(pos[x])
                #print((words[itr],pos[itr][1],l[2]))
                temp.append([words[itr],pos[itr][1],l[2]])
                break
        if f == 0:
            temp.append([words[itr],pos[itr][1],'O'])
        itr=itr+1	
        # if itr ==20:
        # 	break

    t=0
    while t<(len(temp)):
        if temp[t][2]=='ACTIONS' or temp[t][2]=='O':
            #print('ping')
            t=t+1
            continue
        #print(t)
        ctr=t+1
        flag=0
        while(temp[ctr][2]==temp[t][2]):
            #print('pong',temp[ctr])
            flag=1	
            temp[ctr][2]='I-'+temp[t][2]
            #print(temp[ctr])
            ctr=ctr+1

        if flag == 1:
            temp[t][2]='B-'+temp[t][2]
            #print(temp[t])

        t=ctr+1

    final[key]=temp
    key=key+1

dataset=final
X_test = [sent2features(dataset[0])]

print(len(X_test[0]))
print(len(testwords))
# load model
loaded_model = pickle.load(open("crf_model.sav", 'rb'))
y_pred=(loaded_model.predict(X_test))
print(len(y_pred[0]))

for p in range(len(y_pred)):
    for q in range(len(y_pred[p])):
        if y_pred[p][q]=='I-CONDITIONS' or y_pred[p][q]=='B-CONDITIONS':
            y_pred[p][q]='CONDITIONS'
        if y_pred[p][q]=='I-MOLECULES' or y_pred[p][q]=='B-MOLECULES':
            y_pred[p][q]='MOLECULES'
        if y_pred[p][q]=='I-PROCESS' or y_pred[p][q]=='B-PROCESS':
            y_pred[p][q]='PROCESS'
        if y_pred[p][q]=='I-QUANTITY' or y_pred[p][q]=='B-QUANTITY':
            y_pred[p][q]='QUANTITY'


table=[]
table.append(["WORD","TAG"])
for i in range(len(y_pred[0])):
	table.append([testwords[i],y_pred[0][i]])

print(tabulate(table,headers="firstrow"))

# the crf_model.sav is the latest model with added features. While the old one is the one with old features.
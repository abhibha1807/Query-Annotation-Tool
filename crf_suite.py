'''
Sample from dataset
CRICKET NNP I-NP O
- : O O
LEICESTERSHIRE NNP I-NP I-ORG
TAKE NNP I-NP O
OVER IN I-PP O
AT NNP I-NP O
TOP NNP I-NP O
AFTER NNP I-NP O
INNINGS NNP I-NP O
VICTORY NN I-NP O
. . O O
'''

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

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

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
    }
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



import nltk
import os
import ast
import json
from nltk.tokenize import word_tokenize, sent_tokenize 

key=0
final={}
for i in range(2,100):
	fnum='{0:04}'.format(i)
	try:
		with open('/Users/abhibhagupta/Desktop/TCS/NER/annotations/op_doccano/together/'+fnum+'.json') as f:
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
		f=0
		for l in data['labels']:
			if sind>=l[0] and sind<=l[1]:
				f=1
				temp.append([words[itr],pos[itr][1],l[2]])
				break
		if f == 0:
			temp.append([words[itr],pos[itr][1],'O'])
		itr=itr+1	

	# for IOB Tagging
	t=0
	while t<(len(temp)):
		if temp[t][2]=='ACTIONS' or temp[t][2]=='O':
			t=t+1
			continue
		ctr=t+1
		flag=0
		while(temp[ctr][2]==temp[t][2]):
			flag=1	
			temp[ctr][2]='I-'+temp[t][2]
			ctr=ctr+1
		if flag == 1:
			temp[t][2]='B-'+temp[t][2]
		t=ctr+1

	final[key]=temp
	key=key+1
print(len(final))





#BATCH LEARNING
# train test split
dataset=final
train_size=int(0.9*len(dataset))
print(train_size)
train_sents={}
test_sents={}
for i in range(train_size):
	train_sents[i]=dataset[i]

for i in range(train_size,len(dataset)):
	test_sents[i]=dataset[i]

print(len(train_sents),len(test_sents))


#conevrting to feature arrays
X_train = [sent2features(train_sents[s]) for s in range(len(train_sents))]
y_train = [sent2labels(train_sents[s]) for s in range(len(train_sents))]
X_test = [sent2features(test_sents[s]) for s in range(train_size,len(dataset))]
y_test = [sent2labels(test_sents[s]) for s in range(train_size,len(dataset))]
print(len(X_train),len(y_train),len(X_test),len(y_test))

#define algorithm
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(X_train, y_train)
print('labels:',labels)

#prediction and metrics
y_pred = crf.predict(X_test)
print(metrics.flat_f1_score(y_test, y_pred,average='weighted', labels=labels))

sorted_labels = sorted(
    labels,
    key=lambda name: (name[1:], name[0])
)
print(metrics.flat_classification_report(
    y_test, y_pred, labels=sorted_labels, digits=3
))


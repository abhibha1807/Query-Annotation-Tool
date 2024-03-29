
import nltk
import creme
import pandas as pd
import pprint 
from nltk import word_tokenize, pos_tag
from collections import Counter
import matplotlib.pyplot as plt 
from creme import tree
from creme.tree import DecisionTreeClassifier
from creme import metrics
from creme import model_selection
from creme import compose
from datetime import datetime, timedelta 



# create features 
def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 1,
        'is_capitalized': sentence[index][0].upper() == sentence[index][0],
        'is_all_caps': sentence[index].upper() == sentence[index],
        'is_all_lower': sentence[index].lower() == sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'has_hyphen': '-' in sentence[index],
        'is_numeric': sentence[index].isdigit(),
        'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
    }
 
def untag(tagged_sentence):
    return [w for w, t in tagged_sentence]

def transform_to_dataset(tagged_sentences):
    X, Y = [], []
 
    for tagged in tagged_sentences:
        for index in range(len(tagged)):
            X.append(features(untag(tagged), index))
            Y.append(tagged[index][1])


    #X=X[0:10000]
    print(set(Y))

    X_y=[]
    for i in range(len(X)):
    	X_y.append((X[i],Y[i]))
    return(X_y)
 

# get dictionary mapping of word and count
file1 = open('/Users/abhibhagupta/Desktop/TCS/version_control_TCS_POS_exploration/datasets/conll_dataset_pos/pos.train.txt', 'r') 
Lines = file1.readlines() 
#print(type(Lines))
l=[]
t=[]
tagged_sentences=[]
for i in range(len(Lines)):
	l=Lines[i].split(' ')
	if l[0]!='\n':
		l.pop(2)
		t.append(tuple(l))
	else:
		tagged_sentences.append(t)
		t=[]
# print(dataset[0])
# print(len(dataset))


X, Y = [], []

for tagged in tagged_sentences:
    for index in range(len(tagged)):
        X.append(features(untag(tagged), index))


df=pd.DataFrame(X)

cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']
d={}
for col_name in cols:
	q={}
	q=Counter(list(df[col_name]))
	d={**d,**q}
        
#print(d)

def preprocess(x):
	l=['capitals_inside','has_hyphen','is_all_caps','is_all_lower','is_capitalized', 'is_first', 'is_last','is_numeric']
	for i in l:
		if x[i]==True:
			x[i]=1.0
		else:
			x[i]=0.0

	return(x)

# converting text into numbers based on there frequencies of occurence
def preprocess1(x):
	cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']

	for i in cols:
		x[i]=d[x[i]]
	
	return(x)


def main():

	# obtain the tagged sentences
	
	X_y= transform_to_dataset(tagged_sentences)

	metric = metrics.F1()

	# compose pipeline for preprocessing and predictions
	model = compose.Pipeline(
      ('preprocess', preprocess),
      ('preprocess1', preprocess1),
      ('tree', DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy'))
      )

	# print(type(model))
	# print(model)

	# for x, y in X_y:
	# 	y_pred = model.predict_proba_one(x)
	# 	metric = metric.update(y, y_pred)
	# 	model = model.fit_one(x, y)
	# print(metric)
	with open('progress.log', 'w') as f:
		(model_selection.progressive_val_score(X_y=X_y, model=model, metric=metric,print_every=1000,file=f))	

	
if __name__ == '__main__':
	main()


# results (first 10k instances)
# [1,000] F1: 0.107107
# [2,000] F1: 0.122561
# [3,000] F1: 0.128376
# [4,000] F1: 0.126532
# [5,000] F1: 0.125025
# [6,000] F1: 0.127188
# [7,000] F1: 0.126304
# [8,000] F1: 0.126891
# [9,000] F1: 0.123569
# [10,000] F1: 0.123712

# results (first 10k instances (delay=2))
# [1,000] F1: 0.113226
# [2,000] F1: 0.127127
# [3,000] F1: 0.131421
# [4,000] F1: 0.128814
# [5,000] F1: 0.126851
# [6,000] F1: 0.12871
# [7,000] F1: 0.127608
# [8,000] F1: 0.128032
# [9,000] F1: 0.124583
# [10,000] F1: 0.124625
# F1: 0.124625


# results (whole dataset)
# [10,000] F1: 0.123712
# [20,000] F1: 0.126456
# [30,000] F1: 0.127571
# [40,000] F1: 0.128828
# [50,000] F1: 0.134103
# [60,000] F1: 0.137902
# [70,000] F1: 0.142802
# [80,000] F1: 0.148102
# [90,000] F1: 0.153324
# [100,000] F1: 0.158822
# F1: 0.159305

# results whole dataset conll
#F1: 0.220167

# results combined
# almost same as above
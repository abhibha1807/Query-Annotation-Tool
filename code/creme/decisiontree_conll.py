from pprint import pprint
import creme
import pandas as pd
from collections import Counter
from creme import tree
from creme.tree import DecisionTreeClassifier
from creme import metrics
from creme import model_selection
from creme import compose
from datetime import datetime, timedelta 
from creme import multiclass


# create features 
def features(sentence, index):
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

    #print(set(Y))

    X_y=[]
    for i in range(len(X)):
    	X_y.append((X[i],Y[i]))
    return(X_y)
 

# get dictionary mapping of word and count
file1 = open('pos.train.txt', 'r') 
Lines = file1.readlines() 

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
        


def preprocess(x):
	l=['capitals_inside','has_hyphen','is_all_caps','is_all_lower','is_capitalized', 'is_first', 'is_last','is_numeric']
	cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']
	p={}
	for i in l:
		if x[i]==True:
			p[i]=1.0
		else:
			p[i]=0.0
	for i in cols:
		p[i]=d[x[i]]
	return(p)
def main():

    # obtain the tagged sentences
    
    X_y=transform_to_dataset(tagged_sentences)
    metric = metrics.F1()
    model= compose.FuncTransformer(preprocess) | (DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy'))

    for x, y in X_y[0:10]:
        model = model.fit_one(x, y)
    x = X_y[0][0]
    report = model.debug_one(X_y[0][0])
    print(report)

if __name__ == '__main__':
    main()
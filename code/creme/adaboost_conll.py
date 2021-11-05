
import creme
import pandas as pd
from collections import Counter
from creme import tree
from creme.tree import DecisionTreeClassifier
from creme.tree import RandomForestClassifier
from creme import metrics
from creme import model_selection
from creme import compose
from datetime import datetime, timedelta 
from creme import sampling
from creme import optim
import numpy as np
from creme import ensemble
from creme.ensemble import BaggingClassifier

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
    #print(set(Y))
    #return(X,Y)
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

# # converting text into numbers based on there frequencies of occurence
def preprocess1(x):
	cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']

	for i in cols:
		try:
			x[i]=d[x[i]]
		except:
			pass
	#print(x)
	return(x)

# def preprocess(X,Y):
# 	l=['capitals_inside','has_hyphen','is_all_caps','is_all_lower','is_capitalized', 'is_first', 'is_last','is_numeric']
# 	for i in range(len(X)):
# 	  for j in l:
# 	    if X[i][j]==True:
# 	      X[i][j]=1.0
# 	    else:
# 	      X[i][j]=0.0
	
# 	return(X,Y)

# converting text into numbers based on there frequencies of occurence
# def preprocess1(X,Y):
# 	print(type(X))
# 	df=pd.DataFrame((X))

# 	cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']
# 	d={}
# 	for col_name in cols:
# 		q={}
# 		q=Counter(list(df[col_name]))
# 		d={**d,**q}

# 	for name in cols:
# 	  l=list(df[name])
# 	  for i in range(len(l)):
# 	    l[i]=d[l[i]]
# 	  df[name]=l

# 	#print(df.head())
# 	return(df)



# def get_preprocessed_dataset(X,Y):
# 	x=[]
# 	y=[]
# 	for i in range(len(X)):
# 	  x.append(X[i])
# 	  y.append(Y[i])

# 	#print(len(x),len(y))
# 	return(x,y)

def class_freq(y):
	words = y
	Counter(words).keys() 
	Counter(words).values() 
	print("The classes and there frequencies \n")
	print(Counter(words))

def main():

	X_y = transform_to_dataset(tagged_sentences)
	#X_y=(X_y[0:10])
	# X,Y = preprocess(X,Y)
	# df = preprocess1(X,Y)
	# X=df.T.to_dict().values()
	# X=list(X)
	# x_new=[]
	# y_new=Y
	# for i in X:
	# 	x_new.append(list(i.values()))


	# class_freq(y_new)

	# cols=['word','is_first','is_last','is_capitalized','is_all_caps','is_all_lower','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3','prev_word','next_word','has_hyphen','is_numeric','capitals_inside']
	# xtrain=[]
	# ytrain=y_new
	# for i in range(len(x_new)):
	# 	d={}
	# 	c=0
	# 	for j in cols:
	# 		d[j]=x_new[i][c]
	# 		c=c+1
	# 	xtrain.append(d)

	metric = metrics.ClassificationReport()

	# model = compose.Pipeline(
 #      ('preprocess', preprocess),
 #      ('preprocess1', preprocess1),
 #      ('tree', DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy',max_depth=100,min_child_samples=2))
 #      )

	model = ensemble.AdaBoostClassifier(
		model=compose.Pipeline(
			 (preprocess),
			 (preprocess1),
			#(DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy'))
			(RandomForestClassifier(n_trees=5,seed=42,patience=100,confidence=1e-2,criterion='entropy',max_depth=100,min_child_samples=5))
		),
		n_models=50,
		seed=42
	)
	print(type(model))
	print(model)

	# X_y=[]
	# for i in range(len(xtrain)):
	# 	X_y.append((xtrain[i],ytrain[i]))
	
 
	# for x, y in X_y:
	# 	y_pred = model.predict_proba_one(x)
	# 	metric = metric.update(y, y_pred)
	# 	model = model.fit_one(x, y)
	# print(metric)

	print(model_selection.progressive_val_score(X_y=X_y, model=model, metric=metric,print_every=10000,show_time=True,show_memory=True))	

	
if __name__ == '__main__':
	main()


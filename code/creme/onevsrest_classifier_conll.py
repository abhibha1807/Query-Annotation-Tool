import sys
import csv
from pprint import pprint
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
from creme import multiclass

filename = sys.argv[-1]
# create features 
# def features(sentence, index):
#     """ sentence: [w1, w2, ...], index: the index of the word """
#     return {
#         'word': sentence[index],
#         'is_first': index == 0,
#         'is_last': index == len(sentence) - 1,
#         'is_capitalized': sentence[index][0].upper() == sentence[index][0],
#         'is_all_caps': sentence[index].upper() == sentence[index],
#         'is_all_lower': sentence[index].lower() == sentence[index],
#         'prefix-1': sentence[index][0],
#         'prefix-2': sentence[index][:2],
#         'prefix-3': sentence[index][:3],
#         'suffix-1': sentence[index][-1],
#         'suffix-2': sentence[index][-2:],
#         'suffix-3': sentence[index][-3:],
#         'prev_word': '' if index == 0 else sentence[index - 1],
#         'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
#         'has_hyphen': '-' in sentence[index],
#         'is_numeric': sentence[index].isdigit(),
#         'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
#     }
 
# def untag(tagged_sentence):
#     return [w for w, t in tagged_sentence]

# def transform_to_dataset():

	# file1 = open(filename, 'r') 
	# Lines = file1.readlines() 
	# #print(type(Lines))
	# l=[]
	# t=[]
	# tagged_sentences=[]
	# for i in range(len(Lines)):
	# 	l=Lines[i].split(' ')
	# 	if l[0]!='\n':
	# 		l.pop(2)
	# 		t.append(tuple(l))
	# 	else:
	# 		tagged_sentences.append(t)
	# 		t=[]

	# X_y = []
 
	# for tagged in tagged_sentences:
	#     for index in range(len(tagged)):
	#         # X.append(features(untag(tagged), index))
	#         # Y.append(tagged[index][1])
	#         X_y.append((features(untag(tagged), index),tagged[index][1]))

    #X=X[0:10000]
    #print(set(Y))

    # X_y=[]
    # for i in range(len(X)):
    # 	X_y.append((X[i],Y[i]))
	# return(X_y)
 
def get_dict():
	with open(filename) as f:
		a = [{k: v for k, v in row.items()}
        	for row in csv.DictReader(f, skipinitialspace=True)]

	X=[]
	for i in range(len(a)):
		t=a[i].pop('target')
		a[i].pop('')
		X.append(a[i])

	df=pd.DataFrame(X)

	cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']
	d={}
	for col_name in cols:
		q={}
		q=Counter(list(df[col_name]))
		d={**d,**q}
	return(d)
	        
	#print(d)

def preprocess(x):
	l=['capitals_inside','has_hyphen','is_all_caps','is_all_lower','is_capitalized', 'is_first', 'is_last','is_numeric']
	cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']
	p={}
	for i in l:
		if x[i]==True:
			#x[i]=1.0
			p[i]=1.0
		else:
			#x[i]=0.0
			p[i]=0.0
	d=get_dict()
	for i in cols:
		p[i]=d[x[i]]
	return(p)
	#return(x)

# converting text into numbers based on there frequencies of occurence
# def preprocess1(x):
# 	cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']
# 	l=[]
# 	for i in cols:
# 		l.append({i:d[x[i]]})
# 		# x[i]=d[x[i]]
# 	return(l)
	#return(x)


def main():
	
	# obtain the tagged sentences
	with open(filename) as f:
		a = [{k: v for k, v in row.items()}
        	for row in csv.DictReader(f, skipinitialspace=True)]

	X_y=[]
	for i in range(len(a)):
		t=a[i].pop('target')
		a[i].pop('')
		X_y.append((a[i],t))
			

	#X_y=transform_to_dataset()
	#print(X_y[0])
	metric = metrics.F1()
	#metric=metrics.ClassificationReport()
	#t = compose.FuncTransformer(preprocess)
	#print(type(t))
	#pprint(t.transform_one(X_y[0][0]))

	model= compose.FuncTransformer(preprocess) | multiclass.OneVsRestClassifier(DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy'))
	#print(model)

	#RandomForestClassifier(n_trees=20,seed=42,patience=100,confidence=1e-2,criterion='entropy',max_depth=100,min_child_samples=5,n_split_points=60)
	# scaler = preprocessing.StandardScaler()
	# ovr = multiclass.OneVsRestClassifier(linear_model.LogisticRegression())
	# model = scaler | ovr


	# compose pipeline for preprocessing and predictions
	# not much difference in gini and entropy, entropy is a bit difficult to calculate thats all
	# preproc=preprocess()
	# preproc1=preprocess1()
	# tree=multiclass.OneVsRestClassifier(DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy'))
	# model=preproc | preproc1 | tree

	# model = compose.Pipeline(
 #      ('preprocess', preprocess),
 #      ('preprocess1', preprocess1),
 #      ('tree', DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy'))
 #      )

	# print(type(model))
	# print(model)
	
	# for x, y in X_y[0:10]:
		#print((x.items()),type(y))
		# model.predict_one(x)
		# y_pred = model.predict_proba_one(x)
	# 	metric = metric.update(y, y_pred)
		# model = model.fit_one(x, y)
	#print(model.draw())
	#x = X_y[0][0]
	# report = model.debug_one(X_y[0][0])
	# print(report)
	# print(metric)

	# with open('progress.log', 'w') as f:
	print(model_selection.progressive_val_score(X_y=X_y, model=model, metric=metric,print_every=1))	
	# with open('progress.log') as f:
	# 	for line in f.read().splitlines():
	# 		print(line)
	
if __name__ == '__main__':
	main()

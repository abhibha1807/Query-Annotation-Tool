
import nltk
import creme
import pandas as pd
import pprint 
from nltk import word_tokenize, pos_tag
from collections import Counter
import matplotlib.pyplot as plt 
from creme import tree
from creme.tree import DecisionTreeClassifier
from creme.tree import RandomForestClassifier
from creme import metrics
from creme import model_selection
from creme import compose
from creme import linear_model


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
    # print(set(Y))

    # X_y=[]
    # for i in range(len(X)):
    # 	X_y.append((X[i],Y[i]))
    # return(X_y)
    return(X,Y)
 

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
	for p in range(len(x)):
		for i in l:
			if x[p][i]==True:
				x[i]=1.0
			else:
				x[p][i]=0.0

	return(x)

# converting text into numbers based on there frequencies of occurence
def preprocess1(x):
	cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']
	for p in range(len(x)):
		for i in cols:
			x[p][i]=d[x[p][i]]
	
	return(x)


def main():

	# obtain the tagged sentences
	model = compose.Pipeline(
      ('preprocess', preprocess),
      ('preprocess1', preprocess1),
      #('tree', RandomForestClassifier(n_trees=10,seed=42,patience=10,confidence=1e-2,criterion='entropy',max_depth=100,min_child_samples=5,n_split_points=60))
      #linear_model.LinearRegression()
      )

	x,y= transform_to_dataset(tagged_sentences)
	print(dir(model.fit_many(x,y)))
	# for i in range(len(x)):
	# 	x[i]['target']=y[i]
	# print(x[0])
	# metric = metrics.ClassificationReport()
	# df=pd.DataFrame(x)
	# print(df.head())

	# df.to_csv('batch_conll_rf.csv')
	# names=['capitals_inside','has_hyphen','is_all_caps','is_all_lower','is_capitalized', 'is_first', 'is_last','is_numeric','word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3','target']
	
	# for x in pd.read_csv('batch_conll_rf.csv', names=names, chunksize=8096, nrows=3e5):
	# 	#print(type(x))
	#     y = x.pop('target')
	#     y_pred = model.predict_many(x)
	#     model.fit_many(x,y)
	

	# print(type(model))
	# print(model)

	# for x, y in X_y:
	# 	y_pred = model.predict_proba_one(x)
	# 	metric = metric.update(y, y_pred)
	# 	model = model.fit_one(x, y)
	# print(metric)


	# with open('progress.log', 'w') as f:
	# 	(model_selection.progressive_val_score(X_y=X_y, model=model, metric=metric,print_every=10000,file=f))	

	
if __name__ == '__main__':
	main()


# Gaussian whole dataset [211,000] F1: 0.257485
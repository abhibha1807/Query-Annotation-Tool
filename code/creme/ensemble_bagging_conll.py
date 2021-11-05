
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

	model = ensemble.BaggingClassifier(
		model=compose.Pipeline(
			 (preprocess),
			 (preprocess1),
			#(DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy'))
			(RandomForestClassifier(n_trees=5,seed=42,patience=100,confidence=1e-2,criterion='entropy',max_depth=100,min_child_samples=5))
		),
		n_models=5,
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

	print(model_selection.progressive_val_score(X_y=X_y, model=model, metric=metric,print_every=50000,show_time=True,show_memory=True))	

	
if __name__ == '__main__':
	main()

''' models=3
[150,000]            Precision   Recall   F1      Support  
                                                 
       #       0.000    0.000   0.000        17  
       $       0.125    0.001   0.002      1267  
      ''       0.000    0.000   0.000      1097  
       (       0.000    0.000   0.000       194  
       )       0.000    0.000   0.000       200  
       ,       0.209    0.116   0.149      7699  
       .       0.000    0.000   0.000      6298  
       :       0.000    0.000   0.000       731  
      CC       0.000    0.000   0.000      3820  
      CD       0.280    0.001   0.002      5843  
      DT       0.223    0.607   0.326     13031  
      EX       0.000    0.000   0.000       156  
      FW       0.000    0.000   0.000        34  
      IN       0.242    0.450   0.314     16093  
      JJ       0.143    0.000   0.001      9390  
     JJR       0.000    0.000   0.000       615  
     JJS       0.000    0.000   0.000       268  
      MD       0.000    0.000   0.000      1512  
      NN       0.203    0.640   0.309     21300  
     NNP       0.256    0.239   0.247     13699  
    NNPS       0.000    0.000   0.000       294  
     NNS       0.273    0.003   0.006      9690  
     PDT       0.000    0.000   0.000        38  
     POS       0.000    0.000   0.000      1207  
     PRP       0.111    0.000   0.001      2839  
    PRP$       0.000    0.000   0.000      1358  
      RB       0.000    0.000   0.000      4712  
     RBR       0.000    0.000   0.000       226  
     RBS       0.000    0.000   0.000       123  
      RP       0.000    0.000   0.000        52  
     SYM       0.000    0.000   0.000         6  
      TO       0.000    0.000   0.000      3533  
      UH       0.000    0.000   0.000        15  
      VB       0.062    0.000   0.000      4218  
     VBD       0.464    0.020   0.039      4789  
     VBG       0.000    0.000   0.000      2313  
     VBN       0.000    0.000   0.000      3369  
     VBP       0.000    0.000   0.000      2082  
     VBZ       0.000    0.000   0.000      3317  
     WDT       0.000    0.000   0.000       668  
      WP       0.000    0.000   0.000       386  
     WP$       0.000    0.000   0.000        26  
     WRB       0.000    0.000   0.000       347  
      ``       0.000    0.000   0.000      1127  
                                                 
   Macro       0.059    0.047   0.032            
   Micro       0.221    0.221   0.221            
Weighted       0.165    0.221   0.138            

'''

'''
          Precision   Recall   F1      Support  
                                                 
       #       0.000    0.000   0.000        36  
       $       0.000    0.000   0.000      1750  
      ''       0.000    0.000   0.000      1493  
       (       0.000    0.000   0.000       274  
       )       0.000    0.000   0.000       281  
       ,       0.181    0.007   0.013     10770  
       .       0.258    0.383   0.308      8827  
       :       0.000    0.000   0.000      1047  
      CC       0.000    0.000   0.000      5372  
      CD       0.324    0.006   0.011      8315  
      DT       0.221    0.664   0.332     18335  
      EX       0.000    0.000   0.000       206  
      FW       0.000    0.000   0.000        38  
      IN       0.260    0.426   0.322     22764  
      JJ       0.000    0.000   0.000     13085  
     JJR       0.000    0.000   0.000       853  
     JJS       0.000    0.000   0.000       374  
      MD       0.000    0.000   0.000      2167  
      NN       0.208    0.547   0.302     30146  
     NNP       0.303    0.398   0.344     19884  
    NNPS       0.000    0.000   0.000       420  
     NNS       0.277    0.001   0.002     13619  
     PDT       0.000    0.000   0.000        55  
     POS       0.000    0.000   0.000      1769  
     PRP       0.000    0.000   0.000      3820  
    PRP$       0.000    0.000   0.000      1881  
      RB       0.214    0.000   0.001      6607  
     RBR       0.000    0.000   0.000       321  
     RBS       0.000    0.000   0.000       191  
      RP       0.000    0.000   0.000        83  
     SYM       0.000    0.000   0.000         6  
      TO       0.000    0.000   0.000      5081  
      UH       0.000    0.000   0.000        15  
      VB       0.000    0.000   0.000      6017  
     VBD       0.318    0.023   0.043      6745  
     VBG       0.000    0.000   0.000      3272  
     VBN       0.000    0.000   0.000      4763  
     VBP       0.000    0.000   0.000      2868  
     VBZ       0.000    0.000   0.000      4648  
     WDT       0.000    0.000   0.000       955  
      WP       0.000    0.000   0.000       529  
     WP$       0.000    0.000   0.000        35  
     WRB       0.000    0.000   0.000       478  
      ``       0.000    0.000   0.000      1531  
                                                 
   Macro       0.058    0.056   0.038            
   Micro       0.236    0.236   0.236            
Weighted
       0.173    0.236   0.154            

                 23.6% accuracy  
'''                

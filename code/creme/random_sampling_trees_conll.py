'''
Counter({'NN': 30147, 'IN': 22764, 'NNP': 19884, 'DT': 18335, 'NNS': 13619, 'JJ': 13085, ',': 10770, 
'.': 8827, 'CD': 8315, 'VBD': 6745, 'RB': 6607, 'VB': 6017, 'CC': 5372, 'TO': 5081, 'VBN': 4763,
 'VBZ': 4648, 'PRP': 3820, 'VBG': 3272, 'VBP': 2868, 'MD': 2167, 'PRP$': 1881, 'POS': 1769, 
 '$': 1750, '``': 1531, "''": 1493, ':': 1047, 'WDT': 955, 'JJR': 853, 'WP': 529, 'WRB': 478,
  'NNPS': 420, 'JJS': 374, 'RBR': 321, ')': 281, '(': 274, 'EX': 206, 'RBS': 191, 'RP': 83, 'PDT': 55, 
  'FW': 38, '#': 36, 'WP$': 35, 'UH': 15, 'SYM': 6})
'''

'''
ratios:
{'NN': 0.14238618598478228, 'IN': 0.10751581045402807, 'NNP': 0.0939133884672243, 
'DT': 0.08659736358612742, 'NNS': 0.06432339758273625, 'JJ': 0.06180128183934973, 
',': 0.05086739055481823, '.': 0.041690478776915556, 'CD': 0.039272270423706, 
'VBD': 0.031857061215622005, 'RB': 0.031205278495420992, 'VB': 0.028418671213402164,
'CC': 0.025372295455940906, 'TO': 0.02399788406769094, 'VBN': 0.022495949973314694, 
'VBZ': 0.021952797706480516, 'PRP': 0.018042101385274435, 'VBG': 0.01545386275722983, 
'VBP': 0.013545745228525412, 'MD': 0.010234877932431857, 'PRP$': 0.008884081860131206, 
'POS': 0.008355098782866615, '$': 0.00826536058225923, '``': 0.00723100974367936, 
"''": 0.007051533342464589, ':': 0.004945047159785951, 'WDT': 0.004510525346318609, 
'JJR': 0.004028772900952642, 'WP': 0.0024985004274372187, 'WRB': 0.0022576242047542354, 
'NNPS': 0.001983686539742215, 'JJS': 0.001766425633008544, 'RBR': 0.001516103283945836, 
')': 0.0013271807563513393, '(': 0.0012941193140223023, 'EX': 0.0009729510171116579,
 'RBS': 0.0009021050692637217, 'RP': 0.00039201424475858064, 'PDT': 0.00025976847544243294, 
 'FW': 0.00017947640121477186, '#': 0.00017003027483504702, 'WP$': 0.0001653072116451846, 
 'UH': 7.084594784793625e-05, 'SYM': 2.8338379139174502e-05}
 '''

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
from creme import sampling
from creme import optim
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN
import numpy as np

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
        
print(d)

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
		x[i]=d[x[i]]
	
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



def get_preprocessed_dataset(X,Y):
	x=[]
	y=[]
	for i in range(len(X)):
	  x.append(X[i])
	  y.append(Y[i])

	#print(len(x),len(y))
	return(x,y)
def class_freq(y):
	words = y
	Counter(words).keys() 
	Counter(words).values() 
	print("The classes and there frequencies \n")
	print(Counter(words))

def main():

	#oversample = SMOTE(sampling_strategy='minority')
	#undersample=RandomUnderSampler(sampling_strategy='majority')
	# combiner=SMOTEENN(sampling_strategy='all')
	X_y = transform_to_dataset(tagged_sentences)
	
	# X,Y = preprocess(X,Y)
	# df = preprocess1(X,Y)
	# X=df.T.to_dict().values()
	# X=list(X)
	# x_new=[]
	# y_new=Y
	# for i in X:
	# 	x_new.append(list(i.values()))

	# x_new, y_new = oversample.fit_resample(x_new, y_new)
	#x_new, y_new = undersample.fit_resample(x_new, y_new)
	# x_new, y_new = combiner.fit_resample(x_new, y_new)
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
 #      ('tree', DecisionTreeClassifier(patience=10,confidence=1e-2,criterion='entropy',max_depth=100,min_child_samples=1))
 #      )

	model = compose.Pipeline(
   		('preprocess', preprocess),
   		('preprocess1', preprocess1),
    	sampling.RandomSampler(
        classifier=DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy',max_depth=100),
        #desired_dist={'NN': 0.06634159286164461, 'IN': 0.08785802143735723, 'NNP': 0.10058338362502514, 'DT': 0.109080992637033, 'NNS': 0.14685366032748368, 'JJ': 0.15284677111196027, ',': 0.18570102135561745, '.': 0.22657754616517503, 'CD': 0.24052916416115455, 'VBD': 0.2965159377316531, 'RB': 0.3027092477675193, 'VB': 0.33239155725444575, 'CC': 0.37230081906180196, 'TO': 0.39362330249950794, 'VBN': 0.419903422212891, 'VBZ': 0.43029259896729777, 'PRP': 0.5235602094240838, 'VBG': 0.6112469437652812, 'VBP': 0.697350069735007, 'MD': 0.9229349330872173, 'PRP$': 1.063264221158958, 'POS': 1.1305822498586773, '$': 1.1428571428571428, '``': 1.3063357282821686, "''": 1.3395847287340925, ':': 1.9102196752626552, 'WDT': 2.094240837696335, 'JJR': 2.3446658851113718, 'WP': 3.780718336483932, 'WRB': 4.184100418410042, 'NNPS': 4.761904761904762, 'JJS': 5.347593582887701, 'RBR': 6.230529595015576, ')': 7.117437722419929, '(': 7.299270072992701, 'EX': 9.70873786407767, 'RBS': 10.471204188481675, 'RP': 24.096385542168676, 'PDT': 36.36363636363637, 'FW': 52.63157894736842, '#': 55.55555555555556, 'WP$': 57.142857142857146, 'UH': 133.33333333333334, 'SYM': 333.3333333333333},
        desired_dist={'NN': 1, 'IN': 1, 'NNP': 1, 'DT': 1, 'NNS': 1, 'JJ': 1, ',': 1, '.': 1, 'CD': 1, 'VBD': 1, 'RB': 1, 'VB': 1, 'CC': 1, 'TO': 1, 'VBN': 1, 'VBZ': 1, 'PRP': 1, 'VBG': 1, 'VBP': 1, 'MD': 1, 'PRP$':1, 'POS': 1, '$': 1, '``': 1, "''": 1, ':': 1, 'WDT': 1, 'JJR': 1, 'WP': 1, 'WRB': 1, 'NNPS': 1, 'JJS': 1, 'RBR': 1, ')': 1, '(': 1, 'EX': 1, 'RBS': 11, 'RP': 1, 'PDT': 1, 'FW': 1, '#': 1, 'WP$': 1, 'UH': 1, 'SYM': 1},
        sampling_rate=.01,
        seed=42
    )
)
	# model=DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy',max_depth=100,min_child_samples=2)
	# print(type(model))
	# print(model)

	# X_y=[]
	# for i in range(len(xtrain)):
	# 	X_y.append((xtrain[i],ytrain[i]))
	
 
	# for x, y in X_y:
	# 	y_pred = model.predict_proba_one(x)
	# 	metric = metric.update(y, y_pred)
	# 	model = model.fit_one(x, y)
	# print(metric)

	print(model_selection.progressive_val_score(X_y=X_y, model=model, metric=metric,print_every=50000))	

	
if __name__ == '__main__':
	main()

# whole dataset f1: F1: 0.301748 (using creme implmentation of unbalanced datasets)
# undersampling: (using SMOTE)
#           Precision   Recall   F1      Support  
                                                 
#        #       0.486    1.000   0.654        35  
#        $       0.883    0.979   0.928      1750  
#       ''       0.493    0.848   0.623      1493  
#        (       0.000    0.000   0.000       274  
#        )       0.000    0.000   0.000       281  
#        ,       0.988    0.962   0.975     10770  
#        .       0.967    0.992   0.979      8827  
#        :       0.420    0.746   0.538      1047  
#       CC       0.802    0.820   0.811      5372  
#       CD       0.669    0.825   0.739      8315  
#       DT       0.881    0.909   0.895     18335  
#       EX       0.395    0.146   0.213       206  
#       FW       0.000    0.000   0.000        38  
#       IN       0.585    0.844   0.691     22764  
#       JJ       0.569    0.754   0.648     13085  
#      JJR       0.564    0.239   0.336       853  
#      JJS       0.388    0.102   0.161       374  
#       MD       0.308    0.404   0.350      2167  
#       NN       0.000    0.000   0.000         6  
#      NNP       0.680    0.791   0.731     19884  
#     NNPS       0.263    0.248   0.255       420  
#      NNS       0.386    0.516   0.442     13619  
#      PDT       0.000    0.000   0.000        55  
#      POS       0.592    0.529   0.559      1769  
#      PRP       0.492    0.352   0.410      3820  
#     PRP$       0.477    0.539   0.506      1881  
#       RB       0.398    0.248   0.305      6607  
#      RBR       0.000    0.000   0.000       321  
#      RBS       0.266    0.089   0.133       191  
#       RP       0.000    0.000   0.000        83  
#      SYM       0.000    0.000   0.000         6  
#       TO       1.000    0.717   0.835      5081  
#       UH       0.000    0.000   0.000        15  
#       VB       0.500    0.222   0.307      6017  
#      VBD       0.430    0.289   0.346      6745  
#      VBG       0.427    0.143   0.214      3272  
#      VBN       0.627    0.125   0.208      4763  
#      VBP       0.468    0.071   0.124      2868  
#      VBZ       0.819    0.273   0.409      4648  
#      WDT       0.927    0.093   0.169       955  
#       WP       0.000    0.000   0.000       529  
#      WP$       0.000    0.000   0.000        35  
#      WRB       1.000    0.033   0.065       478  
#       ``       1.000    0.013   0.026      1531  
                                                 
#    Macro       0.458    0.360   0.354            
#    Micro       0.652    0.652   0.652            
# Weighted       0.655    0.652   0.624            

#                  65.2% accuracy                  

# combiner f1 score
#            Precision   Recall   F1      Support  
                                                 
#        #       0.998    1.000   0.999     30146  
#        $       0.995    0.998   0.996     30146  
#       ''       0.990    0.995   0.993     29992  
#        (       0.981    0.992   0.986     30081  
#        )       0.979    0.983   0.981     30015  
#        ,       0.962    0.993   0.977     30147  
#        .       0.987    0.990   0.988     30117  
#        :       0.902    0.955   0.928     30118  
#       CC       0.769    0.952   0.851     30035  
#       CD       0.733    0.890   0.804     29495  
#       DT       0.681    0.911   0.779     29567  
#       EX       0.912    0.948   0.930     30135  
#       FW       0.844    0.897   0.870     30142  
#       IN       0.571    0.769   0.655     28512  
#       JJ       0.371    0.641   0.470     22962  
#      JJR       0.499    0.652   0.565     28659  
#      JJS       0.756    0.780   0.768     30103  
#       MD       0.569    0.824   0.673     30097  
#       NN       0.381    0.523   0.441     18843  
#      NNP       0.495    0.581   0.535     23056  
#     NNPS       0.629    0.673   0.650     29851  
#      NNS       0.397    0.405   0.401     26113  
#      PDT       0.893    0.938   0.915     30075  
#      POS       0.618    0.814   0.702     29732  
#      PRP       0.420    0.529   0.468     29794  
#     PRP$       0.573    0.597   0.584     30095  
#       RB       0.314    0.294   0.304     28392  
#      RBR       0.883    0.731   0.800     28874  
#      RBS       0.836    0.838   0.837     30141  
#       RP       0.913    0.792   0.849     29929  
#      SYM       0.968    0.928   0.948     30147  
#       TO       0.771    0.804   0.787     30108  
#       UH       0.787    0.707   0.744     30146  
#       VB       0.388    0.403   0.395     26254  
#      VBD       0.568    0.407   0.474     27210  
#      VBG       0.440    0.348   0.389     29407  
#      VBN       0.487    0.262   0.341     27294  
#      VBP       0.687    0.306   0.423     27322  
#      VBZ       0.729    0.246   0.368     28346  
#      WDT       0.834    0.828   0.831     29453  
#       WP       0.841    0.564   0.675     30135  
#      WP$       0.980    0.813   0.889     30147  
#      WRB       0.998    0.458   0.628     30128  
#       ``       1.000    0.703   0.825     30005  
                                                 
#    Macro       0.735    0.720   0.714            
#    Micro       0.728    0.728   0.728            
# Weighted       0.746    0.728   0.724            


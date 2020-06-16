
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
import sklearn
from sklearn.metrics import classification_report
file1 = open('/Users/abhibhagupta/Desktop/TCS/version_control_TCS_POS_exploration/datasets/conll_dataset_pos/pos.train.txt', 'r') 
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

cutoff = int(.75 * len(tagged_sentences))
training_sentences = tagged_sentences[:cutoff]
test_sentences = tagged_sentences[cutoff:]
 
print (len(training_sentences) ) 
print (len(test_sentences)   )     
 
def transform_to_dataset(tagged_sentences):
    X, y = [], []
 
    for tagged in tagged_sentences:
        for index in range(len(tagged)):
            X.append(features(untag(tagged), index))
            y.append(tagged[index][1])
 
    return X, y
 
X, y = transform_to_dataset(training_sentences)

 
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
 
clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', DecisionTreeClassifier(criterion='entropy'))
])

# print(dir(clf.score))
clf.fit(X[:10000], y[:10000])   

print ('Training completed')
 
X_test, y_test = transform_to_dataset(test_sentences)

y_pred=clf.predict(X_test)

print(type(y_pred),y_pred[0])
print ("F1:", classification_report(y_test,y_pred))
 
#F1:               precision    recall  f1-score   support

           #       1.00      1.00      1.00        18
#            $       1.00      0.99      0.99       421
#           ''       0.93      1.00      0.96       335
#            (       1.00      1.00      1.00        71
#            )       1.00      1.00      1.00        72
#            ,       1.00      1.00      1.00      2685
#            .       1.00      1.00      1.00      2211
#            :       1.00      0.95      0.97       286
#           CC       1.00      0.99      0.99      1338
#           CD       0.99      0.98      0.98      2220
#           DT       0.99      0.98      0.98      4433
#           EX       0.83      0.87      0.85        46
#           FW       0.00      0.00      0.00         3
#           IN       0.95      0.96      0.95      5684
#           JJ       0.75      0.69      0.72      3114
#          JJR       0.62      0.66      0.64       205
#          JJS       0.82      0.80      0.81        97
#           MD       0.98      0.98      0.98       569
#           NN       0.80      0.83      0.82      7518
#          NNP       0.91      0.97      0.94      5432
#         NNPS       0.62      0.14      0.23       116
#          NNS       0.91      0.93      0.92      3412
#          PDT       0.86      0.40      0.55        15
#          POS       0.92      0.95      0.93       479
#          PRP       0.96      0.91      0.93       830
#         PRP$       0.99      0.95      0.97       454
#           RB       0.84      0.82      0.83      1641
#          RBR       0.83      0.24      0.37        79
#          RBS       0.98      0.95      0.97        59
#           RP       1.00      0.21      0.34        29
#           TO       1.00      1.00      1.00      1308
#           VB       0.70      0.69      0.69      1508
#          VBD       0.81      0.87      0.84      1799
#          VBG       0.77      0.87      0.82       815
#          VBN       0.77      0.67      0.72      1204
#          VBP       0.73      0.68      0.70       658
#          VBZ       0.85      0.71      0.77      1075
#          WDT       0.94      0.66      0.78       244
#           WP       0.88      0.95      0.91       117
#          WP$       0.00      0.00      0.00         9
#          WRB       0.99      0.93      0.96       106
#           ``       1.00      1.00      1.00       342

#    micro avg       0.89      0.89      0.89     53057
#    macro avg       0.85      0.79      0.81     53057
# weighted avg       0.89      0.89      0.89     53057

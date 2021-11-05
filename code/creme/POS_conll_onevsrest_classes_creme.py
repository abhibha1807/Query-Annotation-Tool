import sys
import csv
import creme
import pprint 
from collections import Counter
from creme import tree
from creme.tree import DecisionTreeClassifier
from creme.tree import RandomForestClassifier
from creme import metrics
from creme import model_selection
from creme import compose
from creme import multiclass

class POS:
	def __init__(self,filename,model,metric,print_every):

		self.d={}
		self.X_y=[]
		self.cols=['word','prev_word','next_word','prefix-1','prefix-2','prefix-3','suffix-1','suffix-2','suffix-3']
		self.l=['capitals_inside','has_hyphen','is_all_caps','is_all_lower','is_capitalized', 'is_first', 'is_last','is_numeric']
		self.comp_model=compose.FuncTransformer(self.preprocess) | multiclass.OneVsRestClassifier(model)
		self.metric=metric
		self.print_every=print_every

		with open(filename) as f:
			a = [{k: v for k, v in row.items()}
				for row in csv.DictReader(f, skipinitialspace=True)]
		X=[]
		for i in range(len(a)):
			t=a[i].pop('target')
			X.append(a[i])
			self.X_y.append((a[i],t))

		for col_name in self.cols:
			q = [ feature[col_name] for feature in X ] 
			self.d={**self.d,**Counter(q)}
		        
		#print(self.d)


	def preprocess(self,x):
		preprocessed_dict={}
		for i in self.l:
			if x[i]==True:
				preprocessed_dict[i]=1.0
			else:
				preprocessed_dict[i]=0.0
		
		for i in self.cols:
			preprocessed_dict[i]=self.d[x[i]]
		return(preprocessed_dict)

	def train(self):
		with open('progress.log', 'w') as f:
			print(model_selection.progressive_val_score(X_y=self.X_y, model=self.comp_model, metric=self.metric,print_every=self.print_every,file=f))	
		
	def print(self):
		with open('progress.log') as f:
			for line in f.read().splitlines():
				print(line)

	def debug_one(self):
		for x, y in self.X_y[0:10]:
			self.comp_model.fit_one(x,y)
		report = self.comp_model.debug_one(self.X_y[0][0])
		print(report)


filename = sys.argv[-1]	
model=DecisionTreeClassifier(patience=100,confidence=1e-2,criterion='entropy')	
print_every=10000
metric = metrics.F1()
#metric=metrics.ClassificationReport()
obj=POS(filename,model,metric,print_every)
# to understand the flow of the classifier
obj.debug_one()
# obj.train()
# obj.print()


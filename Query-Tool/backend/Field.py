import re
from backend.QueryProcessor import QueryProcessor
from spacy.lang.en import English 
nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))
import itertools
from backend.Boolean import Boolean



class Field:

	def __init__(self,query,db,mode=0):
		self.query=query
		self.db=db
		self.mode=mode

	def MultiWordCombos(self,query):
		results=''
		final=[]
		query=(re.sub(r"\s(?=(word|lemma|tag|entity)=)",",",self.query))
		query=(query.split(','))
	
		for itr in range(len(self.db)):
			doc = nlp(self.db[itr])
			sentences = [sent.string.strip() for sent in doc.sents]
			new_query=[pair.split('|') for pair in query]
			combs=QueryProcessor.Combinations(new_query)

			for sent in range(len(sentences)):
				for c in combs:
					pos_list=[]
					for q in c:
						if QueryProcessor.EvaluateExp(q,sentences[sent])!=None:
							pos_list.append(QueryProcessor.EvaluateExp(q,sentences[sent]))

					if len(pos_list)==len(c):
						pos=[]
						for i in pos_list:
							for j in i:
								pos.append(j)
						final.append([sentences[sent],pos])
						
						ctr=0
						s=''
						for j in pos:
							s=s+sentences[sent][ctr:j[0]]+'<WORD>'+sentences[sent][j[0]:j[1]]+'</WORD>'
							ctr=j[1]+1
						s=s+sentences[sent][ctr:]
						results=results+s+'\n'
		
		
		if self.mode==1:
			return final
		else:
			return results




	def MultiPair(self,query):
		results=''
		query=(re.sub(r"\s(?=(word|lemma|tag|entity)=)",",",self.query))
		query=query.split(',')

		final=[]
		
		for itr in range(len(self.db)):
			doc = nlp(self.db[itr])
			sentences = [sent.string.strip() for sent in doc.sents]
			for sent in range(len(sentences)):
				pos_list=[]
				for pair in query:
					if QueryProcessor.EvaluateExp(pair,sentences[sent])!=None:
							pos_list.append(QueryProcessor.EvaluateExp(pair,sentences[sent]))
	
				if len(pos_list)<=len(query) and len(pos_list)>0:
					pos=[]
					for i in pos_list:
						for j in i:
							pos.append(j)
					final.append([sentences[sent],pos])
				
					ctr=0
					s=''
					for j in pos:
						s=s+sentences[sent][:j[0]]+'<WORD>'+sentences[sent][j[0]:j[1]]+'</WORD>'
						ctr=j[1]+1
					s=s+sentences[sent][ctr:]
					results=results+s+'\n'
				
				
			
		if self.mode==1:
			return final
		else:
			return results



	def CheckQuery(self):
		if '|' in self.query:
			return(self.MultiWordCombos(self.query))
		else:
			return(self.MultiPair(self.query))
		
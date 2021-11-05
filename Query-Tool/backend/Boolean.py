import re
from backend.QueryProcessor import QueryProcessor
from spacy.lang.en import English 
nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))


class Boolean:

	def __init__(self,query,db,mode=0):
		self.query=query
		self.db=db
		self.mode=mode


	def SingleWord(self,query):
		results=''
		final=[]
		for itr in range(len(self.db)):
			doc = nlp(self.db[itr])
			sentences = [sent.string.strip() for sent in doc.sents]
			for sent in range(len(sentences)):
				if len(QueryProcessor.Word(sentences[sent],query))>0:
					final.append([sentences[sent],QueryProcessor.Word(sentences[sent],query)])
					
					pos_list=QueryProcessor.Word(sentences[sent],query)
					ctr=0
					s=''
					for j in pos_list:
						s=s+sentences[sent][ctr:j[0]]+'<WORD>'+sentences[sent][j[0]:j[1]]+'</WORD>'
						ctr=j[1]+1
					s=s+sentences[sent][ctr:]
					results=results+s+'\n'
	
		if self.mode==1:
			return final
		else:
			return results




	def MultiWord(self,query):
		results=''
		final=[]
		for itr in range(len(self.db)):
			doc = nlp(self.db[itr])
			sentences = [sent.string.strip() for sent in doc.sents]

			for sent in range(len(sentences)):
				l=query.split(' ')
				pos_list=[]
				for q in l:
					if QueryProcessor.Word(sentences[sent],q)!=[]:
						pos_list.append(QueryProcessor.Word(sentences[sent],q))
				if len(pos_list)==len(l):
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
			print(results)
			return results
		

	

	def MultiWordCombos(self,query):
		
		final=[]
		results=''
	
		for itr in range(len(self.db)):
			doc = nlp(self.db[itr])
			sentences = [sent.string.strip() for sent in doc.sents]
			new_query=[pair.split('|') for pair in query]
			combs=QueryProcessor.Combinations(new_query)

			for sent in range(len(sentences)):
				for c in combs:
					pos_list=[]
					for q in c:
						if QueryProcessor.Word(sentences[sent],q)!=[]:
							pos_list.append(QueryProcessor.Word(sentences[sent],q))
					
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
		


	def CheckQuery(self):
		if '|' in self.query:
			return(self.MultiWordCombos(self.query.split(' ')))
		elif len(self.query.split(' '))>1:
			return(self.MultiWord(self.query))
		else:
			return(self.SingleWord(self.query))



	
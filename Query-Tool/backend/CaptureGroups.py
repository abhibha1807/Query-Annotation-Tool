import re
from backend.Boolean import Boolean
from backend.QueryProcessor import QueryProcessor
from spacy.lang.en import English 
from backend.Field import Field


nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))
class CaptureGroups:

	def __init__(self,query,db,mode=0):
		self.query=query
		self.db=db
		self.mode=mode


	def MultiPair(self,query):
		results=''
		final=[]
		final_capture={}
		query=(re.split(r"\s(?=\w+:)|:",query))
		for itr in range(len(self.db)):
			doc = nlp(self.db[itr])
			sentences = [sent.string.strip() for sent in doc.sents]
			for sent in range(len(sentences)):
				capture={}
				pos_list=[]
				for i in range(0,len(query),2):
					if QueryProcessor.EvaluateExp(query[i+1],sentences[sent])!=None:
						try:
							capture[query[i]].append([sentences[sent],QueryProcessor.EvaluateExp(query[i+1],sentences[sent])])
						except:
							capture[query[i]]=([sentences[sent],QueryProcessor.EvaluateExp(query[i+1],sentences[sent])])
			
				if len(capture.keys())<=len(query)//2 and len(capture.keys())>0:
					pos=[]
					for i_ in capture.keys():
						try:
							final_capture[i_].append(capture[i_])
						except KeyError:
							final_capture[i_]=[]
							final_capture[i_].append(capture[i_])
						for j_ in capture[i_][1]:
							pos.append(j_)
					final.append([sentences[sent],pos])
					
					ctr=0
					s=''
					for j in pos:
						s=s+sentences[sent][ctr:j[0]]+'<WORD>'+sentences[sent][j[0]:j[1]]+'</WORD>'
						ctr=j[1]+1
					s=s+sentences[sent][ctr:]
					results=results+s+'\n'

		if self.mode==1:
			return final_capture
		else:
			return results


	def MultiWordCombos(self,query):
		results=''
		final=[]
		final_capture={}
		n_vars=self.query.count(':')
		query=(re.split(r"\s(?=\w+:)|:",query))

		for itr in range(1,len(query),2):
			query[itr]=(re.sub(r"\s(?=(word|lemma|tag|entity)=)",",",query[itr]))


		for i in range(0,len(query),2):
			obj=Field(query[i+1],self.db,1)
			temp=obj.CheckQuery()
			try:
				final_capture[query[i]].append(temp)
			except:
				final_capture[query[i]]=(temp)

		
		keys=list(final_capture.keys())
		for k in range(len(keys)):
			for i_ in final_capture[keys[k]]:
					ctr=0
					s=''
					for j in i_[1]:
						s=s+i_[0][ctr:j[0]]+'<WORD>'+i_[0][j[0]:j[1]]+'</WORD>'
						ctr=j[1]+1
					s=s+i_[0][ctr:]
					results=results+s+'\n'			

		if self.mode==1:
			return final_capture
		else:
			return results


	
	def MultiWordOptional(self,query):
		results=''
		final_capture={}
		final=[]
		query=(re.split(r"\s(?=\w+:)|:|\s\(",query))
		query=QueryProcessor.RemoveBrackets(query)
		optional=0
		for itr in range(0,len(query),2):
			if '?' in query[itr]:
				query[itr]=query[itr].replace('?','')
				optional=optional+1

		for i in range(0,len(query),2):
			obj=Field(query[i+1],self.db,1)
			temp=obj.CheckQuery()
			try:
				final_capture[query[i]].append(temp)
			except:
				final_capture[query[i]]=(temp)

		keys=list(final_capture.keys())
		for k in range(len(keys)):
			for i_ in final_capture[keys[k]]:
	
					ctr=0
					s=''
					for j in i_[1]:
						s=s+i_[0][ctr:j[0]]+'<WORD>'+i_[0][j[0]:j[1]]+'</WORD>'
						ctr=j[1]+1
					s=s+i_[0][ctr:]
					results=results+s+'\n'

		if self.mode==1:
			return final_capture
		else:
			return results



	def CheckQuery(self):		
		if '|' in self.query and '?' not in self.query:
			#q21='Coating:word=coating Property:word=stainless|word=carbon|steel'
			return(self.MultiWordCombos(self.query))
		elif '?' in self.query:
			#q22='(?Coating:word=coating) Property: anti-corrosive|anti-corrosion (?Coating:word=coating)'
			return(self.MultiWordOptional(self.query))
		else:
			#q20='Ingredient:word=stainless steel
			return(self.MultiPair(self.query))

	
			
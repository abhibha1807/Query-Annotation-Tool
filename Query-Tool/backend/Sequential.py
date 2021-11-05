from backend.Boolean import Boolean
import re
from backend.QueryProcessor import QueryProcessor
from spacy.lang.en import English 
nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))
from backend.Boolean import Boolean
from backend.CaptureGroups import CaptureGroups
from backend.Field import Field




class Sequential:
	def __init__(self,query,db,mode=0):
		self.query=query
		self.db=db
		self.mode=mode

	def ParseQuery(self,query):
		results=''
		temp={}
		query=query.split(',')
		no=len(query)

		ctr=0

		for i in range(len(query)):
			if '?' in query[i]:
				obj=CaptureGroups(query[i],self.db,mode=1)
				capture=obj.CheckQuery()
				temp[ctr]=capture
			elif 'word' in query[i] or 'lemma' in query[i] or 'tag' in query[i] or 'entity' in query[i]:
					if ':' not in query[i]:
						obj=Field(query[i],self.db,mode=1)
						field=obj.CheckQuery()
						temp[ctr]=field
					else:
						obj=CaptureGroups(query[i],self.db,mode=1)
						capture1=obj.CheckQuery()
						temp[ctr]=capture1
			else:
				if ':' not in query[i]:
					obj=Boolean(query[i],self.db,mode=1)
					bool_=obj.CheckQuery()
					temp[ctr]=bool_
				else:
					obj=CaptureGroups(query[i],self.db,mode=1)
					capture2=obj.CheckQuery()
					temp[ctr]=capture2
			ctr=ctr+1



		for i in temp.values():
			if type(i)==list:
				if len(i)==0:
					print('results don\'t exist')
					return ''
			else:
				if [] in i.values():
					print('results don\'t exist')
					return ''


		total=[]

		for i_ in temp.keys():
			if type(temp[i_])==dict:
				for j_ in temp[i_].values():
					for k_ in j_:
						total.append(k_)

			else:
				print(temp[i_],'\n')
				for j in temp[i_]:
					total.append(j)


		intersect=[]

		for i_ in range(len(total)):
			for j_ in range(i_+1,len(total)):
				if total[i_][0]==total[j_][0]:
					l=total[i_]
					for k_ in total[j_][1]:
						l[1].append(k_)
					intersect.append(l)




		for p in intersect:
			ctr=0
			s=''
			for j in p[1]:
				s=s+p[0][ctr:j[0]]+'<WORD>'+p[0][j[0]:j[1]]+'</WORD>'
				ctr=j[1]+1
			s=s+p[0][ctr:]
			results=results+s+'\n'
		return results



	def CheckQuery(self):
		return(self.ParseQuery(self.query))



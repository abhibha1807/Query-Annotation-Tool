from __future__ import unicode_literals, print_function
import json
import re
from spacy.lang.en import English 
nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer')) # updated
import itertools
from itertools import combinations 
from itertools import permutations  
import nltk
from nltk.stem import WordNetLemmatizer  
from nltk.tokenize import word_tokenize, sent_tokenize
import itertools
from itertools import combinations 
from itertools import permutations  
lemmatizer = WordNetLemmatizer() 
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
nlptok = English()
tokenizer = Tokenizer(nlptok.vocab)
import spacy
model=spacy.load('/Users/abhibhagupta/Desktop/TCS/NER/recommender_system/frontend/tkinter_app/backend/myMdl')
import ast

class QueryProcessor:

#fucntions toparse word,lemma,entity and POS tag
	def Word(sentence,query):
		pos_list=[]
		for i in range(len(sentence)):
			if sentence.startswith(' '+query+' ',i):
				pos_list.append([i,i+len(query)+1])
		return pos_list

	def Lemma(sentence,query):
		pos_list=[]
		pos=0
		tokens=tokenizer(sentence)
		for word in tokens:
			if query==lemmatizer.lemmatize(str(word)):
				pos_list.append([pos,pos+len(word)+1])
			pos=pos+len(word)+1
		print('_______',pos_list)
		return pos_list

	def Entity(sentence,query):
		pos_list=[]
		doc = model(sentence)
		for ent in doc.ents:
			pos=0
			if ent.label_==query:
				pos_list.append([ent.start_char,ent.end_char])
		return pos_list

	def PosTag(sentence,query):
		pos_list=[]
		pos=0
		wordsList = nltk.word_tokenize(sentence)
		tagged = nltk.pos_tag(wordsList) 
		for t in tagged:
			if t[1]==query:
				pos_list.append([pos,pos+len(t[0])])
			pos=pos+len(t[0])+1
		
		return pos_list

	#helper fucntions for parsing query
	def Combinations(query):
		#returns combinations of a list of lists.
		return(list(itertools.product(*query)))

	# def RemoveSpaces(query):
	# 	#removes extra whitespace at the end of a word
	# 	#eg: word=steel_ (_ is an extra space in the end)
	# 	#print('ping',query)
	# 	try:
	# 		l=query.split('=')
	# 		if l[1][-1]==' ':
	# 			l[1]=l[1][:len(l[1])-1]
	# 		return '='.join(l)
	# 	except: 
	# 		return query

	# def RemoveEmptyTuples(query):
	# 	# removes tuples containing '' elements
	# 	l=[]
	# 	for i in query:
	# 		if i[0]!='':
	# 			l.append([i[0],i[1]])
	# 	return l

	# def RemoveNone(query):
	# 	#removes None elements from a list/tuple
	# 	query=list(query)
	# 	res = [i for i in query if i] 
	# 	return res

	def RemoveBrackets(query):
		#removes start and end brackets from a query
		for i in range(len(query)):
			query[i]=query[i].replace('(','')
			query[i]=query[i].replace(')','')
		return query

	# def RemoveNull(query):
	# 	#removes elements of the form '' from a list
	# 	return([i for i in query if i!=''])

	def EvaluateExp(q,sent):
		if q.split('=')[0]=='word':
			if QueryProcessor.Word(sent,q.split('=')[1])!=[]:
				return(QueryProcessor.Word(sent,q.split('=')[1]))

		elif q.split('=')[0]=='lemma':
			if QueryProcessor.Lemma(sent,q.split('=')[1])!=[]:
				return(QueryProcessor.Lemma(sent,q.split('=')[1]))

		elif q.split('=')[0]=='entity':
			if QueryProcessor.Entity(sent,q.split('=')[1])!=[]:
				return(QueryProcessor.Entity(sent,q.split('=')[1]))

		elif q.split('=')[0]=='tag':
			if QueryProcessor.PosTag(sent,q.split('=')[1])!=[]:
				return(QueryProcessor.PosTag(sent,q.split('=')[1]))
		else:
			if QueryProcessor.Word(sent,q.split('=')[0])!=[]:
				return(QueryProcessor.Word(sent,q.split('=')[0]))

	#parses and returns the particular section of the file in the database.
	def get_db(ip_filename,section):
		l=[]
		try:
			with open(ip_filename, 'r') as f:
				s = f.read()
				d=ast.literal_eval(s)
				l.append(d[section])
			f.close()
		except:
			pass

		return l




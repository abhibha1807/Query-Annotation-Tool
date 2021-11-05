from tkinter import *
from tkinter.filedialog import asksaveasfilename
from backend.QueryParser import QueryParser
import pandas as pd
import numpy as np
import csv
import ast
import itertools

ent_dict={}
MUL_ENTS={}

def get_query(text,ip_filepath,section):
	obj=QueryParser(text,ip_filepath,section)
	return(obj.ParseQuery())


#helper function for writing to file
def flatten(v):
	return(np.array(list(itertools.zip_longest(*v, fillvalue=''))).T)

def write_to_file(filename,d):
	cols=list(d.keys())
	temp=[]
	for c in cols:
		t=[]
		for l in d[c]:
			t.append(l[2])
		temp.append(t)
	temp=flatten(temp)
	print('captured!!!',temp)
	df=pd.DataFrame(columns=cols)
	for c in range(len(cols)):
		df[cols[c]]=temp[c]
	print(df.head())
	df.to_csv(filename)

def export_as(mode,query):
	if query.count(':')==1:
		file=query.split(':')[0]
		file=file+'.csv'
	else:
		files = [('CSV Document', '*.csv')] 
		file = asksaveasfilename(filetypes = files, defaultextension = '.csv') 
	
	if mode==1:
		if MUL_ENTS!={}:
			write_to_file(file,MUL_ENTS)
		else:
			print('nothing to export')	
	else:
		if ent_dict!={}:
			write_to_file(file,ent_dict)
		else:
			print('nothing to export')

def export_as_search(results):
	files = [('CSV Document', '*.csv')] 
	file = asksaveasfilename(filetypes = files, defaultextension = '.csv') 
	if type(results)==list:
		file = open(file, 'w+', newline ='') 
		with file:     
			write = csv.writer(file) 
			write.writerows(results)
	else:
		 write_to_file(file,results)




def adding_again(d,start,end):
	f=0
	for k in d.keys():
		for l in d[k]:
			if l[0]==start and l[1]==end:
				f=1
				return 1
	return 0



def create_dict(key,name,start=None,end=None,add=0):
	print('adding in dict',name,start,end)
	if add==0:
		try:
			ent_dict[key].append([start,end,name])
		except:
			ent_dict[key]=[]
			ent_dict[key].append([start,end,name])
		
	else:
		if adding_again(ent_dict,start,end)==1:
			print('entry already exists')
		else:
			try:
				ent_dict[key].append([start,end,name])
			except:
				ent_dict[key]=[]
				ent_dict[key].append([start,end,name])
	print(ent_dict)
			

def create_muldict(key,name,start=None,end=None,add=0):
	global MUL_ENTS
	print('adding in dict',name)
	if add==0:
		MUL_ENTS[key].append([start,end,name])
		print(MUL_ENTS)
	else:
		if adding_again(MUL_ENTS,start,end)==1:
			print('entry already exists')
	print(MUL_ENTS)

#initialize relational entity tagging dict
def create_mulents(key):
	global MUL_ENTS
	MUL_ENTS[key]=[]

#initialize dicts again
def clear_dicts():
	print('dicts initialised')
	global MUL_ENTS
	MUL_ENTS={}
	global ent_dict
	ent_dict={}
	print(MUL_ENTS,ent_dict)



# helper functions
#function to get section names for a particular file
def getOptions(filename):
	with open(filename, 'r') as f:
	    s = f.read()
	    d=ast.literal_eval(s)
	f.close()
	return set(d.keys())

#get instructions from the instructions file
def getInstruct(file):
	with open(file,'r') as f:
		instruct_txt=f.read()
	f.close()
	return(instruct_txt)

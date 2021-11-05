
import csv
import pandas as pd
import numpy as np
import json
from collections import Counter
from collections import defaultdict 
import csv
import os
import re

anything=re.compile('(.*)')


for i in range(2,100):
	fnum='{0:04}'.format(i)

	result = {}
	try:
		with open('amcpe_mw/amcpe_mpq'+fnum+'.csv', 'r') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in csvreader:
				if row[6] in result:
					result[row[6]]=[]
				else:
					result[row[6]]=[]
	except:
		continue
	
	with open('amcpe_mw/amcpe_mpq'+fnum+'.csv', 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in csvreader:
			for j in row[10].split('|'):
				sind=row[6].find(j)
				eind=sind+len(j)
				if sind!=-1 and eind!=1:
					result[row[6]].append([sind,eind,'CONDITION'])

			

			for j in row[9].split('|'):
				sind=row[6].find(j)
				eind=sind+len(j)
				if sind!=-1 and eind!=1:
					result[row[6]].append([sind,eind,'QUANTITY'])

		
			for j in row[8].split('|'):
				sind=row[6].find(j)
				eind=sind+len(j)
				if sind!=0 and eind!=0:
					result[row[6]].append([sind,eind,'PROCESS'])

			for j in row[7].split('|'):
				sind=row[6].find(j)
				eind=sind+len(j)
				if sind!=0 and eind!=0:
					result[row[6]].append([sind,eind,'MOLECULE'])


			for j in row[2].split('|'):
				sind=row[6].find(j)
				eind=sind+len(j)
				if sind!=0 and eind!=0:
					result[row[6]].append([sind,eind,'ACTION'])


		
	

	temp={}
	with open('ip_to_doccano/together'+fnum+'.txt', 'a') as file:
		for itr in (result).keys():

			if itr=='\n' or itr == 'sent':
				continue
			l=[]
			print(result[itr])
			for p in range(len(result[itr])):
				f=0
				for q in range(p+1,len(result[itr])):
					for t in range(len(result[itr][q])-1):
						if result[itr][p][t]==result[itr][q][t]:
							print(result[itr][p][t],result[itr][q][t])
							f=1
							# break
				if f==0:
					l.append(result[itr][p])
				
			result[itr]=l
			print(l)

			temp['text']=itr
			temp['labels']=result[itr]
			file.write(json.dumps(temp))
			file.write('\n')
	file.close()


	os.rename('ip_to_doccano/together'+fnum+'.txt', 'ip_to_doccano/together'+fnum+'.json')		

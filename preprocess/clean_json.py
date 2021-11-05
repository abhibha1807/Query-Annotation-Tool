# remove [-1,1,condition/quantity] to form condn/quan tags cleaned folders.
import ast
import json
import os
for i in range(2,100):
	fnum='{0:04}'.format(i)
	try:
		with open('ip_to_doccano_concatenated/together'+fnum+'.json','r') as f:
		  data=f.readlines()
		f.close()
	except:
		pass

	for i in range(len(data)):
		temp={}
		data[i]=data[i].replace('\n','')
		temp = ast.literal_eval(data[i])
		try:
			while True:
				temp['labels'].remove([-1, 1, "CONDITION"])
				temp['labels'].remove([-1, 1, "QUANTITY"])
		except ValueError:
			pass

		with open('ip_to_doccano_concatenated_clean/together'+fnum+'.txt', 'a') as file:
			file.write(json.dumps(temp))
			file.write('\n')

	os.rename('ip_to_doccano_concatenated_clean/together'+fnum+'.txt', 'ip_to_doccano_concatenated_clean/together'+fnum+'.json')		

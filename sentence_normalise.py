for i in range(3,100):
	print(i)
	fnum='{0:04}'.format(i)
	with open('sentence_ip_to_tagger/sentence_ip_to_tagger_'+fnum+'.txt','r') as f:
		data=f.readlines()
	f.close()

	# print(data)
	for i in range(len(data)):
		data[i]=' '.join(data[i].split())

	with open('sentence_wise_normalised_ip_to_tagger/sentence_ip_to_tagger_'+fnum+'.txt','a') as f:
		for j in data:
			f.write(j)
			f.write('\n')
	f.close()

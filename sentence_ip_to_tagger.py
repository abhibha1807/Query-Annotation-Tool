
from __future__ import unicode_literals, print_function
from spacy.lang.en import English 
nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer')) # updated

for i in range(2,100):
	
	fnum='{0:04}'.format(i)
	print(fnum)
	with open("ip_to_tagger/ip_to_tagger_"+fnum+".txt", "r") as file:
		text=file.readlines()
	file.close()

	txt=''
	for i in range(len(text)):
		text[i]=text[i].replace('\n','')
		txt=txt+text[i]+' '

	doc = nlp(txt)
	sentences = [sent.string.strip() for sent in doc.sents]

	with open("sentence_ip_to_tagger/sentence_ip_to_tagger_"+fnum+".txt", "a") as file:
		for i in sentences:
			file.write(i)
			file.write('\n')

	file.close()


	
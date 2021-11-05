mport spacy
import random
import json
from zipfile import ZipFile
from nltk.tokenize import word_tokenize, sent_tokenize 
# import neuralcoref
TRAIN_DATA=[]
TEST_DATA=[]
DATA=[]
# with ZipFile('/Users/abhibhagupta/TCS/NER/annotations/op_doccano/together.zip', 'r') as zf:
#   zf.printdir()
#   #Extracting the files from zip file
#   zf.extractall()
#   print('Zip Extraction Completed')

for i in range(2,100):
  fnum='{0:04}'.format(i)
  print(fnum)
  try:
      with open('/Users/abhibhagupta/Desktop/TCS/NER/annotations/op_doccano/together/'+fnum+'.json') as f:
          data=f.readlines()
      f.close()
  except:
      continue

  if type(data)==list:
      temp=json.loads(data[0])
  try:
      temp.pop('id')
  except:
      pass

  #print(temp)

  l=[]
  labels={'entities':[]}
  for j in range(len(temp['labels'])):
      f=0
      for k in range(j+1,len(temp['labels'])):
        l1=[x for x in range(temp['labels'][j][0],temp['labels'][j][1]+1)]
        l2=[x for x in range(temp['labels'][k][0],temp['labels'][k][1]+1)]
        if bool(set(l1)&set(l2))== True:
          f=1
          break
      
      if f ==0:
          l.append(temp['labels'][j])
  temp['labels']=l

  
  

  DATA.append((temp['text'],{'entities':[tuple(x) for x in temp['labels']]}))
print(len(DATA))


import random
dataset_size=len(DATA)
test_size=(10*44)/100
instance_no=set()
for i in range(int(test_size)):
  n=random.randint(0,dataset_size-1)
  instance_no.add(n)
for j in instance_no:
  TEST_DATA.append(DATA[j])
for k in range(dataset_size):
  if k not in list(instance_no):
    TRAIN_DATA.append(DATA[k])
print(len(TRAIN_DATA))
print(len(TEST_DATA))


def train_spacy(data,iterations):
    TRAIN_DATA = data
    nlp = spacy.blank('en')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
        # nlp.add_pipe(nlp.create_pipe('sentencizer')) #Adding sentencizer as a prerequisite to coref
        # neuralcoref.add_to_pipe(nlp) #Adding corefering in the pipeline
       

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return nlp


prdnlp = train_spacy(TRAIN_DATA, 25)

# Save our trained Model
# modelfile = input("Enter your Model Name: ")
modelfile= 'myMdl'
prdnlp.to_disk(modelfile)

#Test your text
# test_text = s
y_pred=[]
for i in TEST_DATA:
  doc = prdnlp(i[0])
  l=[]
  for ent in doc.ents:
    l.append(ent.start_char)
  y_pred.append(l)



y_true=[]
for i in range(len(TEST_DATA)):
  l=[]
  for j in range(len(TEST_DATA[i][1]['entities'])):
    s=''
    # print(TEST_DATA[i])
    for k in range(TEST_DATA[i][1]['entities'][j][0],TEST_DATA[i][1]['entities'][j][1]):
      s=s+(TEST_DATA[i][0][k])
    #print(s)
    l.append(TEST_DATA[i][1]['entities'][j][0])
  y_true.append(l)


tp=0
fp=0
tn=0
fn=0


for itr in range(len(TEST_DATA))
  tp=tp+len(set(y_true[itr])&set(y_pred[itr]))

for itr in range(len(TEST_DATA)):
  for i in y_pred[itr]:
    if i in y_true[itr]:
      tp=tp+1
    if i not in y_true[itr]:
      fp=fp+1
  
    
  for i in y_true[itr]:
    if i not in y_pred[itr]:
      fn=fn+1

print(tp)
print(fp)
print(fn)
p=tp/(tp+fp+1)
r=tp/(tp+fn+1)
f1=(2*r*p)/(r+p+1)

print(p,r,f1)


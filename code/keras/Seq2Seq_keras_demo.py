import json
import tensorflow
import tensorflow as tf
from keras.models import model_from_json
import tensorflow_hub as hub
import numpy as np
from tabulate import tabulate
'''
{'ACTIONS': 2,
 'CONDITIONS': 0,
 'MOLECULES': 1,
 'OTHER': 5,
 'PROCESS': 4,
 'QUANTITY': 3}

{0: 'CONDITIONS', 1: 'MOLECULES', 2: 'ACTIONS', 3: 'QUANTITY', 4: 'PROCESS', 5: 'OTHER'}
 '''


#load json and create model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("model.h5")
# print("Loaded model from disk")


# reloaded_model = tf.compat.v1.keras.experimental.load_from_saved_model('path_to_my_model.h5', custom_objects={'FunctionalLayer':hub.KerasLayer})
# print(reloaded_model.get_config())

# #Get input shape from model.get_config()
# reloaded_model.build((None, 224, 224, 3))
# reloaded_model.summary()

import tensorflow as tf
tf.compat.v1.disable_eager_execution()

batch_size = 2
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.python.keras import backend as K
sess=tf.compat.v1.Session()
tf.compat.v1.keras.backend.set_session(sess)

elmo_model = hub.Module("https://tfhub.dev/google/elmo/2", trainable=True)
sess.run(tf.compat.v1.global_variables_initializer())
sess.run(tf.compat.v1.tables_initializer())
max_len=30
n_tags=6
def ElmoEmbedding(x):
    return elmo_model(inputs={
                            "tokens": tf.squeeze(tf.cast(x, tf.string)),
                            "sequence_len": tf.constant(batch_size*[max_len])
                      },
                      signature="tokens",
                      as_dict=True)["elmo"]


from tensorflow.python.keras.models import Model, Input
from tensorflow.python.keras.layers.merge import add
from tensorflow.python.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional, Lambda

input_text = Input(shape=(max_len,), dtype=tf.string)
embedding = Lambda(ElmoEmbedding, output_shape=(max_len, 1024))(input_text)
x = Bidirectional(LSTM(units=512, return_sequences=True,
                       recurrent_dropout=0.2, dropout=0.2))(embedding)
x_rnn = Bidirectional(LSTM(units=512, return_sequences=True,
                           recurrent_dropout=0.2, dropout=0.2))(x)
x = add([x, x_rnn])  # residual connection to the first biLSTM
out = TimeDistributed(Dense(n_tags, activation="softmax"))(x)

model = Model(input_text, out)
model.compile(optimizer="adam", loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))


model.load_weights("model.h5")

# filename = sys.argv[-1]
ctr=0
final={}
final[ctr]=[]
for i in range(2,100):
    fnum='{0:04}'.format(i)
    #print(fnum)
    try:
      with open('/Users/abhibhagupta/Desktop/TCS/NER/annotations/op_doccano/together/'+fnum+'.json') as f:
        data=f.readlines()
      f.close()
    except:
      continue
    if type(data)==list:
      data=json.loads(data[0])
    try:
      data.pop('id')
    except:
      pass



    for itr in range(len(data['labels'])):
      s=''
      for j in range(data['labels'][itr][0],data['labels'][itr][1]+1):
        s=s+data['text'][j]
      final[ctr].append((s,data['labels'][itr][2]))
      if len(final[ctr])==30:
        ctr=ctr+1
        final[ctr]=[]
    
max=0
for i in final.keys():
  if len(final[i])>max:
    max=len(final[i])
#print(max)

words=set()
for i in final.values():
  for x in i:
    words.add(x[0])
words.add('PADword')
n_words = len(words)
#print(n_words)

tags=set()
for i in final.values():
  for x in i:
    tags.add(x[1])
n_tags = len(tags)
# n_tags

words2index = {w:i for i,w in enumerate(words)}
# tags2index = {t:i for i,t in enumerate(tags)}
tags2index={'ACTIONS': 2,
 'CONDITIONS': 0,
 'MOLECULES': 1,
 'OTHER': 5,
 'PROCESS': 4,
 'QUANTITY': 3}
# print(words2index['used'])
# print(tags2index['ACTIONS'])


test_list=[['15 min ',
  '15 min ',
  '20 ° C ',
  'CS)',
  'C,',
  '0.46wt%M',
  '0.27wt%S',
  '0.11wt%C',
  '0.09wt%N',
  '0.01wt %P',
  'P ',
  '0.15wt %C',
  '10 mm X 10 mm ',
  '400 ',
  '1200 grit.',
  '1h.',
  'NiSO4.6H2O)',
  'Nickel Sulphate(',
  '28 ',
  'Sodium hypophosphite(',
  'NaH2PO2)',
  '20 ',
  'Sodium citrate(',
  'C6H8Na3.2H2O)',
  '35 ',
  'Lactic Acid ',
  '5 ',
  'Ammonium Sulphate(',
  'NH4SO4)',
  '30 '],
 ['determine ',
  'coated ',
  'purchased ',
  'Sodium silicate ',
  'Sodium hydroxide ',
  'epoxy ',
  'KBr ',
  'sodium hydroxide ',
  'Na:',
  'Al ',
  'Si:',
  'setting time analysis ',
  'dip coating ',
  '1.13 mm ',
  '300g ',
  '45 µm ',
  'NaOH)',
  'steel ',
  '3mm x 50mm x 127mm)',
  'Demineralized water,',
  '5 minutes.',
  'steel ',
  '60oCf',
  '28 days ',
  'constant temperature.',
  'Water ',
  'AL ',
  ' 60oC ',
  '28 days ',
  '60oC '],
  ]



test_pred = model.predict(np.array(test_list), verbose=1)

idx2tag = {i: w for w, i in tags2index.items()}
def pred2label(pred):
    out = []
    for pred_i in (pred):
      out_i = []
      for p in (pred_i):
          p_i = np.argmax(p)
          out_i.append(idx2tag[p_i].replace("PADword", "O"))
      out.append(out_i)
    return out
pred_labels = pred2label(test_pred)

table=[]
table.append(["WORD","TAG"])
for i in range(len(test_list)):
		for j in range(len(test_list[i])):
			table.append([test_list[i][j],pred_labels[i][j]])

print(tabulate(table,headers="firstrow"))

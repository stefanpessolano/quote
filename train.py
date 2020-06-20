# -*- coding: utf-8 -*-
"""quo-Copy1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hUTfVS_MBxel_4d9skjHqKRvB-xOMZt6
"""

import numpy as np
import tensorflow as tf

path = "inspiration.txt"

quotes = open(path,'r').read()

uniqueCharacters = sorted(set(quotes))

uniqueCharacters.insert(0,'')

ctoi = {c:i for i,c in enumerate(uniqueCharacters)}

itoc = {i:c for i,c in enumerate(uniqueCharacters)}

quotes = str.splitlines(quotes)

encodedQuotes = []
for c in quotes:
    temp = []
    for i in range(len(c)):
        temp.append(ctoi[c[i]])
    encodedQuotes.append(temp)

def ngram(item):
    output = []
    for quote in item:
        for i in range(len(quote)):
            output.append(quote[:i+1])
    return output

sequence = ngram(encodedQuotes)

maxLength = max(len(i) for i in sequence)

paddedSequence = np.array(tf.keras.preprocessing.sequence.pad_sequences(sequence,
                                                      maxlen=maxLength,
                                                      padding='pre',
                                                      value=0))

x = paddedSequence[:,:-1]
labels = paddedSequence[:,-1]
y = tf.keras.utils.to_categorical(labels,num_classes=len(uniqueCharacters))

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM,Embedding,Bidirectional,Dropout,Lambda



def createModel():
    temperature = 1.2
    model = Sequential()
    model.add(Embedding(len(uniqueCharacters),64,input_length=maxLength-1))
    model.add(Bidirectional(LSTM(256,return_sequences=True)))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(256,return_sequences=True)))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(256)))
    model.add(Dropout(0.2))

    model.add(Lambda(lambda x: x / temperature))
    model.add(Dense(len(uniqueCharacters),activation='softmax'))

    model.compile('adam',loss='categorical_crossentropy',metrics=['accuracy'])
    return model

model = createModel()
#model.summary()

#model.fit(x,y,epochs=25,verbose=1)

seed = ''
numChar = 100

def generateQuotes(model,seed,numChar):
  for i in range(numChar):
      encodedSeedSequence = []
      encodedSeed = []
      for i in range(len(seed)):
          encodedSeed.append(ctoi[seed[i]])
      if(len(seed) == 0):
          encodedSeed.append(ctoi[seed])
      encodedSeedSequence.insert(0,encodedSeed)
      paddedSeed = np.array(tf.keras.preprocessing.sequence.pad_sequences(encodedSeedSequence,
                                                      maxlen=maxLength-1,
                                                      padding='pre',
                                                      value=0))
      output = model.predict(paddedSeed)
      prediction = np.random.choice(len(uniqueCharacters),p=output[0])
      prediction = itoc[prediction]
      seed = seed + prediction
  periodIndex = seed.rfind('.')
  if(periodIndex != -1):
    seed = seed[0:periodIndex+1]
  return seed

#print(generateQuotes(model,seed,numChar))

#model.save('quotes.h5')


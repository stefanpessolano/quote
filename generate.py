import numpy as np
import os
import tweepy
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from tensorflow.keras.models import load_model

from train import createModel,generateQuotes

#Load the model
model = createModel()
model.load_weights('quotes.h5')
model.build(tf.TensorShape([1,None]))


auth = tweepy.OAuthHandler(key,secret_key)

auth.set_access_token(token,secret_token)
api = tweepy.API(auth)

seed = input("Seed: ") 
length = input("Length: ") 

quotes = []
for i in range(5):
    quote = generateQuotes(model,seed,int(length))
    quotes.append(quote)
    print(str(i+1)+'. '+quote)

quotenum = input("Which quote?(1-5)")
quotenum = int(quotenum)-1
quote = quotes[quotenum]

response = input("Post quote?(y/n)")
if response == 'y':
    api.update_status(quote)
    print('Tweet posted!')
if response == 'n':
    print('Tweet not posted')

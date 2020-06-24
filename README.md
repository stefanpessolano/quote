# quote
Quote generator using tensorflow. This is my first try creating a text generator using RNNs and Tensorflow. I tried preprocessing the data by using ngrams and splitting the last character to use as the labels rather than using the more common approach of the sliding window. I found due to my small amount of data (there's a limit to motivational quotes before
they start being the same), the ngrams created more unique quotes. By using the sliding window, the model would either not train or overtrain and it wasn't creating good quotes. 

This again is my first attempt at tensorflow and using it to generate text, so what I could be saying could be completely wrong. These are just observations I made messing around with the code.

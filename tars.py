# required modules
import random
import json
import pickle
import numpy as np
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
from apisource import apiQuery
from keras.utils import pad_sequences
from tokentrain import loadTokenizer
import os
from fuzzywuzzy import fuzz, process
import math
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
lemmatizer = WordNetLemmatizer()
apiquery = apiQuery()
# Load files created in training
print("Loading intents....")
intents = json.loads(open("training.json", encoding="utf8").read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
print("Loading TARS....")
model = load_model('tars.h5')
print("Loading tokenizer...")
tokenizer = loadTokenizer.load_tokenizer()
tokenizer_words = [key for key, value in tokenizer.word_index.items()]
if "<OOV>" in tokenizer.word_index:
    tokenizer.word_index["<OOV>"] = len(tokenizer.word_index) + 1
else:
    tokenizer.word_index.setdefault("<OOV>", len(tokenizer.word_index) + 1)
print("=====================================================================")
# Seperate words from sentences we feed as input
def clean(sentence):
    # Corrects spelling mistakes
    corrected_sentence = []
    ignore_letters = ["?", "!", ".", ",", "'", ":", ";", "(",")", "-", "_"]
    for word in sentence.split():
        corrected_word = process.extractOne(word.lower(), words, scorer=fuzz.token_sort_ratio)
        if (corrected_word[1] < 75 or len(word) < 4):
            corrected_sentence.append(word)
        else:
            corrected_sentence.append(corrected_word[0])
    sentence = " ".join(corrected_sentence)
    
    # Lemmatizes the sentence
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word).lower()
                      for word in sentence_words if word not in ignore_letters]
    return sentence_words
# Predict the class of the sentence input by user
#
def predict_class(sentence):
    tokens = tokenizer.texts_to_sequences([sentence])
    tokens = pad_sequences(tokens, maxlen=len(words))
    res = model.predict(np.array(tokens), verbose=0)
    pred = np.argmax(res)
    if (res[0,pred] < 0.832):
        return classes[classes.index('gptQuery')]
    return classes[pred]

# get_response(intents_list, intents_json) generates response from sentence class
def get_response(tag, intents_json, message): 
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['tag'] == tag:
            print(tag)
            # Generate a response
            if i['tag'] == 'gptQuery':
                data_result = apiquery.queryGPT(message)
            elif i['tag'] == 'currentTemperature':
                data_result = apiquery.queryWeather(tag)
                result = random.choice(i['responses']).format(data_result)
            elif i['tag'] == 'currentDewPoint':
                data_result = apiquery.queryWeather(tag)
                result = random.choice(i['responses']).format(data_result, "{:.2f}".format(data_result * 9 / 5 - 459.67))
            elif i['tag'] == 'currentWind':
                data_result = apiquery.queryWeather(tag)
                directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
                result = random.choice(i['responses']).format(data_result[0], directions[math.floor(int(data_result[1] + 22.5) / 45 % 8)])
            elif i['tag'] == 'currentUvi':
                data_result = apiquery.queryWeather(tag)
                result = random.choice(i['responses']).format(data_result)
            elif  i['tag'] == 'dailyHighTemp':
                data_result = apiquery.queryWeather(tag)
                result = random.choice(i['responses']).format(data_result)
            elif i['tag'] == 'dailyLowTemp':
                data_result = apiquery.queryWeather(tag)
                result = random.choice(i['responses']).format(data_result)
            elif i['tag'] == 'dailyRain':
                data_result = apiquery.queryWeather(tag)
                result = random.choice(i['responses']).format(data_result)
            elif i['tag'] == 'dailySunset':
                data_result = apiquery.queryWeather(tag)
                result = random.choice(i['responses']).format(data_result)
            else:
                result = random.choice(i['responses'])
            break
    return result

print("Waking up TARS....")
print("TARS is awake. How can I help you?")
# Conversation loop
flag=True
while (flag==True):
    message = clean(input(""))
    data = predict_class(message)
    res = get_response(data, intents, message)
    # If intent is current temperature, inject temperature into response]
    if(data == "shutdown"):
        flag = False 
    elif(data == "gptQuery"):
         res = apiquery.queryGPT(message)
    print("TARS: ", res)

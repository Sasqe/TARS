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
from tokentrain import load_tokenizer
import os
from fuzzywuzzy import fuzz, process
import math

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Set LOG lvl to 3
lemmatizer = WordNetLemmatizer() # Create NLTK Lemmatizer to lemmatize words
apiquery = apiQuery() # Import apisource.py to query APIs

# Load files created in training
print("Loading language processing dependencies....")
intents = json.loads(open("training.json", encoding="utf8").read()) # intents.json to generate intent responses
words = pickle.load(open('words.pkl', 'rb')) # words.pkl contains the vocabulary that TARS was trained on
classes = pickle.load(open('classes.pkl', 'rb')) # classes.pkl contains the classes that TARS was trained to make predictions on

print("Loading TARS....")
model = load_model('tars.h5') # load TARS's memory from .h5 file

# Keras tokenizer contains TARS' vocab dictionary, as well as it's word vector matrix
print("Loading tokenizer...")
tokenizer = load_tokenizer() # Import tokentrain.py to load Keras tokenizer, update its OOV vector index, and update it's pickle.
tokenizer_words = [key for key, value in tokenizer.word_index.items()] # tokenizer_words contains the words in the word index
    
# ========================================== TARS is ready to go ======================================================================

# Function to clean user input
def clean(sentence):
    corrected_sentence = [] # List to store corrected words
    ignore_letters = ["?", "!", ".", ",", "'", ":", ";", "(",")", "-", "_"] # List of characters to ignore
    for word in sentence.split():# For each word in the sentence
        corrected_word = process.extractOne(word.lower(), words, scorer=fuzz.token_sort_ratio) # process.extractOne() returns the word with the highest ratio
        if (corrected_word[1] < 75 or len(word) < 4): # If the word is not severely mispelled, or is too short
            corrected_sentence.append(word) # Append the original word word as is
            # ^ This is done to ignore short abbreviations, or words that are most likely irrelevant to the conversation's context
        else:
            corrected_sentence.append(corrected_word[0]) # Append corrected word
    sentence = " ".join(corrected_sentence)
    
    # Lemmatizes the sentence
    sentence_words = nltk.word_tokenize(sentence) # Use NLTK's tokenizer to tokenice the sentence
    sentence_words = [lemmatizer.lemmatize(word).lower()
                      for word in sentence_words if word not in ignore_letters] # Lemmatize words, convert to all lowercase, and remove ignore characters
    return sentence_words

# Method Predict the class of the sentence input by user
def predict_class(sentence):
    sentence = clean(sentence) # Clean the sentence
    tokens = tokenizer.texts_to_sequences([sentence]) # Use Keras tokenizer to convert words to tokens
    tokens = pad_sequences(tokens, maxlen=len(words)) # Pad tokens into vector matrix
    res = model.predict(np.array(tokens), verbose=0) # TARS makes its prediction by passing the tokens to it
    pred = np.argmax(res) # Get the index of the highest probability
    if (res[0,pred] < 0.832 and classes[pred] != 'name'): # If tars isn't too sure about what the input says
        return classes[classes.index('gptQuery')] # Set class to 'gptQuery'
                # ^ This is done to tell TARS to access GPT-3 Neural Network to generate a response
    return classes[pred] # Else, return class 

# Function to generate response
def get_response(tag, intents_json, message): 
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['tag'] == tag:
            try:
                # TARS will generate a response uniquely based on which function it needs to perform.
                # Each response has {} tags that will be formatted with the data TARS recieves from the API
                # Some responses may have mathematical operations performed on its format tags, such as converting Kelvin to Fahrenheit
                if i['tag'] == 'gptQuery':
                    result = apiquery.queryGPT(message)
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
            except:
                result = "Oops, I wasn't able to connect to the network."
    return result


def interact():
    print("Waking up TARS....")
    print("*Yawnnnnn* I'm awake i'm awake... How can I help you?")
    # Conversation loop
    flag=True
    while (flag==True):
        message = input("")
        if(message == "sleep"):
            flag = False
        else:
            data = predict_class(message)
            res = get_response(data, intents, message)
            print("TARS: ", res)
if __name__ == "__main__":
    interact()


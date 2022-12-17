# required modules
import random
import json
import pickle
import numpy as np
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Load files created in training
print("Loading intents....")
intents = json.loads(open("intents.json").read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
print("Loading TARS....")
model = load_model('tars.h5')
print("=====================================================================")
# Seperate words from sentences we feed as input
def clean_up_sentences(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word)
                      for word in sentence_words]
    return sentence_words
# Append 1 to a list variable 'bag' if word is contained inside input
def bagw(sentence):
    # Seperate words from input sentence
    sentence_words = clean_up_sentences(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            
            # Check if word is in input
            if word == w:
                bag[i] = 1
    
    # Return bag in numpy array
    return np.array(bag)

# Predict the class of the sentence input by user

def predict_class(sentence):
    # Bow contains numpy binary array
    bow = bagw(sentence)
    res = model.predict(np.array([bow]))[0]
    # Error threshold appends res if value is greater than threshold
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res)
               if r > ERROR_THRESHOLD]
    # then sort using sort function
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]],
                            'probability': str(r[1])})
        return return_list

# get_response(intents_list, intents_json) generates response from sentence class
def get_response(intents_list, intents_json): 
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['tag'] == tag:
            
            # Generate a response
            result = random.choice(i['responses'])
            break
    return result

print("Tars is up!")
# Shutdown list 
shutdownlist = ["sleep"]
# Conversation loop
flag=True
while (flag==True):
    message = input("")
    if any(message.find(shutdown) != -1 for shutdown in shutdownlist):
        print("Going to sleep...")
        flag=False
    else:
        ints = predict_class(message)
        intent = ints[0]["intent"]
        res = get_response(ints, intents)
        # If intent is current temperature, inject temperature into response
        if(intent == "currentTemperature"):
            temperature = "70"
            replaceString = "[Insert Temperature Here]"
            res = res.replace(replaceString, temperature)
        print(res)

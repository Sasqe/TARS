# importing the required modules.
import random
import json
import pickle
import numpy as np
import nltk
import mysql.connector
from keras.models import Sequential
from nltk.stem import WordNetLemmatizer
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from tarsDAO import AIDAO
# Define Lemmatizer
lemmatizer = WordNetLemmatizer()

# Instantiate DAO
tarsDAO = AIDAO()

# reading the json.intense file
intents = json.loads(open("intents.json").read())

# creating empty lists to store data
words = []
classes = []
documents = []
ignore_letters = ["?", "!", ".", ","]
for intent in intents['intents']:
	for pattern in intent['patterns']:
		# separating words from patterns
		word_list = nltk.word_tokenize(pattern)
		words.extend(word_list) # and adding them to words list
		
		# associating patterns with respective tags
		documents.append(((word_list), intent['tag']))

		# appending the tags to the class list
		if intent['tag'] not in classes:
			classes.append(intent['tag'])

# storing the root words or lemma
words = [lemmatizer.lemmatize(word)
		for word in words if word not in ignore_letters]
words = sorted(set(words))

# saving the words and classes list to binary files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))


# Convert data into binary to feed into neural network
training = []
output_empty = [0]*len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(
        word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    
    # copy of output_empty
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
random.shuffle(training)
training = np.array(training, dtype=object)

# Split data into x and y training sets
train_x = list(training[:, 0])
train_y = list(training[:, 1])
print ("HELLO")
if bool(tarsDAO.downloadTARS()):
    print("TARS MEMORY FOUND. DOWNLOADING TARS...")
    model = tarsDAO.downloadTARS()
else:
    print("TARS MEMORY NOT FOUND. RE-CREATING NEURAL NETWORK...")
    model = Sequential()
    # Neural Network layers
    model.add(Dense(128, input_shape=(len(train_x[0]), ),
                    activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), 
                    activation='softmax'))
    
# compile the model
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])
# Activate training
hist = model.fit(np.array(train_x), np.array(train_y),
                 epochs=200, batch_size=5, verbose=1)
  
# saving the model
print("Saving TARS model...")
model.save("tars.h5", hist)
tarsDAO.uploadTARS()
  
# print statement to show the 
# successful training of the model
print("TARS Training Successful.")
# importing the required modules.
import json
import pickle
import numpy as np
import nltk
from keras.models import load_model
from keras.models import Sequential
from nltk.stem import WordNetLemmatizer
from keras.layers import Dense, Dropout, Embedding, LSTM, LeakyReLU, BatchNormalization
from keras import optimizers, regularizers
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils, pad_sequences
from tarsDAO import AIDAO
import h5py
from sklearn.model_selection import KFold

from keras.callbacks import EarlyStopping
# Prompt user to enter a username and password
flag=True
# while(flag==True):
#     username = input("Enter your username: ")
#     password = input("Enter your password: ")
#     if (AIDAO.login('', username, password)):
#         print("Login Succesfull. Beginning training...")
#         flag=False
        
# Define Lemmatizer
lemmatizer = WordNetLemmatizer()
# reading the json.intense file
intents = json.loads(open("training.json", encoding="utf8").read())
Nadam = optimizers.Nadam(learning_rate=0.001, clipvalue=1.0, beta_1=0.9, beta_2=0.999, epsilon=1e-07, name='Nadam')
def reinit(model):
    print("Re-initializing TARS...")
    
########################################################################################################
    model = Sequential()
    model.add(Embedding(tokenizer_vocab_size,32,input_length=len(words)))
    model.add(LSTM(7, kernel_initializer='he_uniform', recurrent_initializer='he_uniform'))
    model.add(BatchNormalization())
    model.add(Dense(128, kernel_regularizer=regularizers.l2(0.2), kernel_initializer='variance_scaling'))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Dropout(0.1))
    model.add(Dense(64, kernel_regularizer=regularizers.l2(0.2)))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Dense(len(classes), 
                        activation='softmax'))
    # compile the model
    model.compile(loss='categorical_crossentropy',
                optimizer=Nadam, metrics=['accuracy'])
    print("TARS Re-initialized.")
    print(model.summary())
    return model
# Initialize a list to store the evaluation metrics
scores = []
def train(model):
      # Set the number of folds
    num_folds = 5

    # Define the K-fold cross-validator
    kf = KFold(n_splits=num_folds, shuffle=True, random_state=42)

        # Loop over the folds
    for train_index, test_index in kf.split(train_x_encoded_padded_words):
        # Get the training and test data for this fold
        x_train, x_test = train_x_encoded_padded_words[train_index], train_x_encoded_padded_words[test_index]
        y_train, y_test = train_y[train_index], train_y[test_index]
                
        # Train the model
        hist = model.fit(x_train, y_train, epochs=30, batch_size=5, callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)], validation_data=(x_test, y_test))
        
        # Evaluate the model on the test data for this fold
        score = model.evaluate(x_test, y_test, verbose=0)
        scores.append(score)
    return hist
# creating empty lists to store data
words = []
classes = []
documents = []
ignore_letters = ["?", "!", ".", ",", "'", ":", ";", "(",")", "-", "_"]
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # separating words from patterns
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list) # and adding them to words list
        
        # associating patterns with respective tags
        documents.append(([word if word == "was" else lemmatizer.lemmatize(word).lower() 
                         for word in word_list if word not in ignore_letters], 
                         intent['tag']))
        
        # appending the tags to the class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Convert data into binary to feed into neural network
# training = []
# output_empty = [0]*len(classes)
# for document in documents:
#     bag = []
#     word_patterns = document[0]
#     word_patterns = [lemmatizer.lemmatize(
#         word.lower()) for word in word_patterns]
#     for word in words:
#         bag.append(1) if word in word_patterns else bag.append(0)
    
#     # copy of output_empty
#     output_row = list(output_empty)
#     output_row[classes.index(document[1])] = 1
#     training.append([bag, output_row])
# random.shuffle(training)
# training = np.array(training, dtype=object)

# # Split data into x and y training sets
# train_x = list(training[:, 0])
# train_y = list(training[:, 1])
# create a tokenizer
# convert text to sequence
train_x = [document[0] for document in documents]
train_x = np.array(train_x, dtype=object)
print("LENGTH OF CLASSES")
print(len(classes))
# saving the words and classes list to binary files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))
# one-hot encoding the output
train_y = np_utils.to_categorical([classes.index(document[1]) for document in documents], num_classes = len(classes))
# PREPROCESSING
# Try converting train_x and train_y to panda dataframes.
text = train_x
print(text)
tokenizer = Tokenizer(oov_token="<OOV>")
# fit the tokenizer on our text
tokenizer.fit_on_texts(text)
tokenizer_vocab_size = len(tokenizer.word_index) + 1
# OOV tokens placed out of index to tell NN they are OOV
print("VOCAB SIZE")
print(tokenizer_vocab_size)
print("X TRAIN SHAPE")
print(train_x.shape)
print("TRAIN_Y SHAPE")
print(train_y.shape)

train_x_encoded_words = tokenizer.texts_to_sequences(train_x)

train_x_encoded_padded_words = pad_sequences(train_x_encoded_words, maxlen=len(words))
# Open TARS
with h5py.File('tars.h5', 'r') as tars:
    if len(tars.keys()) != 0 and not True: # Load TARS if memory is found
        print("TARS MEMORY FOUND. DOWNLOADING TARS...")
        print(tars.keys())
        model = load_model(tars)
    else: # Otherwise create a new neural network
        print("TARS MEMORY NOT FOUND. RE-CREATING NEURAL NETWORK...")
        model = reinit(0)

# Define a callback for early stopping
early_stop = EarlyStopping(monitor='val_accuracy', patience=10, mode='max',  min_delta=0.01,verbose=1,restore_best_weights=True)
# Activate training
try:
    hist = train(model)
except ValueError:
    print(ValueError)
    print("Input data difference detected. Re-initializing TARS.")
    model = reinit(model)
    print("Re-fitting TARS.")
    hist = train(model)
# saving the model
print("Saving TARS model...")
model.save("tars.h5", hist)

print("Saving tokenizer...")
with open('tokenizer.pkl', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
# print statement to show the 
# successful training of the model
# Print the final evaluation metrics
print("Final evaluation metrics:", scores)
print("TARS Training Successful.")


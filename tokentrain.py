import pandas as pd
import pickle

def load_tokenizer():
    with open('tokenizer.pkl', 'rb') as f: # Open tokenizer from pickle
        tokenizer = pickle.load(f)
    if "<OOV>" in tokenizer.word_index: # If OOV token is in tokenizer, move its index to outside of word index
        tokenizer.word_index["<OOV>"] = len(tokenizer.word_index) + 1
            # ^ TARS does not have weights associated with out of index tokens, will not try to correct OOV words.
    else: # Else add the OOV token to the tokenizer at index.
        tokenizer.word_index.setdefault("<OOV>", len(tokenizer.word_index) + 1)
        print("Saving tokenizer...") # Save tokenizer to pickle.
    with open('tokenizer.pkl', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return tokenizer # Also, return the tokenizer.


import pandas as pd
import pickle
class loadTokenizer():
    
    def load_tokenizer():
        print("Opening tokenizer.pkl ...")
        tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))
        if "<OOV>" in tokenizer.word_index:
            tokenizer.word_index["<OOV>"] = len(tokenizer.word_index) + 1
        else:
            tokenizer.word_index.setdefault("<OOV>", len(tokenizer.word_index) + 1)
            print("Saving tokenizer...")
        with open('tokenizer.pkl', 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return tokenizer

import en_core_web_sm
import datetime
nlp = en_core_web_sm.load()
import enchant
import nltk
from nltk.stem import WordNetLemmatizer

# MODULE: ner.py
# LAST UPDATED: 03/25/2023
# AUTHOR: CHRIS KING
# FUNCTION : AI bot to manipulate and return data from user input


# Function to extract day of week from user input
# Using NLTK Named Entity Recognition
# PARAMETERS: input text
# SOURCE MODULE: tars.py
# RETURNS: date of day of week
def extract_day_of_week(input_text):
    # Load input text into NLP model
    doc = nlp(input_text)
    today = datetime.date.today() # <-- Get today's datetime
    current_weekday = today.weekday() # <-- Get today's weekday
    # List of weekdays
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day = ""
    isToday = False 
    # For each entity in the input text
    for ent in doc.ents:
        # If the entity is a date
        if ent.label_ == "DATE":
            # For each word in the entity, if the entity is a week day or today/tomorrow, set day to that day
            for word in ent.text.split():
                if word.capitalize() in weekdays:
                    day = word.capitalize()
                elif word.lower() == "tomorrow":
                    day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%A')
                elif word.lower() == "today":
                    isToday = True
                    day = today.strftime('%A')
                    
    try: # <-- try  to get the index of the day in the list of weekdays
        days_until_day = weekdays.index(day) - current_weekday
    except ValueError: # <-- if the day is not in the list of weekdays, return None
        return None
    # If the are not asking for today but the next occurence of today, set days_until_day to 7
    if days_until_day <= 0 and not isToday:
        days_until_day += 7
    # Return the next occurence of the day
    next = today + datetime.timedelta(days=days_until_day)
    return next

# Function to correct each word in user input
# Using enchant distance algorithm
# PARAMETERS: input text
# SOURCE MODULE: tars.py
# RETURNS: corrected input text
def correct_input(input_text):
     # Initialize the spell checker
    spell_checker = enchant.Dict("en_US")
    spell_checker.add("uvi")
    # Tokenize the input text using split()
    tokens = input_text.split()
    # Store corrected tokens
    corrected_tokens = []
    # For each token, if it is spelled incorrectly, correct it. Else, store the original word.
    for token in tokens:
        token = token.lower()
        if not spell_checker.check(token):
            # If the word is misspelled, try to correct it
            suggestions = spell_checker.suggest(token)
            if suggestions:
                corrected_word = suggestions[0].lower()
                corrected_tokens.append(corrected_word)
            else:
                # If there are no suggestions, use the original word
                corrected_tokens.append(token)
        else:
            # Use the original word
            corrected_tokens.append(token)
    # Reconstruct the corrected text using join()
    corrected_text = ' '.join(corrected_tokens)
    return corrected_text

# Function to clean the user input, lemmatize, lowercase, and remove ignore characters, store in array of tokens
# Using NLTK lemmatization
# PARAMETERS: input text
# SOURCE MODULE: tars.py
# RETURNS: array of tokens
def clean(sentence):
    lemmatizer = WordNetLemmatizer() # Create NLTK Lemmatizer to lemmatize words
    ignore_letters = ["?", "!", ".", ",", "'", ":", ";", "(",")", "-", "_"] # List of characters to ignore
    # Lemmatizes the sentence
    sentence_words = nltk.word_tokenize(sentence) # Use NLTK's tokenizer to tokenice the sentence
    sentence_words = [lemmatizer.lemmatize(word).lower()
                      for word in sentence_words if word not in ignore_letters] # Lemmatize words, convert to all lowercase, and remove ignore characters
    return sentence_words
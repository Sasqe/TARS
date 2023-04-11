import datetime
import enchant
import nltk
import dateparser
from nltk.stem import WordNetLemmatizer

# MODULE: ner.py
# LAST UPDATED: 03/25/2023
# AUTHOR: CHRIS KING
# FUNCTION : AI bot to manipulate and return data from user input


# Function to extract day of week from user input
# Using dateparser Named Entity Recognition
# PARAMETERS: input text
# SOURCE MODULE: tars.py
# RETURNS: date of day of week
def extract_day_of_week(input_text):
    today = datetime.date.today()
    current_weekday = today.weekday()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    is_today = False
    
    # Check for today/tomorrow in the input text
    if "today" in input_text.lower() or "the day" in input_text.lower():
        is_today = True
        day = today.strftime('%A')
    elif "tomorrow" in input_text.lower():
        day = (today + datetime.timedelta(days=1)).strftime('%A')
    else:
        # Parse dates using dateparser library
        parsed_date = dateparser.parse(input_text, settings={'PREFER_DATES_FROM': 'future'})
        if parsed_date and parsed_date.weekday() < 7:
            day = weekdays[parsed_date.weekday()]
        else:
            # Search for a weekday in the input text
            for weekday in weekdays:
                if weekday.lower() in input_text.lower():
                    day = weekday
                    break
            else:
                return None
    
    # Calculate days until next occurrence of the day
    days_until_day = weekdays.index(day) - current_weekday
    if days_until_day <= 0 and not is_today:
        days_until_day += 7
    
    # Return next occurrence of the day
    next_day = today + datetime.timedelta(days=days_until_day)
    return next_day

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
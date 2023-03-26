# required modules
import random
import json
import pickle
import numpy as np
from keras.models import load_model
from apisource import apiQuery
from keras.utils import pad_sequences
from tokentrain import load_tokenizer
import os
import math
from ner import extract_day_of_week, correct_input, clean
from flask import Flask, request
from flask_cors import CORS

# MODULE: tars.py [ ENDPOINT MODULE ]
# LAST UPDATED: 03/25/2023
# AUTHOR: CHRIS KING
# FUNCTION : Endpoint module ( WEATHER )  

app = Flask(__name__) # Flask API app with CORS enabled
CORS(app)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Set LOG lvl to 3
apiquery = apiQuery() # Import apisource.py to query APIs

# Load trained files: intents, words, classes, tars model, and tokenizer

print("Loading language processing dependencies....")
intents = (json.loads(open("training.json", encoding="utf8").read()))['intents'] # intents.json to generate intent responses
words = pickle.load(open('words.pkl', 'rb')) # words.pkl contains the vocabulary that TARS was trained on
classes = pickle.load(open('classes.pkl', 'rb')) # classes.pkl contains the classes that TARS was trained to make predictions on
print("Loading TARS....")
model = load_model('tars.h5') # load TARS's memory from .h5 file

# Keras tokenizer contains TARS' vocab dictionary, as well as it's word vector matrix
print("Loading tokenizer...")
tokenizer = load_tokenizer() # Import tokentrain.py to load Keras tokenizer, update its OOV vector index, and update it's pickle.
# Array to hold message history
messages = []
# Set starting and wakeup prompts.
messages.append({"role": "system", "content": "Your name is TARS, an Artificial Intelligence system developed by a data scientist known as King AI. You have been built with a Long Short-Term Memory (LSTM) Recurrent Neural Network trained on intent-based natural language classification tasks, with JARVIS-like manneurism. If the question is not related to meteorology, answer the question or prompt normally. If it is related to meteorology, respond with a variation of 'My apologies sir. I wasn't trained on how to get that data yet.'. Answer as concisely as possible. Examples: 'What is a neural network?', Answer normally. 'How hot was it yesterday?', 'Oops, my apologies. I wasn't trained on how to get that data yet.', 'What is the Davinci-003 Neural Network?', Answer normally. 'How much will it rain next', 'Sorry sir, I don't think I know how to get that data yet.'. 'System.out.println('Hello World!')', 'Hello World!'"})
# ========================================== TARS is ready to go ======================================================================


# Function to predict the intent of the user's input
# Using TARS' memory and vocabulary
# PARAMETERS: input text
# RETURNS: intent of the input text
def predict_class(message):
    message = clean(message) # Clean the sentence
    tokens = tokenizer.texts_to_sequences([message]) # Use Keras tokenizer to convert words to tokens
    tokens = pad_sequences(tokens, maxlen=len(words)) # Pad tokens into vector matrix
    res = model.predict(np.array(tokens), verbose=0) # TARS makes its prediction by passing the tokens to it
    pred = np.argmax(res) # Get the index of the highest probability
    #print(res[0,pred])
    if (res[0,pred] < 0.832): # If tars isn't too sure about what the input says
        #try:
            return classes[classes.index('gptQuery')] # Set class to 'gptQuery'
                # ^ This is done to tell TARS to access GPT-3 Neural Network to generate a response
        #except:
            #return classes[classes.index('gptQuery')]
    #print("MESSAGE:", message, "CLASS:", classes[pred])
    return classes[pred] # Else, return class 

# Function to generate response from TARS
# Using TARS' intents, apisource.py module, ner.py module
# PARAMETERS: intent, message history
# RETURNS: TARS's fully generated response
def get_response(tag, messages): 
    message = messages[len(messages) - 1]['content'] # <-- Set the user message to the most recent message in the history
    result = "" # <-- initialize result variable
    print(tag)
    
    # Iterate through TARS's intents. Execute NER and API scripts based on intent.
    for i in intents:
        if i['tag'] == tag:
            try:
                # TARS will generate a response uniquely based on which function it needs to perform.
                # Each response has {} tags that will be formatted with the data TARS recieves from the API
                # Some responses may have mathematical operations performed on its format tags, such as converting Kelvin to Fahrenheit
                # VARIABLES: data_result - data recieved from API, result - TARS's generated response.
                
                if i['tag'] == 'gptQuery': # <-- gptQuery - return a response from GPT-3 Neural Network
                    data_result = apiquery.queryGPT(messages) # data_result: response string
                    result = data_result
                    
                elif i['tag'] == 'currentTemperature': # <-- currentTemperature - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: dictionary of weather data
                    result = random.choice(i['responses']).format(data_result['current_temp'], data_result['feels_like'])
                    
                elif i['tag'] == 'currentWeather': # <-- currentWeather - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: dictionary of weather data
                    directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"] 
                    # Math to calculate compass direction from degrees
                    result = random.choice(i['responses']).format(data_result['current_temp'], data_result['current_uvi'], data_result['current_windspeed'], directions[math.floor(int(data_result['current_winddeg'] + 22.5) / 45 % 8)], data_result['current_clouds'])
                    
                elif i['tag'] == 'currentDewPoint': # <-- currentDewPoint - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: dew point float
                    # Math to format float to 2 decimal places and convert to fahrenheit
                    result = random.choice(i['responses']).format(data_result, "{:.2f}".format(data_result * 9 / 5 - 459.67))
                    
                elif i['tag'] == 'currentWind': # <-- currentWind - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: dictionary of weather data
                    directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
                    # Math to calculate compass direction from degrees
                    result = random.choice(i['responses']).format(data_result['wind_speed'], directions[math.floor(int(data_result['wind_deg'] + 22.5) / 45 % 8)])
                
                elif i['tag'] == 'currentUvi': # <-- currentUvi - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: uvi float
                    result = random.choice(i['responses']).format(data_result)
                
                elif i['tag'] == 'currentHumidity': # <-- currentHumidity - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: humidity float
                    result = random.choice(i['responses']).format(data_result)
                    
                elif i['tag'] == 'currentPressure': # <-- currentPressure - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: pressure float
                    # Math to convert hPa to inHg
                    inHg = data_result *  0.0295299830714
                    data_result = {
                        "hPa": data_result,
                        "inHg": inHg
                    }
                    result = random.choice(i['responses']).format(data_result['hPa'], data_result['inHg'])
                    
                elif i['tag'] == 'currentVisibility': # <-- currentVisibility - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: visibility float
                    result = random.choice(i['responses']).format(data_result)
                    
                elif i['tag'] == 'dailyRain': # <-- dailyRain - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: rain float or 0
                    
                    if (data_result != 0): # <-- If rain, return response for rain
                        result = random.choice(i['responses'][0]).format(data_result)
                    else: # <-- Else, return response for no rain
                        result = random.choice(i['responses'][1])
                    
                elif i['tag'] == 'dailySunset': # <-- dailySunset - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: time string
                    result = random.choice(i['responses']).format(data_result)
                    
                elif i['tag'] == 'dailySunrise': # <-- dailySunrise - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: dictionary of weather data
                    result = random.choice(i['responses']).format(data_result['today_sunrise'], data_result['tomorrow_sunrise'])
                    
                    
                elif i['tag'] == 'rainWeek': # <-- rainWeek - return a response from weather API
                    data_result = apiquery.queryWeather(tag) # data_result: dictionary of weather data
                    print("DS", data_result)
                    # If there is rain data, first generate response for today's rain, then for the next week of rain.
                    if data_result:
                        if 'Today' in data_result:
                            # Today's rain response 
                            phrase = random.choice(i['responses'][0])
                            for rain_time, rain_pop in data_result['Today']: # <-- get rain time and rain probability for today.
                                phrase += "\n   - {}, {}%.".format(rain_time, rain_pop * 100)
                            result += phrase
                        else: # <-- If no rain today, return response for no rain today.
                            result = random.choice(i['responses'][1])
                            
                        # If there is rain for more days than today, generate response for next 7 days.
                        if len(data_result) > 1:
                            # Response for next 7 days
                            phrase = random.choice(i['responses'][2])
                            # Loop through each day and rain data of that day in data result
                            for day, rain in data_result.items():
                                # For every day except for today, add a line to the response with the day and amount of rain.
                                if day != 'Today':
                                    phrase += "\n   - {}: {} inches.".format(day, rain)
                            result += phrase
                    
                    # If there is no rain for the whole week, generate response for no rain for the whole week.
                    else:
                        result = random.choice(i['responses'][3])
                
                # WEATHER FORECASTING - all data results will be dictionaries, containing day, date, and data returned.
                # For each intent, the following steps will be executed:
                
                # 1. Extract the day of the week from the user's message with NER bot
                # 2. Query the weather API with the tag and day of the week
                # 3. Generate a response and format the data to the response.
                elif i['tag'] == 'uviForecast':
                    day = extract_day_of_week(message)
                    data_result = apiquery.queryForecast(tag, day)
                    result = random.choice(i['responses']).format(data_result['day'], data_result['date'], data_result['uvi'])
                    
                elif i['tag'] == 'windForecast':
                    day = extract_day_of_week(message)
                    data_result = apiquery.queryForecast(tag, day)
                    result = random.choice(i['responses']).format(data_result['day'], data_result['date'], data_result['wind_speed'])
                    
                elif i['tag'] == 'rainForecast':
                    day = extract_day_of_week(message)
                    data_result = apiquery.queryForecast(tag, day)
                    if data_result['rain']: # <-- If rain, return response for rain
                        result = random.choice(i['responses'][0]).format(data_result['day'], data_result['date'], data_result['rain'])
                    else: # <-- Else, return response for no rain
                        result = random.choice(i['responses'][1]).format(data_result['day'], data_result['date'])
                        
                elif i['tag'] == 'highTempForecast':
                    day = extract_day_of_week(message)
                    data_result = apiquery.queryForecast(tag, day)
                    result = random.choice(i['responses']).format(data_result['day'], data_result['date'], data_result['high_temp'])
                    
                elif i['tag'] == 'lowTempForecast':
                    day = extract_day_of_week(message)
                    data_result = apiquery.queryForecast(tag, day)
                    result = random.choice(i['responses']).format(data_result['day'], data_result['date'], data_result['low_temp'])
                    
                elif i['tag'] == 'weatherForecast':
                    day = extract_day_of_week(message)
                    data_result = apiquery.queryForecast(tag, day)
                    # Math to convert float to percentage
                    result = random.choice(i['responses']).format(data_result['day'], data_result['date'], data_result['avg_temp'], data_result['min_temp'], data_result['max_temp'], data_result['wind_speed'], data_result['wind_gust'], data_result['clouds'], data_result['pop'] * 100)
                    
                elif i['tag'] == 'humidityForecast':
                    day = extract_day_of_week(message)
                    data_result = apiquery.queryForecast(tag, day)
                    result = random.choice(i['responses']).format(data_result['day'], data_result['date'], data_result['humidity'])
                    
                elif i['tag'] == 'pressureForecast':
                    day = extract_day_of_week(message)
                    data_result = apiquery.queryForecast(tag, day)
                    # Math to convert hPa to inHg
                    data_result['inHg'] = data_result['hPa'] *  0.0295299830714 # Convert hPa to inHg
                    result = random.choice(i['responses']).format(data_result['day'], data_result['date'], data_result['hPa'], data_result['inHg'])
                
                elif i['tag'] == 'visibilityForecast':
                    #day = extract_day_of_week(message)
                    #data_result = apiquery.queryForecast(tag, day)
                    result = random.choice(i['responses'])
                # Error handling, generate a random esponse from whatever intent was matched.
                else:
                    result = random.choice(i['responses'])
                
                # Append the response to the message history
                messages.append({"role": "assistant", "content": result})
                break
            # If there is any error, return error response
            except Exception as e:
                result = "Oops, I wasn't able to get that data."
                # Append the response to the message history
                messages.append({"role": "assistant", "content": result})
                   # Associate a traceback object with the exception
                print(e.with_traceback())
    return result

# Function for CONSOLE INTERFACE
# Using TARS
# RETURNS: None, prints TARS' fully generated response to console.
def interact():
    print("Waking up TARS....")
    # Wake up tars by sending starting prompts
    messages.append({"role": "user", "content": "hi there"})
    res = get_response("greetings", messages)
    print("TARS: ", res) # Print response
    # Conversation loop
    while (True):
        message = correct_input(input("")) # NER to correct input 
        print("FINAL MESSAGE",message) # Print corrected input
        messages.append({"role": "user", "content": message}) # Append message to message history
        if(message == "sleep"):
            break
        else:
            # Predict class and print response
            data = predict_class(message)
            res = get_response(data, messages)
            print("TARS: ", res)
            
# Function for CONSOLE INTERFACE
# Using TARS
# USING flask API app
# RETURNS: TARS's fully generated response                  
@app.route('/chat', methods=['POST'])
def chat():
    # Get JSON data from request and correct it with NER
    data = request.get_json()
    message = correct_input(data['prompt'])
    print("Received: ", message)
    print("FINAL MESSAGE",message)
    # Append message to message history
    messages.append({"role": "user", "content": message})
    # Generate and return response
    response = get_response(predict_class(message), messages)
    print("Response: ", response)
    return {"response": response}    

# Execution endpoint
# app.run() for Flask API, interact() for console interface
if __name__ == "__main__":
    #app.run(debug=False)
    interact()
    


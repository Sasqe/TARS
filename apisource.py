# TO DO: Method to make an API CALL to API to retrieve current temperature
import requests
from datetime import datetime
class apiQuery():
    # query GPT
    def queryGPT(self, message):
        import openai # Import openAI library
        # Import openAI api key
        openai.api_key = "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"
         # Configure GPT-3 Neural Network
        response = openai.Completion.create(
            engine="text-ada-001", # Ada is fastest and cheapest, we use for development
            prompt=message,
            max_tokens=50, # Max words for response is 50.
            temperature=0.5, # Temperature to control difference in response given same prompt
            timeout=30
        )
        # Return the response text
        text = response['choices'][0]['text']
        return text
    # Query weather, pass intent as parameter and modify api endpoint based on intent
    def queryWeather(self, intent):
        #try:
            # First, we use API endpoint to generate latitude and longitude based on city and state.
            georeq = 'http://api.openweathermap.org/geo/1.0/direct?q=Phoenix,AZ,US&appid=ebb84e8bcc2b87041ba43e4b76d9c9f8'
            georesponse = requests.get(georeq)
            geojson = georesponse.json()[0]
            lat = geojson["lat"]
            lon = geojson["lon"]
            # Next, we pass latitude and longitude into weather API endpoint
            endpoint = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exlude=hourly,daily,alerts,minutely&units=imperial&appid=ebb84e8bcc2b87041ba43e4b76d9c9f8'
            response = requests.get(endpoint) # Send query to API endpoint
            responsejson = response.json() # Conver to JSON
            # Switch case to get the data we need based on the intent.
            if intent == "currentTemperature": # <-- If intent is currentTemperature
                data = responsejson['current']['temp']
            elif intent == "currentDewPoint": # <-- If intent is currentDewPoint
                data = responsejson['current']['dew_point']
            elif intent == "currentUvi": # <-- If intent is currentUvi
                data = responsejson['current']['uvi']
            elif intent == "currentWind": # <-- If intent is currentWind
                data = [                                   # <-- For this intent, we will return the wind speed and direction in a 2d structure      
                    responsejson['current']['wind_speed'],
                    responsejson['current']['wind_deg']
                ]
                 # For daily data, we will access [0] index to get the current day.
            elif intent == "dailyHighTemp": # <-- If intent is dailyHighTemp
                data = responsejson['daily'][0]['temp']['max']
            elif intent == "dailyLowTemp": # <-- If intent is dailyLowTemp
                data = responsejson['daily'][0]['temp']['min']
            elif intent == "dailyRain": # <-- If intent is dailyRain
                try:
                    data = responsejson['daily'][0]['rain'] # <-- Try train at day [0] ( current day )
                except:
                    data = 0 # <-- If no rain, return 0
            elif intent == "dailySunset": # <-- If intent is dailySunset
                data = responsejson['daily'][0]['sunset']
                timestamp = datetime.fromtimestamp(data) # Convert Unix timestamp to Human-Readable datetime
                data = timestamp.strftime("%H:%M")      
            else:
                data = "Error"
            return data
        
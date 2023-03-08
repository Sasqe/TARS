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
        print("Res")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are TARS, an Artificial Intelligence system developed by King AI. Answer as concisely as possible."},
                {"role": "user", "content": message}
            ]
        )
        print(response)
        return response["choices"][0]["message"]["content"]
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
            endpoint = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,alerts&units=imperial&appid=ebb84e8bcc2b87041ba43e4b76d9c9f8'
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
            elif intent == "currentHumidity": # <-- If intent is currentHumidity
                data = responsejson['current']['humidity']
            elif intent == "currentPressure": # <-- If intent is currentPressure
                data = responsejson['current']['pressure']
            elif intent == "currentVisibility": # <-- If intent is curerntVisibility
                data = responsejson['current']['visibility']
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
            elif intent == "dailySunrise": # <-- If intent is dailySunrise
                data0 = responsejson['daily'][0]['sunrise']
                data1 = responsejson['daily'][1]['sunrise']
                timestamp0 = datetime.fromtimestamp(data0) # Convert Unix timestamp to Human-Readable datetime
                data0 = timestamp0.strftime("%H:%M")
                timestamp1 = datetime.fromtimestamp(data1) # Convert Unix timestamp to Human-Readable datetime
                data1 = timestamp1.strftime("%H:%M")
                data = [
                    data0,
                    data1
                ]
            # FORECASTING
            elif intent == "nextRain24hr":
                days_with_rain = {}
                now = datetime.now()
                # Check if it will rain today
                for forecast in responsejson['hourly']:
                    dt = datetime.fromtimestamp(forecast['dt'])
                    if 'rain' in forecast and forecast['rain']['1h'] > 0 and dt.date() == now.date():
                        days_with_rain[now.strftime("%A")] = [dt.strftime("%I:%M %p %Z")]
                        break

                # Check for rain in the next 7 days
                
                for forecast in responsejson['daily'][1:8]:
                    dt = datetime.fromtimestamp(forecast['dt'])
                    if 'rain' in forecast and forecast['rain'] > 0:
                        days_with_rain[dt.strftime("%A")] = [dt.strftime("%I:%M %p %Z")]
                data = days_with_rain
            else:
                data = "Error"
            return data
        
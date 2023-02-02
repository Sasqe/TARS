# TO DO: Method to make an API CALL to API to retrieve current temperature
import requests
from datetime import datetime
class apiQuery():
    # query GPT
    def queryGPT(self, message):
        # todo
        import openai
        # Set up the OpenAI API client
        openai.api_key = "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"
         # Use the OpenAI API to generate a response to the prompt
        response = openai.Completion.create(
            engine="text-ada-001",
            prompt=message,
            max_tokens=1024,
            temperature=0.5,
            timeout=30
        )
        # Return the response text
        text = response['choices'][0]['text']

        return text
    # Query weather, pass intent as parameter and modify api endpoint based on intent
    def queryWeather(self, intent):
        #try:
            georeq = 'http://api.openweathermap.org/geo/1.0/direct?q=Phoenix,AZ,US&appid=ebb84e8bcc2b87041ba43e4b76d9c9f8'
            georesponse = requests.get(georeq)
            geojson = georesponse.json()[0]
            lat = geojson["lat"]
            lon = geojson["lon"]
            endpoint = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exlude=hourly,daily,alerts,minutely&units=imperial&appid=ebb84e8bcc2b87041ba43e4b76d9c9f8'
            response = requests.get(endpoint)
            responsejson = response.json()
            # if intent is current temperature
            if intent == "currentTemperature":
                data = responsejson['current']['temp']
            elif intent == "currentDewPoint":
                data = responsejson['current']['dew_point']
            elif intent == "currentUvi":
                data = responsejson['current']['uvi']
            elif intent == "currentWind":
                data = [
                    responsejson['current']['wind_speed'],
                    responsejson['current']['wind_deg']
                ]
            elif intent == "dailyHighTemp":
                data = responsejson['daily'][0]['temp']['max']
            elif intent == "dailyLowTemp":
                data = responsejson['daily'][0]['temp']['min']
            elif intent == "dailyRain":
                try:
                    data = responsejson['daily'][0]['rain']
                except:
                    data = 0
            elif intent == "dailySunset":
                data = responsejson['daily'][0]['sunset']
                timestamp = datetime.fromtimestamp(data)
                data = timestamp.strftime("%H:%M")      
            else:
                data = "Error"
            return data
        # except Exception as e:
        #     data = "My apologies, I can't seem to connect to the network."
        #     print(e)
        #     return data
        
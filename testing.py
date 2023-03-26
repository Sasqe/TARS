import unittest
from upload import main as upload
from download import main as download
from tarsDAO import AIDAO
from colorama import Fore, Style
from tars import predict_class, get_response
import json
from io import StringIO
from tokentrain import load_tokenizer
from keras.preprocessing.text import Tokenizer

# MODULE: testing.py
# LAST UPDATED: 03/25/2023
# AUTHOR: CHRIS KING
# FUNCTION : Automated unit testing for TARS

intents = json.loads(open("training.json", encoding="utf8").read()) # intents.json to generate intent responses
dao = AIDAO()
class TestTARS(unittest.TestCase):
    # Function to initialize test predictions with prompts
    # self.(blank) for intent
    # predict_class("blank") to send prompt to TARS
    def setUp(self):
        # CLASS PREDICTION 
        
        # CURRENT TEMPERATURE
        self.current_temp = predict_class("What is the current temperature?")
        # CURRENT WEATHER
        self.current_weather = predict_class("What is the current weather?")
        # CURRENT DEW POINT
        self.current_dew = predict_class("What is the current dew point?")
        # CURRENT UV INDEX
        self.current_uvi = predict_class("What is the current UV index?")
        # CURRENT WIND SPEED
        self.current_wind = predict_class("What is the current wind speed?")
        # CURRENT HUMIDITY
        self.current_humidity = predict_class("What is the current humidity?")
        # CURRENT PRESSURE
        self.current_pressure = predict_class("What is the current pressure?")
        # CURRENT VISIBILITY
        self.current_visibility = predict_class("What is the current visibility?")
        # RAIN TODAY
        self.daily_rain = predict_class("How much rain did we get today?")
        # TODAYS SUNSET
        self.daily_sunset = predict_class("What time is the sunset today?")
        # TODAYS SUNRISE
        self.daily_sunrise = predict_class("What time is the sunrise today?")
        #TODAYS/WEEKS RAIN
        self.rain_week = predict_class("How much rain will we get this week?")
        # UVI FORECAST
        self.uvi_forecast = predict_class("What is the UV index for monday?")
        # WIND FORECAST
        self.wind_forecast = predict_class("What is the wind speed for tuesday?")
        # RAIN FORECAST
        self.rain_forecast = predict_class("Will it rain on wednesday?")
        # HIGH TEMP FORECAST
        self.highTemp_forecast = predict_class("What is the highest temperature for thursday?")
        # LOW TEMP FORECAST
        self.lowTemp_forecast = predict_class("What is the lowest temperature for friday?")
        # WEATHER FORECAST
        self.weather_forecast = predict_class("What is the weather like for saturday?")
        # HUMIDITY FORECAST
        self.humidity_forecast = predict_class("What is the humidity for sunday?")
        # PRESSURE FORECAST
        self.pressure_forecast = predict_class("What is the air pressure for monday?")
        # VISIBILITY FORECAST
        self.visibility_forecast = predict_class("What is the visibility for tuesday?")
    
    # TARS current temperature        
    def test_tars_current_temperature(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.current_temp, "currentTemperature")
    # TARS current weather
    def test_tars_current_weather(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.current_weather, "currentWeather")
    # TARS current dew point
    def test_tars_current_dew_point(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.current_dew, "currentDewPoint")
    # TARS current UV index
    def test_tars_current_uv_index(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.current_uvi, "currentUvi")
    # TARS current wind speed
    def test_tars_current_wind_speed(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.current_wind, "currentWind")
        # TARS current humidity
    def test_tars_current_humidity(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.current_humidity, "currentHumidity")
    # TARS current pressure
    def test_tars_current_pressure(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.current_pressure, "currentPressure")
    # TARS current visibility
    def test_tars_current_visibility(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.current_visibility, "currentVisibility")
    # TARS daily rain
    def test_tars_daily_rain(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.daily_rain, "dailyRain")
    # TARS daily sunset
    def test_tars_daily_sunset(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.daily_sunset, "dailySunset")
    # TARS daily sunrise
    def test_tars_daily_sunrise(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.daily_sunrise, "dailySunrise")
    # TARS rain week
    def test_tars_rain_week(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.rain_week, "rainWeek")
    # TARS UVI forecast
    def test_tars_uvi_forecast(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.uvi_forecast, "uviForecast")
    # TARS wind forecast
    def test_tars_wind_forecast(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.wind_forecast, "windForecast")
    # TARS rain forecast
    def test_tars_rain_forecast(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.rain_forecast, "rainForecast")
    # TARS high temp forecast
    def test_tars_high_temp_forecast(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.highTemp_forecast, "highTempForecast")
    # TARS low temp forecast
    def test_tars_low_temp_forecast(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.lowTemp_forecast, "lowTempForecast")
    # TARS weather forecast
    def test_tars_weather_forecast(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.weather_forecast, "weatherForecast")
    # TARS humidity forecast
    def test_tars_humidity_forecast(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.humidity_forecast, "humidityForecast")
    # TARS pressure forecast
    def test_tars_pressure_forecast(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.pressure_forecast, "pressureForecast")
    # TARS visibility forecast
    def test_tars_visibility_forecast(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.visibility_forecast, "visibilityForecast")
            
            
if __name__ == '__main__':
    import colorama # Colorama used for green/red for ok/failure
    colorama.init()
    buffer = StringIO() # Buffer to redirect script output, we don't need to see it
    test_runner = unittest.TextTestRunner(stream=buffer, descriptions=False, verbosity=0)
    buffer = ''
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(TestTARS) # Test runner
    for i, test_case in enumerate(tests): # For each test in test runner print result.
        result = test_runner.run(test_case) # Get the test result from test runner
        if result.wasSuccessful():
            print(f"{test_case._testMethodName}:" + Fore.LIGHTGREEN_EX + "[OK]" + Style.RESET_ALL)
        else:
            print(f"{test_case._testMethodName}:" + Fore.RED + "[FAILED]" + Style.RESET_ALL)

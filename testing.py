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
intents = json.loads(open("training.json", encoding="utf8").read()) # intents.json to generate intent responses
dao = AIDAO()
class TestTARS(unittest.TestCase):
    def setUp(self):
        self.upload = upload
        self.download = download
        self.tokenizer = load_tokenizer()
        self.login = dao.login("sasqe", "sq")
        # CURRENT TEMPERATURE
        self.current_temp = predict_class("What is the current temperature?")
        # CURRENT DEW POINT
        self.current_dew = predict_class("What is the current dew point?")
        # CURRENT UV INDEX
        self.current_uvi = predict_class("What is the current UV index?")
        # CURRENT WIND SPEED
        self.current_wind = predict_class("What is the current wind speed?")
        # HIGHEST TEMP TODAY
        self.highest_temp = predict_class("What is the highest temperature today?")
        # LOWEST TEMP TODAY
        self.lowest_temp = predict_class("What is the lowest temperature today?")
        # DAILY RAIN
        self.daily_rain = predict_class("How much rain did we get today?")
        # TODAYS SUNSET
        self.daily_sunset = predict_class("What time is the sunset today?")
        # API CURRENT TEMP
        self.api_current_temp = get_response("currentTemperature", intents, "")
        # GPT-3
        self.gpt3 = get_response("gptQuery", intents, "What is two plus two?")
        # API CURRENT DEW POINT
        self.api_current_dew = get_response("currentDewPoint", intents, "")
        # API CURRENT UV INDEX
        self.api_current_uvi = get_response("currentUvi", intents, "")
        # API CURRENT WIND
        self.api_current_wind = get_response("currentWind", intents, "")
        # API DAILY HIGH TEMP
        self.api_highest_temp = get_response("dailyHighTemp", intents, "")
        # API DAILY LOW TEMP
        self.api_lowest_temp = get_response("dailyLowTemp", intents, "")
        # API DAILY RAIN
        self.api_daily_rain = get_response("dailyRain", intents, "")
        # API TODAYS SUNSET
        self.api_daily_sunset = get_response("dailySunset", intents, "")
        self.api_error = "Oops, I wasn't able to connect to the network."
    def test_upload_tars_memory(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            result = self.upload()
            self.assertTrue(result)
        
    def test_download_tars_memory(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            result = self.download()
            self.assertTrue(result)
        
    def test_token_train(self):          
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertIsInstance(self.tokenizer, Tokenizer)
    # TARS current temperature        
    def test_tars_current_temperature(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.current_temp, "currentTemperature")
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
    # TARS highest temperature today
    def test_tars_highest_temp_today(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.highest_temp, "dailyHighTemp")
    # TARS lowest temperature today
    def test_tars_lowest_temp_today(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.lowest_temp, "dailyLowTemp")
    # TARS daily rain
    def test_tars_daily_rain(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.daily_rain, "dailyRain")
    # TARS daily sunset
    def test_tars_daily_sunset(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.daily_sunset, "dailySunset")
    # TARS login
    def test_tars_login(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertTrue(self.login) 
    # TARS API Current Temperature
    def test_tars_api_current_temperature(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertNotEqual(self.api_current_temp, self.api_error)
    # TARS API Current Dew Point
    def test_tars_api_current_dew_point(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertNotEqual(self.api_current_dew, self.api_error)
    # TARS API Current UV Index
    def test_tars_api_current_uv_index(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertNotEqual(self.api_current_uvi, self.api_error)
    # TARS API Current Wind Speed
    def test_tars_api_current_wind_speed(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertNotEqual(self.api_current_wind, self.api_error)
    # TARS API Highest Temperature Today
    def test_tars_api_highest_temp_today(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertNotEqual(self.api_highest_temp, self.api_error)
    # TARS API Lowest Temperature Today
    def test_tars_api_lowest_temp_today(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertNotEqual(self.api_lowest_temp, self.api_error)
    # TARS API Daily Rain
    def test_tars_api_daily_rain(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertNotEqual(self.api_daily_rain, self.api_error)
    # TARS API Daily Sunset
    def test_tars_api_daily_sunset(self):
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertNotEqual(self.api_daily_sunset, self.api_error)
if __name__ == '__main__':
    import colorama # Colorama used for green/red for ok/failure
    colorama.init()
    buffer = StringIO() # Buffer to redirect script output, we don't need to see it
    test_runner = unittest.TextTestRunner(stream=buffer, descriptions=False, verbosity=0)
    buffer = ''
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(TestTARS) # Test runner
    for i, test_case in enumerate(tests): # For each test in test runner print result.
        result = test_runner.run(test_case)
        if result.wasSuccessful():
            print(f"{test_case._testMethodName}:" + Fore.LIGHTGREEN_EX + "[OK]" + Style.RESET_ALL)
        else:
            print(f"{test_case._testMethodName}:" + Fore.RED + "[FAILED]" + Style.RESET_ALL)

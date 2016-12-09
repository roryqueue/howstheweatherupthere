import requests, traceback
from json.decoder import JSONDecodeError
from datetime import datetime, timedelta
from weather_app.settings import WUNDERGROUND_API_URL, WUNDERGROUND_API_KEY

class TodaysWeather(object):
    CACHE_PERIOD = timedelta(minutes=5)
    API_URL_FORMAT = "{base_url}/{api_key}/{endpoint}/q/{state_abbreviation}/{city}.json"

    def __init__(self):
        self.by_location = {}

    def find_for_location(self, location):
        if self.by_location.get(location.state) is None:
            self.by_location[location.state] = {}

        # we check if we have recently cached the weather data we need in memory
        # and only hit the Wunderground API if we do not, to minimize requests
        weather_location_cache = self.by_location.get(location.state, {}).get(location.city)
        if weather_location_cache is None\
        or datetime.now() <= (weather_for_location['request_timestamp'] + CACHE_PERIOD):
            self.by_location[location.state][location.city] = self.fetch_current_weather(location)

        return self.by_location[location.state][location.city].copy()

    def fetch_current_weather(self, location):
        response = self.make_request(location, endpoint='conditions')
        print(response)
        current_weather = response['current_observation']
        location_weather_report = {
            'weather_phrase': current_weather['weather'],
            'temperature': current_weather['temp_f'],
            'icon_url': current_weather['icon_url'],
            'precipitation_inches': float(current_weather['precip_1hr_in'])
        }
        if location_weather_report['precipitation_inches'] > 0.0:
            location_weather_report['weather_qualitative'] = 'poor'
        else:
            temp_vs_historical = self.check_temp_vs_historical(location)
            if temp_vs_historical == 'warmer':
                location_weather_report['weather_qualitative'] = 'good'
            elif temp_vs_historical == 'colder':
                location_weather_report['weather_qualitative'] = 'poor'
            else:
                 location_weather_report['weather_qualitative'] = 'average'

        return location_weather_report

    def check_temp_vs_historical(self, location):
        todays_high = self.fetch_todays_high(location)
        historical_average_high = self.fetch_average_high(location)
        if todays_high - 5.0 >= historical_average_high:
            return 'warmer'
        elif todays_high + 5.0 <= historical_average_high:
            return 'colder'
        else:
            return 'similar'

    def fetch_todays_high(self, location):
        response = self.make_request(location, endpoint='forecast')
        daily_forecasts = response['forecast']['simpleforecast']['forecastday']
        daily_high = None
        for daily_forecast in daily_forecasts:
            if daily_forecast['period'] == 1:
                daily_high = float(daily_forecast['high']['fahrenheit'])
                break

        if daily_high is None:
            raise ValueError(
                'Was unable to find high temperature in response from {} endpoint.'.format(endpoint)
            )

        return daily_high

    def fetch_average_high(self, location):
        response = self.make_request(location, endpoint='almanac')
        return float(response['almanac']['temp_high']['normal']['F'])

    def make_request(self, location, endpoint='conditions'):
        try:
            api_url, response, response_json = None, None, None
            api_url = self.API_URL_FORMAT.format(
                base_url=WUNDERGROUND_API_URL,
                api_key=WUNDERGROUND_API_KEY,
                endpoint=endpoint,
                state_abbreviation=location.state_abbreviation,
                city=location.city.replace(' ', '_')
            )
            response = requests.get(api_url)
            response_json = response.json()
            return response_json

        except Exception as e:
            print('exception: ' + str(Exception))
            print('api_url: ' + api_url)
            print('response: ' + str(response))
            print('response.content: ' + str(response.content))
            print('response_json: ' + str(response_json))
            traceback.print_exc()
            raise

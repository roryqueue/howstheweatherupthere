import requests
from datetime import datetime, timedelta
from weather_app.settings import WUNDERGROUND_API_URL, WUNDERGROUND_API_KEY

class TodaysWeather(object):
  
    cache_period = timedelta(minutes=5)
    endpoints = {
        'current': 'conditions',
        'historical': 'almanac',
        'current_forecast': 'forecast' 
    }
    api_url_format = "{base_url}/{api_key}/{call_type}/q/{state_abbreviation}/{city}.json"

    def __init__(self):
        self.by_location = {}

    def find_for_location(location):
        if self.by_location.get(state) is None:
            self.by_location[state] = {}

        # we check if we have recently cached the weather data we need in memory
        # and only hit the Wunderground API if we do not, to minimize requests
        try:
            weather_for_location = self.by_location[state][city]
            if datetime.now() <= (weather_for_location['request_timestamp'] + cache_period):
                self.by_location[state].pop(city)
                raise KeyError

        except KeyError:
            self.by_location[state][city] = self.fetch_todays_weather(state, city)

        return self.by_location[state][city].copy()

    def fetch_current_weather(location):
        api_url = self.api_url_format.format(
            base_url=WUNDERGROUND_API_URL,
            api_key=WUNDERGROUND_API_KEY,
            call_type=self.endpoints['current'],
            state_abbreviation=location.state_abbreviation,
            city=location.city.replace(' ', '_')
        )
        response = requests.get(api_url).json()
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
            temp_vs_historical = check_temp_vs_historical(location)
            if temp_vs_historical == 'warmer':
                location_weather_report['weather_qualitative'] = 'good'
            elif temp_vs_historical == 'colder':
                location_weather_report['weather_qualitative'] = 'poor'
            else:
                 location_weather_report['weather_qualitative'] = 'average'

    def check_temp_vs_historical(location):
        todays_high = self.fetch_daily_high(location, 'current_forecast')
        historical_average_high = self.fetch_daily_high(location, 'historical')
        if todays_high - 5.0 >= historical_average_high:
            return 'warmer'
        elif todays_high + 5.0 <= historical_average_high:
            return 'colder'
        else:
            return 'similar'

    def fetch_daily_high(location, endpoint):
        api_url = self.api_url_format.format(
            base_url=WUNDERGROUND_API_URL,
            api_key=WUNDERGROUND_API_KEY,
            call_type=self.endpoints[endpoint],
            state_abbreviation=location.state_abbreviation,
            city=location.city.replace(' ', '_')
        )
        response = requests.get(api_url).json()
        
        daily_forecasts = response['forecast']['simpleforecast']
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

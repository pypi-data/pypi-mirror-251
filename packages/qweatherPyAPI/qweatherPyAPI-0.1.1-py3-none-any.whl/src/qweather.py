import logging
from typing import Union
from http_request_manager import HttpRequestsManager
from model import (WeatherData, WeatherSun, WeatherMoon, WeatherAirData, WeatherAirNow, WeatherIndicesData,
                   WeatherSolaraRaadiationData)


def date_request(url: str, params: dict, **kwargs):
    logging.info(f"Request: {url}, params: {params}")
    response = HttpRequestsManager().get(url, params=params).json()
    return response


class QWeatherPy:
    def __url__(self):
        self.url_geoapi = "https://geoapi.qweather.com/v2/city/"
        if self.api_type == 1:
            domain = 'api'
        elif self.api_type == 0:
            domain = 'devapi'
        else:
            raise Exception(
                "api_type 必须是为 (int)0 -> 免费订阅, (int)1 -> 付费订阅"
                f"\n当前为: ({type(self.api_type)}){self.api_type}"
            )

        # weather_api
        self.url_weather_api_now = f"https://{domain}.qweather.com/v7/weather/now?"
        self.url_weather_api_3d = f"https://{domain}.qweather.com/v7/weather/3d?"
        self.url_weather_api_7d = f"https://{domain}.qweather.com/v7/weather/7d?"
        self.url_weather_api_10d = f"https://{domain}.qweather.com/v7/weather/10d?"
        self.url_weather_api_15d = f"https://{domain}.qweather.com/v7/weather/15d?"
        self.url_weather_api_30d = f"https://{domain}.qweather.com/v7/weather/30d?"
        self.url_weather_api_24h = f"https://{domain}.qweather.com/v7/weather/24h?"
        self.url_weather_api_72h = f"https://{domain}.qweather.com/v7/weather/72h?"
        self.url_weather_api_168h = f"https://{domain}.qweather.com/v7/weather/168h?"
        self.url_air_quality_now = f"https://{domain}.qweather.com/v7/air/now?"
        self.url_air_quality_5d = f"https://{domain}.qweather.com/v7/air/5d?"
        self.url_indices_1d = f"https://{domain}.qweather.com/v7/indices/1d?"
        self.url_indices_3d = f"https://{domain}.qweather.com/v7/indices/3d?"
        self.url_solar_24h = f"https://{domain}.qweather.com/v7/solar-radiation/24h?"
        self.url_solar_72h = f"https://{domain}.qweather.com/v7/solar-radiation/72h?"
        self.url_astronomy_sun = f"https://{domain}.qweather.com/v7/astronomy/sun?"
        self.url_astronomy_moon = f"https://{domain}.qweather.com/v7/astronomy/moon?"
        self.url_astronomy_angle = f"https://{domain}.qweather.com/v7/astronomy/solar-elevation-angle?"

    def __init__(self, api_key: str, api_type: Union[int, str] = 0):
        self.apikey = api_key
        self.api_type = int(api_type)
        self.__url__()

    # get the current weather
    def get_weather_now(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        params.update(kwargs)
        data = date_request(self.url_weather_api_now, params)
        if not data:
            return None
        return WeatherData(data)

    # get the 3d weather
    def get_weather_3d(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        params.update(kwargs)
        data = date_request(self.url_weather_api_3d, params)
        return WeatherData(data)

    # get the 7d weather
    def get_weather_7d(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        params.update(kwargs)
        data = date_request(self.url_weather_api_7d, params)
        if not data:
            return None
        return WeatherData(data)

    # get the 10d weather
    def get_weather_10d(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        params.update(kwargs)
        data = date_request(self.url_weather_api_10d, params)
        if not data:
            return None
        return WeatherData(data)

    # get the 15d weather
    def get_weather_15d(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        params.update(kwargs)
        data = date_request(self.url_weather_api_15d, params)
        if not data:
            return None
        return WeatherData(data)

    # get the 30d weather
    def get_weather_30d(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        params.update(kwargs)
        data = date_request(self.url_weather_api_30d, params)
        if not data:
            return None
        return WeatherData(data)

    # get the 24h weather
    def get_weather_24h(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        params.update(kwargs)
        data = date_request(self.url_weather_api_24h, params)
        if not data:
            return None
        return WeatherData(data)

    # get the 72h weather
    def get_weather_72h(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        params.update(kwargs)
        data = date_request(self.url_weather_api_72h, params)
        if not data:
            return None
        return WeatherData(data)

    # get the 168h weather
    def get_weather_168h(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        params.update(kwargs)
        data = date_request(self.url_weather_api_168h, params)
        if not data:
            return None
        return WeatherData(data)

    # get the currently air quality
    def get_air_quality_now(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        data = date_request(self.url_air_quality_now, params)
        if not data:
            return None
        return WeatherAirNow(data)

    # get the 5d air quality
    def get_air_quality_5d(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        data = date_request(self.url_air_quality_5d, params)
        if not data:
            return None
        return WeatherAirData(data)

    # get life index for 1d
    def get_indices_1d(self, location: str, type: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
            "type": type,
        }
        data = date_request(self.url_indices_1d, params)
        if not data:
            return None
        return WeatherIndicesData(data)

    # get life index for 3d
    def get_indices_3d(self, location: str, type: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
            "type": type,
        }
        data = date_request(self.url_indices_3d, params)
        if not data:
            return None
        return WeatherIndicesData(data)

    # get solar radiation for 24h
    def get_solar_24h(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        data = date_request(self.url_solar_24h, params)
        if not data:
            return None
        return WeatherSolaraRaadiationData(data)

    # get solar radiation for 72h

    def get_solar_72h(self, location: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
        }
        data = date_request(self.url_solar_72h, params)
        if not data:
            return None
        return WeatherSolaraRaadiationData(data)

    # get astronomy for sun
    def get_astronomy(self, location: str, date: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
            "date": date,
        }
        data = date_request(self.url_astronomy_sun, params)
        if not data:
            return None
        return WeatherSun(data)

    # get astronomy for moon
    def get_astronomy_moon(self, location: str, date: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
            "date": date,
        }
        data = date_request(self.url_astronomy_moon, params)
        if not data:
            return None
        return WeatherMoon(data)

    # get astronomy for angle
    def get_astronomy_angle(self, location: str, date: str, **kwargs):
        params = {
            "key": self.apikey,
            "location": location,
            "date": date,
        }
        data = date_request(self.url_astronomy_angle, params)
        if not data:
            return None
        return WeatherSun(data)

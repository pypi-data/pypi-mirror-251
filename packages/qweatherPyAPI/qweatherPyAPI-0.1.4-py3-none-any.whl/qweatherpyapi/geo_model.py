from qweatherpyapi.model import WeatherDataSup


class CityLocation(WeatherDataSup):
    def __init__(self, data):
        super().__init__(data)
        self.name = data.get('name')
        self.id = data.get('id')
        self.lat = data.get('lat')
        self.lon = data.get('lon')
        self.adm2 = data.get('adm2')
        self.adm1 = data.get('adm1')
        self.country = data.get('country')
        self.tz = data.get('tz')
        self.utcOffset = data.get('utcOffset')
        self.isDst = data.get('isDst')
        self.type = data.get('type')
        self.rank = data.get('rank')
        self.fxLink = data.get('fxLink')


class GeoWeatherData(WeatherDataSup):
    def __init__(self, data):
        super().__init__(data)
        self.location = [CityLocation(d) for d in data.get('location', [])] if data.get('location') else None
        self.topCityList = [CityLocation(d) for d in data.get('topCityList', [])] if data.get('topCityList') else None
        self.poi = [CityLocation(d) for d in data.get('poi', [])] if data.get('poi') else None
        self.refer = data.get('refer')

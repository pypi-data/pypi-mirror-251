class NowData:
    def __init__(self, data):
        self.obs_time = data['obsTime']
        self.temp = data['temp']
        self.feels_like = data['feelsLike']
        self.icon = data['icon']
        self.text = data['text']
        self.wind_360 = data['wind360']
        self.wind_dir = data['windDir']
        self.wind_scale = data['windScale']
        self.wind_speed = data['windSpeed']
        self.humidity = data['humidity']
        self.precip = data['precip']
        self.pressure = data['pressure']
        self.vis = data['vis']
        self.cloud = data['cloud']
        self.dew = data['dew']


class DailyDetail:
    def __init__(self, data):
        self.fx_date = data['fxDate']
        self.sunrise = data['sunrise']
        self.sunset = data['sunset']
        self.moonrise = data['moonrise']
        self.moonset = data['moonset']
        self.moon_phase = data['moonPhase']
        self.moon_phase_icon = data['moonPhaseIcon']
        self.temp_max = data['tempMax']
        self.temp_min = data['tempMin']
        self.icon_day = data['iconDay']
        self.text_day = data['textDay']
        self.icon_night = data['iconNight']
        self.text_night = data['textNight']
        self.wind_360_day = data['wind360Day']
        self.wind_dir_day = data['windDirDay']
        self.wind_scale_day = data['windScaleDay']
        self.wind_speed_day = data['windSpeedDay']
        self.wind_360_night = data['wind360Night']
        self.wind_dir_night = data['windDirNight']
        self.wind_scale_night = data['windScaleNight']
        self.wind_speed_night = data['windSpeedNight']
        self.humidity = data['humidity']
        self.precip = data['precip']
        self.pressure = data['pressure']
        self.vis = data['vis']
        self.cloud = data['cloud']
        self.uv_index = data['uvIndex']


class HourlyData:
    def __init__(self, data):
        self.fx_time = data['fxTime']
        self.temp = data['temp']
        self.icon = data['icon']
        self.text = data['text']
        self.wind_360 = data['wind360']
        self.wind_dir = data['windDir']
        self.wind_scale = data['windScale']
        self.wind_speed = data['windSpeed']
        self.humidity = data['humidity']
        self.pop = data['pop']
        self.precip = data['precip']
        self.pressure = data['pressure']
        self.cloud = data['cloud']
        self.dew = data['dew']


class MoonPhase:
    def __init__(self, data):
        self.fx_time = data['fxTime']
        self.value = data['value']
        self.name = data['name']
        self.illumination = data['illumination']
        self.icon = data['icon']


class AirDaily:
    def __init__(self, data):
        self.fx_date = data['fxDate']
        self.aqi = data['aqi']
        self.level = data['level']
        self.category = data['category']
        self.primary = data['primary']


class WeatherDataSup:
    def __init__(self, data):
        self.code = data.get('code')
        if self.code == '204':
            self.msg = '请求成功，但你查询的地区暂时没有你需要的数据。'
        elif self.code == '400':
            self.msg = '请求错误，可能包含错误的请求参数或缺少必选的请求参数。'
        elif self.code == '401':
            self.msg = '认证失败，可能使用了错误的KEY、数字签名错误、KEY的类型错误（如使用SDK的KEY去访问Web API）。'
        elif self.code == '402':
            self.msg = '超过访问次数或余额不足以支持继续访问服务，你可以充值、升级访问量或等待访问量重置。'
        elif self.code == '403':
            self.msg = '超过访问次数或余额不足以支持继续访问服务，你可以充值、升级访问量或等待访问量重置。'
        elif self.code == '404':
            self.msg = '查询的数据或地区不存在。'
        elif self.code == '409':
            self.msg = '超过限定的QPM（每分钟访问次数），请参考QPM说明。'
        elif self.code == '500':
            self.msg = '无响应或超时，接口服务异常请联系和风天气。'
        self.update_time = data.get('updateTime')

    def get_dict(self):
        return self.__dict__


class WeatherSun(WeatherDataSup):
    def __init__(self, data):
        super().__init__(data)
        self.sunrise = data.get('sunrise')
        self.sunset = data.get('sunset')
        self.solarElevationAngle = data.get('solarElevationAngle')
        self.solarAzimuthAngle = data.get('solarAzimuthAngle')
        self.solarHour = data.get('solarHour')
        self.hourAngle = data.get('hourAngle')

    def print_parent_dict(self):
        print(super().get_dict())


class WeatherMoon(WeatherDataSup):
    def __int__(self, data):
        super().__init__(data)
        self.moonrise = data.get('moonrise')
        self.moonset = data.get('moonset')
        self.daily = [MoonPhase(d) for d in data.get('moonPhase', [])] if data.get('moonPhase') else None

class AirQualityData:
    def __init__(self, data):
        self.pub_time = data.get('pubTime')
        self.aqi = data.get('aqi')
        self.level = data.get('level')
        self.category = data.get('category')
        self.primary = data.get('primary')
        self.pm10 = data.get('pm10')
        self.pm2p5 = data.get('pm2p5')
        self.no2 = data.get('no2')
        self.so2 = data.get('so2')
        self.co = data.get('co')
        self.o3 = data.get('o3')

class ActivityIndexData:
    def __init__(self, data):
        self.date = data.get('date')
        self.type = data.get('type')
        self.name = data.get('name')
        self.level = data.get('level')
        self.category = data.get('category')
        self.text = data.get('text')

class SolarRadiationData:
    def __init__(self, data):
        self.fx_time = data.get('fxTime')
        self.net = data.get('net')
        self.diffuse = data.get('diffuse')
        self.direct = data.get('direct')
        self.sources = data.get('sources')
        self.license = data.get('license')
class LocationAirQualityData:
    def __init__(self, data):
        self.pub_time = data.get('pubTime')
        self.name = data.get('name')
        self.id = data.get('id')
        self.aqi = data.get('aqi')
        self.level = data.get('level')
        self.category = data.get('category')
        self.primary = data.get('primary')
        self.pm10 = data.get('pm10')
        self.pm2p5 = data.get('pm2p5')
        self.no2 = data.get('no2')
        self.so2 = data.get('so2')
        self.co = data.get('co')
        self.o3 = data.get('o3')
class WeatherData(WeatherDataSup):
    def __init__(self, data):
        super().__init__(data)
        self.now = NowData(data['now']) if data.get('now') else None
        self.daily = [DailyDetail(d) for d in data.get('daily', [])] if data.get('daily') else None
        self.hourly = [HourlyData(d) for d in data.get('hourly', [])] if data.get('hourly') else None
        self.refer = data.get('refer')

class WeatherSolaraRaadiationData(WeatherDataSup):
    def __init__(self, data):
        super().__init__(data)
        self.radiation = [SolarRadiationData(d) for d in data.get('radiation', [])] if data.get('radiation') else None


class WeatherIndicesData(WeatherDataSup):
    def __init__(self, data):
        super().__init__(data)
        self.now = NowData(data['now']) if data.get('now') else None
        self.daily = [ActivityIndexData(d) for d in data.get('daily', [])] if data.get('daily') else None
        self.hourly = [HourlyData(d) for d in data.get('hourly', [])] if data.get('hourly') else None
        self.refer = data.get('refer')

class WeatherAirData(WeatherDataSup):
    def __init__(self, data):
        super().__init__(data)
        self.now = NowData(data['now']) if data.get('now') else None
        self.daily = [AirDaily(d) for d in data.get('daily', [])] if data.get('daily') else None
        self.refer = data.get('refer')

class WeatherAirNow(WeatherDataSup):
    def __init__(self, data):
        super().__init__(data)
        self.now = AirQualityData(data['now']) if data.get('now') else None
        self.now = [LocationAirQualityData(d) for d in data.get('station', [])] if data.get('station') else None
        self.refer = data.get('refer')

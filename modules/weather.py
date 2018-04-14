import json
import logging
from threading import Thread
from urllib.error import HTTPError
from urllib.request import urlopen

from modules.base import BaseModule
from settings import COLORS, open_weather_token, weather_country, weather_city

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

conditions = {"sun": u"",
              "clear": u"",
              "clouds": u"",
              "rain": u"",
              "heavy rain": u"",
              "shower": u"",
              "storm": u"",
              "thunder": u"",
              "lightning": u"",
              "hail": u"",
              "snow": u"",
              "cyclone": u"",
              "wind": u"",
              "partly cloudy": u"",
              "light showers": u"",
              "light rain": u"",
              "tornado": u"",
              "overcast": u"",
              "unknown": u""
              }


class Weather(BaseModule):
    def __init__(self):
        super(Weather, self).__init__()
        self.url = "http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={token}"
        self.thread = Thread(target=self.update)
        self.weather_data = None
        self.data = []

    def update(self):
        """Returns updated weather display"""
        while not self.shutdown:
            self.fetch_forecast()
            self.data = []
            if not self.weather_data:
                self.data.append(self.empty_forecast)
            else:
                self.data.append(self.temp)
                self.data.append(self.condition)
                self.data.append(self.description)
                self.data.append(self.city)

            logging.debug("Completed updating weather...")

            self._sleep()

    def fetch_forecast(self):
        try:
            contents = urlopen(self.url.format(city=weather_city,
                                               country=weather_country,
                                               token=open_weather_token)).read().decode('utf-8')
            self.weather_data = json.loads(contents)
        except HTTPError as err:
            logging.error(err)
            self.weather_data = {}

        # self.weather_data = {"coord": {"lon": 11.97,
        #                                "lat": 57.71},
        #                      "weather": [{"id": 800,
        #                                   "main": "Clear",
        #                                   "description": "clear sky",
        #                                   "icon": "01n"}
        #                                  ],
        #                      "base": "stations",
        #                      "main": {"temp": 279.15,
        #                               "pressure": 1018,
        #                               "humidity": 45,
        #                               "temp_min": 279.15,
        #                               "temp_max": 279.15},
        #                      "visibility": 10000,
        #                      "wind": {"speed": 7.7,
        #                               "deg": 80},
        #                      "clouds": {"all": 0},
        #                      "dt": 1523568000,
        #                      "sys": {"type": 1,
        #                              "id": 5384,
        #                              "message": 0.0022,
        #                              "country": "SE",
        #                              "sunrise": 1523506099,
        #                              "sunset": 1523557109},
        #                      "id": 2711537, "name": "Gothenburg",
        #                      "cod": 200}

    @property
    def empty_forecast(self):
        surface = self.font('light', 0.045).render('Filed to fetch forecast', True, COLORS['red'])
        position = surface.get_rect(left=self.width / 100, top=30)
        return surface, position

    @property
    def temp(self):
        temp = '%d\u00b0' % (self.weather_data['main']['temp'] - 273.15)
        surface = self.font('light', 0.15).render(temp, True, self.color)
        position = surface.get_rect(left=self.width / 200, top=2)
        return surface, position

    @property
    def condition(self):
        condition = conditions[self.weather_data['weather'][0]['main'].lower()]
        surface = self.font('icons', 0.1).render(condition, True, self.color)
        position = surface.get_rect(left=self.width / 6.5, top=3)
        return surface, position

    @property
    def description(self):
        desc = self.weather_data['weather'][0]['description'].title()
        surface = self.font('light', 0.045).render(desc, True, self.color)
        position = surface.get_rect(left=self.width / 100, top=80)
        return surface, position

    @property
    def city(self):
        city_name = self.weather_data['name']
        surface = self.font('light', 0.035).render(city_name, True, self.color)
        position = surface.get_rect(left=self.width / 100, top=110)
        return surface, position

    @property
    def sunset(self):
        pass

    @property
    def sunrise(self):
        pass

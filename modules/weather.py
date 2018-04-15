import json
import logging
import os
from threading import Thread
from urllib.error import HTTPError
from urllib.request import urlopen

import pygame

from modules.base import BaseModule
from settings import COLORS, WEATHER_API_TOKEN, WEATHER_COUNTRY, WEATHER_CITY, FIVE_MINUTES


class Weather(BaseModule):
    def __init__(self):
        super(Weather, self).__init__()
        self.url = "http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={token}"
        self.thread = Thread(target=self.update)
        self.weather_data = None
        self.data = []
        with open(os.path.join('resources', 'icon_map.json')) as f:
            self.icon_mapping = json.loads(f.read())

    def update(self):
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

            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(FIVE_MINUTES)

    def fetch_forecast(self):
        try:
            contents = urlopen(self.url.format(city=WEATHER_CITY,
                                               country=WEATHER_COUNTRY,
                                               token=WEATHER_API_TOKEN)).read().decode('utf-8')
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
        position = surface.get_rect(left=self.width / 100, top=self.height * 0.01)
        return surface, position

    @property
    def temp(self):
        temp = '%d\u00b0' % (self.weather_data['main']['temp'] - 273.15)
        surface = self.font('light', 0.15).render(temp, True, self.color)
        position = surface.get_rect(left=0, top=0)
        return surface, position

    @property
    def condition(self):
        icon_name = self.icon_mapping[str(self.weather_data['weather'][0]['id'])]['icon']
        icon_name = 'cloudy'
        surface = pygame.image.load(os.path.join('resources', 'icons', '%s.png' % icon_name))
        position = surface.get_rect(left=self.width / 8, top=self.height * 0.04)
        return surface, position

    @property
    def description(self):
        desc = self.weather_data['weather'][0]['description'].title()
        surface = self.font('regular', 0.045).render(desc, True, self.color)
        position = surface.get_rect(left=self.width / 100, top=self.height * 0.19)
        return surface, position

    @property
    def city(self):
        city_name = self.weather_data['name']
        surface = self.font('light', 0.035).render(city_name, True, self.color)
        position = surface.get_rect(left=self.width / 100, top=self.height * 0.25)
        return surface, position

    @property
    def sunset(self):
        pass

    @property
    def sunrise(self):
        pass

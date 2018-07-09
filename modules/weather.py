import json
import os
from urllib.request import urlopen

import pygame
from datetime import datetime, timedelta
from dateutil import parser
from threading import Thread

from modules.base import BaseModule
from modules.logs import setup_logger
from settings import COLORS, FIVE_MINUTES, \
    WEATHER_ICON_MAP, WEATHER_CITY, WEATHER_COUNTRY, WEATHER_API_TOKEN

logging = setup_logger(__name__)


class Weather(BaseModule):
    def __init__(self):
        super(Weather, self).__init__()
        self.smhi_api_url = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/' \
                            'version/2/geotype/point/lon/12.002109/lat/57.679769/data.json'

        self.api_url = 'http://api.openweathermap.org/data/2.5'
        self.weather_url = '{api_url}/weather?q={city},{country}&appid={token}'
        self.forecast_url = '{api_url}/forecast?q={city},{country}&appid={token}'
        self.thread = Thread(name=self.__class__.__name__, target=self.update)
        self.weather_data = {}
        self.forecast_data = {}
        self.smhi_forecast = {}
        self.data = []
        self.new_data = []
        self.icon_mapping = WEATHER_ICON_MAP

    def update(self):
        while not self.shutdown:
            self.weather_data = self.fetch_weather(self.weather_url)
            self.forecast_data = self.fetch_weather(self.forecast_url)
            self.smhi_forecast = self.fetch_smhi_forecast()

            if not self.weather_data:
                self.show_empty_forecast()
            else:
                self.show_temp()
                self.show_temp_day()
                self.show_humidity()
                self.show_pressure()
                self.show_condition()
                self.show_description()
                self.show_city()
                self.show_sunrise()
                self.show_sunset()
                self.show_forecast()
            self.data.clear()
            self.data = self.new_data[:]
            self.new_data.clear()

            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(FIVE_MINUTES)
        logging.info('Stopped %s...' % self.__class__.__name__)

    def fetch_smhi_forecast(self):
        try:
            return json.loads(urlopen(self.smhi_api_url).read().decode('utf-8'))
        except Exception as err:
            logging.error(err)
            return {}

    def fetch_weather(self, url):
        try:
            contents = urlopen(url.format(api_url=self.api_url,
                                          city=WEATHER_CITY,
                                          country=WEATHER_COUNTRY,
                                          token=WEATHER_API_TOKEN)).read().decode('utf-8')
            return json.loads(contents)
        except Exception as err:
            logging.error(err)
            return {}

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

    def show_empty_forecast(self):
        surface = self.font('light', 0.045).render('Filed to fetch forecast', True, COLORS['red'])
        position = surface.get_rect(left=self.width / 100, top=self.height * 0.01)
        return surface, position

    def show_temp(self):
        temp = '%d\u00b0' % self.find_temp(self.smhi_forecast['timeSeries'][0])
        surface = self.font('light', 0.035).render(temp, True, self.color)
        position = surface.get_rect(left=self.width * 0.01, top=0)
        self.new_data.append((surface, position))

    def show_temp_day(self):
        step = 3
        counter = 0
        init_left_pos = 0.01

        for weather in self.smhi_forecast['timeSeries']:
            forecast_time = parser.parse(weather['validTime'])
            if forecast_time.hour == (datetime.now() + timedelta(hours=step)).time().hour:
                condition = self.find_condition(weather)
                icon_name = self.icon_mapping.get(condition)['icon']
                if not os.path.isfile(os.path.join('resources', 'icons', '%s.png' % icon_name)):
                    icon_name = 'default'
                surface = pygame.image.load(
                    os.path.join('resources', 'icons', '%s.png' % icon_name))
                surface = pygame.transform.scale(surface,
                                                 (int(self.width * 0.05),
                                                  int(self.width * 0.05)))
                position = surface.get_rect(left=self.width * init_left_pos, top=self.height * 0.09)
                self.new_data.append((surface, position))

                temp = '%d\u00b0' % self.find_temp(weather)
                surface = self.font('light', 0.02).render(temp, True, self.color)
                position = surface.get_rect(left=self.width * init_left_pos, top=self.height * 0.12)
                self.new_data.append((surface, position))

                hours = forecast_time.strftime('%H:%M')
                surface = self.font('light', 0.0095).render(hours, True, self.color)
                position = surface.get_rect(left=self.width * init_left_pos, top=self.height * 0.145)
                self.new_data.append((surface, position))

                init_left_pos += 0.06
                step += 3
                counter += 1
            if counter == 5:
                break

    def find_condition(self, forecast):
        condition = 99

        for param in forecast['parameters']:
            if param['name'] == 'Wsymb2':
                condition = param['values'][0]
                break
        return condition

    def find_temp(self, forecast):
        temp = 99
        for param in forecast['parameters']:
            if param['name'] == 't':
                temp = param['values'][0]
                break
        return temp

    def show_humidity(self):
        hum_pos_top = self.height * 0.04
        hum_pos_left = self.width * 0.185

        humidity = '%d' % (self.weather_data['main']['humidity'])
        surface = self.font('light', 0.015).render(humidity, True, self.color)
        position = surface.get_rect(left=hum_pos_left, top=hum_pos_top)
        self.new_data.append((surface, position))

        hum_icon_pos_top = self.height * 0.0425
        hum_icon_pos_left = self.width * 0.24

        surface = pygame.image.load(os.path.join('resources', 'icons', 'humidity.png'))
        surface = pygame.transform.scale(surface,
                                         (int(self.width * 0.025), int(self.width * 0.025)))
        position = surface.get_rect(left=hum_icon_pos_left, top=hum_icon_pos_top)
        self.new_data.append((surface, position))

    def show_pressure(self):
        pos_top = self.height * 0.06
        pos_left = self.width * 0.17

        pressure = '%d' % (self.weather_data['main']['pressure'])
        surface = self.font('light', 0.015).render(pressure, True, self.color)
        position = surface.get_rect(left=pos_left, top=pos_top)
        self.new_data.append((surface, position))

        icon_pos_top = self.height * 0.0625
        icon_pos_left = self.width * 0.24

        surface = pygame.image.load(os.path.join('resources', 'icons', 'barometer.png'))
        surface = pygame.transform.scale(surface,
                                         (int(self.width * 0.025), int(self.width * 0.025)))
        position = surface.get_rect(left=icon_pos_left, top=icon_pos_top)
        self.new_data.append((surface, position))

    def show_condition(self):
        icon_name = self.icon_mapping.get(self.find_condition(self.smhi_forecast['timeSeries'][0]))[
            'icon']
        if not os.path.isfile(os.path.join('resources', 'icons', '%s.png' % icon_name)):
            icon_name = 'default'
        surface = pygame.image.load(os.path.join('resources', 'icons', '%s.png' % icon_name))
        surface = pygame.transform.scale(surface, (int(self.width * 0.05), int(self.width * 0.05)))
        position = surface.get_rect(left=self.width * 0.09, top=self.height * 0.007)
        self.new_data.append((surface, position))

    def show_description(self):
        condition = 99
        for param in self.smhi_forecast['timeSeries'][0]['parameters']:
            if param['name'] == 'Wsymb2':
                condition = param['values'][0]
                break
        desc = self.icon_mapping.get(condition)['label']
        surface = self.font('light', 0.01).render(desc, True, self.color)
        position = surface.get_rect(left=self.width * 0.01, top=self.height * 0.04)
        self.new_data.append((surface, position))

    def show_city(self):
        city_name = self.weather_data['name']
        surface = self.font('light', 0.01).render(city_name, True, self.color)
        position = surface.get_rect(left=self.width * 0.01, top=self.height * 0.055)
        self.new_data.append((surface, position))

    def show_sunset(self):
        sunset = datetime.fromtimestamp(self.weather_data['sys']['sunset']).strftime("%H:%M")
        surface = self.font('regular', 0.015).render(sunset, True, self.color)
        position = surface.get_rect(left=self.width * 0.17, top=self.height * 0.02)
        self.new_data.append((surface, position))

        surface = pygame.image.load(os.path.join('resources', 'icons', 'sunset.png'))
        surface = pygame.transform.scale(surface,
                                         (int(self.width * 0.025), int(self.width * 0.025)))
        position = surface.get_rect(left=self.width * 0.24, top=self.height * 0.0225)
        self.new_data.append((surface, position))

    def show_sunrise(self):
        sunrise = datetime.fromtimestamp(self.weather_data['sys']['sunrise']).strftime("%H:%M")
        surface = self.font('regular', 0.015).render(sunrise, True, self.color)
        position = surface.get_rect(left=self.width * 0.17, top=self.height * 0)
        self.new_data.append((surface, position))

        surface = pygame.image.load(os.path.join('resources', 'icons', 'sunrise.png'))
        surface = pygame.transform.scale(surface,
                                         (int(self.width * 0.025), int(self.width * 0.025)))
        position = surface.get_rect(left=self.width * 0.24, top=self.height * 0.0025)
        self.new_data.append((surface, position))

    def show_forecast(self):
        tmp = []
        today = datetime.today().replace(hour=12, minute=0, second=0, microsecond=0)
        init_left_pos = 0.01

        for forecast in self.smhi_forecast['timeSeries']:
            dt = parser.parse(forecast['validTime'])
            if dt.time() == today.time() and dt.date() != today.date():
                tmp.append(forecast)

        for weather in tmp[:5]:
            condition = self.find_condition(weather)
            icon_name = self.icon_mapping.get(condition)['icon']
            if not os.path.isfile(os.path.join('resources', 'icons', '%s.png' % icon_name)):
                icon_name = 'default'
            surface = pygame.image.load(
                os.path.join('resources', 'icons', '%s.png' % icon_name))
            surface = pygame.transform.scale(surface,
                                             (int(self.width * 0.05),
                                              int(self.width * 0.05)))
            position = surface.get_rect(left=self.width * init_left_pos, top=self.height * 0.18)
            self.new_data.append((surface, position))

            temp = '%d\u00b0' % self.find_temp(weather)
            surface = self.font('light', 0.02).render(temp, True, self.color)
            position = surface.get_rect(left=self.width * init_left_pos, top=self.height * 0.21)
            self.new_data.append((surface, position))

            hours = parser.parse(weather['validTime']).strftime('%a')
            surface = self.font('light', 0.0095).render(hours, True, self.color)
            position = surface.get_rect(left=self.width * init_left_pos, top=self.height * 0.235)
            self.new_data.append((surface, position))

            init_left_pos += 0.06

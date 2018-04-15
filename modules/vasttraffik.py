import logging
from threading import Thread

import vasttrafik
from datetime import datetime

from modules.base import BaseModule
from settings import VASTTRAFIK_KEY, VASTTRAFIK_SECRET, BUSS_STOPS, VASTTRAFIK_UPDATE_DELAY, \
    SKIP_DIRECTIONS


class Vasttrafik(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.jp = vasttrafik.JournyPlanner(key=VASTTRAFIK_KEY, secret=VASTTRAFIK_SECRET)
        self.data = []
        self.tmp_data = []
        self.traffic_scale = 0.035
        self.traffic_top = 0.26

    def update(self):
        while not self.shutdown:
            self.traffic_top = 0.26

            for stop in BUSS_STOPS:
                self.update_departures(stop)

            self.data.clear()
            self.data = self.tmp_data[:]
            self.tmp_data.clear()
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(VASTTRAFIK_UPDATE_DELAY)

    def update_departures(self, buss_stop):
        buss_stop_id = self.jp.location_name(buss_stop)[0]['id']
        departures = self.jp.departureboard(buss_stop_id)
        if not departures:
            return
        self.traffic_top += 0.042
        msg = '{stop}'.format(stop=buss_stop)
        surface = self.font('regular', self.traffic_scale).render(msg, True, self.color)
        position = surface.get_rect(left=self.width / 1.5, top=self.height * self.traffic_top)
        self.tmp_data.append((surface, position))
        self.traffic_top += 0.042

        for departure in departures:
            if any([stop in departure['direction'] for stop in SKIP_DIRECTIONS]):
                continue

            arr_hours = int(departure['time'].split(':')[0])
            arr_minutes = int(departure['time'].split(':')[1])
            arrival_time = datetime.now().replace(hour=arr_hours, minute=arr_minutes)
            arrive_in = round((arrival_time - datetime.now()).total_seconds() / 60)
            if arrive_in < 1:
                continue
            msg = '{sname}'.format(**departure)
            surface = self.font('light', self.traffic_scale).render(msg, True, self.color)
            position = surface.get_rect(left=self.width / 1.8, top=self.height * self.traffic_top)
            self.tmp_data.append((surface, position))

            msg = '{direction}'.format(**departure)
            surface = self.font('light', self.traffic_scale).render(msg, True, self.color)
            position = surface.get_rect(left=self.width / 1.6, top=self.height * self.traffic_top)
            self.tmp_data.append((surface, position))

            msg = '{time}'.format(time=arrive_in)
            surface = self.font('light', self.traffic_scale).render(msg, True, self.color)
            position = surface.get_rect(left=self.width / 1.15, top=self.height * self.traffic_top)
            self.tmp_data.append((surface, position))
            self.traffic_top += 0.042


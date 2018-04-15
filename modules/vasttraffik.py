import logging
from datetime import datetime
from threading import Thread

import vasttrafik

from modules.base import BaseModule
from settings import vasttrafik_key, vasttrafik_secret, buss_stops, skip_directions, ONE_MINUTE


class Vasttrafik(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.jp = vasttrafik.JournyPlanner(key=vasttrafik_key, secret=vasttrafik_secret)
        self.data = []
        self.tmp_data = []
        self.top = 180

    def update(self):
        while not self.shutdown:
            self.top = 180
            for stop in buss_stops:
                self.update_departures(stop)

            self.data.clear()
            self.data = self.tmp_data[:]
            self.tmp_data.clear()
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(ONE_MINUTE)

    def update_departures(self, buss_stop):
        self.top += 20
        buss_stop_id = self.jp.location_name(buss_stop)[0]['id']
        msg = '{stop}'.format(stop=buss_stop)
        surface = self.font('regular', 0.035).render(msg, True, self.color)
        position = surface.get_rect(left=self.width / 1.8, top=self.top)
        self.tmp_data.append((surface, position))
        self.top += 20

        for departure in self.jp.departureboard(buss_stop_id)[:6]:
            if any([stop in departure['direction'] for stop in skip_directions]):
                continue

            arr_hours = int(departure['time'].split(':')[0])
            arr_minutes = int(departure['time'].split(':')[1])
            arrival_time = datetime.now().replace(hour=arr_hours, minute=arr_minutes)
            arrive_in = round((arrival_time - datetime.now()).total_seconds() / 60)
            if arrive_in < 1:
                continue
            msg = '{sname}'.format(**departure)
            surface = self.font('light', 0.035).render(msg, True, self.color)
            position = surface.get_rect(left=self.width / 1.8, top=self.top)
            self.tmp_data.append((surface, position))

            msg = '{direction}'.format(**departure)
            surface = self.font('light', 0.035).render(msg, True, self.color)
            position = surface.get_rect(left=self.width / 1.6, top=self.top)
            self.tmp_data.append((surface, position))

            msg = '{time}'.format(time=arrive_in)
            surface = self.font('light', 0.035).render(msg, True, self.color)
            position = surface.get_rect(left=self.width / 1.15, top=self.top)
            self.tmp_data.append((surface, position))
            self.top += 20

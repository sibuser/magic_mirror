import logging
from datetime import datetime
from threading import Thread

import vasttrafik

from modules.base import BaseModule
from settings import vasttrafik_key, vasttrafik_secret, buss_stops, skip_directions

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO)


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
            logging.debug("Completed updating vasttrafik")
            self._sleep()

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

            msg = '{sname}'.format(**departure)
            surface = self.font('light', 0.035).render(msg, True, self.color)
            position = surface.get_rect(left=self.width / 1.8, top=self.top)
            self.tmp_data.append((surface, position))

            msg = '{direction}'.format(**departure)
            surface = self.font('light', 0.035).render(msg, True, self.color)
            position = surface.get_rect(left=self.width / 1.6, top=self.top)
            self.tmp_data.append((surface, position))

            arr_hours = int(departure['time'].split(':')[0])
            arr_minutes = int(departure['time'].split(':')[1])
            arrival_time = datetime.now().replace(hour=arr_hours, minute=arr_minutes)
            msg = '{time}'.format(time=round((arrival_time - datetime.now()).total_seconds() / 60))
            surface = self.font('light', 0.035).render(msg, True, self.color)
            position = surface.get_rect(left=self.width / 1.15, top=self.top)
            self.tmp_data.append((surface, position))
            self.top += 20

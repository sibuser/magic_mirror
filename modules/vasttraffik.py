import logging
from collections import defaultdict
from datetime import datetime
from threading import Thread

import vasttrafik

from modules.base import BaseModule
from settings import VASTTRAFIK_KEY, VASTTRAFIK_SECRET, BUSS_STOPS, VASTTRAFIK_UPDATE_DELAY, \
    SKIP_DIRECTIONS


class Vasttrafik(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.jp = vasttrafik.JournyPlanner(key=VASTTRAFIK_KEY, secret=VASTTRAFIK_SECRET)
        self.data = []
        self.new_data = []
        self.traffic_scale = 0.035
        self.traffic_top = 0.26

    def update(self):
        while not self.shutdown:
            self.traffic_top = 0.26

            for stop in BUSS_STOPS:
                self.update_departures(stop)

            self.data.clear()
            self.data = self.new_data[:]
            self.new_data.clear()
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(VASTTRAFIK_UPDATE_DELAY)

    def update_departures(self, buss_stop):
        self.traffic_top += 0.042
        buss_stop_id = self.jp.location_name(buss_stop)[0]['id']

        self.show_stop_name(buss_stop)
        self.move_down()

        for departures in group_board_by_direction(self.jp.departureboard(buss_stop_id)).values():
            if skip_direction(departures):
                continue

            departure = departures[0]

            self.show_line_number(departure)
            self.show_destination(departure)
            self.show_departure_time(departure, 1.12)

            if len(departures) > 1:
                self.show_departure_time(departures[1], 1.06)
            self.move_down()

    def show_departure_time(self, departure, left):
        arrive_in = calc_arrive_time_in_min(departure)
        msg = '{time}'.format(time=arrive_in)
        surface = self.font('light', self.traffic_scale).render(msg, True, self.color)
        position = surface.get_rect(left=self.width / left, top=self.height * self.traffic_top)
        self.new_data.append((surface, position))

    def show_destination(self, departure):
        msg = '{direction}'.format(**departure)
        surface = self.font('light', self.traffic_scale).render(msg, True, self.color)
        position = surface.get_rect(left=self.width / 1.6, top=self.height * self.traffic_top)
        self.new_data.append((surface, position))

    def show_line_number(self, departure):
        msg = '{sname}'.format(**departure)
        surface = self.font('light', self.traffic_scale).render(msg, True, self.color)
        position = surface.get_rect(left=self.width / 1.8, top=self.height * self.traffic_top)
        self.new_data.append((surface, position))

    def show_stop_name(self, buss_stop):
        msg = '{stop}'.format(stop=buss_stop)
        surface = self.font('regular', self.traffic_scale).render(msg, True, self.color)
        position = surface.get_rect(left=self.width / 1.5, top=self.height * self.traffic_top)
        self.new_data.append((surface, position))

    def move_down(self):
        self.traffic_top += 0.042


def skip_direction(departures):
    return any([stop in departures[0]['direction'] for stop in SKIP_DIRECTIONS])


def group_board_by_direction(departures):
    grouped_directions = defaultdict(list)
    for departure in departures:
        grouped_directions[departure['direction']].append(departure)
    return grouped_directions


def calc_arrive_time_in_min(arrival):
    arr_hour, arr_minutes = arrival['time'].split(':')
    arr_year, arr_month, arr_day = arrival['date'].split('-')
    return round((datetime(year=int(arr_year),
                           month=int(arr_month),
                           day=int(arr_day),
                           hour=int(arr_hour),
                           minute=int(arr_minutes)) - datetime.now()).seconds / 60)

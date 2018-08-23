from collections import defaultdict, OrderedDict

import vasttrafik
from datetime import datetime
from threading import Thread

from modules.base import BaseModule
from modules.logs import setup_logger
from settings import VASTTRAFIK_KEY, VASTTRAFIK_SECRET, BUSS_STOPS, VASTTRAFIK_UPDATE_DELAY, \
    SKIP_DIRECTIONS, COLORS

logging = setup_logger(__name__)


class Vasttrafik(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(name=self.__class__.__name__, target=self.update)
        self.data = []
        self.new_data = []
        self.traffic_scale = 0.015
        self.traffic_top = None

    def update(self):
        try:
            while not self.shutdown:
                self.traffic_top = 0.4

                for stop in BUSS_STOPS:
                    self.update_departures(stop)

                self.data.clear()
                self.data = self.new_data[:]
                self.new_data.clear()
                logging.debug("Completed updating %s..." % self.__class__.__name__)
                self.sleep(VASTTRAFIK_UPDATE_DELAY)
        except Exception as e:
                self.data.clear()
                logging.error(e)
        finally:
            if not self.shutdown:
                self.sleep(5)
                self.update()
            logging.info('Stopped %s...' % self.__class__.__name__)

    def update_departures(self, buss_stop):
        self.move_down()
        try:
            jp = vasttrafik.JournyPlanner(key=VASTTRAFIK_KEY, secret=VASTTRAFIK_SECRET, expiery=5)
            buss_stop_id = jp.location_name(buss_stop)[0]['id']
        except Exception as e:
            logging.error(e)
            return
        self.show_stop_name(buss_stop)
        self.move_down()

        for departures in group_board_by_direction(jp.departureboard(buss_stop_id)).values():
            if skip_direction(departures):
                continue

            departure = departures[0]

            self.show_buss_number(departure)
            self.show_destination(departure)

            self.show_departure_time(departure, 0.63)
            if len(departures) > 1:
                self.show_departure_time(departures[1], 0.67)
            self.move_down()

    def show_stop_name(self, buss_stop):
        msg = '{stop}'.format(stop=buss_stop)
        surface = self.font('regular', self.traffic_scale).render(msg, True, self.color)
        position = surface.get_rect(left=self.width * 0.4, top=self.height * self.traffic_top)
        self.new_data.append((surface, position))

    def show_buss_number(self, departure):
        msg = '{sname}'.format(**departure)
        surface = self.font('light', self.traffic_scale).render(msg, True, self.color)
        position = surface.get_rect(left=self.width * 0.345, top=self.height * self.traffic_top)
        self.new_data.append((surface, position))

    def show_destination(self, departure):
        msg = '{direction}'.format(**departure)
        surface = self.font('light', self.traffic_scale).render(msg, True, self.color)
        position = surface.get_rect(left=self.width * 0.4, top=self.height * self.traffic_top)
        self.new_data.append((surface, position))

    def show_departure_time(self, departure, left):
        depart_in = departure['depart_in']
        color = COLORS['white']
        if 10 < depart_in < 15:
            color = COLORS['green']
        if 6 < depart_in <= 10:
            color = COLORS['yellow']
        if depart_in <= 7:
            color = COLORS['red']

        surface = self.font('light', self.traffic_scale).render(str(depart_in), True, color)
        position = surface.get_rect(left=self.width * left, top=self.height * self.traffic_top)
        self.new_data.append((surface, position))

    def move_down(self):
        self.traffic_top += 0.016


def skip_direction(departures):
    return any([stop in departures[0]['direction'] for stop in SKIP_DIRECTIONS])


def group_board_by_direction(departures):
    grouped_directions = defaultdict(list)
    for departure in departures:
        depart_time_in = calc_depart_time_in_min(departure)
        if 1 < depart_time_in < 50:
            departure['depart_in'] = depart_time_in
            grouped_directions[departure['direction']].append(departure)

    sorted_departures = OrderedDict()
    for k, v in sorted(grouped_directions.items(), key=lambda item: item[1][0]['depart_in']):
        sorted_departures[k] = v
    return sorted_departures


def calc_depart_time_in_min(arrival):
    arr_hour, arr_minutes = arrival['time'].split(':')
    arr_year, arr_month, arr_day = arrival['date'].split('-')
    return round((datetime(year=int(arr_year),
                           month=int(arr_month),
                           day=int(arr_day),
                           hour=int(arr_hour),
                           minute=int(arr_minutes)) - datetime.now()).seconds / 60)

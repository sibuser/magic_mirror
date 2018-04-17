import logging
from datetime import datetime
from threading import Thread
from time import sleep

from modules.base import BaseModule
from settings import CLOCK_UPDATE_DELAY


class Clock(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.time_pos = 0
        self.time_scale = 0.1
        self.date_pos = 0.12
        self.date_scale = 0.035

        self.data = []
        self.new_data = []

    def update(self):
        while not self.shutdown:
            self.show_time()
            self.show_date()

            self.data = []
            self.data = self.new_data[:]
            self.new_data.clear()
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            sleep(CLOCK_UPDATE_DELAY)

    def show_time(self):
        current_time = datetime.today().strftime("%H:%M")
        surface = self.font('light', self.time_scale).render(current_time, True, self.color)
        position = surface.get_rect(left=self.width / 1.275, top=self.height * self.time_pos)
        self.new_data.append((surface, position))

    def show_date(self):
        today = datetime.today()
        text = '{weekday}, {month} {day}'.format(weekday='Saturday',
                                                 month=today.strftime('%B'),
                                                 day=today.day)
        surface = self.font('light', self.date_scale).render(text, True, self.color)
        position = surface.get_rect(left=self.width / 1.3, top=self.height * self.date_pos)
        self.new_data.append((surface, position))

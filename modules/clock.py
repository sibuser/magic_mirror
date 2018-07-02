import logging
from datetime import datetime
from threading import Thread

from modules.base import BaseModule
from settings import CLOCK_UPDATE_DELAY


class Clock(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(name=self.__class__.__name__, target=self.update)
        self.time_pos = 0
        self.time_scale = 0.07
        self.date_pos = 0.073
        self.date_scale = 0.03

        self.data = []
        self.new_data = []

    def update(self):
        while not self.shutdown:
            self.show_time()
            self.show_date()

            self.data = []
            self.data = self.new_data[:]
            self.new_data.clear()
            self.sleep(CLOCK_UPDATE_DELAY)
        logging.info('Stopped %s...' % self.__class__.__name__)

    def show_time(self):
        current_time = datetime.today().strftime("%H:%M")
        surface = self.font('regular', self.time_scale).render(current_time, True, self.color)
        position = surface.get_rect(left=self.width * 0.77, top=self.height * self.time_pos)
        self.new_data.append((surface, position))

    def show_date(self):
        today = datetime.today()
        text = '{weekday}, {month} {day}'.format(weekday=today.strftime('%A'),
                                                 month=today.strftime('%B'),
                                                 day=today.day)
        surface = self.font('regular', self.date_scale).render(text, True, self.color)
        position = surface.get_rect(left=self.width * 0.772, top=self.height * self.date_pos)
        self.new_data.append((surface, position))

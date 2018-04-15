import logging
from datetime import datetime
from threading import Thread
from time import sleep

from modules.base import BaseModule
from settings import ONE_SECOND


class Clock(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.data = []
        self.tmp_data = []

    def update(self):
        while not self.shutdown:
            self.tmp_data.append(self.date)
            self.tmp_data.append(self.time)

            self.data = []
            self.data = self.tmp_data[:]
            self.tmp_data.clear()
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            sleep(ONE_SECOND)

    @property
    def time(self):
        current_time = datetime.today().strftime("%H:%M")
        surface = self.font('light', 0.15).render(current_time, True, self.color)
        position = surface.get_rect(left=self.width / 1.4, top=2)
        return surface, position

    @property
    def date(self):
        today = datetime.today()
        text = '{weekday}, {month} {day}'.format(weekday='Saturday',
                                                 month=today.strftime('%B'),
                                                 day=today.day)
        surface = self.font('light', 0.045).render(text, True, self.color)
        position = surface.get_rect(left=self.width / 1.4, top=100)
        return surface, position

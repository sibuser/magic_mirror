from datetime import datetime
from threading import Thread

from modules.base import BaseModule
from modules.logs import setup_logger
from settings import CLOCK_UPDATE_DELAY

logging = setup_logger(__name__)


class Clock(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(name=self.__class__.__name__, target=self.update)

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
        time_pos_top = 0
        time_pos_left = 0.74
        time_scale = 0.048

        current_time = datetime.today().strftime("%H:%M")
        surface = self.font('regular', time_scale).render(current_time, True, self.color)
        position = surface.get_rect(left=self.width * time_pos_left, top=self.height * time_pos_top)
        self.new_data.append((surface, position))

    def show_date(self):
        date_pos_top = 0.052
        date_pos_left = 0.745
        date_scale = 0.02

        today = datetime.today()
        text = '{weekday}, {month} {day}'.format(weekday=today.strftime('%a'),
                                                 month=today.strftime('%b'),
                                                 day=today.day)
        surface = self.font('regular', date_scale).render(text, True, self.color)
        position = surface.get_rect(left=self.width * date_pos_left, top=self.height * date_pos_top)
        self.new_data.append((surface, position))

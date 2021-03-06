import calendar

from datetime import datetime, timedelta
from threading import Thread
from workalendar.europe import Sweden

from modules.base import BaseModule
from modules.logs import setup_logger
from settings import COLORS, CALENDAR_UPDATE_DELAY

logging = setup_logger(__name__)


class Calendar(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(name=self.__class__.__name__, target=self.update)
        self.calendar = Sweden()
        self.data = []
        self.new_data = []

    def update(self):
        while not self.shutdown:
            self.show_week_header()
            self.show_calendar()

            self.data = []
            self.data = self.new_data[:]
            self.new_data.clear()
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(CALENDAR_UPDATE_DELAY)
        logging.info('Stopped %s...' % self.__class__.__name__)

    def show_week_header(self):
        week_header_pos_left = 0.74
        week_header_pos_top = 0.8
        week_header_scale = 0.01

        for name in calendar.weekheader(2).split():
            surface = self.font('regular', week_header_scale).render(name, True, self.color)
            position = surface.get_rect(left=self.width * week_header_pos_left,
                                        top=self.height * week_header_pos_top)
            self.new_data.append((surface, position))
            week_header_pos_left += 0.03

    def show_calendar(self):
        calendar_scale = 0.01
        calendar_week_pos_top = 0.81
        calendar_day_pos_left = 0.75

        today = datetime.today()
        m = datetime.today().replace(day=1) - timedelta(days=1)
        previous_month = calendar.monthcalendar(m.year, m.month)

        for index, day in enumerate(previous_month[-1]):
            if index == 0 and day:
                break
            if day:
                color = COLORS['gray']
                if self.calendar.is_holiday(m.replace(day=day)):
                    color = COLORS['red']
                surface = self.font('regular', calendar_scale).render(str(day), True, color)
                position = surface.get_rect(left=self.width * calendar_day_pos_left,
                                            top=self.height * calendar_week_pos_top)
                self.new_data.append((surface, position))
            calendar_day_pos_left += 0.03
        calendar_day_pos_left = 0.75

        for week in calendar.monthcalendar(today.year, today.month):
            for index, day in enumerate(week):
                if day:
                    color = COLORS['white']
                    if day == today.day:
                        color = COLORS['yellow']
                    elif index == 6 or self.calendar.is_holiday(today.replace(day=day)):
                        color = COLORS['red']
                    surface = self.font('regular', calendar_scale).render(str(day), True, color)
                    position = surface.get_rect(left=self.width * calendar_day_pos_left,
                                                top=self.height * calendar_week_pos_top)
                    self.new_data.append((surface, position))
                calendar_day_pos_left += 0.03
            calendar_day_pos_left = 0.75
            calendar_week_pos_top += 0.015

        m = today.replace(day=calendar.monthrange(today.year, today.month)[1]) + timedelta(days=1)
        next_month = calendar.monthcalendar(m.year, m.month)

        calendar_week_pos_top -= 0.015
        for index, day in enumerate(next_month[0]):
            if index == 0 and day:
                break
            if day:
                color = COLORS['gray']
                if self.calendar.is_holiday(m.replace(day=day)):
                    color = COLORS['red']
                surface = self.font('regular', calendar_scale).render(str(day), True, color)
                position = surface.get_rect(left=self.width * calendar_day_pos_left,
                                            top=self.height * calendar_week_pos_top)
                self.new_data.append((surface, position))
            calendar_day_pos_left += 0.03

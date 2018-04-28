import calendar
import logging
from datetime import datetime
from threading import Thread

from workalendar.europe import Sweden

from modules.base import BaseModule
from settings import COLORS, CALENDAR_UPDATE_DELAY


class Calendar(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(name=self.__class__.__name__, target=self.update)
        self.holidays = Sweden().holidays()

        self.data = []
        self.new_data = []

    def update(self):
        while not self.shutdown:
            self.show_week_header()
            self.show_calendar()
            self.show_holidays()

            self.data = []
            self.data = self.new_data[:]
            self.new_data.clear()
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
        current_month_holidays = []
        for holiday in self.holidays:
            if holiday[0].month == today.month:
                current_month_holidays.append(holiday[0].day)

        if today.month == 1:
            previous_month = calendar.monthcalendar(today.year - 1, 12)
        else:
            previous_month = calendar.monthcalendar(today.year, today.month - 1)

        for index, day in enumerate(previous_month[4]):
            if day:
                surface = self.font('regular', calendar_scale).render(str(day), True,
                                                                      COLORS['gray'])
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
                    elif index == 6 or day in current_month_holidays:
                        color = COLORS['red']
                    surface = self.font('regular', calendar_scale).render(str(day), True, color)
                    position = surface.get_rect(left=self.width * calendar_day_pos_left,
                                                top=self.height * calendar_week_pos_top)
                    self.new_data.append((surface, position))
                calendar_day_pos_left += 0.03
            calendar_day_pos_left = 0.75
            calendar_week_pos_top += 0.015

        if today.month == 12:
            next_month = calendar.monthcalendar(today.year + 1, 1)
        else:
            next_month = calendar.monthcalendar(today.year, today.month + 1)

        calendar_week_pos_top -= 0.015
        for index, day in enumerate(next_month[0]):
            if day:
                surface = self.font('regular', calendar_scale).render(str(day), True,
                                                                      COLORS['gray'])
                position = surface.get_rect(left=self.width * calendar_day_pos_left,
                                            top=self.height * calendar_week_pos_top)
                self.new_data.append((surface, position))
            calendar_day_pos_left += 0.03

    def show_holidays(self):
        holiday_name_scale = 0.01
        holiday_name_pos_left = 0.78
        holiday_name_pos_top = 0.9

        holiday_date_pos_left = 0.75
        holiday_date_pos_top = 0.9

        today = datetime.today()
        for holiday in self.holidays:
            if holiday[0].month == today.month:
                surface = self.font('regular', holiday_name_scale).render(holiday[1], True,
                                                                          self.color)
                position = surface.get_rect(left=self.width * holiday_name_pos_left,
                                            top=self.height * holiday_name_pos_top)
                self.new_data.append((surface, position))

                surface = self.font('regular', holiday_name_scale).render(str(holiday[0].day), True,
                                                                          self.color)
                position = surface.get_rect(left=self.width * holiday_date_pos_left,
                                            top=self.height * holiday_date_pos_top)
                self.new_data.append((surface, position))
                holiday_date_pos_top += 0.015
                holiday_name_pos_top += 0.015

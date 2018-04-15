import json
import logging
import os
from datetime import datetime, date
from threading import Thread
from time import sleep

from modules.base import BaseModule

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO)


class Birthday(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.data = []
        self.birthdays = None

    def update(self):
        while not self.shutdown:
            with open(os.path.join('resources', 'birthdays.json')) as f:
                self.birthdays = json.loads(f.read())

            self.data.append(self.header)
            self.data.append(self.delimiter)
            for event in self.upcoming_birthdays:
                self.data.append(event)
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            sleep(0.100)

    @property
    def header(self):
        surface = self.font('light', 0.035).render('Upcoming Birthdays', True, self.color)
        position = surface.get_rect(left=self.width / 100, top=150)
        return surface, position

    @property
    def delimiter(self):
        surface = self.font('light', 0.045).render('-'*20, True, self.color)
        position = surface.get_rect(left=self.width / 100, top=160)
        return surface, position

    @property
    def upcoming_birthdays(self):
        top = 180
        for brth_as_str in self.get_events():
            surface = self.font('light', 0.035).render(brth_as_str, True, self.color)
            position = surface.get_rect(left=self.width / 100, top=top)
            top += 20
            yield surface, position

    def get_events(self):
        today = date.today()
        for birthday in self.birthdays:
            if birthday['month'] - today.month > 1:
                continue
            feature_date = date(today.year, 4, 20)
            yield '{name} in {days} days'.format(name=birthday['name'],
                                                 days=(feature_date - today).days)

    @property
    def date(self):
        today = datetime.today()
        text = '{weekday}, {month} {day}'.format(weekday='Saturday',
                                                 month=today.strftime('%B'),
                                                 day=today.day)
        surface = self.font('light', 0.045).render(text, True, self.color)
        position = surface.get_rect(left=self.width / 1.4, top=100)
        return surface, position

import logging
from threading import Thread

from currency_converter import CurrencyConverter

from modules.base import BaseModule
from settings import CURRENCY_UPDATE_DELAY


class Currency(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.data = []
        self.new_data = []

    def update(self):
        while not self.shutdown:
            self.show_rate()
            self.data.clear()
            self.data = self.new_data[:]
            self.new_data.clear()
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(CURRENCY_UPDATE_DELAY)

    def show_rate(self):
        surface = self.font('regular', 0.025).render('SEK/RUB', True, self.color)
        position = surface.get_rect(left=self.width / 24, top=300)
        self.new_data.append((surface, position))

        rate = CurrencyConverter().convert(1, 'SEK', 'RUB')
        surface = self.font('regular', 0.025).render(str(round(rate, 2)), True, self.color)
        position = surface.get_rect(left=self.width / 7, top=300)
        self.new_data.append((surface, position))

        surface = self.font('regular', 0.025).render('USD/RUB', True, self.color)
        position = surface.get_rect(left=self.width / 24, top=320)
        self.new_data.append((surface, position))

        rate = CurrencyConverter().convert(1, 'USD', 'RUB')
        surface = self.font('regular', 0.025).render(str(round(rate, 2)), True, self.color)
        position = surface.get_rect(left=self.width / 7, top=320)
        self.new_data.append((surface, position))

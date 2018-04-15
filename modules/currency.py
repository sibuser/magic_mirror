import logging
from threading import Thread

from currency_converter import CurrencyConverter

from modules.base import BaseModule


class Currency(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.data = []
        self.tmp_data = []

    def update(self):
        while not self.shutdown:
            self.update_rate()
            self.data = []
            self.data = self.tmp_data[:]
            self.tmp_data.clear()
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(3600)

    def update_rate(self):
        surface = self.font('regular', 0.025).render('SEK/RUB', True, self.color)
        position = surface.get_rect(left=self.width / 24, top=300)
        self.tmp_data.append((surface, position))

        rate = CurrencyConverter().convert(1, 'SEK', 'RUB')
        surface = self.font('regular', 0.025).render(str(round(rate, 2)), True, self.color)
        position = surface.get_rect(left=self.width / 7, top=300)
        self.tmp_data.append((surface, position))

        surface = self.font('regular', 0.025).render('USD/RUB', True, self.color)
        position = surface.get_rect(left=self.width / 24, top=320)
        self.tmp_data.append((surface, position))

        rate = CurrencyConverter().convert(1, 'USD', 'RUB')
        surface = self.font('regular', 0.025).render(str(round(rate, 2)), True, self.color)
        position = surface.get_rect(left=self.width / 7, top=320)
        self.tmp_data.append((surface, position))

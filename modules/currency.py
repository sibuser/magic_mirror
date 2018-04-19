import logging
from threading import Thread
from urllib.request import urlopen

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
        ecb_url = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        exchange_rates = urlopen(ecb_url).read().decode('utf-8')
        import xml.etree.ElementTree as ET
        root = ET.fromstring(exchange_rates)
        rub, sek = None, None

        for child in root[2][0]:
            if child.attrib['currency'] == 'RUB':
                rub = child.attrib['rate']
            elif child.attrib['currency'] == 'SEK':
                sek = child.attrib['rate']
            if rub and sek:
                break
        surface = self.font('regular', 0.01).render('SEK/RUB', True, self.color)
        position = surface.get_rect(left=self.width * 0.4, top=self.height * 0.005)
        self.new_data.append((surface, position))

        surface = self.font('regular', 0.01).render(str(round(float(rub)/float(sek), 2)), True, self.color)
        position = surface.get_rect(left=self.width * 0.5, top=self.height * 0.005)
        self.new_data.append((surface, position))

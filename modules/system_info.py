import logging
import netifaces as ni
import socket

from threading import Thread

from modules.base import BaseModule
from settings import SYS_INFO_UPDATE_DELAY, IP_INTERFACE


class SystemInfo(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(name=self.__class__.__name__, target=self.update)
        self.ip_scale = 0.010

        self.data = []
        self.new_data = []

    def update(self):
        while not self.shutdown:
            self.show_ip()

            self.data = []
            self.data = self.new_data[:]
            self.new_data.clear()
            self.sleep(SYS_INFO_UPDATE_DELAY)
        logging.info('Stopped %s...' % self.__class__.__name__)

    def show_ip(self):
        if socket.gethostname() == 'mirror':
            ip = ni.ifaddresses(IP_INTERFACE)[ni.AF_INET][0]['addr']
            surface = self.font('regular', self.ip_scale).render(ip, True, self.color)
            position = surface.get_rect(left=self.width * 0.01, top=self.height * 0.98)
            self.new_data.append((surface, position))

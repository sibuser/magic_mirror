import logging
from time import sleep

import pygame

from settings import FONTS, COLORS


class BaseModule(object):
    def __init__(self):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.shutdown = False
        self.thread = None
        self.color = COLORS['white']
        self.time_pos = 0
        self.time_scale = 0.15
        self.date_pos = 0.18
        self.date_scale = 0.045

    def font(self, name, scale):
        return pygame.font.Font(FONTS[name], int(scale * self.height))

    def sleep(self, max_sleep_sec=1):
        """Custom sleep method to support keyboard interruptions"""
        slept_sec = 0
        sleep_step_sec = 1
        while slept_sec <= max_sleep_sec and not self.shutdown:
            slept_sec += sleep_step_sec
            sleep(sleep_step_sec)

    def start(self):
        logging.info('Started "%s" thread' % self.__class__.__name__)
        self.thread.start()

    def stop(self):
        logging.info('Stopping "%s" thread' % self.__class__.__name__)
        self.shutdown = True

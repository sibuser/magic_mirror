# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from time import sleep

import pygame

from settings import FONTS, COLORS

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class BaseModule(object):
    def __init__(self):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.shutdown = False
        self.thread = None
        self.color = COLORS['white']

    def font(self, name, scale):
        return pygame.font.Font(FONTS[name], int(scale * self.height))

    def _sleep(self):
        """Custom sleep method to support keyboard interruptions"""
        tick = 0.0
        step = 0.1
        while tick <= 60 and not self.shutdown:
            tick += step
            sleep(step)

    def start(self):
        logging.info('Started "%s" thread' % self.__class__.__name__)
        self.thread.start()

    def stop(self):
        logging.info('Stopping "%s" thread' % self.__class__.__name__)
        self.shutdown = True

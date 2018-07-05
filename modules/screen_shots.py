import pygame
from threading import Thread

from modules.base import BaseModule
from modules.logs import setup_logger
from settings import SCREEN_SHOT_UPDATE_DELAY

logging = setup_logger(__name__)


class ScreenShot(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(name=self.__class__.__name__, target=self.update)
        self.data = []
        self.new_data = []

    def update(self):
        self.sleep(5)
        logging.info('Continue after pause')
        while not self.shutdown:
            pygame.image.save(pygame.display.get_surface(), 'screen_shot.jpg')
            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(SCREEN_SHOT_UPDATE_DELAY)
        logging.info('Stopped %s...' % self.__class__.__name__)

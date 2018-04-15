import logging
import subprocess
from datetime import datetime
from threading import Thread

from modules.base import BaseModule
from settings import TIME_TURN_ON_SCREEN, TIME_TURN_OFF_SCREEN, DISPLAY_ON_OFF_UPDATE_DELAY, \
    ENABLE_OF_OFF_SCREEN


class DisplayOnOff(BaseModule):
    """Automatically turns off the display on a Raspberry Pi"""

    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.data = []

        self.display_on = self.display_status()

    def update(self):
        logging.debug('Display status %s' % self.display_on)
        if not self.display_on and datetime.today().hour >= TIME_TURN_ON_SCREEN and ENABLE_OF_OFF_SCREEN:
            self.turn_on()
        if self.display_on and datetime.today().hour >= TIME_TURN_OFF_SCREEN and ENABLE_OF_OFF_SCREEN:
            self.turn_off()
            self.display_on = self.display_status()
        logging.debug("Completed updating %s..." % self.__class__.__name__)
        self.sleep(DISPLAY_ON_OFF_UPDATE_DELAY)

    def display_status(self):
        return int(subprocess.check_output(["vcgencmd", "display_power"]).decode("UTF-8")[-2])

    def turn_on(self):
        logging.debug("Turning screen on")
        subprocess.call(["vcgencmd", "display_power", "1"])
        self.display_on = self.display_status()

    def turn_off(self):
        logging.debug("Turning screen off")
        subprocess.call(["vcgencmd", "display_power", "0"])
        self.display_on = self.display_status()

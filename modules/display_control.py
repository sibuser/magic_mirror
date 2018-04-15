import subprocess
from datetime import datetime

from modules.base import BaseModule


class DisplayOnOff(BaseModule):
    """Automatically turns off the display on a Raspberry Pi"""
    def __init__(self):
        super().__init__()
        self.display_on = self.display_status()

    def update(self):
        if not self.display_on and datetime.today().hour > 6:
            self.turn_on()
        if self.display_on and datetime.today().hour > 23:
            self.turn_off()
            self.display_on = self.display_status()

    def display_status(self):
        return int(subprocess.check_output(["vcgencmd", "display_power"]).decode("UTF-8")[-2])

    def turn_on(self):
        subprocess.call(["vcgencmd", "display_power", "1"])
        self.display_on = self.display_status()

    def turn_off(self):
        subprocess.call(["vcgencmd", "display_power", "0"])
        self.display_on = self.display_status()

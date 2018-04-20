#!/usr/bin/env python3

import logging
from subprocess import call

import click
import pygame

from modules.birthday import Birthday
from modules.clock import Clock
from modules.currency import Currency
from modules.vasttraffik import Vasttrafik
from modules.weather import Weather
from settings import MOUSE_VISIBLE, COLORS, KEY_DOWN, KEY_ESCAPE, KEY_WINDOW_X, TEN_MS

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def check_if_exit():
    for event in pygame.event.get():
        if (event.type == KEY_DOWN and event.key == KEY_ESCAPE) or (event.type == KEY_WINDOW_X):
            logging.info('Pressed %d' % event.type)
            logging.info('Exiting...')
            return True


@click.command()
@click.option('--fullscreen', '-f',
              default=False,
              help='Run in full screen mode', is_flag=True)
@click.option('--resolution', '-r',
              default=(1080, 1920),
              type=(int, int),
              help='Window size width height')
def main(fullscreen, resolution):
    logging.info('Started the mirror')
    logging.info('Loading modules')

    pygame.init()
    mode = 0
    if fullscreen:
        logging.info('Launching in full screen mode')
        mode = pygame.FULLSCREEN
        resolution = [0, 0]
    screen = pygame.display.set_mode(resolution, mode)
    screen.fill(COLORS['black'])

    modules = [
        Weather(),
        Clock(),
        Birthday(),
        Currency(),
        Vasttrafik()
    ]
    try:
        # Check if vcgencmd is installed, to see if it is running on a
        # raspberry pi with the requires software installed
        call("vcgencmd")
        # modules.append(DisplayOnOff())
    except FileNotFoundError:
        pass

    for module in modules:
        module.start()

    pygame.mouse.set_visible(MOUSE_VISIBLE)
    try:
        while True:
            screen.fill(COLORS['black'])
            for module in modules:
                data = module.data
                for surface, position in data:
                    screen.blit(surface, position)
            pygame.display.flip()

            if check_if_exit():
                return
            pygame.time.wait(TEN_MS)
    finally:

        logging.info('Stopping all threads')
        for module in modules:
            module.stop()


if __name__ == '__main__':
    main()

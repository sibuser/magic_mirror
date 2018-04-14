#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

import logging

import click
import pygame

from modules.clock import Clock
from modules.weather import Weather
from settings import mouse_visible, COLORS, KEY_DOWN, KEY_ESCAPE, KEY_WINDOW_X

logging.basicConfig(format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO)


def check_if_exit():
    for event in pygame.event.get():
        if (event.type == KEY_DOWN and event.key == KEY_ESCAPE) or (event.type == KEY_WINDOW_X):
            logging.info('Pressed %d' % event.type)
            logging.info('Exiting...')
            return True


@click.command()
@click.option('--fullscreen', default=False, help='Run in full screen mode')
@click.option('--resolution', default=(640, 480), type=(int, int), help='Window size width height')
def main(fullscreen, resolution):
    logging.info('Started the mirror')
    logging.info('Loading modules')

    pygame.init()
    screen = pygame.display.set_mode(resolution, fullscreen)
    screen.fill(COLORS['black'])

    modules = [Weather(), Clock()]
    for module in modules:
        module.start()

    game_clock = pygame.time.Clock()
    pygame.mouse.set_visible(mouse_visible)

    while True:
        screen.fill(COLORS['black'])
        for module in modules:
            data = module.data
            for surface, position in data:
                logging.info('Got surface %s' % surface)
                screen.blit(surface, position)

        logging.info('Flip')
        pygame.display.flip()

        if check_if_exit():
            for module in modules:
                module.stop()
            return
        pygame.time.wait(1000)
        game_clock.tick(1000)


if __name__ == '__main__':
    main()

from os import path, environ

from dotenv import load_dotenv

env_path = path.join('.', '.env')
load_dotenv(dotenv_path=env_path, verbose=True)

VERSION = "0.2"

ONE_HOUR = 3600
ONE_SECOND = 1
FIVE_MINUTES = 300
ONE_MINUTE = 60
TEN_MS = 10

MOUSE_VISIBLE = False

WEATHER_API_TOKEN = environ.get('OPEN_WEATHER_TOKEN')
WEATHER_CITY = 'Gothenburg'
WEATHER_COUNTRY = 'se'
WEATHER_UPDATE_DELAY = 3600

CLOCK_UPDATE_DELAY = ONE_SECOND

CURRENCY_UPDATE_DELAY = ONE_HOUR
BIRTHDAY_UPDATE_DELAY = ONE_HOUR

TIME_TURN_OFF_SCREEN = 23
TIME_TURN_ON_SCREEN = 6

VASTTRAFIK_UPDATE_DELAY = ONE_MINUTE
VASTTRAFIK_KEY = environ.get('VASTTRAFIK_KEY')
VASTTRAFIK_SECRET = environ.get('VASTTRAFIK_SECRET')
BUSS_STOPS = ['Bifrost', 'Havrekornsgatan']
SKIP_DIRECTIONS = ['Helenedal']

KEY_DOWN = 2
KEY_ESCAPE = 27
KEY_WINDOW_X = 12

COLORS = {
    'white': (255, 255, 255),
    'gray': (128, 128, 128),
    'red': (255, 0, 0),
    'black': (0, 0, 0)
}

FONTS = {
    'heavy': path.join("resources", "font", "font-heavy.ttf"),
    'light': path.join("resources", "font", "font-light.ttf"),
    'regular': path.join("resources", "font", "font-regular.ttf")
}



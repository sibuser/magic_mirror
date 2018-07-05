from os import path, environ

from dotenv import load_dotenv

env_path = path.join('.', '.env')
load_dotenv(dotenv_path=env_path, verbose=True)

VERSION = "0.2"

THREE_HOURS = 10800
ONE_HOUR = 3600
ONE_SECOND = 1
FIVE_MINUTES = 300
ONE_MINUTE = 60
TEN_MS = 10

MOUSE_VISIBLE = False

CALENDAR_ID = environ.get('CALENDAR_ID')

WEATHER_API_TOKEN = environ.get('OPEN_WEATHER_TOKEN')
WEATHER_CITY = 'Gothenburg'
WEATHER_COUNTRY = 'se'
WEATHER_UPDATE_DELAY = 3600

SYS_INFO_UPDATE_DELAY = THREE_HOURS
IP_INTERFACE = 'wlan0'
CLOCK_UPDATE_DELAY = ONE_SECOND
CALENDAR_UPDATE_DELAY = ONE_HOUR
SCREEN_SHOT_UPDATE_DELAY = ONE_MINUTE

CURRENCY_UPDATE_DELAY = THREE_HOURS
BIRTHDAY_UPDATE_DELAY = ONE_HOUR
DISPLAY_ON_OFF_UPDATE_DELAY = ONE_MINUTE

TIME_TURN_OFF_SCREEN = 0
TIME_TURN_ON_SCREEN = 6
ENABLE_OF_OFF_SCREEN = environ.get('ENABLE_ON_OFF_SCREEN', True)

VASTTRAFIK_UPDATE_DELAY = ONE_MINUTE
VASTTRAFIK_KEY = environ.get('VASTTRAFIK_KEY')
VASTTRAFIK_SECRET = environ.get('VASTTRAFIK_SECRET')
BUSS_STOPS = ['Bifrost', 'Vetekornsgatan']
SKIP_DIRECTIONS = ['Helenedal']

KEY_DOWN = 2
KEY_ESCAPE = 27
KEY_WINDOW_X = 12

COLORS = {
    'black': (0, 0, 0),
    'aqua': (0, 255, 255),
    'blue': (0, 0, 255),
    'fuchsia': (255, 0, 255),
    'gray': (128, 128, 128),
    'green': (0, 128, 0),
    'lime': (0, 255, 0),
    'maroon': (128, 0, 0),
    'navy_blue': (0, 0, 128),
    'olive': (128, 128, 0),
    'purple': (128, 0, 128),
    'red': (255, 0, 0),
    'silver': (192, 192, 192),
    'teal': (0, 128, 128),
    'white': (255, 255, 255),
    'yellow': (255, 255, 0),
}

FONTS = {
    'heavy': path.join("resources", "font", "font-heavy.ttf"),
    'light': path.join("resources", "font", "font-light.ttf"),
    'regular': path.join("resources", "font", "font-regular.ttf")
}


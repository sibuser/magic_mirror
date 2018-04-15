from os import path, environ

version = "0.1"

mouse_visible = False

weather_city = 'Gothenburg'

weather_country = 'se'

# Delay before allowing data update in seconds,
weather_update_delay = 3600

open_weather_token = environ.get('OPEN_WEATHER_TOKEN')

vasttrafik_key = environ.get('VASTTRAFIK_KEY')
vasttrafik_secret = environ.get('VASTTRAFIK_SECRET')
buss_stops = ['Bifrost', 'Havrekornsgatan']
skip_directions = ['Helenedal']

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


ONE_HOUR = 3600
ONE_SECOND = 1
FIVE_MINUTES = 300
ONE_MINUTE = 60
TEN_MS = 10
from os import path, environ

version = "0.1"

mouse_visible = False

weather_city = 'Gothenburg'

weather_country = 'se'

# Delay before allowing data update in seconds,
weather_update_delay = 3600

open_weather_token = environ.get('OPEN_WEATHER_TOKEN')

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
    'regular': path.join("resources", "font", "font-regular.ttf"),
    'icons': path.join("resources", "font", "weather-icons.ttf"),
}

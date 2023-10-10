import web
import re


service_info: dict = {
    "url": "https://www.ventusky.com/ru/{0};{1}"
}

cities: dict = {
    "екатеринбург": ["56.821", "60.584"],
    "томск": ["56.463", "84.964"]
}


class WeatherState:
    temperature: float | None = None
    condition: str | None = None
    coordinates: list[float] = [0.0, 0.0]

    def __init__(self, temperature=0.0, condition="", coordinates=[0.0, 0.0]):
        self.temperature = temperature
        self.condition = condition
        self.coordinates = coordinates

    def __repr__(self):
        return "Weather: temperature - {0}; condition = {1}; coordinates - {2}".format(
            self.temperature, self.condition, self.coordinates
        )

    def __str__(self):
        return "Weather: temperature - {0}; condition = {1}; coordinates - {2}".format(
            self.temperature, self.condition, self.coordinates
        )


def get_weather(x_coord, y_coord) -> WeatherState | None:
    url = service_info["url"].format(x_coord, y_coord)
    source = web.get_page_source(url)
    if not source:
        return None

    temperature = web.get_class_elements(
        source, "td", "temperature")
    condition = None  # web.get_class_elements(source, "div", "link__condition day-anchor i-bem")

    weather = WeatherState()
    weather.coordinates = [x_coord, y_coord]
    try:
        weather.temperature = re.compile("\w+").findall(temperature[0])[0]
    except (IndexError, ValueError):
        weather.temperature = None

    try:
        weather.condition = None
    except (IndexError, ValueError):
        weather.condition = None

    return weather


def get_weather_by_city(city) -> WeatherState | None:
    if city not in cities.keys():
        return None

    return get_weather(cities[city][0], cities[city][1])

import sys
from constants import WEATHER_TYPES, WIND_DIRECTIONS, DEFAULT_MIN

MINIMUM_SNOW_TEMP = 2

class Day:
    def __init__(self, day):
        self._humidity = []
        self._precipitation = []
        self._pressure = []
        self._temperature = []
        self._wind_direction = []
        self._wind_speed = []
        self.is_snowing = False
        self.max_values = {"humidity": 0, "precipitation": 0, "pressure": 0, "temperature": 0,"wind_speed": 0}
        self.min_values = {"humidity": DEFAULT_MIN, "precipitation": DEFAULT_MIN, "pressure": DEFAULT_MIN,
                           "temperature": DEFAULT_MIN, "wind_speed": DEFAULT_MIN}

    # returns the weather type for a specific time
    def get_weather(self, weather_type, time):
        if weather_type == "humidity":
            return self._humidity[time]
        elif weather_type == "precipitation":
            return self._precipitation[time]
        elif weather_type == "pressure":
            return self._pressure[time]
        elif weather_type == "temperature":
            return self._temperature[time]
        elif weather_type == "wind_direction":
            return self._wind_direction[time]
        elif weather_type == "wind_speed":
            return self._wind_speed[time]
        else:
            print("Incorrect API data: weather type {} not handled. Exiting program.".format(weather_type))
            sys.exit()

    # sets the weather for each temperature type, the weather type lists fills up for each hour
    def set_weather(self, weather_type, value, city_min_values, city_max_values, overall_min_values,
                    overall_max_values, city_name):
        if isinstance(value, int):
            if weather_type == "humidity":
                self._humidity.append(value)
            elif weather_type == "precipitation":
                self._precipitation.append(value)
            elif weather_type == "pressure":
                self._pressure.append(value)
            elif weather_type == "temperature":
                self._temperature.append(value)
                if self._temperature[-1] < MINIMUM_SNOW_TEMP and self._precipitation[-1] > 0:
                    self.is_snowing = True
            elif weather_type == "wind_speed":
                self._wind_speed.append(value)

            if value < self.min_values[weather_type]:   # calculates min and max values for current day
                self.min_values[weather_type] = value
            elif value > self.max_values[weather_type]:
                self.max_values[weather_type] = value

            if value < city_min_values[weather_type]:   # calculates min and max values for current city for the week
                city_min_values[weather_type] = value
            elif value > city_max_values[weather_type]:
                city_max_values[weather_type] = value

            if value < overall_min_values[weather_type][0]:  # calculates min and max values for all cities for the week
                overall_min_values[weather_type] = [value, city_name]
            elif value > overall_max_values[weather_type][0]:
                overall_max_values[weather_type] = [value, city_name]
            elif value == overall_min_values[weather_type][0]:  # makes sure the smallest alphabetically is returned
                overall_min_values[weather_type][1] = min(overall_min_values[weather_type][1], city_name)
            elif value == overall_max_values[weather_type][0]:
                overall_min_values[weather_type][1] = min(overall_max_values[weather_type][1], city_name)

        # wind direction only has a value, no numerical operations
        elif weather_type == "wind_direction" and value in WIND_DIRECTIONS:
            self._wind_direction.append(value)
        else:
            print("Incorrect API data: Invalid value {} for weather type {}. Exiting program.".format(value, weather_type))
            sys.exit()

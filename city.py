import statistics
from constants import DAYS, WEATHER_TYPES, COMPARE_OPERATORS, DEFAULT_MIN, WIND_DIR_INDEX
from day import Day


class City:
    def __init__(self, name):
        self.name = name
        self.days = {DAYS[0]: Day(DAYS[0]),
                     DAYS[1]: Day(DAYS[1]),
                     DAYS[2]: Day(DAYS[2]),
                     DAYS[3]: Day(DAYS[3]),
                     DAYS[4]: Day(DAYS[4]),
                     DAYS[5]: Day(DAYS[5]),
                     DAYS[6]: Day(DAYS[6])}

        self.max_values = {"humidity": 0, "precipitation": 0, "pressure": 0, "temperature": 0, "wind_speed": 0}
        self.min_values = {"humidity": DEFAULT_MIN, "precipitation": DEFAULT_MIN, "pressure": DEFAULT_MIN,
                           "temperature": DEFAULT_MIN,"wind_speed": DEFAULT_MIN}
        self.median_values = {"humidity": 0, "precipitation": 0, "pressure": 0, "temperature": 0, "wind_speed": 0}
        self.is_snowing = False

    # parse the json data for the city
    def parse_json(self, weather_json, overall_min_values, overall_max_values, overall_snowing):
        all_values = {"humidity": [], "precipitation": [], "pressure": [], "temperature": [], "wind_speed": []}
        for day in DAYS:
            day_json = weather_json[day]
            for index in range(len(day_json)):
                for weather_type in WEATHER_TYPES:
                    self.days[day].set_weather(weather_type,
                                               day_json[index][weather_type],
                                               self.min_values,
                                               self.max_values,
                                               overall_min_values,
                                               overall_max_values,
                                               self.name)
                    if weather_type != WEATHER_TYPES[WIND_DIR_INDEX]:
                        all_values[weather_type].append(self.days[day].get_weather(weather_type, index))
            if not overall_snowing and self.days[day].is_snowing:
                self.is_snowing = True
        # todo - check day length if not 24
        self.set_median_values(all_values)

    # set the median values for each weather type
    def set_median_values(self, all_values):
        for weather_type in WEATHER_TYPES:
            if weather_type != WEATHER_TYPES[WIND_DIR_INDEX]:
                self.median_values[weather_type] = statistics.median(all_values[weather_type])

    # get a value for a specific weather type at a specific time
    def get_specific_value(self, weather_type, day, time):
        return self.days[day].get_weather(weather_type, time)

    # compare max or min weather value with a specified value
    def compare_value(self, weather_type, compare_operator, value, day):
        if day == "":  # if its looking through the whole week
            if compare_operator == COMPARE_OPERATORS[0]:
                return self.min_values[weather_type] < value
            elif compare_operator == COMPARE_OPERATORS[1]:
                return self.max_values[weather_type] > value
        else:          # for a specific day
            if compare_operator == COMPARE_OPERATORS[0]:
                return self.days[day].min_values[weather_type] < value
            elif compare_operator == COMPARE_OPERATORS[1]:
                return self.days[day].max_values[weather_type] > value

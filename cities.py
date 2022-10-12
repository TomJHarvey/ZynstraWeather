import requests
from city import City
from constants import DEFAULT_MIN

WEATHER_URL = "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/"


class Cities:
    def __init__(self, cities_list_json, candidate_id):
        self.max_values = {"humidity": [0, ""], "precipitation": [0, ""], "pressure": [0, ""], "temperature": [0, ""],
                           "wind_speed": [0, ""]}
        self.min_values = {"humidity": [DEFAULT_MIN, ""], "precipitation": [DEFAULT_MIN, ""],
                           "pressure": [DEFAULT_MIN, ""], "temperature": [DEFAULT_MIN, ""],
                           "wind_speed": [DEFAULT_MIN, ""]}
        self.is_snowing = False
        self.cities = {}
        self._candidate_id = candidate_id
        self._cities_list_json = cities_list_json["cities"]
        self._cities_json = {}

    # parse the json file from the api for each city
    def set_data(self, cities_json):
        for city in cities_json:  # loop through all cities and store the data in a unique City class
            self.cities[city] = City(city)
            self.cities[city].parse_json(self._cities_json[city], self.min_values, self.max_values, self.is_snowing)
            if not self.is_snowing and self.cities[city].is_snowing:
                self.is_snowing = True

    def parse_json(self):
        for city in self._cities_list_json:
            response = requests.get(WEATHER_URL + self._candidate_id + "/" + city)  # error check?
            self._cities_json[city] = response.json()

    def background_load_data(self):
        self.parse_json()
        self.set_data(self._cities_list_json)


import sys
import os
import json
import requests
import threading
from constants import DAYS, WEATHER_TYPES, COMPARE_OPERATORS, USER_INSTRUCTIONS, CHOOSE_FILE_LOCATION_STR, ENTER_FULL_PATH_STR
from cities import Cities

CITIES_URL = "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/cities/"
RECORD_PARAMS = ["high", "low"]
TOTAL_HOURS = 24
RESULTS_FILE_NAME = "results.txt"
SPEC_INPUTS_LEN = 5
COMPARE_INPUTS_LEN = 5
REC_INPUTS_LEN = 3
MED_INPUTS_LEN = 3


def main(argv):
    if len(argv) != 2 and argv[1].isnumeric():
        print("Incorrect number of args, please enter a unique candidate id between 0-100.")
        sys.exit()

    candidate_id = argv[1]
    response = requests.get(CITIES_URL)  # error check?
    cities = Cities(response.json(), candidate_id)

    # start thread to load in the api data in the background
    json_parser_thread = threading.Thread(target=cities.background_load_data, args=())
    json_parser_thread.start()

    # while data is being loaded, user can select a file path and instructions are displayed
    file_location_path = create_output_directory()
    display_user_instructions()

    # thread is passed in, so if the data is still being parsed then the user will have to wait before accessing it
    output = query_data(cities.cities, cities.max_values, cities.min_values, cities.is_snowing, json_parser_thread)
    write_output_to_file(output, file_location_path)


# creates a user input loop to interact with the dataset retrieved from the API
def query_data(cities, max_values, min_values, is_snowing, json_parser_thread):
    results = {}
    result_counter = 0
    while True:
        print("Please enter a new query.")
        successful_query = False
        user_input = input()
        if not json_parser_thread.is_alive():
            if user_input == 'q':
                break
            inputs = user_input.split()
            if len(inputs) > 0:
                if inputs[0] == "spec":
                    if len(inputs) == SPEC_INPUTS_LEN and inputs[1] in WEATHER_TYPES and inputs[2] in cities and inputs[3] in DAYS and 0 <= int(inputs[4]) < TOTAL_HOURS:
                        results[result_counter] = cities[inputs[2]].get_specific_value(inputs[1], inputs[3], int(inputs[4]))
                        print(results[result_counter])
                        result_counter += 1
                        successful_query = True
                elif inputs[0] == "compare":
                    if len(inputs) >= COMPARE_INPUTS_LEN and inputs[1] in WEATHER_TYPES and inputs[1] != WEATHER_TYPES[4] and inputs[2] in COMPARE_OPERATORS and inputs[3].isnumeric() and inputs[4] in cities:
                        day = ""
                        if len(inputs) != COMPARE_INPUTS_LEN:  # if there is the optional day argument
                            if len(inputs) == COMPARE_INPUTS_LEN + 1:
                                if inputs[5] in DAYS:
                                    day = inputs[5]  # set the day argument
                                else:
                                    continue
                        results[result_counter] = cities[inputs[4]].compare_value(inputs[1], inputs[2], int(inputs[3]), day)
                        print(results[result_counter])
                        result_counter += 1
                        successful_query = True
                elif inputs[0] == "rec":
                    if len(inputs) == REC_INPUTS_LEN and inputs[1] in WEATHER_TYPES and inputs[1] != WEATHER_TYPES[4] and inputs[2] in RECORD_PARAMS:
                        val = 0
                        if inputs[2] == RECORD_PARAMS[0]:  # chek if higher than input value
                            val = max_values[inputs[1]]
                        elif inputs[2] == RECORD_PARAMS[1]:  # check if lower than input value
                            val = min_values[inputs[1]]
                        results[result_counter] = val[1]
                        print(results[result_counter])
                        result_counter += 1
                        successful_query = True
                elif inputs[0] == "med":
                    if len(inputs) == MED_INPUTS_LEN and inputs[1] in WEATHER_TYPES and inputs[1] != WEATHER_TYPES[4] and inputs[2] in cities:
                        results[result_counter] = cities[inputs[2]].median_values[inputs[1]] # fix
                        print(results[result_counter])
                        successful_query = True
                        result_counter += 1
                elif inputs[0] == "snowing":
                    results[result_counter] = is_snowing
                    print(results[result_counter])
                    successful_query = True
                    result_counter += 1
                elif inputs[0] == "man":
                    display_user_instructions()
                elif inputs[0] == "location":
                    for city in cities:
                        print(city)
                if not successful_query:
                    print("Please enter a valid query. Type \"man\" for help.")
        else:
            print("Waiting for api data to load")
    return results


# writes the output to a json formatted file
def write_output_to_file(output, file_location_path):
    json_object = json.dumps(output, indent=4)
    with open(os.path.join(file_location_path, RESULTS_FILE_NAME), "w") as outfile:
        outfile.write(json_object)
    print("file written to {}".format(os.path.join(file_location_path, RESULTS_FILE_NAME)))


# displays user instructions
def display_user_instructions():
    print(USER_INSTRUCTIONS)


# instructs user to choose the output directory, it doesn't exist it will create it
def create_output_directory():
    valid_directory = False
    file_location_path = ""
    while not valid_directory:
        file_location_input = input(
            CHOOSE_FILE_LOCATION_STR
            + os.getcwd() + "\n" + ENTER_FULL_PATH_STR)
        if file_location_input == "":
            file_location_path = os.getcwd()
            valid_directory = True
            break

        # if a full path isn't trying to be created
        if not file_location_input.startswith(os.sep):
            file_location_path = os.path.join(os.getcwd(), file_location_input)

        if not os.path.exists(file_location_input):
            try:
                os.mkdir(file_location_input)
            except OSError:
                # this can be improved
                print("Failed to create directory")
                continue

        valid_directory = True
    print("output directory path set to {} ".format(file_location_path))
    return file_location_path


if __name__ == '__main__':
    main(sys.argv)

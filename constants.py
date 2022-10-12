WEATHER_TYPES = ["humidity", "precipitation", "pressure", "temperature", "wind_direction", "wind_speed"]
WIND_DIR_INDEX = 4
WIND_DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
COMPARE_OPERATORS = ["<", ">"]
DEFAULT_MIN = 1000000

CHOOSE_FILE_LOCATION_STR = "Please choose a location for your output text file. Press enter to use current directory or type a folder path to use in the current directory: "
ENTER_FULL_PATH_STR = "Alternatively enter a full path which is specified by starting with the platform specific file seperator / or \\ \n"

USER_INSTRUCTIONS = '''
*————————————————————————————————————————————————————*
Hello and welcome to the weather API which is used to query the weather in U.K for a specific week.
/////////////////////////////////////////////////////
The following query params are as follows

weather:
humidity, precipitation, pressure, temperature, wind_direction (only used with spec), wind_speed

location:
type “location” to see list of u.k locations

day
monday-friday

time
0-23 denoting each hour of the day

For use with compare only:

operators
“<”, “>”

unit
a numerical value for the specified weather type

For use with record only:

height
"low", "high"

/////////////////////////////////////////////////////
The following queries are available, please make sure all characters are lowercase.

q
Quit the application

location
Display list of available locations

spec
Find a specific weather type at a specific time and location
spec [weather] [location] [day] [time]
Example - spec temperature bath wednesday 10  

compare
To see if a weather type is above or below a certain value
compare [weather] [operators] [unit] [location] | optional - [day] 
Example - compare pressure < 1000 edinburgh friday 

median
Get the median value for a weather type for a specific location
med [weather] [location] | optional -[day]
Example - med temperature cardiff

record
Get the city with highest or lowest weather value that week
rec [weather] [height]
Example - rec humidity high

snowing
Returns if it has snowed at all this week in any city

man
Display this user instruction message again
*————————————————————————————————————————————————————*
'''

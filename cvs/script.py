import requests
import json
import time
import datetime

# change this value to your state abbreviation
state = ''

# change this value to the names of the cities to track
cities = []

# text returned indicating city is booked
booked_text = 'Fully Booked'

# seconds to wait between requests
delay = 10

# flag to determine if extra spacing should be given in the output
first_loop = True

# create request headers object
# 'referer' is required for request to succeed
headers = {
    'referer': 'https://www.cvs.com/immunizations/covid-19-vaccine'
}

# execute requests in a loop
while True:
    # execute network request
    response = requests.get('https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo'.format(state), headers=headers)

    # convert response to json and access city data
    city_data_list = response.json()['responsePayloadData']['data'][state.upper()]

    # convert from a list of data to an object keyed by city
    status_by_city = dict((city_data['city'], city_data['status']) for city_data in city_data_list)

    # create list of cities that are not booked
    open_cities = []

    # print city statuses
    # add open cities to open list
    # print any missing cities
    for city in cities:
        if not first_loop:
            print()
        print('CITY STATUSES: {}'.format(datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')))
        print('-----------------------------------')
        status = status_by_city[city.upper()]
        if status is not None:
            if status != booked_text:
                open_cities.append(city)
            print('{}: {}'.format(city, status))
        else:
            print('Could not find city {}'.format(city))

    # if cities are open print them and exit request loop
    if len(open_cities) > 0:
        print()
        print('CITIES WITH OPEN APPOINTMENTS')
        print('-----------------------------')

        if len(open_cities) > 0:
            for city in open_cities:
                print(city)
        
            # exit loop because cities found
            break
        else:
            print('None')

    # update flag for output padding
    first_loop = False

    # sleep for delay duration
    time.sleep(delay)
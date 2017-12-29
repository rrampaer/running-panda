import json
import csv
import requests
from http.cookies import SimpleCookie

# To get started open garmin connect in Google Chrome, log in and grab the id of your latest activity as in https://connect.garmin.com/modern/activity/<START_ID>
START_ID = 2399797019 # Paste it here
END_ID = 0 # Id to stop at if you've run this script before, leave 0 otherwise

# Then, press F12, click on "Network", press F5, scroll to the very first element, it will have your <START_ID> as name. Click on it and copy the whole value of "Cookie" in Headers > Request Headers
RAW_DATA = 'SESSION=944e7356-2189-43 ...' # Paste it inside the ''

cookie = SimpleCookie()
cookie.load(RAW_DATA)
cookies = {}
for key, morsel in cookie.items():
    cookies[key] = morsel.value

# Crawl politely, leave a way for them to contact you
headers = {
    'User-Agent': 'Some hobbyist runner and pythonista trying to bulk extract CSVs, get in touch if you have an issue with this',
    'From': 'you@domain.com'
} 

def get_next_activity_id(activity_id):
    url = 'https://connect.garmin.com/modern/proxy/activity-service/activity/{}/relative'.format(activity_id)
    r = requests.get(url, headers=headers, cookies=cookies)
    try:
        next_activity_id =  r.json()["nextActivityId"]
        return(next_activity_id)
    except KeyError as KeyError:
        print("Issue getting ")


def get_previous_activity_id(activity_id):
    url = 'https://connect.garmin.com/modern/proxy/activity-service/activity/{}/relative'.format(activity_id)
    r = requests.get(url, headers=headers, cookies=cookies)
    try:
        previous_activity_id =  r.json()["previousActivityId"]
        return(previous_activity_id)
    except KeyError:
        print('Issue getting the key ["previousActivityId"] for activity with id {}'.format(activity_id))
        return KeyError


def export_activity_laps(activity_id):
    url = 'https://connect.garmin.com/modern/proxy/download-service/export/csv/activity/{}'.format(activity_id)
    r = requests.get(url, headers=headers, cookies=cookies)
    try:
        with open('data/activities/{}.csv'.format(activity_id), 'w') as temp_file:
            temp_file.writelines(r.content.decode('utf-8'))
        return True
    except Exception as e:
        print('Issue writing the csv file for activity {}'.format(activity_id))
        return e


def export(activity_id):
    previous_id = get_previous_activity_id(activity_id)
    export_activity_laps(activity_id)
    if previous_id and previous_id != END_ID :
        export(previous_id)
    else:
        print("Finished exporting")


def main():
    export(START_ID)

if __name__ == '__main__':
    main()
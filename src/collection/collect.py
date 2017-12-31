import json
import csv
import requests
from http.cookies import SimpleCookie

# Relative path to folder in which to save the CSVs
PATH_TO_CSV_FOLDER = 'data/activities'

# To get started open garmin connect in Google Chrome, log in and grab the id of your latest activity as in https://connect.garmin.com/modern/activity/<START_ID>
START_ID = 2399797019 # Paste it here
END_ID = 0 # Id to stop at if you've run this script before, leave 0 otherwise

# Then, press F12, click on "Network", press F5, scroll to the very first element, it will have your <START_ID> as name. Click on it and copy the whole value of "Cookie" in Headers > Request Headers
RAW_DATA = 'SESSION=63497e03-bcbc-4...'

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


def get_previous_activity_id(activity_id):
    url = 'https://connect.garmin.com/modern/proxy/activity-service/activity/{}/relative'.format(activity_id)
    r = requests.get(url, headers=headers, cookies=cookies)
    try:
        previous_activity_id =  r.json()["previousActivityId"]
        return(previous_activity_id)
    except KeyError:
        print('Issue getting the key ["previousActivityId"] for activity with id {}'.format(activity_id))
        return None


def export_activity_laps(activity_id):
    url = 'https://connect.garmin.com/modern/proxy/download-service/export/csv/activity/{}'.format(activity_id)
    r = requests.get(url, headers=headers, cookies=cookies)
    try:
        with open('{}/{}.csv'.format(PATH_TO_CSV_FOLDER, activity_id), 'w') as temp_file:
            temp_file.writelines(r.content.decode('utf-8'))
    except Exception as e:
        print('Issue writing the csv file for activity {}'.format(activity_id))
        return e


def export(activity_id):
    while activity_id and activity_id != END_ID :
        export_activity_laps(activity_id)
        activity_id = get_previous_activity_id(activity_id)
    print("Finished exporting")


def main():
    export(START_ID)

if __name__ == '__main__':
    main()
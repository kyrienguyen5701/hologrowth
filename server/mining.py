import time
from datetime import datetime
import os
import json
import pandas as pd
import requests

date_format = '%Y-%m-%d'
today = datetime.now().strftime(date_format)
subDB = 'holo_subcounts.csv'
viewDB = 'holo_viewcounts.csv'
META = json.load(open('talents.json', 'r'))
YOUTUBE_V3_API_KEY = 'AIzaSyDGNHvi3763dJK_LTSXVWWwXgTGq2m7yXk'
SLEEPING_TIME = 24 * 60 * 60

sub_today, view_today = {'Date': [today]}, {'Date': [today]}

def getDataFromYoutube(API_URL, talent_name):
    req_data = json.loads(requests.get(API_URL).text)['items'][0]

    # get subscriberCount and viewCount
    sub_count = req_data['statistics']['subscriberCount']
    view_count = req_data['statistics']['viewCount']
    sub_today[talent_name] = [sub_count]
    view_today[talent_name] = [view_count]

def updateDB():
    global subDB, viewDB
    subDF = pd.read_csv(subDB, parse_dates=['Date'], encoding='utf-8')
    viewDF = pd.read_csv(viewDB, parse_dates=['Date'], encoding='utf-8')
    subDF = pd.concat([pd.DataFrame(sub_today), subDF])
    viewDF = pd.concat([pd.DataFrame(view_today), viewDF])
    subDF.set_index('Date', inplace=True)
    subDF.index = pd.to_datetime(subDF.index, format=date_format)
    viewDF.set_index('Date', inplace=True)
    viewDF.index = pd.to_datetime(viewDF.index, format=date_format)
    subDF.astype('int64').to_csv(subDB)
    viewDF.astype('int64').to_csv(viewDB)

def main():
    for branch in META.items():
        branch_name = branch[0]
        talents = branch[1]
        for talent in talents.items():
            talent_name = talent[0]
            talent_info = talent[1]
            print(f'Fetching data of {talent_name} ...')
            
            # fetch from API
            API_URL = 'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}'.format(talent_info['channelId'], YOUTUBE_V3_API_KEY)
            getDataFromYoutube(API_URL, talent_name)

    # write to DB   
    updateDB()

if __name__ == '__main__':
    while True:
        print(f'Begin mining data for {today} ...')
        sub_today, view_today = {'Date': [today]}, {'Date': [today]}
        main()
        print('Done. Go to sleeping mode')
        time.sleep(SLEEPING_TIME)
        today = datetime.now().strftime(date_format)
        
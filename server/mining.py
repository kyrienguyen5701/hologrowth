from datetime import datetime
import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(today)
subDB = '../public/holo_subcounts.csv'
viewDB = '../public/holo_viewcounts.csv'
subDF = pd.read_csv(subDB, parse_dates=['Date'], encoding="utf-8")
viewDF = pd.read_csv(viewDB, parse_dates=['Date'], encoding="utf-8")
META = json.load(open('../public/talents.json', 'r'))
AVA_FOLDER = '../src/assets/talentAvatars/'
BANNER_FOLDER = '../src/assets/talentBanners/'
API_KEY = 'AIzaSyDGNHvi3763dJK_LTSXVWWwXgTGq2m7yXk'

sub_today, view_today = {'Date': [today]}, {'Date': [today]}
for branch in META.items():
    branch_name = branch[0]
    talents = branch[1]
    for talent in talents.items():
        talent_name = talent[0]
        talent_info = talent[1]
        print(f'Fetching data of {talent_name} ...')
        API_URL = 'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics%2CbrandingSettings&id={}&key={}'.format(talent_info['channelId'], API_KEY)
        req_data = json.loads(requests.get(API_URL).text)['items'][0]
        channel_name = req_data['snippet']['title']
        sub_count = req_data['statistics']['subscriberCount']
        view_count = req_data['statistics']['viewCount']
        sub_today[channel_name] = [sub_count]
        view_today[channel_name] = [view_count]

        avatars = req_data['snippet']['thumbnails']
        for resolution, avatar in avatars.items():
            avaUrl = avatar['url']
            avaBin = requests.get(avaUrl).content
            with open(os.path.join(AVA_FOLDER, f'{talent_name}_{resolution}.png'), 'wb+') as ava:
                ava.write(avaBin)
        
subDF = pd.concat([pd.DataFrame(sub_today), subDF])
viewDF = pd.concat([pd.DataFrame(view_today), viewDF])
subDF.set_index('Date', inplace=True)
viewDF.set_index('Date', inplace=True)
subDF.to_csv(subDB)
viewDF.to_csv(viewDB)
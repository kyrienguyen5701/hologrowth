from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import requests
import re
import pandas as pd

today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
ENV_PATH = join(dirname(__file__), '../.env.local')
subDB = join(dirname(__file__), '../public/holo_subcounts.csv')
viewDB = join(dirname(__file__), '../public/holo_viewcounts.csv')
subDF = pd.read_csv(subDB, parse_dates=['Date'], encoding="utf-8")
viewDF = pd.read_csv(viewDB, parse_dates=['Date'], encoding="utf-8")
META = json.load(open(join(dirname(__file__), '../public/talents.json'), 'r'))
AVA_FOLDER = join(dirname(__file__), '../src/assets/talentAvatars/')
BANNER_FOLDER = join(dirname(__file__), '../src/assets/talentBanners/')
YOUTUBE_BANNER_START_URL = "yt3.ggpht.com/"
YOUTUBE_BANNER_END_URL = "-no-nd-rj"

load_dotenv(ENV_PATH)
YOUTUBE_V3_API_KEY = os.getenv('YOUTUBE_V3_API_KEY')

def getYoutubeChannelBanners(talent_name, channelId):
    channel = requests.get(f'https://www.youtube.com/channel/{channelId}')
    pattern = YOUTUBE_BANNER_START_URL + "(.*?)" + YOUTUBE_BANNER_END_URL
    matches = re.findall(pattern, str(channel.content))
    list_of_banners = {
        'default': {
            '1138 x 188': matches[1],
            '1707 x 282': matches[2],
            '2120 x 350': matches[3],
            '2276 x 376': matches[4],
            '2560 x 423': matches[5],
        },
        'high': {
            '320 x 180': matches[6],
            '854 x 480': matches[7],
            '1280 x 720': matches[8],
            '1920 x 1080': matches[9],
            '2120 x 1192': matches[10],
        },
        'medium': {
            '320 x 52': matches[11],
            '640 x 105': matches[12],
            '960 x 158': matches[13],
            '1280 x 211': matches[14],
            '1440 x 238': matches[15]
        }
    }
    for resolution, banners in list_of_banners.items():
        for dimension, banner in banners.items():
            bannerUrl = f'https://{YOUTUBE_BANNER_START_URL}{banner}{YOUTUBE_BANNER_END_URL}'
            bannerBin = requests.get(bannerUrl).content
            with open(os.path.join(BANNER_FOLDER, resolution, f'{talent_name}_{dimension}.png'), 'wb+') as img:
                img.write(bannerBin)

sub_today, view_today = {'Date': [today]}, {'Date': [today]}
for branch in META.items():
    branch_name = branch[0]
    talents = branch[1]
    for talent in talents.items():
        talent_name = talent[0]
        talent_info = talent[1]
        print(f'Fetching data of {talent_name} ...')

        # fetch banners
        # if talent_name != 'haato': # kaette kudasai, haato-chan
        #     getYoutubeChannelBanners(talent_name, talent_info['channelId'])
        
        # fetch from API
        API_URL = 'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}'.format(talent_info['channelId'], YOUTUBE_V3_API_KEY)
        req_data = json.loads(requests.get(API_URL).text)['items'][0]

        # get subscriberCount and viewCount
        channel_name = req_data['snippet']['title']
        sub_count = req_data['statistics']['subscriberCount']
        view_count = req_data['statistics']['viewCount']
        sub_today[channel_name] = [sub_count]
        view_today[channel_name] = [view_count]

        # get avatars
        # avatars = req_data['snippet']['thumbnails']
        # for resolution, avatar in avatars.items():
        #     avaUrl = avatar['url']
        #     avaBin = requests.get(avaUrl).content
        #     with open(os.path.join(AVA_FOLDER, resolution, f'{talent_name}.png'), 'wb+') as img:
        #         img.write(avaBin)

# write to DB   
subDF = pd.concat([pd.DataFrame(sub_today), subDF])
viewDF = pd.concat([pd.DataFrame(view_today), viewDF])
subDF.set_index('Date', inplace=True)
viewDF.set_index('Date', inplace=True)
subDF.to_csv(subDB)
viewDF.to_csv(viewDB)
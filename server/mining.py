from datetime import datetime
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json
import requests
import re
import pandas as pd

today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
ENV_PATH = os.path.join(os.path.dirname(__file__), '../.env.local')
subDB = os.path.join(os.path.dirname(__file__), '../public/holo_subcounts.csv')
viewDB = os.path.join(os.path.dirname(__file__), '../public/holo_viewcounts.csv')
subDF = pd.read_csv(subDB, parse_dates=['Date'], encoding='utf-8')
viewDF = pd.read_csv(viewDB, parse_dates=['Date'], encoding='utf-8')
META = json.load(open(os.path.join(os.path.dirname(__file__), '../public/talents.json'), 'r'))
AVA_FOLDER = os.path.join(os.path.dirname(__file__), '../src/assets/talentAvatars/')
BANNER_FOLDER = os.path.join(os.path.dirname(__file__), '../src/assets/talentBanners/')
ICON_FOLDER = os.path.join(os.path.dirname(__file__), '../src/assets/talentIcons/')
SIGNATURE_FOLDER = os.path.join(os.path.dirname(__file__), '../src/assets/talentSignatures/')
MAIN_COSTUME_FOLDER = os.path.join(os.path.dirname(__file__), '../src/assets/talentMainCostumes/')
LIVE_COSTUME_FOLDER = os.path.join(os.path.dirname(__file__), '../src/assets/talentLiveCostumes/')
THREED_COSTUME_FOLDER = os.path.join(os.path.dirname(__file__), '../src/assets/talent3DCostumes/')
WIKI_START_URL = 'https://hololive.wiki/wiki/'
YOUTUBE_BANNER_START_URL = 'yt3.ggpht.com/'
YOUTUBE_BANNER_END_URL = '-no-nd-rj'

load_dotenv(ENV_PATH)
YOUTUBE_V3_API_KEY = os.getenv('YOUTUBE_V3_API_KEY')

sub_today, view_today = {'Date': [today]}, {'Date': [today]}

def download_picture(srcUrl, destFolder, talent_name, resolution='default', dimension='', ext='.png'):
    srcBin = requests.get(srcUrl).content
    destFile = f'{talent_name}_{dimension}{ext}' if dimension else f'{talent_name}{ext}'
    with open(os.path.join(destFolder, resolution, destFile), 'wb+') as img:
        img.write(srcBin)

def getIcon(talent_name):
    url_talent_name = talent_name.replace(' ', '_')
    wiki = requests.get(f'{WIKI_START_URL}{url_talent_name}')
    soup = BeautifulSoup(wiki.content, 'html.parser')
    iconSrc = soup.find('img', {'width': '16', 'height': '16'})
    if iconSrc:
        print(iconSrc)
        iconUrl = iconSrc['alt'].replace(' ', '_')
        soup = BeautifulSoup(requests.get(f'{WIKI_START_URL}File:{iconUrl}').content, 'html.parser')
        iconUrl = soup.find('img', {'width': '512', 'height': '512'}).parent['href']
        ext = iconUrl[-4:]
        download_picture(iconUrl, ICON_FOLDER, talent_name, ext=ext)

def getSignature(talent_name):
    url_talent_name = talent_name.replace(' ', '_')
    wiki = requests.get(f'{WIKI_START_URL}{url_talent_name}')
    soup = BeautifulSoup(wiki.content, 'html.parser')
    signaturesSrc = soup.find('img', {'alt': f'{talent_name} - Signature.png'})
    signatures = dict()
    if signaturesSrc:
        signatures = {
            'default': str(signaturesSrc['src'])
        }
        if signaturesSrc.has_attr('srcset'):
            alternatives = str(signaturesSrc['srcset']).split(', ')
            for alt in alternatives:
                url_size = alt.split(' ')
                url = url_size[0]
                size = url_size[1]
                size = 'medium' if size == '1.5x' else 'high'
                signatures[size] = url
    if signatures:
        for resolution, signatureUrl in signatures.items():
            download_picture(signatureUrl, SIGNATURE_FOLDER, talent_name, resolution=resolution)

def getYoutubeChannelBanners(talent_name, channelId):
    channel = requests.get(f'https://www.youtube.com/channel/{channelId}')
    pattern = YOUTUBE_BANNER_START_URL + '(.*?)' + YOUTUBE_BANNER_END_URL
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
            download_picture(bannerUrl, BANNER_FOLDER, talent_name, resolution=resolution, dimension=dimension)

def getDataFromYoutube(API_URL):
    req_data = json.loads(requests.get(API_URL).text)['items'][0]

    # get subscriberCount and viewCount
    channel_name = req_data['snippet']['title']
    sub_count = req_data['statistics']['subscriberCount']
    view_count = req_data['statistics']['viewCount']
    sub_today[channel_name] = [sub_count]
    view_today[channel_name] = [view_count]

    # # get avatars
    # avatars = req_data['snippet']['thumbnails']
    # for resolution, avatar in avatars.items():
    #     avaUrl = avatar['url']
    #     download_picture(avaUrl, AVA_FOLDER, talent_name, resolution)

def updateDB():
    subDF = pd.concat([pd.DataFrame(sub_today), subDF])
    viewDF = pd.concat([pd.DataFrame(view_today), viewDF])
    subDF.set_index('Date', inplace=True)
    viewDF.set_index('Date', inplace=True)
    subDF.to_csv(subDB)
    viewDF.to_csv(viewDB)

def main():
    for branch in META.items():
        branch_name = branch[0]
        talents = branch[1]
        for talent in talents.items():
            talent_name = talent[0]
            talent_info = talent[1]
            print(f'Fetching data of {talent_name} ...')

            # # fetch banners
            # if talent_name != 'haato': # kaette kudasai, haato-chan
            #     getYoutubeChannelBanners(talent_name, talent_info['channelId'])
            
            # fetch from API
            API_URL = 'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}'.format(talent_info['channelId'], YOUTUBE_V3_API_KEY)
            getDataFromYoutube(API_URL)        

            # # fetch icons
            # getIcon(talent_name)

            # # fetch signatures
            # getSignature(talent_name)

    # write to DB   
    updateDB()

if __name__ == '__main__':
    main()

# TODO: add argparse
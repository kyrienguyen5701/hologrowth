import os
from datetime import datetime
import json
import pandas as pd
import requests
from db_mgr import gcp_csv_to_df, df_to_gcp_csv, gcs_bucket_name

date_format = '%Y-%m-%d'
today = datetime.now().strftime(date_format)

env = os.environ.get('ENVIRONMENT')
sub_fn = 'holo_subcounts_dev.csv'
view_fn = 'holo_viewcounts_dev.csv'
if env == 'prod':
    sub_fn = f'holo_subcounts.csv'
    view_fn = f'holo_viewcounts.csv'
sub_df = gcp_csv_to_df(gcs_bucket_name, sub_fn, parse_dates=['Date'])
view_df = gcp_csv_to_df(gcs_bucket_name, view_fn, parse_dates=['Date'])
META = json.load(open(os.path.join(os.getcwd(), 'talents.json'), 'r'))
YOUTUBE_V3_API_KEY = os.environ.get('YOUTUBE_V3_API_KEY')

sub_today, view_today = {'Date': [today]}, {'Date': [today]}

def prRed(skk): return "\033[91m{}\033[00m".format(skk)
 
def prGreen(skk): return "\033[92m{}\033[00m".format(skk)

def prCyan(skk): return "\033[96m{}\033[00m".format(skk)

def getDataFromYoutube(API_URL, talent_name):
    global sub_df, view_df
    try:
        json_data = requests.get(API_URL).text
        req_data = json.loads(json_data)['items'][0]

    	# get subscriberCount and viewCount
        sub_count = req_data['statistics']['subscriberCount']
        view_count = req_data['statistics']['viewCount']
        sub_today[talent_name] = [sub_count]
        view_today[talent_name] = [view_count]
    except requests.exceptions.MissingSchema as e:
        print(prRed('[ERROR] Cannot find the channel. Please check if the URL is valid or whether the channel is banned or terminated.\n'))
        sub_today[talent_name] = [sub_df.iloc[0][talent_name]]
        view_today[talent_name] = [view_df.iloc[0][talent_name]]

def updateDB():
    global sub_fn, view_fn, sub_df, view_df
    sub_df = pd.concat([pd.DataFrame(sub_today), sub_df])
    view_df = pd.concat([pd.DataFrame(view_today), view_df])
    sub_df.set_index('Date', inplace=True)
    sub_df.index = pd.to_datetime(sub_df.index, format=date_format)
    view_df.set_index('Date', inplace=True)
    view_df.index = pd.to_datetime(view_df.index, format=date_format)
    sub_df = sub_df.astype('int64')
    view_df = view_df.astype('int64')
    df_to_gcp_csv(sub_df, gcs_bucket_name, sub_fn)
    df_to_gcp_csv(view_df, gcs_bucket_name, view_fn)

def main():
    for branch in META.items():
        branch_name = branch[0]
        talents = branch[1]
        for talent in talents.items():
            talent_name = talent[0]
            talent_info = talent[1]
            print(f'Fetching data of {prCyan(talent_name)} ...')
            
            # fetch from API
            API_URL = 'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}'.format(talent_info['channelId'], YOUTUBE_V3_API_KEY)
            getDataFromYoutube(API_URL, talent_name)

    # write to DB   
    updateDB()

if __name__ == '__main__':
    print(f'[LOG] Begin mining data for {prGreen(today)} ...')
    sub_today, view_today = {'Date': [today]}, {'Date': [today]}
    main()
    print('[LOG] Done.')
    
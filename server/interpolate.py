import re
import os
import requests
from bs4 import BeautifulSoup
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
META = json.load(open(os.path.join(os.path.dirname(__file__), '../public/talents.json'), 'r', encoding='utf-8'))
END_INTERPOLATE = '2021-03-23'
months = {
    "Jan.": "01",
    "Feb.": "02",
    "Mar.": "03",
    "Apr.": "04",
    "May": "05",
    "May.": "05",
    "June": "06",
    "Jun ": "06",
    "Jun.": "06",
    "Jul.": "07",
    "Jule": "07",
    "July": "07",
    "Aug.": "08",
    "Sep.": "09",
    "Oct.": "10",
    "Nov.": "11",
    "Dec.": "12"
}

# spike when milestone is near
def padding(sub_count):
    if sub_count >= 100000:
        sub_count += (sub_count + 100000) // 200000 * 1000
    return sub_count

df = pd.DataFrame()
for branch in META.items():
    branch_name = branch[0]
    talents = branch[1]
    for talent in talents.items():
        talent_name = talent[0]
        talent_info = talent[1]
        print(f'Fetching data of {talent_name} ...')
        url_talent_name = talent_name.replace(' ', '_')
        url = f'https://hololive.wiki/wiki/{url_talent_name}'
        info = requests.get(url).content
        soup = BeautifulSoup(info, "html.parser")
        allh3 = soup.findAll('h3')

        milestones = dict()

        for h3 in allh3:
            content = str(h3.string)
            if re.compile('\d{4}').search(content):
                year = re.findall(r'\d{4}', content)[0]
                timestamps = str(h3.find_next_sibling())

                pattern = '<b>(.{7})</b> Achieved a (\d.*) You' if talent_name != 'Yuzuki Choco' else '<b>(.{7})</b> The main YouTube channel achieved a (\d.*) YouTube'
                matches = re.findall(pattern, timestamps)
                end_interpolate = '2021-03-23' if talent_name != 'IRyS' else '2021-07-25'
                for match in matches:
                    date = match[0]
                    milestone = padding(int(match[1].split()[0].replace(',', '')))
                    if f'{year}-{months[date[:4]]}-{date[5:]}' >= end_interpolate:
                        continue
                    milestones[milestone] = f'{year}-{months[date[:4]]}-{date[5:]}'

        df = pd.DataFrame({
            'Date': milestones.values(),
            talent_name: milestones.keys()
        })
        interpolatePath = f'../archive/temp/{talent_name}.csv'
        # df = pd.read_csv(interpolatePath, parse_dates=['Date'], encoding='utf-8')
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index)
        number_of_milestones = len(df.index)
        for idx, date in enumerate(df.index):
            if idx >= 2:
                previous_day = date - datetime.timedelta(days=1)
                dist = (date - df.index[idx - 1]).days
                if dist == 1:
                    continue
                current_milestone = df.loc[date][talent_name]
                previous_milestone = df.loc[df.index[idx - 1]][talent_name]
                spike = int((current_milestone - previous_milestone) / dist * 2)
                df.loc[previous_day] = df.loc[date] - spike 
        df = df.resample('D').interpolate('spline', order=1.2)
        df[talent_name] //= 1
        df.loc['2019-08-01':][talent_name][df[talent_name] >= 1000] = df[talent_name] // 100 * 100
        df.loc['2019-08-01':][talent_name][df[talent_name] >= 100000] = df[talent_name] // 1000 * 1000
        # print(df.head())
        df[talent_name] = df[talent_name].astype('int64')
        df.to_csv(os.path.join(os.path.dirname(__file__), interpolatePath))
        # plt.plot(df.index, df[talent_name], color='red')
        # plt.title(r'Houshou Ichimi Count since debut')
        # plt.xticks(rotation=45)
        # plt.ylabel('Overseas Sexy Guys & Ladies Count')
        # plt.show()
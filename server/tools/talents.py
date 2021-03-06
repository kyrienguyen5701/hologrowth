import os
import json
import pandas as pd

talentsFilePath = '../../public/talents.json'
talentsDestPath = '../../src/assets/json/talents.json'
bgmDir = '../../src/assets/sounds/bgm'
soloDir = '../../src/assets/sounds/solo'

with open(talentsFilePath) as f:
    content = json.load(f)

df = pd.DataFrame(columns=['branch', 'genNumber', 'genName', 'genOther', 'name', 'channelId', 'bgm', 'solo'])

i = 0
for branch, branchInfo in content.items():
    for talentName, talentInfo in branchInfo.items():
        channelId = talentInfo['channelId']
        gens = talentInfo['generation']
        
        genNum = gens[0]
        genName = ''
        genOther = []

        if not isinstance(genNum, int):
            genName = genNum
            try:
                genNum = gens[1]
            except:
                genNum = ''
        else:
            genNum = str(genNum)
            
        if len(gens) > 2:
            genOther = gens[2:]

        bgm = os.listdir(f'{bgmDir}/{talentName}')
        solo = os.listdir(f'{soloDir}/{talentName}')

        df.loc[i] = [branch, genNum, genName, genOther, talentName, channelId, bgm, solo]
        i += 1

df['genNumber'] = df['genNumber'].astype('str')
df.to_json(talentsDestPath, orient='records', force_ascii=False, indent=4)
import os
import json
import pandas as pd

talentsFilePath = '../../public/talents.json'
talentsDestPath = '../../src/assets/json/talents.json'
bgmDir = '../../src/assets/sounds/bgm'
soloDir = '../../src/assets/sounds/solo'
localizeFilePath = '../../src/assets/json/localization.json'

with open(talentsFilePath, 'r', encoding='utf-8') as f:
    content = json.load(f)

with open(localizeFilePath, 'r', encoding='utf-8') as f:
    localize = json.load(f)

df = pd.DataFrame(columns=['id', 'branch', 'genNumber', 'genName', 'genOther', 'name', 'basicInfo', 'officialBio', 'tags', 'channelId', 'twitter', 'bgm', 'solo'])

i = 0
for branch, branchInfo in content.items():
    for talentName, talentInfo in branchInfo.items():
        twitter = talentInfo['twitter']
        channelId = talentInfo['channelId']
        gens = talentInfo['generation']
        idx = i
        genNum = gens[0]
        genName = ''
        genOther = []
        tags = talentInfo['tags']

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

        basicInfo = {
            "debutDate": talentInfo["debutDate"],
            "officialWebsite": talentInfo["officialWebsite"],
            "age": talentInfo["age"] if "age" in talentInfo.keys() else '',
            "birthday": talentInfo["birthday"],
            "height": talentInfo["height"],
            "zodiacSign": talentInfo["zodiacSign"],
        }

        localize_key = f'bio-{"-".join(talentName.lower().split(" "))}'
        officialBio = localize_key
        localize[localize_key] = {
            "en": talentInfo["officialBio"],
            "jp": ''
        }

        bgm = os.listdir(f'{bgmDir}/{talentName}') if os.path.isdir(f'{bgmDir}/{talentName}') else []
        solo = os.listdir(f'{soloDir}/{talentName}') if os.path.isdir(f'{soloDir}/{talentName}') else []

        df.loc[i] = [idx, branch, genNum, genName, genOther, talentName, basicInfo, officialBio, tags, channelId, twitter, bgm, solo]
        i += 1

df['genNumber'] = df['genNumber'].astype('str')
df.to_json(talentsDestPath, orient='records', force_ascii=False, indent=4)
json.dump(localize, open(localizeFilePath, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
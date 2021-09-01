
import os
import json
import pandas as pd

talentsFilePath = '../public/talents.json'
talentsDestPath = '../src/assets/json/talents.json'
bgmDir = '../src/assets/sounds/bgm'
soloDir = '../src/assets/sounds/solo'
localizeFilePath = '../src/assets/json/localization.json'

with open(talentsFilePath, 'r', encoding='utf-8') as f:
    content = json.load(f)

with open(localizeFilePath, 'r', encoding='utf-8') as f:
    localize = json.load(f)

df = pd.DataFrame(columns=['id', 'branch', 'genNumber', 'genName', 'genOther', 'name', 'basicInfo', 'officialBio', 'tags', 'channelId', 'twitter', 'officialWebsiteEN', 'officialWebsiteJP','bgm', 'solo'])

i = 0
for branch, branchInfo in content.items():
    for talentName, talentInfo in branchInfo.items():
        twitter = talentInfo['twitter'].replace("https://twitter.com/", "")
        channelId = talentInfo['channelId']
        officialWebsiteEN = talentInfo["officialWebsite"]["en"]
        officialWebsiteJP = talentInfo["officialWebsite"]["jp"]
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
            "age": talentInfo["age"].replace(" years old", "") if "age" in talentInfo.keys() else '',
            "height": talentInfo["height"] if "height" in talentInfo.keys() else '',
            "birthday": talentInfo["birthday"] if "birthday" in talentInfo.keys() else '',
            "debutDate": talentInfo["debutDate"],
            "zodiacSign": talentInfo["zodiacSign"] if "zodiacSign" in talentInfo.keys() else ''
        }

        if talentName not in localize.keys():
            localize[talentName] = {
                "en": talentName,
                "jp": tags[0]
            }
        menu_localize_key = f'menu-{"-".join(talentName.lower().split(" "))}'
        if menu_localize_key not in localize.keys():
            localize[menu_localize_key] = {
                "en": talentName,
                "jp": tags[0]
            }
        bio_localize_key = f'bio-{"-".join(talentName.lower().split(" "))}'
        officialBio = bio_localize_key
        if bio_localize_key not in localize.keys():
            localize[bio_localize_key] = {
                "en": talentInfo["officialBio"],
                "jp": ''
            }

        bgm = os.listdir(f'{bgmDir}/{talentName}') if os.path.isdir(f'{bgmDir}/{talentName}') else []
        solo = os.listdir(f'{soloDir}/{talentName}') if os.path.isdir(f'{soloDir}/{talentName}') else []

        df.loc[i] = [idx, branch, genNum, genName, genOther, talentName, basicInfo, officialBio, tags, channelId, twitter, officialWebsiteEN, officialWebsiteJP, bgm, solo]
        i += 1

df['genNumber'] = df['genNumber'].astype('str')
jsonStr = df.to_json(orient='records', force_ascii=False, indent=2)
jsonStr = jsonStr.replace("\\/", "/")
with open(talentsDestPath, mode='w+', encoding='utf-8') as f:
    f.writelines(jsonStr)

json.dump(localize, open(localizeFilePath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
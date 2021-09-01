import json
import statistics

talents = json.load(open('../src/assets/json/talents.json', 'r', encoding='utf-8'))
songs = json.load(open('../src/assets/json/songs.json', 'r', encoding='utf-8'))

def missing_data():
    for talent in talents:
        for song in talent['bgm'] + talent['solo']:
            flag = False
            for v in songs.values():
                if song == v['path']:
                    flag = True
            if not flag:
                print(f'Song not found: {talent["name"]} - {song}')

def song_count():
    counts = []
    for talent in talents:
        count = len(talent['bgm'] + talent['solo'])
        print(f'{talent["name"]}: {count}')
        counts.append(count)
    print(f'Mean: {statistics.mean(counts)}')
    print(f'Mode: {statistics.mode(counts)}')
    print(f'Max: {max(counts)}')
    print(f'Min: {min(counts)}')


cmds = {
    'missing_data': missing_data,
    'song_count': song_count,
    'q': exit
}
    
if __name__ == '__main__':
    while True:
        cmd = input('Command: ')
        if cmd not in cmds.keys():
            print('Invalid command.')
        else:
            cmds[cmd]();
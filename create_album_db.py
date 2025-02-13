#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import collections
from requests.exceptions import ReadTimeout
import time

# auth
# https://developer.spotify.com/dashboard
#

album_db_file='albums_db.json'

global sp

def lookup(artist, track):
    data = None
    duration = 0
    sleep=30
    c=0
    
    while data == None:
        c+=1
        try:
            data, duration = api_lookup(artist[:100], track[:100])
        except ReadTimeout:
            if c >= 5:
                print(f'hit max retry {c}, skipping this request...')
                return None, 0
            print(f'The request timed out, try {c}. Trying again in {sleep}s')
            time.sleep(sleep)
            continue

    
    return data, duration

def api_lookup(artist, track):
    q="track:\"%s\" artist:\"%s\" " % (track, artist)    
    result = sp.search(q=q, limit=2, offset=0, type='track', market='US')
    if result['tracks']['total'] == 0:
        # none found
        return "", (30 * 1000) # 30s
    if result['tracks']['total'] > 1:
        # multiple found, choosing first
        print("!!!! WARNING: multiple results found", result['tracks']['total'], q)
        for a in result['tracks']['items']:
            print(f'\t - {a['album']['name']}')


    album = result['tracks']['items'][0]['album']['name']
    duration = result['tracks']['items'][0]['duration_ms']
    return album, duration

def load():
    db=collections.defaultdict(dict)
    with open('data.json', 'r') as file:
        data = json.load(file)
        
        count = 0
        
        for d in data:
            a = d["master_metadata_album_artist_name"]
            t = d["master_metadata_track_name"]
            if t in db[a]:
                db[a][t]+=1
            else:
                db[a][t] = 1
                count+=1
    
    print(f'loaded {len(data)} into {count} from {len(db)} artists')
    return db


def save(albums):
    with open(album_db_file, "w") as file:
        json.dump(albums, file, indent=2)

def run(db):
    albums={}
    try:
        with open(album_db_file, 'r') as file:
            albums = json.load(file)
    except:
        pass

    count=0
    for artist in db:
        for track in db[artist]:
            count+=1
            
            if artist not in albums:
                print(f'new artist: {artist}')
                albums[artist] = {}
                
            if track in albums[artist]:
                continue
            print(f'{count}: new track: {track}')
            album, ms = lookup(artist, track)
            albums[artist][track] = {
                "album": album,
                "ms_played": ms
            }
            print(f'\t{album}')
            
            # save every so often to resume if needed
            if count % 100 == 0:
                print(f'## at count: {count}, saving')
                save(albums)
    
    print(f'finished at count {count}, saving')
    save(albums)

def main(): 
    global sp
    
    # auth
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # run
    db = load()
    run(db)
    
    
if __name__ == "__main__": 
    main()

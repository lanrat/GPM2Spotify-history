#!/usr/bin/env python
import json
import collections

def load_albums():
    data = []
    albums = db=collections.defaultdict(dict)
    with open('data.json', 'r') as file:
        data = json.load(file)
    with open('albums_db.json', 'r') as file:
        albums = json.load(file)
    out = []
    
    count=0
    
    for d in data:
        a = d["master_metadata_album_artist_name"]
        t = d["master_metadata_track_name"]
        album_data = albums[a][t]
        if album_data:
            d["master_metadata_album_album_name"] = album_data['album']
            d['ms_played'] = album_data['ms_played']
            count+=1
        out.append(d)
    
    print(f'added {count}/{len(out)} albums to tracks')
    return out


def main():
    
    data = load_albums()
    with open("Streaming_History_Audio_Spotify.json", "w") as file:
        json.dump(data, file, indent=2)
    
if __name__ == "__main__": 
    main() 
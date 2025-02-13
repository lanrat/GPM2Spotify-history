#!/usr/bin/env python3
from pyquery import PyQuery
import dateparser
from datetime import datetime
import json

def parseActivity(file): 
    pq = PyQuery(filename=file)
    tag = pq('div.mdl-typography--body-1')
    
    items = []
    for item in tag:
        if item.text == None:
            continue
        t = item.text_content()
        if not t.startswith("Listened"):
            continue

        parts = []
        for p in item.itertext():
            # cleanup
            p = p.strip()
            p = p.replace("\n", " ")
            p = ' '.join(p.split())
            
            # remove junk elements
            if p.startswith("Activity: "):
                continue
            if p.startswith("Temperature: "):
                continue
            if p.startswith("Weather: "):
                continue
            if p.startswith("Sun: "):
                continue
            if p.startswith("Served ") and p.endswith(" recommendations"):
                continue
            if p.startswith("Location: "):
                continue
            
            parts.append(p.strip())
        parts[0] = parts[0].removeprefix('Listened toÂ').strip()
        
        if len(parts) != 3:
            # just a few don't parse, ok to skip over
            continue

        title = parts[0]
        artist = parts[1]
        date_str = parts[2]
        date = dateparser.parse(date_str)
        
        #print("[%s] %s: %s" % (date, artist, title))
        
        song = {}
        song["ts"] = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        song["master_metadata_track_name"] = title
        song["master_metadata_album_artist_name"] = artist
        
        items.append(song)
        
    return items
        

def main(): 
    items = parseActivity('MyActivity.html') 
    print(f' got {len(items)} to save')
    with open("data.json", "w") as file:
        json.dump(items, file, indent=2)
    print("done")
      
      
if __name__ == "__main__": 
    main()

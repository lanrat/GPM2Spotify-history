# Google Play Music Activity to Spotify Activity

These scripts convert `MyActivity.html` files generated from legacy Google Takeout dumps to the JSON export format used by Spotify.

This allows you to use old data saved from GPM on more modern tools that can accept the Spotify format, like scrobbles.

## parse_gmp_activity.py

This program reads the data from your `MyActivity.html` and generates a Spotify compliant export named `data.json`. The only fields set are the timestamp, track title, and artist.

Notably the Album is mussing. This is a limitation due to the data Google provided in `MyActivity.html`.

## create_album_db.py

This program makes uses the previously generated `data.json` and the Spotify API to create `albums_db.json` which contains the missing album information for `data.json`

## add_albums.py

This program takes the previously generated album data from `albums_db.json` to add album data to `data.json` and saves it in `data_albums.json`.

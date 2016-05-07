#!/usr/bin/env python

import os
from similarity import Similarity
from models import Artist

ROOT = 'lyrics/'
artists = []

# load all the artists (and their songs)
for (dirpath, dirnames, filenames) in os.walk(ROOT):
    if dirpath != ROOT:
        artists.append(Artist(dirpath))

sim = Similarity(artists)

# count number of artists in similarity database
count = 0
for artist in artists:
	if artist.name in sim.artist_name_to_db_id.keys():
		count += 1

# print out the results
print "number of scraped artists IN similarity database:", count
print "total scraped artists:", len(artists)

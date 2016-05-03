#!/usr/bin/env python
import os
from similarity import Similarity
from cluster import Cluster
from artist import Artist
from collections import defaultdict

ROOT = 'lyrics/'

artists = []

for (dirpath, dirnames, filenames) in os.walk(ROOT):
    if dirpath != ROOT:
        artists.append(Artist(dirpath))

name_to_obj = {}
for artist in artists:
    name_to_obj[artist.name] = artist

sim = Similarity()
for artist in artists:
    correct_similar_names = sim.who_is_similar_to(artist.name)
    artist.correct_similar = map(lambda name: name_to_obj[artist], correct_similar_names)

cluster = Cluster(artists)
cluster.cluster()

label_to_artists = defaultdict(lambda: [])

for artist in artists:
    label_to_artists[artist.label].append(artist)

for artist in artists:
    artist.predicted_similar = label_to_artists[artist.label][:].remove(artist)

import pdb; pdb.set_trace()
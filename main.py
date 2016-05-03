#!/usr/bin/env python
import os
from similarity import Similarity
from cluster import Cluster
from artist import Artist
from collections import defaultdict
from marble_exceptions import NoArtistWithNameError

ROOT = 'lyrics/'

artists = []

for (dirpath, dirnames, filenames) in os.walk(ROOT):
    if dirpath != ROOT:
        artists.append(Artist(dirpath))

name_to_obj = {}
for artist in artists:
    name_to_obj[artist.name] = artist

def names_to_objs(names):
    objs = []
    for name in names:
        try:
            objs.append(name_to_obj[name])
        except KeyError,e:
            continue
    return objs


sim = Similarity()
for artist in artists:
    try:
        correct_similar_names = sim.who_is_similar_to(artist.name)
        artist.correct_similar = names_to_objs(correct_similar_names)
    except NoArtistWithNameError,e:
        continue

cluster = Cluster(artists)
cluster.cluster()

label_to_artists = defaultdict(lambda: [])

for artist in artists:
    label_to_artists[artist.label].append(artist)

for artist in artists:
    predicted_artists = label_to_artists[artist.label][:]

    # remove this artist from the cluster
    predicted_artists.remove(artist)
    
    artist.predicted_similar = predicted_artists

total_correct = 0
for artist in artists:
    total_correct += artist.num_correct()

print "correct", total_correct
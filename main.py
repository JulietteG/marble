#!/usr/bin/env python
import os
import numpy as np
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

# remove artists not in the similarity database
artists = filter(lambda artist: artist.name in sim.artist_to_id.keys(),artists)

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

num_correct,gold,precision,recall = [],[],[],[]
for artist in artists:
    num_correct.append(artist.num_correct())
    precision.append(artist.precision())
    recall.append(artist.recall())
    gold.append(len(artist.correct_similar))

print "correct:", sum(num_correct)
print "total gold:", sum(gold)
print "avg precision:", np.average(precision)
print "avg recall:", np.average(recall)
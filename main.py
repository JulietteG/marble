#!/usr/bin/env python
import os,sys
import numpy as np
from similarity import Similarity
from cluster import Cluster
from artist import Artist
from collections import defaultdict
from marble_exceptions import NoArtistWithNameError

ROOT = 'lyrics/'

def progress(n,mod=100):
    if n % mod == 0:
        sys.stderr.write('.')

def load_artists():
    sys.stderr.write("Loading artists...")

    artists = []
    _id = 1
    for (dirpath, dirnames, filenames) in os.walk(ROOT):
        if dirpath != ROOT:
            progress(_id)
            artists.append(Artist(_id,dirpath))
            _id += 1

    sys.stderr.write("\n")

    return artists

def load_sim_db(artists):
    sys.stderr.write("Loading similarity database...")
    sim = Similarity(artists)

    # remove artists not in the similarity database
    artists = filter(lambda artist: artist.in_sim_db,artists)

    sys.stderr.write("\n")

    return sim

def load_gold_standard(sim,artists):
    sys.stderr.write("Processing gold standard...")

    # set correct_similar for all artists
    for (i,artist) in enumerate(artists):
        progress(i)
        try:
            artist.correct_similar = sim.who_is_similar_to(artist)
        except NoArtistWithNameError, e:
            continue

    sys.stderr.write("\n")

def calc_stats(artists):
    sys.stderr.write("Calculating statistics...\n")

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

if __name__ == '__main__':
    artists = load_artists()
    sim = load_sim_db(artists)
    load_gold_standard(sim,artists)
    calc_stats(artists)
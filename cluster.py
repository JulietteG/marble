#!/usr/bin/env python

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

class Cluster(object):
    def __init__(self,artists):
        self.artists = artists

    def cluster(self):
        data = map(lambda artist: artist.all_songs_text(), self.artists)

        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(data)

        km = KMeans(n_clusters=50)
        km.fit(X)

        for (i,label) in enumerate(km.labels_):
            self.artists[i].label = label
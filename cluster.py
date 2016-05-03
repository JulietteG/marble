#!/usr/bin/env python

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

class Cluster(object):
    def __init__(self,artists):
        self.artists = artists

    def cluster(self):
        data = map(lambda artist: artist.all_songs_text(), self.artists)

        vectorizer = CountVectorizer(ngram_range=(1,2),stop_words='english')
        X = vectorizer.fit_transform(data)

        # for (i,artist) in enumerate(self.artists):
        #     lines = artist.all_songs_lines()

        #     # TODO: this is actually just the number of words per line
        #     syllables = map(lambda line: len(line.split()), lines)
        #     avg_length = np.average(syllables)

        #     # TODO: this doesn't work.
        #     print X[i]
        #     X[i] = np.append(X[i],avg_length)

        km = KMeans(n_clusters=50)
        km.fit(X)

        for (i,label) in enumerate(km.labels_):
            self.artists[i].label = label
#!/usr/bin/env python

import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import cmudict
from curses.ascii import isdigit

class Cluster(object):
    def __init__(self,artists):
        self.artists = artists

    def cluster(self):
        d = cmudict.dict()

        data = map(lambda artist: artist.all_songs_text(), self.artists)

        vectorizer = CountVectorizer(ngram_range=(1,2),stop_words='english',max_features=10**4)
        X = vectorizer.fit_transform(data)

        Y = np.zeros((len(data),1))
        for (i,artist) in enumerate(self.artists):
            lines = artist.all_songs_lines()
            
            syllable_lengths = []
            
            for line in lines:
                num_syllables = 0
                for word in line.split():
                    if word.lower() in d:
                        syllable_list = [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
                        num_syllables += syllable_list[0]
                syllable_lengths.append(num_syllables)
        
            if len(syllable_lengths) > 0:
                avg_syllables = np.average(syllable_lengths)
            else:
                avg_syllables = 0.0


            Y[i] = avg_syllables

        # convert Y to a sparse matrix
        Y = sparse.coo_matrix(Y)

        V = sparse.hstack((X,Y))

        km = KMeans(n_clusters=50)
        km.fit(V)

        for (i,label) in enumerate(km.labels_):
            self.artists[i].label = label
#!/usr/bin/env python

import numpy as np
import re
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
        counts_vector = vectorizer.fit_transform(data)

        """
        Count the average number of syllables per line in the artist's music
        """
        syllables_vector = np.zeros((len(data),1))
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


            syllables_vector[i] = avg_syllables
        
        # convert syllables_vector to a sparse matrix
        syllables_vector = sparse.coo_matrix(syllables_vector)

        """
        Detect drawn-out words
        """
        drawn_vector = np.zeros((len(data),1))
        for (i,artist) in enumerate(self.artists):
            lyrics = artist.all_songs_text()

            pattern = r"([a-z])\1\1+"
            prog = re.compile(pattern)
            result = prog.findall(lyrics)
            drawn_vector[i] = len(result)

        # convert drawn_vector to a sparse matrix
        drawn_vector = sparse.coo_matrix(drawn_vector)

        """
        Detect parenthesis (indicating background music)
        """
        parens_vector = np.zeros((len(data),1))
        for (i,artist) in enumerate(self.artists):
            lyrics = artist.all_songs_text()

            pattern = r"\([^)]+?\)"
            prog = re.compile(pattern)
            result = prog.findall(lyrics)
            parens_vector[i] = len(result)

        # convert parens_vector to a sparse matrix
        parens_vector = sparse.coo_matrix(parens_vector)

        V = sparse.hstack((counts_vector,syllables_vector,drawn_vector,parens_vector))

        km = KMeans(n_clusters=50)
        km.fit(V)

        for (i,label) in enumerate(km.labels_):
            self.artists[i].label = label
#!/usr/bin/env python

import numpy as np
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

class Song(object):
    def __init__(self,path,artist,title):
        self.path = path
        self.artist = artist
        self.title = title

        with open(self.path,"r") as f:
            self.lyrics = f.readlines()

    def __repr__(self):
        return "<Song: artist=%r, title=%r, path=%r>" % (self.artist, self.title, self.path)

ROOT = 'lyrics/'

corpus = []

for (dirpath, dirnames, filenames) in os.walk(ROOT):
    for filename in filenames:
        artist = dirpath.split("/")[-1]
        title = filename.split(".")[0]

        path = os.path.join(dirpath,filename)
        corpus.append(Song(path,artist,title))

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(map(lambda song: "".join(song.lyrics), corpus))

km = KMeans(n_clusters=2)
km.fit(X)

print km.labels_
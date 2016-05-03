#!/usr/bin/env python

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

from song import Song


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(map(lambda song: "".join(song.lyrics), corpus))

km = KMeans(n_clusters=2)
km.fit(X)

for (i,label) in enumerate(km.labels_):
    print corpus[i], label
#!/usr/bin/env python
import sys,json,os,pickle
import numpy as np
from marble import Marble
from main import main
from collections import defaultdict

from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

class KMeansMarble(Marble):
    """
    MLPMarble inherits from Marble and controls the training and testing of the MLP classifier. 
    """
    def __init__(self,conf,mode="train",verbose=False,max_artists=sys.maxint):
        # initialize the superclass
        Marble.__init__(self,conf,mode,verbose,max_artists)

        self.kmeans = KMeans(n_clusters=conf["kmeans"]["num_clusters"])

    def train(self):
        """
        Train the KMeansMarble algorithm
        Then, calculate predictions and print the statistics.
        """

        # fit the kmeans model
        self.kmeans.fit(self.m_features)

        # label the artists
        for (i,label) in enumerate(self.kmeans.labels_):
            self.artists[i].label = label 

	label_to_artist_ids = defaultdict(lambda: [])

	# construct the hash
	for artist in self.artists:
	    label_to_artist_ids[artist.label].append(artist._id)

	# and determine which artists are predicted
	for artist in self.artists:
	    predicted_artists = label_to_artist_ids[artist.label][:]

	    # remove this artist from the cluster
	    predicted_artists.remove(artist._id)

	    artist.predicted_similar = predicted_artists

	# finally, calculate the statistics
        self.calc_stats()


    def test(self):
        """
        No testing for KMeans
        """
        sys.stderr.write("KMeans is an unsupervised training algorithm, therefore no testing framework has been implemented\n")

if __name__ == '__main__':
    main(KMeansMarble)

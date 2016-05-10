#!/usr/bin/env python
import sys,json
import numpy as np 
from marble import Marble
from util import progress
from optparse import OptionParser

from sklearn.neighbors import NearestNeighbors

class EMMarble(Marble):
    def __init__(self,root,conf,verbose=False,max_artists=sys.maxint):
        # initialize the superclass
        Marble.__init__(self,root,conf,verbose,max_artists)

        self.initialize_weights()
        self.em_iter = conf["em_iter"]

        self.neigh = NearestNeighbors(n_neighbors=conf["neighbors"],metric=conf["metric"])
        
    def initialize_weights(self):
        sys.stderr.write("Initializing weights...")
        self.weights = np.ones(self.m_features.shape[1])
        sys.stderr.write("\n")


    def calc_x(self):
        X = np.zeros(self.m_features.shape)

        for artist_num in xrange(self.m_features.shape[0]):
            X[artist_num] = np.multiply(self.m_features[artist_num],self.weights)

        return X

    def np_divide(self,x,y):
        res = np.zeros(x.shape)
        for i in xrange(len(x)):
            res[i] = (x[i] / y[i] if y[i] > 0.0 else 0.0)
        return res

    def update_weights(self,X):

        sys.stderr.write("\tUpdating weights...")

        LAMBDA = 0.01

        for (i,artist) in enumerate(self.artists):
            progress(i)
            
            if len(artist.correct_similar) == 0:
                continue

            # this artist's features and current x vector
            features = self.m_features[artist._id]
            current_x = X[artist._id]

            # calculate the average x vector for similar artists
            avg_simil = np.average([X[simil_id] for simil_id in artist.correct_similar],axis=0)

            # determine ideal weights for this artist
            better_weights = self.np_divide(avg_simil,features)

            # and adjust self.weights by LAMBDA * (better_weights - self.weights)
            diff = np.subtract(better_weights,self.weights)
            adjust_by = np.multiply(diff,LAMBDA)
            self.weights = np.add(self.weights, adjust_by)

        sys.stderr.write("\n")

    def find_neighbors(self,X):
        sys.stderr.write("\tFinding nearest neighbors...")
        for i in xrange(len(X)):
            progress(i)
            (_,ind) = self.neigh.kneighbors(X[i].reshape(1,-1))
            self.artists[i].predicted_similar = ind[0]
        sys.stderr.write("\n")

    def train(self):
        for i in xrange(self.em_iter):
            sys.stderr.write("EM Iteration " + str(i + 1) + "\n")

            X = self.calc_x()
            sys.stderr.write("\tFitting X...")
            self.neigh.fit(X)
            sys.stderr.write("\n")

            self.find_neighbors(X)
            self.update_weights(X)

            self.calc_stats()

    def test(self):
        pass


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-l", "--lyrics", dest="lyrics_root",
                      help="where are the lyrics files located?", default="lyrics/")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")
    parser.add_option("-a", "--artists", dest="max_artists", type='int', default=sys.maxint,
                      help="number of artists to run")
    parser.add_option("-c", "--conf", dest="conf", default="conf/em.json",
            help="location of the em json config file, specifying model parameters")

    (options, args) = parser.parse_args()

    # open and parse the config file
    with open(options.conf) as f:
        conf = json.load(f)
        sys.stderr.write("Using parameters: " + str(conf) + "\n")

        d = EMMarble(options.lyrics_root,conf,verbose=options.verbose,max_artists=options.max_artists)
        d.train()

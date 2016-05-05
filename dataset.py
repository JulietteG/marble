import sys,os
import numpy as np

from artist import Artist
from utils import progress
from similarity import Similarity
from marble_exceptions import NoArtistWithNameError
from sklearn import cross_validation
from kneighbors import KNeighbors
from features import FeatureExtractor

class Dataset(object):
    def __init__(self,root):
        self.load_artists(root)

        self.load_sim_db()
        self.process_gold_standard()

        self.extractor = FeatureExtractor()
        self.extract_features()

        self.kn = KNeighbors()
        self.initialize_weights()

    def load_artists(self,root):
        sys.stderr.write("Loading artists...")

        self.artists = []
        self.id_to_artist = {}

        _id = 1
        for (dirpath, dirnames, filenames) in os.walk(root):
            if dirpath != root:
                progress(_id)

                artist = Artist(_id,dirpath)
                self.artists.append(artist)
                self.id_to_artist[_id] = artist

                _id += 1

        sys.stderr.write("\n")

    def initialize_weights(self):
        self.weights = np.ones(self.m_features.shape[1])

    def load_sim_db(self):
        sys.stderr.write("Loading similarity database...")
        self.sim = Similarity(self.artists)

        # remove artists not in the similarity database
        self.artists = filter(lambda artist: artist.in_sim_db,self.artists)

        sys.stderr.write("\n")

    def process_gold_standard(self):
        sys.stderr.write("Processing gold standard...")

        # set correct_similar for all artists
        for (i,artist) in enumerate(self.artists):
            progress(i)
            try:
                artist.correct_similar = self.sim.who_is_similar_to(artist)
            except NoArtistWithNameError, e:
                continue

        sys.stderr.write("\n")

    def extract_features(self):
        sys.stderr.write("Extracting features...")
        self.m_features = self.extractor.extract(self.artists)
        sys.stderr.write("\n")

    def calc_x(self):
        X = np.zeros(self.m_features.shape)

        for artist_num in xrange(self.m_features.shape[0]):
            for feature_num in xrange(self.m_features.shape[1]):
                X[artist_num,feature_num] = self.m_features[artist_num,feature_num] * self.weights[feature_num]

        return X
        
    def calc_stats(self):

        sys.stderr.write("Calculating statistics...\n")

        num_correct,gold,precision,recall = [],[],[],[]
        for artist in self.artists:
            num_correct.append(artist.num_correct(self.id_to_artist))
            # precision.append(artist.precision())
            # recall.append(artist.recall())
            # gold.append(len(artist.correct_similar))

        print "correct:", sum(num_correct)
        # print "total gold:", sum(gold)
        # print "avg precision:", np.average(precision)
        # print "avg recall:", np.average(recall)

    def find_neighbors(self,X):
        sys.stderr.write("Finding nearest neighbors...")
        for i in xrange(len(X)):
            progress(i)
            (_,ind) = self.kn.neighbors(X[i].reshape(1,-1))
            self.artists[i].predicted_similar = ind[0]
        sys.stderr.write("\n")

    def run(self):

        X = self.calc_x()
        sys.stderr.write("Fitting X...")
        self.kn.fit(self.X)
        sys.stderr.write("\n")

        self.find_neighbors(self.X)

        self.calc_stats()

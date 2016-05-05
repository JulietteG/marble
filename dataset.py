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

        for (i, (dirpath, dirnames, filenames)) in enumerate(os.walk(root)):
            if dirpath != root:
                progress(i)
                artist = Artist(dirpath)
                self.artists.append(artist)

        sys.stderr.write("\n")

    def initialize_weights(self):
        sys.stderr.write("Initializing weights...")
        self.weights = np.ones(self.m_features.shape[1])
        sys.stderr.write("\n")

    def load_sim_db(self):
        sys.stderr.write("Loading similarity database...")

        # set up sim db
        self.sim = Similarity(self.artists)

        # figure out who is in the database
        self.artists = self.sim.whos_in_db()

        # set the artist ids, finish loading the sim db
        self.set_artist_ids()
        self.sim.load()

        sys.stderr.write("\n")

    def set_artist_ids(self):
        self.id_to_artist = {}

        _id = 0
        for artist in self.artists:
            self.id_to_artist[_id] = artist
            artist._id = _id
            _id += 1

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
        self.m_features = self.extractor.extract(self.artists).toarray()
        sys.stderr.write("\n")

    def calc_x(self):
        X = np.zeros(self.m_features.shape)

        for artist_num in xrange(self.m_features.shape[0]):
            X[artist_num] = np.multiply(self.m_features[artist_num],self.weights)

        return X

    def update_weights(self,X):

        sys.stderr.write("Updating weights...")

        LAMBDA = 0.001

        for (i,artist) in enumerate(self.artists):
            progress(i)
            
            if len(artist.correct_similar) == 0:
                continue

            import pdb; pdb.set_trace()
            # this artist's features and current x vector
            features = self.m_features[artist._id]
            current_x = X[artist._id]

            # calculate the average of similar artist x vectors
            avg_simil_x = np.average([X[simil_id] for simil_id in artist.correct_similar], axis=0)

            # calc ideal weights for this artist
            perfect_weights = np.divide(avg_simil_x,current_x)
            adjust_by = np.multiply(perfect_weights,LAMBDA)
            self.weights = np.sum(self.weights, adjust_by)

        sys.stderr.write("\n")


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

    def run(self,num_iter):

        for i in xrange(num_iter):
            sys.stderr.write("EM Iteration " + str(i + 1) + "\n")

            X = self.calc_x()
            sys.stderr.write("Fitting X...")
            self.kn.fit(X)
            sys.stderr.write("\n")

            self.find_neighbors(X)
            self.update_weights(X)

        self.calc_stats()

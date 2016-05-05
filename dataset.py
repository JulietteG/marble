import sys,os
import numpy as np

from artist import Artist
from utils import progress
from similarity import Similarity
from marble_exceptions import NoArtistWithNameError
from sklearn import cross_validation
from kneighbors import KNeighbors
from features import FeatureExtractor

from split import Split

class Dataset(object):
    def __init__(self,root):
        self.load_artists(root)
        self.initialize_weights()

        self.load_sim_db()
        self.process_gold_standard()

        self.extractor = FeatureExtractor()
        self.kn = KNeighbors()

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
        self.weights = np.ones(len(self.artists))

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
        X = self.extractor.extract(self.artists)
        sys.stderr.write("\n")

        return X

    def construct_target(self):
        sys.stderr.write("Constructing target...")
        y = np.zeros((len(self.artists),100))

        for (i,artist) in enumerate(self.artists):
            for (j,simil_id) in enumerate(artist.correct_similar):
                y[i][j] = simil_id

        # sort similar artist ids in increasing order
        y = np.sort(y)
        sys.stderr.write("\n")

        return y

    def split_artists(self,X,y):
        sys.stderr.write("Splitting data into train / test sets...")
        artist_indices = range(len(X))
        
        # split the indices in half using train_test_split
        train,test = cross_validation.train_test_split(artist_indices,test_size=0.5)

        # calculate new X arrays
        self.X_train = np.take(X,train,axis=0)
        self.X_test = np.take(X,test,axis=0)

        # calculate new y arrays
        self.y_train = np.take(y,train,axis=0)
        self.y_test = np.take(y,test,axis=0)

        # filter out unused similar artists in self.y_train
        for i in xrange(len(self.y_train)):
            for j in xrange(len(self.y_train[i])):
                if self.y_train[i][j] not in train:
                    self.y_train[i][j] = 0

        # filter out unused similar artists in self.y_test
        for i in xrange(len(self.y_test)):
            for j in xrange(len(self.y_test[i])):
                if self.y_test[i][j] not in test:
                    self.y_test[i][j] = 0

        # and sort all y arrays
        np.sort(self.y_train)
        np.sort(self.y_test)

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

    def run(self):
        self.X = self.extract_features().toarray()
        self.y = self.construct_target()

        self.split_artists(self.X,self.y)

        sys.stderr.write("Fitting X...")
        self.kn.fit(self.X)
        sys.stderr.write("\n")

        self.find_neighbors(self.X)

        self.calc_stats()

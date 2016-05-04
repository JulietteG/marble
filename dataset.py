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
        self.kn = KNeighbors()

    def load_artists(self,root):
        sys.stderr.write("Loading artists...")

        self.artists = []
        _id = 1
        for (dirpath, dirnames, filenames) in os.walk(root):
            if dirpath != root:
                progress(_id)
                self.artists.append(Artist(_id,dirpath))
                _id += 1

        sys.stderr.write("\n")

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
            for (j,simil) in enumerate(artist.correct_similar):
                y[i][j] = simil._id

        # sort similar artist ids in increasing order
        y = np.sort(y)
        sys.stderr.write("\n")

        return y

    def split_artists(self,X,y):
        return cross_validation.train_test_split(X, y, test_size=0.5, random_state=0)

    def run(self):
        X = self.extract_features()
        y = self.construct_target()

        self.X_train, self.X_test, self.y_train, self.y_test = self.split_artists(X,y)

        sys.stderr.write("Training KNeighbors...")
        self.kn.train(self.X_train,self.y_train)
        sys.stderr.write("\n")

        sys.stderr.write("Predicting for test set...")
        y_predicted = self.kn.test(self.X_test)
        sys.stderr.write("\n")

        print "distance", distance(y_predicted,self.y_test)

    def calc_stats(self):
        sys.stderr.write("Calculating statistics...\n")

        num_correct,gold,precision,recall = [],[],[],[]
        for artist in self.artists:
            num_correct.append(artist.num_correct())
            precision.append(artist.precision())
            recall.append(artist.recall())
            gold.append(len(artist.correct_similar))

        print "correct:", sum(num_correct)
        print "total gold:", sum(gold)
        print "avg precision:", np.average(precision)
        print "avg recall:", np.average(recall)

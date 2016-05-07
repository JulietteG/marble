import sys,os,random
import numpy as np

from similarity import Similarity
from features import FeatureExtractor
from pca import pca
from models import Artist
from util import progress,NoArtistWithNameError

from sklearn.neighbors import NearestNeighbors
from sklearn.neural_network import MLPClassifier

class Marble(object):
    def __init__(self,root,verbose=False,max_artists=sys.maxint,pca_components=100):
        self.verbose = verbose

        self.load_artists(root,max_artists)
        self.load_sim()

        self.construct_target()
        self.extract_features()
        
        # perform PCA if requesting less components than the feature vector currently contains
        if pca_components < self.m_features.shape[1]:
            # using the pca method from pca.py
            self.m_features = pca(self.m_features,n_components=pca_components)

        self.neigh = NearestNeighbors(n_neighbors=num_neighbors,metric="minkowski")
        self.clf = MLPClassifier(hidden_layer_sizes=(100,),max_iter=1000)

    def load_artists(self,root,max_artists=sys.maxint):
        sys.stderr.write("Loading artists...")

        self.artists = []

        for (i,(dirpath, dirnames, filenames)) in enumerate(os.walk(root)):

            if dirpath != root:
                progress(i)
                artist = Artist(dirpath)

                self.artists.append(artist)

        sys.stderr.write("\n")

        # select a random sample of the artists we've loaded
        if len(self.artists) > max_artists:
            sys.stderr.write("Selecting random sample of " + str(max_artists) + " artists...\n")
            self.artists = random.sample(self.artists,max_artists)

    def _set_artist_ids(self):
        self.id_to_artist = {}

        _id = 0
        for artist in self.artists:
            self.id_to_artist[_id] = artist
            artist._id = _id
            _id += 1

    def load_sim(self):
        sys.stderr.write("Loading similarity database...")

        # set up sim db
        self.sim = Similarity(self.artists)

        # figure out who is in the database
        self.artists = self.sim.whos_in_db()

        # set the artist ids, finish loading the sim db
        self._set_artist_ids()
        self.sim.load()

        sys.stderr.write("\n")

    def _process_gold_standard(self):
        # set correct_similar for all artists
        for (i,artist) in enumerate(self.artists):
            try:
                artist.correct_similar = self.sim.who_is_similar_to(artist)
            except NoArtistWithNameError, e:
                continue

    def construct_target(self):
        # first process the gold standard
        self._process_gold_standard()

        # and then construct the y target matrix
        self.target = np.zeros((len(self.artists),len(self.artists)))
        for artist in self.artists:
            for simil_id in artist.correct_similar:
                self.target[artist._id,simil_id] = 1

    def extract_features(self):
        sys.stderr.write("Extracting features...")
        extractor = FeatureExtractor()
        self.m_features = extractor.extract(self.artists).toarray()
        sys.stderr.write("\n")

    def calc_stats(self):

        sys.stderr.write("Calculating statistics...\n")

        num_correct,gold,precision,recall = [],[],[],[]
        for artist in self.artists:
            num_correct.append(artist.num_correct(self.id_to_artist,verbose=self.verbose))
            # precision.append(artist.precision())
            # recall.append(artist.recall())
            gold.append(len(artist.correct_similar))

        print "\tCorrect:", sum(num_correct), "/", sum(gold)
        # print "avg precision:", np.average(precision)
        # print "avg recall:", np.average(recall)

    def find_neighbors(self,X):
        sys.stderr.write("\tFinding nearest neighbors...")
        for i in xrange(len(X)):
            progress(i)
            (_,ind) = self.neigh.kneighbors(X[i].reshape(1,-1))
            self.artists[i].predicted_similar = ind[0]
        sys.stderr.write("\n")

    def run(self,num_iter):
        sys.stderr.write("Training Multi-layer Perceptron classifier...")
        self.clf.fit(self.m_features,self.target)
        sys.stderr.write("\n")

        sys.stderr.write("Calculating MLP Predictions...")
        for artist in self.artists:
            predicted_similar = self.clf.predict(self.m_features[artist._id].reshape(1,-1))
            for i,yes in enumerate(predicted_similar[0]):
                if yes == 1:
                    artist.predicted_similar.append(i)
        sys.stderr.write("\n")
        
        self.calc_stats()

import sys,os,random
import numpy as np
from exceptions import NotImplementedError

from similarity import Similarity
from features import FeatureExtractor
from models import Artist
from util import progress,NoArtistWithNameError

class Marble(object):
    """
    Marble is the superclass for all training / testing scripts and includes the following
    functionality:

    - load_artists: load the artists and their lyrics from file
    - load_sim: load the similarity relationships between artists
    - process_gold_standard: label artists in the gold standard from the similarity database
    - construct_target: construct the target matrix used in MLP classification
    - extract_features: extract the features for the artists
    - calc_stats: calculate statistics on the predicted results
    """
    def __init__(self,conf,mode,verbose=False,max_artists=sys.maxint):
        self.conf = conf 
        self.mode = mode 
        self.verbose = verbose

        self.load_artists(max_artists)
        self.load_sim()
        
        # always process the gold standard
        self.process_gold_standard()

        # only construct a target if we're training
        if self.mode == "train":
            self.construct_target()
        
        # and always extract the features
        self.extract_features()

    def load_artists(self,max_artists=sys.maxint):
        """
        Load the artists and their lyrics from the corresponding files
        """
        sys.stderr.write("Loading artists...")

        self.artists = []
        
        # grab the lyrics root from the conf dictionary
        root = self.conf["lyrics_root"][self.mode]

        # iterate through the lyrics root
        for (i,(dirpath, dirnames, filenames)) in enumerate(os.walk(root)):

            if dirpath != root:
                progress(i)

                #construct the artist and append it to the list
                artist = Artist(dirpath)
                self.artists.append(artist)

        sys.stderr.write("\n")

        # select a random sample of the artists we've loaded
        if len(self.artists) > max_artists:
            sys.stderr.write("Selecting random sample of " + str(max_artists) + " artists...\n")
            self.artists = random.sample(self.artists,max_artists)

    def _set_artist_ids(self):
        """
        Set the artist ids incrementally, after the artists have been filtered.
        """
        self.id_to_artist = {}

        _id = 0
        for artist in self.artists:
            self.id_to_artist[_id] = artist
            artist._id = _id
            _id += 1

    def load_sim(self):
        """
        Load artist similarity relationships from the database
        """
        sys.stderr.write("Loading similarity database...")

        # set up sim db
        self.sim = Similarity(self.conf,self.artists)

        # figure out who is in the database
        self.artists = self.sim.whos_in_db()

        # set the artist ids, finish loading the sim db
        self._set_artist_ids()
        self.sim.load()

        sys.stderr.write("\n")

    def process_gold_standard(self):
        """
        Set the correct similar relationship for all artists
        """
        # set correct_similar for all artists
        for (i,artist) in enumerate(self.artists):
            try:
                artist.correct_similar = self.sim.who_is_similar_to(artist)
            except NoArtistWithNameError, e:
                continue

    def construct_target(self):
        """
        Construct the target matrix used in MLP classification
        """
        # and then construct the y target matrix
        self.target = np.zeros((len(self.artists),len(self.artists)))
        for artist in self.artists:
            for simil_id in artist.correct_similar:
                self.target[artist._id,simil_id] = 1

    def extract_features(self):
        """
        Extract features from the artists in the dataset
        """
        extractor = FeatureExtractor(self.conf,self.mode)
        self.m_features = extractor.extract(self.artists)

    def calc_stats(self):
        """
        Calculate statistics based on the predicted similarity relationships
        """

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

    def train(self):
        raise NotImplementedError("Marble.train must be overriden in subclass")

    def test(self):
        raise NotImplementedError("Marble.test must be overriden in subclass")

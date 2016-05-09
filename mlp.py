#!/usr/bin/env python
import sys,json,os,pickle
import numpy as np
from marble import Marble
from optparse import OptionParser

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import NearestNeighbors

class MLPMarble(Marble):
    """
    MLPMarble inherits from Marble and controls the training and testing of the MLP classifier. 
    """
    def __init__(self,conf,mode="train",verbose=False,max_artists=sys.maxint):
        # initialize the superclass
        Marble.__init__(self,conf,mode,verbose,max_artists)

        self.clf = MLPClassifier(hidden_layer_sizes=tuple(self.conf["mlp"]["hidden_layer_sizes"]),max_iter=self.conf["mlp"]["max_iter"])
        self.neigh = NearestNeighbors(n_neighbors=self.conf["mlp"]["neighbors"],metric=self.conf["mlp"]["metric"])

    def train(self):
        """
        Train the Multi-Layer Perceptron Classifier on the dataset
        Then, calculate predictions and print the statistics.
        """
        sys.stderr.write("Training Multi-layer Perceptron classifier...")
        self.clf.fit(self.m_features,self.target)
        sys.stderr.write("\n")
        
        # save the trained model to file
        with open(os.path.join(self.conf["paths"]["dir"],self.conf["paths"]["mlp"]),"w") as f:
            pickle.dump(self.clf,f)
        
        sys.stderr.write("Calculating MLP Predictions...")
        for artist in self.artists:
            # predict the similarities
            predicted_similar = self.clf.predict(self.m_features[artist._id].reshape(1,-1))
            
            # and convert to the appropriate format
            for i,yes in enumerate(predicted_similar[0]):
                if yes == 1:
                    artist.predicted_similar.append(i)
        sys.stderr.write("\n")

        self.calc_stats()


    def test(self):
        """
        Test a trained MLP model on a new test dataset.
        Load the MLP model from file, calculate the hidden layer, run nearest neighbors,
        and print statistics regarding the predicted similarity relationships.
        """
        with open(os.path.join(self.conf["paths"]["dir"],self.conf["paths"]["mlp"])) as f:
            self.clf = pickle.load(f)
        
        # grab the weights matrix from the saved clf model
        weight_m = self.clf.coefs_[0]

        artist_vectors = []
        for i in xrange(len(self.artists)):
            
            # calculate the hidden layer for artist i
            feature_v = self.m_features[i]
            artist_v = np.dot(weight_m,feature_v)
            artist_vectors.append(artist_v)

        self.neigh.fit(artist_vectors)

        # run kneighbors and store the results in predicted_similar
        for (i,artist_v) in enumerate(artist_vectors):
            (_,ind) = self.neigh.kneighbors(artist_v.reshape(1,-1))
            self.artists[i].predicted_similar = ind[0]

        self.calc_stats()

if __name__ == '__main__':

    parser = OptionParser(usage="usage: prog <train|test> [options]")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")
    parser.add_option("-a", "--artists", dest="max_artists", type='int', default=sys.maxint,
                      help="number of artists to run")
    parser.add_option("-c", "--conf", dest="conf", default="conf.json",
            help="location of the mlp json config file, specifying model parameters")

    (options, args) = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    else:
        # train | test
        mode = sys.argv[1]

        # make sure it's either train | test
        if mode != "train" and mode != "test":
            parser.print_help()
            sys.exit(1)

        sys.stderr.write("mode = " + mode + "\n")
    
    # open and parse the config file
    with open(options.conf) as f:
        conf = json.load(f)
        sys.stderr.write("Using parameters: " + str(conf) + "\n")

        # construct the marble
        d = MLPMarble(conf,mode,verbose=options.verbose,max_artists=options.max_artists)
        
        # test / train as appropriate
        if mode == "train":
            d.train()
        else:
            d.test()


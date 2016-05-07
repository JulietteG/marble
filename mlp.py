#!/usr/bin/env python
import sys,json
from marble import Marble
from optparse import OptionParser

from sklearn.neural_network import MLPClassifier

class MLPMarble(Marble):
    def __init__(self,root,conf,verbose=False,max_artists=sys.maxint):
        # initialize the superclass
        Marble.__init__(self,root,conf,verbose,max_artists)

        self.clf = MLPClassifier(hidden_layer_sizes=tuple(conf["hidden_layer_sizes"]),max_iter=conf["max_iter"])

    def train(self):
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
    parser.add_option("-c", "--conf", dest="conf", default="conf/mlp.json",
            help="location of the mlp json config file, specifying model parameters")

    (options, args) = parser.parse_args()

    # open and parse the config file
    with open(options.conf) as f:
        conf = json.load(f)
        sys.stderr.write("Using parameters: " + str(conf) + "\n")

        d = MLPMarble(options.lyrics_root,conf,verbose=options.verbose,max_artists=options.max_artists)
        d.train()

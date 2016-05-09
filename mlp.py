#!/usr/bin/env python
import sys,json,os,pickle
import numpy as np
from marble import Marble
from optparse import OptionParser

from sklearn.neural_network import MLPClassifier

class MLPMarble(Marble):
    def __init__(self,conf,mode="train",verbose=False,max_artists=sys.maxint):
        # initialize the superclass
        Marble.__init__(self,conf,mode,verbose,max_artists)

        self.clf = MLPClassifier(hidden_layer_sizes=tuple(self.conf["mlp"]["hidden_layer_sizes"]),max_iter=self.conf["mlp"]["max_iter"])

    def train(self):
        sys.stderr.write("Training Multi-layer Perceptron classifier...")
        self.clf.fit(self.m_features,self.target)
        sys.stderr.write("\n")
        
        with open(os.path.join(self.conf["paths"]["dir"],self.conf["paths"]["mlp"]),"w") as f:
            pickle.dump(self.clf,f)
        
        self.predict()

    def test(self):
        with open(os.path.join(self.conf["paths"]["dir"],self.conf["paths"]["mlp"])) as f:
            self.clf = pickle.load(f)
        
        self.predict()

    def predict(self):
        sys.stderr.write("Calculating MLP Predictions...")
        for artist in self.artists:
            predicted_similar = self.clf.predict(self.m_features[artist._id].reshape(1,-1))
            for i,yes in enumerate(predicted_similar[0]):
                if yes == 1:
                    artist.predicted_similar.append(i)
        sys.stderr.write("\n")

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


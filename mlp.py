#!/usr/bin/env python
import sys,json,os
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

    parser = OptionParser(usage="usage: mlp.py <train|test> [options]")
    parser.add_option("-l", "--lyrics", dest="lyrics_root",
                      help="where are the lyrics files located?", default="lyrics/")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")
    parser.add_option("-a", "--artists", dest="max_artists", type='int', default=sys.maxint,
                      help="number of artists to run")
    parser.add_option("-c", "--conf", dest="conf", default="conf/mlp.json",
            help="location of the mlp json config file, specifying model parameters")
    parser.add_option("-f", "--filename", dest="model_name", default="out/model.mlp",
            help="location of the model file (either to write if training, or to read if testing)")

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

    # make the training directory if it does not already exist
    if mode == "train" and not os.path.isdir(os.path.dirname(options.model_name)):
        os.mkdir(os.path.dirname(options.model_name))

    # open the model file
    with open(options.model_name,("w" if mode == "train" else "r")) as model_file:
        sys.stderr.write("Model file: " + options.model_name + "\n")

        d = MLPMarble(options.lyrics_root,conf,verbose=options.verbose,max_artists=options.max_artists)
        
        if mode == "train":
            d.train(model_file)
        else:
            d.test(model_file)


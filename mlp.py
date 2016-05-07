#!/usr/bin/env python
import sys
from marble import Marble
from optparse import OptionParser

class MLPMarble(Marble):
    def __init__(self,root,verbose=False,max_artists=sys.maxint,pca_components=100):
        # initialize the superclass
        Marble.__init__(self,root,verbose,max_artists,pca_components)

        self.clf = MLPClassifier(hidden_layer_sizes=(100,),max_iter=1000)

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
    parser.add_option("-p", "--pca", dest="pca_components", type='int', default=100, help="number of PCA components")

    (options, args) = parser.parse_args()

    d = MLPMarble(options.lyrics_root,verbose=options.verbose,
        max_artists=options.max_artists, pca_components=options.pca_components)
    d.train(num_iter=options.num_iter)

#!/usr/bin/env python
import sys,json,os,pickle
import numpy as np
from marble import Marble
from main import main

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import NearestNeighbors

class MLPMarble(Marble):
    """
    MLPMarble inherits from Marble and controls the training and testing of the MLP classifier. 
    """
    def __init__(self,conf,mode="train",verbose=False,max_artists=sys.maxint):
        # initialize the superclass
        Marble.__init__(self,conf,mode,verbose,max_artists)

        self.clf = MLPClassifier(hidden_layer_sizes=tuple(self.conf["mlp"]["hidden_layer_sizes"]),max_iter=self.conf["mlp"]["max_iter"],verbose=verbose)
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
        
        # grab the weights matrix, biases from the saved clf model
        weight_m = self.clf.coefs_[0]
        hidden_bias_v = self.clf.intercepts_[0]

        import pdb; pdb.set_trace()
        artist_vectors = []
        for i in xrange(len(self.artists)):
            
            # calculate the hidden layer for artist i
            input_v = self.m_features[i]
            hidden_v = np.dot(weight_m,input_v)
            hidden_v = np.add(hidden_v,hidden_bias_v)
            artist_vectors.append(hidden_v)

        self.neigh.fit(artist_vectors)

        # run kneighbors and store the results in predicted_similar
        for (i,artist_v) in enumerate(artist_vectors):
            (_,ind) = self.neigh.kneighbors(artist_v.reshape(1,-1))
            self.artists[i].predicted_similar = ind[0]

        self.calc_stats()

if __name__ == '__main__':
    main(MLPMarble)

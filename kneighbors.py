import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from metric import distance
from features import FeatureExtractor

class KNeighbors(object):
	def __init__(self,artists):
        self.artists = artists
        self.kn = KNeighborsClassifier(n_neighbors=100,metric='pyfunc',func=distance)
        self.extractor = FeatureExtractor(self.artists)

    def construct_y(self):
    	y = np.zeros((len(self.artists),100))

    	for (i,artist) in enumerate(artists):
    		for (j,simil) in enumerate(artists.correct_similar):
    			y[i][j] = simil._id

    	# sort similar artist ids in increasing order
    	y = np.sort(y)
    	return y


    def train(self):

    	X = self.extractor.extract()
    	y = self.construct_y()

    	self.kn.fit(X,y)

    def test(self):
    	pass



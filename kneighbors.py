from sklearn.neighbors import NearestNeighbors
from metric import distance

class KNeighbors(object):
    def __init__(self):
        self.kn = NearestNeighbors(n_neighbors=3,metric="minkowski")

    def fit(self,X):
        return self.kn.fit(X)

    def neighbors(self,X):
        return self.kn.kneighbors(X)

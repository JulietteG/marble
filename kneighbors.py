from sklearn.neighbors import KNeighborsClassifier
from metric import distance

class KNeighbors(object):
    def __init__(self):
        self.kn = KNeighborsClassifier(n_neighbors=100,metric='pyfunc',func=distance)

    def train(self,X,y):
        return self.kn.fit(X,y)

    def test(self,X):
        return self.kn.predict(X)

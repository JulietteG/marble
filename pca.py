import sys
from sklearn.decomposition import PCA

def pca(X,n_components=100):
    """
    Run Principal Component Analysis to reduce the vector X
    to n_components dimensions
    """

    sys.stderr.write("Principal component analysis...")
    
    # construct, fit, and transform using the PCA
    pca = PCA(n_components=n_components)
    pca.fit(X)
    X = pca.transform(X)
    
    sys.stderr.write("\n")

    return X

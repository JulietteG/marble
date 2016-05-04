import numpy as np

# takes SORTED lists (of == len) of similarities and return the number of differences
def _distance_bw(x,y):
    i,j = 0,0
    matches = 0

    while i < len(x) and j < len(y):
        if x[i] == y[j]:
            matches += 1
            i += 1
            j += 1
        elif x[i] > y[j]:
            j += 1
        else:
            i += 1

    return len(x) - matches


def distance(x,y):
    if len(x) != len(y):
        raise ValueError("Different numbers of artists")

    # ensure that x,y similarity lists are sorted
    x = np.sort(x)
    y = np.sort(y)

    diff = 0

    for i in xrange(len(x)):
        diff += _distance_bw(x[i],y[i])

    return diff
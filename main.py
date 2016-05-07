#!/usr/bin/env python
import sys
from marble import Marble
from optparse import OptionParser

LYRICS_ROOT = 'lyrics/'

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-l", "--lyrics", dest="lyrics_root",
                      help="where are the lyrics files located?", default="lyrics/")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")
    parser.add_option("-i", "--iter", dest="num_iter", type='int', default=5,
                      help="number of e/m iterations to run")
    parser.add_option("-a", "--artists", dest="max_artists", type='int', default=sys.maxint,
                      help="number of artists to run")
    parser.add_option("-n", "--neighbors", dest="num_neighbors", type='int', default=100,
                      help="number of neighbors to find for each artist")

    (options, args) = parser.parse_args()

    d = Marble(options.lyrics_root,verbose=options.verbose,
        max_artists=options.max_artists)
    d.run(num_iter=options.num_iter)

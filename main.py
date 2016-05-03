#!/usr/bin/env python
import os
# from similarity import Similarity
# from cluster import Cluster
from artist import Artist

ROOT = 'lyrics/'

artists = []

for (dirpath, dirnames, filenames) in os.walk(ROOT):
    if dirpath != ROOT:
        artists.append(Artist(dirpath))

import pdb; pdb.set_trace()
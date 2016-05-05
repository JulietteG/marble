#!/usr/bin/env python

from dataset import Dataset

LYRICS_ROOT = 'lyrics/'

if __name__ == '__main__':
    d = Dataset(LYRICS_ROOT)
    d.run(num_iter=100)
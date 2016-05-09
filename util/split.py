#!/usr/bin/env python

import sys,os,random
from optparse import OptionParser

def split(lyrics_root, test_root, test_size=0.4):

    paths = [path for path in os.walk(lyrics_root)]

    test = random.sample(paths,int(round(test_size*float(len(paths)))))

    for (dirpath, dirnames, filenames) in test:
        if dirpath == lyrics_root:
            continue

        src = dirpath 
        dest = os.path.join(test_root, os.path.basename(dirpath))

        print src, "->", dest

        os.rename(src,dest)

if __name__ == "__main__":
    
    parser = OptionParser(usage="usage: prog <lyrics_root> <test_root> [options]")
    parser.add_option("-t", "--test-size", dest="test_size", default=0.4, type='float',
            help="size of the test set")

    (options, args) = parser.parse_args()

    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit(1)

    split(sys.argv[1],sys.argv[2],options.test_size)

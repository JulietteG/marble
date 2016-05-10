import sys,os,json
from optparse import OptionParser
from util import verify_paths
from pprint import PrettyPrinter

def main(cls):
    """
    Parse command-line arguments, construct appropriate Marble subclass,
    and either train / test the model.
    """
    parser = OptionParser(usage="usage: prog <train|test> [options]")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")
    parser.add_option("-a", "--artists", dest="max_artists", type='int', default=sys.maxint,
                      help="number of artists to run")
    parser.add_option("-c", "--conf", dest="conf", default="conf.json",
            help="location of the mlp json config file, specifying model parameters")

    (options, args) = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    else:
        # train | test
        mode = sys.argv[1]

        # make sure it's either train | test
        if mode != "train" and mode != "test":
            parser.print_help()
            sys.exit(1)

        sys.stderr.write("mode = " + mode + "\n")
    
    # open and parse the config file
    with open(options.conf) as f:
        conf = json.load(f)
        
        # construct a pretty printer
        pp = PrettyPrinter(stream=sys.stderr)
        
        # log the parameters used
        sys.stderr.write("Using parameters from " + options.conf + ":\n")
        pp.pprint(conf)

        # Verify that all paths are valid
        verify_paths(conf["paths"],mode=mode)

        # construct the marble
        d = cls(conf,mode,verbose=options.verbose,max_artists=options.max_artists)
        
        # test / train as appropriate
        if mode == "train":
            d.train()
        else:
            d.test()


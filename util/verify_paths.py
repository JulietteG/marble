import sys, os

def verify_paths(paths,mode="train"):
    """
    Verify the files/directories in the paths part of the conf hash.
    """

    # ensure that dir is a valid directory, for both training and testing
    if not os.path.isdir(paths["dir"]):
        sys.stderr.write("Error: " + paths["dir"] + " must be a valid directory.\n\tGo ahead and create it.\n")
        sys.exit(1)

    # ensure that each file exists, when testing
    if mode == "test":
        for (key,fname) in paths.items():
            if key != "dir":
                path = os.path.join(paths["dir"],fname)
                if not os.path.isfile(path):
                    sys.stderr.write("Error: " + path + " is not a file.\n\tNote that training must be performed before testing!\n")
                    sys.exit(1)

class NoArtistWithNameError(Exception):
    """
    Custom exception class to be raised when there is no artist with the 
    specified name
    """
    def __init__(self,artist):
        self.artist = artist
        Exception.__init__(self)
class Song(object):
    """
    A Song object is composed of:
        - a path (where it is located on the filesystem)
        - an artist object (who wrote the song)
        - a title
        - lyrics: an array of lyrics, line-by-line
    """
    def __init__(self,artist,path):
        self.path = path
        self.artist = artist
        self.title = self.path.split("/")[-1].split(".")[0]

        self._load_lyrics()

    def _load_lyrics(self):
        """
        Load the lyrics from file
        """
        with open(self.path,"r") as f:
            self.lyrics = map(lambda line: line.decode('ascii', 'ignore'),f.readlines())

    def __repr__(self):
        """
        Let's make sure there's a nice representation
        """
        return "<Song: artist=%r, title=%r, path=%r>" % (self.artist, self.title, self.path)

    def lyric_text(self):
        """
        join the lines and return string
        """
        return "".join(self.lyrics)
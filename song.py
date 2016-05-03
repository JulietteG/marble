class Song(object):
    def __init__(self,artist,path):
        self.path = path
        self.artist = artist
        self.title = self.path.split("/")[-1].split(".")[0]

        self._load_lyrics()

    def _load_lyrics(self):
        with open(self.path,"r") as f:
            self.lyrics = map(lambda line: line.decode('ascii', 'ignore'),f.readlines())

    def __repr__(self):
        return "<Song: artist=%r, title=%r, path=%r>" % (self.artist, self.title, self.path)
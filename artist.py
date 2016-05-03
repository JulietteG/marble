import os
from song import Song

class Artist(object):
    def __init__(self,dirpath):
        self.dirpath = dirpath
        self.name = dirpath.split("/")[-1]

        self.songs = []
        self._load_songs()

    def __repr__(self):
        return "<Artist: name=%r, dirpath=%r>" % (self.name, self.dirpath)

    def _load_songs(self):
        for (dirpath, dirnames, filenames) in os.walk(self.dirpath):
            for filename in filenames:
                song_path = os.path.join(dirpath,filename)
                self.songs.append(Song(self,song_path))

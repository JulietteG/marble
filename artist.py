import os
from song import Song

class Artist(object):
    def __init__(self,dirpath):
        self.dirpath = dirpath
        self.name = dirpath.split("/")[-1]

        self.songs = []
        self._load_songs()
        self.label = None
        self.predicted_similar = []
        self.correct_similar = []

    def __repr__(self):
        return "<Artist: name=%r, label=%r>" % (self.name, self.label)

    def _load_songs(self):
        for (dirpath, dirnames, filenames) in os.walk(self.dirpath):
            for filename in filenames:
                song_path = os.path.join(dirpath,filename)
                self.songs.append(Song(self,song_path))

    # concatenate all songs together and return the string
    def all_songs_text(self):
        return "\n".join(map(lambda song: song.lyric_text(), self.songs))

    def num_correct(self):
        # TODO: maybe catch if one isn't defined?
        num = 0
        for predicted in self.predicted_similar:
            if predicted in self.correct_similar:
                print "in", self, "correctly predicted", predicted
                num += 1
        return num
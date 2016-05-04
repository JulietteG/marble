import os
from song import Song

class Artist(object):
    def __init__(self,_id,dirpath):
        self._id = _id
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

    # return an array of the text of the songs
    def all_songs(self):
        return map(lambda song: song.lyric_text(), self.songs)

    # concatenate all songs together and return the string
    def all_songs_text(self):
        return "\n".join(self.all_songs())

    def all_songs_lines(self):
        lines = []
        for song in self.songs:
            lines += song.lyrics
        return lines

    # returns the number of true positives
    def num_correct(self):
        # TODO: maybe catch if one isn't defined?
        num = 0
        for predicted in self.predicted_similar:
            if predicted in self.correct_similar:
                print "in", self, "correctly predicted", predicted
                num += 1
        return num

    def precision(self):
        if len(self.predicted_similar) > 0:
            return float(self.num_correct()) / float(len(self.predicted_similar))
        else:
            return 1.0

    def recall(self):
        if len(self.correct_similar) > 0:
            return float(self.num_correct()) / float(len(self.correct_similar))
        else:
            return 1.0
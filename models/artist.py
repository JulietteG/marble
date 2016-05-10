import os
from song import Song

class Artist(object):
    """
    An Artist object is composed of:
        - dirpath: the directory containing the artist's songs 
        - name: the name of the artist
        - songs: an array of the Song objects that this artist wrote
        - label: used in clusering algorithms
        - correct_similar: the gold-standard similar artists
        - predicted_similar: those artists the algorithm predicts are similar 
    """
    def __init__(self,dirpath):
        self.dirpath = dirpath
        self.name = dirpath.split("/")[-1]

        self.songs = []
        self._load_songs()
        self.label = None

        self.predicted_similar = []
        self.correct_similar = []

    def __repr__(self):
        """
        Let's make sure there's a nice representation
        """
        return "<Artist: name=%r, label=%r>" % (self.name, self.label)

    def _load_songs(self):
        """
        Load all this artists songs
        """
        for (dirpath, dirnames, filenames) in os.walk(self.dirpath):
            for filename in filenames:
                song_path = os.path.join(dirpath,filename)
                self.songs.append(Song(self,song_path))

    def all_songs(self):
        """
        return an array of the text of the songs
        """
        return map(lambda song: song.lyric_text(), self.songs)

    def all_songs_text(self):
        """
        concatenate all songs together and return the string
        """
        return "\n".join(self.all_songs())

    def all_songs_lines(self):
        """
        return a concatenated array of all songs, line-by-line
        """
        lines = []
        for song in self.songs:
            lines += song.lyrics
        return lines

    def num_correct(self,id_to_artist,verbose=False):
        """
        returns the number of true positives
        """
        num = 0
        for predicted in self.predicted_similar:
            if predicted in self.correct_similar:
                if verbose:
                    print "\tin", self, "correctly predicted", id_to_artist[predicted]
                num += 1
        return num

    def precision(self):
        """
        precision for this particular artist 
        """
        if len(self.predicted_similar) > 0:
            return float(self.num_correct()) / float(len(self.predicted_similar))
        else:
            return 1.0

    def recall(self):
        """
        recall for this particular artist 
        """
        if len(self.correct_similar) > 0:
            return float(self.num_correct()) / float(len(self.correct_similar))
        else:
            return 1.0
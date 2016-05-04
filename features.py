import numpy as np
import re
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import cmudict
from curses.ascii import isdigit

class FeatureExtractor(object):
    def __init__(self,artists):
        self.artists = artists
        self._cmudict = cmudict.dict()

    def extract(self):

        # calculate the various feature sets
        v_counts = self.counts()
        v_syllables_per_line = self.syllables_per_line()
        v_syllables_per_verse = self.syllables_per_verse()
        v_drawn_out = self.drawn_out()
        v_parentheses = self.parentheses()
        v_length_words = self.length_words()
        v_slang = self.slang()
        
        # hstack features together
        return sparse.hstack((v_counts,v_syllables_per_line))

    def counts(self):
        data = map(lambda artist: artist.all_songs_text(), self.artists)
        vectorizer = CountVectorizer(ngram_range=(1,2),stop_words='english',max_features=10**4)
        return vectorizer.fit_transform(data)

    """
    Count the average number of syllables per line in the artist's music
    """
    def syllables_per_line(self):
        syllables_vector = np.zeros((len(data),1))
        for (i,artist) in enumerate(self.artists):
            lines = artist.all_songs_lines()
            
            syllable_lengths = []
            
            for line in lines:
                num_syllables = 0
                for word in line.split():
                    if word.lower() in d:
                        syllable_list = [len(list(y for y in x if y[-1].isdigit())) for x in self._cmudict[word.lower()]]
                        num_syllables += syllable_list[0]
                syllable_lengths.append(num_syllables)
        
            if len(syllable_lengths) > 0:
                avg_syllables = np.average(syllable_lengths)
            else:
                avg_syllables = 0.0


            syllables_vector[i] = avg_syllables
        
        # convert syllables_vector to a sparse matrix
        return sparse.coo_matrix(syllables_vector)

    """
    Count the average number of syllables per verse in the artist's music
    """
    def syllables_per_verse(self):
        syllables_verse_vector = np.zeros((len(data),1))
        for (i,artist) in enumerate(self.artists):
            lines = artist.all_songs_lines()
            
            syllable_verse_lengths = []
            num_syllables = 0
            
            for line in lines:
                for word in line.split():
                    if word.lower() in d:
                        syllable_list = [len(list(y for y in x if y[-1].isdigit())) for x in self._cmudict[word.lower()]]
                        num_syllables += syllable_list[0]
                if line.split() and line.split()[0] == '\n':
                    syllable_verse_lengths.append(num_syllables)
                    num_syllables = 0
        
            if len(syllable_verse_lengths) > 0:
                avg_syllables = np.average(syllable_verse_lengths)
            else:
                avg_syllables = 0.0


            syllables_verse_vector[i] = avg_syllables
        
        # convert syllables_verse_vector to a sparse matrix
        return sparse.coo_matrix(syllables_verse_vector)

    """
    Detect drawn-out words
    """
    def drawn_out(self):
        drawn_vector = np.zeros((len(data),1))
        for (i,artist) in enumerate(self.artists):
            lyrics = artist.all_songs_text()

            pattern = r"([a-z])\1\1+"
            prog = re.compile(pattern)
            result = prog.findall(lyrics)
            drawn_vector[i] = len(result)

        # convert drawn_vector to a sparse matrix
        return sparse.coo_matrix(drawn_vector)

    """
    Detect parentheses (indicating background music)
    """
    def parentheses(self):
        parens_vector = np.zeros((len(data),1))
        for (i,artist) in enumerate(self.artists):
            lyrics = artist.all_songs_text()

            pattern = r"\([^)]+?\)"
            prog = re.compile(pattern)
            result = prog.findall(lyrics)
            parens_vector[i] = len(result)

        # convert parens_vector to a sparse matrix
        return sparse.coo_matrix(parens_vector)

    """
    Count the average length (in words) of songs for each artist
    """
    def length_words(self):
        lengths_vector = np.zeros((len(data),1))
        for (i,artist) in enumerate(self.artists):
            song_lengths = []
            for song_text in artist.all_songs():
                song_lengths.append(len(song_text.split()))

            if len(song_lengths) > 0:
                lengths_vector[i] = np.average(song_lengths)
            else:
                lengths_vector[i] = 0
        
        return sparse.coo_matrix(lengths_vector)

    """
    Number of slang words in artist's songs
    """
    def slang(self):
        slang_vector = np.zeros((len(data),1))
        for (i,artist) in enumerate(self.artists):
            songs_text = artist.all_songs_text()

            pattern1 = r"\b[a-zA-Z]*\'/b"
            pattern2 = r"\b\'[a-zA-z]*/b"
            prog = re.compile(pattern)
            result = prog.findall(lyrics)
            parens_vector[i] = len(result)

        return sparse.coo_matrix(slang_vector)

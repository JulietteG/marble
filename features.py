import numpy as np
import re
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import cmudict
from curses.ascii import isdigit
from nltk.corpus import wordnet as wn

class FeatureExtractor(object):
    def __init__(self):
        self._cmudict = cmudict.dict()

        """
        Pronunciation inits
        """

        NUMBER_OF_PHONEMES = 69

        # makes a set of all phonemes
        phonemes = set()

        for keys, values in self._cmudict.iteritems():
            for value in values[0]:
                phonemes.add(value)

        # makes a dictionary of phoneme to index in phoneme array
        phoneme_dict = {}

        for i, phoneme in enumerate(phonemes):
            phoneme_dict[phoneme] = i

        """
        Wordnet inits
        """
        my_synsets = [wn.synsets('depression')[0], 
wn.synsets('love')[0], 
wn.synsets('religion')[0],
wn.synsets('violence')[0],
wn.synsets('happiness')[0],
wn.synsets('sadness')[0],
wn.synsets('nature')[0],
wn.synsets('betrayal')[0],
wn.synsets('regret')[0],
wn.synsets('death')[0],
wn.synsets('faith')[0],
wn.synsets('animal')[0],
wn.synsets('country')[0],
wn.synsets('war')[0],
wn.synsets('loss')[0],
wn.synsets('hope')[0],
wn.synsets('dream')[0],
wn.synsets('light')[0],
wn.synsets('dark')[0],
wn.synsets('loneliness')[0],
wn.synsets('home')[0],
wn.synsets('fear')[0],
wn.synsets('pain')[0],
wn.synsets('devil')[0],
wn.synsets('angel')[0],
wn.synsets('family')[0],
wn.synsets('travel')[0],
wn.synsets('hate')[0],
wn.synsets('memory')[0],
wn.synsets('distance')[0],
wn.synsets('youth')[0],
wn.synsets('bravery')[0],
wn.synsets('work')[0],
wn.synsets('poverty')[0],
wn.synsets('money')[0],
wn.synsets('beauty')[0],
wn.synsets('anger')[0],
wn.synsets('mother')[0],
wn.synsets('victory')[0],
wn.synsets('defeat')[0]]

        NUM_OF_SYNSETS = len(my_synsets)

    def extract(self,artists):

        # calculate the various feature sets
        v_counts = self.counts(artists)
        v_syllables_per_line = self.syllables_per_line(artists)
        v_syllables_per_verse = self.syllables_per_verse(artists)
        v_drawn_out = self.drawn_out(artists)
        v_parentheses = self.parentheses(artists)
        v_length_words = self.length_words(artists)
        v_slang = self.slang(artists)
        # v_pronunciation = self.pronunciation(artists)
        # v_wordnet = self.wordnet_relations(artists)
        
        # hstack features together
        return sparse.hstack((v_counts,v_syllables_per_line,v_syllables_per_verse,v_drawn_out,v_parentheses,v_length_words,v_slang))

    def counts(self,artists):
        data = map(lambda artist: artist.all_songs_text(), artists)
        vectorizer = CountVectorizer(ngram_range=(1,2),stop_words='english',max_features=10**4)
        return vectorizer.fit_transform(data)

    """
    Count the average number of syllables per line in the artist's music
    """
    def syllables_per_line(self,artists):
        syllables_vector = np.zeros((len(artists),1))
        for (i,artist) in enumerate(artists):
            lines = artist.all_songs_lines()
            
            syllable_lengths = []
            
            for line in lines:
                num_syllables = 0
                for word in line.split():
                    if word.lower() in self._cmudict:
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
    def syllables_per_verse(self,artists):
        syllables_verse_vector = np.zeros((len(artists),1))
        for (i,artist) in enumerate(artists):
            lines = artist.all_songs_lines()
            
            syllable_verse_lengths = []
            num_syllables = 0
            
            for line in lines:
                for word in line.split():
                    if word.lower() in self._cmudict:
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
    def drawn_out(self,artists):
        drawn_vector = np.zeros((len(artists),1))
        for (i,artist) in enumerate(artists):
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
    def parentheses(self,artists):
        parens_vector = np.zeros((len(artists),1))
        for (i,artist) in enumerate(artists):
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
    def length_words(self,artists):
        lengths_vector = np.zeros((len(artists),1))
        for (i,artist) in enumerate(artists):
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
    def slang(self,artists):
        slang_vector = np.zeros((len(artists),1))
        for (i,artist) in enumerate(artists):
            songs_text = artist.all_songs_text()

            # finds words with apostrophe at end or beginning
            pattern = r"(\b(\w+?)[']\B)|(\B['](\w+?)\b)"
            prog = re.compile(pattern)
            result = prog.findall(songs_text)
            slang_vector[i] = len(result)

        return sparse.coo_matrix(slang_vector)

    def pronunciation(self,artists):
        pronunciation_vector = np.zeros((len(artists),NUMBER_OF_PHONEMES))

        for (i,artist) in enumerate(artists):
            for word in artist.all_songs_text.split():
                if word in d.words():
                    for phoneme in d.dict()[word][0]:
                        index = phoneme_dict[phoneme]
                        pronunciation_vector[i][index] += 1

        return sparse.coo_matrix(pronunciation_vector)

    def wordnet_relations(self,artists):
        wordnet_vector = np.zeros((len(artists),NUMBER_OF_SYNSETS))

        for (i,artist) in enumerate(artists):
            for word in artist.all_songs_text.split():
                for j, synset in enumerate(my_synsets):
                    synword = wn.synsets(word)
                    if synword:
                        synword = synword[0]
                        wordnet_vector[i][j] += synword.path_similarity(synset)

        return sparse.coo_matrix(wordnet_vector)



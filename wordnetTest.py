from nltk.corpus import wordnet as wn
import sys

word1= wn.synsets(sys.argv[1]).hypernyms()
word2 = wn.synsets(sys.argv[2]).hypernyms()
word3 = wn.synsets(sys.argv[3]).hypernyms()

print word1
print word2
print word3

#sim12 = word1.path_similarity(word2)
#sim13 = word1.path_similarity(word3)
#sim23 = word2.path_similarity(word3)

# print word1, word2, sim12
# print word1, word3, sim13
# print word2, word3, sim23

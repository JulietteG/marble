import curses 
from curses.ascii import isdigit 
import nltk 
from nltk.corpus import cmudict 
import sys

d = cmudict.dict() 

word = sys.argv[1]
print word

syllables = [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]] 
print syllables[0]
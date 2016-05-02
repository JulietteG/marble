import sqlite3 as lite
import sys

filename = "/Users/juliettegrantham/Documents/artistsID_list.txt"

class SimilarityCalculator(object):
	def __init__(self):

		fp = open(filename, 'r')

		contents = fp.read().split('\n')

		self.artist_to_id = {}
		self.id_to_artist = {}

		for entry in contents:
			artist = entry.split('<SEP>')
			self.artist_to_id[artist[-1].lower().replace(" ", "")] = artist[0]
			self.id_to_artist[artist[0]] = artist[-1].lower().replace(" ", "")

	def who_is_similar_to(self,artist):

		with lite.connect('artist_similarity.db') as conn:
			cur = conn.cursor()

			artistName = sys.argv[1]
			artistID = self.artist_to_id[artistName]

			cur.execute("SELECT similar FROM similarity where target = \'" + artistID + "\'")

			rows = cur.fetchall()

			return map(lambda row: self.id_to_artist[row[0]], rows)

if __name__ == '__main__':
	calc = SimilarityCalculator()
	print calc.who_is_similar_to(sys.argv[1])

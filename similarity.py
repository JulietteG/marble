import sqlite3 as lite
import sys
from marble_exceptions import NoArtistWithNameError

filename = "data/unique_artists.txt"

class Similarity(object):
	def __init__(self,artist_objs):
		self.artist_objs = artist_objs

		with open(filename, 'r') as fp:
			contents = fp.read().split('\n')

		self.artist_name_to_db_id = {}
		self.db_id_to_artist_name = {}

		for entry in contents:
			artist = entry.split('<SEP>')
			self.artist_name_to_db_id[artist[-1].lower().replace(" ", "")] = artist[0]
			self.db_id_to_artist_name[artist[0]] = artist[-1].lower().replace(" ", "")

	def whos_in_db(self):
		for artist in artist_objs:
			artist.in_sim_db = (artist.name in self.artist_name_to_db_id.keys())

		self.artist_objs = filter(lambda artist: artist.in_sim_db,self.artist_objs)
		return self.artist_objs

	def load(self):
		self.artist_name_to_obj_id = {}
		self.obj_id_to_artist_name = {}
		
		if artist.in_sim_db:
			self.artist_name_to_obj_id[artist.name] = artist._id
			self.obj_id_to_artist_name[artist._id] = artist.name

	def who_is_similar_to(self,artist):
		"""
		Returns a list of object ids of artists who are similar to artist with artist_id 
		"""

		with lite.connect('data/artist_similarity.db') as conn:
			cur = conn.cursor()

			try:
				artistID = self.artist_name_to_db_id[artist.name]
			except KeyError,e:
				raise NoArtistWithNameError(artist.name)

			cur.execute("SELECT similar FROM similarity where target = \'" + artistID + "\'")

			rows = cur.fetchall()

			obj_ids = []
			for row in rows:
				try:
					_name = self.db_id_to_artist_name[row[0]]
					_obj_id = self.artist_name_to_obj_id[_name]
					obj_ids.append(_obj_id)
				except KeyError,e:
					continue

			return obj_ids
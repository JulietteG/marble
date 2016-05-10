import sqlite3 as lite
import sys
from util import NoArtistWithNameError

class Similarity(object):
    """
    The Similarity class manages the processing of the gold standard
    similarities for a given artist.
    Specifically, it uses the "artist_similarity.db" to find valid
    similarity relationships.
    """
    def __init__(self,conf,artist_objs):
    
        self.artist_objs = artist_objs
        self.sim_db_name = conf["sim_root"]["artist_similarity.db"]

        with open(conf["sim_root"]["unique_artists.txt"], 'r') as fp:
            contents = fp.read().split('\n')

        self.artist_name_to_db_id = {}
        self.db_id_to_artist_name = {}

        for entry in contents:
            artist = entry.split('<SEP>')
            self.artist_name_to_db_id[artist[-1].lower().replace(" ", "")] = artist[0]
            self.db_id_to_artist_name[artist[0]] = artist[-1].lower().replace(" ", "")

    def whos_in_db(self):
        """
        Filter artists to only include those in the database.
        """
        for artist in self.artist_objs:
            artist.in_sim_db = (artist.name in self.artist_name_to_db_id.keys())

        self.artist_objs = filter(lambda artist: artist.in_sim_db,self.artist_objs)
        return self.artist_objs

    def load(self):
        """
        Construct a bidirectional mapping between artist names and their object id's
        """
        self.artist_name_to_obj_id = {}
        self.obj_id_to_artist_name = {}
        
        for artist in self.artist_objs:
            if artist.in_sim_db:
                self.artist_name_to_obj_id[artist.name] = artist._id
                self.obj_id_to_artist_name[artist._id] = artist.name

    def who_is_similar_to(self,artist):
        """
        Returns a list of object ids of artists who are similar to artist
        """

        with lite.connect(self.sim_db_name) as conn:
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

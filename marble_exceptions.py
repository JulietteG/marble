class NoArtistWithNameError(Exception):
	def __init__(self,artist):
		self.artist = artist
		Exception.__init__(self)
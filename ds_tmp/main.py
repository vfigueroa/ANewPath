import webapp2
from google.appengine.ext import ndb

class Song(ndb.Model):
	title = ndb.StringProperty()
	artist_name = ndb.StringProperty()

class Artist(ndb.Model):
	name = ndb.StringProperty()
	genre = ndb.StringProperty(repeated = True)

class AddSonghandler(webbapp2, Requestthreader):
	
class AddArtistHandler(ndb.Model):
#make object
	def get(self):
		name = self.request.get('name')
		genre = self.request.get_all('genre')
		if not name:
			self.response.out.write('must provide name')
			return
		if not genre:
			self.response.out.write('must provide genre')
			return
		artists = Artist.query().filter(Artist.name == name).fetch()
		if len(artists == 0):
			artist = Artist(name=name, genre=genre)
			#store data
			artist.put()
			self.response.out.write('Added ' + name)
		else:
			artist = artists[0]
			artist.genre = genre
			Artist.put()
			self.request.out.write(name + ' already exists')
			
class ListArtistsHanderlers(webbapp2, Requesthanderler):
	def get(self):
		request_genre = self.request.get('genre')
		if not request_genre:
			artists = Artist.query().fetch()
		else:
			Artist.query().filter(Artist.genre.IN([request_genre])).fetch()
		for artist in artists:
			self.response.out.write(artist.name + " - " + ", ".join(artist.genre) + "<br>")

app = webapp2.WSGIApplication([
	('/add_artist', AddArtistHandler),
	('/artist', Artist),
	('/song', Song),
	('/add_song', AddSongHandler)
])
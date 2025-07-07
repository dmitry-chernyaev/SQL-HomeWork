CREATE TABLE IF NOT EXISTS genres (
	genre_id SERIAL PRIMARY KEY,
	genre_name VARCHAR(40) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS artists (
	artist_id SERIAL PRIMARY KEY,
	artist_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS GenresArtists (
	genre_id INTEGER REFERENCES genres(genre_id),
	artist_id INTEGER REFERENCES artists(artist_id),
	CONSTRAINT pk_genres_artists PRIMARY KEY (genre_id, artist_id)
);

CREATE TABLE IF NOT EXISTS albums (
	album_id SERIAL PRIMARY KEY,
	album_name VARCHAR(120) NOT NULL UNIQUE,
	album_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS AlbumsArtists (
	album_id INTEGER REFERENCES albums(album_id),
	artist_id INTEGER REFERENCES artists(artist_id),
	CONSTRAINT pk_albums_artists PRIMARY KEY(album_id, artist_id)
);

CREATE TABLE IF NOT EXISTS tracks (
	track_id SERIAL PRIMARY KEY,
	track_name VARCHAR(100) NOT NULL,
	track_duration INTERVAL NOT NULL,
	album_id INTEGER REFERENCES albums(album_id) NOT NULL
);

CREATE TABLE IF NOT EXISTS collections (
	collection_id SERIAL PRIMARY KEY,
	collection_name VARCHAR(100) NOT NULL UNIQUE,
	collection_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS CollectionsTracks (
	collection_id INTEGER REFERENCES collections(collection_id),
	track_id INTEGER REFERENCES tracks(track_id),
	CONSTRAINT pk_collections_tracks PRIMARY KEY(collection_id, track_id)
);

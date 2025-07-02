INSERT INTO artists(artist_name)
VALUES 
	('steve lacy'),
	('frank sinatra'),
	('miles davis'),
	('rihanna'),
	('lorde'),
	('britney spears'),
	('pink floyd'),
	('queen'),
	('brian may'),
	('david gilmour'),
	('bob dylan'),
	('bon iver'),
	('simon&garfunkel'),
	('frank ocean'),
	('beyonce')

	
INSERT INTO genres(genre_name)
VALUES 
	('jazz'),
	('pop'),
	('rock'),
	('folk'),
	('rnb')


INSERT INTO genresartists(genre_id, artist_id)
VALUES 
	(1, 1),
	(1, 2),
	(1, 3),
	(2, 4),
	(2, 5),
	(2, 6),
	(3, 7),
	(3, 8),
	(3, 9),
	(3, 10),
	(4, 11),
	(4, 12),
	(4, 13),
	(5, 14),
	(5, 15)



INSERT INTO albums(album_name, album_date)
VALUES 
	('gemini rights', '2022-07-14'),
	('september of my years', '1986-10-12'),
	('the new sounds', '1951-05-12'),
	('meddle', '1971-03-30'),
	('a night at the opera', '1974-04-13'),
	('back to the light', '1992-07-02')
--ON CONFLICT (album_name) DO NOTHING



INSERT INTO tracks(track_name, track_duration, album_id)
VALUES 
	('echoes', '23:29', 4),
	('san tropes', '3:43', 4),
	('''39', '3:31', 5), -- экранирование апострофа
	('Bohemian Rhapsody', '5:55', 5),
	('the dark', '2:22', 6),
	('static', '2:36', 1)
	
INSERT INTO albumsartists(album_id, artist_id)
VALUES
	(1, 1),
	(2, 2),
	(3, 3),
	(4, 7),
	(5, 8),
	(6, 9)
	
INSERT INTO collections(collection_name, collection_date)
VALUES 
	('the best rock', '1990-01-01'),
	('the best jazz', '2000-01-01'),
	('the best pop', '2022-01-01'),
	('the best folk', '1976-01-01')
	
INSERT INTO collectionstracks(collection_id, track_id)
VALUES 
	(1, 1),
	(1, 2),
	(1, 3),
	(1, 4),
	(3, 5),
	(2, 6)
	
